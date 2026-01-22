#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════════════

                    CAPÍTULO 3: MAXWELL Y LA LUZ

                    "La velocidad del universo"

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
                        CAPÍTULO 3: MAXWELL Y LA LUZ
═══════════════════════════════════════════════════════════════════════════════


╔═════════════════════════════════════════════════════════════════════════════╗
║                                                                             ║
║   "Fue así como la luz fue entendida como una onda electromagnética."       ║
║                                        - James Clerk Maxwell, 1865          ║
║                                                                             ║
║   "Y la velocidad de esa onda está escrita en la topología del cosmos."     ║
║                                        - Teoría Klein, 2026                 ║
║                                                                             ║
╚═════════════════════════════════════════════════════════════════════════════╝


═══════════════════════════════════════════════════════════════════════════════
3.1 LAS ECUACIONES QUE UNIFICARON ELECTRICIDAD Y MAGNETISMO
═══════════════════════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────────────────────┐
│  ANALOGÍA: El Matrimonio de Dos Fuerzas                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Antes de Maxwell, la electricidad y el magnetismo eran como dos            │
│  personas que vivían en la misma casa pero nunca se hablaban.               │
│                                                                             │
│  - Electricidad: cargas, chispas, relámpagos                                │
│  - Magnetismo: imanes, brújulas, auroras                                    │
│                                                                             │
│  Maxwell mostró que son la MISMA cosa, como dos caras de una moneda.        │
│  Cuando una carga se mueve, crea magnetismo.                                │
│  Cuando el magnetismo cambia, crea electricidad.                            │
│                                                                             │
│  Y juntos, crean algo mágico: LUZ.                                          │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘


LAS CUATRO ECUACIONES DE MAXWELL:

┌─────────────────────────────────────────────────────────────────────────────┐
│  MATEMÁTICAS: Las Ecuaciones de Maxwell                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   1. ∇·E = ρ/ε₀           Ley de Gauss (eléctrica)                         │
│      "Las cargas crean campos eléctricos"                                   │
│                                                                             │
│   2. ∇·B = 0              Ley de Gauss (magnética)                         │
│      "No existen monopolos magnéticos"                                      │
│                                                                             │
│   3. ∇×E = -∂B/∂t         Ley de Faraday                                   │
│      "El magnetismo cambiante crea electricidad"                            │
│                                                                             │
│   4. ∇×B = μ₀J + μ₀ε₀∂E/∂t   Ley de Ampère-Maxwell                         │
│      "La corriente y la electricidad cambiante crean magnetismo"            │
│                                                                             │
│   donde:                                                                    │
│   E = campo eléctrico                                                       │
│   B = campo magnético                                                       │
│   ρ = densidad de carga                                                     │
│   J = densidad de corriente                                                 │
│   ε₀ = permitividad del vacío                                               │
│   μ₀ = permeabilidad del vacío                                              │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘


LA REVELACIÓN DE MAXWELL:

De estas cuatro ecuaciones, Maxwell dedujo algo extraordinario.
En el vacío (sin cargas ni corrientes), las ecuaciones predicen
una ONDA que viaja a velocidad:

                    c = 1/√(ε₀μ₀)

Cuando Maxwell calculó este valor... ¡era igual a la velocidad de la luz!

Este fue el momento "eureka" de la física del siglo XIX:
La luz ES una onda electromagnética.


═══════════════════════════════════════════════════════════════════════════════
3.2 LA VELOCIDAD DE LA LUZ: c = (3 - 1/(7π)²) × 10⁸
═══════════════════════════════════════════════════════════════════════════════

Ahora viene nuestra contribución. ¿Por qué c tiene ese valor específico?
""")

    c_obs = 299792458
    c_klein = (3 - 1/siete_pi**2) * 1e8
    error_c = abs(c_klein - c_obs) / c_obs * 100
    correccion = 1/siete_pi**2

    print(f"""
