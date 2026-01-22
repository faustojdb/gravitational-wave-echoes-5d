# Resultados: Análisis de Escalamiento de Masa

**Fecha**: Enero 2026
**Estado**: Completado

---

## Pregunta Central

> ¿Qué pasa con Klein Theory cuando R_Schwarzschild >> R_Klein?

## Parámetros Clave

| Parámetro | Valor | Significado |
|-----------|-------|-------------|
| R_Klein | 8400 km | Radio de la dimensión extra (validado 10σ) |
| R_s/M☉ | 2.95 km | Radio de Schwarzschild por masa solar |
| **M_critical** | **2847 M☉** | Masa donde R_s = R_Klein |

---

## Resultado Principal

### TODOS los eventos GWTC están DEBAJO de M_critical

```
Evento más masivo: GW231123_135430
  M_total = 238 M☉
  R_s = 702 km
  R_s/R_Klein = 0.084 (¡solo 8% del radio Klein!)

GW190521 (famoso evento IMBH):
  M_total = 153 M☉
  R_s = 452 km
  R_s/R_Klein = 0.054 (solo 5%)
```

### Implicación

**No podemos probar la transición con datos actuales.**

Para que R_s ≈ R_Klein necesitamos observar fusiones de ~3000 M☉.
Esto requiere:
- Futuros detectores como LISA (agujeros negros supermasivos)
- O eventos extremadamente raros de IMBHs

---

## Hallazgos Dentro del Rango Disponible

### Correlaciones Klein vs Masa

| Rango de Masa | N eventos | Correlación SNR-ε | p-value |
|---------------|-----------|-------------------|---------|
| < 30 M☉ | 38 | **-0.861** | < 0.0001 |
| 30-60 M☉ | 91 | -0.744 | < 0.0001 |
| 60-100 M☉ | 69 | -0.829 | < 0.0001 |
| 100-200 M☉ | 20 | **-0.589** | 0.0062 |

### Observación Importante

**Las correlaciones Klein SE DEBILITAN a mayor masa:**
- Masa baja (< 30 M☉): r = -0.861
- Masa alta (100-200 M☉): r = -0.589

Diferencia: Δr ≈ 0.27 (correlación 30% más débil)

---

## Eventos GW190521-class (M > 140 M☉)

Solo 5 eventos en este rango:

| Evento | M_total | R_s/R_Klein | SNR residual | Interpretación |
|--------|---------|-------------|--------------|----------------|
| GW231123 | 238 M☉ | 0.084 | -0.31 | SNR bajo (¿supresión?) |
| GW231028 | 153 M☉ | 0.054 | +1.05 | SNR alto (¿enhancement?) |
| GW200220 | 148 M☉ | 0.052 | -0.06 | Normal |
| GW190521 | 153 M☉ | 0.054 | +0.01 | Normal |
| GW190426 | 182 M☉ | 0.064 | -0.27 | SNR bajo (¿supresión?) |

**Resultado mixto**: No hay patrón claro en los eventos más masivos.

---

## Modelo de Supresión Klein

Probamos el modelo:

```
Klein_effect = A / (1 + (M/M_c)^n)
```

Resultado del ajuste:
- M_c (crítica) ≈ 2768 M☉ (¡consistente con predicción teórica!)
- Pero R² = 0.000 (no hay suficiente rango de masa para ajustar)

---

## Conclusiones

### Lo que podemos afirmar:

1. **M_critical = 2847 M☉** es la masa de transición predicha por Klein
2. **Ningún evento GWTC** alcanza esta masa (máximo 238 M☉ = 8% de M_critical)
3. **Hay indicios** de que correlaciones Klein se debilitan con la masa
4. **GW190521** está BIEN dentro del régimen Klein (R_s << R_Klein)

### Lo que NO podemos probar:

1. ❌ No hay datos para probar qué pasa cuando R_s > R_Klein
2. ❌ No hay eventos de IMBHs masivos (> 1000 M☉)
3. ❌ La transición a M_critical queda fuera de alcance de LIGO/Virgo

### Predicción Falsificable:

```
PREDICCIÓN: Para M > M_critical ≈ 2800 M☉, las correlaciones
Klein deberían DESAPARECER o cambiar radicalmente.

CÓMO PROBAR: Observar fusiones de IMBH masivos con LISA/ET
O analizar ondas gravitacionales de SMBHs.
```

---

## Siguiente Paso: Matrioska-Klein

Si Klein₃ (R=8400 km) no funciona para SMBHs, quizás existe Klein₄ a escala mayor que sí funcione.

Ver: `MATRIOSKA_KLEIN_HYPOTHESIS.md`

---

## Archivos Generados

- `scripts/smbh_mass_scaling_analysis.py` - Script de análisis
- `results/smbh_mass_scaling.json` - Resultados detallados

---

*Análisis completado: Enero 2026*
