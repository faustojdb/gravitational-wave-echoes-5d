# 4. El espacio-tiempo como medio elástico: derivación sin parámetros libres

Nivel de cada afirmación según `CLAUDE.md`: **[T]** teorema o derivación, **[M]** supuesto de modelo, **[D]** dato o cota publicada. Todos los números provienen de `3_Codigo/numeros_modelo_elastico.py` (salida en `4_Resultados/numeros_modelo_elastico.md`). No hay ningún parámetro ajustado.

Fe de erratas: en la conversación que motivó este documento se afirmó que una onda gravitacional con h ~ 10⁻²¹ transporta más energía por área que la luz solar. Es falso: el flujo es de 10⁻³ a 4×10⁻² W/m², entre 10⁻⁶ y 3×10⁻⁵ de la constante solar (§2.3).

---

## 1. Punto de partida: qué ecuaciones son posibles

**[T] Teorema de Lovelock (1971–72).** En cuatro dimensiones, el único tensor simétrico de rango 2, construido sólo con la métrica y sus derivadas hasta segundo orden, lineal en las segundas derivadas y con divergencia nula, es

$$E_{\mu\nu} = A\,G_{\mu\nu} + B\,g_{\mu\nu},$$

con $A$ y $B$ constantes. Igualándolo a la fuente conservada $T_{\mu\nu}$ se obtiene la ecuación de Einstein con constante cosmológica, y **nada más**:

$$G_{\mu\nu} + \Lambda g_{\mu\nu} = \frac{8\pi G}{c^4}\,T_{\mu\nu}.$$

Consecuencia directa para la pregunta "¿es $c^4/8\pi G$ un solo término de una ecuación mayor?": en 4D, con localidad, covariancia y segundo orden, la ecuación tiene **exactamente dos términos geométricos**, con dos constantes. Cualquier término adicional exige abandonar al menos una hipótesis del teorema: (i) derivadas de orden superior, (ii) campos adicionales a la métrica, (iii) más de cuatro dimensiones, (iv) no localidad. Ésta es la clasificación completa; no hay una quinta vía.

## 2. Lectura elástica de los dos términos

### 2.1 Rigidez

**[T]** Linealizando $g_{\mu\nu} = \eta_{\mu\nu} + h_{\mu\nu}$ en el gauge transverso sin traza, la acción de Einstein–Hilbert se reduce a

$$S = \frac{c^4}{64\pi G}\int d^4x\,\left[-\tfrac12\,\partial_\lambda h_{ij}\,\partial^\lambda h^{ij}\right],$$

que es la acción de un medio elástico con deformación adimensional $h_{ij}$ y **módulo** $K = c^4/8\pi G$. En unidades SI:

$$K = 4.8\times10^{42}\ \text{N}.$$

Es la única combinación de $c$ y $G$ con dimensiones de fuerza, y por eso no admite ajuste.

### 2.2 Pretensión

**[T]** El término $\Lambda g_{\mu\nu}$ equivale a un tensor de energía-momento $T^{(\Lambda)}_{\mu\nu} = -\rho_\Lambda c^2 g_{\mu\nu}$ con $\rho_\Lambda c^2 = \Lambda c^4/8\pi G$. En lenguaje elástico es una **tensión isótropa de reposo** del medio:

$$\Lambda c^4/8\pi G = 5.3\times10^{-10}\ \text{J/m}^3 \quad \text{[D: Λ de Planck 2018]}.$$

El cociente entre los dos términos de la ecuación define la única longitud que contienen: $L_\Lambda = 1/\sqrt{\Lambda} = 9.6\times10^{25}$ m. A escalas $L \ll L_\Lambda$ la pretensión es despreciable (el término "tiende a 0"); a $L \sim L_\Lambda$ domina.

### 2.3 Energía transportada por una deformación

**[T] (Isaacson).** El flujo de energía de una onda gravitacional es $F = \frac{c^3}{16\pi G}\langle \dot h_+^2 + \dot h_\times^2\rangle$. Para una onda monocromática de amplitud $h$ y frecuencia $f$: $F = \frac{c^3}{16\pi G}\,\frac{(2\pi f h)^2}{2}$.

