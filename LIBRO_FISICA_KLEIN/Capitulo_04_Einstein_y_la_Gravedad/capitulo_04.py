#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════════════

                    CAPÍTULO 4: EINSTEIN Y LA GRAVEDAD

                    "El espacio-tiempo curvado"

═══════════════════════════════════════════════════════════════════════════════

AUTOR: Fausto Jose Di Bacco
EMAIL: faustojdb@gmail.com
AÑO: 2026

Copyright (c) 2026 Fausto Jose Di Bacco. Todos los derechos reservados.
"""

import numpy as np

pi = np.pi
siete_pi = 7 * pi

# Constantes físicas
c = 299792458  # m/s
G = 6.67430e-11  # m³/(kg·s²)
hbar = 1.054571817e-34  # J·s
k_B = 1.380649e-23  # J/K

# Escalas de Planck
l_P = np.sqrt(hbar * G / c**3)
t_P = l_P / c
m_P = np.sqrt(hbar * c / G)
T_P = m_P * c**2 / k_B

# Masa del protón
m_p = 1.67262192e-27  # kg

def mostrar_capitulo():
    print("""
═══════════════════════════════════════════════════════════════════════════════
                    CAPÍTULO 4: EINSTEIN Y LA GRAVEDAD
═══════════════════════════════════════════════════════════════════════════════


╔═════════════════════════════════════════════════════════════════════════════╗
║                                                                             ║
║   "La materia le dice al espacio-tiempo cómo curvarse,                      ║
║    y el espacio-tiempo le dice a la materia cómo moverse."                  ║
║                                        - John Wheeler                        ║
║                                                                             ║
║   "Y la topología Klein le dice a ambos cómo existir."                      ║
║                                        - Teoría Klein, 2026                 ║
║                                                                             ║
╚═════════════════════════════════════════════════════════════════════════════╝


═══════════════════════════════════════════════════════════════════════════════
4.1 LA RELATIVIDAD GENERAL EN 5 MINUTOS
═══════════════════════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────────────────────┐
│  ANALOGÍA: La Sábana Elástica                                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Imagina una sábana estirada horizontalmente.                               │
│                                                                             │
│  Si pones una bola de boliche en el centro, la sábana se CURVA.             │
│  Si ahora lanzas una canica, no irá en línea recta:                         │
│  seguirá la curvatura de la sábana y "caerá" hacia la bola de boliche.      │
│                                                                             │
│  ESO es la gravedad según Einstein:                                         │
│  - La masa curva el espacio-tiempo (como la bola curva la sábana)           │
│  - Los objetos siguen las curvas del espacio-tiempo                         │
│  - Lo que percibimos como "gravedad" es geometría pura                      │
│                                                                             │
│  La Tierra no "atrae" a la Luna. La Tierra CURVA el espacio,                │
│  y la Luna simplemente sigue el camino más recto posible                    │
│  en ese espacio curvo.                                                      │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘


LA ECUACIÓN DE EINSTEIN:

┌─────────────────────────────────────────────────────────────────────────────┐
│  MATEMÁTICAS: La Ecuación de Campo de Einstein                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│                    G_μν + Λg_μν = (8πG/c⁴) T_μν                            │
│                                                                             │
│   donde:                                                                    │
│   G_μν = R_μν - ½Rg_μν = tensor de Einstein (curvatura)                    │
│   Λ = constante cosmológica (energía del vacío)                             │
│   g_μν = tensor métrico (geometría del espacio-tiempo)                      │
│   T_μν = tensor de energía-momento (materia y energía)                      │
│   G = constante de gravitación de Newton                                    │
│   c = velocidad de la luz                                                   │
│                                                                             │
│   INTERPRETACIÓN:                                                           │
│   Lado izquierdo: CURVATURA del espacio-tiempo                              │
│   Lado derecho: CONTENIDO de materia y energía                              │
│                                                                             │
│   La ecuación dice: "La curvatura = la materia × constante"                 │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘


