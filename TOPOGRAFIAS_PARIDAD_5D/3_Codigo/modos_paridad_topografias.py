#!/usr/bin/env python3
"""
Topografías 5D con selección de paridad par/impar en las paredes.

Calcula, para cada topografía candidata de la dimensión extra, las funciones
de modo de Kaluza-Klein (KK), el espectro de masas y el "peso" de cada modo en
los dos extremos (pared I = nuestra brana, pared II = brana sombra). Muestra
en qué topografías los modos de número KK par se anulan en una pared y los de
número impar en la otra, y qué condiciones hacen falta para ello.

Topografías tratadas
--------------------
1. S^1                    círculo liso, sin paredes
2. S^1/Z_2                intervalo con dos paredes idénticas
3. S^1/(Z_2 x Z_2')       intervalo con dos paredes DISTINTAS (Kawamura 2001;
                          Barbieri-Hall-Nomura 2001). Equivale a S^1/Z_2 con
                          fases de Scherk-Schwarz no triviales (Nilse 2006).
4. Botella de Klein R^2/pg  sin puntos fijos; paridad definida por la reflexión
                          deslizante (Nilse 2006, sec. 3.2)
5. Banda de Möbius        borde pero sin puntos fijos; torsión -> espectro
                          semientero para los modos impares en el ancho
6. Randall-Sundrum        warped: RS1 (dos branas, torre discreta de Bessel) y
                          RS2 (una brana, modo cero ligado + continuo)
7. Cuerda negra RS (Seahra-Clarkson-Maartens 2005): m_n = (z_n/l) e^{-d/l},
                          frecuencias KK vs banda LIGO.

Además se hace una simulación 1+1 (onda escalar en y) con las cuatro
combinaciones de condiciones de contorno Neumann/Dirichlet en las dos paredes,
que es el análogo exacto de las cuatro paridades (P,P') del orbifold, y se
muestra el espectro registrado en cada pared.

Uso:  python3 modos_paridad_topografias.py [--outdir ../4_Resultados]
"""
import argparse
import json
import os

import numpy as np
from scipy import special
from scipy.optimize import brentq

# ----------------------------------------------------------------------------
# utilidades
# ----------------------------------------------------------------------------

C_LIGHT = 299_792_458.0  # m/s


def peso_en_pared(f, y_pared, eps=1e-9):
    """|f(y)|^2 normalizado a 1 en el máximo del modo."""
    return abs(f(y_pared)) ** 2


# ----------------------------------------------------------------------------
# 1-3. Orbifolds unidimensionales planos
# ----------------------------------------------------------------------------

def modos_orbifold_1d(R=1.0, nmax=8):
    """
    Devuelve una lista de diccionarios con las funciones de modo y masas de
    S^1, S^1/Z_2 y S^1/(Z_2 x Z_2'), y su valor en las dos paredes.

    Convenciones (Kawamura 2001, Prog. Theor. Phys. 105, 999):
      Z_2 : y -> -y            pared I  en y = 0
      Z_2': y' -> -y', y' = y + pi R/2   pared II en y = -pi R/2 (equiv. +pi R/2)
    Longitud física del intervalo fundamental: pi R / 2.
    """
    yI, yII = 0.0, np.pi * R / 2  # usamos +pi R/2 por simetría

    sectores = []
    # --- S^1: e^{i n y / R}, |f|=1 en todas partes. Sin paredes.
    for n in range(0, nmax + 1):
        sectores.append(dict(topo="S^1", sector="(periodico)", n=n,
                             masa=n / R, en_I=1.0, en_II=1.0))
    # --- S^1/Z_2: longitud pi R; paredes en 0 y pi R.  Z2-par: cos(n y/R),
    #     Z2-impar: sin(n y/R).  Ambas paredes IDÉNTICAS.
    for n in range(0, nmax + 1):
        f_par = lambda y, n=n: np.cos(n * y / R)
        f_imp = lambda y, n=n: np.sin(n * y / R)
        sectores.append(dict(topo="S^1/Z_2", sector="(+) par", n=n, masa=n / R,
                             en_I=f_par(0.0) ** 2, en_II=f_par(np.pi * R) ** 2))
        if n > 0:
            sectores.append(dict(topo="S^1/Z_2", sector="(-) impar", n=n, masa=n / R,
                                 en_I=f_imp(0.0) ** 2, en_II=f_imp(np.pi * R) ** 2))
    # --- S^1/(Z_2 x Z_2'): cuatro sectores (P,P')
    for n in range(0, nmax + 1):
        modos = {
            "(+,+)": (lambda y, n=n: np.cos(2 * n * y / R), 2 * n / R),
            "(+,-)": (lambda y, n=n: np.cos((2 * n + 1) * y / R), (2 * n + 1) / R),
            "(-,+)": (lambda y, n=n: np.sin((2 * n + 1) * y / R), (2 * n + 1) / R),
            "(-,-)": (lambda y, n=n: np.sin((2 * n + 2) * y / R), (2 * n + 2) / R),
        }
        for sec, (f, m) in modos.items():
            sectores.append(dict(topo="S^1/(Z_2xZ_2')", sector=sec, n=n, masa=m,
                                 en_I=float(f(yI) ** 2), en_II=float(f(yII) ** 2)))
    return sectores


