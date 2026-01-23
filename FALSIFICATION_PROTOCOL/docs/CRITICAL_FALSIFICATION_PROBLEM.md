# PROBLEMA CRÍTICO: ¿Cómo falsear si f₀ está fuera de LIGO?

**Fecha:** Enero 2026
**Status:** ⚠️ PROBLEMA EPISTEMOLÓGICO ABIERTO

---

## El Problema

```
LIGO detecta:     20 - 2000 Hz
Klein f₀:         5.68 Hz
                  ↓
            FUERA DEL RANGO
```

**Pregunta:** Si no podemos detectar directamente f₀ = 5.68 Hz, ¿la teoría es falseable?

---

## Lo que SÍ podemos medir

### 1. Ecos (Echo Delay)

El delay de eco es τ = 1/f₀:

```
τ = 1 / 5.68 Hz = 176 ms
```

**ESTO SÍ ES DETECTABLE** - Los ecos post-merger ocurren en escalas de ~100-500 ms.

**Búsqueda de falsificación:**
- Si NO hay ecos a τ ~ 176 ms en NINGÚN evento → FALSIFICADO
- Búsquedas actuales (Abedi et al.) reportan señales tentativas

### 2. Efectos Doppler Indirectos

Lo que medimos con 10σ son efectos INDIRECTOS:
- Twist factors modifican amplitudes
- Correlación z-Doppler (r = -0.9996)
- Distribución de estados Klein

**Problema:** ¿Son estos efectos reales o ajuste de ruido?

### 3. Correlaciones Espurias

**Preocupación legítima:**
- 5 parámetros libres pueden ajustar cualquier cosa
- ¿El 10σ es real o artifact estadístico?

---

## Propuestas de Falsificación Directa

### A. Búsqueda de Ecos a τ = 176 ms

```python
# Predicción específica
τ_klein = 1 / 5.68  # = 176.06 ms
Δτ = ±10 ms         # Incertidumbre

# Búsqueda en datos post-merger
# Si 0 detecciones en 200+ eventos → PROBLEMA
```

**Status:** Factible con datos actuales

### B. Detectores de Baja Frecuencia (Futuro)

| Detector | Rango | f₀ = 5.68 Hz |
|----------|-------|--------------|
| LIGO | 20-2000 Hz | NO |
| Einstein Telescope | 3-10,000 Hz | **SÍ** |
| LISA | 0.1 mHz - 1 Hz | NO |
| Pulsar Timing | nHz-μHz | NO |

**Einstein Telescope** (2030s) podría detectar f₀ = 5.68 Hz directamente.

### C. Test de Predicción Ciega

Hacer predicciones ANTES de O4/O5:
1. Predecir distribución de twist factors
2. Predecir correlaciones específicas
3. Comparar con datos nuevos

Si las predicciones fallan → FALSIFICADO

### D. Galaxias Ornitorrinco (Independiente)

Si Klein es correcto:
- σ_v ~ 10 km/s para Platypus
- Morfología sin mergers

Si JWST muestra σ_v > 50 km/s → Klein falsificado independientemente

---

## Análisis Crítico del 10σ

### ¿Es real o espurio?

**Argumentos a favor:**
- r = -0.9996 es demasiado perfecto para ser ruido
- Twist factors muestran 6.12σ vs random
- Múltiples correlaciones consistentes

**Argumentos en contra:**
- No medimos f₀ directamente
- Modelo tiene parámetros ajustables
- Correlación perfecta es... ¿sospechosa?

### Test de robustez necesario

```python
# 1. Jackknife: remover 10% de eventos
#    Si 10σ cae a 2σ → Resultado frágil

# 2. Cross-validation: train/test split
#    Si test muestra 0σ → Overfitting

# 3. Datos sintéticos: generar con H0 (sin Klein)
#    Si igual damos 10σ → Metodología mal
```

---

## Conclusión Honesta

### Lo que sabemos:
- Doppler-Klein pasa 5/5 tests (10σ)
- ε_max = 0.65 es robusto
- Correlaciones son fuertes

### Lo que NO sabemos:
- Si f₀ = 5.68 Hz existe realmente
- Si los efectos son genuinos o fitting
- Si la teoría es falseable con LIGO

### Camino hacia falsificación real:

1. **AHORA:** Búsqueda de ecos a τ = 176 ms
2. **PRONTO:** Predicciones ciegas para O4
3. **FUTURO:** Einstein Telescope (detección directa)
4. **INDEPENDIENTE:** JWST Platypus (σ_v ~ 10 km/s)

---

## Propuesta de Trabajo

Crear un script que:
1. Busque ecos en datos post-merger a τ = 176 ± 20 ms
2. Compare con τ random para null hypothesis
3. Reporte si hay señal estadística

**Si NO hay ecos → Evidencia contra Klein**
**Si SÍ hay ecos → Confirmación independiente**

---

*"Una teoría que no puede ser refutada por ningún suceso concebible no es científica."* — Karl Popper