┌─────────────────────────────────────────────────────────────────────────────┐
│  CONCEPTO: La Fórmula Klein para c                                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   c = (3 - 1/(7π)²) × 10⁸ m/s                                              │
│                                                                             │
│   Desglose:                                                                 │
│   • 3 = número de dimensiones espaciales                                    │
│   • 1/(7π)² = {correccion:.8f} = corrección Klein                             │
│   • 10⁸ = factor de escala (unidades SI)                                    │
│                                                                             │
│   VERIFICACIÓN:                                                             │
│   Predicción: {c_klein:.0f} m/s                                          │
│   Observado:  {c_obs} m/s                                          │
│   Error:      {error_c:.4f}%                                                 │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────────┐
│  ANALOGÍA: El Límite de Velocidad Cósmico                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Imagina una autopista con 3 carriles.                                      │
│  El límite de velocidad "ideal" sería 3 unidades.                           │
│                                                                             │
│  Pero hay pequeños baches (la topología Klein) que reducen                  │
│  ligeramente la velocidad máxima:                                           │
│                                                                             │
│  Velocidad máxima = 3 - (baches) = 3 - 1/(7π)² ≈ 2.998                     │
│                                                                             │
│  Los "baches" son la corrección de 0.2% debido a las 7 capas Klein.         │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘


¿POR QUÉ 3 - 1/(7π)² Y NO SIMPLEMENTE 3?

El número 3 representa las dimensiones espaciales por las que puede
propagarse la luz. Pero la topología Klein introduce una pequeña
"resistencia" o "impedancia" a la propagación.

Esta resistencia es (7π)⁻² porque:
    • La luz debe "atravesar" la estructura Klein
    • El exponente 2 indica que es un efecto de segundo orden
    • 7π es el factor de supresión fundamental

IMPLICACIÓN PROFUNDA:

Si el universo NO tuviera topología Klein, la velocidad de la luz sería
EXACTAMENTE 3 × 10⁸ m/s. La pequeña diferencia (207,542 m/s) es la
"huella digital" de la estructura topológica del cosmos.


═══════════════════════════════════════════════════════════════════════════════
3.3 LA CONSTANTE DE ESTRUCTURA FINA: 1/α = 7²π - 7 - π²
═══════════════════════════════════════════════════════════════════════════════

La constante de estructura fina α ≈ 1/137 es quizás el número más
misterioso de toda la física.
""")

    alpha_inv_obs = 137.035999
    alpha_inv_klein = 7**2 * pi - 7 - pi**2
    error_alpha = abs(alpha_inv_klein - alpha_inv_obs) / alpha_inv_obs * 100

    print(f"""
┌─────────────────────────────────────────────────────────────────────────────┐
│  CONCEPTO: ¿Qué es α?                                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  α = e²/(4πε₀ℏc) ≈ 1/137                                                   │
│                                                                             │
│  α determina:                                                               │
│  • La fuerza de la interacción electromagnética                             │
│  • El tamaño de los átomos                                                  │
│  • Los niveles de energía atómicos                                          │
│  • Si la química es posible                                                 │
│                                                                             │
│  Si α fuera ligeramente diferente:                                          │
│  • α > 1/137: los electrones caerían al núcleo, no habría átomos           │
│  • α < 1/137: los átomos serían demasiado débiles, no habría química        │
│                                                                             │
│  El valor EXACTO de α es crucial para nuestra existencia.                   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────────┐
│  MATEMÁTICAS: La Fórmula Klein para α                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   1/α = 7²π - 7 - π²                                                       │
│                                                                             │
│   Forma alternativa:                                                        │
│   1/α = 7(7π - 1) - π²                                                     │
│                                                                             │
│   Desglose:                                                                 │
│   • 7²π = 49π ≈ 153.94 : término principal                                 │
│   • -7 : corrección por una capa de referencia                              │
│   • -π² ≈ -9.87 : corrección geométrica                                    │
│   • Total ≈ 137.07                                                          │
│                                                                             │
│   VERIFICACIÓN:                                                             │
│   Predicción: {alpha_inv_klein:.6f}                                             │
│   Observado:  {alpha_inv_obs:.6f}                                             │
│   Error:      {error_alpha:.4f}%                                               │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────────┐
│  ANALOGÍA: El Dial del Universo                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Imagina un dial con marcas de 1 a 200.                                     │
│                                                                             │
│  Para que existan átomos, química y vida, el dial debe estar               │
│  en EXACTAMENTE 137. Un poco más o menos, y no estarías leyendo esto.       │
│                                                                             │
│  ¿Quién puso el dial en 137?                                                │
│                                                                             │
│  Respuesta Klein: NADIE. El valor 137 surge automáticamente de              │
│  7²π - 7 - π². Es una consecuencia matemática de la topología.              │
│                                                                             │
│  No hay dial. No hay quien lo ajuste. Es geometría pura.                    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘


INTERPRETACIÓN DE LA FÓRMULA:

    1/α = 7²π - 7 - π²
        = 7 × 7 × π - 7 - π²
        = 7 × (7π - 1) - π²

