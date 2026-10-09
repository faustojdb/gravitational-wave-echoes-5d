# 5. La ventana submilimétrica: qué puede vivir entre 38.6 µm y la longitud de Planck

Etiquetas: **[T]** derivación, **[M]** supuesto de modelo, **[D]** dato publicado. Números en `4_Resultados/numeros_ventana_submm.md`, generados por `3_Codigo/numeros_ventana_submm.py` sin parámetros libres.

## 1. Dónde empieza la ventana y por qué

**[D]** La ley 1/r² está confirmada a intensidad gravitacional hasta λ = 38.6 µm (Lee, Adelberger, Cook, Fleischer y Heckel 2020, *PRL* 124, 101101). Por debajo no hay medida de la rigidez del espacio-tiempo.

**[T]** Con G, c, ħ y Λ se construyen exactamente dos longitudes: ℓ_P = 1.6×10⁻³⁵ m y L_Λ = 1/√Λ = 9.6×10²⁵ m (§3 de `04_modelo_elastico.md`). Toda longitud intermedia **sin constantes nuevas** es de la forma ℓ_P^a L_Λ^(1−a). Hay una sola con significado físico independiente: la que resulta de tratar la pretensión como densidad de energía cuántica. La densidad ρ_Λ = Λc⁴/8πG define una energía E_Λ = (ρ_Λ ħ³c³)^{1/4} y una longitud

$$L_{\rm mix} = \frac{\hbar c}{E_\Lambda} = \left(\frac{8\pi G\hbar}{\Lambda c^3}\right)^{1/4} = (8\pi)^{1/4}\sqrt{\ell_P\,L_\Lambda}.$$

Es la **media geométrica** de las dos escalas extremas, con un factor (8π)^{1/4} = 2.24 que sólo depende de la convención 8πG de la ecuación de Einstein:

| | valor |
|---|---|
| √(ℓ_P L_Λ) | 39.3 µm |
| E_Λ = ρ_Λ^{1/4} | 2.24 meV |
| L_mix = ħc/E_Λ | 88.1 µm |
| cota experimental actual | 38.6 µm |

**[T]** Por lo tanto la ventana submilimétrica no es un intervalo arbitrario: empieza exactamente en la única longitud que la física conocida produce al combinar su término más pequeño con su término más grande. El cociente entre la cota de laboratorio y √(ℓ_P L_Λ) es 0.98.

**[D] Qué es y qué no es esta coincidencia.** La cota de 38.6 µm es el alcance actual de un aparato; no mide nada en esa escala, sólo dice que hasta ahí no hay desviación. Que coincida con √(ℓ_P L_Λ) es, en parte, diseño: el programa Eöt-Wash se planteó explícitamente alcanzar la "longitud de la energía oscura" de ~85 µm (Adelberger, Heckel y Nelson 2003, *Ann. Rev. Nucl. Part. Sci.* 53, 77; ⚠️ cita de memoria, verificar sección). Lo que queda establecido es sólo esto: **los experimentos acaban de cruzar L_mix y están a un factor 2 de √(ℓ_P L_Λ)**, y por debajo no hay ninguna otra longitud que la teoría conocida señale hasta ℓ_P, treinta órdenes de magnitud más abajo. Si existe una constante nueva en la ventana, ya no tiene dónde esconderse "naturalmente" salvo en ese factor 2 o en un lugar sin motivación.

## 2. Qué predice una dimensión extra en la ventana para la ley de Newton

**[T]** Si el gravitón se propaga en una dimensión extra compacta y la materia está confinada a una pared (supuesto [M] estándar de los mundos brana), el potencial entre dos masas en la pared es la suma sobre la torre KK:

$$V(r) = -\frac{G m_1 m_2}{r}\left[1 + \sum_{n\ge1} c_n\, e^{-m_n r}\right],\qquad c_n = \frac{|f_n(y_{\rm pared})|^2}{|f_0|^2},$$