| $h$ | $f$ | $F$ [W/m²] | $F$/constante solar |
|---|---|---|---|
| 10⁻²¹ | 100 Hz | 1.6×10⁻³ | 1.2×10⁻⁶ |
| 10⁻²¹ | 250 Hz | 9.9×10⁻³ | 7.3×10⁻⁶ |
| 2×10⁻²¹ | 250 Hz | 4.0×10⁻² | 2.9×10⁻⁵ |

La rigidez es enorme, pero la deformación es tan pequeña que el flujo en la Tierra es modesto. La luminosidad en la fuente sí es gigantesca ($\sim 10^{49}$ W para GW150914) porque el flujo se reparte sobre una esfera de 400 Mpc.

## 3. ¿Puede la rigidez depender de la escala? Qué forma está permitida

**[T] (análisis dimensional, teorema π de Buckingham).** Con las constantes $G$, $c$, $\hbar$ y $\Lambda$ se pueden formar exactamente **dos** longitudes independientes:

$$\ell_P = \sqrt{\hbar G/c^3} = 1.6\times10^{-35}\ \text{m},\qquad L_\Lambda = 1/\sqrt\Lambda = 9.6\times10^{25}\ \text{m},$$

separadas por $5.9\times10^{60}$. Por lo tanto, cualquier rigidez efectiva dependiente de la escala que **no introduzca una constante nueva** tiene necesariamente la forma

$$K(L) = \frac{c^4}{8\pi G}\;F\!\left(\frac{\ell_P}{L},\ \frac{L}{L_\Lambda}\right),\qquad F\to 1 \text{ cuando ambos argumentos}\to 0.$$

Éste es el contenido preciso de la intuición "un término tiende a 0, otro a G, otro a 1": los únicos términos adicionales que admiten $G$, $c$, $\hbar$ y $\Lambda$ son potencias de $\ell_P/L$ (se apagan hacia escalas grandes) y de $L/L_\Lambda$ (se apagan hacia escalas chicas), con el 1 en el medio. Un tercer tipo de término exige una **constante dimensional nueva** (un radio de compactificación, una tensión de brana, una escala de cruce), y eso ya es nivel **[M]**: no se deriva, se postula y se acota.

### 3.1 El término cuántico: tamaño calculado, no estimado

**[T] (Bjerrum-Bohr, Donoghue y Holstein 2003, teoría efectiva de la gravedad).** El potencial entre dos masas, incluyendo la primera corrección cuántica, es

$$U(r) = -\frac{GMm}{r}\left[1 + \frac{3G(M+m)}{rc^2} + \frac{41}{10\pi}\frac{\ell_P^2}{r^2}\right],$$

donde el segundo sumando es clásico (post-newtoniano) y el tercero es el término $(\ell_P/L)^2$ de la forma general anterior, con coeficiente calculado. (Trabajos posteriores agregan una contribución $-\tfrac{43}{12\pi}\ell_P^2/r^2$ de fluctuaciones de las partículas; el orden de magnitud no cambia.) Tamaño:

| $r$ | $\frac{41}{10\pi}(\ell_P/r)^2$ |
|---|---|
| 1 m | 3×10⁻⁷⁰ |
| 38.6 µm (límite Eöt-Wash) | 2×10⁻⁶¹ |
| 1 fm | 3×10⁻⁴⁰ |

Comparación: el término clásico $3G(M+m)/rc^2$ para dos masas solares a 10⁶ m vale 9×10⁻³. **Conclusión [T]:** la "conciliación con la mecánica cuántica" dentro de la propia ecuación de Einstein existe, está calculada, y es inobservable por sesenta órdenes de magnitud a cualquier escala de laboratorio o astrofísica. Esto no es una opinión: es el tamaño del único término cuántico que la estructura permite sin constantes nuevas.

### 3.2 Dónde las cotas dejan lugar

**[D]** Cotas publicadas sobre $|F - 1|$, usando las referencias de `2_Bibliografia`:

| Escala | Medición | $|F-1|$ permitido |
|---|---|---|
| < 38.6 µm | ninguna | sin cota; 30.4 décadas hasta $\ell_P$ |
| 50 µm – 3 mm | Lee et al. 2020 | Yukawa de intensidad gravitacional excluida |
| 10⁶ – 10¹² m | Sistema Solar (PPN) | ~10⁻⁵ |
| 10⁵ m, deformación ~1 | ringdown LVK (GWTC-3) | ~10–20 % |
| 10²³ – 10²⁵ m | GW170817: $D = 4.02^{+0.07}_{-0.10}$, $c_{gw} = c$ | ~10⁻² en fuga de amplitud |
| 10²⁶ m | expansión acelerada | aquí manda $L/L_\Lambda$ |

