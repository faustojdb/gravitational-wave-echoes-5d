#!/usr/bin/env python3
"""
DERIVACIÓN DEL FACTOR 10^20.86 EN LA JERARQUÍA MATRIOSKA-KLEIN

El factor misterioso: 10^20.86 ≈ 7.24×10²⁰

¿De dónde sale este número? Exploramos todas las combinaciones posibles
de constantes fundamentales.
"""

import numpy as np
from itertools import product

# =============================================================================
# CONSTANTES FUNDAMENTALES
# =============================================================================

# Masas
m_planck = 2.176e-8      # kg (masa de Planck)
m_proton = 1.673e-27     # kg
m_electron = 9.109e-31   # kg
m_neutron = 1.675e-27    # kg

# Longitudes
L_planck = 1.616e-35     # m
r_electron = 2.818e-15   # m (radio clásico del electrón)
a_bohr = 5.292e-11       # m (radio de Bohr)
r_proton = 8.414e-16     # m (radio del protón)

# Constantes adimensionales
alpha = 1/137.036        # constante de estructura fina
mu = m_proton/m_electron # ratio de masas = 1836.15

# Otras
c = 2.998e8              # m/s
hbar = 1.055e-34         # J·s
G = 6.674e-11            # m³/(kg·s²)

# =============================================================================
# EL NÚMERO OBJETIVO
# =============================================================================

TARGET = 10**20.86  # ≈ 7.24×10²⁰
TARGET_LOG = 20.86

print("=" * 70)
print("BÚSQUEDA DEL FACTOR 10^20.86 EN LA JERARQUÍA KLEIN")
print("=" * 70)
print(f"\nObjetivo: 10^{TARGET_LOG:.2f} = {TARGET:.3e}")
print()

# =============================================================================
# RATIOS FUNDAMENTALES
# =============================================================================

print("RATIOS FUNDAMENTALES:")
print("-" * 50)

ratios = {
    "M_Planck/m_proton": m_planck/m_proton,
    "M_Planck/m_electron": m_planck/m_electron,
    "m_proton/m_electron (μ)": mu,
    "1/α": 1/alpha,
    "α": alpha,
    "M_Planck/√(m_p·m_e)": m_planck/np.sqrt(m_proton*m_electron),
    "L_Planck/r_proton": L_planck/r_proton,
    "a_Bohr/L_Planck": a_bohr/L_planck,
}

for name, value in ratios.items():
    log_val = np.log10(value)
    print(f"  {name:30s} = {value:.3e}  (10^{log_val:.2f})")

# =============================================================================
# COMBINACIONES SIMPLES
# =============================================================================

print("\n" + "=" * 70)
print("COMBINACIONES QUE DAN ~10^20.86:")
print("=" * 70)

def check_combination(formula, value, tolerance=0.5):
    """Verifica si una combinación está cerca del objetivo"""
    log_val = np.log10(abs(value)) if value > 0 else 0
    error = abs(log_val - TARGET_LOG)
    if error < tolerance:
        return True, log_val, error
    return False, log_val, error

combinations = []

# Potencias simples de ratios fundamentales
for name, value in ratios.items():
    for exp in np.arange(0.5, 3.0, 0.1):
        result = value**exp
        match, log_val, error = check_combination(f"({name})^{exp}", result, 0.3)
        if match:
            combinations.append((f"({name})^{exp:.2f}", result, log_val, error))

# Productos de ratios
for (n1, v1), (n2, v2) in product(ratios.items(), ratios.items()):
    if n1 != n2:
        for e1 in [0.5, 1.0, 1.5, 2.0]:
            for e2 in [0.5, 1.0, -0.5, -1.0]:
                result = (v1**e1) * (v2**e2)
                formula = f"({n1})^{e1} × ({n2})^{e2}"
                match, log_val, error = check_combination(formula, result, 0.2)
                if match:
                    combinations.append((formula, result, log_val, error))

# Ordenar por error
combinations.sort(key=lambda x: x[3])

print("\nMEJORES COINCIDENCIAS (ordenadas por precisión):\n")
seen = set()
for formula, value, log_val, error in combinations[:15]:
    # Evitar duplicados
    key = f"{log_val:.2f}"
    if key not in seen:
        seen.add(key)
        stars = "★★★" if error < 0.1 else "★★" if error < 0.2 else "★"
        print(f"  {stars} 10^{log_val:.3f}  (error: {error:.3f})")
        print(f"      {formula}")
        print(f"      = {value:.3e}")
        print()

# =============================================================================
# ANÁLISIS PROFUNDO: ¿Qué combinación tiene sentido físico?
# =============================================================================

print("\n" + "=" * 70)
print("ANÁLISIS DE CANDIDATOS CON SENTIDO FÍSICO:")
print("=" * 70)

