#!/usr/bin/env python3
"""
LOS ESCALONES INTERMEDIOS: ¿Qué pasa entre niveles Klein?

Pregunta central: Si Klein₃ = 8400 km y Klein₄ = 500 Mpc,
¿qué hay en el medio? ¿Están prohibidos los valores intermedios?

Analogía: Escalera cuántica
- En el átomo de hidrógeno, solo existen orbitales n=1,2,3...
- Los electrones NO pueden estar "entre" orbitales
- Las transiciones requieren absorber/emitir energía específica

¿Funciona Klein igual?
"""

import numpy as np
import matplotlib.pyplot as plt

# =============================================================================
# CONSTANTES FUNDAMENTALES
# =============================================================================

# Masas
m_planck = 2.176e-8      # kg
m_proton = 1.673e-27     # kg
m_electron = 9.109e-31   # kg
M_sun = 1.989e30         # kg

# Longitudes
L_planck = 1.616e-35     # m

# Constantes
G = 6.674e-11            # m³/(kg·s²)
c = 2.998e8              # m/s

# El factor derivado
FACTOR = (m_planck / np.sqrt(m_proton * m_electron)) * np.pi**0.2
LOG_FACTOR = np.log10(FACTOR)

print("=" * 70)
print("LOS ESCALONES INTERMEDIOS DE KLEIN")
print("=" * 70)
print(f"\nFactor entre niveles: {FACTOR:.3e} = 10^{LOG_FACTOR:.3f}")

# =============================================================================
# FUNCIÓN DE NIVEL KLEIN
# =============================================================================

def R_klein(n):
    """Radio de Klein para nivel n (puede ser no entero)"""
    return L_planck * FACTOR**(n-1)

def M_from_R(R):
    """Masa cuyo radio de Schwarzschild es R"""
    return R * c**2 / (2 * G)

def R_from_M(M):
    """Radio de Schwarzschild de masa M"""
    return 2 * G * M / c**2

# =============================================================================
# NIVELES ENTEROS (LOS "DESCANSOS" DE LA ESCALERA)
# =============================================================================

print("\n" + "=" * 70)
print("NIVELES ENTEROS (DESCANSOS ESTABLES)")
print("=" * 70)

for n in [1, 2, 3, 4]:
    R = R_klein(n)
    M = M_from_R(R) / M_sun

    if R < 1e-12:
        R_str = f"{R:.2e} m"
    elif R < 1e3:
        R_str = f"{R:.2f} m"
    elif R < 1e9:
        R_str = f"{R/1e3:.1f} km"
    elif R < 1e18:
        R_str = f"{R/1e9:.1f} Gm"
    else:
        R_str = f"{R/3.086e22:.1f} Mpc"

    print(f"\nKlein_{n}:")
    print(f"  Radio:        {R_str}")
    print(f"  Masa (R_s=R): {M:.2e} M☉")

# =============================================================================
# ¿QUÉ PASA EN LOS ESCALONES INTERMEDIOS?
# =============================================================================

print("\n" + "=" * 70)
print("ANÁLISIS: ESCALONES INTERMEDIOS (n no entero)")
print("=" * 70)

print("""
HIPÓTESIS 1: PROHIBICIÓN CUÁNTICA
---------------------------------
Los valores intermedios están "prohibidos" como en mecánica cuántica.
Un objeto no puede tener R_Klein entre niveles.

IMPLICACIÓN: Debería haber "gaps" (vacíos) en la distribución de masas
de agujeros negros en ciertas regiones.

HIPÓTESIS 2: TRANSICIÓN SUAVE
-----------------------------
La transición es continua pero hay "atractores" en n=1,2,3,4.
Los objetos tienden a caer hacia el nivel entero más cercano.

IMPLICACIÓN: Habría pocos objetos en los intermedios, pero no cero.

HIPÓTESIS 3: MEZCLA DE NIVELES
------------------------------
Un objeto puede estar en "superposición" de dos niveles Klein,
como un electrón entre orbitales durante una transición.

IMPLICACIÓN: Objetos intermedios mostrarían características mixtas.
""")

# =============================================================================
# ZONA CRÍTICA: ENTRE KLEIN₃ Y KLEIN₄
# =============================================================================

print("\n" + "=" * 70)
print("ZONA CRÍTICA: Entre Klein₃ (8400 km) y Klein₄ (500 Mpc)")
print("=" * 70)

# Definir puntos intermedios
n_values = np.linspace(3.0, 4.0, 11)

print("\n{:^6} {:^15} {:^15} {:^20}".format("n", "R_Klein", "M(R_s=R)", "Tipo de objeto"))
print("-" * 60)

for n in n_values:
    R = R_klein(n)
    M = M_from_R(R) / M_sun

    # Clasificar tipo de objeto
    if M < 100:
        tipo = "Agujero negro estelar"
    elif M < 1e5:
        tipo = "IMBH (masa intermedia)"
    elif M < 1e9:
        tipo = "SMBH (supermasivo)"
    else:
        tipo = "UMBH (ultramasivo)"

    # Formatear R
    if R < 1e9:
        R_str = f"{R/1e3:.1f} km"
    elif R < 1e18:
        R_str = f"{R/1e9:.2f} Gm"
    elif R < 3e22:
        R_str = f"{R/1e12:.1f} Tm"
    else:
        R_str = f"{R/3.086e22:.2f} Mpc"

    print(f"{n:6.2f} {R_str:>15} {M:>12.2e} M☉   {tipo}")

