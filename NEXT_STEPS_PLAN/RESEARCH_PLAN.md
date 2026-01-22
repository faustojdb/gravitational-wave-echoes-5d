# Plan de Investigación: Klein Theory - Próximos Pasos

**Fecha**: Enero 2026
**Estado**: Planificación para siguiente sesión

---

## Resumen del Progreso Actual

### Logros Validados
- **Doppler-Klein**: R=8400 km, f₀=5.68 Hz validado a 10σ con datos GWTC
- **ML Pattern Discovery**: Features Klein mejoran R² en +0.556 sobre features estándar
- **Correlaciones significativas**: ε vs residuos (r=-0.818), twist factor (6.12σ)

### Resultados Negativos (Honestos)
- **H₀ Tension**: Klein NO explica la tensión (ε≈0 requerido)
- **FRBs**: Evidencia débil con datos simulados

### Problemas Identificados
1. **Escala de SMBH**: R_Schwarzschild >> R_Klein para agujeros negros supermasivos
2. **H₀ a escala cosmológica**: Klein₃ no funciona a distancias z>>1

---

## Idea 1: Problema de Masa de SMBH

### El Problema

```
BH Estelar (30 M☉):    R_s = 90 km     << R_Klein = 8400 km  ✓ Funciona
BH Intermedio (1000 M☉): R_s = 3000 km   < R_Klein = 8400 km  ✓ Funciona
SMBH (10⁶ M☉):         R_s = 3×10⁶ km  >> R_Klein = 8400 km  ✗ ¿Qué pasa?
M87* (6.5×10⁹ M☉):     R_s = 2×10¹⁰ km >> R_Klein = 8400 km  ✗ ¿Qué pasa?
```

### Preguntas a Responder

1. ¿Desaparece el efecto Klein cuando R_s >> R_Klein?
2. ¿O hay un cambio de régimen a una escala Klein diferente?
3. ¿Qué predicen las observaciones de EHT (M87*, Sgr A*)?

### Plan de Análisis

#### Paso 1: Análisis de GWTC por Rangos de Masa
```python
# Dividir eventos por masa total
bins = [
    (0, 50),      # Stellar BH mergers
    (50, 200),    # Heavy stellar / light IMBH
    (200, 1000),  # IMBH range
    (1000, 10000) # Upper IMBH (si hay datos)
]

# Para cada bin:
# 1. Calcular correlación Klein
# 2. Ver si hay cambio de comportamiento cerca de M_critica
```

#### Paso 2: Buscar M_crítica
```python
# M_crítica = masa donde R_s ≈ R_Klein
# R_s = 3 × M_solar km
# R_Klein = 8400 km
# M_crítica ≈ 2800 M☉

# Predicción: transición de régimen cerca de esta masa
```

#### Paso 3: Comparar con Datos de IMBH
- Buscar eventos LIGO/Virgo con M > 100 M☉
- GW190521 (150 M☉) es candidato clave
- ¿Las correlaciones Klein cambian para eventos masivos?

### Archivos a Crear
- `scripts/smbh_mass_scaling_analysis.py`
- `results/mass_regime_transition.json`

---

## Idea 2: Hipótesis Matrioska-Klein

### Concepto

No hay UNA sola dimensión Klein, sino múltiples niveles anidados:

```
┌─────────────────────────────────────────────────────┐
│  Klein₁ (R ~ 10⁻³⁵ m) - Escala Planck              │
│    ┌─────────────────────────────────────────────┐  │
│    │  Klein₂ (R ~ 10⁻¹⁵ m) - Escala nuclear     │  │
│    │    ┌─────────────────────────────────────┐  │  │
│    │    │  Klein₃ (R = 8400 km) - GW         │  │  │  ← VALIDADO
│    │    │    ┌─────────────────────────────┐  │  │  │
│    │    │    │  Klein₄ (R ~ 10²² m) - Cosmo│  │  │  │  ← ¿Explica H₀?
│    │    │    └─────────────────────────────┘  │  │  │
│    │    └─────────────────────────────────────┘  │  │
│    └─────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
```

### Predicciones Testables

| Nivel | Radio | Frecuencia | Observable |
|-------|-------|------------|------------|
| Klein₃ | 8400 km | 5.68 Hz | Ecos GW (τ=176ms) |
| Klein₄ | ~10²² m | ~10⁻¹⁴ Hz | PTAs / NANOGrav |

### Plan de Análisis

#### Paso 1: Re-analizar H₀ con Klein₄
```python
# Hipótesis: Klein₄ tiene R ~ escala Hubble
# R_Hubble ~ c/H₀ ~ 4×10²⁶ m

# Nuevo modelo:
def klein4_distance_correction(z, R_klein4):
    """
    Klein₄ actúa a escalas cosmológicas.
    Diferente de Klein₃ que actúa a escalas de km.
    """
    # Efecto acumulativo sobre distancia cosmológica
    ...
```

