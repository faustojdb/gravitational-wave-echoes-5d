# 6. Materia sombra: derivación exacta de cómo gravita la materia de la otra pared

Etiquetas: **[T]** derivación, **[M]** supuesto de modelo, **[D]** dato publicado. Números y verificación numérica en `4_Resultados/numeros_materia_sombra.md` (`3_Codigo/numeros_materia_sombra.py`). Sin parámetros libres salvo la separación L entre paredes, que ya está acotada (L ≲ 40 µm para geometría plana, `05_ventana_submilimetrica.md`).

## 1. Supuestos (todos de modelo, y los mínimos)

**[M1]** Una dimensión extra plana con dos extremos: nuestra pared en y = 0 y otra en y = L. Topológicamente es el intervalo S¹/Z₂ con L = πR, o S¹/(Z₂×Z₂′) con L = πR/2 y el gravitón en el sector (+,+). Los resultados de abajo dependen sólo de L.
**[M2]** La materia (la nuestra y la de la otra pared) está confinada a su pared. La gravedad se propaga en el bulk. Es el supuesto estándar de los mundos brana; sin él no hay "otra pared".
**[M3]** Régimen de campo débil y distancias r ≫ ℓ_P. Nada más.

No se supone nada sobre la naturaleza de la materia sombra: puede ser una copia del Modelo Estándar, otra cosa, o nada.

## 2. El potencial gravitacional, exacto

**[T] Suma de modos.** Una masa puntual m en la posición y_s de la dimensión extra produce en un punto de nuestra pared (y = 0), a distancia r a lo largo de la pared, el potencial

$$V(r) = -\frac{G m}{r}\sum_{n\ge0}\frac{f_n(0)\,f_n(y_s)}{f_0^2}\,e^{-m_n r},$$

con f_n las funciones de modo normalizadas y m_n las masas KK (es la función de Green de la ecuación de Poisson en 5D descompuesta en modos, con G = G₅/(2πR) para que el modo cero reproduzca Newton). Para el intervalo con condición de Neumann en ambas paredes: f_0 = 1/√L, f_n = √(2/L) cos(nπy/L), m_n = nπ/L.

**[T] Nuestra materia (y_s = 0):** f_n(0)² / f_0² = 2 para todo n ≥ 1, luego

$$V_{\rm propio}(r) = -\frac{Gm}{r}\Big[1 + 2\sum_{n\ge1} e^{-n\pi r/L}\Big] = -\frac{Gm}{r}\,\frac{1+x}{1-x} = -\frac{Gm}{r}\coth\!\left(\frac{\pi r}{2L}\right),\qquad x\equiv e^{-\pi r/L}.$$

**[T] Materia sombra (y_s = L):** f_n(L)/f_n(0) = cos(nπ) = (−1)ⁿ, luego

$$V_{\rm sombra}(r) = -\frac{Gm_s}{r}\Big[1 + 2\sum_{n\ge1} (-1)^n e^{-n\pi r/L}\Big] = -\frac{Gm_s}{r}\,\frac{1-x}{1+x} = -\frac{Gm_s}{r}\tanh\!\left(\frac{\pi r}{2L}\right).$$

Las dos series geométricas se suman en forma cerrada; no hay aproximación.

**[T] Verificación independiente por imágenes.** El mismo potencial se obtiene sin modos: en el cubrimiento S¹ de circunferencia 2L, una masa a distancia d en la dimensión extra equivale a una fila infinita de imágenes a distancias d + 2Lk, cada una con el potencial de Newton 5D ∝ 1/(r² + (d+2Lk)²). Por la fórmula de sumación de Poisson, esa suma es idéntica a la suma de modos. El script lo comprueba numéricamente para d = 0 y d = L: las tres expresiones (modos, imágenes, forma cerrada) coinciden a 10⁻⁶ en todo el rango.

## 3. Límites y lectura física