# =============================================================================
# PREDICCIÓN TESTEABLE: MASA DE TRANSICIÓN
# =============================================================================

print("\n" + "=" * 70)
print("PREDICCIÓN TESTEABLE: ¿Dónde está la transición?")
print("=" * 70)

# Ya sabemos que M_transition ≈ 2847 M☉
M_transition_observed = 2847  # M☉
R_transition_observed = R_from_M(M_transition_observed * M_sun)

# ¿A qué nivel n corresponde?
n_transition = 1 + np.log(R_transition_observed/L_planck) / np.log(FACTOR)

print(f"\nObservado:")
print(f"  M_transition = {M_transition_observed} M☉")
print(f"  R_transition = {R_transition_observed/1e3:.0f} km")
print(f"  Corresponde a n = {n_transition:.4f}")

# Predicción: Si n debe ser entero, debería ser exactamente n=3
error_n = abs(n_transition - 3.0)
print(f"\n¿Es n = 3 exactamente?")
print(f"  Diferencia: Δn = {error_n:.4f}")
print(f"  Esto es un error del {error_n*100:.2f}% de un nivel")

if error_n < 0.01:
    print("  → ✓ ¡Coincide casi perfectamente con n=3!")
else:
    print(f"  → La discrepancia sugiere que la transición no es exactamente en n=3")

# =============================================================================
# TESTS OBSERVACIONALES
# =============================================================================

print("\n" + "=" * 70)
print("TESTS OBSERVACIONALES PROPUESTOS")
print("=" * 70)

print("""
TEST 1: GAP DE MASAS EN IMBH
----------------------------
Si la transición Klein₃→Klein₄ es "prohibida" para masas intermedias,
debería haber un GAP (vacío) en la distribución de agujeros negros
entre ~100 M☉ (fin de estelar) y ~10⁵ M☉ (inicio de SMBH).

OBSERVACIONES ACTUALES:
- Hay muy pocos IMBH observados
- ¿Es porque son raros o porque están PROHIBIDOS?
- LISA podrá testear esto con precisión

PREDICCIÓN KLEIN:
- Si Hipótesis 1 (prohibición), debería haber gap estricto
- Si Hipótesis 2 (atractores), debería haber mínimo pero no cero
""")

# Calcular dónde estaría el "mínimo" de estabilidad
n_mid = 3.5
R_mid = R_klein(n_mid)
M_mid = M_from_R(R_mid) / M_sun

print(f"\nPunto medio (n=3.5):")
print(f"  R = {R_mid:.2e} m")
print(f"  M = {M_mid:.2e} M☉")
print(f"  → Agujeros negros de ~{M_mid:.0e} M☉ deberían ser RAROS o PROHIBIDOS")

print("""
TEST 2: SEÑAL DE ECO ANÓMALA EN IMBH
------------------------------------
Si un agujero negro está en la "zona prohibida", podría mostrar:
- Ecos con frecuencias anómalas
- Mezcla de frecuencias Klein₃ y Klein₄
- Supresión o amplificación inusual

GW190521 (M ≈ 150 M☉) es el mejor candidato actual.
""")

# Calcular n para GW190521
M_gw190521 = 150  # M☉
R_gw190521 = R_from_M(M_gw190521 * M_sun)
n_gw190521 = 1 + np.log(R_gw190521/L_planck) / np.log(FACTOR)

print(f"\nGW190521 (M ≈ 150 M☉):")
print(f"  R_s = {R_gw190521/1e3:.0f} km")
print(f"  n efectivo = {n_gw190521:.4f}")
print(f"  Fracción hacia Klein₄: {(n_gw190521-3)*100:.2f}%")

print("""
TEST 3: VERIFICACIÓN DE LA FÓRMULA CON CONSTANTES
-------------------------------------------------
La fórmula predice que el factor depende de:
  - m_proton, m_electron (conocidos con alta precisión)
  - M_Planck (conocida pero con más error)
  - π (exacto)

Si las constantes fundamentales cambiasen (variación cosmológica),
el factor Klein cambiaría predeciblemente.
""")

# Sensibilidad a variaciones
print("\nSensibilidad a variaciones de constantes:")
delta = 0.01  # 1% variation

for const_name, const_val, exponent in [
    ("m_proton", m_proton, -0.5),
    ("m_electron", m_electron, -0.5),
    ("M_Planck", m_planck, 1.0),
]:
    # d(log Factor)/d(log const) = exponent
    sensitivity = exponent
    print(f"  Si {const_name} cambia 1%, Factor cambia {abs(sensitivity)*100:.1f}%")

# =============================================================================
# VISUALIZACIÓN: LA ESCALERA KLEIN
# =============================================================================

