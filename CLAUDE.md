# Lineamientos para trabajar en este repositorio

Estos lineamientos fueron fijados por el autor (Fausto José Di Bacco) el 9 de octubre de 2026 y aplican a toda sesión futura, en cualquier carpeta del repositorio.

## Principios no negociables

1. **Nada sintético presentado como evidencia.** Simulaciones, datos generados, "toy models" y figuras de fórmulas pueden usarse para ilustrar un argumento matemático, pero deben estar etiquetados como tales y nunca contarse como resultado observacional, significancia estadística ni "validación".
2. **No cherry-picking.** No se eligen eventos, segmentos, frecuencias, parámetros ni referencias por conveniencia. Toda selección de muestra se define antes de mirar el resultado y se documenta. Los controles (segmentos de ruido fuera de eventos, inyecciones nulas, permutaciones) se corren con el mismo pipeline que el análisis.
3. **Nada ad hoc.** Ningún parámetro se ajusta a mano para que salga un resultado. Si una hipótesis necesita un supuesto adicional, se declara como supuesto de modelo, separado del teorema y del dato.
4. **Solo datos reales.** Los únicos datos aceptados son los públicos de LIGO-Virgo-KAGRA (GWOSC: strain, catálogos GWTC, posteriores), de NANOGrav u otros experimentos reconocidos, siempre descargados de la fuente y con el origen registrado.
5. **Separar tres niveles en todo documento de resultados:** (a) teorema o resultado matemático, (b) supuesto de modelo, (c) dato observacional o cota publicada. No mezclar niveles en una misma afirmación.
6. **Bibliografía verificada.** Cada referencia citada se verifica contra arXiv, la revista o el texto. Las no verificadas se marcan explícitamente como tales.

## Sobre trabajo previo en el repositorio

- Las carpetas de la "teoría de Klein" (KLEIN FIELD THEORY, FUNDAMENTAL_RADIUS_INVESTIGATION, teoria_refinada, Klein_Studies, KLEIN_* y afines) **no se usan como insumo**: ni sus fórmulas, ni sus radios, ni sus significancias. No se citan para sostener nada nuevo. Sólo se reutilizan scripts de descarga o de acceso a datos reales que puedan servir, previa lectura.
- El trabajo nuevo vive en `TOPOGRAFIAS_PARIDAD_5D/` y en las carpetas que se creen a partir de ahora.

## Sobre el lenguaje físico

- "Pared", "punto fijo" o "borde" de una dimensión extra significa una **limitación dimensional** (una condición sobre las configuraciones posibles del campo), no un objeto físico. Si un modelo requiere un objeto físico (brana con tensión, fuente del warping), se dice explícitamente que es un supuesto adicional.
- La onda principal detectada por LIGO es el modo sin masa; una dimensión extra no cambia su frecuencia. Cualquier efecto de la dimensión extra se discute como modos masivos (líneas tardías), fugas de amplitud o polarizaciones extra, no como corrimientos del chirp.

## Práctica de sesión

- Antes de analizar datos, escribir el protocolo (muestra, método, controles, criterio de éxito) en un archivo y no cambiarlo después de ver los resultados.
- Reportar resultados negativos con el mismo detalle que los positivos.
- Commits en ramas nuevas; `main` no se toca sin pedido explícito del autor.
