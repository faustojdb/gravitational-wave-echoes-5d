# Reporte v2: veto de glitches a priori y Virgo — búsqueda ciega de líneas tardías en GWTC-3

Fecha: 9 de octubre de 2026. Protocolo: `../PROTOCOLO_v2.md`, commiteado antes de que existiera ningún resultado (commit `88b5b20`). Script: `../busqueda_lineas_tardias_v2.py`. Sin enmiendas durante la corrida.

## Resultado confirmatorio (pre-registrado): NEGATIVO

| Ventana | Eventos apilados | Zmax observado | f del máximo | p (nula por el mismo pipeline) | p corregida (×2) | mediana nula | criterio |
|---|---|---|---|---|---|---|---|
| W1 = [t0+0.05, t0+1.05] s | 18 | 52.3 | 1619 Hz | 0.955 | 1.00 | 60.9 | p_corr < 0.001: **no** |
| W2 = [t0+1.05, t0+5.05] s | 18 | 48.4 | 1460 Hz | 0.682 | 1.00 | 51.7 | p_corr < 0.001: **no** |

Como en v1, el máximo observado está **por debajo de la mediana** de la distribución nula en las dos ventanas. No hay frecuencia en 20–1800 Hz con exceso común a los eventos después de la fusión.

## Qué cambió respecto de v1 y qué efecto tuvo

| | v1 (H1+L1, sin veto) | v2 (H1+L1+V1, veto a priori) |
|---|---|---|
| Detectores-evento usados en W1 | 32 | 44 |
| Detectores-evento usados en W2 | 32 | 43 |
| Eventos con Virgo | 0 | 11 |
| Nula W1: mediana / p95 / p99.9 de Zmax | 50 / 1020 / 590 022 | 61 / 359 / 2 614 |
| Nula W2: mediana / p95 / p99.9 de Zmax | 45 / 60 811 / 141 238 | 52 / 984 / 3 822 |
| Fracción de réplicas nulas con Zmax > 100 | 16 % (W1), 32 % (W2) | 18 % (W1), 13 % (W2) |

El umbral de detección (percentil 99.9 de la nula) bajó dos órdenes de magnitud. Pero la nula sigue teniendo una cola que no es gaussiana: el veto de amplitud en el dominio del tiempo (6σ) atrapa glitches anchos, no transitorios de **banda angosta** (líneas que suben y bajan de potencia), que producen z de decenas o cientos en un bin aislado. Eso es lo que hoy limita la sensibilidad. El umbral limitado sólo por ruido gaussiano sería Z ≈ 65 (ver exploratorio abajo).

## Contabilidad de vetos (todo reportado, nada descartado en silencio)

- **Veto A (banderas CBC_CAT2):** actuó en un solo detector-evento: L1 de GW200129, cuya ventana on-source está fuera de CAT2 en W1 y W2 (y 44 + 18 ventanas off-source vetadas). Es el evento con un glitch conocido en L1 sustraído por la colaboración. Se excluyó L1 y el evento siguió con H1 + V1.
- **Veto B (amplitud > 6σ, simétrico):** vetó entre 0 y 4 ventanas off-source por detector-evento (10 en V1 de GW200302), y **una** ventana on-source: H1 de GW200208 en W2. Ese detector-evento se excluyó de W2 y el evento siguió con L1 + V1.
- **Virgo:** sin datos públicos continuos en 7 de 18 eventos (NaN o ausente: GW191109, GW191129, GW191204, GW191222, GW200128, GW200225, GW200316). Usado en 11.
- Ningún evento quedó sin detectores; los 18 se apilaron en ambas ventanas.

## Controles

- **Normalización** (`fig_control_z.png`): on-source media 1.10 y desviación 2.31 en W1 (0.77 y 2.15 en W2), coincidente con el cuerpo de las nulas (1.08 y 0.74 de media). Con tres detectores la media sube proporcionalmente, como corresponde a una suma de z sesgados positivamente (la potencia es χ² y la normalización es por mediana/MAD).
- **Resultados individuales**: 36 tests (18 eventos × 2 ventanas). El mínimo es GW191215, W2: zmax = 26.6 a 502 Hz con p individual = 0/27 (< 0.037). Diagnóstico (sólo reporte): el exceso está **enteramente en V1** (z = 26.8; potencia on-source 17 veces la mediana off-source en ese bin), mientras que H1 y L1 en el mismo bin y la misma ventana tienen z = −0.65 y 0.38, y V1 en W1 tiene z = −0.58. Una señal astrofísica visible a 17× en Virgo tendría que ser mucho mayor en H1 y L1, que son más sensibles; su ausencia allí indica un transitorio instrumental de Virgo. Los otros 35 tests tienen p ≥ 0.07. Con 36 tests y resolución de p de 1/27, un valor así por azar es esperable.

## Análisis exploratorio post hoc (NO confirmatorio) — `../exploratorio_posthoc.py resultados_v2`

Recorte simétrico de z para medir sensibilidad. Ningún p de esta tabla es evidencia.

| Ventana | recorte | Zmax | f | p | mediana nula | p99.9 nula |
|---|---|---|---|---|---|---|
| W1 | ±5 | 43.4 | 1138 Hz | 0.84 | 45.9 | 61.1 |
| W1 | ±10 | 52.1 | 1619 Hz | 0.83 | 55.4 | 76.6 |
| W1 | ±20 | 52.3 | 1619 Hz | 0.94 | 58.2 | 99.3 |
| W2 | ±5 | 38.7 | 755 Hz | 0.72 | 40.2 | 52.0 |
| W2 | ±10 | 45.1 | 1460 Hz | 0.71 | 47.0 | 69.2 |
| W2 | ±20 | 48.4 | 1460 Hz | 0.56 | 49.1 | 81.1 |

Con cualquier recorte el observado sigue en la mediana de la nula. Conclusión negativa robusta.

## Interpretación en tres niveles

- **Dato:** 18 fusiones BBH de GWTC-3, tres detectores, veto a priori: no hay líneas tardías de frecuencia fija comunes a los eventos en 20–1800 Hz. Compatible con LVK (arXiv:2112.06861) y Miani et al. (arXiv:2302.12158).
- **Modelo:** desfavorecidas las variantes con modos masivos en banda con potencia relativa ≳ 2 MAD por evento y detector. Las de frecuencias fuera de banda no se ven afectadas.
- **Teorema:** sin cambios.

## Limitaciones declaradas

1. La cola de la nula sigue dominada por no estacionariedad de banda angosta. Un v3 pre-registrado debería vetar ventanas con z máximo anómalo por bin medido en datos **previos** al evento (no en las propias ventanas nulas), o usar estadísticos robustos por bin definidos de antemano.
2. Sin criterio formal de coincidencia entre detectores por bin; el caso GW191215/V1 muestra que haría falta uno, definido a priori.
3. Virgo disponible sólo en 11 de 18 eventos.
4. Sin inyecciones: no hay límite en amplitud de strain.
5. Ventanas hasta 5 s posfusión.

## Archivos

`resumen.json` (incluye la contabilidad completa de vetos en `vetos`), `apilado_W1.npz`, `apilado_W2.npz`, `fig_apilado.png`, `fig_control_z.png`, `exploratorio_posthoc.json`, `fig_exploratorio_posthoc.png`, `log.txt`.
