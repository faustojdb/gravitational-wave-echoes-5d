# Auditoría del trabajo previo del repositorio: superficies, radios, frecuencias y por qué fallaron

Fecha: 9 de octubre de 2026. Alcance: todas las carpetas del repositorio salvo `TOPOGRAFIAS_PARIDAD_5D/`. Propósito: inventariar lo que se probó y establecer, con citas a archivo y línea, por qué no se sostiene. Este documento **lee** el trabajo previo como objeto de auditoría; no lo usa como insumo para ninguna afirmación nueva (`CLAUDE.md`). Toda afirmación de abajo fue verificada en esta sesión abriendo el archivo citado; donde una verificación la hizo un agente de búsqueda y no se re-leyó a mano, se indica "(inventario)".

## 0. Resumen en una página

1. **Ningún resultado "observacional" del trabajo previo proviene de strain real de LIGO analizado con un estadístico definido y una nula.** Los pipelines que reportan significancias generan la población, las detecciones o los tiempos de eco con `np.random`, o construyen plantillas con la señal buscada ya puesta. No hay ningún control off-source, time-slide, permutación ni inyección en todo el repositorio.
2. **El mecanismo "modos pares prohibidos, impares permitidos" nunca se deriva.** El único intento de expansión de modos escrito en el paper previo obtiene **n par** y a renglón seguido afirma que sobreviven los impares. En el código la supresión es un factor numérico constante, calibrado para que la razón salga 40:1.
3. **Las significancias altas son artefactos de la combinación.** 9.25σ = √Σσᵢ² sobre 65 valores individuales de 0.5 a 2σ, con eventos simulados en la muestra. 8.53σ = √(0.871² + 6² + 6²), donde 0.871 es un coeficiente de correlación (no una σ) y los 6.00 son **topes** escritos en el código (`sigma_level = 6.0 # Cap en 6σ`). 2.80σ ± 0.28σ proviene de una población cuyas detecciones y tiempos se sortean al azar.
4. **Los radios son ajustes, no derivaciones**, y los propios documentos del repositorio lo admiten: 8400 km surge de un parámetro γ_GW "calibrado empíricamente" tras una primera estimación errada por 15 órdenes de magnitud; 419.3 km surge de λ_Compton × exp(137 × 0.336), con 0.336 elegido para que el exponencial dé ~10²⁰.
5. **Los números son físicamente inviables aunque fueran reales.** Una dimensión extra plana de 419 a 8400 km está excluida por 10¹⁰–10¹¹ respecto de los tests de la ley 1/r² y haría 5D la gravedad en el Sistema Solar. La "frecuencia universal" 5.68 Hz (y 6.65, 4.19, 2.84, 8.2 Hz) está por debajo del muro sísmico de LIGO: no es medible en el strain público. La ley de retardo τ ∝ M^(−0.826) decrece con la masa, al revés de todo mecanismo publicado (modos KK: independiente de M; ecos de objetos compactos: ∝ M).
6. **El repositorio ya contiene su propia refutación parcial**: `ANALISIS_CRITICO_BANDERAS_ROJAS.md` (circularidad de 8400 km), `ANÁLISIS_CRÍTICO_INCONSISTENCIAS.md` (419 km), `KLEIN_COMPREHENSIVE_ASSESSMENT.md` (tests termodinámicos y electromagnéticos: media 1.12σ, "FALSIFIED"), `CRITICAL_ANALYSIS_SUMMARY.md` (algoritmo subumbral con salida constante; validación con relatividad numérica 0/4). Lo que falta es que esas autocríticas se propaguen a los README y a los papers, que siguen anunciando "breakthroughs".

## 1. Superficies probadas y cronología de radios

Cronología según los propios documentos y el historial git (primera publicación 28-may-2025; v2.0 30-may; v3 4-jun; multi-topología 5-jun; reorganización 23-jul; 419 km 27-ago). Todas las filas fueron verificadas abriendo al menos uno de los archivos citados.

