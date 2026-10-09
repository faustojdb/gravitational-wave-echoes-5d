#!/usr/bin/env python3
"""
Versión 2 de la búsqueda ciega de líneas tardías: H1+L1+V1 y veto de glitches
a priori (banderas CBC_CAT2 de GWOSC + veto simétrico de amplitud 6σ).
Protocolo: 5_Datos_Reales/PROTOCOLO_v2.md. Todo lo no mencionado allí es
idéntico a busqueda_lineas_tardias.py (v1), cuyas funciones se reutilizan.

Uso: python3 busqueda_lineas_tardias_v2.py [--nrep 2000]
"""
import argparse, json, os, sys, time, traceback
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from busqueda_lineas_tardias import C as C1, cargar_muestra, espectro_1hz, normalizar

C = dict(C1)
C.update(detectores=("H1", "L1", "V1"), flag="CBC_CAT2", umbral_amplitud=6.0, min_ventanas=20)


def segundos_validos(det, t_ini, t_fin, log):
    """Conjunto de segundos enteros activos en {det}_CBC_CAT2 dentro de [t_ini, t_fin]."""
    from gwpy.segments import DataQualityFlag
    f = DataQualityFlag.fetch_open_data(f"{det}_{C['flag']}", int(np.floor(t_ini)), int(np.ceil(t_fin)))
    ok = set()
    for s in f.active:
        for sec in range(int(np.floor(float(s[0]))), int(np.ceil(float(s[1])))):
            ok.add(sec)
    return ok


def ventana_valida_flags(ok, ta, tb):
    return all(sec in ok for sec in range(int(np.floor(ta)), int(np.ceil(tb))))