# ----------------------------------------------------------------------------
# 4. Botella de Klein (Nilse 2006, sec. 3.2):  z ~ z + i r,  z ~ z* + i r + 1/2
#    Base: F^(±)_{k,l}(y5,y6) ∝ e^{i2π(k y5 + l y6)} ± (-1)^k e^{i2π(k y5 - l y6)}
#    Espectro m^2 ∝ k^2 + (l/r)^2, independiente de la paridad.
#    Modos cero en y6 (l=0): F^(+)_{2k+1,0} = F^(-)_{2k,0} = 0.
# ----------------------------------------------------------------------------

def modos_klein(kmax=6, lmax=2, r=1.0):
    out = []
    for k in range(-kmax, kmax + 1):
        for l in range(0, lmax + 1):
            for p in (+1, -1):
                # amplitud del modo l=0: 1 ± (-1)^k ; para l>0 nunca se anula
                if l == 0:
                    amp = 1 + p * (-1) ** k
                else:
                    amp = 2.0  # magnitud generica (no nula)
                out.append(dict(k=k, l=l, paridad="+" if p > 0 else "-",
                                masa2=(2 * np.pi) ** 2 * (k ** 2 + (l / r) ** 2),
                                sobrevive=bool(abs(amp) > 1e-12)))
    return out


# ----------------------------------------------------------------------------
# 5. Banda de Möbius: franja y ∈ [-w, w], x ∈ R con (x, y) ~ (x + L, -y)
#    f(x+L, -y) = f(x, y).  Separando f = e^{i 2π q x / L} g(y):
#      g par en y  -> q entero
#      g impar en y -> q semientero  (torsión = fase de Scherk-Schwarz 1/2)
#    El borde |y| = w es un borde genuino (no un punto fijo): allí se impone
#    Dirichlet o Neumann por física, no por topología.
# ----------------------------------------------------------------------------

def modos_mobius(L=1.0, w=0.5, jmax=3, qmax=3, borde="neumann"):
    out = []
    for j in range(0, jmax + 1):
        for q2 in range(-2 * qmax, 2 * qmax + 1):  # 2q
            if borde == "neumann":
                # pares: cos(j π y / w) (incluye j=0); impares: sin((j+1/2)π y/w)... usamos esquema simple
                g_par = (lambda y, j=j: np.cos(j * np.pi * y / w))
                g_imp = (lambda y, j=j: np.sin((j + 0.5) * np.pi * y / w))
                ky_par, ky_imp = j * np.pi / w, (j + 0.5) * np.pi / w
            else:  # dirichlet
                g_par = (lambda y, j=j: np.cos((j + 0.5) * np.pi * y / w))
                g_imp = (lambda y, j=j: np.sin((j + 1) * np.pi * y / w))
                ky_par, ky_imp = (j + 0.5) * np.pi / w, (j + 1) * np.pi / w
            q = q2 / 2
            if q2 % 2 == 0:  # q entero -> g par
                out.append(dict(j=j, q=q, tipo_y="par", k_x=2 * np.pi * q / L,
                                masa2=(2 * np.pi * q / L) ** 2 + ky_par ** 2,
                                permitido=True))
            else:  # q semientero -> g impar
                out.append(dict(j=j, q=q, tipo_y="impar", k_x=2 * np.pi * q / L,
                                masa2=(2 * np.pi * q / L) ** 2 + ky_imp ** 2,
                                permitido=True))
    return out


# ----------------------------------------------------------------------------
# 6. Randall-Sundrum
# ----------------------------------------------------------------------------

