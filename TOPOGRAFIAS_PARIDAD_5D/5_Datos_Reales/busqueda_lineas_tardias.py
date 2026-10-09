#!/usr/bin/env python3
"""
Búsqueda ciega de líneas tardías de frecuencia fija, comunes a todos los
eventos, en strain público de LIGO (GWOSC), según 5_Datos_Reales/PROTOCOLO.md.

No asume frecuencia, modelo ni radio. Los controles off-source corren con el
mismo pipeline. Resultado positivo o negativo se reporta igual.

Uso: python3 busqueda_lineas_tardias.py [--nrep 2000] [--outdir resultados]
"""
import argparse, json, os, sys, time, traceback
import numpy as np

C = dict(
    catalogo="GWTC-3-confident",
    snr_min=10.0, far_max=1.0, m_min=3.0,
    detectores=("H1", "L1"), fs=4096,
    seg=128.0,                 # [t0-128, t0+128]
    psd_ini=-124.0, psd_fin=-8.0, fftlength=4.0, overlap=2.0,
    band=(20.0, 1800.0),
    ventanas={"W1": (0.05, 1.0), "W2": (1.05, 4.0)},   # (inicio relativo a t0, duración)
    off_rangos=((-120.0, -8.0), (8.0, 120.0)),
    df_out=1.0,
)


def cargar_muestra(path_cat):
    d = json.load(open(path_cat))["events"]
    rows = []
    for k, v in d.items():
        snr, far = v.get("network_matched_filter_snr"), v.get("far")
        m1, m2 = v.get("mass_1_source"), v.get("mass_2_source")
        if snr is None or far is None or m1 is None or m2 is None:
            continue
        if snr >= C["snr_min"] and far <= C["far_max"] and m1 > C["m_min"] and m2 > C["m_min"]:
            rows.append(dict(nombre=v["commonName"], gps=float(v["GPS"]), snr=snr, far=far,
                             m1=m1, m2=m2, mf=v.get("final_mass_source")))
    rows.sort(key=lambda r: r["gps"])
    return rows


def espectro_1hz(x, fs, df_out):
    """Potencia (Hann) re-agrupada a bins de df_out Hz. Devuelve (f_centros, P)."""
    n = len(x)
    w = np.hanning(n)
    X = np.fft.rfft(x * w)
    P = np.abs(X) ** 2 / np.sum(w ** 2)
    f = np.fft.rfftfreq(n, 1.0 / fs)
    df = f[1] - f[0]
    g = int(round(df_out / df))
    if g > 1:
        nb = len(P) // g
        P = P[:nb * g].reshape(nb, g).mean(axis=1)
        f = f[:nb * g].reshape(nb, g).mean(axis=1)
    return f, P


def analizar_evento(ev, outdir, log):
    from gwpy.timeseries import TimeSeries
    t0 = ev["gps"]
    res = {}
    for det in C["detectores"]:
        try:
            ts = TimeSeries.fetch_open_data(det, t0 - C["seg"], t0 + C["seg"], sample_rate=C["fs"], cache=True)
        except Exception as e:
            log(f"  {ev['nombre']} {det}: sin datos ({type(e).__name__}: {e})")
            continue
        if np.isnan(ts.value).any():
            log(f"  {ev['nombre']} {det}: NaN en el segmento, detector descartado")
            continue
        fs = float(ts.sample_rate.value)
        # PSD pre-fusión y blanqueo con esa PSD
        pre = ts.crop(t0 + C["psd_ini"], t0 + C["psd_fin"])
        asd = pre.asd(fftlength=C["fftlength"], overlap=C["overlap"], method="median")
        wh = ts.whiten(fftlength=C["fftlength"], overlap=C["overlap"], asd=asd)
        wh = wh.highpass(C["band"][0])  # el límite superior se aplica seleccionando bins del espectro (Enmienda 2)
        tt = wh.times.value
        x = wh.value
        det_res = {}
        for vn, (ini, dur) in C["ventanas"].items():
            # on-source
            s = (tt >= t0 + ini) & (tt < t0 + ini + dur)
            f, Pon = espectro_1hz(x[s], fs, C["df_out"])
            # off-source
            offs = []
            toff = []
            for (a, b) in C["off_rangos"]:
                k = 0
                while a + (k + 1) * dur <= b:
                    sa = t0 + a + k * dur
                    so = (tt >= sa) & (tt < sa + dur)
                    if so.sum() == s.sum():
                        _, Po = espectro_1hz(x[so], fs, C["df_out"])
                        offs.append(Po); toff.append(sa - t0)
                    k += 1
            offs = np.array(offs)
            sel = (f >= C["band"][0]) & (f <= C["band"][1])
            det_res[vn] = dict(f=f[sel], on=Pon[sel], off=offs[:, sel], toff=np.array(toff))
        res[det] = det_res
        log(f"  {ev['nombre']} {det}: ok, off W1={len(res[det]['W1']['toff'])} W2={len(res[det]['W2']['toff'])}")
        del ts, wh, x
    return res


