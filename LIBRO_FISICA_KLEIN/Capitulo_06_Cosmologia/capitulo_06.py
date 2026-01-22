#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════════════

                    CAPÍTULO 6: COSMOLOGÍA

                    "El universo a gran escala"

═══════════════════════════════════════════════════════════════════════════════

AUTOR: Fausto Jose Di Bacco
EMAIL: faustojdb@gmail.com
AÑO: 2026

Copyright (c) 2026 Fausto Jose Di Bacco. Todos los derechos reservados.
"""

import numpy as np

pi = np.pi
siete_pi = 7 * pi

def mostrar_capitulo():
    print("""
═══════════════════════════════════════════════════════════════════════════════
                        CAPÍTULO 6: COSMOLOGÍA
═══════════════════════════════════════════════════════════════════════════════


╔═════════════════════════════════════════════════════════════════════════════╗
║                                                                             ║
║   "El universo no solo tiene una historia,                                  ║
║    tiene una TEMPERATURA."                                                  ║
║                                        - Cosmología moderna                  ║
║                                                                             ║
║   "Y esa temperatura está escrita en 7π."                                   ║
║                                        - Teoría Klein, 2026                 ║
║                                                                             ║
╚═════════════════════════════════════════════════════════════════════════════╝


═══════════════════════════════════════════════════════════════════════════════
6.1 EL UNIVERSO A GRAN ESCALA
═══════════════════════════════════════════════════════════════════════════════

El universo comenzó hace 13.8 mil millones de años en el Big Bang.
Desde entonces:
    • Se expandió (y sigue expandiéndose)
    • Se enfrió (de 10³² K a 2.7 K)
    • Formó estructuras (galaxias, estrellas, planetas)

Tres observaciones clave conectan con Klein:

    1. La temperatura del CMB (radiación cósmica de fondo)
    2. La constante cosmológica (energía oscura)
    3. El número de Avogadro (conexión macro-micro)


═══════════════════════════════════════════════════════════════════════════════
6.2 LA CONSTANTE COSMOLÓGICA: ρ_Λ/ρ_P = (7/2)×(7π)⁻⁹²
═══════════════════════════════════════════════════════════════════════════════

(Ya visto en Capítulo 4, aquí profundizamos)
""")

    # Constante cosmológica
    ratio_klein = (7/2) * siete_pi**(-92)
    print(f"""
┌─────────────────────────────────────────────────────────────────────────────┐
│  El problema de la constante cosmológica es el "peor desacuerdo"            │
│  en la historia de la física: 10¹²³ órdenes de magnitud.                    │
│                                                                             │
│  FÓRMULA KLEIN:                                                             │
│                                                                             │
│      ρ_Λ / ρ_P = (7/2) × (7π)⁻⁹²                                           │
│                                                                             │
│  donde 92 = 4 × 23 = 4D × (dim(SU(5)) - 1)                                 │
│                                                                             │
│  (7π)⁻⁹² ≈ {siete_pi**(-92):.2e}                                             │
│                                                                             │
│  ¡Esto EXPLICA los 123 órdenes de magnitud!                                 │
│  Error: ~0.7%                                                               │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘


═══════════════════════════════════════════════════════════════════════════════
6.3 LA TEMPERATURA DEL CMB: T_CMB = π×T_P/(7π)²⁴
═══════════════════════════════════════════════════════════════════════════════
""")

    # CMB
    T_P = 1.416808e32  # K
    T_CMB_obs = 2.7255  # K
    T_CMB_klein = pi * T_P / siete_pi**24
    error_CMB = abs(T_CMB_klein - T_CMB_obs) / T_CMB_obs * 100

    print(f"""
