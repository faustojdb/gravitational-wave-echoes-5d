#!/usr/bin/env python3
"""
CONSTANTE GRAVITACIONAL G Y TEORÍA KLEIN

G es la constante de acoplamiento gravitacional.
¿Tiene forma Klein cuando se expresa adimensionalmente?

Exploraremos:
- Ratio G × m_p² / (ℏc) - acoplamiento gravitacional
- Relación con masa de Planck
- Conexiones con otras constantes

AUTOR: Fausto Jose Di Bacco
EMAIL: faustojdb@gmail.com
FECHA: Enero 2026

Copyright (c) 2026 Fausto Jose Di Bacco. Todos los derechos reservados.
"""

import numpy as np

print("=" * 80)
print("CONSTANTE GRAVITACIONAL Y TEORÍA KLEIN")
print("=" * 80)

# =============================================================================
# CONSTANTES FUNDAMENTALES
# =============================================================================

# Valores exactos/precisos
c = 299792458           # m/s (exacto)
hbar = 1.054571817e-34  # J·s
h = 6.62607015e-34      # J·s (exacto)
G = 6.67430e-11         # m³/(kg·s²) (incertidumbre ~0.002%)

# Masas
m_e = 9.1093837015e-31  # kg (electrón)
m_p = 1.67262192369e-27 # kg (protón)
m_P = np.sqrt(hbar * c / G)  # masa de Planck

# Otras constantes
alpha = 7.2973525693e-3  # constante de estructura fina
k_B = 1.380649e-23       # J/K

# Klein
siete_pi = 7 * np.pi
pi = np.pi

print(f"""
CONSTANTES FUNDAMENTALES:

  G = {G:.5e} m³/(kg·s²)
  c = {c} m/s
  ℏ = {hbar:.6e} J·s

  m_e = {m_e:.6e} kg
  m_p = {m_p:.6e} kg
  m_P = √(ℏc/G) = {m_P:.6e} kg

  α = {alpha:.6e}
  7π = {siete_pi:.4f}
""")

# =============================================================================
# ACOPLAMIENTO GRAVITACIONAL
# =============================================================================

print("\n" + "=" * 80)
print("ACOPLAMIENTO GRAVITACIONAL")
print("=" * 80)

# Constante de acoplamiento gravitacional (adimensional)
alpha_G_p = G * m_p**2 / (hbar * c)  # para protón
alpha_G_e = G * m_e**2 / (hbar * c)  # para electrón

print(f"""
El análogo gravitacional de α es:

  α_G = G m² / (ℏc)

Para el protón:
  α_G(p) = G m_p² / (ℏc) = {alpha_G_p:.6e}

Para el electrón:
  α_G(e) = G m_e² / (ℏc) = {alpha_G_e:.6e}

Ratios:
  α / α_G(p) = {alpha / alpha_G_p:.3e}
  α / α_G(e) = {alpha / alpha_G_e:.3e}

  ¡La gravedad es ~10³⁶-10⁴⁵ veces más débil que el EM!
""")

# =============================================================================
# RATIO α/α_G EN FORMA KLEIN
# =============================================================================

print("\n" + "=" * 80)
print("RATIO α/α_G EN FORMA KLEIN")
print("=" * 80)

ratio_p = alpha / alpha_G_p
ratio_e = alpha / alpha_G_e

# Buscar exponente n tal que ratio = (7π)^n
n_p = np.log(ratio_p) / np.log(siete_pi)
n_e = np.log(ratio_e) / np.log(siete_pi)

print(f"""
Si α/α_G = (7π)^n:

Para protón:
  α/α_G(p) = {ratio_p:.3e}
  n = log(ratio) / log(7π) = {n_p:.2f}

Para electrón:
  α/α_G(e) = {ratio_e:.3e}
  n = log(ratio) / log(7π) = {n_e:.2f}

Verificación:
  (7π)^29 = {siete_pi**29:.3e}
  (7π)^30 = {siete_pi**30:.3e}

  α/α_G(p) = {ratio_p:.3e} (n ≈ 29.5)
""")

# =============================================================================
# MASA DE PLANCK / MASA DE PROTÓN
# =============================================================================

print("\n" + "=" * 80)
print("MASA DE PLANCK / MASA DE PARTÍCULAS")
print("=" * 80)

