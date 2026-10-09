# Números de la materia sombra (generados por `3_Codigo/numeros_materia_sombra.py`)

## Verificación: suma KK = suma de imágenes 5D (S¹ de radio R; nuestra pared y = 0, pared sombra y = πR)

| r/R | KK propio 1+2Σe^{−nr/R} | imágenes d=0 | coth(r/2R) | KK sombra 1+2Σ(−1)ⁿe^{−nr/R} | imágenes d=πR | tanh(r/2R) |
|---|---|---|---|---|---|---|
| 0.05 | 40.008333 | 40.008333 | 40.008333 | 0.024995 | 0.024995 | 0.024995 |
| 0.2 | 10.033311 | 10.033311 | 10.033311 | 0.099668 | 0.099668 | 0.099668 |
| 0.5 | 4.082988 | 4.082988 | 4.082988 | 0.244919 | 0.244918 | 0.244919 |
| 1 | 2.163953 | 2.163953 | 2.163953 | 0.462117 | 0.462117 | 0.462117 |
| 2 | 1.313035 | 1.313034 | 1.313035 | 0.761594 | 0.761593 | 0.761594 |
| 5 | 1.013567 | 1.013565 | 1.013567 | 0.986614 | 0.986612 | 0.986614 |
| 10 | 1.000091 | 1.000086 | 1.000091 | 0.999909 | 0.999904 | 0.999909 |

Las tres columnas de cada bloque coinciden a 10⁻⁶: la suma de modos es exactamente coth(r/2R) para materia propia y tanh(r/2R) para materia sombra.

## Permeabilidad gravitacional P(r) = tanh(πr/2L) en función de la separación física L entre paredes

| r/L | P(r) = V_sombra/V_newton | V_propio/V_newton = coth(πr/2L) | razón sombra/propio = tanh² |
|---|---|---|---|
| 0.01 | 0.0157 | 63.6672 | 0.0002 |
| 0.1 | 0.1558 | 6.4185 | 0.0243 |
| 0.25 | 0.3737 | 2.6761 | 0.1396 |
| 0.5 | 0.6558 | 1.5249 | 0.4301 |
| 1 | 0.9172 | 1.0903 | 0.8412 |
| 2 | 0.9963 | 1.0037 | 0.9926 |
| 3 | 0.9998 | 1.0002 | 0.9997 |
| 5 | 1.0000 | 1.0000 | 1.0000 |

## Límites analíticos

| Régimen | materia propia | materia sombra |
|---|---|---|
| r ≪ L | V → −2GmR/r² = −G₅m/(πr²) (Newton 5D) | V → −Gm_s/(2R) = −πGm_s/(2L): **finito** |
| r ≫ L | V → −Gm/r [1 + 2e^{−πr/L}] | V → −Gm_s/r [1 − 2e^{−πr/L}] |
| fuerza, r ≪ L | F → 4GmR/r³ (∝ 1/r³) | F → −G m_s r/(12R³) = −π³G m_s r/(12L³): restauradora, ∝ r, → 0 |

## Modos masivos no radiados (evanescencia)

| fuente | ħω | m₁c² para R = 38.6 µm | ω/m₁ |
|---|---|---|---|
| fusión BBH, 250 Hz | 1.03e-12 eV | 5.11e-03 eV | 2.0e-10 |
| BNS, 2 kHz | 8.27e-12 eV | 5.11e-03 eV | 1.6e-09 |
| radio KK f₁ = c/2πR | 5.11e-03 eV | 5.11e-03 eV | 1.0e+00 |

Un modo de masa m sólo se propaga si ħω > mc²; para toda fuente astrofísica ω/m₁ ≲ 10⁻⁹, de modo que las ondas gravitacionales de materia sombra son **exactamente** las del modo cero, con la forma de onda de la relatividad general 4D.

## Si la materia sombra fuera toda la materia oscura

| magnitud | valor | origen |
|---|---|---|
| Ω_c h² (Planck 2018) | 0.120 | dato |
| Ω_b h² (Planck 2018) | 0.0224 | dato |
| m_s / m_b necesario | 5.36 | cociente |

