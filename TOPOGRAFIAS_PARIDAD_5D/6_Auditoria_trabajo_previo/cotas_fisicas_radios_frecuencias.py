#!/usr/bin/env python3
"""
Confronta los radios y frecuencias propuestos en el trabajo previo del
repositorio con cotas físicas publicadas. Sólo aritmética con constantes y
cotas citadas en 2_Bibliografia; no usa ninguna fórmula del trabajo previo
salvo para evaluarla. Genera cotas_fisicas.md.
"""
import math
c = 299_792_458.0; G = 6.674e-11; Msun = 1.989e30
LAMBDA_EOTWASH = 38.6e-6      # m, Lee et al. 2020 (PRL 124, 101101): Yukawa > 38.6 µm excluido al 95 %
R_TIERRA = 6.371e6
LIGO_BAND = (10.0, 5000.0)    # Hz, banda útil aproximada; por debajo de ~10-20 Hz domina el ruido sísmico

radios_km = {"8400 (R_eff, v3 y 'Klein Field Theory')": 8400.0, "419.3 (FUNDAMENTAL_RADIUS)": 419.3,
             "1751.173 (KLEIN_SPACETIME_ATOMS y otros)": 1751.173, "8187 (variante)": 8187.0}
lineas = ["# Cotas físicas sobre los radios y frecuencias propuestos en el trabajo previo", "",
          "Generado por `cotas_fisicas_radios_frecuencias.py`. Nivel: **dato** (cotas publicadas) aplicado a los **números del trabajo previo**.", "",
          "## Radios propuestos vs. test de la ley 1/r² (compactificación plana)", "",
          "| R propuesto [km] | f = c/(2πR) [Hz] | f = c/(4πR) [Hz] | 2πR/c [s] | R / cota Eöt-Wash (38.6 µm) | R / R_Tierra |",
          "|---|---|---|---|---|---|"]
for k, Rkm in radios_km.items():
    R = Rkm * 1e3
    lineas.append(f"| {k} | {c/(2*math.pi*R):.3f} | {c/(4*math.pi*R):.3f} | {2*math.pi*R/c:.4f} | {R/LAMBDA_EOTWASH:.1e} | {R/R_TIERRA:.3f} |")
lineas += ["", "Lectura: una dimensión extra plana de radio R hace que la gravedad sea 5D a distancias r < R, es decir F ∝ 1/r³ en vez de 1/r². "
           "Los tests de torsión confirman 1/r² hasta 38.6 µm; la mecánica celeste (LLR, efemérides planetarias) lo confirma de 10⁶ a 10¹² m con precisión mejor que 10⁻⁸. "
           "Todos los radios propuestos están entre 10¹⁰ y 10¹¹ veces por encima de la cota de laboratorio y dentro del rango donde las órbitas planetarias serían 5D. "
           "Sólo un warping con brana física podría evitarlo, y el trabajo previo no lo propone.", ""]

frecs = {"5.68 Hz (f₀ 'universal', ~420 menciones)": 5.68, "6.65 Hz (paper v3 y multi-topología)": 6.65, "2.84 Hz (c/4πR con R=8400 km)": 2.84,
         "4.19 Hz (ℝP², multi-topología)": 4.19, "8.2 Hz (Möbius, multi-topología)": 8.2, "113.79 Hz (R=419.3 km)": 113.79, "27.25 Hz (R=1751 km)": 27.25}
lineas += ["## Frecuencias propuestas vs. banda sensible de LIGO", "", "| f propuesta | en banda LIGO (≳10 Hz)? | comentario |", "|---|---|---|"]
for k, f in frecs.items():
    enb = LIGO_BAND[0] <= f <= LIGO_BAND[1]
    com = "medible en strain" if enb else "por debajo del muro sísmico: el strain público se filtra por encima de ~10–20 Hz; una 'frecuencia universal' ahí no es observable con LIGO"
    lineas.append(f"| {k} | {'sí' if enb else 'NO'} | {com} |")
lineas += ["", "## Ley de retardo τ = 2.574·M^(−0.826) + 0.273 s vs. mecanismos físicos", "",
           "| M remanente [M☉] | τ previo [s] | τ ecos de objeto compacto exótico ≈ 8GM/c³·ln(M/ℓ_P)·(1/c) [s] | período KK 2πR/c, R=8400 km [s] |", "|---|---|---|---|"]
lp = 1.616e-35
for M in (10, 20, 40, 62, 100, 142):
    tau_prev = 2.574 * M ** (-0.826) + 0.273
    rs = 2 * G * M * Msun / c**2
    tau_eco = 8 * (G * M * Msun / c**3) * math.log(rs / lp)
    lineas.append(f"| {M} | {tau_prev:.3f} | {tau_eco:.3f} | {2*math.pi*8.4e6/c:.3f} |")
lineas += ["", "Lectura: la ley previa **decrece** con la masa. Un modo de Kaluza-Klein tiene frecuencia fijada por la geometría y es **independiente** de M. "
           "Los ecos de objetos compactos exóticos (Cardoso–Franzin–Pani 2016) **crecen** linealmente con M. Ningún mecanismo publicado da τ ∝ M^(−0.826); "
           "el exponente es un ajuste y el término constante 0.273 s coincide con el que se esperaría de 2πR/c para R≈8400 km sólo dentro de un factor 1.5.", ""]
open("cotas_fisicas.md", "w").write("\n".join(lineas) + "\n"); print("\n".join(lineas))