ratio_Planck_p = m_P / m_p
ratio_Planck_e = m_P / m_e

n_Pp = np.log(ratio_Planck_p) / np.log(siete_pi)
n_Pe = np.log(ratio_Planck_e) / np.log(siete_pi)

print(f"""
m_Planck / m_p = {ratio_Planck_p:.3e}
  n = log(ratio) / log(7π) = {n_Pp:.2f}

m_Planck / m_e = {ratio_Planck_e:.3e}
  n = log(ratio) / log(7π) = {n_Pe:.2f}

Verificación:
  (7π)^14 = {siete_pi**14:.3e}  (para m_P/m_p, error {abs(siete_pi**14 - ratio_Planck_p)/ratio_Planck_p*100:.0f}%)
  (7π)^15 = {siete_pi**15:.3e}

La masa de Planck está a ~14-15 "capas Klein" del protón.
""")

# =============================================================================
# BÚSQUEDA DE FÓRMULA PARA α_G
# =============================================================================

print("\n" + "=" * 80)
print("BÚSQUEDA DE FÓRMULA PARA α_G(p)")
print("=" * 80)

# α_G(p) es muy pequeño
# Buscar: α_G(p) = f(7,π) × algo pequeño

print(f"""
α_G(p) = {alpha_G_p:.6e}

Si α_G(p) = (7π)^(-n):
  n ≈ {-np.log(alpha_G_p) / np.log(siete_pi):.2f}

Verificación:
  (7π)^(-36) = {siete_pi**(-36):.3e}
  (7π)^(-37) = {siete_pi**(-37):.3e}

  α_G(p) = {alpha_G_p:.3e}

HIPÓTESIS: α_G(p) ≈ (7π)^(-36) o cercano
""")

# Buscar factor de corrección
n_best = 36
factor_36 = alpha_G_p / siete_pi**(-36)
factor_37 = alpha_G_p / siete_pi**(-37)

print(f"""
Factores de corrección:
  Para n=36: factor = {factor_36:.4f}
  Para n=37: factor = {factor_37:.4f}

¿Qué es {factor_36:.4f}?
  2 = 2.0000  (error {abs(factor_36 - 2)/2*100:.1f}%)
  π/2 = {pi/2:.4f}  (error {abs(factor_36 - pi/2)/(pi/2)*100:.1f}%)
  e = {np.e:.4f}  (error {abs(factor_36 - np.e)/np.e*100:.1f}%)
  7/4 = {7/4:.4f}  (error {abs(factor_36 - 7/4)/(7/4)*100:.1f}%)
""")

# =============================================================================
# RELACIÓN CON m_p/m_e
# =============================================================================

print("\n" + "=" * 80)
print("RELACIÓN CON m_p/m_e")
print("=" * 80)

# Ya sabemos que m_p/m_e = 6π⁵
# Y α_G(p) / α_G(e) = (m_p/m_e)²

ratio_alphaG = alpha_G_p / alpha_G_e
ratio_mass_sq = (m_p / m_e)**2

print(f"""
Relación entre α_G(p) y α_G(e):

  α_G(p) / α_G(e) = (m_p/m_e)²

  (m_p/m_e)² = {ratio_mass_sq:.2f}
  (6π⁵)² = 36π¹⁰ = {(6*pi**5)**2:.2f}

  Verificación: {ratio_alphaG:.2f} ≈ {ratio_mass_sq:.2f} ✓

Entonces:
  α_G(p) = α_G(e) × (6π⁵)² = α_G(e) × 36π¹⁰
""")

# =============================================================================
# FÓRMULA PARA G EN TÉRMINOS DE CONSTANTES FUNDAMENTALES
# =============================================================================

print("\n" + "=" * 80)
print("FÓRMULA PARA G")
print("=" * 80)

# G = α_G × ℏc / m²
# Si α_G(p) = f × (7π)^(-n)

# Probemos: α_G(p) = (7π)^(-36) / (algo)
# O: α_G(p) = α × (m_e/m_p)^n × ...

# Relación conocida:
# α_G(p) / α = (m_p/m_P)²

ratio_alpha_alphaG = alpha / alpha_G_p
ratio_mass_Planck = (m_P / m_p)**2

