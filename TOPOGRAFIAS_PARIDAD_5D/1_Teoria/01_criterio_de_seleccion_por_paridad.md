# 1. El criterio matemático: ¿qué topografía de la 5ª dimensión anula los modos pares de un lado y los impares del otro?

## 1.1 Planteo

La hipótesis de trabajo es la siguiente. Una fusión de agujeros negros (o una supernova) emite ondas gravitacionales que, si el espacio-tiempo tiene una quinta dimensión, también propagan "hacia adentro" de esa dimensión. La idea es que la geometría de esa dimensión extra actúa como un filtro de paridad: **cuando la onda vuelve a nuestro lado un conjunto de modos (digamos los pares) queda anulado, y cuando va hacia el otro lado se anula el conjunto contrario (los impares)**. La imagen física es la de una onda de agua que vive en la superficie pero no debajo del agua.

Para convertir esta imagen en una condición matemática verificable hay que responder tres preguntas:

1. ¿Qué significa "modo par / impar" en una dimensión extra? → número de Kaluza-Klein (KK) y paridad bajo una reflexión.
2. ¿Qué significa "nuestro lado" y "el otro lado"? → dos puntos distinguidos (paredes, branas, puntos fijos) de la dimensión extra.
3. ¿Qué propiedad de la topografía hace que un mismo modo se anule en un punto y no en el otro? → que las dos paredes sean **puntos fijos de reflexiones distintas**, es decir que la dimensión extra no sea simétrica entre sus dos extremos.

## 1.2 Descomposición de Kaluza-Klein

Tomemos un campo sin masa en 5D (vale para un escalar y, con cambios menores de normalización, para la perturbación tensorial transversa-sin-traza $h_{\mu\nu}$ del gravitón, que es lo que importa para ondas gravitacionales):

$$\left(\Box_4 + \partial_y^2\right)\Phi(x,y)=0,\qquad \Phi(x,y)=\sum_n \phi_n(x)\,f_n(y),\qquad -f_n''=m_n^2 f_n .$$

Cada $f_n(y)$ es un **modo KK**; en 4D el campo $\phi_n$ se comporta como una partícula de masa $m_n$. El modo con $m_0=0$ es el gravitón ordinario de la Relatividad General; los demás son gravitones masivos. La geometría/topología de la dimensión $y$ fija (a) qué $f_n$ existen, (b) sus masas $m_n$, y (c) **el valor $f_n(y_\star)$ en el punto $y_\star$ donde está nuestra brana**. Ese valor es el acoplamiento del modo $n$ con la materia de nuestra brana: un modo con $f_n(y_\star)=0$ **no se emite ni se detecta** en nuestra brana. Esa es la traducción precisa de "el modo queda anulado de nuestro lado".

## 1.3 Paridad = condición de contorno

Si la dimensión extra tiene una reflexión $y\to -y$ como simetría (orbifold), cada campo tiene una paridad $P=\pm 1$ bajo ella, y en el punto fijo $y=0$:

| paridad del campo en el punto fijo | condición de contorno en $y=0$ | modos |
|---|---|---|
| $P=+1$ (par) | Neumann, $f'(0)=0$ | $\cos$: **no se anulan** en la pared |
| $P=-1$ (impar) | Dirichlet, $f(0)=0$ | $\sin$: **se anulan** en la pared |

Esto es estándar en modelos de orbifold (Hořava–Witten 1996; Randall–Sundrum 1999; lecciones de Csáki 2004). Un campo impar bajo la reflexión **no tiene modo cero** y **vale cero sobre la pared**: no puede acoplarse a materia confinada allí.

## 1.4 El criterio: dos paredes, dos reflexiones distintas