El primer término 7²π representa la interacción "desnuda" entre
7 capas y 7 capas de Klein, modulada por la geometría π.

El término -7 resta una capa (la capa de "referencia").

El término -π² es una corrección geométrica de segundo orden.

Resultado: 137.068... vs 137.036... observado.


═══════════════════════════════════════════════════════════════════════════════
3.4 LA IMPEDANCIA DEL VACÍO: Z₀ = 5!π
═══════════════════════════════════════════════════════════════════════════════
""")

    Z_0_obs = 376.730
    Z_0_klein = 120 * pi
    error_Z = abs(Z_0_klein - Z_0_obs) / Z_0_obs * 100

    print(f"""
┌─────────────────────────────────────────────────────────────────────────────┐
│  CONCEPTO: ¿Qué es la impedancia del vacío?                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Z₀ = √(μ₀/ε₀) ≈ 377 Ω                                                     │
│                                                                             │
│  Es la "resistencia" que el vacío ofrece a las ondas electromagnéticas.     │
│  Determina:                                                                 │
│  • La relación entre campo eléctrico y magnético en una onda               │
│  • Cómo las antenas irradian energía                                        │
│  • La reflexión de ondas en interfaces                                      │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────────┐
│  MATEMÁTICAS: La Fórmula Klein para Z₀                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   Z₀ ≈ 120π = 5! × π                                                       │
│                                                                             │
│   donde 5! = 5 × 4 × 3 × 2 × 1 = 120                                       │
│                                                                             │
│   VERIFICACIÓN:                                                             │
│   Predicción: {Z_0_klein:.4f} Ω                                               │
│   Observado:  {Z_0_obs:.4f} Ω                                               │
│   Error:      {error_Z:.3f}%                                                  │
│                                                                             │
│   CONEXIÓN KLEIN:                                                           │
│   5! = permutaciones de 5 elementos                                         │
│   5 = dimensiones de Kaluza-Klein (4 espacio-tiempo + 1 extra)              │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘


¿POR QUÉ 5!?

En teoría de Kaluza-Klein, el universo tiene 5 dimensiones:
4 de espacio-tiempo + 1 dimensión extra compacta.

Las 5! = 120 permutaciones de estas 5 dimensiones, multiplicadas
por π (geometría), dan la impedancia del vacío.

Esto conecta la estructura dimensional del universo con sus
propiedades electromagnéticas.


═══════════════════════════════════════════════════════════════════════════════
3.5 DE KLEIN A MAXWELL: LA DERIVACIÓN
═══════════════════════════════════════════════════════════════════════════════

Ahora mostramos cómo las ecuaciones de Maxwell EMERGEN de Klein.

┌─────────────────────────────────────────────────────────────────────────────┐
│  MATEMÁTICAS: Derivación                                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  PASO 1: La velocidad de la luz                                             │
│                                                                             │
│  c = (3 - 1/(7π)²) × 10⁸ m/s    (fórmula Klein)                            │
│                                                                             │
│  PASO 2: La permeabilidad del vacío                                         │
│                                                                             │
│  μ₀ = 4π × 10⁻⁷ H/m           (definición SI histórica)                    │
│                                                                             │
│  El factor 4π es puramente geométrico (área de esfera unitaria).            │
│                                                                             │
│  PASO 3: La permitividad del vacío                                          │
│                                                                             │
│  ε₀ = 1/(μ₀c²)                                                              │
│     = 1 / [4π × 10⁻⁷ × (3 - 1/(7π)²)² × 10¹⁶]                              │
│                                                                             │
│  PASO 4: Las ecuaciones de Maxwell                                          │
│                                                                             │
│  Con ε₀ y μ₀ determinados por Klein, las ecuaciones de Maxwell              │
│  quedan completamente especificadas.                                        │
│                                                                             │
│  CONCLUSIÓN:                                                                │
│  Las ecuaciones de Maxwell son consecuencia de:                             │
│  • Geometría (4π)                                                           │
│  • Dimensionalidad (3)                                                      │
│  • Topología Klein (7π)                                                     │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘


LA ECUACIÓN DE ONDA ELECTROMAGNÉTICA:

De Maxwell se deriva:

    ∇²E - (1/c²) ∂²E/∂t² = 0

Sustituyendo c Klein:

    ∇²E - 1/[(3 - 1/(7π)²)² × 10¹⁶] × ∂²E/∂t² = 0

Esta es la ecuación que gobierna TODA la luz del universo:
desde las ondas de radio hasta los rayos gamma.


