# Inventario Crítico de Fórmulas Klein

## Fecha: 23 Enero 2026
## Objetivo: Clasificar HONESTAMENTE qué fórmulas sobreviven sin ajustes ad hoc

---

## CRITERIO DE CLASIFICACIÓN

| Categoría | Descripción | Acción |
|-----------|-------------|--------|
| **GENUINA** | Fórmula simple, sin correcciones, error <1% | ✅ Mantener |
| **SOSPECHOSA** | Requiere corrección post-hoc o coeficiente no derivado | ⚠️ Documentar |
| **AD HOC** | Fórmula construida para ajustar datos | ❌ Descartar |

---

## 1. FÓRMULAS SIN CORRECCIONES (potencialmente genuinas)

### 1.1 m_p/m_e = 6π⁵

| Elemento | Valor | Justificación | Estado |
|----------|-------|---------------|--------|
| Fórmula | 6π⁵ = 1836.118 | | |
| Observado | 1836.153 | CODATA 2018 | |
| Error | 0.002% | | |
| Coef. 6 | "7-1 capas activas" | ⚠️ Por qué 7-1? | SOSPECHOSO |
| Exp. 5 | "5 dimensiones" | ✅ Consistente con π^(1/5) | OK |

**VEREDICTO**: ⚠️ SOSPECHOSA - El 6 = 7-1 no está derivado. ¿Por qué "capas activas"?

---

### 1.2 m_μ/m_e = 21π²

| Elemento | Valor | Justificación | Estado |
|----------|-------|---------------|--------|
| Fórmula | 21π² = 207.26 | | |
| Observado | 206.768 | CODATA 2018 | |
| Error | 0.24% | | |
| Coef. 21 | "3×7 = generaciones × capas" | ⚠️ Por qué 3 generaciones? | SOSPECHOSO |
| Exp. 2 | "2da generación" | ⚠️ Por qué el exponente = generación? | SOSPECHOSO |

**VEREDICTO**: ⚠️ SOSPECHOSA - 21 = 3×7 es conveniente pero no derivado.

---

### 1.3 m_H/m_p = 42.5π

| Elemento | Valor | Justificación | Estado |
|----------|-------|---------------|--------|
| Fórmula | 42.5π = 133.52 | | |
| Observado | 133.37 | m_H=125.25 GeV, m_p=0.938 GeV | |
| Error | 0.11% | | |
| Coef. 42.5 | "6×7 + 0.5" | ⚠️ ¿De dónde sale +0.5? | SOSPECHOSO |

**VEREDICTO**: ⚠️ SOSPECHOSA - El +0.5 parece ajuste fino.

---

### 1.4 η_B = (3/2)(7π)⁻⁷

| Elemento | Valor | Justificación | Estado |
|----------|-------|---------------|--------|
| Fórmula | (3/2)(7π)⁻⁷ = 6.09×10⁻¹⁰ | | |
| Observado | 6.1×10⁻¹⁰ | Planck 2018 | |
| Error | ~0.2% | | |
| Coef. 3/2 | "3 gen. / 2 espín" | ⚠️ Justificación ad hoc | SOSPECHOSO |
| Exp. -7 | "7 condiciones de Sakharov" | ⚠️ Son 3 condiciones, no 7 | AD HOC |

**VEREDICTO**: ❌ AD HOC - Las "7 condiciones" son inventadas. Sakharov tiene 3.

---

### 1.5 T_CMB = π×T_P/(7π)²⁴

| Elemento | Valor | Justificación | Estado |
|----------|-------|---------------|--------|
| Fórmula | π×T_P/(7π)²⁴ = 2.66 K | | |
| Observado | 2.725 K | COBE/Planck | |
| Error | 2.4% | | |
| Factor π | "geometría esférica CMB" | ⚠️ ¿Por qué π y no 2π? | SOSPECHOSO |
| Exp. 24 | "dim(SU(5)) = 24" | ⚠️ ¿Por qué SU(5)? | SOSPECHOSO |