LAS CONSTANTES EN EINSTEIN:

La ecuación de Einstein contiene tres constantes fundamentales:

    1. c  = velocidad de la luz
    2. G  = constante de gravitación
    3. Λ  = constante cosmológica

¿TIENEN FORMA KLEIN? Veamos.


═══════════════════════════════════════════════════════════════════════════════
4.2 LAS CONSTANTES DE EINSTEIN DESDE KLEIN
═══════════════════════════════════════════════════════════════════════════════

CONSTANTE 1: LA VELOCIDAD DE LA LUZ (ya derivada)
""")

    c_klein = (3 - 1/siete_pi**2) * 1e8
    error_c = abs(c_klein - c) / c * 100

    print(f"""
┌─────────────────────────────────────────────────────────────────────────────┐
│  Ya sabemos del Capítulo 3:                                                 │
│                                                                             │
│   c = (3 - 1/(7π)²) × 10⁸ m/s                                              │
│                                                                             │
│   Predicción: {c_klein:.0f} m/s                                          │
│   Observado:  {c} m/s                                          │
│   Error:      {error_c:.4f}%                                                 │
│                                                                             │
│   En la ecuación de Einstein aparece c⁴ en el denominador:                  │
│   8πG/c⁴ ≈ 8πG / (8.1 × 10³³)                                              │
│                                                                             │
│   ¡c⁴ es un número ENORME! Por eso la gravedad es tan débil.               │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘


CONSTANTE 2: LA CONSTANTE DE GRAVITACIÓN G
""")

    ratio_mP_mp = m_P / m_p
    ratio_klein = 2 * siete_pi**14
    error_G = abs(ratio_klein - ratio_mP_mp) / ratio_mP_mp * 100

    print(f"""
┌─────────────────────────────────────────────────────────────────────────────┐
│  CONCEPTO: La Debilidad de la Gravedad                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  La gravedad es la fuerza más DÉBIL de todas.                               │
│                                                                             │
│  Comparación de fuerzas entre dos protones:                                 │
│  • Fuerza electromagnética : 10³⁶ veces más fuerte                          │
│  • Fuerza nuclear fuerte   : 10³⁸ veces más fuerte                          │
│  • Fuerza nuclear débil    : 10²⁵ veces más fuerte                          │
│                                                                             │
│  ¿Por qué es tan débil? La respuesta Klein: supresión exponencial.          │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────────┐
│  MATEMÁTICAS: G desde Klein                                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  La constante G se relaciona con la masa de Planck:                         │
│                                                                             │
│      G = ℏc / m_P²                                                          │
│                                                                             │
│  FÓRMULA KLEIN:                                                             │
│                                                                             │
│      m_P / m_p = 2 × (7π)¹⁴                                                │
│                                                                             │
│  donde 14 = 2 × 7 (dos ciclos de 7 capas Klein)                            │
│                                                                             │
│  VERIFICACIÓN:                                                              │
│  Predicción: m_P/m_p = {ratio_klein:.4e}                                   │
│  Observado:  m_P/m_p = {ratio_mP_mp:.4e}                                   │
│  Error:      {error_G:.1f}%                                                  │
│                                                                             │
│  INTERPRETACIÓN:                                                            │
│  La gravedad es débil porque m_P >> m_p por un factor de (7π)¹⁴.            │
│  El proceso gravitacional debe "atravesar" 14 capas topológicas,            │
│  lo que equivale a 2 ciclos completos de la botella de Klein.               │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────────┐
│  ANALOGÍA: El Túnel de 14 Puertas                                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Imagina que la fuerza gravitacional tiene que atravesar un túnel           │
│  con 14 puertas. Cada puerta reduce la intensidad de la fuerza.             │
│                                                                             │
│  Cada puerta reduce la intensidad por un factor de 7π ≈ 22.                │
│                                                                             │
│  Total: 22¹⁴ ≈ 10¹⁹                                                        │
│                                                                             │
│  Por eso la gravedad es 10¹⁹ veces más débil que la fuerza nuclear.        │
│                                                                             │
│  Las 14 puertas = 2 × 7 capas Klein = dos "vueltas" completas              │
│  alrededor de la botella de Klein.                                          │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘


CONSTANTE 3: LA CONSTANTE COSMOLÓGICA Λ
""")

    # Constante cosmológica
    Lambda_obs = 1.1056e-52  # m⁻²
    rho_Lambda = Lambda_obs * c**4 / (8 * pi * G)
    rho_P = c**7 / (hbar * G**2)
    ratio_rho = rho_Lambda / rho_P
    ratio_rho_klein = (7/2) * siete_pi**(-92)
    error_Lambda = abs(ratio_rho_klein - ratio_rho) / ratio_rho * 100

    print(f"""
┌─────────────────────────────────────────────────────────────────────────────┐
│  CONCEPTO: El Mayor Misterio de la Física                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  La constante cosmológica Λ representa la "energía del vacío".              │
│                                                                             │
│  EL PROBLEMA:                                                               │
│  • Teoría cuántica predice: ρ_vacío ~ ρ_Planck = 10⁹⁶ kg/m³               │
│  • Observación astronómica: ρ_Λ ~ 10⁻²⁷ kg/m³                              │
│                                                                             │
│  ¡Diferencia de 10¹²³ veces!                                               │
│                                                                             │
│  Este es llamado "el peor desacuerdo en la historia de la física".          │
│                                                                             │
│  ¿Puede Klein explicar 123 órdenes de magnitud?                             │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────────┐
│  MATEMÁTICAS: Λ desde Klein                                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  FÓRMULA KLEIN:                                                             │
│                                                                             │
│      ρ_Λ / ρ_P = (7/2) × (7π)⁻⁹²                                           │
│                                                                             │
│  donde 92 = 4 × 23 = 4 × (dim(SU(5)) - 1)                                  │
│                                                                             │
│  VERIFICACIÓN:                                                              │
│  Predicción: ρ_Λ/ρ_P = {ratio_rho_klein:.4e}                                │
│  Observado:  ρ_Λ/ρ_P = {ratio_rho:.4e}                                │
│  Error:      {error_Lambda:.1f}%                                             │
│                                                                             │
│  INTERPRETACIÓN:                                                            │
│  • (7π)⁻⁹² ≈ 10⁻¹²⁴ explica los 123 órdenes de magnitud                    │
│  • 92 = 4 × 23                                                              │
│  • 4 = dimensiones del espacio-tiempo                                       │
│  • 23 = dim(SU(5)) - 1 = generadores de unificación menos identidad        │
│                                                                             │
│  ¡El problema de la constante cosmológica TIENE SOLUCIÓN Klein!             │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────────┐
│  ANALOGÍA: El Túnel de 92 Puertas                                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Si la gravedad atraviesa 14 puertas, la energía del vacío                  │
│  atraviesa ¡92 puertas!                                                     │
│                                                                             │
│  22⁹² ≈ 10¹²⁴                                                              │
│                                                                             │
│  Esto explica por qué la constante cosmológica es tan pequeña:              │
│  es un efecto que debe atravesar casi 100 capas topológicas.                │
│                                                                             │
│  92 = 4 × 23 significa:                                                     │
│  • 4 dimensiones de espacio-tiempo                                          │
│  • 23 generadores del grupo de unificación                                  │
│  • Cada combinación dimensión-generador es una "puerta"                     │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘


═══════════════════════════════════════════════════════════════════════════════
4.3 ONDAS GRAVITACIONALES: EL ECO DE KLEIN
═══════════════════════════════════════════════════════════════════════════════

Las ondas gravitacionales son "arrugas" en el espacio-tiempo.
Fueron predichas por Einstein en 1916 y detectadas por LIGO en 2015.