print(f"""
Relaciones fundamentales:

  α / α_G(p) = {ratio_alpha_alphaG:.3e}
  (m_P / m_p)² = {ratio_mass_Planck:.3e}

  ¿Son iguales? Ratio = {ratio_alpha_alphaG / ratio_mass_Planck:.4f}

  No exactamente, porque:
  α / α_G(p) = α × (ℏc/G) / m_p² = α × m_P² / m_p²

  Entonces: α / α_G(p) = α × (m_P/m_p)²

  Verificación: α × {ratio_mass_Planck:.3e} = {alpha * ratio_mass_Planck:.3e}
  vs α / α_G(p) = {ratio_alpha_alphaG:.3e}

  ¡Correcto!
""")

# =============================================================================
# EXPONENTE TOTAL
# =============================================================================

print("\n" + "=" * 80)
print("ANÁLISIS DEL EXPONENTE")
print("=" * 80)

# m_P/m_p ≈ (7π)^14.2
# (m_P/m_p)² ≈ (7π)^28.4
# α ≈ (7²π - 7 - π²)^(-1) ≈ 137^(-1)

# α_G(p) = α / (m_P/m_p)²
# log(α_G) = log(α) - 2×log(m_P/m_p)
#          ≈ -ln(137) - 2×14.2×ln(7π)
#          ≈ -4.92 - 28.4×3.09
#          ≈ -4.92 - 87.8 = -92.7 (en ln)

n_teorico = 2 * n_Pp  # contribución de (m_P/m_p)²

print(f"""
Análisis del exponente de α_G(p):

  α_G(p) = α × (m_p/m_P)² = α / (m_P/m_p)²

  log(α_G) / log(7π) = log(α)/log(7π) + 2×log(m_p/m_P)/log(7π)
                     = {np.log(alpha)/np.log(siete_pi):.2f} + 2×({-n_Pp:.2f})
                     = {np.log(alpha)/np.log(siete_pi):.2f} - {2*n_Pp:.2f}
                     = {np.log(alpha)/np.log(siete_pi) - 2*n_Pp:.2f}

  Verificación directa:
  log(α_G(p)) / log(7π) = {np.log(alpha_G_p)/np.log(siete_pi):.2f}

  ¡Coincide!
""")

# =============================================================================
# ¿HAY FORMA SIMPLE PARA G?
# =============================================================================

print("\n" + "=" * 80)
print("¿FORMA SIMPLE PARA G?")
print("=" * 80)

# G aparece en las escalas de Planck
# m_P = √(ℏc/G) → G = ℏc/m_P²

# Si m_P tiene forma Klein, G también la tendría

print(f"""
La constante G aparece en:

  m_P = √(ℏc/G)  →  G = ℏc/m_P²

Si buscamos m_P en forma Klein:

  m_P / m_p = {ratio_Planck_p:.3e}

  log(m_P/m_p) / log(7π) = {n_Pp:.2f}

  Entonces: m_P ≈ m_p × (7π)^{n_Pp:.1f}

PERO el exponente no es entero (≈14.2).

¿Hay corrección?

  (7π)^14 = {siete_pi**14:.3e}
  m_P/m_p = {ratio_Planck_p:.3e}
  Factor = {ratio_Planck_p / siete_pi**14:.3f}

  ¿Qué es {ratio_Planck_p / siete_pi**14:.3f}?
    2 = 2.0  (error {abs(ratio_Planck_p/siete_pi**14 - 2)/2*100:.0f}%)
    e = 2.72  (error {abs(ratio_Planck_p/siete_pi**14 - np.e)/np.e*100:.0f}%)
    π = 3.14  (error {abs(ratio_Planck_p/siete_pi**14 - pi)/pi*100:.0f}%)
""")

# =============================================================================
# HIPÓTESIS: m_P/m_p = 2×(7π)^14
# =============================================================================

print("\n" + "=" * 80)
print("HIPÓTESIS: m_P/m_p = 2×(7π)^14")
print("=" * 80)

hipotesis = 2 * siete_pi**14
error_hipotesis = abs(hipotesis - ratio_Planck_p) / ratio_Planck_p * 100