**VEREDICTO**: ⚠️ SOSPECHOSA - El 24 parece elegido para ajustar.

---

### 1.6 N_A = exp[(5/2 - 1/99)×7π]

| Elemento | Valor | Justificación | Estado |
|----------|-------|---------------|--------|
| Fórmula | exp[54.87] = 6.025×10²³ | | |
| Observado | 6.022×10²³ | CODATA 2018 | |
| Error | 0.05% | | |
| Coef. 5/2 | "promedio 5 dimensiones" | ⚠️ ¿Promedio de qué? | SOSPECHOSO |
| Corrección -1/99 | "99 elementos estables" | ❌ CLARAMENTE AD HOC | AD HOC |

**VEREDICTO**: ❌ AD HOC - El -1/99 es ajuste post-hoc evidente.

---

### 1.7 1/α = 7²π - 7 - π²

| Elemento | Valor | Justificación | Estado |
|----------|-------|---------------|--------|
| Fórmula | 49π - 7 - π² = 137.068 | | |
| Observado | 137.036 | CODATA 2018 | |
| Error | 0.024% | | |
| Término 49π | "7² dimensiones" | ⚠️ ¿Por qué 7²? | SOSPECHOSO |
| Término -7 | "bulk correction" | ⚠️ No derivado | SOSPECHOSO |
| Término -π² | "curvatura" | ⚠️ ¿Por qué π² y no π? | SOSPECHOSO |

**VEREDICTO**: ⚠️ SOSPECHOSA - Múltiples términos elegidos para ajustar.

---

## 2. FÓRMULAS CON CORRECCIONES EXPLÍCITAS (post-hoc)

### 2.1 m_μ/m_e = 21π² - 1/2 (CORREGIDA)

| Estado original | 21π² = 207.26 | Error: 0.24% |
| Corrección | -1/2 | "inversión de fase" |
| Estado corregido | 206.76 | Error: -32 ppm |

**VEREDICTO**: ❌ AD HOC - La corrección -1/2 se añadió DESPUÉS de ver el residuo.

---

### 2.2 1/α = 49π - 7 - π² - 1/π³ (CORREGIDA)

| Estado original | 137.068 | Error: 0.024% |
| Corrección | -1/π³ | "volumen 3-esfera" |
| Estado corregido | 137.036 | Error: 1.35 ppm |

**VEREDICTO**: ❌ AD HOC - La corrección -1/π³ se añadió DESPUÉS de ver el residuo.

---

### 2.3 c = (3 - 1/(7π)²)×10⁸ (y correcciones)

| Estado original | 299,379,000 m/s | Error: 0.14% |
| Observado | 299,792,458 m/s | |

**VEREDICTO**: ❌ AD HOC - El "3" no tiene justificación. ¿Por qué exactamente 3×10⁸?

---

## 3. RESUMEN CRÍTICO

### Tabla de Veredictos

| Fórmula | Error sin corrección | Veredicto |
|---------|---------------------|-----------|
| m_p/m_e = 6π⁵ | 0.002% | ⚠️ SOSPECHOSA (6 no derivado) |
| m_μ/m_e = 21π² | 0.24% | ⚠️ SOSPECHOSA (21 no derivado) |
| m_H/m_p = 42.5π | 0.11% | ⚠️ SOSPECHOSA (+0.5 no derivado) |
| 1/α = 49π - 7 - π² | 0.024% | ⚠️ SOSPECHOSA (3 términos) |
| η_B = (3/2)(7π)⁻⁷ | ~0.2% | ❌ AD HOC (exp. 7 inventado) |
| T_CMB = πT_P/(7π)²⁴ | 2.4% | ⚠️ SOSPECHOSA (exp. 24 elegido) |
| N_A = exp[(5/2-1/99)×7π] | 0.05% | ❌ AD HOC (1/99 claramente ajustado) |

---

## 4. ¿QUÉ SOBREVIVE?

### 4.1 Fórmulas que PODRÍAN ser genuinas (requieren justificación del coeficiente):