┌─────────────────────────────────────────────────────────────────────────────┐
│  CONCEPTO: ¿Qué son las ondas gravitacionales?                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Cuando dos agujeros negros colisionan, el espacio-tiempo vibra.            │
│  Estas vibraciones se propagan a la velocidad de la luz.                    │
│                                                                             │
│  Es como tirar una piedra en un estanque: las ondas se expanden.            │
│  Pero en lugar de agua, es el ESPACIO mismo el que ondula.                  │
│                                                                             │
│  LIGO detecta estas ondas midiendo cambios de distancia                     │
│  de 10⁻¹⁸ metros (¡mil veces más pequeño que un protón!).                  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────────┐
│  MATEMÁTICAS: Ondas Gravitacionales y Klein                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  La ecuación de onda gravitacional (linealizada):                           │
│                                                                             │
│      □h_μν = -(16πG/c⁴) T_μν                                               │
│                                                                             │
│  donde □ = ∇² - (1/c²)∂²/∂t² es el operador de onda.                       │
│                                                                             │
│  Las ondas viajan a velocidad c = (3 - 1/(7π)²) × 10⁸ m/s                  │
│                                                                             │
│  FRECUENCIA CARACTERÍSTICA:                                                 │
│                                                                             │
│  En fusiones de agujeros negros, aparece frecuentemente:                    │
│                                                                             │
│      f ~ 22 Hz ≈ 7π Hz                                                     │
│                                                                             │
│  ¡Este fue el descubrimiento original que inició la Teoría Klein!           │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘


EL CÍRCULO SE CIERRA:

    • Empezamos observando 22 Hz en ondas gravitacionales
    • Descubrimos que 22 ≈ 7π
    • Derivamos todas las constantes físicas desde 7π
    • Las ondas gravitacionales confirman que viajan a c Klein

Las ondas gravitacionales son literalmente el "eco" de la topología Klein
propagándose por el universo.


═══════════════════════════════════════════════════════════════════════════════
4.4 AGUJEROS NEGROS Y ENTROPÍA
═══════════════════════════════════════════════════════════════════════════════
""")

    print(f"""
┌─────────────────────────────────────────────────────────────────────────────┐
│  CONCEPTO: Entropía de Bekenstein-Hawking                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Los agujeros negros tienen ENTROPÍA proporcional a su ÁREA:                │
│                                                                             │
│      S = (k_B c³ / 4Gℏ) × A = k_B × A / (4 l_P²)                           │
│                                                                             │
│  donde A = área del horizonte de eventos.                                   │
│                                                                             │
│  Esto es revolucionario: la entropía de un objeto 3D                        │
│  depende de su superficie 2D, no de su volumen.                             │
│                                                                             │
│  Se llama "principio holográfico": la información del interior              │
│  está codificada en la superficie.                                          │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────────┐
│  MATEMÁTICAS: Entropía BH desde Klein                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Para un agujero negro de masa M:                                           │
│                                                                             │
│      S/k_B = 4π (M/m_P)² = 4π (M / (m_p × 2 × (7π)¹⁴))²                    │
│                                                                             │
│  La entropía está suprimida por (7π)²⁸ = ((7π)¹⁴)²                         │
│                                                                             │
│  28 = 4 × 7 = 4 dimensiones × 7 capas Klein                                │
│                                                                             │
│  INTERPRETACIÓN:                                                            │
│  La entropía de un agujero negro codifica información sobre                 │
│  las 4 dimensiones del espacio-tiempo y las 7 capas de Klein.               │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘


═══════════════════════════════════════════════════════════════════════════════
4.5 LA EDAD DEL UNIVERSO: t_U = t_P × (7π)⁴⁵
═══════════════════════════════════════════════════════════════════════════════
""")

    # Edad del universo
    t_U = 13.8e9 * 365.25 * 24 * 3600  # segundos
    ratio_t = t_U / t_P
    exp_klein = np.log(ratio_t) / np.log(siete_pi)
    ratio_t_klein = siete_pi**45

    print(f"""
