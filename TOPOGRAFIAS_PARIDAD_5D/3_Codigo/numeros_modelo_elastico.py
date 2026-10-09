#!/usr/bin/env python3
"""
Todos los números citados en 1_Teoria/04_modelo_elastico.md se calculan aquí
a partir de constantes CODATA y de cotas publicadas (ver 2_Bibliografia).
Ningún parámetro libre. Salida: 4_Resultados/numeros_modelo_elastico.md
"""
import math, os
c = 299_792_458.0; G = 6.674_30e-11; hbar = 1.054_571_817e-34; h = 2*math.pi*hbar
kB = 1.380_649e-23; e = 1.602_176_634e-19; me = 9.109_383_7e-31; eps0 = 8.854_187_8e-12; mu0 = 4e-7*math.pi
Msun = 1.988_47e30
H0 = 67.4e3/3.0857e22          # s^-1 (Planck 2018, 67.4 km/s/Mpc)
OmegaL = 0.685
Lambda = 3*OmegaL*H0**2/c**2   # m^-2
S_sol = 1361.0                 # W/m^2, constante solar
lam_eotwash = 38.6e-6          # m, Lee et al. 2020

out = []
def row(k, v, u="", nota=""): out.append(f"| {k} | {v} | {u} | {nota} |")
out += ["# Números del modelo elástico (generados por `3_Codigo/numeros_modelo_elastico.py`)", "",
        "| Magnitud | Valor | Unidad | Origen |", "|---|---|---|---|"]

K = c**4/(8*math.pi*G); row("Rigidez K = c⁴/8πG", f"{K:.3e}", "N", "constantes")
row("Pretensión Λc⁴/8πG", f"{Lambda*K:.3e}", "N/m² = J/m³ (= ρ_Λ c²)", "Λ de Planck 2018")
LL = 1/math.sqrt(Lambda); row("Longitud de la pretensión 1/√Λ", f"{LL:.3e}", "m", "cociente de los dos términos")
lP = math.sqrt(hbar*G/c**3); mP = math.sqrt(hbar*c/G)
row("Longitud de Planck ℓ_P = √(ħG/c³)", f"{lP:.3e}", "m", "única longitud con ħ, G, c")
row("Masa de Planck m_P = √(ħc/G)", f"{mP:.3e}", "kg", "")
row("Cociente de escalas 1/(√Λ ℓ_P)", f"{LL/lP:.2e}", "", "órdenes de magnitud entre los dos términos")
m_cross = math.sqrt(hbar*c/(2*G)); row("Masa donde λ_Compton = r_Schwarzschild", f"{m_cross:.3e} = m_P/√2", "kg", "ħ/(mc) = 2Gm/c²")
# flujo GW (Isaacson): F = (c³/16πG) <ḣ₊² + ḣₓ²>; onda monocromática h₊ = h cos(2πft), hₓ=0 -> <ḣ²> = (2πf h)²/2
for f_, h_ in ((100.0, 1e-21), (250.0, 1e-21), (250.0, 2e-21)):
    F = c**3/(16*math.pi*G) * (2*math.pi*f_*h_)**2/2
    row(f"Flujo de energía GW, h={h_:.0e}, f={f_:.0f} Hz", f"{F:.2e}", "W/m²", f"Isaacson; = {F/S_sol:.1e} × constante solar")
# Donoghue: U = -(GMm/r)(1 + 3G(M+m)/(rc²) + (41/10π) ℓ_P²/r²)
for r in (1.0, lam_eotwash, 1e-15):
    row(f"Corrección cuántica (41/10π)(ℓ_P/r)², r = {r:.1e} m", f"{41/(10*math.pi)*(lP/r)**2:.1e}", "", "Bjerrum-Bohr–Donoghue–Holstein 2003")
row("Corrección post-newtoniana 3G(M+m)/rc², M+m = 2 M☉, r = 10⁶ m", f"{3*G*2*Msun/(1e6*c**2):.1e}", "", "misma fórmula, término clásico")
# Schwinger, Unruh, Hawking
ES = me**2*c**3/(e*hbar); row("Campo de Schwinger E_S = m_e²c³/(eħ)", f"{ES:.2e}", "V/m", "QED, Sauter 1931 / Schwinger 1951")
row("Longitud de Compton reducida del electrón ħ/(m_e c)", f"{hbar/(me*c):.3e}", "m", "")
TU = hbar*9.81/(2*math.pi*c*kB); row("Temperatura de Unruh para a = g", f"{TU:.1e}", "K", "T = ħa/(2πck_B)")
for M in (62.0, 1.0):
    TH = hbar*c**3/(8*math.pi*G*M*Msun*kB); row(f"Temperatura de Hawking, M = {M:.0f} M☉", f"{TH:.1e}", "K", "T = ħc³/(8πGMk_B)")
# Membrana
Z0 = math.sqrt(mu0/eps0); row("Impedancia del vacío = resistividad superficial del horizonte", f"{Z0:.1f}", "Ω", "Damour 1978; Thorne–Price–Macdonald 1986")
eta = c**3/(16*math.pi*G); row("Viscosidad de cizalla del horizonte η = c³/16πG", f"{eta:.2e}", "Pa·s", "paradigma de la membrana (ζ = −η)")
# deformación ~1: r_S
for M in (30.0, 62.0):
    rS = 2*G*M*Msun/c**2; row(f"r_Schwarzschild, M = {M:.0f} M☉", f"{rS/1e3:.1f}", "km", "deformación h ~ r_S/r = 1")
# Escalas donde no hay cota sobre F(L)
row("Órdenes de magnitud sin medir entre 38.6 µm y ℓ_P", f"{math.log10(lam_eotwash/lP):.1f}", "décadas", "ventana libre submilimétrica")
os.makedirs("../4_Resultados", exist_ok=True)
open("../4_Resultados/numeros_modelo_elastico.md","w").write("\n".join(out)+"\n"); print("\n".join(out))