# Candidato 1: (M_Planck/m_proton)^1.09
candidate1 = (m_planck/m_proton)**1.09
log1 = np.log10(candidate1)
print(f"\n1. (M_Planck/m_proton)^1.09")
print(f"   = {candidate1:.3e}")
print(f"   = 10^{log1:.3f}")
print(f"   Error: {abs(log1 - TARGET_LOG):.3f}")
print(f"   Interpretación: Casi lineal en ratio de masas Planck/barión")

# Candidato 2: (M_Planck/m_proton) × μ^0.17
candidate2 = (m_planck/m_proton) * (mu**0.17)
log2 = np.log10(candidate2)
print(f"\n2. (M_Planck/m_proton) × (m_p/m_e)^0.17")
print(f"   = {candidate2:.3e}")
print(f"   = 10^{log2:.3f}")
print(f"   Error: {abs(log2 - TARGET_LOG):.3f}")
print(f"   Interpretación: Factor de masa Planck/barión con corrección leptónica")

# Candidato 3: M_Planck/√(m_p·m_e)
candidate3 = m_planck/np.sqrt(m_proton*m_electron)
log3 = np.log10(candidate3)
print(f"\n3. M_Planck/√(m_proton × m_electron)")
print(f"   = {candidate3:.3e}")
print(f"   = 10^{log3:.3f}")
print(f"   Error: {abs(log3 - TARGET_LOG):.3f}")
print(f"   Interpretación: Masa geométrica media de materia ordinaria")

# Candidato 4: (M_Planck/m_electron)^0.95
candidate4 = (m_planck/m_electron)**0.95
log4 = np.log10(candidate4)
print(f"\n4. (M_Planck/m_electron)^0.95")
print(f"   = {candidate4:.3e}")
print(f"   = 10^{log4:.3f}")
print(f"   Error: {abs(log4 - TARGET_LOG):.3f}")
print(f"   Interpretación: Escala de masa electrónica casi lineal")

# Candidato 5: Combinación con α
candidate5 = (m_planck/m_proton) * (1/alpha)**0.5
log5 = np.log10(candidate5)
print(f"\n5. (M_Planck/m_proton) × α^(-0.5)")
print(f"   = {candidate5:.3e}")
print(f"   = 10^{log5:.3f}")
print(f"   Error: {abs(log5 - TARGET_LOG):.3f}")
print(f"   Interpretación: Escala de masa con corrección electromagnética")

# =============================================================================
# BÚSQUEDA EXACTA: ¿Qué exponentes ajustan exactamente?
# =============================================================================

print("\n" + "=" * 70)
print("EXPONENTES EXACTOS PARA TARGET = 10^20.86:")
print("=" * 70)

# Si factor = (M_Planck/m_proton)^x, ¿cuál es x?
log_mp_over_proton = np.log10(m_planck/m_proton)
x_exact = TARGET_LOG / log_mp_over_proton
print(f"\n(M_Planck/m_proton)^x = 10^20.86")
print(f"x = 20.86 / {log_mp_over_proton:.3f} = {x_exact:.4f}")

# Si factor = (M_Planck/m_electron)^y, ¿cuál es y?
log_mp_over_electron = np.log10(m_planck/m_electron)
y_exact = TARGET_LOG / log_mp_over_electron
print(f"\n(M_Planck/m_electron)^y = 10^20.86")
print(f"y = 20.86 / {log_mp_over_electron:.3f} = {y_exact:.4f}")

# Si factor = μ^z, ¿cuál es z?
log_mu = np.log10(mu)
z_exact = TARGET_LOG / log_mu
print(f"\n(m_proton/m_electron)^z = 10^20.86")
print(f"z = 20.86 / {log_mu:.3f} = {z_exact:.4f}")

# =============================================================================
# HIPÓTESIS: RELACIÓN CON CHANDRASEKHAR
# =============================================================================

print("\n" + "=" * 70)
print("HIPÓTESIS: CONEXIÓN CON MASA DE CHANDRASEKHAR")
print("=" * 70)

# Ya sabemos que M_transition ≈ M_Ch × (m_p/m_e)
M_sun = 1.989e30  # kg
M_Ch = 1.44 * M_sun  # kg
M_transition = 2847 * M_sun  # kg

print(f"\nM_transition = {M_transition/M_sun:.0f} M☉")
print(f"M_Chandrasekhar = {M_Ch/M_sun:.2f} M☉")
print(f"M_transition / M_Ch = {M_transition/M_Ch:.1f} ≈ m_p/m_e = {mu:.1f}")

# R_Klein desde M_transition
R_Klein = 2 * G * M_transition / c**2
print(f"\nR_Klein = 2GM_trans/c² = {R_Klein/1000:.0f} km")

# Factor entre R₂ y R₃
R_2 = 1.17e-14  # m (escala nuclear)
R_3 = R_Klein
factor_2_to_3 = R_3 / R_2
log_factor = np.log10(factor_2_to_3)