| Fecha | Superficie | Radio | Cómo se obtuvo según el texto | Predicción | Qué pasó después |
|---|---|---|---|---|---|
| may-2025 (v1) | Botella de Klein | 1000 km | Asumido; `c_eff = 2.67e7` "calculado para dar ω₀ = 42" (`OLD/analysis/klein_simulation.py:27`) | τ = 0.1496 s, ω₀ = 42 rad/s, sólo modos impares | Reemplazado en v2.0 |
| may-2025 (v2.0) | Botella de Klein | 1751.173 km, "exacto" | Invertido del τ observado: R = τ·c_eff/4 con una velocidad efectiva c_eff = c/6.4 sin justificación (`OLD/papers/DiBacco_2024_Klein_Theory_v2_Complete_English.md:146`) | τ = 0.1496 ± 0.0021 s **independiente de la masa** (:253); 3.1σ con 5/10 eventos de GWTC-1 y test binomial contra tasa nula asumida 0.1 | El mismo paper admite "Ω_DM >> 1, clearly incorrect" (:300). Abandonado en v3 |
| jun-2025 (v3) | Botella de Klein | R_eff = 8400 ± 150 km (prior 1000–50000 km) | "Ajuste poblacional" sobre 65 eventos cuyas detecciones y tiempos se sortean (§4). El JSON de salida del script de optimización no contiene R | τ = 2.574·M^(−0.826) + 0.273 s, **ahora dependiente de la masa**; f₀ = 6.65 Hz | El mismo paper da en sus conclusiones R₅ = (1.2 ± 0.3)×10⁻⁴ m (`Klein_Echoes_Paper_Enhanced.tex:1317`): sub-milimétrico y 8400 km en el mismo documento, sin comentario |
| jun-2025 (multi-topología) | Klein, ℝP², Möbius, toro torcido, orientifold | Tres juegos de radios incompatibles (p. ej. Klein 7175 / 22541 / 25502 km) según el "factor geométrico" elegido; toro torcido fijado en 8400 km | f₀ por topología escrito a mano (6.65 / 4.19 / 8.2 / 5.68 / 6.8 Hz); mismo exponente −0.826 para las cinco | `conservative_report_20250605_025849.md`: con factores = 1 **las cinco topologías dan 0.00σ**, y el informe escribe "0.00σ represents moderate evidence". El factor 7.997 del toro fue declarado "ad hoc" y corregido a 1.061. **5.68 Hz aparece por primera vez como f₀ del toro torcido**, = c/(2π·8400 km) (`Theory/twisted_torus.py:359`), no de la botella de Klein |
| jun–ago 2025 (Elastic Paradigm, Klein Field Theory) | Botella de Klein | 8400 ± 100 km | Tres relatos distintos: balance (α/β)^(1/3); inversión de f₀ = c/(2πR) = 5.68 Hz; "γ_GW ajustada para dar R ~ 8400 km" (`macroscopic_scale_theoretical_justification.md:239`) | f₀ = 5.68 Hz "universal", ε_max = 0.65, razón impar/par 40:1 | `KLEIN_THEORY_UNIFIED_FRAMEWORK.md:260,348` lo etiqueta "empírico, sin derivación fundamental" |
| jul-2025 | "Átomo Klein" galáctico | 8.4 kpc | Confusión de unidades: 8400 km leído como 8.4 kpc, luego ajustado a curvas SPARC | núcleo universal de materia oscura | `CRITICAL_UNITS_CORRECTION_GUIDE.md:23`: "off by a factor of ~31,000,000". El README de esa carpeta sigue usando 8.4 kpc |
| jul–ago 2025 (teoria_refinada, Doppler, EM, termo) | Botella de Klein | código: `R_5D = 8.4e6` **km** (8.4 millones de km); texto: 8400 km | copiado "de framework" | γ(L) ∝ (L/R)^α | Sin corrección registrada |
| ago-2025 (FUNDAMENTAL_RADIUS) | Botella de Klein | 419.3 ± 0.1 km (alternativas 8187, 38323, 2606, 1853 km) | λ_Compton(e⁻) × exp(137 × 0.336); "primeros principios" | f = 113.79 Hz "óptima para LIGO"; 13.9σ en 219 eventos por `snr_klein = snr × factor_resonancia` | El propio README la declara "methodologically invalid… arbitrary SNR multiplication" (:15, :88-90) y a la vez "Discovery confirmed (13.9σ)" (:132, :184). `KLEIN_MODEL_CORRECTED.md:72`: "γ ≈ 0.336 surge del ajuste" |
| ago-2025 (ciego) | T³, K², ℝP², género alto | T³ 30000 km; K² 8400 km | Retro-calculado desde f₀ = 5.68 Hz con c/(2πf₀) en una línea y c/(4πR) en otra del mismo archivo | f₀ = 5.68 Hz | `EVALUACION_REDESCUBRIMIENTO_INDEPENDIENTE.md:190-193,303`: "completamente ciego: NO… no resuelve circularidad" |
| ago-2025 (independiente) | Esfera S² | R libre | Teoría pura | sólo razones f_l ∝ √(l(l+1)) | `DERIVACION_R_FUNDAMENTAL.md:497`: "NINGÚN mecanismo fundamental puede fijar R" |
| ago-2025 (estabilización) | 6D warped, superconductividad, retrocausal | 8400 km, 0, 1 km, 10⁻⁴³ m | intentos numéricos | radio estabilizado | `SINTESIS_FINAL_INVESTIGACION_REVOLUCIONARIA.md:124,225`: "legitimidad: CERO… Ningún mecanismo derivó R_Klein legítimamente" |