def analizar_evento(ev, log):
    from gwpy.timeseries import TimeSeries
    t0 = ev["gps"]
    res, vetos = {}, {}
    for det in C["detectores"]:
        try:
            ts = TimeSeries.fetch_open_data(det, t0 - C["seg"], t0 + C["seg"], sample_rate=C["fs"], cache=True)
        except Exception as e:
            log(f"  {ev['nombre']} {det}: sin datos ({type(e).__name__})"); vetos[det] = "sin datos"; continue
        if np.isnan(ts.value).any():
            log(f"  {ev['nombre']} {det}: NaN, descartado"); vetos[det] = "NaN"; continue
        try:
            ok = segundos_validos(det, t0 - C["seg"], t0 + C["seg"], log)
        except Exception as e:
            log(f"  {ev['nombre']} {det}: sin banderas ({type(e).__name__}), descartado"); vetos[det] = "sin banderas"; continue
        fs = float(ts.sample_rate.value)
        pre = ts.crop(t0 + C["psd_ini"], t0 + C["psd_fin"])
        asd = pre.asd(fftlength=C["fftlength"], overlap=C["overlap"], method="median")
        wh = ts.whiten(fftlength=C["fftlength"], overlap=C["overlap"], asd=asd).highpass(C["band"][0])
        tt, x = wh.times.value, wh.value
        det_res, det_veto = {}, {}
        for vn, (ini, dur) in C["ventanas"].items():
            ta = t0 + ini
            s = (tt >= ta) & (tt < ta + dur)
            on_flag = ventana_valida_flags(ok, ta, ta + dur)
            on_amp = bool(np.abs(x[s]).max() <= C["umbral_amplitud"])
            nA = nB = 0
            offs, toff = [], []
            for (a, b) in C["off_rangos"]:
                k = 0
                while a + (k + 1) * dur <= b:
                    sa = t0 + a + k * dur; k += 1
                    so = (tt >= sa) & (tt < sa + dur)
                    if so.sum() != s.sum():
                        continue
                    if not ventana_valida_flags(ok, sa, sa + dur):
                        nA += 1; continue
                    if np.abs(x[so]).max() > C["umbral_amplitud"]:
                        nB += 1; continue
                    _, Po = espectro_1hz(x[so], fs, C["df_out"]); offs.append(Po); toff.append(sa - t0)
            det_veto[vn] = dict(on_valida_flags=on_flag, on_valida_amplitud=on_amp, off_vetadas_A=nA, off_vetadas_B=nB, off_validas=len(offs))
            if not (on_flag and on_amp):
                log(f"  {ev['nombre']} {det} {vn}: on-source vetada (flags={on_flag}, amp={on_amp}); excluido"); continue
            if len(offs) < 2 * C["min_ventanas"]:
                log(f"  {ev['nombre']} {det} {vn}: sólo {len(offs)} off válidas (<{2*C['min_ventanas']}); excluido"); continue
            f, Pon = espectro_1hz(x[s], fs, C["df_out"])
            offs = np.array(offs); sel = (f >= C["band"][0]) & (f <= C["band"][1])
            det_res[vn] = dict(f=f[sel], on=Pon[sel], off=offs[:, sel], toff=np.array(toff))
            log(f"  {ev['nombre']} {det} {vn}: ok, off válidas={len(offs)} (vetadas A={nA}, B={nB})")
        if det_res:
            res[det] = det_res
        vetos[det] = det_veto
        del ts, wh, x
    return res, vetos


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--nrep", type=int, default=2000)
    ap.add_argument("--outdir", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "resultados_v2"))
    a = ap.parse_args()
    os.makedirs(a.outdir, exist_ok=True)
    logf = open(os.path.join(a.outdir, "log.txt"), "a")

    def log(m):
        line = f"[{time.strftime('%H:%M:%S')}] {m}"; print(line); logf.write(line + "\n"); logf.flush()

    base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resultados")
    muestra = json.load(open(os.path.join(base, "muestra.json")))["eventos"]
    log(f"v2: {len(muestra)} eventos; config: {json.dumps(C)}")
    rng = np.random.default_rng(20261009)
    por_evento, vetos_all, Zs, f_ref = {}, {}, {}, {}
    for ev in muestra:
        log(f"evento {ev['nombre']} (SNR {ev['snr']}, Mf {ev['mf']})")
        try:
            R, V = analizar_evento(ev, log)
        except Exception:
            log(traceback.format_exc()); continue
        vetos_all[ev["nombre"]] = V
        if not R:
            log(f"  {ev['nombre']}: sin detectores válidos; excluido"); continue
        Z = normalizar(R)
        por_evento[ev["nombre"]] = {}
        for vn in C["ventanas"]:
            dets = [d for d in Z if vn in Z[d]]
            if not dets:
                log(f"  {ev['nombre']} {vn}: sin detectores válidos; excluido de esta ventana"); continue
            f = Z[dets[0]][vn]["f"]; f_ref.setdefault(vn, f)
            z_on = sum(Z[d][vn]["z_on"] for d in dets)
            nmin = min(Z[d][vn]["z_nul"].shape[0] for d in dets)
            z_nul = sum(Z[d][vn]["z_nul"][:nmin] for d in dets)
            Zs.setdefault(vn, {"on": [], "nul": [], "ev": []})
            Zs[vn]["on"].append(z_on); Zs[vn]["nul"].append(z_nul); Zs[vn]["ev"].append(ev["nombre"])
            zmax_on = float(z_on.max()); fmax = float(f[int(z_on.argmax())])
            p_ev = float((z_nul.max(axis=1) >= zmax_on).mean())
            por_evento[ev["nombre"]][vn] = dict(detectores=dets, zmax_on=zmax_on, f_zmax=fmax, p_individual=p_ev, n_nulas=int(nmin),
                                                z_on_media=float(z_on.mean()), z_on_std=float(z_on.std()),
                                                z_nul_media=float(z_nul.mean()), z_nul_std=float(z_nul.std()))
            log(f"  {vn}: dets={dets} zmax_on={zmax_on:.2f} @ {fmax:.0f} Hz, p_ind={p_ev:.3f} (n_nulas={nmin}, nul std={z_nul.std():.2f})")

    resumen = dict(protocolo="PROTOCOLO_v2.md", por_evento=por_evento, vetos=vetos_all, apilado={})
    for vn in Zs:
        on = np.array(Zs[vn]["on"]); nul = Zs[vn]["nul"]; nev = len(nul)
        Zf = on.sum(axis=0); Zmax = float(Zf.max()); fZ = float(f_ref[vn][int(Zf.argmax())])
        Zmax_nul = np.empty(a.nrep)
        for r in range(a.nrep):
            acc = np.zeros_like(Zf)
            for e in range(nev):
                acc += nul[e][rng.integers(nul[e].shape[0])]
            Zmax_nul[r] = acc.max()
        p = float((Zmax_nul >= Zmax).mean()); p_corr = min(1.0, p * len(Zs)); ib = int(Zf.argmax())
        resumen["apilado"][vn] = dict(n_eventos=nev, eventos=Zs[vn]["ev"], Zmax=Zmax, f_Zmax_Hz=fZ, p=p, p_corr_bonferroni=p_corr,
                                      nula_mediana=float(np.median(Zmax_nul)), nula_p95=float(np.quantile(Zmax_nul, 0.95)),
                                      nula_p999=float(np.quantile(Zmax_nul, 0.999)), frac_eventos_z_positivo_en_fmax=float((on[:, ib] > 0).mean()),
                                      criterio_exito="p_corr < 0.001", exito=bool(p_corr < 0.001))
        np.savez(os.path.join(a.outdir, f"apilado_{vn}.npz"), f=f_ref[vn], Z=Zf, z_on=on, Zmax_nul=Zmax_nul,
                 eventos=np.array(Zs[vn]["ev"]), **{f"z_nul_{e}": nul[e] for e in range(nev)})
        log(f"APILADO {vn}: n_ev={nev} Zmax={Zmax:.2f} @ {fZ:.0f} Hz, p={p:.4f}, p_corr={p_corr:.4f}, nula mediana={np.median(Zmax_nul):.1f} p95={np.quantile(Zmax_nul,0.95):.1f} p99.9={np.quantile(Zmax_nul,0.999):.1f}")
    json.dump(resumen, open(os.path.join(a.outdir, "resumen.json"), "w"), indent=1)

    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    fig, axs = plt.subplots(len(Zs), 2, figsize=(13, 4 * len(Zs))); axs = np.atleast_2d(axs)
    for i, vn in enumerate(Zs):
        d = np.load(os.path.join(a.outdir, f"apilado_{vn}.npz")); r = resumen["apilado"][vn]
        axs[i, 0].plot(d["f"], d["Z"], lw=0.6)
        axs[i, 0].axhline(r["nula_p95"], color="C1", ls="--", label=f"nula p95 = {r['nula_p95']:.1f}")
        axs[i, 0].axhline(r["nula_p999"], color="C3", ls=":", label=f"nula p99.9 = {r['nula_p999']:.1f}")
        axs[i, 0].set_title(f"{vn} (v2, veto a priori, H1+L1+V1): {r['n_eventos']} eventos; Zmax={r['Zmax']:.1f} @ {r['f_Zmax_Hz']:.0f} Hz, p={r['p']:.3f}", fontsize=9)
        axs[i, 0].set_xlabel("f [Hz]"); axs[i, 0].set_ylabel("Z(f)"); axs[i, 0].legend(fontsize=7)
        axs[i, 1].hist(d["Zmax_nul"], bins=60, alpha=0.7, label="Zmax réplicas nulas"); axs[i, 1].axvline(r["Zmax"], color="k", label="Zmax observado")
        axs[i, 1].set_xlabel("Zmax"); axs[i, 1].legend(fontsize=7); axs[i, 1].set_title(f"{vn}: distribución nula", fontsize=9)
    fig.tight_layout(); fig.savefig(os.path.join(a.outdir, "fig_apilado.png"), dpi=140); plt.close(fig)
    fig, axs = plt.subplots(1, len(Zs), figsize=(6 * len(Zs), 3.5)); axs = np.atleast_1d(axs)
    for i, vn in enumerate(Zs):
        on = np.concatenate(Zs[vn]["on"]); nu = np.concatenate([z.ravel() for z in Zs[vn]["nul"]])
        axs[i].hist(nu, bins=100, range=(-8, 15), density=True, alpha=0.6, label=f"nulas (media {nu.mean():.2f}, std {nu.std():.2f})")
        axs[i].hist(on, bins=100, range=(-8, 15), density=True, alpha=0.6, label=f"on-source (media {on.mean():.2f}, std {on.std():.2f})")
        axs[i].set_yscale("log"); axs[i].set_xlabel("z por bin (suma sobre detectores)"); axs[i].legend(fontsize=7); axs[i].set_title(f"{vn}: control de normalización (v2)", fontsize=9)
    fig.tight_layout(); fig.savefig(os.path.join(a.outdir, "fig_control_z.png"), dpi=140); plt.close(fig)
    log("fin")


if __name__ == "__main__":
    main()