donde f_n son las funciones de modo normalizadas en la dimensión extra. Esto es exactamente lo que calcula `modos_paridad_topografias.py`, ahora aplicado a la gravedad estática. Resultados, por topografía:

| Topografía (radio del círculo de cubrimiento R; longitud física del intervalo L) | f_n en nuestra pared | masas | c_n | forma de la corrección |
|---|---|---|---|---|
| S¹ | e^{iny/R}, todos de módulo 1 | n/R | 2 (±n) | 1 + 2Σe^{−nr/R}: Yukawa con **α = 2, λ = R** (Kehagias–Sfetsos 2000, α = 2n para Tⁿ) |
| S¹/Z₂, L = πR | √(2/πR) cos(ny/R); f_0 = 1/√(πR) | n/R | 2 | idéntico: α = 2, λ = R = L/π |
| S¹/(Z₂×Z₂′), gravitón (+,+), L = πR/2 | √(4/πR) cos(2ny/R); f_0 = √(2/πR) | 2n/R | 2 | α = 2, λ = R/2 = L/π |
| S¹/(Z₂×Z₂′), sector (−,+) | sin((2n+1)y/R) → 0 en y = 0 | (2n+1)/R | **0** | no contribuye a nuestra ley de Newton |
| RS2 warped, radio AdS ℓ, r ≫ ℓ | continuo | — | — | 1 + 2ℓ²/3r²: **potencia**, no Yukawa (Garriga–Tanaka 2000) |

Tres consecuencias derivadas:

1. **La ley de Newton en nuestra pared no distingue el orbifold con paridad del intervalo simple.** Escrita en función de la longitud física del intervalo L, la corrección es α = 2, λ = L/π en los dos casos. La selección de paridad por lado es **invisible** para los experimentos de torsión con fuentes y detectores en nuestra pared.
2. **Donde sí se distingue es en la materia de la otra pared.** Una masa en la pared sombra (y = πR/2) actúa sobre la nuestra con factor Σ f_n(0) f_n(πR/2)/f_0² = 1 + 2Σ(−1)ⁿ e^{−2nr/R}, serie **alternante** porque cos(nπ) = (−1)ⁿ. Sumando la geométrica con x = e^{−2r/R}:

   $$\text{propio: } \frac{1+x}{1-x},\qquad \text{sombra: } \frac{1-x}{1+x}.$$

   | r/R | factor propio | factor sombra |
   |---|---|---|
   | 0.05 | 19.0 | 0.05 |
   | 0.35 | 3.0 | 0.33 |
   | 1.15 | 1.22 | 0.82 |
   | ≫ 1 | 1 | 1 |

   A distancias cortas nuestra propia materia gravita en 5D (el factor crece como R/r, que es la ley 1/r² en 5D) mientras que la materia de la otra pared **desaparece** (su distancia a través del bulk, πR/2, domina). A distancias largas ambas gravitan igual. Ésa es la "permeabilidad" derivada de la ventana: la materia sombra es, para nosotros, masa que gravita a larga distancia y se apaga a corta distancia. Los sectores (−,+) que la pared sombra pueda excitar no llegan jamás a la nuestra. Nada de esto requiere un parámetro: sólo R.
3. **Una sola medida fija todo.** Si un experimento de torsión detectara una Yukawa con α = 2, el valor de λ daría R; con λ_eff = R/2 en el caso con paridad no hay forma de saber desde nuestra pared cuál de los dos orbifolds es, salvo midiendo materia sombra. Si detectara α ≠ 2 o una ley de potencia, el modelo sería otro (más dimensiones: α = 2n; esfera: α = n+1; warped: potencia).

## 3. Qué implica la ventana para todo lo demás

