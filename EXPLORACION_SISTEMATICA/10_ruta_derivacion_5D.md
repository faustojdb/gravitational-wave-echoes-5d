# Ruta de Derivación: De 5D a m_p/m_e = 6π⁵

## Fecha: 23 Enero 2026
## Estado: PLAN DE TRABAJO DEFINIDO

---

## PUNTO DE PARTIDA

Lo que sabemos con certeza:

1. **Lenz (1951)**: m_p/m_e ≈ 6π⁵ con 19 ppm de precisión
2. **Stefan-Boltzmann 3D**: σ = 2π⁵k⁴/(15h³c²) contiene π⁵ y 6=Γ(4)
3. **En D dimensiones**: aparece π^(D+1) en factores geométricos
4. **Klein Bottle Cosmology**: 6D = M₄ × K², χ(K²) = 6

## PREGUNTA CENTRAL

> ¿Si el universo tiene estructura 5D, la física térmica del universo
> temprano produce naturalmente 6π⁵ en los ratios de masa?

---

## PASO 1: Stefan-Boltzmann en D dimensiones

### Tipo: VERIFICABLE (matemática pura)

### Paper de referencia:
- Landsberg & De Vos, "The Stefan-Boltzmann constant in n-dimensional space"
- J. Phys. A: Math. Gen. 22 (1989) 1073-1084

### Tarea:
Derivar la fórmula generalizada:
```
σ_D = [constantes] × π^f(D) × Γ(g(D)) × ζ(D+1)
```

### Pregunta específica:
Para D=4 espacial (5D total): ¿Aparece π⁵ y factores relacionados con 6?

### Resultado esperado:
Fórmula explícita. Si no tiene π⁵, el camino se cierra aquí.

### Esfuerzo: ~2 horas

---

## PASO 2: Masas en teorías Kaluza-Klein

### Tipo: VERIFICABLE (física establecida)

### Papers originales:
- Kaluza (1921): "Zum Unitätsproblem der Physik"
- Klein (1926): "Quantentheorie und fünfdimensionale Relativitätstheorie"
- Overduin & Wesson (1997): "Kaluza-Klein Gravity" (review moderno)

### Fórmula conocida:
En Kaluza-Klein clásico:
```
m_n = n/R₅  (donde R₅ es radio de dimensión compacta, n = entero)
```

### Pregunta específica:
¿El ratio m_p/m_e puede expresarse en términos de geometría 5D?

### Resultado esperado:
Relación masa ↔ geometría, o descarte de este camino.

### Esfuerzo: ~4 horas

---

## PASO 3: Conexión térmica-masa

### Tipo: ESPECULATIVO pero guiado

### Hipótesis:
En el universo temprano (dominado por radiación), las masas se
"congelaron" durante transición de fase, heredando estructura
matemática de estadística de Bose-Einstein en 5D.

### Papers a revisar:
- Weinberg (1972): "Gravitation and Cosmology" - cosmología temprana
- Kolb & Turner: "The Early Universe" - transiciones de fase
- Papers sobre "electroweak phase transition" y origen de masas

### Pregunta específica:
¿Hay mecanismo conocido donde temperatura de congelamiento fije ratios?

### Resultado esperado:
Mecanismo existente o descarte de esta vía.

### Esfuerzo: ~4 horas

---

## PASO 4: QCD y origen de m_p

### Tipo: VERIFICACIÓN CRUZADA

### Contexto:
La masa del protón viene ~95% de energía de gluones (no de quarks).
QCD en lattice puede calcular m_p numéricamente.

### Paper clave:
- Dürr et al. (2008): "Ab initio determination of light hadron masses"
- Science 322, 1224

### Pregunta específica:
¿Las simulaciones QCD muestran alguna estructura con π⁵ o factores de 6?

### Resultado esperado:
Probablemente NO (QCD es muy compleja), pero verificar.

### Esfuerzo: ~2 horas

---

## CRITERIOS DE DECISIÓN

### ✅ ÉXITO (continuar):
- Paso 1 + Paso 2 conectan naturalmente a 6π⁵
- Sin parámetros libres ad-hoc
- La derivación es única (no hay muchas formas de llegar)

### ❌ FRACASO (abandonar):
- Cada paso introduce parámetros libres
- La conexión requiere ajustes numéricos
- Hay muchas formas alternativas de llegar al mismo número

### ❓ AMBIGUO (investigar más):
- La conexión existe pero requiere coincidencias adicionales
- Algunos pasos son naturales, otros no
- Necesita input de expertos en el área

---

## ORDEN ÓPTIMO

```
PASO 1 (Stefan-Boltzmann D-dim)
    ↓
    ¿π⁵ aparece naturalmente?
    ↓ SÍ                    ↓ NO
    ↓                       → STOP (coincidencia numérica)
    ↓
PASO 2 (Kaluza-Klein)
    ↓
    ¿Masas conectan con geometría 5D?
    ↓ SÍ                    ↓ NO
    ↓                       → STOP (no hay conexión)
    ↓
PASO 3 (Térmica-masa)
    ↓
    ¿Hay mecanismo de congelamiento?
    ↓ SÍ                    ↓ NO
    ↓                       → Paper especulativo
    ↓
PASO 4 (Verificación QCD)
    ↓
    ¿Consistente con lattice QCD?
    ↓ SÍ                    ↓ NO
    ↓                       → Revisar pasos anteriores
    ↓
PUBLICACIÓN
```

---

## RECURSOS NECESARIOS

### Papers (acceso requerido):
1. [ ] Landsberg & De Vos (1989) - Stefan-Boltzmann D-dim
2. [ ] Kaluza (1921) - original (en alemán, hay traducciones)
3. [ ] Klein (1926) - original
4. [ ] Overduin & Wesson (1997) - review Kaluza-Klein
5. [ ] Dürr et al. (2008) - lattice QCD
6. [ ] arXiv:2511.23447 - Klein Bottle Cosmology (ya revisado)

### Conocimientos:
- Cálculo en D dimensiones
- Funciones Gamma y Zeta
- Teoría de Kaluza-Klein básica
- Cosmología del universo temprano

---

## ESTIMACIÓN TOTAL

| Paso | Horas | Probabilidad de éxito |
|------|-------|----------------------|
| 1 | 2 | 80% (matemática directa) |
| 2 | 4 | 50% (puede no conectar) |
| 3 | 4 | 30% (especulativo) |
| 4 | 2 | 90% (verificación) |
| **Total** | **12** | **~20% de conexión completa** |

La probabilidad es baja, pero el payoff (explicar coincidencia de 73 años)
justifica el esfuerzo.

---

*Plan creado: 23 Enero 2026*
*Próximo paso: PASO 1 - Stefan-Boltzmann en D dimensiones*
