# Reporte: búsqueda ciega de líneas tardías de frecuencia fija en strain real de LIGO (GWTC-3)

Fecha: 9 de octubre de 2026. Protocolo: `../PROTOCOLO.md` (fijado antes de mirar los datos, con tres enmiendas fechadas). Script: `../busqueda_lineas_tardias.py`. Datos: strain público de GWOSC, 4096 Hz, H1 y L1.

## Resultado confirmatorio (pre-registrado): NEGATIVO

| Ventana | Eventos | Zmax observado | f del máximo | p (nula por el mismo pipeline, incluye look-elsewhere) | p corregida (×2 ventanas) | mediana nula de Zmax | criterio |
|---|---|---|---|---|---|---|---|
| W1 = [t0+0.05, t0+1.05] s | 18 | 41.9 | 95 Hz | 0.980 | 1.00 | 50.1 | p_corr < 0.001: **no** |
| W2 = [t0+1.05, t0+5.05] s | 18 | 40.6 | 1011 Hz | 0.730 | 1.00 | 44.8 | p_corr < 0.001: **no** |

El máximo observado del estadístico apilado está **por debajo de la mediana** de la distribución nula en las dos ventanas. No hay ninguna frecuencia en 20–1800 Hz en la que los 18 eventos muestren exceso común de potencia después de la fusión.

## Muestra efectivamente analizada

18 eventos BBH de GWTC-3-confident con SNR ≥ 10, FAR ≤ 1/año y ambas masas > 3 M☉ (`muestra.json`). Detectores usados:

| Evento | Detectores | Motivo si falta uno |
|---|---|---|
| GW191216_213338 | H1 | L1 sin datos públicos en el segmento (evento H1+V1) |
| GW200112_155838 | L1 | H1 sin datos públicos (evento L1+V1) |
| GW200302_015811 | H1 | L1 sin datos públicos (evento de un detector) |
| GW200316_215756 | H1 | L1 con hueco (NaN) en el segmento de 256 s |
| otros 14 | H1 + L1 | — |

Resultados individuales (`resumen.json`): el p individual mínimo es 0.07 (GW200224, W1, 1097 Hz) y 0.14 (GW191129, W2, 1111 Hz); con 18 eventos × 2 ventanas, valores así son esperables bajo la nula.

## Controles

- **Normalización** (`fig_control_z.png`): el cuerpo de la distribución de z on-source (media 0.77, desviación 1.95 en W1; 0.58 y 1.86 en W2) coincide con el de las ventanas nulas en el rango ±12. Es decir, el espectro posfusión blanqueado es indistinguible del ruido fuera de los eventos.
- **Cola de la nula**: la desviación estándar de z en las nulas es 1279 (W1) y 484 (W2) frente a ≈ 2 on-source. La cola la producen glitches en ventanas off-source de 4 eventos (GW191109, GW191222, GW191230, GW200316, con desviaciones nulas de 186 a 5103). Un 16 % (W1) y 32 % (W2) de las réplicas nulas tienen Zmax > 100. Consecuencia: el test pre-registrado es **honesto pero poco sensible**, porque el umbral de detección queda fijado por los glitches (percentil 99.9 de la nula: 5.9×10⁵ en W1 y 1.4×10⁵ en W2).

## Análisis exploratorio post hoc (NO confirmatorio) — `../exploratorio_posthoc.py`

Escrito después de ver el resultado, para medir la sensibilidad del test si se limita la influencia de los glitches con un recorte simétrico de z (mismo recorte para on-source y nulas). Ningún p de esta tabla cuenta como evidencia.

| Ventana | recorte de z | Zmax | f | p | mediana nula | p99.9 nula (umbral) |
|---|---|---|---|---|---|---|
| W1 | ±5 | 38.4 | 1673 Hz | 0.70 | 39.8 | 51.2 |
| W1 | ±10 | 41.9 | 95 Hz | 0.94 | 46.7 | 67.3 |
| W1 | ±20 | 41.9 | 95 Hz | 0.98 | 48.7 | 77.2 |
| W2 | ±5 | 38.8 | 1682 Hz | 0.16 | 35.7 | 48.7 |
| W2 | ±10 | 40.2 | 1682 Hz | 0.61 | 41.3 | 63.6 |
| W2 | ±20 | 40.6 | 1011 Hz | 0.71 | 43.5 | 91.2 |

Con cualquier recorte el máximo observado sigue en la mediana de la nula. La conclusión negativa no depende de los glitches. Con recorte ±10 el umbral de detección (p99.9) es Z ≈ 65, lo que corresponde a un exceso medio de z ≈ 2 por evento y detector en un mismo bin de 1 Hz: una línea común con esa potencia relativa en los 18 eventos habría sido detectada. Traducir eso a amplitud de strain requiere inyecciones de eficiencia, que no se hicieron (y si se hacen, se reportarán como tales, no como evidencia).

## Interpretación en tres niveles (`CLAUDE.md`)

- **Dato:** en 18 fusiones de GWTC-3 no hay líneas tardías de frecuencia fija comunes a los eventos en 20–1800 Hz, dentro de la sensibilidad descrita. Compatible con la búsqueda de ecos negativa de LVK (arXiv:2112.06861) y con los límites de Miani et al. (arXiv:2302.12158).
- **Modelo:** cualquier variante de dimensión extra que predijera modos masivos excitados por la fusión con potencia relativa ≳ 2 MAD por evento en esta banda está desfavorecida. Modelos con frecuencias fuera de 20–1800 Hz (en particular toda compactificación plana permitida por los tests de laboratorio, con f₁ > 10¹² Hz) no quedan afectados por este análisis.
- **Teorema:** nada de lo anterior toca el resultado matemático de selección de paridad por lado en S¹/(Z₂×Z₂′); sólo su realización observable.

## Limitaciones declaradas

1. Sólo H1 y L1; no se usó Virgo.
2. Dos ventanas fijas (hasta 5 s posfusión). Modos de decaimiento muy lento con amplitud muy baja requerirían integraciones más largas y un tratamiento de líneas instrumentales distinto.
3. Sin inyecciones: no hay límite superior en amplitud de strain, sólo en potencia relativa.
4. La coherencia entre detectores se exigió sólo en frecuencia, no en fase.
5. Glitches en off-source degradan la sensibilidad del test pre-registrado; una versión futura debería incorporar un veto de glitches definido a priori (por ejemplo, con las banderas de calidad de datos de GWOSC), no post hoc.

## Archivos

`resumen.json` (todos los números), `apilado_W1.npz`, `apilado_W2.npz` (Z(f), z por evento, réplicas nulas), `fig_apilado.png`, `fig_control_z.png`, `exploratorio_posthoc.json`, `fig_exploratorio_posthoc.png`, `log.txt`, `muestra.json`, catálogo GWOSC descargado.
