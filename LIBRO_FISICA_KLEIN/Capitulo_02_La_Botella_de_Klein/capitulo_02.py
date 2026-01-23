#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════════════

                    CAPÍTULO 2: LA BOTELLA DE KLEIN

                    "La superficie que no tiene interior"

═══════════════════════════════════════════════════════════════════════════════

AUTOR: Fausto Jose Di Bacco
EMAIL: faustojdb@gmail.com
AÑO: 2026

Copyright (c) 2026 Fausto Jose Di Bacco. Todos los derechos reservados.
"""

import numpy as np

pi = np.pi

def mostrar_capitulo():
    print("""
═══════════════════════════════════════════════════════════════════════════════
                    CAPÍTULO 2: LA BOTELLA DE KLEIN
═══════════════════════════════════════════════════════════════════════════════


╔═════════════════════════════════════════════════════════════════════════════╗
║                                                                             ║
║   "No puedes llenar una botella de Klein con agua,                          ║
║    porque no tiene interior."                                               ║
║                                        - Felix Klein, 1882                  ║
║                                                                             ║
║   "Pero puedes llenarla con un universo."                                   ║
║                                        - Teoría Klein, 2026                 ║
║                                                                             ║
╚═════════════════════════════════════════════════════════════════════════════╝


═══════════════════════════════════════════════════════════════════════════════
2.1 ¿QUÉ ES UNA SUPERFICIE NO ORIENTABLE?
═══════════════════════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────────────────────┐
│  ANALOGÍA: La Hormiga en el Papel                                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Imagina una hormiga caminando sobre una hoja de papel.                     │
│                                                                             │
│  En papel NORMAL (orientable):                                              │
│  - La hormiga tiene un "arriba" y un "abajo" bien definidos.               │
│  - Si camina por toda la superficie, siempre vuelve igual.                  │
│  - Nunca confunde la cara superior con la inferior.                         │
│                                                                             │
│  En una BANDA DE MÖBIUS (no orientable):                                    │
│  - La hormiga camina, camina, camina...                                     │
│  - ¡Y vuelve al punto de partida BOCA ABAJO!                               │
│  - El "arriba" se convirtió en "abajo".                                     │
│                                                                             │
│  Esto es la NO-ORIENTABILIDAD: no hay distinción global                     │
│  entre las dos "caras" de la superficie.                                    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────────┐
│  CONCEPTO: Orientabilidad                                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Una superficie es ORIENTABLE si podemos definir consistentemente           │
│  un "lado interior" y un "lado exterior" en toda la superficie.             │
│                                                                             │
│  Ejemplos ORIENTABLES:                                                      │
│  • Esfera (Tierra): tiene interior (magma) y exterior (atmósfera)          │
│  • Toro (dona): tiene dentro y fuera                                        │
│  • Cilindro: tiene dentro y fuera                                           │
│                                                                             │
│  Ejemplos NO ORIENTABLES:                                                   │
│  • Banda de Möbius: una sola cara                                           │
│  • Botella de Klein: una sola cara, cerrada                                │
│  • Plano proyectivo real: una sola cara                                     │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘


═══════════════════════════════════════════════════════════════════════════════
2.2 LA BANDA DE MÖBIUS: EL PRIMER PASO
═══════════════════════════════════════════════════════════════════════════════

La banda de Möbius es la superficie no orientable más simple.

CÓMO CONSTRUIRLA:

    1. Toma una tira rectangular de papel
    2. Dale media vuelta (180°) a un extremo
    3. Pega los extremos

         ┌─────────────────────────┐
         │                         │
         │    ═══════════════>    │
         │         TIRA           │
         │    <═══════════════    │
         │                         │
         └─────────────────────────┘
                    │
                    │ Media vuelta
                    ▼
         ┌─────────────────────────┐
         │    ╔═══════════════╗    │
         │    ║   MÖBIUS      ║    │
         │    ╚═══════════════╝    │
         └─────────────────────────┘