Si la dimensión extra es un intervalo con dos paredes, cada pared puede ser el punto fijo de **su propia** reflexión. En el orbifold $S^1/(Z_2\times Z_2')$ (Kawamura 2001; Barbieri–Hall–Nomura 2001) las reflexiones son

$$Z_2:\ y\to -y \quad(\text{pared I en } y=0),\qquad Z_2':\ y'\to -y',\ \ y'=y+\tfrac{\pi R}{2}\quad(\text{pared II en } y=-\tfrac{\pi R}{2}),$$

y cada campo lleva **dos** paridades $(P,P')$. Las funciones de modo (verificadas en el texto de Kawamura, Prog. Theor. Phys. 105, 999) son:

| $(P,P')$ | $f_n(y)$ | masa | en pared I ($y=0$) | en pared II ($|y|=\pi R/2$) |
|---|---|---|---|---|
| $(+,+)$ | $\cos(2ny/R)$ | $2n/R$ (0, 2, 4, …) | $\neq 0$ | $\neq 0$ |
| $(+,-)$ | $\cos((2n+1)y/R)$ | $(2n+1)/R$ (1, 3, 5, …) | $\neq 0$ | **$=0$** |
| $(-,+)$ | $\sin((2n+1)y/R)$ | $(2n+1)/R$ (1, 3, 5, …) | **$=0$** | $\neq 0$ |
| $(-,-)$ | $\sin((2n+2)y/R)$ | $(2n+2)/R$ (2, 4, 6, …) | **$=0$** | **$=0$** |

Léase así: **los modos de número KK impar vienen en dos familias espejo**. La familia $(+,-)$ vive en nuestra pared y está anulada en la pared sombra; la familia $(-,+)$ está anulada en nuestra pared y vive en la sombra. Los modos de número KK par $(+,+)$ viven en ambas, y $(-,-)$ en ninguna. Esto es, con toda exactitud, el mecanismo que propone la hipótesis: la misma onda 5D, al "ir hacia nuestro lado" sólo puede materializarse en los modos no nulos en la pared I; al "ir hacia el otro lado" sólo en los no nulos en la pared II. Y los dos conjuntos son complementarios para los modos impares. La figura `4_Resultados/figuras/fig1_modos_S1_Z2xZ2p.png` muestra los cuatro sectores, y la simulación 1+1 de `fig6_simulacion_dos_paredes.png` lo muestra dinámicamente: un pulso emitido junto a la pared I con condiciones (N,D) se registra con armónicos 1,3,5,7 en la pared I y **nada** en la pared II; con (D,N) ocurre exactamente lo contrario.

**Condición necesaria y suficiente (nivel de campo libre):** para que exista selección de paridad *dependiente del lado* hacen falta
1. **dos puntos fijos** (paredes) en la dimensión extra, y
2. que las reflexiones asociadas a cada pared sean **independientes**, de modo que un campo pueda ser par respecto a una e impar respecto a la otra.

Nilse (2006) muestra que (2) equivale a tomar el intervalo ordinario $S^1/Z_2$ con **fases de Scherk–Schwarz no triviales**: "los campos de paridad $(p,q)$ en $S^1/Z_2$ de radio $R$ corresponden a paridades $(p,pq)$ en $S^1/(Z_2\times Z_2')$ de radio $2R$". Es decir: la topografía buscada **no es exótica**; es el intervalo de siempre, pero con una **torsión global** (una fase $-1$ al dar la vuelta) que hace que las dos paredes sean inequivalentes.

## 1.5 Lo que NO cumple el criterio

* **Círculo $S^1$**: no hay paredes, todos los modos $e^{iny/R}$ tienen $|f_n|=1$ en todas partes. Sin selección.
* **Intervalo simétrico $S^1/Z_2$** (una sola paridad): las dos paredes son equivalentes. Un campo impar se anula en **ambas**; uno par no se anula en ninguna. Hay selección por paridad del campo, pero **no por lado**. Lo único que distingue las paredes es el signo $(-1)^n$ de $\cos(n\pi)$: los modos impares llegan a la segunda pared con el signo invertido (ésta es la "paridad KK" de los modelos UED de Appelquist–Cheng–Dobrescu 2001 y Cheng–Matchev–Schmaltz 2002), pero no anulados.
* **Botella de Klein** $R^2/pg$ (Nilse 2006, sec. 3.2): la paridad se define respecto de una **reflexión deslizante**, que no tiene puntos fijos. Resultado verificado: con $l=0$, $F^{(+)}_{2k+1,0}=F^{(-)}_{2k,0}=0$, o sea **un campo de paridad $+$ sólo tiene $k$ pares y uno de paridad $-$ sólo $k$ impares**. Hay selección par/impar, pero es una propiedad **del campo**, no **del lugar**: como no hay paredes, no hay "nuestro lado" y "el otro lado". Para que la botella de Klein produzca selección por lado hay que agregarle paredes a mano: Greene, Kabat, Levin y Porrati (2025) construyen la Klein bottle en 6D como $(x^4,x^5)\sim(-x^4,x^5+2\pi r_5)$ y encuentran que la **reflexión** $x^4\to-x^4$ sí deja "paredes de paridad" en $x^4=0,\pi r_4$ donde la densidad de energía se concentra. Eso recupera dos puntos distinguidos, pero su mecanismo requiere dos dimensiones extra, no una.
* **Banda de Möbius**: tiene un borde genuino (no un punto fijo) y una torsión. Separando $f=e^{i2\pi qx/L}g(y)$ con $(x,y)\sim(x+L,-y)$: los modos **pares en el ancho** tienen $q$ entero y los **impares** tienen $q$ **semientero**. La torsión desplaza en ½ el espectro de una de las dos familias (es una fase de Scherk–Schwarz geométrica), pero el borde es uno solo y conexo: no hay dos lados distinguidos.

## 1.6 Qué cambia con el warping (Randall–Sundrum)

Todo lo anterior es plano. Si la métrica es $ds^2=e^{-2k|y|}\eta_{\mu\nu}dx^\mu dx^\nu+dy^2$ (Randall–Sundrum), las paridades y las condiciones de contorno son las mismas (Neumann para el gravitón par en cada brana), pero:

* las funciones de modo pasan de senos/cosenos a **funciones de Bessel** $z^2[J_2(mz)+bY_2(mz)]$ en la coordenada conforme $z=e^{ky}/k$;
* el espectro deja de ser $n/R$ y pasa a $m_n\simeq x_n\,k\,e^{-kL}$ con $x_n$ los ceros de $J_1$ (3.83, 7.02, 10.17, …): **exponencialmente comprimido**;
* el peso de cada modo KK es **mucho mayor en la brana IR que en la UV** (`fig4_randall_sundrum.png`, panel derecho): el warping es por sí mismo un filtro asimétrico entre los dos lados, aunque no de paridad;
* en RS2 (una sola brana, $L\to\infty$) el modo cero queda **ligado a la brana** con perfil $\psi_0\propto e^{-3k|y|/2}$ en distancia propia, exactamente el perfil de una onda de agua profunda ($\propto e^{-k\cdot\text{profundidad}}$, Lamb §228). Ésta es la versión rigurosa de la analogía "la onda vive en la superficie pero no debajo del agua": el continuo de modos masivos está suprimido en la brana por el potencial "volcán" $V(z)=15k^2/[8(k|z|+1)^2]-(3k/2)\delta(z)$ y la gravedad newtoniana sólo recibe la corrección $V(r)\propto\frac{1}{r}\left(1+\frac{1}{k^2r^2}\right)$.

Combinar (a) dos branas con reflexiones independientes y (b) warping es perfectamente consistente: Hořava–Witten ya es un $S^1/Z_2$ con dos paredes de 10D; RS1 es un $S^1/Z_2$ warped; y los modelos de GUT en orbifold (Kawamura; Hall–Nomura) usan $S^1/(Z_2\times Z_2')$. Nadie, hasta donde encontramos en esta búsqueda, ha calculado **la señal de ondas gravitacionales** de una fusión en una brana de un $S^1/(Z_2\times Z_2')$ warped. Esa es la laguna que este estudio identifica.

## 1.7 Cómo se vería en una onda gravitacional

Importante para no confundir el observable:

* La onda que detecta LIGO de una fusión es el **modo cero** (sin masa). Su frecuencia (chirp, ringdown) la fija la dinámica 4D de los agujeros negros, no la dimensión extra.
* Los modos KK son **gravitones masivos**. Un observador en la brana los ve como oscilaciones **tardías y casi monocromáticas** de frecuencia $f_n=m_nc/2\pi$ con decaimiento lento $\propto t^{-5/6}\sin(m_nt)$ (Seahra–Clarkson–Maartens 2005), **independientes de la masa del agujero negro**. No son "ecos" en el sentido de repeticiones del pulso; son líneas espectrales.
* "La energía que salta de un lado al otro": una fuente en nuestra brana excita los modos con $f_n(y_I)\neq0$; esos modos llegan a la brana sombra con amplitud $f_n(y_{II})$. Clarkson–Seahra (2007) muestran que **materia en la brana sombra** produce en nuestra brana un espectro discreto de alta frecuencia potencialmente detectable. En $S^1/(Z_2\times Z_2')$ la selección es más fuerte: los impares de tipo $(+,-)$ no cruzan en absoluto, los $(-,+)$ sólo existen del otro lado, y los pares $(+,+)$ cruzan libremente.