def rs1_espectro(k=1.0, L=None, kL=None, nmodos=6):
    """
    Torre de gravitones KK en RS1 con branas en y=0 (UV) y y=L (IR),
    métrica ds^2 = e^{-2k|y|} η dx dx + dy^2.
    Condición Neumann (modo Z2-par) en ambas branas:
        J_1(m/k) Y_1(m e^{kL}/k) - Y_1(m/k) J_1(m e^{kL}/k) = 0
    (es la misma ecuación de Seahra-Clarkson-Maartens 2005, ec. (4), con
    z = m e^{kL}/k y l = 1/k).  Para e^{kL} >> 1 las raíces son ≈ x_n k e^{-kL}
    con x_n los ceros de J_1: 3.83, 7.02, 10.17, ...
    Perfil del modo (coordenada conforme z = e^{ky}/k):  ψ_m(z) ∝ z^2 [J_2(mz) + b Y_2(mz)].
    """
    if kL is None:
        kL = np.log(L) if L else 10.0
    zUV, zIR = 1.0 / k, np.exp(kL) / k

    def F(m):
        return (special.j1(m * zUV) * special.y1(m * zIR)
                - special.y1(m * zUV) * special.j1(m * zIR))

    # buscar raíces barriendo
    ms = np.linspace(1e-6, 40.0 / zIR, 40000)
    vals = F(ms)
    raices = []
    for i in range(len(ms) - 1):
        if np.sign(vals[i]) != np.sign(vals[i + 1]):
            raices.append(brentq(F, ms[i], ms[i + 1]))
        if len(raices) >= nmodos:
            break
    modos = []
    for m in raices:
        # coeficiente b tal que ψ'(zUV)=0 para ψ = z^2 [J2 + b Y2]  (equiv. a condición en J1)
        b = -special.j1(m * zUV) / special.y1(m * zUV)
        psi = lambda z, m=m, b=b: z ** 2 * (special.jv(2, m * z) + b * special.yv(2, m * z))
        # normalizar con medida dz/z^3  (acción 5D en coord. conforme)
        zz = np.linspace(zUV, zIR, 20000)
        norm = np.sqrt(np.trapezoid(psi(zz) ** 2 / zz ** 3, zz))
        modos.append(dict(m=m, m_sobre_k=m / k,
                          m_sobre_k_eIR=m / k * np.exp(kL),
                          psi_UV=float(psi(zUV) / norm / zUV ** 1.5),
                          psi_IR=float(psi(zIR) / norm / zIR ** 1.5)))
    # modo cero: ψ_0 ∝ z^{-?}: en estas variables h_0 = const en y; peso relativo
    return dict(kL=kL, modos=modos)


def rs2_perfiles(k=1.0, zmax=40.0, n=2000):
    """Modo cero ψ0(z) = k^{-1}(k|z|+1)^{-3/2} y potencial volcán
    V(z) = 15k^2 / (8 (k|z|+1)^2) - (3k/2) δ(z)   (Randall-Sundrum 1999, ec. 10),
    en la coordenada conforme z = (e^{k|y|}-1)/k.  En distancia propia y,
    k|z|+1 = e^{k|y|}, de modo que ψ0 ∝ e^{-3k|y|/2}: decaimiento EXPONENCIAL
    alejándose de la brana, igual que una onda de agua profunda (∝ e^{-k·profundidad},
    Lamb §228; dispersión ω² = g k)."""
    z = np.linspace(0, zmax, n)
    psi0 = (k * z + 1) ** (-1.5) / k
    V = 15 * k ** 2 / (8 * (k * z + 1) ** 2)
    y = np.linspace(0, 6.0 / k, n)
    psi0_y = np.exp(-1.5 * k * y)
    agua = np.exp(-k * y)  # perfil de onda superficial de agua profunda
    return z, psi0, V, (y, psi0_y, agua)


# ----------------------------------------------------------------------------
# 7. Cuerda negra RS: frecuencias KK vs banda LIGO
# ----------------------------------------------------------------------------

def frecuencias_cuerda_negra(ell_m=1e-4, d_sobre_ell=np.arange(5, 31), nmodos=4):
    """
    Seahra, Clarkson & Maartens, PRL 94, 121302 (2005), ec. (4):
        m_n = (z_n / l) e^{-d/l},  Y1(m_n l) J1(z_n) = J1(m_n l) Y1(z_n)
    Para e^{-d/l} << 1: z_n ≈ ceros de J1 (3.8317, 7.0156, 10.1735, 13.3237).
    Clarkson & Seahra, CQG 24, F33 (2007) dan la aproximación
        ω_n ≈ (c/l)(n + 1/4) π e^{-d/l}.
    Frecuencia física f_n = m_n c / (2π)  (m_n en 1/m).
    """
    ceros_j1 = special.jn_zeros(1, nmodos)
    res = []
    for dl in d_sobre_ell:
        fs = [float(zn / ell_m * np.exp(-dl) * C_LIGHT / (2 * np.pi)) for zn in ceros_j1]
        f_aprox = [float(C_LIGHT / ell_m * (n + 0.25) * np.pi * np.exp(-dl) / (2 * np.pi))
                   for n in range(1, nmodos + 1)]
        res.append(dict(d_sobre_l=int(dl), f_Hz=fs, f_aprox_Hz=f_aprox))
    return res


