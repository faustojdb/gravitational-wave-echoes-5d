# Protocolo v2: veto de glitches a priori y tercer detector (Virgo)

Fijado el 9 de octubre de 2026 **antes** de correr el análisis v2 y sin mirar strain nuevo. Reemplaza al v1 (`PROTOCOLO.md`) sólo en lo que aquí se dice; todo lo demás (muestra, ventanas, PSD, blanqueo, estadístico, nula, criterio de éxito) es idéntico. El resultado v1 queda archivado en `resultados/` y no se modifica.

## Motivación (del reporte v1)

La distribución nula v1 estaba dominada por glitches en ventanas off-source de 4 eventos, lo que degradaba la sensibilidad del test sin cambiar su conclusión. El v1 también usó sólo H1 y L1.

## Cambios

1. **Detectores: H1, L1 y V1** (Virgo), strain público GWOSC a 4096 Hz. Un detector sin datos públicos o con huecos (NaN) en el segmento de 256 s se descarta para ese evento y se anota, como en v1.

2. **Veto A, por banderas de calidad de datos (a priori, público):** se usa la bandera `{det}_CBC_CAT2` de GWOSC (incluye CAT1). Una ventana, on-source u off-source, es válida sólo si **todos los segundos enteros que solapa** están activos en CBC_CAT2 de ese detector. Las banderas tienen granularidad de 1 s. Se eligió CAT2 porque es la categoría estándar de vetos por acoplamientos instrumentales conocidos que la colaboración aplica a búsquedas de binarias compactas; CAT3 se descartó por ser más agresiva y opcional.

3. **Veto B, por amplitud en el dominio del tiempo (a priori, simétrico):** sobre la serie blanqueada y filtrada (σ ≈ 1 por muestra), una ventana se veta si `max |x| > 6`. Bajo ruido gaussiano la probabilidad de superar 6σ en una ventana de 4 s (16384 muestras) es ≈ 3×10⁻⁵, así que el veto sólo actúa sobre transitorios no gaussianos. **Se aplica exactamente igual a la ventana on-source y a las off-source.** Justificación de que no sesga: las ventanas on-source empiezan 50 ms después de la fusión, cuando el ringdown de un remanente de hasta ~150 M☉ ya decayó más de e⁻⁵; una línea tardía de la amplitud que buscamos (z ~ 2 por bin) nunca produce 6σ en el dominio del tiempo.

4. **Reglas de exclusión, fijadas ahora:**
   - Si la ventana on-source de un detector está vetada (A o B), ese detector-evento se excluye de esa ventana y se reporta con el motivo.
   - Si tras el veto quedan menos de 20 ventanas de referencia o menos de 20 nulas para un detector-evento, ese detector-evento se excluye y se reporta.
   - Si un evento queda sin detectores en una ventana, se excluye del apilado de esa ventana y se reporta. El número de eventos apilados puede ser menor que 18 y se declara.

5. **Sin cambios:** mismas 18 fusiones (`resultados/muestra.json`), W1 = [t0+0.05, t0+1.05] s, W2 = [t0+1.05, t0+5.05] s, PSD de Welch mediana en [t0−124, t0−8] s, pasa-altos 20 Hz y bins 20–1800 Hz, `z = (P_on − mediana_ref)/MAD_ref`, división referencia/nula alternada, suma sobre detectores y eventos, 2000 réplicas nulas con la misma semilla (20261009), `p_corr = 2p`, éxito si `p_corr < 0.001`.

6. **Se reporta siempre:** número de ventanas vetadas por A y por B por detector-evento; comparación v1/v2 de la mediana y el percentil 99.9 de la nula (medida directa de la ganancia en sensibilidad); los mismos controles de normalización que en v1.

## Lo que este protocolo NO hace

No cambia el estadístico ni el criterio de éxito. No ajusta umbrales después de ver los datos: el 6σ y CAT2 quedan fijados aquí. No usa inyecciones ni datos simulados.

## Enmiendas

(ninguna)
