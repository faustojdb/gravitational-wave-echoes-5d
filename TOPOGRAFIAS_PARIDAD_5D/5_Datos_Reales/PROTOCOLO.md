# Protocolo de búsqueda de líneas tardías de frecuencia fija en strain real de LIGO

Fijado el 9 de octubre de 2026 **antes** de descargar o mirar los datos. No se modifica después de ver resultados; cualquier cambio posterior se registra como enmienda fechada al pie, con su motivo, y no reemplaza el análisis original.

## Hipótesis a contrastar (nivel teorema + modelo, ver `1_Teoria/03_prediccion_independiente_del_modelo.md`)

Si existe una dimensión extra con modos de Kaluza-Klein accesibles a la banda de los detectores, cada fusión debería ir seguida de oscilaciones tardías, casi monocromáticas, en frecuencias **fijas e iguales para todos los eventos** (no escalan con la masa del remanente), de decaimiento lento. La hipótesis nula es la Relatividad General en 4D: después del ringdown no hay líneas comunes entre eventos.

## Muestra (definida por el catálogo, no por nosotros)

- Catálogo: **GWTC-3-confident** (GWOSC, `eventapi/json/GWTC-3-confident/`), descargado el 9 oct 2026.
- Criterios, todos fijados a priori: (i) SNR de red ≥ 10; (ii) FAR ≤ 1 por año; (iii) ambas masas fuente > 3 M☉ (binarias de agujeros negros; se excluyen BNS y NSBH porque su posfusión tiene física propia).
- Detectores: H1 y L1 a 4096 Hz. Si un detector no tiene datos públicos en el segmento, el evento se analiza con el detector disponible y se anota; no se descarta el evento.
- Resultado: 18 eventos (lista en `resultados/muestra.json`, generada por el script a partir del catálogo con esos filtros).

## Datos

- Strain público de GWOSC, segmento `[t0 − 128 s, t0 + 128 s]` por evento y detector, con `t0` el GPS del catálogo.
- Preprocesado idéntico para on-source y off-source: PSD de Welch sobre `[t0 − 124, t0 − 8]` s (antes de la fusión), blanqueo con esa PSD, pasa-banda 20–1800 Hz. Sin filtros de líneas: las líneas instrumentales persistentes se controlan con los off-source, no suprimiéndolas.

## Ventanas

- **W1** (posfusión temprana): `[t0 + 0.05, t0 + 1.05]` s, resolución 1 Hz.
- **W2** (posfusión tardía): `[t0 + 1.05, t0 + 5.05]` s, resolución 0.25 Hz, re-agrupada a 1 Hz para comparar.
- Off-source: ventanas de la misma duración, no solapadas, dentro de `[t0 − 120, t0 − 8]` y `[t0 + 8, t0 + 120]` s. Son ≥ 40 por evento y detector.

## Estadístico

1. Para cada evento, detector y bin de frecuencia `f`: potencia blanqueada `P_on(f)` en la ventana on-source y la distribución `{P_off(f)}` de las off-source. Se define `z(f) = [P_on(f) − mediana_off(f)] / MAD_off(f)`. Esto normaliza por bin, de modo que una línea instrumental persistente (60 Hz y armónicos, modos violín, líneas de calibración) tiene `z ≈ 0`.
2. Por evento: `z_ev(f) = Σ_detectores z(f)` (coherencia en frecuencia entre detectores; no se exige fase por simplicidad y porque los modos masivos de distinta velocidad de grupo no la conservan).
3. Apilado entre eventos (la predicción es una frecuencia común): `Z(f) = Σ_eventos z_ev(f)`. Estadístico de prueba: `Z_max = max_f Z(f)` en 20–1800 Hz, por ventana.
4. **Distribución nula por el mismo pipeline**: se repite el apilado 2000 veces reemplazando la ventana on-source de cada evento por una off-source elegida al azar (con reposición) y se obtiene la distribución de `Z_max` bajo la nula, que ya incluye el efecto "look-elsewhere" sobre todos los bins.
5. `p = fracción de réplicas nulas con Z_max ≥ Z_max observado`. Se corrige por las dos ventanas (Bonferroni ×2).

## Criterio de éxito / fracaso, fijado ahora

- **Detección candidata**: `p_corr < 0.001` en W1 o W2. Entonces se reporta la frecuencia, se verifica que el bin tenga `z > 0` en la mayoría de los eventos (no dominado por uno solo) y se contrasta con la lista de líneas conocidas de O3 de GWOSC.
- **Resultado negativo**: en cualquier otro caso. Se reporta `Z_max`, su `p`, el percentil 95 de la nula y el `Z(f)` completo para que cualquiera lo revise. Un resultado negativo se escribe con el mismo detalle que uno positivo.

## Controles adicionales que se reportan siempre

- Histograma de `z` off-source vs. on-source para verificar que la normalización es correcta (debe ser ≈ 0 ± 1 fuera de la fusión).
- Resultado por evento individual (`max_f z_ev(f)` y su p individual contra sus propias off-source), para detectar si algún evento domina.
- Lo que ya publicó la colaboración: la búsqueda de ecos y el test de ringdown de "Tests of GR with GWTC-3" (arXiv:2112.06861) y los límites de Miani et al. (arXiv:2302.12158). Nuestro resultado debe ser compatible o explicar por qué no.

## Lo que este protocolo NO hace

- No asume una frecuencia, un modelo de brana ni un radio. No usa ninguna fórmula de trabajos previos del repositorio.
- No ajusta parámetros después de ver los datos.
- No usa datos simulados ni inyecciones como evidencia (sólo, si hiciera falta, para medir eficiencia, y se diría).

## Enmiendas

(ninguna)

**Enmienda 1 (9 oct 2026, antes de correr el análisis, por implementación):** para evitar que cada ventana off-source entre en su propia mediana/MAD, las ventanas off-source de cada evento y detector se dividen en dos mitades por orden temporal alternado: mitad "referencia" (define mediana y MAD por bin) y mitad "nula" (provee las réplicas del apilado). La ventana on-source y las ventanas nulas se normalizan ambas con la mitad de referencia, de modo que el tratamiento es idéntico. Las réplicas nulas usan el mismo índice temporal de ventana para H1 y L1, imitando la coincidencia on-source.