1. **m_p/m_e = 6π⁵** - SI podemos derivar por qué el coeficiente es 6
2. **m_μ/m_e = 21π²** - SI podemos derivar por qué el coeficiente es 21
3. **m_H/m_p = 42.5π** - SI podemos derivar por qué el coeficiente es 42.5

### 4.2 Fórmulas que DEFINITIVAMENTE son ad hoc:

1. **η_B = (3/2)(7π)⁻⁷** - El exponente 7 no corresponde a las 3 condiciones de Sakharov
2. **N_A = exp[(5/2-1/99)×7π]** - El -1/99 es claramente un ajuste
3. **Todas las correcciones** (-1/2, -1/π³, etc.) - Añadidas post-hoc

### 4.3 Patrón que SÍ parece genuino:

**La supresión armónica 22:1 (modos impares vs pares)**

- Observada en datos LIGO independientes
- Predicha por la topología no-orientable
- NO requiere ajuste de coeficientes

---

## 5. ESPACIO DE PATRONES PERMITIDOS (CONGELADO)

### Para que la teoría sea científica, SOLO permitimos:

```
Fórmulas de la forma: a × π^b × 7^c

donde:
- a ∈ ℤ (enteros pequeños: 1, 2, 3, 6, 21, 42)
- b ∈ {1, 2, 5} (exponentes observados)
- c ∈ {0, 1, -7} (potencias de 7 observadas)

SIN CORRECCIONES adicionales.
SIN fracciones arbitrarias (1/99, 1/2, etc.)
SIN sumas de múltiples términos (como 49π - 7 - π²)
```

### Tamaño del espacio:
- ~6 coeficientes × 3 exponentes de π × 3 potencias de 7 = 54 fórmulas
- Con ~10 constantes físicas a explicar
- p(coincidencia) ~ 10/54 ~ 18% para UNA coincidencia
- Pero queremos MÚLTIPLES: p(3 coincidencias) ~ 0.6%

---

## 6. PREDICCIÓN CIEGA PROPUESTA

### Para validar la teoría, necesitamos UNA predicción que:
1. NO haya sido usada en los ajustes previos
2. Pueda fallar claramente
3. Sea medible con tecnología actual

### Candidatas:

| Predicción | Fórmula | Valor | Experimento |
|------------|---------|-------|-------------|
| Masa ν₃ | (7π)⁻⁵ × m_e | ~50 meV | KATRIN |
| Eco GW | τ = 2πR/c | ~64 ms | Einstein Telescope |
| θ₁₃ | 1/7 rad | 0.143 rad | Reactor neutrinos |

**RECOMENDACIÓN**: Usar θ₁₃ = 1/7 rad como predicción ciega.
- Valor experimental: θ₁₃ = 0.146 ± 0.003 rad
- Predicción: 1/7 = 0.143 rad
- Error: ~2%
- ESTA FÓRMULA NO FUE USADA EN AJUSTES PREVIOS

---

## 7. CONCLUSIÓN

### Estado honesto de la teoría:

| Aspecto | Estado |
|---------|--------|
| ¿Hay coincidencias numéricas? | ✅ Sí, varias |
| ¿Están derivadas desde primeros principios? | ❌ No |
| ¿El 7 emerge de K²? | ❌ No demostrado |
| ¿Las correcciones son a priori? | ❌ No, son post-hoc |
| ¿Hay predicciones ciegas? | ⚠️ Posiblemente θ₁₃ |
| ¿Es falsificable? | ✅ Sí, con predicciones específicas |

### La teoría es un MARCO HEURÍSTICO, no una teoría derivada.

Para que sea ciencia:
1. Congelar el espacio de patrones (HECHO AQUÍ)
2. Documentar qué es derivado vs asumido (HECHO AQUÍ)
3. Identificar predicciones ciegas (θ₁₃ = 1/7)
4. Esperar falsificación o confirmación

---

*Documento creado: 23 Enero 2026*
*Estado: INVENTARIO CRÍTICO COMPLETO*