G_NEWTON = 6.674e-11
M_SOL = 1.989e30
MU_CRIT = 0.4301  # Seahra-Clarkson-Maartens 2005: GM m_1 > mu_crit para evitar Gregory-Laflamme


def f_minima_estabilidad(M_sol):
    """Cuerda negra estable solo si G M m_1 / c^2 > mu_crit (m_1 en 1/m)  ->
    f_1 > mu_crit c^3 / (2π G M).  Da la frecuencia KK MÍNIMA compatible con
    un agujero negro de masa M en la brana."""
    M = np.asarray(M_sol) * M_SOL
    return MU_CRIT * C_LIGHT ** 3 / (2 * np.pi * G_NEWTON * M)


def radio_plano_para_frecuencia(f_Hz):
    """Compactificación plana: m_1 = 1/R  ->  R = c / (2π f)."""
    return C_LIGHT / (2 * np.pi * f_Hz)


# ----------------------------------------------------------------------------
# 8. Simulación 1+1: onda en el intervalo con paredes N/D
# ----------------------------------------------------------------------------

def simular_dos_paredes(Ly=np.pi / 2, Ny=400, T=60.0, cfl=0.5, bcI="N", bcII="N",
                        y0=0.15, sigma=0.04):
    """
    ∂_t^2 φ = ∂_y^2 φ en y ∈ [0, Ly] con φ(y) inicial gaussiano cerca de la pared I.
    bc = 'N' (Neumann, ∂_y φ = 0: campo Z2-PAR en esa pared) o
         'D' (Dirichlet, φ = 0: campo Z2-IMPAR en esa pared).
    Devuelve las series temporales registradas junto a la pared I y la pared II
    y sus espectros. Con Ly = π/2 (R=1) las masas KK son las de Kawamura:
        NN -> 0,2,4,...   ND -> 1,3,5,...   DN -> 1,3,5,...   DD -> 2,4,6,...
    pero el PESO de cada armónico en cada pared es lo que distingue (+,-) de (-,+).
    """
    y = np.linspace(0, Ly, Ny)
    dy = y[1] - y[0]
    dt = cfl * dy
    nt = int(T / dt)
    phi = np.exp(-((y - y0) ** 2) / (2 * sigma ** 2))
    phi_old = phi.copy()  # velocidad inicial nula
    # sondas: un poco adentro de cada pared (si la pared es D el campo es 0 justo ahí)
    iI, iII = 3, Ny - 4
    sI, sII = np.zeros(nt), np.zeros(nt)
    lap = np.zeros_like(phi)
    for it in range(nt):
        lap[1:-1] = (phi[2:] - 2 * phi[1:-1] + phi[:-2]) / dy ** 2
        # contornos
        if bcI == "N":
            lap[0] = 2 * (phi[1] - phi[0]) / dy ** 2
        else:
            lap[0] = 0.0
        if bcII == "N":
            lap[-1] = 2 * (phi[-2] - phi[-1]) / dy ** 2
        else:
            lap[-1] = 0.0
        phi_new = 2 * phi - phi_old + dt ** 2 * lap
        if bcI == "D":
            phi_new[0] = 0.0
        if bcII == "D":
            phi_new[-1] = 0.0
        phi_old, phi = phi, phi_new
        sI[it], sII[it] = phi[iI], phi[iII]
    t = np.arange(nt) * dt
    # espectros
    win = np.hanning(nt)
    freqs = np.fft.rfftfreq(nt, dt) * 2 * np.pi  # frecuencia angular = masa KK (c=1)
    SI = np.abs(np.fft.rfft(sI * win))
    SII = np.abs(np.fft.rfft(sII * win))
    return t, sI, sII, freqs, SI, SII


def picos_espectro(freqs, S, Smax=None, mmax=8.5, umbral=0.05):
    """Devuelve las masas KK (enteros) con amplitud relativa > umbral.
    Smax permite normalizar las dos sondas con la misma escala."""
    S = S / (S.max() if Smax is None else Smax)
    picos = {}
    for m in range(0, int(mmax) + 1):
        sel = (freqs > m - 0.4) & (freqs < m + 0.4)
        picos[m] = float(S[sel].max()) if sel.any() else 0.0
    return {m: v for m, v in picos.items() if v > umbral}


