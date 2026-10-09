#!/usr/bin/env python3
"""
ANÁLISIS EXPLORATORIO POST HOC — NO CONFIRMATORIO.

Se escribió DESPUÉS de ver el resultado del análisis pre-registrado
(busqueda_lineas_tardias.py), que fue negativo con una distribución nula
dominada por glitches en ventanas off-source (percentil 95 de Zmax nulo
≈ 10^3–10^5 frente a un Zmax observado ≈ 42).

Pregunta que responde: si se limita la influencia de los glitches con un
recorte simétrico de z (aplicado por igual a on-source y a réplicas nulas),
¿cambia la conclusión? Esto mide la SENSIBILIDAD del test, no reabre la
hipótesis: cualquier p obtenido aquí no cuenta como evidencia, porque el
recorte se eligió después de ver los datos.

Usa los arrays guardados por el análisis principal (Enmienda 3).
"""
import json, os, sys
import numpy as np

outdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), sys.argv[1] if len(sys.argv) > 1 else "resultados")
rng = np.random.default_rng(20261009)
NREP = 2000
CLIPS = [5.0, 10.0, 20.0]   # recortes de z por bin (suma sobre detectores)

res = {"advertencia": "EXPLORATORIO POST HOC. No confirmatorio. Recortes elegidos tras ver los datos.",
       "ventanas": {}}
for vn in ("W1", "W2"):
    d = np.load(os.path.join(outdir, f"apilado_{vn}.npz"), allow_pickle=True)
    f = d["f"]; on = d["z_on"]; nev = on.shape[0]
    if len(f) != on.shape[1]:
        f = f[:on.shape[1]]
    nul = [d[f"z_nul_{e}"] for e in range(nev)]
    res["ventanas"][vn] = {}
    for clip in CLIPS:
        onc = np.clip(on, -clip, clip)
        Zf = onc.sum(axis=0); Zmax = float(Zf.max()); fZ = float(f[int(Zf.argmax())])
        Zn = np.empty(NREP)
        for r in range(NREP):
            acc = np.zeros_like(Zf)
            for e in range(nev):
                acc += np.clip(nul[e][rng.integers(nul[e].shape[0])], -clip, clip)
            Zn[r] = acc.max()
        p = float((Zn >= Zmax).mean())
        # sensibilidad: cuántas sigmas (en unidades de la nula) sería necesario para p<0.001
        res["ventanas"][vn][f"clip_{clip:g}"] = dict(
            Zmax=Zmax, f_Zmax_Hz=fZ, p=p, nula_mediana=float(np.median(Zn)),
            nula_p95=float(np.quantile(Zn, 0.95)), nula_p999=float(np.quantile(Zn, 0.999)),
            umbral_deteccion_Z=float(np.quantile(Zn, 0.999)))
        print(f"{vn} clip={clip:g}: Zmax={Zmax:.1f} @ {fZ:.0f} Hz, p={p:.3f}, nula mediana={np.median(Zn):.1f}, p95={np.quantile(Zn,0.95):.1f}, p99.9={np.quantile(Zn,0.999):.1f}")
    # top-5 bins con el recorte intermedio (clip 10)
    onc = np.clip(on, -10, 10); Zf = onc.sum(axis=0)
    idx = np.argsort(Zf)[::-1][:5]
    res["ventanas"][vn]["top5_bins_clip10"] = [dict(f_Hz=float(f[i]), Z=float(Zf[i]), frac_eventos_z_pos=float((on[:, i] > 0).mean())) for i in idx]
json.dump(res, open(os.path.join(outdir, "exploratorio_posthoc.json"), "w"), indent=1)

import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
fig, axs = plt.subplots(2, 1, figsize=(12, 7))
for ax, vn in zip(axs, ("W1", "W2")):
    d = np.load(os.path.join(outdir, f"apilado_{vn}.npz"), allow_pickle=True)
    f = d["f"]; on = np.clip(d["z_on"], -10, 10); Zf = on.sum(axis=0)
    r = res["ventanas"][vn]["clip_10"]
    ax.plot(f, Zf, lw=0.6, label="Z(f) apilado, z recortado a ±10 (post hoc)")
    ax.axhline(r["nula_p95"], color="C1", ls="--", label=f"nula p95 = {r['nula_p95']:.1f}")
    ax.axhline(r["nula_p999"], color="C3", ls=":", label=f"nula p99.9 = {r['nula_p999']:.1f} (umbral de detección)")
    ax.set_title(f"{vn} — EXPLORATORIO POST HOC — Zmax={r['Zmax']:.1f} @ {r['f_Zmax_Hz']:.0f} Hz, p={r['p']:.3f}", fontsize=10)
    ax.set_xlabel("f [Hz]"); ax.set_ylabel("Z(f)"); ax.legend(fontsize=8)
fig.tight_layout(); fig.savefig(os.path.join(outdir, "fig_exploratorio_posthoc.png"), dpi=140)
print("ok")