def normalizar(R):
    """Divide off en referencia/nula (índices alternados) y calcula z para on y nulas."""
    Z = {}
    for det, dr in R.items():
        Z[det] = {}
        for vn, d in dr.items():
            off = d["off"]
            ref, nul = off[0::2], off[1::2]
            med = np.median(ref, axis=0)
            mad = np.median(np.abs(ref - med), axis=0) * 1.4826 + 1e-30
            Z[det][vn] = dict(f=d["f"], z_on=(d["on"] - med) / mad, z_nul=(nul - med) / mad)
    return Z


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--nrep", type=int, default=2000)
    ap.add_argument("--outdir", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "resultados"))
    ap.add_argument("--catalogo", default=None)
    ap.add_argument("--max_eventos", type=int, default=None)
    a = ap.parse_args()
    os.makedirs(a.outdir, exist_ok=True)
    logf = open(os.path.join(a.outdir, "log.txt"), "a")

    def log(m):
        line = f"[{time.strftime('%H:%M:%S')}] {m}"
        print(line); logf.write(line + "\n"); logf.flush()

    cat = a.catalogo or os.path.join(a.outdir, "gwtc3_confident_catalogo_gwosc_2026-10-09.json")
    muestra = cargar_muestra(cat)
    if a.max_eventos:
        muestra = muestra[:a.max_eventos]
    json.dump(dict(criterios={k: C[k] for k in ("catalogo", "snr_min", "far_max", "m_min")}, eventos=muestra),
              open(os.path.join(a.outdir, "muestra.json"), "w"), indent=1)
    log(f"muestra: {len(muestra)} eventos; config: {json.dumps(C)}")

    rng = np.random.default_rng(20261009)
    por_evento = {}
    Zs = {}
    f_ref = None
    for ev in muestra:
        log(f"evento {ev['nombre']} (SNR {ev['snr']}, Mf {ev['mf']})")
        try:
            R = analizar_evento(ev, a.outdir, log)
        except Exception:
            log(traceback.format_exc()); continue
        if not R:
            continue
        Z = normalizar(R)
        por_evento[ev["nombre"]] = {}
        for vn in C["ventanas"]:
            dets = [d for d in Z if vn in Z[d]]
            f = Z[dets[0]][vn]["f"]
            if f_ref is None:
                f_ref = f
            z_on = sum(Z[d][vn]["z_on"] for d in dets)
            nmin = min(Z[d][vn]["z_nul"].shape[0] for d in dets)
            z_nul = sum(Z[d][vn]["z_nul"][:nmin] for d in dets)  # mismo índice temporal en ambos detectores
            Zs.setdefault(vn, {"on": [], "nul": [], "dets": []})
            Zs[vn]["on"].append(z_on); Zs[vn]["nul"].append(z_nul); Zs[vn]["dets"].append(dets)
            # resultado individual
            zmax_on = float(z_on.max()); fmax_on = float(f[int(z_on.argmax())])
            zmax_nul = z_nul.max(axis=1)
            p_ev = float((zmax_nul >= zmax_on).mean())
            por_evento[ev["nombre"]][vn] = dict(detectores=dets, zmax_on=zmax_on, f_zmax=fmax_on, p_individual=p_ev,
                                                n_nulas=int(nmin), z_on_media=float(z_on.mean()), z_on_std=float(z_on.std()),
                                                z_nul_media=float(z_nul.mean()), z_nul_std=float(z_nul.std()))
            log(f"  {vn}: dets={dets} zmax_on={zmax_on:.2f} @ {fmax_on:.0f} Hz, p_ind={p_ev:.3f} (n_nulas={nmin})")

    # apilado y nula
    resumen = dict(muestra_analizada=list(por_evento), por_evento=por_evento, apilado={})
    for vn in Zs:
        on = np.array(Zs[vn]["on"]); nul = Zs[vn]["nul"]
        Zf = on.sum(axis=0)
        Zmax = float(Zf.max()); fZ = float(f_ref[int(Zf.argmax())])
        nev = len(nul)
        Zmax_nul = np.empty(a.nrep)
        for r in range(a.nrep):
            acc = np.zeros_like(Zf)
            for e in range(nev):
                acc += nul[e][rng.integers(nul[e].shape[0])]
            Zmax_nul[r] = acc.max()
        p = float((Zmax_nul >= Zmax).mean())
        p_corr = min(1.0, p * len(Zs))
        # fracción de eventos con z>0 en el bin máximo
        ib = int(Zf.argmax())
        frac_pos = float((on[:, ib] > 0).mean())
        resumen["apilado"][vn] = dict(n_eventos=nev, Zmax=Zmax, f_Zmax_Hz=fZ, p=p, p_corr_bonferroni=p_corr,
                                      nula_p95=float(np.quantile(Zmax_nul, 0.95)), nula_p999=float(np.quantile(Zmax_nul, 0.999)),
                                      nula_mediana=float(np.median(Zmax_nul)), frac_eventos_z_positivo_en_fmax=frac_pos,
                                      criterio_exito="p_corr < 0.001", exito=bool(p_corr < 0.001))
        np.savez(os.path.join(a.outdir, f"apilado_{vn}.npz"), f=f_ref, Z=Zf, z_on=on, Zmax_nul=Zmax_nul)
        log(f"APILADO {vn}: Zmax={Zmax:.2f} @ {fZ:.0f} Hz, p={p:.4f}, p_corr={p_corr:.4f}, nula p95={resumen['apilado'][vn]['nula_p95']:.2f}")
    json.dump(resumen, open(os.path.join(a.outdir, "resumen.json"), "w"), indent=1)

    # figuras
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    fig, axs = plt.subplots(len(Zs), 2, figsize=(13, 4 * len(Zs)))
    axs = np.atleast_2d(axs)
    for i, vn in enumerate(Zs):
        d = np.load(os.path.join(a.outdir, f"apilado_{vn}.npz"))
        r = resumen["apilado"][vn]
        axs[i, 0].plot(d["f"], d["Z"], lw=0.6)
        axs[i, 0].axhline(r["nula_p95"], color="C1", ls="--", label="percentil 95 de la nula (max sobre bins)")
        axs[i, 0].axhline(r["nula_p999"], color="C3", ls=":", label="percentil 99.9 de la nula")
        axs[i, 0].set_title(f"{vn}: Z(f) apilado sobre {r['n_eventos']} eventos; Zmax={r['Zmax']:.1f} @ {r['f_Zmax_Hz']:.0f} Hz, p_corr={r['p_corr_bonferroni']:.3f}", fontsize=9)
        axs[i, 0].set_xlabel("f [Hz]"); axs[i, 0].set_ylabel("Z(f) = Σ_ev Σ_det z"); axs[i, 0].legend(fontsize=7)
        axs[i, 1].hist(d["Zmax_nul"], bins=60, alpha=0.7, label="Zmax en réplicas nulas (mismo pipeline)")
        axs[i, 1].axvline(r["Zmax"], color="k", label="Zmax observado")
        axs[i, 1].set_xlabel("Zmax"); axs[i, 1].legend(fontsize=7)
        axs[i, 1].set_title(f"{vn}: distribución nula de Zmax", fontsize=9)
    fig.tight_layout(); fig.savefig(os.path.join(a.outdir, "fig_apilado.png"), dpi=140); plt.close(fig)

    # control: histogramas de z on vs nulas
    fig, axs = plt.subplots(1, len(Zs), figsize=(6 * len(Zs), 3.5))
    axs = np.atleast_1d(axs)
    for i, vn in enumerate(Zs):
        on = np.concatenate([z for z in Zs[vn]["on"]]); nu = np.concatenate([z.ravel() for z in Zs[vn]["nul"]])
        axs[i].hist(nu, bins=100, range=(-8, 12), density=True, alpha=0.6, label=f"nulas (media {nu.mean():.2f}, std {nu.std():.2f})")
        axs[i].hist(on, bins=100, range=(-8, 12), density=True, alpha=0.6, label=f"on-source (media {on.mean():.2f}, std {on.std():.2f})")
        axs[i].set_yscale("log"); axs[i].set_xlabel("z por bin (suma sobre detectores)"); axs[i].legend(fontsize=7); axs[i].set_title(f"{vn}: control de normalización", fontsize=9)
    fig.tight_layout(); fig.savefig(os.path.join(a.outdir, "fig_control_z.png"), dpi=140); plt.close(fig)
    log("fin")


if __name__ == "__main__":
    main()