# ----------------------------------------------------------------------------
# main: figuras y tablas
# ----------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--outdir", default=os.path.join(os.path.dirname(__file__), "..", "4_Resultados"))
    args = ap.parse_args()
    outdir = os.path.abspath(args.outdir)
    figdir = os.path.join(outdir, "figuras")
    os.makedirs(figdir, exist_ok=True)

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"font.size": 10, "axes.grid": True, "grid.alpha": 0.3})

    resumen = {}

    # ---------------- 1-3 orbifolds planos ----------------
    sect = modos_orbifold_1d(R=1.0, nmax=4)
    resumen["orbifolds_1d"] = sect

    # Figura 1: funciones de modo de los cuatro sectores de S^1/(Z2xZ2')
    R = 1.0
    y = np.linspace(0, np.pi * R / 2, 400)
    fig, axs = plt.subplots(2, 2, figsize=(10, 6.5), sharex=True)
    defs = {
        "(+,+): cos(2ny/R)  m=2n/R  [pared I ≠0, pared II ≠0]": lambda n: np.cos(2 * n * y / R),
        "(+,-): cos((2n+1)y/R)  m=(2n+1)/R  [pared I ≠0, pared II =0]": lambda n: np.cos((2 * n + 1) * y / R),
        "(-,+): sin((2n+1)y/R)  m=(2n+1)/R  [pared I =0, pared II ≠0]": lambda n: np.sin((2 * n + 1) * y / R),
        "(-,-): sin((2n+2)y/R)  m=(2n+2)/R  [pared I =0, pared II =0]": lambda n: np.sin((2 * n + 2) * y / R),
    }
    for ax, (titulo, f) in zip(axs.flat, defs.items()):
        for n in range(0, 3):
            ax.plot(y, f(n), label=f"n={n}")
        ax.axvline(0, color="k", lw=2)
        ax.axvline(np.pi * R / 2, color="k", lw=2)
        ax.text(0.01, 1.05, "pared I\n(nosotros)", fontsize=8, va="bottom")
        ax.text(np.pi * R / 2 - 0.35, 1.05, "pared II\n(sombra)", fontsize=8, va="bottom")
        ax.set_title(titulo, fontsize=9)
        ax.set_ylim(-1.2, 1.5)
        ax.legend(fontsize=8, loc="lower left")
    for ax in axs[1]:
        ax.set_xlabel("y  (intervalo fundamental 0 … πR/2)")
    fig.suptitle("Orbifold S¹/(Z₂×Z₂′): cada sector de paridad decide en qué pared se anula el modo", fontsize=11)
    fig.tight_layout()
    fig.savefig(os.path.join(figdir, "fig1_modos_S1_Z2xZ2p.png"), dpi=150)
    plt.close(fig)

    # Figura 2: comparación de espectros y pesos en pared I / II para las topografías planas
    fig, axs = plt.subplots(1, 3, figsize=(12, 4))
    topos = ["S^1", "S^1/Z_2", "S^1/(Z_2xZ_2')"]
    for ax, topo in zip(axs, topos):
        rows = [s for s in sect if s["topo"] == topo and s["masa"] <= 6.01]
        sectores = sorted(set(r["sector"] for r in rows))
        offs = np.linspace(-0.25, 0.25, len(sectores)) if len(sectores) > 1 else [0]
        for off, sec in zip(offs, sectores):
            rr = [r for r in rows if r["sector"] == sec]
            m = np.array([r["masa"] for r in rr])
            wI = np.array([r["en_I"] for r in rr])
            wII = np.array([r["en_II"] for r in rr])
            ax.scatter(m + off, np.full_like(m, 1.0), s=120 * wI + 5, label=f"{sec} en pared I", marker="o")
            ax.scatter(m + off, np.full_like(m, 0.0), s=120 * wII + 5, marker="s")
        ax.set_yticks([0, 1])
        ax.set_yticklabels(["pared II", "pared I"])
        ax.set_xlabel("masa KK  m R")
        ax.set_title(topo)
        ax.set_ylim(-0.6, 1.6)
        ax.legend(fontsize=7, loc="upper right")
    fig.suptitle("Peso |f_n|² de cada modo KK en las paredes (tamaño del marcador). "
                 "Solo S¹/(Z₂×Z₂′) separa pares/impares por pared.", fontsize=10)
    fig.tight_layout()
    fig.savefig(os.path.join(figdir, "fig2_pesos_en_paredes.png"), dpi=150)
    plt.close(fig)

    # ---------------- 4 Klein ----------------
    klein = modos_klein(kmax=5, lmax=1)
    resumen["klein"] = klein
    # ---------------- 5 Möbius ----------------
    mob = modos_mobius()
    resumen["mobius"] = mob

    # Figura 3: Klein (l=0) y Möbius: qué k sobreviven según paridad / tipo
    fig, axs = plt.subplots(1, 2, figsize=(11, 3.8))
    ax = axs[0]
    for p, color, dy_ in (("+", "C0", 0.1), ("-", "C3", -0.1)):
        ks = [m["k"] for m in klein if m["l"] == 0 and m["paridad"] == p and m["sobrevive"]]
        ax.scatter(ks, [dy_] * len(ks), color=color, s=80, label=f"paridad glide {p}: k sobrevivientes")
        kdead = [m["k"] for m in klein if m["l"] == 0 and m["paridad"] == p and not m["sobrevive"]]
        ax.scatter(kdead, [dy_] * len(kdead), facecolors="none", edgecolors=color, s=80)
    ax.set_yticks([])
    ax.set_xlabel("número KK k a lo largo de y⁵ (modos con l=0)")
    ax.set_title("Botella de Klein R²/pg: la paridad del CAMPO elige k par o impar\n(sin puntos fijos: no hay 'lado')", fontsize=9)
    ax.legend(fontsize=7)
    ax = axs[1]
    for tipo, color in (("par", "C0"), ("impar", "C3")):
        qs = sorted(set(m["q"] for m in mob if m["tipo_y"] == tipo))
        ax.scatter(qs, [0.1 if tipo == "par" else -0.1] * len(qs), color=color, s=80,
                   label=f"g(y) {tipo} en el ancho → q {'entero' if tipo=='par' else 'semientero'}")
    ax.set_yticks([])
    ax.set_xlabel("momento q a lo largo de la banda (en unidades 2π/L)")
    ax.set_title("Banda de Möbius: la torsión desplaza en ½ el espectro de los modos impares\n(borde real, sin puntos fijos)", fontsize=9)
    ax.legend(fontsize=7)
    fig.tight_layout()
    fig.savefig(os.path.join(figdir, "fig3_klein_mobius.png"), dpi=150)
    plt.close(fig)

    # ---------------- 6 RS ----------------
    rs1 = rs1_espectro(k=1.0, kL=5.0, nmodos=5)
    resumen["rs1_kL5"] = rs1
    z, psi0, V, (yy, psi0_y, agua) = rs2_perfiles()
    fig, axs = plt.subplots(1, 3, figsize=(12, 3.8))
    axs[0].plot(yy, psi0_y, label="modo cero RS2 en distancia propia  ψ₀ ∝ e^{-3k|y|/2}")
    axs[0].plot(yy, agua, "--", label="onda de agua profunda  ∝ e^{-k·profundidad}")
    axs[0].set_xlabel("distancia propia a la brana  k y")
    axs[0].set_title("Gravitón ligado a la brana vs. onda superficial de agua", fontsize=9)
    axs[0].legend(fontsize=7)
    axs[0].set_yscale("log")
    axs[0].set_ylim(1e-3, 1.5)
    axs[1].plot(z, V)
    axs[1].set_title("Potencial 'volcán' RS2  V(z)=15k²/[8(k|z|+1)²] − (3k/2)δ(z)", fontsize=9)
    axs[1].set_xlabel("k z")
    axs[1].set_xlim(0, 10)
    mm = [m["m_sobre_k_eIR"] for m in rs1["modos"]]
    pUV = [abs(m["psi_UV"]) for m in rs1["modos"]]
    pIR = [abs(m["psi_IR"]) for m in rs1["modos"]]
    axs[2].semilogy(mm, pUV, "o-", label="|ψ_n| en brana UV (Planck)")
    axs[2].semilogy(mm, pIR, "s-", label="|ψ_n| en brana IR (TeV)")
    axs[2].set_xlabel("m_n e^{kL}/k  (≈ ceros de J₁: 3.83, 7.02, 10.17…)")
    axs[2].set_title(f"RS1 (kL={rs1['kL']}): la torre KK pesa mucho más en la brana IR", fontsize=9)
    axs[2].legend(fontsize=7)
    fig.tight_layout()
    fig.savefig(os.path.join(figdir, "fig4_randall_sundrum.png"), dpi=150)
    plt.close(fig)

    # ---------------- 7 cuerda negra ----------------
    cn = frecuencias_cuerda_negra()
    resumen["cuerda_negra_ell_0.1mm"] = cn
    fig, ax = plt.subplots(figsize=(7, 4.2))
    dls = [c["d_sobre_l"] for c in cn]
    for n in range(4):
        ax.semilogy(dls, [c["f_Hz"][n] for c in cn], "o-", ms=3, label=f"f_{n+1}")
    ax.axhspan(10, 5000, color="C2", alpha=0.15, label="banda LIGO/Virgo/KAGRA (10 Hz–5 kHz)")
    ax.axhspan(1e-4, 1e-1, color="C4", alpha=0.12, label="banda LISA")
    ax.axvspan(0, 5, color="gray", alpha=0.3, label="excluido: ω_BD < 4×10⁴ (d/ℓ ≳ 5)")
    ax.set_xlabel("separación entre branas  d/ℓ   (ℓ = 0.1 mm, cota de laboratorio)")
    ax.set_ylabel("frecuencia KK  f_n [Hz]")
    ax.set_title("Cuerda negra RS: m_n = (z_n/ℓ) e^{-d/ℓ}  →  frecuencias en banda LIGO si d/ℓ ≈ 19–25", fontsize=9)
    ax.legend(fontsize=7, loc="lower left")
    ax.set_ylim(1e-5, 1e13)
    fig.tight_layout()
    fig.savefig(os.path.join(figdir, "fig5_cuerda_negra_frecuencias.png"), dpi=150)
    plt.close(fig)

    # Figura 7: frecuencia KK mínima por estabilidad vs masa del agujero negro
    Ms = np.logspace(0, 3, 200)
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.loglog(Ms, f_minima_estabilidad(Ms), label="f₁ mínima: G M m₁/c² = μ_crit = 0.4301")
    ax.axhspan(10, 5000, color="C2", alpha=0.15, label="banda LIGO/Virgo/KAGRA")
    for M, nombre in ((30, "GW150914-like (~30+30 M☉ → 62 M☉)"), (2.7, "GW170817 remanente ~2.7 M☉")):
        pass
    ax.axvline(62, color="k", ls=":", lw=1); ax.text(64, 20, "GW150914 remanente 62 M☉", fontsize=7, rotation=90)
    ax.axvline(142, color="k", ls=":", lw=1); ax.text(146, 20, "GW190521 remanente 142 M☉", fontsize=7, rotation=90)
    ax.set_xlabel("masa del agujero negro M [M☉]")
    ax.set_ylabel("f₁ [Hz]")
    ax.set_title("Cuerda negra RS: la estabilidad de Gregory-Laflamme exige que el primer modo KK\n"
                 "esté POR ENCIMA de ~0.43 c³/(2πGM); para M ≈ 10–300 M☉ eso cae en la banda LIGO", fontsize=9)
    ax.legend(fontsize=7)
    fig.tight_layout()
    fig.savefig(os.path.join(figdir, "fig7_estabilidad_GL_frecuencia_minima.png"), dpi=150)
    plt.close(fig)
    resumen["f_minima_estabilidad_Hz"] = {f"M={M}Msol": float(f_minima_estabilidad(M)) for M in (3, 10, 30, 62, 142, 1000)}

    resumen["radio_plano_para_f"] = {
        "f=30Hz_R_m": radio_plano_para_frecuencia(30.0),
        "f=300Hz_R_m": radio_plano_para_frecuencia(300.0),
        "f=3000Hz_R_m": radio_plano_para_frecuencia(3000.0),
        "cota_EotWash_2020_Yukawa_lambda_m": 38.6e-6,
    }

    # ---------------- 8 simulación dos paredes ----------------
    combos = {"NN ≡ (+,+)": ("N", "N"), "ND ≡ (+,−)": ("N", "D"),
              "DN ≡ (−,+)": ("D", "N"), "DD ≡ (−,−)": ("D", "D")}
    fig, axs = plt.subplots(4, 2, figsize=(11, 10))
    sim_res = {}
    for i, (nombre, (bI, bII)) in enumerate(combos.items()):
        t, sI, sII, fr, SI, SII = simular_dos_paredes(bcI=bI, bcII=bII)
        axs[i, 0].plot(t, sI, lw=0.7, label="junto a pared I")
        axs[i, 0].plot(t, sII, lw=0.7, alpha=0.8, label="junto a pared II")
        axs[i, 0].set_title(f"{nombre}: señal en el tiempo", fontsize=9)
        axs[i, 0].legend(fontsize=7)
        Smax = max(SI.max(), SII.max())  # normalización común: compara amplitudes entre paredes
        axs[i, 1].plot(fr, SI / Smax, label="espectro en pared I")
        axs[i, 1].plot(fr, SII / Smax, alpha=0.8, label="espectro en pared II")
        axs[i, 1].set_xlim(0, 8.5)
        for m in range(0, 9):
            axs[i, 1].axvline(m, color="gray", lw=0.5, ls=":")
        pI, pII = picos_espectro(fr, SI, Smax), picos_espectro(fr, SII, Smax)
        axs[i, 1].set_title(f"{nombre}: masas KK vistas — pared I: {sorted(pI)}   pared II: {sorted(pII)}", fontsize=8)
        axs[i, 1].legend(fontsize=7)
        sim_res[nombre] = dict(picos_pared_I=pI, picos_pared_II=pII)
    axs[-1, 0].set_xlabel("t")
    axs[-1, 1].set_xlabel("frecuencia angular = masa KK (R=1)")
    fig.suptitle("Pulso emitido junto a la pared I en un intervalo de longitud πR/2 con paredes Neumann (N, campo par) o Dirichlet (D, campo impar)", fontsize=10)
    fig.tight_layout()
    fig.savefig(os.path.join(figdir, "fig6_simulacion_dos_paredes.png"), dpi=150)
    plt.close(fig)
    resumen["simulacion_dos_paredes"] = sim_res

    # ---------------- tabla markdown ----------------
    lineas = ["# Tabla resumen generada por `3_Codigo/modos_paridad_topografias.py`", ""]
    lineas += ["## Orbifold S¹/(Z₂×Z₂′): peso |f_n(y)|² en cada pared (R=1)", "",
               "| sector (P,P′) | n | masa m R | pared I (y=0) | pared II (y=πR/2) |", "|---|---|---|---|---|"]
    for s in sect:
        if s["topo"] == "S^1/(Z_2xZ_2')" and s["n"] <= 2:
            lineas.append(f"| {s['sector']} | {s['n']} | {s['masa']:.0f} | {s['en_I']:.2f} | {s['en_II']:.2f} |")
    lineas += ["", "## Botella de Klein (l=0): modos k que sobreviven según la paridad del campo", "",
               "| paridad glide | k sobrevivientes (|k|≤5) |", "|---|---|"]
    for p in ("+", "-"):
        ks = sorted(m["k"] for m in klein if m["l"] == 0 and m["paridad"] == p and m["sobrevive"])
        lineas.append(f"| {p} | {ks} |")
    lineas += ["", "## Simulación 1+1: masas KK registradas en cada pared (pulso emitido junto a la pared I; amplitud > 5 % del máximo común)", "",
               "| contornos (I,II) | vistas en pared I | vistas en pared II |", "|---|---|---|"]
    for nombre, r in sim_res.items():
        lineas.append(f"| {nombre} | {sorted(r['picos_pared_I'])} | {sorted(r['picos_pared_II'])} |")
    lineas += ["", "## RS1 (kL=5): torre KK y amplitud relativa en cada brana", "",
               "| n | m_n e^{kL}/k | |ψ_n| brana UV | |ψ_n| brana IR |", "|---|---|---|---|"]
    for i, m in enumerate(rs1["modos"], 1):
        lineas.append(f"| {i} | {m['m_sobre_k_eIR']:.3f} | {abs(m['psi_UV']):.3e} | {abs(m['psi_IR']):.3e} |")
    lineas += ["", "## Cuerda negra RS (ℓ = 0.1 mm): primera frecuencia KK", "",
               "| d/ℓ | f₁ [Hz] | f₂ [Hz] |", "|---|---|---|"]
    for c in cn:
        if c["d_sobre_l"] in (5, 10, 15, 18, 20, 22, 24, 26, 30):
            lineas.append(f"| {c['d_sobre_l']} | {c['f_Hz'][0]:.3g} | {c['f_Hz'][1]:.3g} |")
    lineas += ["", "## Cuerda negra: frecuencia KK mínima por estabilidad (GM m₁/c² > 0.4301)", "",
               "| M [M☉] | f₁ mínima [Hz] |", "|---|---|"]
    for kM, fv in resumen["f_minima_estabilidad_Hz"].items():
        lineas.append(f"| {kM.split('=')[1].replace('Msol','')} | {fv:.3g} |")
    rp = resumen["radio_plano_para_f"]
    lineas += ["", "## Compactificación plana: radio necesario para que m₁ c²/h caiga en banda LIGO", "",
               "| f [Hz] | R = c/(2πf) [m] | cota Eöt-Wash 2020 (Yukawa) [m] |", "|---|---|---|"]
    for f in (30, 300, 3000):
        lineas.append(f"| {f} | {rp[f'f={f}Hz_R_m']:.3g} | {rp['cota_EotWash_2020_Yukawa_lambda_m']:.3g} |")
    with open(os.path.join(outdir, "tabla_resumen.md"), "w") as fh:
        fh.write("\n".join(lineas) + "\n")
    with open(os.path.join(outdir, "resumen_numerico.json"), "w") as fh:
        json.dump(resumen, fh, indent=1, default=float)
    print("\n".join(lineas))
    print(f"\nFiguras en {figdir}")


if __name__ == "__main__":
    main()