#### Paso 2: Buscar f₀_cosmológico en NANOGrav
```python
# NANOGrav detecta GW en nHz (10⁻⁹ Hz)
# Si Klein₄ existe: f₀_cosmo ~ 10⁻⁸ - 10⁻¹⁴ Hz

# Buscar:
# 1. Estructura periódica en espectro PTA
# 2. Correlaciones espaciales tipo Klein
```

#### Paso 3: Análisis EHT
```python
# M87* y Sgr A* deberían "ver" Klein₄
# Predicciones:
# 1. Desviaciones de sombra respecto a GR
# 2. Diferencias sistemáticas entre SMBHs de diferente masa
```

### Archivos a Crear
- `scripts/matrioska_klein_analysis.py`
- `scripts/nanograv_klein4_search.py`
- `scripts/h0_tension_klein4.py`
- `results/matrioska_predictions.json`

---

## Plan de Ejecución Detallado

### Día 1: Análisis de Masa

**Mañana**
1. [ ] Cargar datos GWTC completos
2. [ ] Implementar análisis por bins de masa
3. [ ] Calcular correlaciones Klein para cada bin

**Tarde**
4. [ ] Buscar M_crítica en los datos
5. [ ] Analizar GW190521 y otros eventos masivos
6. [ ] Documentar resultados

### Día 2: Matrioska-Klein

**Mañana**
1. [ ] Implementar modelo Klein₄ para cosmología
2. [ ] Re-analizar H₀ tension con Klein₄
3. [ ] Buscar datos públicos de NANOGrav

**Tarde**
4. [ ] Analizar espectro PTA buscando f₀_cosmo
5. [ ] Calcular predicciones para EHT
6. [ ] Documentar hipótesis y predicciones

### Día 3: Integración

1. [ ] Unificar resultados de ambas líneas
2. [ ] Escribir documento teórico completo
3. [ ] Identificar predicciones falsificables
4. [ ] Preparar para posible publicación

---

## Predicciones Falsificables

### Para Idea 1 (Masa SMBH)
```
PREDICCIÓN: Correlaciones Klein deberían DEBILITARSE
para M_total > M_crítica ≈ 2800 M☉

FALSIFICACIÓN: Si correlaciones se mantienen iguales
para todos los rangos de masa → El modelo actual es incompleto
```

### Para Idea 2 (Matrioska-Klein)
```
PREDICCIÓN 1: H₀ tension explicable si Klein₄ tiene R ~ 10²⁶ m
FALSIFICACIÓN: Si Klein₄ no mejora fit de H₀ → Matrioska no explica cosmología

PREDICCIÓN 2: NANOGrav debería mostrar f₀_cosmo en espectro
FALSIFICACIÓN: Si espectro PTA es suave sin estructura → No hay Klein₄ detectable

PREDICCIÓN 3: Transición de régimen entre Klein₃ y Klein₄
FALSIFICACIÓN: Si no hay cambio de comportamiento cerca de M_crítica
```

---

## Datos Necesarios

### Disponibles
- [x] GWTC-1, 2, 3 (ya descargados)
- [x] Parámetros validados de Klein₃

### A Obtener
- [ ] Datos públicos de NANOGrav 15-year
- [ ] Mediciones EHT de M87* y Sgr A*
- [ ] Lista completa de eventos IMBH candidatos

---

## Notas Importantes

### Lo que sabemos
1. Klein₃ (R=8400 km) funciona para BH estelares (10σ)
2. H₀ tension NO se explica con Klein₃
3. Features Klein capturan información real (ML: R²+0.556)

### Lo que no sabemos
1. ¿Hay transición de régimen a masas altas?
2. ¿Existe Klein₄ a escala cosmológica?
3. ¿Por qué f₀=5.68 Hz y no otro valor?

### Filosofía de investigación
> "La ciencia avanza por predicciones falsificables. Cada análisis debe
> tener un resultado claro que pueda decir 'sí' o 'no' a la hipótesis."

---

## Recursos

### Papers relevantes
- Abedi et al. (2017): Echoes from the Abyss
- NANOGrav Collaboration: 15-year data release
- EHT Collaboration: M87* and Sgr A* results

### Código existente
- `FALSIFICATION_PROTOCOL/scripts/ml_klein_pattern_discovery.py`
- `FALSIFICATION_PROTOCOL/scripts/h0_tension_klein_analysis.py`
- `FALSIFICATION_PROTOCOL/docs/MATRIOSKA_KLEIN_HYPOTHESIS.md`

---

*Plan creado: Enero 2026*
*Para continuar mañana con análisis detallado*
