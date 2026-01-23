#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════════════

                    CAPÍTULO 5: PARTÍCULAS ELEMENTALES

                    "Los ladrillos del universo"

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
                    CAPÍTULO 5: PARTÍCULAS ELEMENTALES
═══════════════════════════════════════════════════════════════════════════════


╔═════════════════════════════════════════════════════════════════════════════╗
║                                                                             ║
║   "¿Por qué el protón es 1836 veces más pesado que el electrón?"            ║
║                                        - Pregunta sin respuesta, siglo XX   ║
║                                                                             ║
║   "Porque 1836 = 6π⁵."                                                      ║
║                                        - Teoría Klein, 2026                 ║
║                                                                             ║
╚═════════════════════════════════════════════════════════════════════════════╝


═══════════════════════════════════════════════════════════════════════════════
5.1 EL ZOOLÓGICO DE PARTÍCULAS
═══════════════════════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────────────────────┐
│  ANALOGÍA: El LEGO Cósmico                                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Imagina que todo el universo está hecho de piezas de LEGO.                 │
│  Pero no hay infinitos tipos de piezas - solo unas pocas fundamentales.     │
│                                                                             │
│  FERMIONES (materia):                                                       │
│  ┌─────────────────────────────────────────────────────────────────┐        │
│  │  QUARKS          │  LEPTONES                                    │        │
│  │  u (up)    d (down)     │  e (electrón)   νₑ (neutrino e)      │        │
│  │  c (charm) s (strange)  │  μ (muón)       νᵤ (neutrino μ)      │        │
│  │  t (top)   b (bottom)   │  τ (tau)        ν_τ (neutrino τ)     │        │
│  └─────────────────────────────────────────────────────────────────┘        │
│                                                                             │
│  BOSONES (fuerzas):                                                         │
│  • Fotón (γ): fuerza electromagnética                                       │
│  • Gluones (g): fuerza nuclear fuerte                                       │
│  • W±, Z⁰: fuerza nuclear débil                                             │
│  • Higgs (H): da masa a las partículas                                      │
│  • Gravitón (?): fuerza gravitacional (aún no detectado)                    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘


EL MISTERIO DE LAS MASAS:

¿Por qué estas partículas tienen las masas que tienen?
El Modelo Estándar NO lo explica - son "parámetros libres".

    Electrón:  mₑ = 0.511 MeV
    Muón:      mᵤ = 105.66 MeV
    Tau:       m_τ = 1776.86 MeV
    Protón:    m_p = 938.27 MeV
    Higgs:     m_H = 125,250 MeV

¿Hay un patrón? La Teoría Klein dice que SÍ.


═══════════════════════════════════════════════════════════════════════════════
5.2 LA MASA DEL PROTÓN: m_p/m_e = 6π⁵
═══════════════════════════════════════════════════════════════════════════════

El ratio entre la masa del protón y el electrón es uno de los
números más importantes de la física.
""")

    # Ratio protón/electrón
    mp_me_obs = 1836.15267
    mp_me_klein = 6 * pi**5
    error_mp = abs(mp_me_klein - mp_me_obs) / mp_me_obs * 100

    print(f"""