**[T] Frecuencias.** El primer modo KK tiene f₁ = c/2πR. Para R < 38.6 µm, f₁ > 1.24 THz, es decir m₁c² > 5 meV. Está **nueve órdenes de magnitud** por encima de la banda de LIGO. Ningún detector de ondas gravitacionales existente o proyectado accede a la ventana. Esto cierra la discusión sobre LIGO para cualquier dimensión extra plana compatible con el laboratorio: la ventana sólo se prueba con gravedad de corto alcance.

**[T] Escala fundamental.** Con una dimensión extra plana de radio R donde sólo propaga la gravedad, la escala de Planck fundamental cumple M_*³ R = M_P² (hasta factores 2π). Para R = 38.6 µm, M_* ≈ 9×10⁸ GeV; para R = 1 µm, 3×10⁹ GeV. Está muy por encima del alcance de colisionadores y de las cotas de enfriamiento de supernovas y estrellas de neutrones, que sólo muerden cuando M_* ~ TeV. **Una dimensión plana en la ventana no está excluida por ninguna observación astrofísica ni de altas energías; sólo por el laboratorio, y sólo hasta 38.6 µm.**

**[T] Rigidez y pretensión.** En la ventana, la rigidez efectiva a distancias r < R pasa de c⁴/8πG a su valor 5D, K₅ = K·(πR) en el intervalo simple: el tejido es más blando cuanto más adentro se mira, con la razón fijada por R. La pretensión Λ no interviene: L_Λ/R ≳ 10³⁰.

## 4. Qué está medido en la ventana y qué no

**[D]** Panorama experimental (Adelberger, Heckel y Nelson 2003; Lee et al. 2020; ⚠️ los límites por debajo de 10 µm se citan de memoria de ese review y deben verificarse antes de usarse):

| Rango | Técnica | Qué acota |
|---|---|---|
| 38.6 µm – 3 mm | balanza de torsión, atractor rotante | α de orden 1 excluido (intensidad gravitacional) |
| 0.1 – 10 µm | fuerza de Casimir entre superficies | sólo α ≳ 10³–10⁸, por la fuerza electromagnética de fondo |
| 1 nm – 0.1 µm | dispersión de neutrones | sólo α ≳ 10²⁰ |
| < 1 nm | nada a intensidad gravitacional | — |

Es decir: la gravedad propiamente dicha está medida sólo hasta 38.6 µm; por debajo, las cotas son sobre fuerzas mucho más intensas que la gravedad y no restringen una dimensión extra con α = 2.

## 5. Síntesis

- **[T]** La ventana empieza en la única longitud que la física conocida construye entre Planck y Hubble, √(ℓ_P L_Λ) ≈ 39 µm, y los experimentos están a un factor 2 de ella.
- **[T]** Una dimensión extra en la ventana predice una corrección Yukawa a la ley de Newton con **α = 2 exacto** y λ = L/π, idéntica con o sin selección de paridad; la paridad sólo se manifiesta en la gravedad de la materia sombra, que se apaga a distancias r ≲ R con el factor (1−x)/(1+x).
- **[T]** Sus frecuencias KK están en los terahercios: fuera de la gravedad ondulatoria. La ventana se prueba con balanzas, no con LIGO.
- **[T]** No hay cota astrofísica ni de colisionadores: M_* ≈ 10⁹ GeV.
- **[D]** Lo único que falta es un factor 2 en el alcance de los experimentos de torsión para cruzar √(ℓ_P L_Λ). Si no aparece nada ahí, ya no queda ninguna longitud señalada por la teoría conocida entre 20 µm y la de Planck.

Lo que esto significa para el proyecto: la hipótesis de "una dimensión más con filtro de paridad" es compatible con todo lo observado **si y sólo si** vive en la ventana, y entonces su única predicción accesible es α = 2 en la ley de Newton por debajo de 40 µm. Eso no se puede probar con datos de GWOSC. Se puede, en cambio, seguir la literatura de Eöt-Wash y experimentos sucesores, cuyo próximo factor 2 decide la cuestión.