Lo verificado a mano sobre el mecanismo de selección de modos:

| Afirmación del trabajo previo | Dónde | Qué dice realmente el texto o el código |
|---|---|---|
| "La identificación (φ,χ)~(φ+π,−χ) fuerza ψ(φ+π) = −ψ(φ) y elimina los modos pares" | `KLEIN FIELD THEORY/1_Theory/ioplatexguidelines/Klein_Echoes_Paper_Enhanced.tex:91-94` | Afirmación sin derivación. En la línea 235 la misma identificación se escribe con signo **más**. |
| Expansión de modos ψ = e^{inφ+imχ} | mismo archivo, líneas 251-261 | Obtiene "m = 0 y e^{inπ} = 1, por lo tanto **n = 2k (sólo enteros pares)**", y en la frase siguiente: "el análisis completo muestra que sobreviven los impares". El análisis completo no está. |
| Condiciones g(y+2πR)=g(y), g(−y)=g(y), ∮ε dy = 0 como "no orientabilidad" | `Klein Elastic Paradigm/KLEIN_ELASTIC_PARADIGM_COMPLETE_UNIFIED_PAPER.tex:130-132` y copias | g(−y)=g(y) es una **paridad Z₂** (orbifold S¹/Z₂), no no-orientabilidad; una botella de Klein no tiene puntos fijos y por lo tanto no admite esa condición (Nilse 2006, §3.2). La condición ∮ε dy = 0 elimina el modo cero, no los pares. |
| "Klein factor = sin(πn) = 0 para n par; cos(πn/2) ≠ 0 para n impar" | mismo .tex, 412-428 | sin(πn) = 0 para **todo** entero n, y cos(πn/2) = 0 para todo n **impar**. Las dos fórmulas dicen lo contrario de lo que el texto les atribuye. |
| Razón impar/par ≈ 40 "observada" | `Klein Elastic Paradigm/3_Validation/harmonic_analysis_klein_breathing_modes.py:131-134` | `suppression_factor = 0.055  # Calibración final para ratio 40:1 ± 5`. Los modos pares se multiplican por esa constante; los impares se generan con una fórmula más ruido aleatorio. Luego se hace un t-test sobre el factor que se acaba de aplicar. |
| Razón 40.6 en PTA | `EMPIRICAL_KLEIN_STUDIES/2_PTA_Analysis/pta_klein_analysis.py:45` | `'ratio_odd_even': 40.6` escrito a mano. |
| "Paridad" en la ecuación maestra refinada | `teoria_refinada/scripts/klein_master_equation_refinada.py:101-126` | La paridad la fija un **umbral de energía** (E/10 > 0.30 ⇒ par, < 0.15 ⇒ impar), no la topología. |

Lo que sí es cierto, y ya está en `1_Teoria/`: la selección par/impar **dependiente del lado** existe, pero en el orbifold S¹/(Z₂×Z₂′), no en la botella de Klein, y la botella de Klein da selección por paridad del campo, sin "lados".

## 2. Radios