┌─────────────────────────────────────────────────────────────────────────────┐
│  CONCEPTO: ¿Por qué importa m_p/m_e?                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Este ratio determina:                                                      │
│  • El tamaño de los átomos                                                  │
│  • La velocidad de las reacciones químicas                                  │
│  • La estabilidad del hidrógeno                                             │
│  • Si la vida es posible                                                    │
│                                                                             │
│  Si fuera muy diferente, no habría química, ni planetas, ni vida.           │
│                                                                             │
│  Valor observado: m_p/m_e = {mp_me_obs:.5f}                                    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────────┐
│  MATEMÁTICAS: La Fórmula Klein para m_p/m_e                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   m_p / m_e = 6π⁵ = (7-1) × π⁵                                             │
│                                                                             │
│   Desglose:                                                                 │
│   • π⁵ = {pi**5:.4f} (quinta potencia de π)                                   │
│   • 6 = 7 - 1 (capas Klein menos una de referencia)                         │
│   • 6π⁵ = {6*pi**5:.4f}                                                       │
│                                                                             │
│   VERIFICACIÓN:                                                             │
│   Predicción: {mp_me_klein:.5f}                                                │
│   Observado:  {mp_me_obs:.5f}                                                │
│   Error:      {error_mp:.4f}%                                                 │
│                                                                             │
│   ¡ESTA ES NUESTRA MEJOR PREDICCIÓN!                                        │
│   Solo 0.002% de error - mejor que muchas mediciones experimentales.        │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────────┐
│  ANALOGÍA: Las 6 Capas Activas                                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  La botella de Klein tiene 7 capas.                                         │
│  Pero UNA capa es especial: es la "referencia" o el "origen".               │
│                                                                             │
│  Las otras 6 capas son "activas" y contribuyen a la física.                 │
│                                                                             │
│       Capa 7 ──┐                                                            │
│       Capa 6   │                                                            │
│       Capa 5   │ ← 6 capas activas                                          │
│       Capa 4   │                                                            │
│       Capa 3   │                                                            │
│       Capa 2 ──┘                                                            │
│       Capa 1 ──── ← 1 capa de referencia                                    │
│                                                                             │
│  El factor 6 = 7-1 aparece en el ratio de masas porque                      │
│  el protón "siente" las 6 capas activas, mientras el electrón               │
│  es una partícula fundamental que vive en la capa de referencia.            │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘


¿POR QUÉ π⁵?

El exponente 5 no es arbitrario:
    • 5 = dimensiones de Kaluza-Klein (4 espacio-tiempo + 1 extra)
    • 5 = número de dimensiones donde la botella de Klein es natural
    • 5 aparece en dim(SU(5)) = 24 = 5² - 1

La masa del protón codifica la estructura 5-dimensional del universo.


═══════════════════════════════════════════════════════════════════════════════
5.3 LA MASA DEL MUÓN: m_μ/m_e = 21π² = 3×7×π²
═══════════════════════════════════════════════════════════════════════════════

El muón es como un "electrón gordo" - misma carga, pero 207 veces más pesado.
""")

    # Ratio muón/electrón
    mu_me_obs = 206.7682830
    mu_me_klein = 21 * pi**2
    error_mu = abs(mu_me_klein - mu_me_obs) / mu_me_obs * 100

    print(f"""
┌─────────────────────────────────────────────────────────────────────────────┐
│  MATEMÁTICAS: La Fórmula Klein para m_μ/m_e                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   m_μ / m_e = 21π² = 3 × 7 × π²                                            │
│                                                                             │
│   Desglose:                                                                 │
│   • π² = {pi**2:.6f}                                                         │
│   • 21 = 3 × 7 (generaciones × capas Klein)                                │
│   • 21π² = {21*pi**2:.4f}                                                     │
│                                                                             │
│   VERIFICACIÓN:                                                             │
│   Predicción: {mu_me_klein:.4f}                                                │
│   Observado:  {mu_me_obs:.4f}                                                │
│   Error:      {error_mu:.3f}%                                                 │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘


INTERPRETACIÓN:

El factor 21 = 3 × 7 tiene significado profundo:

    • 3 = número de generaciones de fermiones (e, μ, τ)
    • 7 = número de capas de Klein

El muón es la "segunda generación" del electrón.
Su masa codifica tanto la estructura generacional (3) como la topológica (7).

Nota: 21 ≈ 7π ≈ 22. ¡El muón también "conoce" la constante Klein!


═══════════════════════════════════════════════════════════════════════════════
5.4 LA MASA DEL HIGGS: m_H/m_p = 42.5π = (6×7 + 1/2)π
═══════════════════════════════════════════════════════════════════════════════

El bosón de Higgs es especial: da masa a todas las demás partículas.
""")

    # Ratio Higgs/protón
    mH = 125250  # MeV
    mp = 938.27  # MeV
    mH_mp_obs = mH / mp
    mH_mp_klein = (6*7 + 0.5) * pi
    error_H = abs(mH_mp_klein - mH_mp_obs) / mH_mp_obs * 100

    print(f"""