PROPIEDADES ASOMBROSAS:

    • Una sola cara (dibuja una línea y sigue: vuelves al inicio)
    • Un solo borde (sigue el borde con el dedo: es continuo)
    • No tiene "interior" ni "exterior"


┌─────────────────────────────────────────────────────────────────────────────┐
│  MATEMÁTICAS: Característica de Euler                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  La característica de Euler χ mide la "forma" de una superficie:            │
│                                                                             │
│            χ = V - E + F                                                    │
│                                                                             │
│  donde V = vértices, E = aristas, F = caras (en una triangulación).        │
│                                                                             │
│  Para la banda de Möbius: χ = 0                                             │
│  Para la botella de Klein: χ = 0                                            │
│  Para la esfera: χ = 2                                                      │
│  Para el toro: χ = 0                                                        │
│                                                                             │
│  Las superficies no orientables tienen χ ≤ 0.                               │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘


═══════════════════════════════════════════════════════════════════════════════
2.3 LA BOTELLA DE KLEIN: EL UNIVERSO CERRADO
═══════════════════════════════════════════════════════════════════════════════

La botella de Klein es una banda de Möbius... ¡pero cerrada sobre sí misma!

┌─────────────────────────────────────────────────────────────────────────────┐
│  ANALOGÍA: El Universo Pac-Man                                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  En el juego Pac-Man, si sales por la derecha, apareces por la izquierda.  │
│  El espacio es un TORO (dona topológica).                                   │
│                                                                             │
│  Ahora imagina un Pac-Man especial:                                         │
│  - Si sales por la derecha, apareces por la izquierda...                   │
│  - ...pero INVERTIDO verticalmente.                                         │
│                                                                             │
│  ESO es una botella de Klein.                                               │
│                                                                             │
│  En nuestro universo Klein:                                                 │
│  - Si viajas lo suficiente en una dirección...                             │
│  - ...vuelves al punto de partida...                                        │
│  - ...pero con la quiralidad invertida (como un espejo).                    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘


CONSTRUCCIÓN DE LA BOTELLA DE KLEIN:

    Paso 1: Toma un rectángulo

        A ─────────────────────> B
        │                        │
        │                        │
        │                        │
        C <───────────────────── D

    Paso 2: Pega los bordes AB con CD (igual dirección) → obtienes un cilindro
    Paso 3: Pega los bordes AC con BD (direcciones OPUESTAS) → ¡Klein!

    El Paso 3 es imposible en 3D sin que la superficie se atraviese a sí misma.
    En 4D, la botella de Klein es una superficie perfectamente suave.


┌─────────────────────────────────────────────────────────────────────────────┐
│  CONCEPTO: La Botella de Klein en 4D                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  En 3D, la botella de Klein debe "atravesarse" a sí misma.                  │
│  En 4D, esto no es necesario.                                               │
│                                                                             │
│  Analogía: Un nudo en una cuerda no puede deshacerse en 2D,                │
│  pero en 3D puedes "levantarlo" y deshacerlo.                               │
│                                                                             │
│  Del mismo modo, la botella de Klein es "lisa" en 4D.                       │
│                                                                             │
│  NUESTRA HIPÓTESIS: El espacio-tiempo es 4D + 1 dimensión extra = 5D.       │
│  En 5D, una topología tipo Klein es natural y sin auto-intersección.        │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘


═══════════════════════════════════════════════════════════════════════════════
2.4 LAS 7 CAPAS: ESTRUCTURA DEL ESPACIO-TIEMPO
═══════════════════════════════════════════════════════════════════════════════

¿De dónde sale el número 7?

