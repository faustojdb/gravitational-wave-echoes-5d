#!/usr/bin/env python3
"""
ANÁLISIS DEL PATRÓN DE ERROR

Observación del usuario: El error aumenta con Z, Q y "tamaño" del isótopo.
¿Hay una corrección sistemática que podamos aplicar?
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import stats

# =============================================================================
# DATOS
# =============================================================================

isotopes = [
    {"name": "Re-187", "Z": 75, "A": 187, "Q": 2.5, "log_ratio_obs": 9.106, "tipo": "EXP"},
    {"name": "Pu-241", "Z": 94, "A": 241, "Q": 20.8, "log_ratio_obs": 3.096, "tipo": "EXP"},
    {"name": "Ra-228", "Z": 88, "A": 228, "Q": 39.4, "log_ratio_obs": 3.013, "tipo": "TEO"},
    {"name": "Ac-227", "Z": 89, "A": 227, "Q": 44.7, "log_ratio_obs": 2.176, "tipo": "TEO"},
]

LOG_FACTOR = 20.8456
Z_MAX = 172
Q_REF = 2.5
ALPHA = 0.6

print("=" * 80)
print("ANÁLISIS DEL PATRÓN DE ERROR")
print("=" * 80)

# Calcular predicciones y errores
for iso in isotopes:
    iso["pred"] = LOG_FACTOR * (iso["Z"] / Z_MAX) * (Q_REF / iso["Q"])**ALPHA
    iso["error"] = iso["pred"] - iso["log_ratio_obs"]
    iso["error_pct"] = abs(iso["error"]) / iso["log_ratio_obs"] * 100
    iso["error_rel"] = iso["pred"] / iso["log_ratio_obs"]

print("\n" + "-" * 90)
print(f"{'Isótopo':<10} {'Z':<5} {'A':<5} {'Q':<8} {'Pred':<10} {'Obs':<10} {'Error':<10} {'Error%':<10}")
print("-" * 90)

for iso in isotopes:
    print(f"{iso['name']:<10} {iso['Z']:<5} {iso['A']:<5} {iso['Q']:<8.1f} {iso['pred']:<10.3f} {iso['log_ratio_obs']:<10.3f} {iso['error']:<10.3f} {iso['error_pct']:<10.1f}")

# =============================================================================
# BUSCAR CORRELACIONES
# =============================================================================

print("\n" + "=" * 80)
print("CORRELACIONES DEL ERROR CON PARÁMETROS")
print("=" * 80)

Zs = np.array([iso["Z"] for iso in isotopes])
As = np.array([iso["A"] for iso in isotopes])
Qs = np.array([iso["Q"] for iso in isotopes])
errors = np.array([iso["error"] for iso in isotopes])
errors_pct = np.array([iso["error_pct"] for iso in isotopes])

# Correlaciones
params = [("Z", Zs), ("A", As), ("Q", Qs), ("log(Q)", np.log10(Qs)), ("Z×Q", Zs*Qs), ("A/Z", As/Zs)]

print("\nCorrelación de Pearson entre ERROR y parámetros:")
print("-" * 50)

for name, param in params:
    r, p = stats.pearsonr(errors, param)
    print(f"Error vs {name:<8}: r = {r:+.3f}, p = {p:.4f}")

print("\nCorrelación de Pearson entre ERROR% y parámetros:")
print("-" * 50)

for name, param in params:
    r, p = stats.pearsonr(errors_pct, param)
    significativo = "***" if p < 0.05 else ""
    print(f"Error% vs {name:<8}: r = {r:+.3f}, p = {p:.4f} {significativo}")

# =============================================================================
# LA CORRELACIÓN CON Q ES CLARA
# =============================================================================

print("\n" + "=" * 80)
print("ANÁLISIS DETALLADO: ERROR vs Q")
print("=" * 80)

print("""
Los datos ordenados por Q:

Q (keV)  |  Error%  |  Isótopo  |  Tipo
---------|----------|-----------|-------""")

sorted_iso = sorted(isotopes, key=lambda x: x["Q"])
for iso in sorted_iso:
    print(f"  {iso['Q']:<6.1f} |  {iso['error_pct']:<7.1f} |  {iso['name']:<9} |  {iso['tipo']}")

print("""
OBSERVACIÓN:
- Q = 2.5 keV (Re-187): Error 0.1%
- Q = 20.8 keV (Pu-241): Error 3.3%
- Q = 39.4 keV (Ra-228): Error 32.3%
- Q = 44.7 keV (Ac-227): Error 12.1%

El patrón NO es perfectamente monótono (Ra-228 tiene más error que Ac-227),
pero la tendencia general es: mayor Q → mayor error.

EXCEPCIÓN: Ra-228 tiene error anómalo. ¿Por qué?
""")

# =============================================================================
# HIPÓTESIS: α DEPENDE DE Q
# =============================================================================

print("\n" + "=" * 80)
print("HIPÓTESIS: α DEPENDE DE Q")
print("=" * 80)

print("""
Si el exponente α no es constante, sino que depende de Q:

    α(Q) = α₀ + β × log(Q/Q_ref)