┌─────────────────────────────────────────────────────────────────────────────┐
│  CONCEPTO: El Bosón de Higgs                                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  El campo de Higgs permea todo el universo como un "jarabe cósmico".        │
│  Las partículas que interactúan con él adquieren masa.                      │
│                                                                             │
│  • Fotones: no interactúan → sin masa                                       │
│  • Electrones: interactúan poco → masa pequeña                              │
│  • Quarks top: interactúan mucho → masa enorme                              │
│                                                                             │
│  El Higgs mismo tiene masa: m_H = 125.25 GeV                                │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────────┐
│  MATEMÁTICAS: La Fórmula Klein para m_H/m_p                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   m_H / m_p = (6×7 + 1/2) × π = 42.5π                                      │
│                                                                             │
│   Desglose:                                                                 │
│   • 6 × 7 = 42 (capas activas × capas totales)                             │
│   • + 1/2 = corrección cuántica                                             │
│   • × π = factor geométrico                                                 │
│   • 42.5π = {42.5*pi:.4f}                                                     │
│                                                                             │
│   VERIFICACIÓN:                                                             │
│   Predicción: {mH_mp_klein:.4f}                                                │
│   Observado:  {mH_mp_obs:.4f}                                                │
│   Error:      {error_H:.3f}%                                                  │
│                                                                             │
│   ¡Segunda mejor predicción después de m_p/m_e!                             │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────────┐
│  ANALOGÍA: El Número 42                                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  En "La Guía del Autoestopista Galáctico", 42 es la respuesta              │
│  a la vida, el universo y todo lo demás.                                    │
│                                                                             │
│  ¡Y resulta que 42 = 6 × 7 aparece en la masa del Higgs!                   │
│                                                                             │
│  Douglas Adams quizás estaba más cerca de la verdad de lo que pensaba.      │
│                                                                             │
│  El Higgs, que da masa a todo, tiene un ratio de masa con el protón        │
│  de aproximadamente 42π. El número 42 ESTÁ en la física fundamental.       │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘


═══════════════════════════════════════════════════════════════════════════════
5.5 EL PATRÓN DE LAS MASAS
═══════════════════════════════════════════════════════════════════════════════

Reuniendo todas las fórmulas de masas:
""")

    print(f"""
┌─────────────────────────────────────────────────────────────────────────────┐
│  TABLA: Masas de Partículas desde Klein                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   Partícula │ Ratio        │ Fórmula Klein    │ Error   │ Exponente de π   │
│   ──────────┼──────────────┼──────────────────┼─────────┼─────────────────  │
│   Protón    │ m_p/m_e      │ 6π⁵              │ 0.002%  │ 5                │
│   Higgs     │ m_H/m_p      │ 42.5π            │ 0.02%   │ 1                │
│   Muón      │ m_μ/m_e      │ 21π²             │ 0.24%   │ 2                │
│                                                                             │
│   PATRÓN EN LOS EXPONENTES: 1, 2, 5                                         │
│                                                                             │
│   ¡Son los primeros números de la secuencia de Fibonacci!                   │
│   (1, 1, 2, 3, 5, 8, 13, ...)                                               │
│                                                                             │
│   También son los primeros números primos: 2, 3, 5                          │
│   (exceptuando el 1)                                                        │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────────┐
│  CONCEPTO: La Jerarquía de Masas                                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Las masas de partículas varían enormemente:                                │
│                                                                             │
│  neutrino < electrón < muón < protón < Higgs < top quark                   │
│  ~0.05 eV    511 keV   106 MeV  938 MeV  125 GeV  173 GeV                   │
│                                                                             │
│  Ratio extremo: m_top / m_ν ~ 10¹²                                          │
│                                                                             │
│  ¿Por qué esta jerarquía? Klein responde:                                   │
│                                                                             │
│  • Cada tipo de partícula "siente" diferente número de capas               │
│  • Las supresiones (7π)⁻ⁿ generan la jerarquía                             │
│  • Los exponentes n siguen patrones matemáticos (Fibonacci, primos)        │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘


LOS COEFICIENTES (6, 21, 42.5):

    6    = 7 - 1       = capas activas
    21   = 3 × 7       = generaciones × capas
    42.5 = 6 × 7 + 0.5 = activas × totales + corrección

Todos involucran el número 7 (capas Klein).

El patrón es claro: las masas de partículas codifican la estructura
de 7 capas de la botella de Klein.