| R | Dónde se propone | Cómo se obtiene según el propio repositorio | Estado según el propio repositorio |
|---|---|---|---|
| 8400 km (R_eff, R_Klein, R_K) | paper v3, Klein Field Theory, Klein Elastic Paradigm; >100 menciones | Parámetro óptimo del ajuste poblacional de v3 (sobre población simulada, ver §4); luego "derivado" en `ANALISIS_CRITICO_ESCALA_MACROSCOPICA/DERIVACION_RIGUROSA_ESCALA_MACROSCOPICA.md` | `ANALISIS_CRITICO_BANDERAS_ROJAS.md`: "γ_GW ajustado empíricamente para dar R_K = 8400 km — CIRCULAR"; "primera estimación da R ~ 10²³ m"; "8400 km no aparece naturalmente en ninguna física fundamental". |
| 419.3 km | `FUNDAMENTAL_RADIUS_INVESTIGATION/` | λ_Compton(e⁻) × exp(137 × 0.336) | `6_Documentation/ANÁLISIS_CRÍTICO_INCONSISTENCIAS.md`: "0.336 parece ser un ajuste numérico para que exp(137×0.336) ≈ 10²⁰"; inconsistencia dimensional en la presentación. El README cita un archivo `VALIDACION_CRITICA_METODOLOGIA.md` que **no existe** en el repositorio. |
| 1751.173 km | v2.0 (`README_v2.0.md`, `OLD/papers/`) | R = τ·c_eff/4 con c_eff = c/6.4 | El propio paper v2 admite Ω_DM >> 1 "clearly incorrect"; abandonado en v3 |
| 8187 km | `FUNDAMENTAL_RADIUS_INVESTIGATION/5_Code/klein_dynamic_corrected.py` | radio "estático" alternativo | — |

Confrontación física: ver `cotas_fisicas.md`. Todos están entre 1.1×10¹⁰ y 2.2×10¹¹ veces por encima de la cota de Lee et al. 2020 para una dimensión plana, y entre 0.07 y 1.3 radios terrestres: la gravedad sería 5D dentro de la órbita lunar.

## 3. Frecuencias y retardos

| Valor | Dónde | Observación |
|---|---|---|
| f₀ = 5.68 Hz (≈ 420 menciones) | casi todas las carpetas | = c/(2πR) con R = 8400 km. **Por debajo de ~10 Hz LIGO no tiene sensibilidad**: el strain público está dominado por ruido sísmico y los análisis lo filtran. Ninguna "frecuencia universal" a 5.68 Hz es medible en esos datos. |
| f₀ = c/(4πR) | 16 menciones, incluida la "redescubierta a ciegas" | Con R = 8400 km da 2.84 Hz, no 5.68 Hz. La relación y el radio que el documento ciego dice haber redescubierto son aritméticamente incompatibles entre sí (factor 2). |
| f₀ = 6.65 Hz | paper v3 y multi-topología | Distinto de 5.68 Hz sin explicación; también fuera de banda. Además, el informe de verificación armónica (`Results/harmonic_verification_report_20250605_041601.md`) encuentra sólo n = 1 ("11.91σ", 5/20 eventos) y **0.00σ para n = 3, 5, 7, 9**: la "estructura de armónicos impares" nunca se observó, ni siquiera en la propia simulación. |
| f₀ = 6.68 Hz, ω₀ = 42 rad/s | v2.0 | Tercera versión de la misma frecuencia. |
| τ = 0.1496 ± 0.0021 s, independiente de M | v2.0 | Contradice frontalmente la ley dependiente de M de v3 un mes después; el repositorio no comenta el cambio. |
| τ predicho 176 ms vs medido 64–112 ms | `teoria_refinada/resultados/ligo/RESUMEN_EJECUTIVO_LIGO.md:31-32` | Desviación admitida en el propio resumen. |
| 113.79 Hz, 27.25 Hz | R = 419.3 km, 1751 km | En banda, pero el radio está excluido (§2). |
| τ = 2.574·M^(−0.826) + 0.273 s | paper v3 y multi-topología | Ajuste sobre tiempos de eco **simulados** (`expand_to_all_events.py:211`: `measured_tau = predictions['tau_echo'] + np.random.normal(0, 0.005)`). Decrece con M; ningún mecanismo publicado lo hace. Las otras cuatro topologías del paper multi-topología usan **el mismo exponente −0.826** con coeficientes distintos, lo que confirma que es un parámetro de ajuste compartido, no una predicción de cada geometría. |

## 4. Pipelines de datos y estadística

### 4.1 Qué datos reales se tocaron