Dos regiones no están acotadas: la **submilimétrica** y el **campo fuerte**. Toda constante nueva [M] tiene que vivir en una de las dos para no estar ya excluida.

## 4. Rotura

### 4.1 Rotura gravitacional: deformación de orden uno

**[T]** La expansión $g = \eta + h$ tiene como parámetro $h \sim \Phi/c^2 \sim GM/(rc^2) = r_S/2r$, con $r_S = 2GM/c^2$. La teoría lineal deja de valer cuando $h \sim 1$, es decir $r \sim r_S$. La **conjetura del aro** (Thorne 1972) formaliza que una masa confinada dentro de su $r_S$ en todas las direcciones forma un horizonte. Para el remanente de GW150914 (62 M☉), $r_S = 183$ km; para 30 M☉, 89 km.

Lo que se rompe en $r = r_S$ no es el tejido, cuya curvatura $\sim 1/r_S^2$ es finita y pequeña para masas grandes, sino la **estructura causal**: aparece una superficie de un solo sentido. En lenguaje elástico, la deformación llega a uno y el medio deja de ser lineal; ésa es la lectura rigurosa de "lo más grande roto".

### 4.2 Rotura cuántica: localización de orden uno

**[T]** Localizar una partícula de masa $m$ en $\Delta x$ cuesta $\Delta E \gtrsim \hbar c/\Delta x$. Cuando $\Delta x \lesssim \hbar/mc$ (longitud de Compton reducida, 3.9×10⁻¹³ m para el electrón), $\Delta E \gtrsim mc^2$ y la energía alcanza para crear pares: la noción de "una partícula" se pierde. La versión con campo es el **límite de Schwinger**: la tasa de creación de pares en un campo eléctrico $E$ va como $\exp(-\pi E_S/E)$ con

$$E_S = \frac{m_e^2 c^3}{e\hbar} = 1.3\times10^{18}\ \text{V/m}.$$

El vacío tiene una **resistencia a la tracción finita**: estirado por encima de $E_S$ se desgarra en pares. Ésta es la versión cuántica rigurosa de "cuando se estira suficiente pasan elementos de un lado al otro": lo que pasa son partículas desde el vacío, y la condición es un campo crítico calculable, no un parámetro.

### 4.3 Las dos roturas se cruzan en un único punto

**[T]** $r_S$ crece con $m$; $\lambda_C$ decrece con $m$. Igualando $\hbar/mc = 2Gm/c^2$:

$$m_\times = \sqrt{\hbar c/2G} = m_P/\sqrt2 = 1.5\times10^{-8}\ \text{kg},\qquad \text{escala } \ell_P.$$

Por debajo de $\ell_P$ medir una distancia requiere una energía cuyo $r_S$ supera la distancia medida. **La rotura gravitacional más grande y la rotura cuántica más pequeña coinciden en una sola escala**; es un resultado de análisis dimensional, y es exactamente el punto donde la ecuación de §1 deja de ser una teoría efectiva válida. Que ahí no haya teoría completa es el problema abierto de la gravedad cuántica. Ninguna teoría elástica lo resuelve por sí misma: sólo reescribe la pregunta.

## 5. Permeabilidad: qué pasa de un lado al otro y con qué coeficientes

### 5.1 La membrana clásica

**[T] (Damour 1978; Thorne, Price y Macdonald 1986).** Proyectando las ecuaciones de Einstein y Maxwell sobre una superficie temporal justo fuera del horizonte (el "horizonte estirado"), se obtiene que ese horizonte se comporta exactamente como una membrana con:

| Propiedad | Valor | Derivación |
|---|---|---|
| resistividad superficial | $4\pi/c$ (gaussiano) $= \sqrt{\mu_0/\epsilon_0} = 376.7\ \Omega$ | condición de contorno de Maxwell en el horizonte |
| viscosidad de cizalla | $\eta = c^3/16\pi G = 8.0\times10^{33}$ Pa·s | ecuación de Raychaudhuri para la cizalla |
| viscosidad volumétrica | $\zeta = -\eta$ | ecuación de Raychaudhuri para la expansión |
| transmisión | total hacia adentro, nula hacia afuera | estructura causal |

