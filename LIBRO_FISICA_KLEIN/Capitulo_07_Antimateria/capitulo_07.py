#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════════════

                    CAPÍTULO 7: ANTIMATERIA

                    "El espejo de la materia"

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
    # Datos
    eta_B_obs = 6.12e-10
    eta_B_klein = (3/2) * siete_pi**(-7)
    error_eta = abs(eta_B_klein - eta_B_obs) / eta_B_obs * 100

    epsilon_obs = 2.228e-3
    epsilon_klein = siete_pi**(-2)
    error_eps = abs(epsilon_klein - epsilon_obs) / epsilon_obs * 100

    print(f"""
═══════════════════════════════════════════════════════════════════════════════
                        CAPÍTULO 7: ANTIMATERIA
═══════════════════════════════════════════════════════════════════════════════


╔═════════════════════════════════════════════════════════════════════════════╗
║                                                                             ║
║   "¿Por qué hay algo en lugar de nada?"                                     ║
║                                        - Pregunta filosófica antigua        ║
║                                                                             ║
║   "Porque (7π)⁻⁷ ≠ 0."                                                     ║
║                                        - Teoría Klein, 2026                 ║
║                                                                             ║
╚═════════════════════════════════════════════════════════════════════════════╝


═══════════════════════════════════════════════════════════════════════════════
7.1 EL ESPEJO DE LA MATERIA
═══════════════════════════════════════════════════════════════════════════════

Para cada partícula existe una ANTIPARTÍCULA:
    • Electrón (e⁻) ↔ Positrón (e⁺)
    • Protón (p) ↔ Antiprotón (p̄)
    • Neutrón (n) ↔ Antineutrón (n̄)

Cuando materia y antimateria se encuentran: ¡ANIQUILACIÓN!
Toda la masa se convierte en energía pura (E = mc²).

EL GRAN MISTERIO:
El Big Bang debió crear cantidades IGUALES de materia y antimateria.
¿Por qué el universo está hecho solo de materia?

La pequeña asimetría que permitió nuestra existencia:
    η_B = (n_B - n_B̄) / n_γ ≈ 6 × 10⁻¹⁰

Por cada mil millones de pares materia-antimateria que se aniquilaron,
sobró UNA partícula de materia. Esa es nuestra existencia.


═══════════════════════════════════════════════════════════════════════════════
7.2 LA ASIMETRÍA BARIÓNICA: η_B = (3/2)×(7π)⁻⁷
═══════════════════════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────────────────────┐
│  MATEMÁTICAS: η_B desde Klein                                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   η_B = (3/2) × (7π)⁻⁷                                                     │
│                                                                             │
│   donde:                                                                    │
│   • 3/2 = corrección cosmológica (3 dimensiones espaciales)                │
│   • 7 = número de capas Klein (exponente)                                   │
│   • (7π)⁻⁷ = supresión por atravesar 7 capas                               │
│                                                                             │
│   VERIFICACIÓN:                                                             │
│   Predicción: η_B = {eta_B_klein:.3e}                                         │
│   Observado:  η_B = {eta_B_obs:.3e}                                         │
│   Error:      {error_eta:.1f}%                                                 │
│                                                                             │
│   INTERPRETACIÓN:                                                           │
│   La asimetría es pequeña porque el proceso de bariogénesis                 │
│   debe "atravesar" las 7 capas de la botella de Klein.                      │
│   Cada capa suprime por factor 7π ≈ 22.                                    │
│   Total: 22⁷ ≈ 2.5 × 10⁹                                                   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘


═══════════════════════════════════════════════════════════════════════════════
7.3 VIOLACIÓN CP: ε = (7π)⁻²
═══════════════════════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────────────────────┐
│  CONCEPTO: Violación CP                                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  C = conjugación de carga (cambiar partícula por antipartícula)            │
│  P = paridad (reflejar en un espejo)                                        │
│  CP = ambas operaciones juntas                                              │
│                                                                             │
│  La física CASI respeta CP, pero no exactamente.                           │
│  La violación CP es necesaria para explicar la asimetría materia-antimateria│
│                                                                             │
│   FÓRMULA KLEIN:                                                            │
│                                                                             │
│   ε_CP = (7π)⁻² ≈ {siete_pi**(-2):.4f}                                       │
│                                                                             │
│   Predicción: {epsilon_klein:.4f}                                             │
│   Observado:  {epsilon_obs:.4f}                                             │
│   Error:      {error_eps:.1f}%                                                 │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘


═══════════════════════════════════════════════════════════════════════════════
7.4 LA OSCILACIÓN NEUTRÓN-ANTINEUTRÓN
═══════════════════════════════════════════════════════════════════════════════

Una predicción Klein aún no verificada:

    τ(n→n̄) ~ (7π)²⁴ × τ_natural ~ 10⁸ - 10⁹ segundos

El neutrón puede ESPONTÁNEAMENTE convertirse en antineutrón.
Esto violaría la conservación del número bariónico.

El exponente 24 = dim(SU(5)) conecta con unificación de fuerzas.

Experimentos en ESS (European Spallation Source) buscan este efecto.


═══════════════════════════════════════════════════════════════════════════════
7.5 RESUMEN DEL CAPÍTULO
═══════════════════════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│  PREDICCIONES ANTIMATERIA KLEIN:                                            │
│                                                                             │
│  1. η_B = (3/2)×(7π)⁻⁷         [1.5% error] - Asimetría bariónica         │
│  2. ε_CP = (7π)⁻²              [7.2% error] - Violación CP                 │
│  3. τ(n→n̄) ~ (7π)²⁴×τ_nat     [predicción] - Oscilación n-n̄              │
│                                                                             │
│  RESPUESTA AL MISTERIO:                                                     │
│  Existimos porque la bariogénesis atraviesa 7 capas Klein,                  │
│  suprimiendo la simetría materia-antimateria por (7π)⁻⁷.                    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘


═══════════════════════════════════════════════════════════════════════════════
                          FIN DEL CAPÍTULO 7
═══════════════════════════════════════════════════════════════════════════════
""")


if __name__ == "__main__":
    mostrar_capitulo()