- **Strain real**: sólo en `FUNDAMENTAL_RADIUS_INVESTIGATION/` (descargado a una ruta externa `/mnt/d/...`, no incluida en el repositorio) y analizado con un estadístico propio ("advantage" = razón de factores de amplificación del modelo, umbral 1.05) sobre 10 archivos; la media fue 1.017 y se reportó como "16.07σ" mediante un t-test de una muestra. No hay nula ni control.
- **Catálogo real (GWTC-3, 35 eventos, CSV de GWOSC)**: `teoria_refinada/`, `DOPPLER_KLEIN_EXT/`. Se correlaciona la energía radiada del catálogo con la deformación **calculada por el propio modelo** a partir de esa energía (r = 0.871). Es una correlación de una función con su argumento.
- **Ningún script del repositorio llama a `gwosc`, `fetch_open_data`, `pycbc` ni implementa un matched filter** (inventario). `expand_to_all_events.py` importa `TimeSeries` de gwpy y no lo usa.

### 4.2 De dónde salen las significancias publicadas

| Cifra | Archivo | Mecanismo real |
|---|---|---|
| 2.80σ ± 0.28σ, 4.24σ máx., "100 experimentos aleatorios" (v3) | `OLD/v3/Code_Essential/Population_Analysis/expand_to_all_events.py:203-212`; `Random_Experiments/script2_random_experiments.py:124-150` | Comentario literal: "En implementación real, aquí iría el análisis de strain". Detección: `if np.random.random() < detection_prob`; tiempo medido = predicho + N(0, 5 ms). Si falta el JSON, `generate_synthetic_population()` con `significance = 2.0 + np.random.exponential(1.0)` (media 3σ por construcción). |
| 9.25σ, "discovery evidence" (multi-topología) | `.../Comprehensive_Multi_Topology_Analysis_9p25_Sigma_Discovery.pdf.md:312-333` | σ_comb = √Σσᵢ² sobre 56 "detecciones" con σᵢ entre 0.53 y 2.08. Esa fórmula convierte ruido en "descubrimiento": 56 valores de ~1.2σ dan √(56·1.5) ≈ 9.2 aunque no haya señal. La lista de "detecciones notables" incluye **GW_sim_17**, un evento simulado. |
| 8.53σ "Fisher combinado" (teoria_refinada) | `README.md`; `teoria_refinada/scripts/pta/pta_analysis_refinado.py:298`, `cmb/cmb_analysis_refinado.py:264`, `em_marginal_analysis.py:178,246` | √(0.871² + 6.00² + 6.00²). El 0.871 es un coeficiente de correlación de Pearson, no una significancia. Los 6.00 son `sigma_level = 6.0  # Cap en 6σ`: un tope fijo en el código, no un resultado. El PTA da **1.06σ** (Δχ² = 2.48, p = 0.29) en `resultados/pta/RESUMEN_EJECUTIVO_PTA.md:19-23`; con ese valor el propio `RESUMEN_FINAL_REFINAMIENTO_KLEIN_THEORY.md:95` obtiene 6.15σ, no 8.53σ, y aun así lo llama "VALIDADA". El mismo documento (:5, :161) reconoce que antes del "refinamiento" el combinado era ~1.9σ y que los parámetros γ(L) y el signo par/impar se agregaron después para subirlo. |
| 13.9σ (t = 13.9, p = 3×10⁻³²), 219 eventos | `FUNDAMENTAL_RADIUS_INVESTIGATION/2_Analysis/prepare_219_events_analysis.py:128-156` | `snr_klein = snr × (1.2 + 1.8·resonancia)`: se multiplica el SNR del catálogo por un factor del modelo y se testea que el producto sea mayor que el SNR original. Declarado inválido por el propio README de la carpeta. |
| 10.00σ, p < 10⁻³⁰⁰ (Doppler, 405 eventos subumbral) | `DOPPLER_KLEIN_EXT/RESUMEN_FINAL_ANALISIS_KLEIN_DOPPLER.md:5-15` | Combinación de Fisher de 8 correlaciones, una de ellas r = 1.000 entre energía y deformación (la deformación se calcula a partir de la energía). Eventos con GPS, SNR, masas y velocidades generados al azar (`integrated_final_klein_doppler.py:255-342`). |
| log₁₀ B = 345, "115 eventos" | `KLEIN_FIELD_THEORY_COMPLETE_PAPER.md:592,694` | Los armónicos están marcados "(simulado)" en `comprehensive_115_events_analysis.md:440`. |
| p < 10⁻¹⁹⁸, "0 violaciones en 2357 eventos" (subumbral) | `Klein Subthreshold Theory/` | `klein_subthreshold_analyzer.py:314-327`: "Mock strain data generation", ruido gaussiano con un eco inyectado a 5.68 Hz. El propio `CRITICAL_ANALYSIS_SUMMARY.md` reconoce que el algoritmo devuelve ε_max = 0.010 constante para cualquier entrada y que la validación con relatividad numérica dio 0/4 y 0 % de detección de f₀. |
| ratio 40.6 ± 0.6, t = 19.97, p = 8×10⁻⁸² (armónicos, "113 eventos") | `harmonic_analysis_klein_breathing_modes.py`; `Informe_Analisis_Armonico_Final.md:73-74` | 9 nombres reales + 104 eventos generados ("Eventos sintéticos O3a/O3b", según el propio informe). Factor 0.055 aplicado a mano (§1). |
| S/N a 5.68 Hz en "45 eventos LIGO" | `KLEIN FIELD THEORY/5_Code/real_ligo_klein_analysis.py:181-199` | Construye las formas de onda con una modulación a `self.f0_klein` incluida y luego mide el pico de FFT a esa frecuencia. No lee ningún dato. |
| "Null tests: random phase stacking yields S/N ≈ 1" | `KLEIN FIELD THEORY/KLEIN_FIELD_THEORY_COMPLETE_PAPER.md:651` | No hay código que lo implemente (inventario). |