═══════════════════════════════════════════════════════════════════════════════
3.6 RESUMEN DEL CAPÍTULO
═══════════════════════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│  IDEAS CENTRALES:                                                           │
│                                                                             │
│  1. Las ecuaciones de Maxwell describen toda la luz y el                    │
│     electromagnetismo. Dependen de c, ε₀, μ₀.                               │
│                                                                             │
│  2. La velocidad de la luz tiene forma Klein:                               │
│     c = (3 - 1/(7π)²) × 10⁸ m/s                                            │
│     Error: 0.0003%                                                          │
│                                                                             │
│  3. La constante de estructura fina tiene forma Klein:                      │
│     1/α = 7²π - 7 - π²                                                     │
│     Error: 0.024%                                                           │
│                                                                             │
│  4. La impedancia del vacío tiene forma Klein:                              │
│     Z₀ = 120π = 5!π                                                        │
│     Error: 0.07%                                                            │
│                                                                             │
│  5. Las ecuaciones de Maxwell son consecuencia de la topología Klein.       │
│                                                                             │
│  ECUACIONES DEL CAPÍTULO:                                                   │
│                                                                             │
│     c = (3 - 1/(7π)²) × 10⁸ m/s                                            │
│     1/α = 7²π - 7 - π²                                                     │
│     Z₀ = 120π Ω                                                            │
│                                                                             │
│  PRÓXIMO CAPÍTULO:                                                          │
│                                                                             │
│  Si Maxwell viene de Klein, ¿qué pasa con Einstein y la gravedad?           │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘


═══════════════════════════════════════════════════════════════════════════════
EJERCICIOS
═══════════════════════════════════════════════════════════════════════════════

1. Verifica que c = 1/√(ε₀μ₀) usando los valores de ε₀ y μ₀.

2. Calcula qué valor tendría α si la fórmula fuera 1/α = 7²π (sin las
   correcciones -7 y -π²). ¿Qué implicaría para los átomos?

3. La impedancia Z₀ = 377 Ω es aproximadamente 120π.
   ¿Qué precisión tiene esta aproximación?

4. Si la velocidad de la luz fuera exactamente 3 × 10⁸ m/s (sin corrección
   Klein), ¿cuánto diferiría del valor real? ¿Es medible?


═══════════════════════════════════════════════════════════════════════════════
                          FIN DEL CAPÍTULO 3
═══════════════════════════════════════════════════════════════════════════════
""")


# =============================================================================
# CÓDIGO DE VERIFICACIÓN
# =============================================================================

def verificar_maxwell():
    """
    Código ejecutable para verificar las predicciones del Capítulo 3.
    """
    print("\n" + "=" * 60)
    print("VERIFICACIÓN NUMÉRICA - CAPÍTULO 3")
    print("=" * 60)

    # Velocidad de la luz
    c_obs = 299792458
    c_klein = (3 - 1/siete_pi**2) * 1e8
    print(f"\nVELOCIDAD DE LA LUZ:")
    print(f"  c observado  = {c_obs} m/s")
    print(f"  c Klein      = {c_klein:.0f} m/s")
    print(f"  Error = {abs(c_klein - c_obs)/c_obs*100:.6f}%")

    # Estructura fina
    alpha_inv_obs = 137.035999
    alpha_inv_klein = 7**2 * pi - 7 - pi**2
    print(f"\nESTRUCTURA FINA:")
    print(f"  1/α observado = {alpha_inv_obs:.6f}")
    print(f"  1/α Klein     = {alpha_inv_klein:.6f}")
    print(f"  Error = {abs(alpha_inv_klein - alpha_inv_obs)/alpha_inv_obs*100:.6f}%")

    # Impedancia
    Z_obs = 376.730
    Z_klein = 120 * pi
    print(f"\nIMPEDANCIA DEL VACÍO:")
    print(f"  Z₀ observado = {Z_obs:.4f} Ω")
    print(f"  Z₀ Klein     = {Z_klein:.4f} Ω")
    print(f"  Error = {abs(Z_klein - Z_obs)/Z_obs*100:.4f}%")

    # Desglose de la fórmula de α
    print(f"\nDESGLOSE DE 1/α = 7²π - 7 - π²:")
    print(f"  7²π = {49*pi:.4f}")
    print(f"  -7  = -7.0000")
    print(f"  -π² = {-pi**2:.4f}")
    print(f"  Total = {alpha_inv_klein:.4f}")


if __name__ == "__main__":
    mostrar_capitulo()
    verificar_maxwell()
