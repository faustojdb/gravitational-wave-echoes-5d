# TOPOGRAFIAS_PARIDAD_5D — ¿Qué forma de la 5ª dimensión anula los modos pares de un lado y los impares del otro?

Estudio independiente, iniciado el 9 de octubre de 2026, dentro del repositorio `gravitational-wave-echoes-5d` (se reutilizan sus herramientas de descarga/análisis de LIGO, no sus conclusiones).

## Hipótesis que se estudia

Una fusión de agujeros negros o una supernova emite ondas gravitacionales que también se propagan en una quinta dimensión. La propuesta es que la **topografía** de esa dimensión actúa como un filtro: cuando la onda regresa a nuestro lado un conjunto de modos (par o impar) queda anulado, y cuando va hacia el otro lado se anula el conjunto contrario. Analogía: una onda de agua vive sobre la superficie, no debajo del agua. Preguntas: ¿qué topografías pueden hacer eso? ¿qué características necesitan? ¿existen en la literatura seria?

## Respuesta en tres líneas

1. La selección par/impar **dependiente del lado** exige dos paredes **inequivalentes**: el orbifold $S^1/(Z_2\times Z_2')$ (intervalo con fase de Scherk–Schwarz). En él los modos impares vienen en dos familias espejo, una visible sólo desde nuestra pared y otra sólo desde la pared sombra; los pares se ven desde ambas.
2. Topografías sin paredes (círculo, **botella de Klein**, $RP^2$, Möbius) filtran por paridad **del campo**, no **del lado**: no tienen "lados".
3. Esa topografía existe y está publicada (Kawamura 2001; Barbieri–Hall–Nomura 2001; Nilse 2006). **Con paredes puramente dimensionales y geometría plana el efecto no es observable** (radio permitido < 39 μm ⇒ f₁ > 10¹² Hz). Sólo entra en la banda de LIGO si se agrega un supuesto físico adicional: warping sostenido por una brana con tensión (Randall–Sundrum, cuerda negra de Seahra–Clarkson–Maartens 2005), que fija $f_1\gtrsim460\,(30M_\odot/M)$ Hz. El cálculo de ondas gravitacionales en ese orbifold warped no existe en la literatura.

4. **Resultado sobre datos reales (9 oct 2026): negativo, en dos versiones pre-registradas.** Búsqueda ciega de líneas tardías de frecuencia fija en 18 fusiones BBH de GWTC-3 (strain GWOSC, nula por el mismo pipeline). v1 (H1+L1): p = 0.98 y 0.73. v2 (H1+L1+V1, veto de glitches a priori con banderas CBC_CAT2 y umbral simétrico de 6σ): p = 0.95 y 0.68. En ambas el máximo observado está por debajo de la mediana de la nula. Detalle en `5_Datos_Reales/resultados/REPORTE.md` y `5_Datos_Reales/resultados_v2/REPORTE.md`.

**Niveles de afirmación (ver CLAUDE.md):** (a) teorema: selección de paridad por lado en $S^1/(Z_2\times Z_2')$; (b) supuesto de modelo: warping con brana física; (c) dato: cotas publicadas de LVK y de laboratorio. Nada de esta carpeta usa datos sintéticos como evidencia; el análisis con strain real está en `5_Datos_Reales/`.

## Estructura

```
TOPOGRAFIAS_PARIDAD_5D/
├── README.md                                   ← este archivo
├── 1_Teoria/
│   ├── 01_criterio_de_seleccion_por_paridad.md ← formalismo KK, paridad ⇔ Neumann/Dirichlet, criterio de dos paredes
│   ├── 02_catalogo_topografias_candidatas.md   ← tabla de 11 topografías, características requeridas, ¿existen?
│   ├── 03_prediccion_independiente_del_modelo.md ← lo que TODAS las variantes predicen en común
│   └── 04_modelo_elastico.md                   ← derivación pura: rigidez, pretensión, rotura, permeabilidad, escalas (sin parámetros libres)
├── 2_Bibliografia/
│   └── bibliografia_anotada.md                 ← 36 referencias; ✅ = verificada en esta sesión, ⚠️ = de memoria
├── 3_Codigo/
│   ├── modos_paridad_topografias.py            ← espectros y funciones de modo por topografía, simulación 1+1, RS, cuerda negra
│   └── numeros_modelo_elastico.py              ← todos los números citados en 04_modelo_elastico.md
├── 4_Resultados/
│   ├── CONCLUSIONES.md                         ← síntesis en tres niveles (teorema / modelo / dato), próximos pasos
│   ├── tabla_resumen.md                        ← tablas generadas por el código
│   ├── resumen_numerico.json
│   └── figuras/fig1 … fig7
├── 6_Auditoria_trabajo_previo/
│   ├── AUDITORIA.md                            ← inventario con archivo:línea de superficies, radios, frecuencias, significancias y causas de fallo
│   └── cotas_fisicas.md
└── 5_Datos_Reales/
    ├── PROTOCOLO.md                            ← protocolo fijado ANTES de mirar los datos
    ├── busqueda_lineas_tardias.py              ← descarga strain de GWOSC y busca líneas tardías (con controles)
    ├── exploratorio_posthoc.py                 ← sensibilidad con recorte de glitches (post hoc, NO confirmatorio)
    ├── resultados/REPORTE.md                   ← v1 (H1+L1): negativo; tablas, figuras, limitaciones
    ├── PROTOCOLO_v2.md                         ← v2 fijado antes de correr: veto a priori (CAT2 + 6σ simétrico) y Virgo
    ├── busqueda_lineas_tardias_v2.py
    └── resultados_v2/REPORTE.md                ← v2 (H1+L1+V1): negativo; comparación de sensibilidad v1/v2
```

## Reproducir

```bash
pip install numpy scipy matplotlib
cd TOPOGRAFIAS_PARIDAD_5D/3_Codigo
python3 modos_paridad_topografias.py          # ~1 min; escribe 4_Resultados/
```

## Figuras

| | |
|---|---|
| fig1 | Funciones de modo de los cuatro sectores $(P,P')$ de $S^1/(Z_2\times Z_2')$ y su valor en cada pared |
| fig2 | Peso $|f_n|^2$ en pared I y II para $S^1$, $S^1/Z_2$, $S^1/(Z_2\times Z_2')$ |
| fig3 | Botella de Klein (selección por paridad del campo) y banda de Möbius (espectro semientero) |
| fig4 | Randall–Sundrum: modo cero ligado vs. onda de agua, potencial volcán, torre KK en branas UV/IR |
| fig5 | Cuerda negra RS: frecuencias KK vs. separación de branas y bandas LIGO/LISA |
| fig6 | Simulación 1+1 (**ilustración numérica de un teorema, no evidencia**): pulso junto a la pared I con contornos NN, ND, DN, DD; espectro visto en cada pared |
| fig7 | Frecuencia KK mínima impuesta por la estabilidad de Gregory–Laflamme vs. masa del agujero negro |