| Régimen | materia propia | materia sombra |
|---|---|---|
| r ≫ L | −Gm/r [1 + 2e^{−πr/L}] | −Gm_s/r [1 − 2e^{−πr/L}] |
| r ≪ L | −2GmL/(πr²): Newton en 5D | −πGm_s/(2L): **finito** |
| fuerza, r ≪ L | 4GmL/(πr³), atractiva, ∝ 1/r³ | −π³Gm_s r/(12L³): restauradora, ∝ r, → 0 |

**[T] Tres consecuencias exactas:**

1. **A distancias mayores que unas pocas L, la materia sombra gravita exactamente como la nuestra.** La diferencia relativa es 4e^{−πr/L}: a r = 3L es 3×10⁻⁴, a r = 5L es 6×10⁻⁷. Con L < 40 µm, toda escala astrofísica, geofísica y de laboratorio ordinario está en este régimen.
2. **A distancias menores que L, la materia sombra desaparece gravitacionalmente.** Su potencial en r = 0 es finito, −πGm_s/2L, porque la separación a través del bulk domina. No hay singularidad ni fuerza divergente: una masa sombra justo "debajo" de un punto de nuestra pared no lo atrae, y a pequeñas r la fuerza es una restauradora débil proporcional a r.
3. **La función de permeabilidad gravitacional** es

$$P(r) \equiv \frac{V_{\rm sombra}}{V_{\rm Newton}} = \tanh\!\left(\frac{\pi r}{2L}\right),$$

con P → 0 en r ≪ L y P → 1 en r ≫ L. Es la única función que la geometría permite; no tiene parámetros aparte de L.

| r/L | P(r) | V_propio/V_Newton | sombra/propio = P² |
|---|---|---|---|
| 0.1 | 0.16 | 6.42 | 0.02 |
| 0.5 | 0.66 | 1.52 | 0.43 |
| 1 | 0.92 | 1.09 | 0.84 |
| 2 | 0.996 | 1.004 | 0.993 |
| 5 | 1.0000 | 1.0000 | 1.0000 |

**[T] Qué cambia con la selección de paridad.** En S¹/(Z₂×Z₂′) la pared sombra puede excitar además el sector (−,+). Esas funciones se anulan en y = 0: su contribución a nuestro potencial es idénticamente cero. Y los sectores (+,−) que excitamos nosotros se anulan en la pared sombra. Luego la permeabilidad entre paredes la lleva **sólo** el sector (+,+), con la fórmula de arriba. La paridad no agrega un parámetro; quita canales.

## 4. Ondas gravitacionales de materia sombra

**[T] Teorema de evanescencia.** Un modo KK de masa m_n sólo se propaga hasta el infinito si ħω > m_n c²; por debajo es evanescente y no transporta energía. Para L < 40 µm, m₁c² > 5 meV, mientras que ħω ≈ 10⁻¹² eV para una fusión a 250 Hz: ω/m₁ ≈ 2×10⁻¹⁰. Por lo tanto **toda** la radiación gravitacional de cualquier fuente astrofísica, propia o sombra, va al modo cero.

**[T] Consecuencia.** El modo cero es constante en y: f_0(0) = f_0(L). Una fusión en la pared sombra produce en nuestros detectores **exactamente** la forma de onda de la relatividad general 4D, con la misma amplitud, la misma fase y la misma relación distancia–amplitud que una fusión propia. Nada en la señal gravitacional la distingue. Lo mismo vale para las lentes gravitacionales a parámetros de impacto ≫ L: deflexión idéntica.

Así que la materia sombra es, para todo observable gravitacional accesible, **indistinguible de la materia ordinaria**; y para todo observable no gravitacional (luz, colisiones, química) es **inexistente**. Ésa es, palabra por palabra, la definición operativa de materia oscura. Esto no es una hipótesis que se agrega: es lo que las fórmulas de §2 y §4 implican.

## 5. Lo que ya está acotado y lo que no

**[M]** La abundancia de materia sombra es libre. Si fuera toda la materia oscura, m_s/m_b = Ω_c/Ω_b = 5.4 (Planck 2018) **[D]**.