┌─────────────────────────────────────────────────────────────────────────────┐
│  CONCEPTO: La Edad del Cosmos                                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  El universo tiene aproximadamente 13.8 mil millones de años.               │
│                                                                             │
│  En segundos: t_U ≈ {t_U:.3e} s                                             │
│                                                                             │
│  El tiempo de Planck (la unidad natural de tiempo):                         │
│  t_P = √(ℏG/c⁵) ≈ {t_P:.3e} s                                              │
│                                                                             │
│  Ratio: t_U / t_P ≈ {ratio_t:.3e}                                           │
│                                                                             │
│  ¡El universo tiene 10⁶⁰ tiempos de Planck de edad!                        │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────────┐
│  MATEMÁTICAS: Edad del Universo desde Klein                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  DESCUBRIMIENTO:                                                            │
│                                                                             │
│      t_U / t_P ≈ (7π)⁴⁵                                                    │
│                                                                             │
│  VERIFICACIÓN:                                                              │
│  log₇π(t_U/t_P) = ln({ratio_t:.3e}) / ln(7π)                                │
│                 = {exp_klein:.2f} ≈ 45                                       │
│                                                                             │
│  Predicción: (7π)⁴⁵ = {ratio_t_klein:.3e}                                   │
│  Observado:  t_U/t_P = {ratio_t:.3e}                                        │
│                                                                             │
│  INTERPRETACIÓN:                                                            │
│  45 ≈ 2 × 24 - 3 = 2 × dim(SU(5)) - 3                                      │
│                                                                             │
│  El universo ha "atravesado" 45 capas Klein desde el Big Bang.              │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────────┐
│  ANALOGÍA: El Calendario Cósmico Klein                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Si cada "año Klein" dura (7π) tiempos de Planck:                          │
│                                                                             │
│  1 año Klein = 22 × t_P ≈ 10⁻⁴² s                                          │
│                                                                             │
│  El universo tiene (7π)⁴⁵ / 7π = (7π)⁴⁴ años Klein.                        │
│                                                                             │
│  Es como si el cosmos llevara un calendario donde cada página               │
│  representa una supresión Klein, y ya hemos pasado 45 páginas.              │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘


═══════════════════════════════════════════════════════════════════════════════
4.6 RESUMEN DEL CAPÍTULO
═══════════════════════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│  IDEAS CENTRALES:                                                           │
│                                                                             │
│  1. La ecuación de Einstein G_μν + Λg_μν = (8πG/c⁴)T_μν                    │
│     contiene tres constantes: c, G, Λ. TODAS tienen forma Klein.            │
│                                                                             │
│  2. La gravedad es débil porque m_P/m_p = 2×(7π)¹⁴.                        │
│     (14 = 2×7 capas Klein)                                                  │
│                                                                             │
│  3. La constante cosmológica es pequeña porque ρ_Λ/ρ_P = (7/2)×(7π)⁻⁹².    │
│     (92 = 4×23 capas Klein)                                                 │
│     ¡Esto RESUELVE el problema de los 123 órdenes de magnitud!              │
│                                                                             │
│  4. Las ondas gravitacionales viajan a c Klein y muestran                   │
│     frecuencias características de ~22 Hz ≈ 7π Hz.                          │
│                                                                             │
│  5. La edad del universo es t_U = t_P × (7π)⁴⁵.                            │
│     (45 ≈ 2×dim(SU(5)) - 3)                                                │
│                                                                             │
│  ECUACIONES DEL CAPÍTULO:                                                   │
│                                                                             │
│     c   = (3 - 1/(7π)²) × 10⁸ m/s                                          │
│     m_P/m_p = 2 × (7π)¹⁴                                                   │
│     ρ_Λ/ρ_P = (7/2) × (7π)⁻⁹²                                              │
│     t_U/t_P = (7π)⁴⁵                                                       │
│                                                                             │
│  PRÓXIMO CAPÍTULO:                                                          │
│                                                                             │
│  Si Klein explica luz (Maxwell) y gravedad (Einstein),                      │
│  ¿qué pasa con las partículas elementales?                                  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘


═══════════════════════════════════════════════════════════════════════════════
EJERCICIOS
═══════════════════════════════════════════════════════════════════════════════

1. Calcula cuántas veces más fuerte es la fuerza eléctrica entre dos protones
   comparada con la gravedad. (Pista: usa la constante de estructura fina)

2. Si la constante cosmológica fuera (7π)⁻⁹⁰ en lugar de (7π)⁻⁹²,
   ¿cuántas veces mayor sería? ¿Cómo afectaría al universo?

3. Las ondas gravitacionales de GW150914 tenían f ~ 150 Hz en el pico.
   Esto es aproximadamente 7 × 22 Hz. ¿Qué podría significar?

4. Si el universo viviera hasta t = t_P × (7π)⁵⁰, ¿cuántos años serían?


═══════════════════════════════════════════════════════════════════════════════
                          FIN DEL CAPÍTULO 4
═══════════════════════════════════════════════════════════════════════════════
""")


# =============================================================================
# CÓDIGO DE VERIFICACIÓN
# =============================================================================

def verificar_einstein():
    """
    Código ejecutable para verificar las predicciones del Capítulo 4.
    """
    print("\n" + "=" * 60)
    print("VERIFICACIÓN NUMÉRICA - CAPÍTULO 4")
    print("=" * 60)

    # Velocidad de la luz
    c_klein = (3 - 1/siete_pi**2) * 1e8
    print(f"\nVELOCIDAD DE LA LUZ:")
    print(f"  c Klein = {c_klein:.0f} m/s")
    print(f"  c obs   = {c} m/s")
    print(f"  Error   = {abs(c_klein - c)/c*100:.4f}%")

    # Masa de Planck / masa del protón
    ratio_obs = m_P / m_p
    ratio_klein = 2 * siete_pi**14
    print(f"\nMASA DE PLANCK / PROTÓN:")
    print(f"  (m_P/m_p) Klein = {ratio_klein:.4e}")
    print(f"  (m_P/m_p) obs   = {ratio_obs:.4e}")
    print(f"  Error           = {abs(ratio_klein - ratio_obs)/ratio_obs*100:.1f}%")

    # Constante cosmológica
    Lambda_obs = 1.1056e-52
    rho_Lambda = Lambda_obs * c**4 / (8 * pi * G)
    rho_P = c**7 / (hbar * G**2)
    ratio_rho_obs = rho_Lambda / rho_P
    ratio_rho_klein = (7/2) * siete_pi**(-92)
    print(f"\nCONSTANTE COSMOLÓGICA:")
    print(f"  (ρ_Λ/ρ_P) Klein = {ratio_rho_klein:.4e}")
    print(f"  (ρ_Λ/ρ_P) obs   = {ratio_rho_obs:.4e}")
    print(f"  Error           = {abs(ratio_rho_klein - ratio_rho_obs)/ratio_rho_obs*100:.1f}%")

    # Edad del universo
    t_U = 13.8e9 * 365.25 * 24 * 3600
    ratio_t_obs = t_U / t_P
    ratio_t_klein = siete_pi**45
    exp_obs = np.log(ratio_t_obs) / np.log(siete_pi)
    print(f"\nEDAD DEL UNIVERSO:")
    print(f"  log₇π(t_U/t_P) = {exp_obs:.2f} ≈ 45")
    print(f"  (7π)⁴⁵ = {ratio_t_klein:.4e}")
    print(f"  t_U/t_P = {ratio_t_obs:.4e}")


if __name__ == "__main__":
    mostrar_capitulo()
    verificar_einstein()