entonces podemos calcular el α efectivo para cada isótopo:
""")

# Calcular α efectivo para cada isótopo (excepto Re-187 donde Q=Q_ref)
print("\nα efectivo para cada isótopo (asumiendo Z_max = 172):")
print("-" * 60)

alphas_eff = []
for iso in isotopes:
    if iso["Q"] != Q_REF:
        # log(ratio) = LOG_FACTOR * (Z/Z_max) * (Q_ref/Q)^α
        # α = log[log_ratio / (LOG_FACTOR * Z/Z_max)] / log(Q_ref/Q)
        base = LOG_FACTOR * iso["Z"] / Z_MAX
        alpha_eff = np.log(iso["log_ratio_obs"] / base) / np.log(Q_REF / iso["Q"])
        iso["alpha_eff"] = alpha_eff
        alphas_eff.append((iso["Q"], alpha_eff))
        print(f"{iso['name']:<10}: α_eff = {alpha_eff:.4f} (Q = {iso['Q']} keV)")
    else:
        iso["alpha_eff"] = None
        print(f"{iso['name']:<10}: Q = Q_ref, no se puede calcular α_eff")

# Ajustar α como función de Q
if len(alphas_eff) >= 2:
    Qs_fit = np.array([x[0] for x in alphas_eff])
    alphas_fit = np.array([x[1] for x in alphas_eff])

    # Ajuste lineal en log(Q)
    log_Qs = np.log10(Qs_fit)
    slope, intercept, r, p, se = stats.linregress(log_Qs, alphas_fit)

    print(f"\nAjuste lineal: α = {intercept:.4f} + {slope:.4f} × log₁₀(Q)")
    print(f"R² = {r**2:.4f}, p = {p:.4f}")

    # Nuevo modelo
    print(f"""
NUEVO MODELO PROPUESTO:

    α(Q) = {intercept:.3f} + {slope:.3f} × log₁₀(Q)

En Q = 2.5 keV: α = {intercept + slope * np.log10(2.5):.3f}
En Q = 20 keV: α = {intercept + slope * np.log10(20):.3f}
En Q = 40 keV: α = {intercept + slope * np.log10(40):.3f}
""")

# =============================================================================
# PROBAR NUEVO MODELO CON α VARIABLE
# =============================================================================

print("\n" + "=" * 80)
print("PRUEBA DEL NUEVO MODELO: α = f(Q)")
print("=" * 80)

print("-" * 90)
print(f"{'Isótopo':<10} {'α_usado':<10} {'Pred_nuevo':<12} {'Observado':<12} {'Error%':<10} {'Mejora?':<10}")
print("-" * 90)

for iso in isotopes:
    # Calcular α para este Q
    alpha_var = intercept + slope * np.log10(iso["Q"])

    # Nueva predicción
    pred_nuevo = LOG_FACTOR * (iso["Z"] / Z_MAX) * (Q_REF / iso["Q"])**alpha_var
    error_nuevo = abs(pred_nuevo - iso["log_ratio_obs"]) / iso["log_ratio_obs"] * 100

    mejora = "✓ SÍ" if error_nuevo < iso["error_pct"] else "✗ NO"

    print(f"{iso['name']:<10} {alpha_var:<10.3f} {pred_nuevo:<12.3f} {iso['log_ratio_obs']:<12.3f} {error_nuevo:<10.1f} {mejora:<10}")

# =============================================================================
# INTERPRETACIÓN FÍSICA
# =============================================================================

print("\n" + "=" * 80)
print("INTERPRETACIÓN FÍSICA")
print("=" * 80)

print(f"""
¿Por qué α dependería de Q?

FÍSICA DEL DECAIMIENTO β:

1. ESPACIO DE FASE
   - Para decaimiento β continuo: λ ∝ Q⁵ (regla de Sargent)
   - Para bound-state β: λ ∝ Q² (aproximación)

   El RATIO de tasas depende de cómo Q afecta cada canal.

2. TRANSICIONES PROHIBIDAS
   - Cuando Q es muy bajo (~keV), solo algunas transiciones son posibles
   - Cuando Q es más alto (~50 keV), más transiciones contribuyen

   El exponente α podría reflejar cuántas transiciones contribuyen.

3. INTERPRETACIÓN KLEIN
   Si la modulación Klein opera a través de la geometría del espacio-tiempo,
   isótopos con más energía disponible (Q alto) podrían ser menos sensibles
   a la modulación topológica.

   Es como un barco pequeño vs uno grande: el pequeño siente más las olas.

FÓRMULA MEJORADA:

   log₁₀(τ_n/τ_i) = 20.85 × (Z/172) × (Q_ref/Q)^α(Q)

   donde: α(Q) = {intercept:.3f} + {slope:.3f} × log₁₀(Q)