═══════════════════════════════════════════════════════════════════════════════
5.6 RESUMEN DEL CAPÍTULO
═══════════════════════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│  IDEAS CENTRALES:                                                           │
│                                                                             │
│  1. Las masas de partículas elementales tienen fórmulas Klein simples.      │
│                                                                             │
│  2. m_p/m_e = 6π⁵ con 0.002% de error (¡nuestra mejor predicción!)         │
│                                                                             │
│  3. m_H/m_p = 42.5π con 0.02% de error (el número 42 es real)              │
│                                                                             │
│  4. m_μ/m_e = 21π² con 0.24% de error                                      │
│                                                                             │
│  5. Los exponentes de π son 1, 2, 5 (Fibonacci/primos).                    │
│     Los coeficientes son 6, 21, 42.5 (todos involucran el 7).              │
│                                                                             │
│  ECUACIONES DEL CAPÍTULO:                                                   │
│                                                                             │
│     m_p/m_e = 6π⁵ = (7-1)π⁵                                                │
│     m_μ/m_e = 21π² = 3×7×π²                                                │
│     m_H/m_p = 42.5π = (6×7 + 1/2)π                                         │
│                                                                             │
│  PRÓXIMO CAPÍTULO:                                                          │
│                                                                             │
│  ¿Cómo explica Klein la cosmología: el CMB, la constante cosmológica,      │
│  y el número de Avogadro?                                                   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘


═══════════════════════════════════════════════════════════════════════════════
EJERCICIOS
═══════════════════════════════════════════════════════════════════════════════

1. Verifica que 6π⁵ ≈ 1836. ¿Cuál es el error exacto?

2. El tau (τ) es el leptón más pesado, con m_τ/m_e ≈ 3477.
   ¿Puedes encontrar una fórmula Klein para este número?
   (Pista: prueba con múltiplos de 7 y potencias de π)

3. Si el protón fuera más liviano (m_p/m_e = 1000), ¿cómo cambiaría
   la química? ¿Serían los átomos más grandes o más pequeños?

4. El número 42 aparece en la masa del Higgs. Investiga otros lugares
   en la física donde aparece 42 (o 6×7).


═══════════════════════════════════════════════════════════════════════════════
                          FIN DEL CAPÍTULO 5
═══════════════════════════════════════════════════════════════════════════════
""")


# =============================================================================
# CÓDIGO DE VERIFICACIÓN
# =============================================================================

def verificar_particulas():
    """
    Código ejecutable para verificar las predicciones del Capítulo 5.
    """
    print("\n" + "=" * 60)
    print("VERIFICACIÓN NUMÉRICA - CAPÍTULO 5")
    print("=" * 60)

    # Protón/electrón
    mp_me_obs = 1836.15267
    mp_me_klein = 6 * pi**5
    print(f"\nPROTÓN/ELECTRÓN:")
    print(f"  6π⁵ = 6 × {pi**5:.4f} = {mp_me_klein:.5f}")
    print(f"  Observado = {mp_me_obs:.5f}")
    print(f"  Error = {abs(mp_me_klein - mp_me_obs)/mp_me_obs*100:.4f}%")

    # Muón/electrón
    mu_me_obs = 206.7682830
    mu_me_klein = 21 * pi**2
    print(f"\nMUÓN/ELECTRÓN:")
    print(f"  21π² = 21 × {pi**2:.6f} = {mu_me_klein:.4f}")
    print(f"  Observado = {mu_me_obs:.4f}")
    print(f"  Error = {abs(mu_me_klein - mu_me_obs)/mu_me_obs*100:.3f}%")

    # Higgs/protón
    mH_mp_obs = 125250 / 938.27
    mH_mp_klein = 42.5 * pi
    print(f"\nHIGGS/PROTÓN:")
    print(f"  42.5π = 42.5 × {pi:.6f} = {mH_mp_klein:.4f}")
    print(f"  Observado = {mH_mp_obs:.4f}")
    print(f"  Error = {abs(mH_mp_klein - mH_mp_obs)/mH_mp_obs*100:.3f}%")

    # Resumen de coeficientes
    print(f"\nCOEFICIENTES Y SU RELACIÓN CON 7:")
    print(f"  6    = 7 - 1")
    print(f"  21   = 3 × 7")
    print(f"  42.5 = 6 × 7 + 0.5")


if __name__ == "__main__":
    mostrar_capitulo()
    verificar_particulas()