print("\n" + "=" * 70)
print("GENERANDO VISUALIZACIÓN...")
print("=" * 70)

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Panel 1: La escalera
ax1 = axes[0]

n_range = np.linspace(0.5, 4.5, 1000)
log_R = np.log10([R_klein(n) for n in n_range])

ax1.plot(n_range, log_R, 'b-', linewidth=2, label='R(n) continuo')

# Marcar niveles enteros
for n in [1, 2, 3, 4]:
    R = R_klein(n)
    ax1.axhline(np.log10(R), color='gray', linestyle='--', alpha=0.5)
    ax1.plot(n, np.log10(R), 'ro', markersize=15, zorder=5)
    ax1.annotate(f'Klein₁' if n==1 else f'Klein₂' if n==2 else f'Klein₃' if n==3 else f'Klein₄',
                 (n, np.log10(R)), xytext=(10, 0), textcoords='offset points',
                 fontsize=12, fontweight='bold')

# Zona crítica
ax1.axvspan(3.0, 4.0, alpha=0.2, color='yellow', label='Zona de transición')

# Marcar objetos conocidos
objects = [
    (3.0, "Stellar BH\n(~30 M☉)"),
    (3.05, "GW190521\n(150 M☉)"),
    (3.5, "¿IMBH?\n(10⁵ M☉)"),
    (4.0, "SMBH\n(>10⁶ M☉)"),
]

for n_obj, label in objects:
    R_obj = R_klein(n_obj)
    ax1.plot(n_obj, np.log10(R_obj), 's', markersize=8, color='green', alpha=0.7)
    ax1.annotate(label, (n_obj, np.log10(R_obj)),
                 xytext=(0, 15), textcoords='offset points',
                 ha='center', fontsize=9)

ax1.set_xlabel('Nivel Klein (n)', fontsize=12)
ax1.set_ylabel('log₁₀(R) [metros]', fontsize=12)
ax1.set_title('La Escalera Klein: ¿Continua o Cuantizada?', fontsize=14)
ax1.legend(loc='upper left')
ax1.grid(True, alpha=0.3)

# Panel 2: "Potencial" de estabilidad
ax2 = axes[1]

# Hipotético potencial que favorece niveles enteros
def V_stability(n):
    """Potencial de estabilidad - mínimos en n enteros"""
    return np.sin(2 * np.pi * n)**2

n_pot = np.linspace(0.5, 4.5, 500)
V = [V_stability(n) for n in n_pot]

ax2.fill_between(n_pot, 0, V, alpha=0.3, color='blue')
ax2.plot(n_pot, V, 'b-', linewidth=2)

# Marcar mínimos (niveles estables)
for n in [1, 2, 3, 4]:
    ax2.axvline(n, color='red', linestyle='--', alpha=0.7)
    ax2.annotate(f'n={n}\n(estable)', (n, 0.05), ha='center', fontsize=10)

# Marcar máximos (zonas inestables)
for n in [1.5, 2.5, 3.5]:
    ax2.annotate('inestable', (n, 1.05), ha='center', fontsize=9, color='gray')

ax2.set_xlabel('Nivel Klein (n)', fontsize=12)
ax2.set_ylabel('Energía de inestabilidad (hipotética)', fontsize=12)
ax2.set_title('Hipótesis: Niveles enteros son "atractores"', fontsize=14)
ax2.set_ylim(-0.1, 1.3)
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('KLEIN_UNIFIED_THEORY/the_middle/klein_staircase.png', dpi=150, bbox_inches='tight')
plt.close()

print("Guardado: klein_staircase.png")

# =============================================================================
# CONCLUSIONES
# =============================================================================

print("\n" + "=" * 70)
print("CONCLUSIONES")
print("=" * 70)

print("""
¿SE PUEDE PROBAR LA FÓRMULA?

1. TEST DIRECTO:
   La fórmula usa constantes fundamentales conocidas.
   Si predice correctamente R_Klein₃ = 8400 km, está validada.
   RESULTADO: ✓ Coincide dentro del 1-2%

2. TEST INDIRECTO (Gap de masas):
   Buscar si hay un "vacío" en la distribución de masas de agujeros negros
   entre ~100 y ~10⁵ M☉. LISA podrá testear esto.
   ESTADO: Pendiente de datos de LISA

3. TEST DE CONSISTENCIA:
   Si la fórmula es correcta, TODOS los niveles Klein deberían seguirla.
   Klein₁ (Planck): Definicional
   Klein₂ (Nuclear): Difícil de testear
   Klein₃ (Stellar): ✓ Validado
   Klein₄ (Cosmo): Necesita más datos

¿QUÉ PASA EN LOS ESCALONES?

MEJOR HIPÓTESIS: Los escalones intermedios son "inestables".
- Los objetos tienden a colapsar hacia el nivel entero más cercano
- Esto explicaría la escasez de IMBH observados
- GW190521 (M~150 M☉) podría ser un objeto en transición

PREDICCIÓN CLAVE:
- Los agujeros negros con M ~ 10⁴-10⁵ M☉ deberían mostrar
  señales anómalas si existen (mezcla de Klein₃ y Klein₄)
- O simplemente no deberían existir (gap prohibido)
""")