**[D]** Cotas publicadas que se aplican según cómo esté distribuida (las marcadas ⚠️ se citan de memoria y deben verificarse antes de usarse):

| Si la materia sombra… | entonces la acota | estado |
|---|---|---|
| forma objetos compactos (estrellas, planetas sombra) | microlente: EROS-2 2007 excluye que objetos de 10⁻⁷–15 M☉ sean más del ~8 % del halo; OGLE 2024 baja ese techo al ~1 % en un rango amplio ⚠️ | fuertemente acotada |
| tiene su propia radiación en la nucleosíntesis | N_eff: su temperatura debe ser T_s/T ≲ 0.5 (literatura de materia espejo, Berezhiani; Foot) ⚠️ | acotada |
| se disipa y forma un disco oscuro | cinemática de Gaia sobre la densidad local del disco ⚠️ | acotada |
| forma estrellas de neutrones que se fusionan | ondas gravitacionales con masas de BNS y sin kilonova. GW170817 tuvo contraparte; GW190425 no la tuvo, pero su localización de ~8000 grados² no permite concluir | sin cota útil hoy |
| es colisionless y difusa | nada la distingue de la materia oscura fría estándar | sin cota: es materia oscura fría |

**[T] Lo que no se puede medir.** La única firma que distingue a la materia sombra de la materia oscura ordinaria es la supresión tanh a r ≲ L < 40 µm. Para medirla haría falta una masa sombra conocida a decenas de micras de un sensor. Si la materia sombra es difusa, su densidad local sería a lo sumo la de la materia oscura, 0.4 GeV/cm³, un fondo uniforme sin gradiente: fuerza neta nula. La firma es, por tanto, **inaccesible** con cualquier instrumento concebible. Esto es una consecuencia de las fórmulas, no una opinión.

## 6. Sobre "elementos que pasan de un lado al otro"

**[T]** Con los supuestos [M1]–[M3], **nada material pasa**. Lo único que cruza el bulk es gravedad: el modo cero completo, y modos masivos sólo por encima de los terahercios. La permeabilidad P(r) describe cuánta gravedad de la otra pared llega, no cuánta materia.

**[M]** Para que pase materia haría falta un campo que viva en el bulk y se acople a la materia de ambas paredes, o una oscilación entre estados de las dos paredes. Eso sí tiene cotas directas: la materia de nuestra pared desaparecería a una tasa Γ, y la conservación de energía en nuestra pared está verificada a precisiones altísimas; para neutrones, los límites sobre oscilaciones a un "neutrón espejo" exigen tiempos característicos mayores que cientos de segundos ⚠️ (Berezhiani y colaboradores, experimentos con neutrones ultrafríos). Cualquier mecanismo de paso tiene que ser más lento que eso.

## 7. Síntesis

- **[T]** Materia propia: V = −(Gm/r) coth(πr/2L). Materia sombra: V = −(Gm_s/r) tanh(πr/2L). Exacto, verificado por dos métodos.
- **[T]** Permeabilidad gravitacional P = tanh(πr/2L): la otra pared gravita por completo de lejos y nada de cerca.
- **[T]** La paridad del orbifold sólo cierra canales; el que queda es el (+,+), con la fórmula anterior.
- **[T]** Sus ondas gravitacionales y sus lentes son idénticas a las nuestras. Es materia oscura por construcción.
- **[M]+[D]** Su abundancia es libre; su distribución está acotada por microlentes, nucleosíntesis y cinemática galáctica si no es difusa y fría.
- **[T]** Su única firma propia (la supresión por debajo de 40 µm) es inaccesible.

Conclusión honesta para el proyecto: la materia sombra es una **realización geométrica** de la materia oscura fría, elegante y sin parámetros en su gravedad, pero que no añade ninguna predicción comprobable que la materia oscura fría no tenga ya. Lo que podría distinguirla es su física interna (si tiene fotones propios, estrellas propias, fusiones propias), y eso ya no es geometría: es un modelo de partículas de la otra pared, con las cotas de la tabla de §5.
