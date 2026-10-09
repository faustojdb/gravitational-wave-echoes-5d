#!/usr/bin/env python3
"""
Números para 1_Teoria/05_ventana_submilimetrica.md. Sólo constantes CODATA,
Λ de Planck 2018 y la cota de Lee et al. 2020. Sin parámetros ajustados.
Salida: 4_Resultados/numeros_ventana_submm.md
"""
import math, os
c=299_792_458.0; G=6.674_30e-11; hbar=1.054_571_817e-34; kB=1.380_649e-23; eV=1.602_176_634e-19
H0=67.4e3/3.0857e22; OmegaL=0.685; Lam=3*OmegaL*H0**2/c**2
lP=math.sqrt(hbar*G/c**3); LL=1/math.sqrt(Lam); lam_lab=38.6e-6
MP_GeV=math.sqrt(hbar*c/G)*c**2/eV/1e9  # masa de Planck en GeV
out=["# Números de la ventana submilimétrica (generados por `3_Codigo/numeros_ventana_submm.py`)","","| Magnitud | Valor | Unidad | Derivación |","|---|---|---|---|"]
def row(k,v,u="",d=""): out.append(f"| {k} | {v} | {u} | {d} |")
# 1. la única longitud mixta
Lmix=math.sqrt(lP*LL); row("√(ℓ_P · L_Λ)", f"{Lmix*1e6:.1f}", "µm", "media geométrica de las dos únicas longitudes de G, c, ħ, Λ")
rho=Lam*c**4/(8*math.pi*G); E_de=(rho*hbar**3*c**3)**0.25; L_de=hbar*c/E_de
row("ρ_Λ^{1/4} (escala de energía oscura)", f"{E_de/eV*1e3:.2f}", "meV", "(ρ_Λ ħ³c³)^{1/4}")
row("ħc/ρ_Λ^{1/4} (longitud de energía oscura)", f"{L_de*1e6:.1f}", "µm", f"= (8π)^{{1/4}} √(ℓ_P L_Λ); (8π)^{{1/4}} = {(8*math.pi)**0.25:.3f}")
row("Cota de laboratorio λ (Lee et al. 2020)", f"{lam_lab*1e6:.1f}", "µm", "dato; cociente con √(ℓ_P L_Λ) = %.2f" % (lam_lab/Lmix))
# 2. KK en la ventana
for R in (lam_lab, 10e-6, 1e-6, 1e-9):
    f1=c/(2*math.pi*R); m1=hbar*c/R/eV
    Mstar=(MP_GeV**2 * (hbar*c/R/eV/1e9))**(1/3)   # M*^3 R = M_P^2 (n=1, sin factores 2π)
    row(f"R = {R*1e6:g} µm: f₁ = c/2πR", f"{f1:.2e}", "Hz", "primer modo KK; m₁c² = %.2e eV" % m1)
    row(f"R = {R*1e6:g} µm: escala fundamental 5D M* = (M_P²/R)^{{1/3}}", f"{Mstar:.1e}", "GeV", "n = 1 dimensión plana, gravedad en el bulk")
# 3. coeficientes Yukawa derivados de las funciones de modo
row("S¹ radio R: V = −Gm₁m₂/r [1 + 2 Σ e^{−nr/R}]", "α = 2, λ = R", "", "Kehagias–Sfetsos 2000 (α = 2n para Tⁿ)")
row("S¹/Z₂, brana en y=0: |f_n(0)|²/|f_0|²", "2", "", "f_0 = 1/√(πR), f_n = √(2/πR) cos(ny/R) ⇒ α = 2, λ = R")
row("S¹/(Z₂×Z₂′), gravitón (+,+), nuestra pared: masas", "2n/R", "", "cos(2ny/R) ⇒ α = 2, λ_eff = R/2")
row("S¹/(Z₂×Z₂′), sector (−,+) visto desde nuestra pared", "0", "", "sin(…) se anula en y = 0: no contribuye a nuestro 1/r²")
row("Materia en la pared sombra vista desde la nuestra", "1 + 2 Σ (−1)ⁿ e^{−2nr/R}", "", "cos(nπ) = (−1)ⁿ ⇒ serie alternante")
for x in (0.9, 0.5, 0.1):   # x = e^{-2r/R}
    propio=(1+x)/(1-x); sombra=(1-x)/(1+x)
    r_over_R=-math.log(x)/2
    row(f"r/R = {r_over_R:.2f}: factor propio (1+x)/(1−x), factor sombra (1−x)/(1+x)", f"{propio:.2f} / {sombra:.2f}", "", "x = e^{−2r/R}")
row("RS2, r ≫ ℓ: V = −Gm₁m₂/r [1 + 2ℓ²/(3r²)]", "potencia, no Yukawa", "", "Garriga–Tanaka 2000")
# 4. GW: inaccesible
row("Frecuencia KK mínima en la ventana (R < 38.6 µm)", f"> {c/(2*math.pi*lam_lab):.2e}", "Hz", "ningún detector de GW; terahercios")
row("Órdenes de magnitud entre esa f y la banda de LIGO (≈ 1 kHz)", f"{math.log10(c/(2*math.pi*lam_lab)/1e3):.1f}", "décadas", "")
os.makedirs("../4_Resultados",exist_ok=True); open("../4_Resultados/numeros_ventana_submm.md","w").write("\n".join(out)+"\n"); print("\n".join(out))
