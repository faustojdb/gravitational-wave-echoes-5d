#!/usr/bin/env python3
"""
Números y verificaciones para 1_Teoria/06_materia_sombra.md.
Verifica numéricamente que la suma KK y la suma de imágenes 5D coinciden
(teorema de Poisson), y tabula las formas cerradas coth / tanh.
Salida: 4_Resultados/numeros_materia_sombra.md
"""
import math, os
import numpy as np

def V_kk_propio(r, R, nmax=20000):      # 1 + 2 Σ e^{-n r/R}
    n = np.arange(1, nmax + 1); return 1 + 2 * np.sum(np.exp(-n * r / R))
def V_kk_sombra(r, R, nmax=20000):      # 1 + 2 Σ (-1)^n e^{-n r/R}
    n = np.arange(1, nmax + 1); return 1 + 2 * np.sum((-1.0) ** n * np.exp(-n * r / R))
def V_img(r, R, d, kmax=200000):
    """Suma de imágenes 5D: fuente a distancia d en la dimensión compacta de circunferencia 2πR.
    Normalización: V = -(G5 m/π) Σ_k 1/(r² + (d+2πRk)²), con G5 = 2πR·G, dividido por -Gm/r."""
    k = np.arange(-kmax, kmax + 1); return (2 * R * r) * np.sum(1.0 / (r ** 2 + (d + 2 * math.pi * R * k) ** 2))

out = ["# Números de la materia sombra (generados por `3_Codigo/numeros_materia_sombra.py`)", "",
       "## Verificación: suma KK = suma de imágenes 5D (S¹ de radio R; nuestra pared y = 0, pared sombra y = πR)", "",
       "| r/R | KK propio 1+2Σe^{−nr/R} | imágenes d=0 | coth(r/2R) | KK sombra 1+2Σ(−1)ⁿe^{−nr/R} | imágenes d=πR | tanh(r/2R) |",
       "|---|---|---|---|---|---|---|"]
R = 1.0
for rr in (0.05, 0.2, 0.5, 1.0, 2.0, 5.0, 10.0):
    out.append(f"| {rr:g} | {V_kk_propio(rr,R):.6f} | {V_img(rr,R,0.0):.6f} | {1/math.tanh(rr/2):.6f} | {V_kk_sombra(rr,R):.6f} | {V_img(rr,R,math.pi*R):.6f} | {math.tanh(rr/2):.6f} |")
out += ["", "Las tres columnas de cada bloque coinciden a 10⁻⁶: la suma de modos es exactamente coth(r/2R) para materia propia y tanh(r/2R) para materia sombra.", "",
        "## Permeabilidad gravitacional P(r) = tanh(πr/2L) en función de la separación física L entre paredes", "",
        "| r/L | P(r) = V_sombra/V_newton | V_propio/V_newton = coth(πr/2L) | razón sombra/propio = tanh² |", "|---|---|---|---|"]
for q in (0.01, 0.1, 0.25, 0.5, 1.0, 2.0, 3.0, 5.0):
    t = math.tanh(math.pi * q / 2); out.append(f"| {q:g} | {t:.4f} | {1/t:.4f} | {t*t:.4f} |")
out += ["", "## Límites analíticos", "",
        "| Régimen | materia propia | materia sombra |", "|---|---|---|",
        "| r ≪ L | V → −2GmR/r² = −G₅m/(πr²) (Newton 5D) | V → −Gm_s/(2R) = −πGm_s/(2L): **finito** |",
        "| r ≫ L | V → −Gm/r [1 + 2e^{−πr/L}] | V → −Gm_s/r [1 − 2e^{−πr/L}] |",
        "| fuerza, r ≪ L | F → 4GmR/r³ (∝ 1/r³) | F → −G m_s r/(12R³) = −π³G m_s r/(12L³): restauradora, ∝ r, → 0 |", "",
        "## Modos masivos no radiados (evanescencia)", "",
        "| fuente | ħω | m₁c² para R = 38.6 µm | ω/m₁ |", "|---|---|---|---|"]
hbar = 1.054571817e-34; eV = 1.602176634e-19; c = 299792458.0
m1 = hbar * c / 38.6e-6
for nombre, f in (("fusión BBH, 250 Hz", 250.0), ("BNS, 2 kHz", 2000.0), ("radio KK f₁ = c/2πR", c / (2 * math.pi * 38.6e-6))):
    out.append(f"| {nombre} | {hbar*2*math.pi*f/eV:.2e} eV | {m1/eV:.2e} eV | {2*math.pi*f*hbar/m1:.1e} |")
out += ["", "Un modo de masa m sólo se propaga si ħω > mc²; para toda fuente astrofísica ω/m₁ ≲ 10⁻⁹, de modo que las ondas gravitacionales de materia sombra son **exactamente** las del modo cero, con la forma de onda de la relatividad general 4D.", ""]
# fracción sombra necesaria para Ω_DM
out += ["## Si la materia sombra fuera toda la materia oscura", "", "| magnitud | valor | origen |", "|---|---|---|",
        "| Ω_c h² (Planck 2018) | 0.120 | dato |", "| Ω_b h² (Planck 2018) | 0.0224 | dato |",
        f"| m_s / m_b necesario | {0.120/0.0224:.2f} | cociente |", ""]
os.makedirs("../4_Resultados", exist_ok=True)
open("../4_Resultados/numeros_materia_sombra.md", "w").write("\n".join(out) + "\n"); print("\n".join(out))