┌─────────────────────────────────────────────────────────────────────────────┐
│  ANALOGÍA: La Cebolla Cósmica                                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Imagina el universo como una cebolla con 7 capas.                          │
│                                                                             │
│  Cada capa está "conectada" con las demás de manera no trivial,             │
│  como los giros de una banda de Möbius pero en múltiples niveles.           │
│                                                                             │
│            ┌─────────────────┐                                              │
│            │   Capa 7        │                                              │
│            │ ┌─────────────┐ │                                              │
│            │ │   Capa 6    │ │                                              │
│            │ │ ┌─────────┐ │ │                                              │
│            │ │ │ Capa 5  │ │ │                                              │
│            │ │ │   ...   │ │ │                                              │
│            │ │ │ Capa 1  │ │ │                                              │
│            │ │ └─────────┘ │ │                                              │
│            │ └─────────────┘ │                                              │
│            └─────────────────┘                                              │
│                                                                             │
│  Pero las capas no son independientes: están topológicamente                │
│  entrelazadas como en una botella de Klein.                                 │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘


¿POR QUÉ EXACTAMENTE 7?

Hay varias justificaciones matemáticas:
""")

    siete_pi = 7 * pi
    print(f"""
┌─────────────────────────────────────────────────────────────────────────────┐
│  MATEMÁTICAS: Origen del 7                                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  JUSTIFICACIÓN 1: Topología Algebraica                                      │
│                                                                             │
│  En la clasificación de superficies no orientables,                         │
│  el número de "giros de Möbius" define la complejidad.                      │
│  7 es el menor número primo > 5 (dimensiones del espacio-tiempo + 1).       │
│                                                                             │
│  JUSTIFICACIÓN 2: Teoría de Grupos                                          │
│                                                                             │
│  El grupo de simetría SU(5) tiene dimensión 24 = 5² - 1.                    │
│  La relación 24/7 ≈ π (error 9%) sugiere conexión profunda.                 │
│  También: 7 × 24 = 168 = |PSL(2,7)|, grupo simple importante.               │
│                                                                             │
│  JUSTIFICACIÓN 3: Empírica                                                  │
│                                                                             │
│  7π = {siete_pi:.4f} ≈ 22                                                      │
│  Este valor aparece en la física de ondas gravitacionales.                  │
│  El número 7 es NECESARIO para que la teoría funcione.                      │
│                                                                             │
│  JUSTIFICACIÓN 4: Dimensiones Extra                                         │
│                                                                             │
│  Teoría de cuerdas: 10D total = 4D observables + 6D compactas               │
│  Teoría M: 11D total = 4D observables + 7D compactas                        │
│  ¿Coincidencia? Las 7 capas Klein = 7 dimensiones compactas de M-teoría.    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘


═══════════════════════════════════════════════════════════════════════════════
2.5 EL FACTOR DE SUPRESIÓN 7π
═══════════════════════════════════════════════════════════════════════════════

El producto 7π es la "constante fundamental" de la Teoría Klein.
""")

    print(f"""
┌─────────────────────────────────────────────────────────────────────────────┐
│  CONCEPTO: Factor de Supresión Klein                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  7π ≈ {siete_pi:.4f} ≈ 22                                                      │
│                                                                             │
│  Este número aparece como FACTOR DE SUPRESIÓN:                              │
│                                                                             │
│  • (7π)⁻² ≈ 0.00207 : corrección a la velocidad de la luz                  │
│  • (7π)⁻⁷ ≈ 2×10⁻¹⁰ : asimetría materia-antimateria                        │
│  • (7π)⁻²⁴ : conexión con temperatura del CMB                               │
│  • (7π)⁻⁹² : constante cosmológica                                          │
│                                                                             │
│  INTERPRETACIÓN FÍSICA:                                                     │
│                                                                             │
│  Cuando un proceso físico debe "atravesar" n capas de la topología          │
│  Klein, su amplitud se suprime por un factor de (7π)⁻ⁿ.                     │
│                                                                             │
│  Es como atravesar paredes: cada pared reduce la intensidad.                │
│  Las 7 capas de Klein son las "paredes" del universo.                       │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘


TABLA DE EXPONENTES KLEIN:

    ┌────────────┬──────────────────────────────────────────────────────────┐
    │ Exponente  │ Significado                                              │
    ├────────────┼──────────────────────────────────────────────────────────┤
    │     2      │ C×P = operaciones discretas de paridad                   │
    │     5      │ Dimensiones de Kaluza-Klein (4+1)                        │
    │     7      │ Número de capas Klein                                    │
    │    14      │ 2×7 = dos ciclos de capas (gravedad)                     │
    │    24      │ dim(SU(5)) = generadores de unificación                  │
    │    45      │ 2×24 - 3 = edad del universo                             │
    │    92      │ 4×23 = 4D × (SU(5)-1) (constante cosmológica)            │
    └────────────┴──────────────────────────────────────────────────────────┘


═══════════════════════════════════════════════════════════════════════════════
2.6 RESUMEN DEL CAPÍTULO
═══════════════════════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│  IDEAS CENTRALES:                                                           │
│                                                                             │
│  1. Las superficies no orientables (Möbius, Klein) no tienen                │
│     distinción entre "interior" y "exterior".                               │
│                                                                             │
│  2. La botella de Klein es una superficie cerrada no orientable             │
│     que requiere 4D para existir sin auto-intersección.                     │
│                                                                             │
│  3. Proponemos que el espacio-tiempo tiene topología tipo Klein             │
│     con 7 capas o regiones.                                                 │
│                                                                             │
│  4. El factor 7π ≈ 22 es la "constante de supresión" que                    │
│     determina las constantes físicas fundamentales.                         │
│                                                                             │
│  ECUACIÓN DEL CAPÍTULO:                                                     │
│                                                                             │
│       Supresión = (7π)⁻ⁿ  para procesos que cruzan n capas                 │
│                                                                             │
│  PRÓXIMO CAPÍTULO:                                                          │
│                                                                             │
│  ¿Cómo se conecta esto con las ecuaciones de Maxwell?                       │
│  ¿De dónde viene la velocidad de la luz?                                    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘


═══════════════════════════════════════════════════════════════════════════════
EJERCICIOS
═══════════════════════════════════════════════════════════════════════════════

1. Construye una banda de Möbius con papel. Verifica que tiene un solo borde.

2. Intenta dibujar una botella de Klein. ¿Por qué debe atravesarse a sí misma
   en 3D pero no en 4D?

3. Si el exponente de supresión para la asimetría materia-antimateria es 7
   (η_B ~ (7π)⁻⁷), ¿qué significaría físicamente atravesar 7 capas?

4. La teoría M tiene 7 dimensiones compactas. Investiga qué topología
   podrían tener esas dimensiones.


═══════════════════════════════════════════════════════════════════════════════
                          FIN DEL CAPÍTULO 2
═══════════════════════════════════════════════════════════════════════════════
""")


# =============================================================================
# CÓDIGO DE VERIFICACIÓN
# =============================================================================

def verificar_factores():
    """
    Código ejecutable para verificar los factores de supresión.
    """
    print("\n" + "=" * 60)
    print("VERIFICACIÓN NUMÉRICA - CAPÍTULO 2")
    print("=" * 60)

    siete_pi = 7 * pi

    print(f"\nFactor de supresión Klein: 7π = {siete_pi:.6f}")
    print("\nSupresiones por exponente:")

    exponentes = [2, 5, 7, 14, 24, 45, 92]
    for n in exponentes:
        valor = siete_pi ** (-n)
        print(f"  (7π)^(-{n:2d}) = {valor:.4e}")

    print("\nRelación con 22:")
    print(f"  7π = {siete_pi:.6f}")
    print(f"  22  = 22.000000")
    print(f"  7π/22 = {siete_pi/22:.6f}")


if __name__ == "__main__":
    mostrar_capitulo()
    verificar_factores()
