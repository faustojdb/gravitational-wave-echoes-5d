# Protocolo de Análisis: Supresión Armónica en Datos LIGO Reales

## DOCUMENTO CONGELADO - 23 Enero 2026
## NO MODIFICAR DESPUÉS DE INICIAR ANÁLISIS

---

## 1. OBJETIVO

Determinar si existe supresión de modos armónicos pares en formas de onda gravitacionales reales de LIGO, como predice la Teoría Klein.

---

## 2. HIPÓTESIS (definidas ANTES de ver datos)

### H₀ (Hipótesis Nula - GR Estándar):
```
No hay supresión preferencial de modos pares.
Ratio esperado: A_odd / A_even ≈ 1.0 ± 0.5
```

### H₁ (Hipótesis Klein):
```
Los modos pares están suprimidos por topología no-orientable.
Ratio esperado: A_odd / A_even ≈ 7π ≈ 22 (rango: 15-30)
```

### H₂ (Hipótesis Klein Fuerte):
```
Supresión extrema de modos pares.
Ratio esperado: A_odd / A_even ≈ 40 (rango: 35-45)
```

---

## 3. CRITERIOS DE DECISIÓN (pre-registrados)

| Ratio Observado | Decisión |
|-----------------|----------|
| < 2 | ✅ Confirma H₀, ❌ Refuta Klein |
| 2 - 10 | ⚠️ Ambiguo, requiere más datos |
| 10 - 20 | ⚠️ Sugestivo de Klein, no conclusivo |
| 20 - 35 | ✅ Confirma H₁ (Klein moderado) |
| > 35 | ✅ Confirma H₂ (Klein fuerte) |

### Significancia estadística requerida:
- p < 0.05 para rechazar H₀
- Al menos 3 eventos con ratio consistente

---

## 4. DATOS A USAR

### Fuente:
- GWOSC (Gravitational Wave Open Science Center)
- https://gwosc.org

### Eventos seleccionados (por SNR):

| Evento | SNR | Tipo | Justificación |
|--------|-----|------|---------------|
| GW150914 | 24 | BBH | Primer evento, gold standard |
| GW170814 | 15 | BBH | Triple detección (HLV) |
| GW190521 | 15 | BBH | Masa extrema (IMBH) |
| GW170817 | 32 | BNS | Control: si Klein aplica, NS también |

### Formato de datos:
- Archivos HDF5 de GWOSC
- Sampling rate: 4096 Hz o 16384 Hz
- Duración: ±4 segundos alrededor del merger

---

## 5. METODOLOGÍA

### Paso 1: Descarga de datos
```python
# Usar GWOSC API
# Descargar strain data para cada evento
# Verificar integridad (checksum)
```

### Paso 2: Pre-procesamiento
```python
# Extraer ventana temporal: t_merger ± 2 segundos
# Aplicar bandpass filter: 20-500 Hz
# Whitening para normalizar ruido
# NO aplicar ningún modelo Klein
```

### Paso 3: Análisis FFT
```python
# Calcular FFT de la señal
# Identificar frecuencia fundamental f_0 (peak más alto)
# Calcular amplitudes en armónicos: f_0, 2*f_0, 3*f_0, ...
```

### Paso 4: Separación odd/even
```python
# Armónicos impares: n = 1, 3, 5, 7, ...
# Armónicos pares: n = 2, 4, 6, 8, ...
# Calcular: A_odd = mean(amplitudes impares)
# Calcular: A_even = mean(amplitudes pares)
# Ratio = A_odd / A_even
```

### Paso 5: Análisis estadístico
```python
# t-test entre distribuciones odd vs even
# Bootstrap para intervalos de confianza
# Calcular p-value
```

---

## 6. CONTROLES DE CALIDAD

### Control 1: Ruido instrumental
- Verificar que el ratio NO aparece en segmentos sin señal
- Usar datos "off-source" como control

### Control 2: Consistencia entre detectores
- Analizar H1, L1, V1 independientemente
- El ratio debe ser consistente entre detectores

### Control 3: Independencia de masa
- Si es topológico, ratio debe ser similar para todas las masas
- Comparar GW150914 (62 M☉) vs GW170817 (2.7 M☉)

---

## 7. RESULTADOS ESPERADOS

### Si H₀ es correcta (GR estándar):
- Ratio ≈ 1 para todos los eventos
- Sin correlación con parámetros físicos
- Distribución de amplitudes simétrica

### Si H₁ es correcta (Klein):
- Ratio ≈ 22 consistente entre eventos
- Independiente de masa y distancia
- p < 0.05 en t-test

### Si H₂ es correcta (Klein fuerte):
- Ratio ≈ 40 como en análisis previo
- Evidencia de topología no-orientable

---

## 8. COMPROMISOS

### Nos comprometemos a:
1. **NO modificar** este protocolo después de ver los datos
2. **Reportar** el resultado sea cual sea (positivo o negativo)
3. **NO ajustar** parámetros para mejorar el resultado
4. **Publicar** tanto confirmación como refutación

### Si el resultado es negativo (ratio ≈ 1):
- Documentar como **refutación** de predicción Klein para LIGO
- Actualizar estado de la teoría honestamente
- Considerar que el modelo de análisis previo era circular

### Si el resultado es positivo (ratio > 15):
- Documentar como **evidencia observacional**
- Buscar verificación independiente
- Considerar publicación formal

---

## 9. REGISTRO TEMPORAL

| Fecha | Acción | Firma |
|-------|--------|-------|
| 2026-01-23 | Protocolo creado | Claude/Fausto |
| 2026-01-23 | Predicciones registradas | Pre-análisis |
| [PENDIENTE] | Análisis ejecutado | Post-datos |
| [PENDIENTE] | Resultados documentados | Final |

---

## 10. CÓDIGO A USAR

El código se escribirá en el archivo:
`VALIDACION_LIGO_REAL/01_analisis_strain_real.py`

Debe ser:
- Reproducible (semilla aleatoria fija)
- Documentado (cada paso explicado)
- Independiente del modelo Klein (análisis ciego)

---

*Protocolo congelado: 23 Enero 2026*
*NO MODIFICAR DESPUÉS DE ESTA FECHA*