Es decir: la relatividad general **ya asigna** al tejido, en su punto de rotura, una elasticidad ($K$), una pretensión ($\Lambda$), una viscosidad ($\eta$) y una permeabilidad (de un solo sentido, con impedancia de 377 Ω). Todos son teoremas; ninguno es un parámetro nuevo.

### 5.2 Qué pasa realmente a través de la membrana

**[T]** Para un observador acelerado con aceleración $a$, el vacío de Minkowski es un baño térmico a $T = \hbar a/2\pi c k_B$ (Unruh 1976); un horizonte de masa $M$ radia a $T = \hbar c^3/8\pi G M k_B$ (Hawking 1974). Para $a = g$: $T = 4\times10^{-20}$ K. Para 62 M☉: $T = 10^{-9}$ K. Luego la membrana **sí** deja pasar algo hacia afuera, pero es radiación térmica cuántica de temperatura ínfima para cualquier agujero negro astrofísico. Ésta es la única "permeabilidad hacia afuera" que la física establecida permite, y su tamaño está fijado.

### 5.3 Permeabilidad distinta de la clásica

**[M]** Toda propuesta en la que "pasen elementos al otro lado" con amplitud mayor que la de Hawking equivale a asignar al horizonte estirado una **reflectividad** $\mathcal R(\omega) \neq 0$ o una transmisión hacia una región externa (otra brana, otro lado de la dimensión extra). Eso es un parámetro nuevo. Sus consecuencias observables son conocidas y únicas: **ecos** tras el ringdown con retardo $\tau \simeq \frac{2 r_S}{c}\ln(r_S/\delta)$, creciente con $M$ (Cardoso, Franzin y Pani 2016), y modificación del espectro de modos cuasinormales.

**[D]** Ese parámetro ya está acotado: búsquedas de ecos de la colaboración LVK sobre GWTC-3 (negativas), límites de amplitud de Miani et al. 2023, y nuestros propios análisis v1 y v2 sobre 18 fusiones (negativos, `5_Datos_Reales/`). La región que sobrevive es la de reflectividad baja, en la zona de 10–20 % donde el ringdown aún no discrimina.

## 6. Síntesis: qué queda demostrado y qué queda abierto

**Demostrado [T]:**
1. La ecuación tiene exactamente dos términos geométricos (Lovelock); $c^4/8\pi G$ es la rigidez y $\Lambda c^4/8\pi G$ la pretensión.
2. Sin constantes nuevas, cualquier dependencia de la rigidez con la escala es función de $\ell_P/L$ y $L/L_\Lambda$; el término cuántico está calculado y es $\sim 10^{-61}$ incluso en el límite de laboratorio.
3. La rotura gravitacional (deformación ~1, horizonte) y la rotura cuántica (localización ~1, pares) se cruzan en la masa de Planck.
4. El horizonte tiene elasticidad, pretensión, viscosidad y permeabilidad de un solo sentido con coeficientes derivados; hacia afuera sólo pasa radiación de Hawking.

**Abierto, y acotado [M]+[D]:**
5. Cualquier término adicional necesita una constante dimensional nueva que viva por debajo de 38.6 µm o en campo fuerte. En campo fuerte su firma única son ecos con retardo creciente con la masa; los datos actuales los excluyen por encima de cierta amplitud y nuestros análisis no vieron líneas comunes.

**Lo que esto implica para la hipótesis original.** La "pared" como limitación dimensional, el filtro de paridad y el "pasar al otro lado" tienen cada uno una versión rigurosa, y las tres versiones ya están en la física establecida: orbifold $S^1/(Z_2\times Z_2')$, horizonte estirado, efecto Schwinger/Hawking. Una teoría nueva tendría que predecir algo que **ninguna** de las tres predice y que no esté en la tabla de cotas de §3.2. Hoy el único lugar donde eso es posible con datos de LIGO es el campo fuerte, y la predicción allí no es una frecuencia fija sino un retardo proporcional a la masa.