┌─────────────────────────────────────────────────────────────────────────────┐
│  CONCEPTO: La Radiación Cósmica de Fondo (CMB)                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  380,000 años después del Big Bang, el universo se enfrió lo suficiente     │
│  para que los electrones se unieran a los protones formando hidrógeno.      │
│                                                                             │
│  La luz de ese momento TODAVÍA llena el universo.                           │
│  La vemos como radiación de microondas a 2.7255 K.                          │
│                                                                             │
│  Esta es la "foto más antigua" del universo.                                │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────────┐
│  MATEMÁTICAS: T_CMB desde Klein                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   T_CMB = π × T_Planck / (7π)²⁴                                            │
│                                                                             │
│   donde:                                                                    │
│   • T_Planck = {T_P:.3e} K (temperatura de Planck)                          │
│   • 24 = dim(SU(5)) = 5² - 1                                               │
│                                                                             │
│   VERIFICACIÓN:                                                             │
│   Predicción: T_CMB = {T_CMB_klein:.4f} K                                      │
│   Observado:  T_CMB = {T_CMB_obs} K (Planck 2018)                            │
│   Error:      {error_CMB:.2f}%                                                 │
│                                                                             │
│   INTERPRETACIÓN:                                                           │
│   El universo se ha enfriado por un factor de (7π)²⁴ desde el Big Bang.    │
│   El exponente 24 = dim(SU(5)) conecta cosmología con física de partículas. │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘


═══════════════════════════════════════════════════════════════════════════════
6.4 EL NÚMERO DE AVOGADRO: N_A = e^[(5/2 - 1/99)×7π]
═══════════════════════════════════════════════════════════════════════════════
""")

    # Avogadro
    N_A_obs = 6.02214076e23
    coef = 5/2 - 1/99
    N_A_klein = np.exp(coef * siete_pi)
    error_NA = abs(N_A_klein - N_A_obs) / N_A_obs * 100

    print(f"""
┌─────────────────────────────────────────────────────────────────────────────┐
│  CONCEPTO: El Puente Macro-Micro                                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  N_A = 6.022 × 10²³ es el número de átomos en un mol de sustancia.         │
│                                                                             │
│  Conecta el mundo macroscópico (gramos, litros) con el microscópico        │
│  (átomos, moléculas).                                                       │
│                                                                             │
│  ¿Por qué este número específico?                                           │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────────┐
│  MATEMÁTICAS: N_A desde Klein                                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   N_A = e^[(5/2 - 1/99) × 7π]                                              │
│                                                                             │
│   Desglose:                                                                 │
│   • 5/2 = 2.5 (corrección termodinámica, 5 dimensiones)                    │
│   • 1/99 ≈ 0.0101 (corrección fina)                                        │
│   • 5/2 - 1/99 = {coef:.6f}                                                   │
│   • × 7π = × {siete_pi:.4f}                                                   │
│   • Exponente total = {coef * siete_pi:.4f}                                   │
│                                                                             │
│   VERIFICACIÓN:                                                             │
│   Predicción: N_A = {N_A_klein:.5e}                                           │
│   Observado:  N_A = {N_A_obs:.5e}                                           │
│   Error:      {error_NA:.2f}%                                                 │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘


═══════════════════════════════════════════════════════════════════════════════
6.5 RESUMEN DEL CAPÍTULO
═══════════════════════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│  PREDICCIONES COSMOLÓGICAS KLEIN:                                           │
│                                                                             │
│  1. ρ_Λ/ρ_P = (7/2)×(7π)⁻⁹²    [0.7% error] - Constante cosmológica       │
│  2. T_CMB = π×T_P/(7π)²⁴        [0.22% error] - Temperatura CMB            │
│  3. N_A = e^[(5/2-1/99)×7π]     [0.08% error] - Número de Avogadro         │
│  4. t_U/t_P = (7π)⁴⁵            [~5% error] - Edad del universo            │
│                                                                             │
│  EXPONENTES CLAVE:                                                          │
│  • 24 = dim(SU(5)) → T_CMB                                                  │
│  • 45 ≈ 2×24-3 → edad del universo                                         │
│  • 92 = 4×23 → constante cosmológica                                       │
│                                                                             │
│  PRÓXIMO CAPÍTULO: Antimateria                                              │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘


═══════════════════════════════════════════════════════════════════════════════
                          FIN DEL CAPÍTULO 6
═══════════════════════════════════════════════════════════════════════════════
""")


if __name__ == "__main__":
    mostrar_capitulo()
