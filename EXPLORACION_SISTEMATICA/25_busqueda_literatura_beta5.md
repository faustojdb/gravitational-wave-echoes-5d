# Búsqueda en Literatura: ¿β(5) en QCD?

**Fecha**: 25 Enero 2026
**Propósito**: Verificar si β(5) aparece en cálculos de física QCD
**Resultado**: NEGATIVO - No encontrado

---

## 1. LA PREGUNTA

Si T_c/m_e ≈ π⁵, y β(5) = 5π⁵/1536 es la única función en argumento 5 que contiene π⁵, entonces:

> **¿Aparece β(5) en algún cálculo publicado de QCD o transiciones de fase?**

---

## 2. LO QUE BUSCAMOS

| Término | Contexto |
|---------|----------|
| "Dirichlet beta function" + QCD | Conexión directa |
| β(5) + thermodynamics | En termodinámica |
| ζ(5) + QCD pressure | En presión a alta T |
| Antiperiodic + fermion + Casimir | Condiciones de borde |
| Fermi-Dirac + QCD crossover | Integrales térmicas |

---

## 3. LO QUE ENCONTRAMOS

### 3.1 Física térmica estándar usa η(s), NO β(s)

```
Bosones:   condición periódica     → ζ(s)
Fermiones: condición antiperiódica → η(s) = (1 - 2^(1-s))ζ(s)
```

**Verificado numéricamente:**
```
η(5) = 0.9721...  ← IRRACIONAL (no tiene π⁵)
ζ(5) = 1.0369...  ← IRRACIONAL (no tiene π⁵)
β(5) = 0.9962...  = 5π⁵/1536  ✓ TIENE π⁵
```

### 3.2 β(s) requiere condiciones especiales

La función β(s) = Σ(-1)^n/(2n+1)^s suma sobre IMPARES solamente.

Esto NO es lo que hacen los fermiones estándar (que suman alternadamente sobre TODOS los enteros).

Para obtener β(s) necesitaríamos:
- Restricción a modos impares solamente
- O equivalente: período 4 efectivo en lugar de 2

### 3.3 En QCD a alta temperatura

De la literatura (arXiv:hep-ph/0211321, arXiv:2002.10188):

- La presión se conoce hasta orden g⁶ ln(1/g)
- Aparecen ζ(3), ζ(5) en correcciones de loops altos
- ζ(5) aparece pero como número irracional
- **NO se encontró β(5) ni 5π⁵/1536**

### 3.4 En efecto Casimir fermiónico

De la literatura sobre Casimir con fermiones:

- Antiperiódico usa ζ(s, 1/2) = (2^s - 1)ζ(s)
- Esto da η(s), no β(s)
- **NO se encontró β(s) en Casimir fermiónico estándar**

---

## 4. RESULTADO DE LA BÚSQUEDA

```
┌─────────────────────────────────────────────────────────────┐
│                     RESULTADO: NEGATIVO                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  β(5) = 5π⁵/1536 NO aparece en:                            │
│                                                             │
│  ✗ Cálculos de presión QCD a alta temperatura              │
│  ✗ Termodinámica del plasma quark-gluón                    │
│  ✗ Efecto Casimir fermiónico estándar                      │
│  ✗ Integrales de Fermi-Dirac en QFT térmica               │
│                                                             │
│  La conexión β(5) ↔ T_c NO ESTÁ ESTABLECIDA               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 5. IMPLICACIONES

### Lo que sigue siendo válido:

1. **Observación numérica**: T_c/m_e ≈ π⁵ (error 0.08%)
2. **Matemática**: β(5) = 5π⁵/1536 contiene π⁵
3. **Geometría**: Volumen 5D Klein = π⁵

### Lo que NO está establecido:

1. **Conexión física** entre β(5) y QCD
2. **Mecanismo** que introduzca β(s) en lugar de η(s)
3. **Derivación** de T_c/m_e = π⁵ desde primeros principios

### Conclusión:

> **La estructura matemática es elegante pero la conexión física es especulativa.**
>
> Sin un mecanismo que produzca β(s) en física de QCD, la relación T_c/m_e ≈ π⁵ puede ser coincidencia numérica.

---

## 6. FUENTES CONSULTADAS

1. [Perturbative Thermal QCD: Formalism and Applications](https://arxiv.org/abs/2002.10188)
2. [The pressure of hot QCD up to g⁶ ln(1/g)](https://arxiv.org/abs/hep-ph/0211321)
3. [Fermionic Casimir effect](https://www.academia.edu/6084238)
4. [Zeta function regularization - Wikipedia](https://en.wikipedia.org/wiki/Zeta_function_regularization)
5. [Dirichlet beta function - Wikipedia](https://en.wikipedia.org/wiki/Dirichlet_beta_function)
6. [Finite-Temperature Field Theory (Kapusta & Gale)](https://library.oapen.org/handle/20.500.12657/64016)
7. [Basics of Thermal Field Theory (Laine)](http://laine.itp.unibe.ch/basics.pdf)

---

## 7. POSIBLES DIRECCIONES FUTURAS

Si se quisiera establecer la conexión, habría que:

1. **Buscar escenarios** donde β(s) aparezca naturalmente:
   - ¿Sistemas con simetría especial que restrinja a modos impares?
   - ¿Dimensiones compactas con identificación tipo Klein?
   - ¿Teorías con estructura de período 4?

2. **Calcular explícitamente** si alguna cantidad en QCD tiene β(5):
   - Susceptibilidades quirales
   - Correladores a temperatura finita
   - Correcciones no perturbativas

3. **Consultar expertos** en QCD térmica sobre esta posibilidad.

---

*"Un resultado negativo honesto es mejor que una conexión forzada."*

---

**Estado final**: La hipótesis β(5) ↔ T_c permanece ESPECULATIVA.