NOTA DE CAUTELA:
   Con solo 4 puntos de datos (y 2 teóricos con incertidumbre),
   no podemos estar seguros de que α realmente depende de Q.
   Podría ser que el error en Ra-228 sea simplemente error del cálculo teórico.

PRÓXIMO PASO:
   Medir Ra-228 o Ac-227 experimentalmente para resolver esta ambigüedad.
""")

# =============================================================================
# GRÁFICO
# =============================================================================

fig, axes = plt.subplots(1, 3, figsize=(15, 5))

# Panel 1: Error vs Q
ax1 = axes[0]
colors = ['green' if iso['tipo'] == 'EXP' else 'orange' for iso in isotopes]
ax1.scatter(Qs, errors_pct, c=colors, s=100, edgecolors='black')
for iso in isotopes:
    ax1.annotate(iso['name'], (iso['Q'], iso['error_pct']), textcoords="offset points", xytext=(5,5))
ax1.set_xlabel('Q (keV)')
ax1.set_ylabel('Error (%)')
ax1.set_title('Error vs Q-value')
ax1.axhline(y=10, color='red', linestyle='--', alpha=0.5, label='10% threshold')
ax1.legend()

# Panel 2: α efectivo vs log(Q)
ax2 = axes[1]
Qs_eff = [iso['Q'] for iso in isotopes if iso['alpha_eff'] is not None]
alphas_plot = [iso['alpha_eff'] for iso in isotopes if iso['alpha_eff'] is not None]
colors2 = ['green' if iso['tipo'] == 'EXP' else 'orange' for iso in isotopes if iso['alpha_eff'] is not None]

ax2.scatter(np.log10(Qs_eff), alphas_plot, c=colors2, s=100, edgecolors='black')
for iso in isotopes:
    if iso['alpha_eff'] is not None:
        ax2.annotate(iso['name'], (np.log10(iso['Q']), iso['alpha_eff']), textcoords="offset points", xytext=(5,5))

# Línea de ajuste
x_fit = np.linspace(0.3, 1.7, 100)
y_fit = intercept + slope * x_fit
ax2.plot(x_fit, y_fit, 'r--', label=f'α = {intercept:.2f} + {slope:.2f}×log(Q)')

ax2.set_xlabel('log₁₀(Q)')
ax2.set_ylabel('α efectivo')
ax2.set_title('α efectivo vs log(Q)')
ax2.legend()
ax2.axhline(y=0.6, color='gray', linestyle=':', alpha=0.5, label='α = 0.6 (original)')

# Panel 3: Predicción vs Observado
ax3 = axes[2]
obs = [iso['log_ratio_obs'] for iso in isotopes]
pred = [iso['pred'] for iso in isotopes]
colors3 = ['green' if iso['tipo'] == 'EXP' else 'orange' for iso in isotopes]

ax3.scatter(obs, pred, c=colors3, s=100, edgecolors='black')
for iso in isotopes:
    ax3.annotate(iso['name'], (iso['log_ratio_obs'], iso['pred']), textcoords="offset points", xytext=(5,5))

# Línea perfecta
lims = [min(min(obs), min(pred))-0.5, max(max(obs), max(pred))+0.5]
ax3.plot(lims, lims, 'k--', alpha=0.5, label='Predicción perfecta')
ax3.set_xlim(lims)
ax3.set_ylim(lims)
ax3.set_xlabel('log(ratio) Observado')
ax3.set_ylabel('log(ratio) Predicho')
ax3.set_title('Predicción vs Observado')
ax3.legend()

plt.tight_layout()
plt.savefig('/home/user/gravitational-wave-echoes-5d/QUANTUM_KLEIN_DEVELOPMENT/error_pattern_analysis.png', dpi=150)
print("\n[Gráfico guardado en error_pattern_analysis.png]")

# =============================================================================
# CONCLUSIÓN
# =============================================================================

print("\n" + "=" * 80)
print("CONCLUSIÓN")
print("=" * 80)

print(f"""
HALLAZGO PRINCIPAL:
   El error de predicción correlaciona con Q-value.
   Isótopos con Q más alto tienen mayor error (en general).

POSIBLES EXPLICACIONES:

1. α DEPENDE DE Q (física nueva):
   La modulación Klein es más efectiva para decaimientos de baja energía.
   α(Q) = {intercept:.3f} + {slope:.3f} × log₁₀(Q)

2. ERROR EN CÁLCULOS TEÓRICOS:
   Ra-228 y Ac-227 son cálculos teóricos con incertidumbre factor ~2.
   El error podría estar en ellos, no en Klein.

3. FÍSICA NUCLEAR ADICIONAL:
   Isótopos pesados/complejos tienen más canales de decaimiento.
   La fórmula simple podría necesitar correcciones.

RECOMENDACIÓN:
   Esperar datos experimentales de Ra-228 o Ac-227 antes de concluir.
   Si coinciden con la predicción Klein (α constante), el error es teórico.
   Si no coinciden, α variable podría ser necesario.
""")