### 4.3 Controles

Ningún off-source, time-slide, permutación, inyección-recuperación ni blind analysis en todo el repositorio. La única "nula" es un 5 % de falsos positivos **asumido** en un test binomial (`expand_to_all_events.py:331`).

## 5. Por qué falló: diagnóstico en tres niveles

- **Nivel teorema.** El mecanismo topológico atribuido a la botella de Klein no existe tal como se enunció: la condición usada es una paridad de orbifold, la expansión escrita da el resultado opuesto, y las fórmulas trigonométricas citadas son falsas para los n que se pretende. La parte correcta de la intuición (selección par/impar por lado) requiere un intervalo con dos extremos inequivalentes, que es otra topografía.
- **Nivel modelo.** Los radios se fijaron para reproducir una escala de tiempo (~0.18–0.3 s) y luego se "derivaron" hacia atrás; los documentos críticos internos lo reconocen. Los radios resultantes violan la ley 1/r² por diez órdenes de magnitud y las frecuencias asociadas caen fuera de la banda del instrumento.
- **Nivel dato.** No hubo dato. Las poblaciones, detecciones, tiempos, plantillas y amplitudes relativas fueron generadas por el código; las significancias combinadas usan fórmulas inválidas sobre esas salidas. Cuando se intentó cruzar con algo externo (relatividad numérica, Monte Carlo propio, tests termodinámicos y electromagnéticos), falló, y eso quedó escrito en el repositorio.

## 6. Qué se rescata

- Los dos scripts de descarga de GWOSC (`download_using_gwosc_api.py`, `download_ascii_from_csv.py`) y la lista de 219 eventos del catálogo son reutilizables previa lectura; en esta carpeta ya se usó `gwpy.fetch_open_data` directamente, que es más simple.
- Los documentos autocríticos (`ANALISIS_CRITICO_BANDERAS_ROJAS.md`, `ANÁLISIS_CRÍTICO_INCONSISTENCIAS.md`, `KLEIN_COMPREHENSIVE_ASSESSMENT.md`, `CRITICAL_ANALYSIS_SUMMARY.md`, `NEGATIVE_RESULTS_ANALYSIS.md`) son el mejor material del trabajo previo y deberían enlazarse desde el README raíz, que hoy los contradice.
- La pregunta de fondo (¿qué topografía filtra paridad por lado?) tenía respuesta en la literatura de 2001 y ya está documentada en `1_Teoria/`.

## 7. Recomendaciones concretas sobre el repositorio

1. Marcar en el README raíz que las significancias listadas (2.80σ, 4.24σ, 8.53σ, 9.25σ, 13.9σ, 16.07σ, p<10⁻¹⁹⁸) provienen de datos simulados o de combinaciones inválidas, con enlace a este documento.
2. Retirar o renombrar los archivos cuyo nombre dice "real_ligo" o "real_data" pero no leen datos.
3. No volver a usar √Σσᵢ² ni topes de σ; toda significancia debe salir de una nula construida con el mismo pipeline, como en `5_Datos_Reales/`.
4. Conservar las carpetas previas como registro histórico, sin borrarlas, con una nota de estado al inicio de cada README.