print(f"\nFactor R₃/R₂ = {factor_2_to_3:.3e} = 10^{log_factor:.2f}")
print(f"Target: 10^{TARGET_LOG:.2f}")
print(f"Diferencia: {abs(log_factor - TARGET_LOG):.2f} órdenes de magnitud")

# =============================================================================
# FÓRMULA PROPUESTA
# =============================================================================

print("\n" + "=" * 70)
print("FÓRMULA PROPUESTA PARA EL FACTOR:")
print("=" * 70)

# La mejor aproximación física
print("""
CANDIDATO MÁS PROMETEDOR:

    Factor = M_Planck / √(m_proton × m_electron)

           = √(ℏc/G) / √(m_p × m_e)

           = √(ℏc / (G × m_p × m_e))

Esto da 10^{:.2f} (error: {:.2f})

INTERPRETACIÓN FÍSICA:
- Es la media geométrica entre las escalas de masa de Planck y materia ordinaria
- Combina gravedad cuántica (ℏ, G, c) con materia (m_p, m_e)
- Es simétrico entre protón y electrón
- Aparece naturalmente en límites de estabilidad gravitacional
""".format(log3, abs(log3 - TARGET_LOG)))

# =============================================================================
# VERIFICACIÓN CON DATOS OBSERVACIONALES
# =============================================================================

print("\n" + "=" * 70)
print("VERIFICACIÓN CON JERARQUÍA OBSERVADA:")
print("=" * 70)

# Usar el candidato 3 para predecir la jerarquía
factor_proposed = m_planck/np.sqrt(m_proton*m_electron)

levels = {
    "Klein₁": L_planck,
    "Klein₂": L_planck * factor_proposed,
    "Klein₃": L_planck * factor_proposed**2,
    "Klein₄": L_planck * factor_proposed**3,
}

observations = {
    "Klein₁": 1.62e-35,      # Planck (por definición)
    "Klein₂": 1.17e-14,      # Nuclear
    "Klein₃": 8.4e6,         # Stellar BH (validado!)
    "Klein₄": 5e27 * 0.3086e17,  # ~500 Mpc en metros
}

print(f"\nUsando Factor = M_Planck/√(m_p·m_e) = {factor_proposed:.3e}")
print()

for level, predicted in levels.items():
    observed = observations[level]
    ratio = predicted / observed
    log_ratio = np.log10(ratio) if ratio > 0 else 0
    status = "✓" if abs(log_ratio) < 1 else "✗"

    print(f"{level}:")
    print(f"  Predicho:  {predicted:.2e} m")
    print(f"  Observado: {observed:.2e} m")
    print(f"  Ratio: {ratio:.2f} (10^{log_ratio:.1f}) {status}")
    print()

# =============================================================================
# CONCLUSIÓN
# =============================================================================

print("\n" + "=" * 70)
print("CONCLUSIÓN")
print("=" * 70)
print("""
El factor 10^20.86 en la jerarquía Matrioska-Klein puede expresarse como:

    Factor ≈ M_Planck / √(m_proton × m_electron)

           = √(ℏc / (G × m_proton × m_electron))

           ≈ 5.6 × 10²⁰

SIGNIFICADO FÍSICO:
- Conecta la gravedad cuántica (escala de Planck) con la materia ordinaria
- Es simétrico entre las partículas fundamentales estables
- Aparece en la condición de estabilidad gravitacional
- Sugiere que los niveles Klein están determinados por límites de estabilidad

DISCREPANCIA:
- Predicho: 10^20.75
- Observado: 10^20.86
- Error: ~30% (0.11 en log)

Este error del 30% podría deberse a:
1. Factores topológicos (π, 2, etc.) no incluidos
2. Correcciones cuánticas
3. La definición exacta de R_Klein

SIGUIENTE PASO:
Buscar si hay un factor π o similar que corrija la discrepancia.
""")

# Verificar si π ayuda
candidate_with_pi = candidate3 * np.pi**0.2
log_with_pi = np.log10(candidate_with_pi)
print(f"\nCon factor π^0.2: 10^{log_with_pi:.3f} (error: {abs(log_with_pi-TARGET_LOG):.3f})")

candidate_with_2 = candidate3 * 2**0.5
log_with_2 = np.log10(candidate_with_2)
print(f"Con factor √2:    10^{log_with_2:.3f} (error: {abs(log_with_2-TARGET_LOG):.3f})")

# Mejor ajuste
for factor in [1.0, 1.1, 1.2, 1.3, 1.4, 1.5]:
    test = candidate3 * factor
    log_test = np.log10(test)
    if abs(log_test - TARGET_LOG) < 0.05:
        print(f"\n★★★ Factor de corrección {factor:.2f} da 10^{log_test:.3f} (error: {abs(log_test-TARGET_LOG):.3f})")
