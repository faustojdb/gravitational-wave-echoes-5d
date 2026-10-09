# Conclusiones del estudio: topografías 5D con selección de paridad por lado

## Respuesta corta a las tres preguntas

**¿Qué topografías son candidatas?** Una sola familia cumple el requisito de que "un lado anule los modos pares (o impares) y el otro lado los contrarios": el intervalo con dos paredes **inequivalentes**, es decir el orbifold $S^1/(Z_2\times Z_2')$, que es el intervalo ordinario $S^1/Z_2$ con una fase de Scherk–Schwarz $-1$. En él los modos de número KK impar se parten en dos familias espejo: $(+,-)$ existe sólo en nuestra pared y $(-,+)$ sólo en la pared sombra; los pares $(+,+)$ existen en ambas. Para que sus frecuencias caigan en la banda de los detectores respetando los tests de laboratorio, el intervalo debe además estar **warped** (Randall–Sundrum).

**¿Qué características deben tener?** (1) dos extremos distinguidos; (2) reflexiones independientes en cada extremo (torsión global); (3) gravitón con componentes de ambas paridades; (4) warping $e^{-2k|y|}$ con $\ell\lesssim0.1$ mm y separación $d/\ell\approx19$–$26$; (5) estabilidad de Gregory–Laflamme, que impone $f_1>0.43\,c^3/(2\pi GM)$; (6) modo cero exactamente 4D para respetar GW170817. Detalle en `1_Teoria/02_catalogo_topografias_candidatas.md`.

**¿Existen en bibliografía seria?** Sí. El $S^1/(Z_2\times Z_2')$ está publicado y es de uso corriente en física de partículas (Kawamura 2001, *Prog. Theor. Phys.*; Barbieri–Hall–Nomura 2001, *Phys. Rev. D*; clasificación de Nilse 2006). El warping con dos branas y agujero negro tiene predicción de ondas gravitacionales publicada (Seahra–Clarkson–Maartens 2005, *PRL*; Clarkson–Seahra 2007, *CQG*). Los ecos en branas gruesas están en *JHEP* 2025. **Lo que no existe** es la unión de ambas cosas: nadie ha calculado la señal de una fusión en un $S^1/(Z_2\times Z_2')$ warped con los cuatro sectores de paridad. Ésa es la contribución original posible.

## Resultados numéricos de esta sesión (`tabla_resumen.md`, `figuras/`)

| Resultado | Valor | Figura |
|---|---|---|
| Peso de los modos impares $(+,-)$ en pared II y $(-,+)$ en pared I | exactamente 0 | fig1, fig2 |
| Simulación 1+1, paredes (N,D): armónicos vistos en I / en II | 1,3,5,7 / ninguno | fig6 |
| Simulación 1+1, paredes (D,N): armónicos vistos en I / en II | ninguno (≤5 %) / 1,3,5,7 | fig6 |
| Botella de Klein, $l=0$: $k$ sobrevivientes para paridad $+$ / $-$ | pares / impares (sin dependencia del lado) | fig3 |
| Radio plano para $f_1=300$ Hz | $1.6\times10^5$ m, vs. cota Eöt-Wash $3.9\times10^{-5}$ m | tabla |
| Cuerda negra RS, $\ell=0.1$ mm: $f_1$ para $d/\ell=20,22,24,26$ | 3.8 kHz, 510 Hz, 69 Hz, 9 Hz | fig5 |
| Frecuencia KK mínima por estabilidad, $M=30,62,142\,M_\odot$ | 463, 224, 98 Hz | fig7 |
| RS1 ($kL=5$): $|\psi_n|$ en brana IR / UV | ≈5× mayor en IR | fig4 |

## Lo que la hipótesis acierta y lo que hay que corregir

**Acierta:**
- La idea de que la dimensión extra actúa como filtro de paridad es correcta y estándar: paridad $\pm$ ⇔ Neumann/Dirichlet en la pared.
- La imagen "onda de agua sobre el agua" tiene realización rigurosa: en RS2 el gravitón sin masa queda ligado a la brana con perfil $e^{-3k|y|/2}$ en distancia propia, análogo al $e^{-k\cdot\text{profundidad}}$ de las ondas de superficie, y el continuo masivo queda suprimido por el potencial volcán.
- "Energía que salta de un lado al otro" es exactamente la **materia sombra** de Garriga–Tanaka y Clarkson–Seahra: una fuente en una brana excita modos KK que llegan a la otra.

**Hay que corregir:**
- Una topografía **sin paredes** (círculo, botella de Klein, $RP^2$, Möbius) **no puede** producir selección dependiente del lado, porque no tiene lados. La botella de Klein da selección par/impar por paridad del campo, que es otra cosa. Esto afecta a los documentos anteriores del repositorio que atribuyen la supresión de modos pares a la no orientabilidad.
- La dimensión extra **no cambia la frecuencia de la onda principal** (el modo cero). Los modos KK aparecen como **líneas espectrales tardías** de frecuencia $f_n$ independiente de la masa del agujero negro, con decaimiento $t^{-5/6}$, no como ecos del pulso ni como un corrimiento del chirp.
- En compactificación plana, llevar $f_1$ a la banda LIGO exige $R\sim10^4$–$10^6$ m, excluido por $\sim10$ órdenes de magnitud por los tests de la ley $1/r^2$ (λ > 38.6 μm excluido, Lee et al. 2020). Sólo el warping salva la propuesta.

## Predicciones falsables del modelo candidato ($S^1/(Z_2\times Z_2')$ warped + cuerda negra)

1. **Líneas KK tardías** en $f_n\approx(z_n/\ell)e^{-d/\ell}c/2\pi$, con $z_n\to$ ceros de $J_1$ (razones $f_2/f_1\approx1.83$, $f_3/f_1\approx2.66$ en el límite $e^{-d/\ell}\ll1$), **iguales para todos los eventos** (no escalan con $M$).
2. **Cota inferior por estabilidad**: $f_1\gtrsim460\,(30M_\odot/M)$ Hz. Para una población de fusiones, la línea debería estar por encima de la cota del evento más masivo que sea estable; un evento con $M>0.43c^3/(2\pi G f_1)$ tendría una cuerda negra inestable (señal cualitativamente distinta).
3. **Selección de paridad**: en nuestra brana sólo son observables los sectores $(+,+)$ (frecuencias $\propto 2n$) y $(+,-)$ (frecuencias $\propto 2n+1$); el sector $(-,+)$ es invisible aquí. Si el tensor $h_{\mu\nu}$ se asigna a $(+,+)$ y el gravifotón/radión a los otros sectores, la predicción es que **las líneas de número impar deberían faltar (o estar en otra polarización)** en el espectro tardío. Esto es lo opuesto de lo propuesto en los documentos previos del repositorio y es decidible con datos.
4. **Ausencia de modo de respiración** fuerte: en una compactificación warped tipo RS el modo escalar sin masa (radión) adquiere masa por estabilización (Goldberger–Wise), de modo que no se espera la polarización de respiración de Andriot–Lucena Gómez a baja frecuencia.

## Próximos pasos concretos (en orden)

1. **Generalizar la ecuación (3) de Seahra–Clarkson–Maartens** $a^2Z''-2(aa')'Z=-m^2Z$ a las cuatro combinaciones de contorno (N,N), (N,D), (D,N), (D,D) en las branas $y=0,d$ y obtener las torres $m_n^{(P,P')}$ con Bessel. Es una extensión directa de `rs1_espectro()` en `3_Codigo/modos_paridad_topografias.py`.
2. **Reproducir la Fig. 4–5 de SCM 2005** (señal $\psi_{tot}=\sum c_nZ_n(0)\psi_n$ con potencial de Regge–Wheeler masivo) y calcular el espectro tardío para cada sector.
3. **Confrontar con GWTC-3/GWTC-4**: buscar líneas tardías comunes a todos los eventos (frecuencia fija, no escalada con $M$) con el formalismo de Miani et al. 2023, y usar la cota de estabilidad como prior. Los catálogos y herramientas de descarga ya existen en `Klein Subthreshold Theory/6_Data_Sources/`.
4. **Fijar las asignaciones $(P,P')$ de las componentes de la métrica** de forma consistente (como Barbieri–Hall–Nomura hacen para la materia), y revisar los documentos previos del repositorio que atribuyen la supresión de modos a la botella de Klein.
