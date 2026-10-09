# 3. Predicción común a todas las variantes (independiente del modelo concreto)

Separación de niveles exigida por `CLAUDE.md`.

## (a) Teorema

En cualquier espacio-tiempo 4D × (dimensión extra compacta o con borde), toda perturbación gravitacional se descompone en un modo sin masa más una torre de modos masivos $m_n$ fijados **sólo** por la geometría de la dimensión extra (no por la fuente). Esto vale para $S^1$, $S^1/Z_2$, $S^1/(Z_2\times Z_2')$, botella de Klein, Möbius y para el caso warped. Lo que cambia entre topografías es (i) el espaciado de la torre y (ii) qué modos tienen amplitud no nula en el punto de la dimensión extra donde está la fuente y el detector.

Consecuencia observable común: si alguno de esos modos masivos es excitado por una fusión, en el detector aparece una oscilación de frecuencia $f_n = m_n c/2\pi$ **igual para todos los eventos**, porque $m_n$ no depende de la masa de los agujeros negros. Para una perturbación masiva en un fondo de agujero negro la señal tardía decae como $t^{-5/6}\sin(m_nt)$ (Seahra–Clarkson–Maartens 2005, con referencia a los resultados clásicos de campos masivos en Schwarzschild), es decir mucho más lento que el ringdown.

## (b) Supuestos de modelo (lo que varía)

| Supuesto | Qué fija | Quién lo necesita |
|---|---|---|
| Topografía plana vs. warped | espaciado de la torre ($n/R$ vs. $x_nke^{-kL}$) | todos |
| Dos paredes inequivalentes | qué paridades se anulan en cada lado | sólo la hipótesis de selección por lado |
| Brana con tensión | la existencia del warping | sólo la versión observable en banda LIGO |
| Cuerda negra entre branas | cota de estabilidad $f_1>0.43c^3/2\pi GM$ y razones $f_n/f_1$ de ceros de $J_1$ | sólo ese modelo |

## (c) Datos y cotas ya publicadas

- Tests de laboratorio de la ley $1/r^2$: $\lambda>38.6\ \mu$m excluido (Lee et al. 2020). Con topografía plana esto empuja $f_1$ por encima de $10^{12}$ Hz: **no observable**.
- GW170817: $D=4.02^{+0.07}_{-0.10}$, apantallamiento $>20$ Mpc (Pardo et al. 2018); radio AdS$_5$ $<0.535$ Mpc (Visinelli et al. 2018). Restringen la fuga del modo cero, no la existencia de modos masivos.
- GWTC-3: búsqueda de ecos negativa (LVK 2021); límites de amplitud de transitorios en el segundo posterior a la fusión (Miani et al. 2023).

## Lo que se va a buscar en los datos (y por qué es lo mínimo)

Una **línea tardía a frecuencia fija, común a todos los eventos, no proporcional a la masa del remanente**. Es la única firma que comparten todas las variantes de (b). No se asume frecuencia ni modelo. El protocolo está en `5_Datos_Reales/PROTOCOLO.md`.

Si no aparece, el resultado acota la amplitud relativa de cualquier modo masivo excitable en 20–1800 Hz, con independencia de la topografía. Si aparece, recién entonces tendría sentido discriminar topografías (por las razones $f_n/f_1$ y por qué paridades faltan).