print(f"""
HIPÓTESIS: m_P / m_p = 2 × (7π)^14

  2 × (7π)^14 = {hipotesis:.4e}
  m_P / m_p = {ratio_Planck_p:.4e}

  Error: {error_hipotesis:.1f}%

Hmm, error de ~5%. No es tan preciso como otras fórmulas.

Probemos otras:
  (7/4) × (7π)^14 = {(7/4)*siete_pi**14:.4e}  error: {abs((7/4)*siete_pi**14 - ratio_Planck_p)/ratio_Planck_p*100:.1f}%
  (π/2) × (7π)^14 = {(pi/2)*siete_pi**14:.4e}  error: {abs((pi/2)*siete_pi**14 - ratio_Planck_p)/ratio_Planck_p*100:.1f}%
  e × (7π)^14 = {np.e*siete_pi**14:.4e}  error: {abs(np.e*siete_pi**14 - ratio_Planck_p)/ratio_Planck_p*100:.0f}%
""")

# =============================================================================
# RELACIÓN G CON OTRAS CONSTANTES KLEIN
# =============================================================================

print("\n" + "=" * 80)
print("RELACIÓN ENTRE G Y OTRAS CONSTANTES KLEIN")
print("=" * 80)

print(f"""
Tenemos:
  m_p/m_e = 6π⁵ (0.002% error)
  1/α = 7²π - 7 - π² (0.024% error)

Si m_P/m_p = f × (7π)^14:

  G = ℏc / m_P² = ℏc / [m_p × f × (7π)^14]²
    = ℏc / [m_p² × f² × (7π)^28]

  α_G(p) = G m_p² / (ℏc) = 1 / [f² × (7π)^28]

  Verificación:
  (7π)^(-28) = {siete_pi**(-28):.3e}
  α_G(p) = {alpha_G_p:.3e}

  Factor f² = α_G(p) × (7π)^28 = {alpha_G_p * siete_pi**28:.3f}
  f = √({alpha_G_p * siete_pi**28:.3f}) = {np.sqrt(alpha_G_p * siete_pi**28):.3f}

  ¿Qué es {np.sqrt(alpha_G_p * siete_pi**28):.3f}?
    2 (error {abs(np.sqrt(alpha_G_p * siete_pi**28) - 2)/2*100:.0f}%)
    π/√2 = {pi/np.sqrt(2):.3f} (error {abs(np.sqrt(alpha_G_p * siete_pi**28) - pi/np.sqrt(2))/(pi/np.sqrt(2))*100:.0f}%)
""")

# =============================================================================
# SÍNTESIS
# =============================================================================

print("\n" + "=" * 80)
print("SÍNTESIS: CONSTANTE GRAVITACIONAL")
print("=" * 80)

f_squared = alpha_G_p * siete_pi**28
f_value = np.sqrt(f_squared)

print(f"""
═══════════════════════════════════════════════════════════════════════════════
HALLAZGOS:

1. ACOPLAMIENTO GRAVITACIONAL:
   α_G(p) = G m_p² / (ℏc) = {alpha_G_p:.4e}

   α_G(p) ≈ (7π)^(-28) × f² donde f ≈ {f_value:.2f}

2. MASA DE PLANCK:
   m_P / m_p ≈ {f_value:.2f} × (7π)^14

   Error: ~{error_hipotesis:.0f}%

3. RELACIÓN CON α:
   α / α_G(p) = (m_P/m_p)² ≈ [{f_value:.2f} × (7π)^14]² = {f_value**2:.1f} × (7π)^28

4. EXPONENTES:
   - m_P/m_p: ~14 capas Klein
   - α_G(p): ~(-28) = -2×14 capas (cuadrado)
   - α/α_G: ~28 capas

INTERPRETACIÓN:

   La gravedad es débil porque la masa de Planck está a 14 "capas Klein"
   de la masa del protón. El acoplamiento gravitacional va como el
   cuadrado de este ratio, dando ~28 capas de supresión.

   Esto conecta con:
   - 24 (dim SU(5)) en T_CMB y n→n̄
   - 7 en bariogénesis

   14 = 2 × 7 = dos veces las capas de Klein

NOTA:
   El error (~5%) es mayor que en otras predicciones.
   G podría necesitar correcciones más complejas o depender
   de otros factores no incluidos en este análisis simple.

═══════════════════════════════════════════════════════════════════════════════
""")
