# EXTENSIÓN DOPPLER-KLEIN

## Resumen

Esta carpeta contiene la **extensión fundamental Doppler-Klein** del framework teórico, incorporando efectos de propagación relativista, elevación/decantación viscosa de átomos Klein, y algoritmos de limpieza de ruido basados en modos topológicos prohibidos.

## 🌟 Características Principales

### 1. **Efectos Doppler Klein**
- Propagación relativista en topología Klein bottle 5D
- Shifts de frecuencia por velocidades peculiares
- Correcciones dependientes de escala física

### 2. **Elevación/Decantación Viscosa**
- Átomos Klein "elevándose" temporalmente a 5D activa
- Decantación por "gravedad topológica" 
- Medio viscoso con amortiguación escalada

### 3. **Ecuaciones de Segundo Orden**
- Dinámica completa: [ε, dε/dt, h, dh/dt]
- Aceleración de deformación Klein
- Inercia en proyección 5D → 4D

### 4. **Algoritmo Denoising**
- Identificación de modos prohibidos
- Sustracción de componentes impar/par incorrectas
- Mejora SNR en eventos subthreshold

## 📁 Archivos

### Scripts Principales
- **`klein_master_equation_doppler_extension.py`**: Versión inicial con extensión completa
- **`klein_master_equation_doppler_extension_improved.py`**: ⭐ **Versión mejorada production-ready**
- **`subthreshold_doppler_analysis.py`**: Análisis especializado para eventos subthreshold
- **`test_doppler_extension.py`**: Tests de funcionalidad y validación
- **`compare_versions.py`**: Comparación entre versión original y mejorada

### Documentación
- **`README.md`**: Este archivo
- **`doppler_init_conv.md`**: Conversación inicial sobre fundamentos Doppler

## ⭐ VERSIÓN MEJORADA (v2.0)

### Mejoras Implementadas

**1. 🔧 Manejo Flexible de Unidades**
```python
# Auto-conversión de unidades
klein = KleinMasterEquationDopplerExtensionImproved(distance_unit='Mpc')
result = klein.solve_extended_evolution_improved(E=2.5, L=1000)  # 1000 Mpc automático
```

**2. 🌊 Doppler Asimétrico con Klein Twist**
```python
# Incorpora efectos de no-orientabilidad Klein bottle
factor = klein.calculate_doppler_shift_asymmetric(v, L, direction, par_impar)
# par_impar crea asimetría por topología twist
```

**3. 💧 Viscosidad y Segundo Orden Completos**
```python
# Sistema completo: [ε, dε/dt, h, dh/dt]
# Viscosidad explícita: -η(L) dh/dt
# Segundo orden: d²ε/dt², d²h/dt²
```

**4. ⚡ Solver Adaptativo Optimizado**
```python
# Múltiples modos de performance
klein = KleinMasterEquationDopplerExtensionImproved(performance_mode='adaptive')
# 'adaptive' (solve_ivp RK45), 'fixed' (odeint), 'fast' (euler)
```

**5. 🔍 Validación y Logging Integrados**
```python
# Asserts automáticos para conservación topológica
assert 0 <= epsilon <= epsilon_max
assert topology_conserved == True
# Logging detallado con timestamps
```

**6. 📊 Visualización y Debug Mejorados**
```python
# Plot automático para debug
result = klein.solve_extended_evolution_improved(E, L, auto_plot=True)
```

## 🚀 Uso Rápido

### Test Básico
```bash
python test_doppler_extension.py
```

### Comparar Versiones
```bash
python compare_versions.py  # ⭐ Demuestra todas las mejoras
```

### Análisis Subthreshold
```bash
python subthreshold_doppler_analysis.py
```

### Uso Programático (Versión Original)
```python
from klein_master_equation_doppler_extension import KleinMasterEquationDopplerExtension

# Inicializar
klein = KleinMasterEquationDopplerExtension()

# Análisis con Doppler (conversión manual)
result = klein.solve_extended_evolution(
    E_initial=2.5,     # M☉c²
    L=1000*3.086e19,   # 1000 Mpc convertido a km manualmente
    v_peculiar=0.1     # 0.1c receding
)

print(f"Doppler shift: {result['doppler_shift_hz']:.4f} Hz")
print(f"Max elevación: {result['max_elevation']:.1f} km")
```

### ⭐ Uso Programático (Versión Mejorada - RECOMENDADO)
```python
from klein_master_equation_doppler_extension_improved import KleinMasterEquationDopplerExtensionImproved

# Inicializar con configuración flexible
klein = KleinMasterEquationDopplerExtensionImproved(
    distance_unit='Mpc',          # Auto-conversión de unidades
    performance_mode='adaptive',   # Solver optimizado
    enable_logging=True           # Logging detallado
)

# Análisis con Doppler (mucho más simple)
result = klein.solve_extended_evolution_improved(
    E_initial=2.5,     # M☉c²
    L=1000,           # 1000 Mpc (conversión automática)
    v_peculiar=0.1,   # 0.1c receding
    auto_plot=True    # Plot automático para debug
)

print(f"Doppler shift: {result['doppler_shift_hz']:.4f} Hz")
print(f"Max elevación: {result['max_elevation']:.1f} km")
print(f"Solver usado: {result['solver_used']}")
print(f"Topología conservada: {result['topology_conserved']}")
```

## 🔬 Fundamentos Teóricos

### Sin Parámetros Ad Hoc
Todo deriva del framework Klein existente:

- **Escalado dinámico**: γ(L) ∝ (L/R₅D)^α (de multiscale theory)
- **Modos par/impar**: De topología Klein bottle no-orientable
- **Viscosidad**: Extensión natural de amortiguación γ
- **Doppler**: Relatividad estándar en 5D Klein

### Ecuación Maestra Extendida
```
Sistema: [ε, dε/dt, h, dh/dt]

dε/dt = -γ(L)ε + κ(L)E(t)(ε_max - ε) sin(2πf₀t + φ_Doppler) × par_impar × coupling_elevation

d²h/dt² = F_excitación - η(L)dh/dt - g_topo h
```

### Parámetros Nuevos (Derivados)
- **η_base = 10.0**: Viscosidad base (∝ γ_base)
- **g_topo = 5.0**: Gravedad topológica (preserva Klein bottle)
- **α_visc = 4.0**: Exponente viscosidad (como thermal suppression)

## 📊 Predicciones y Tests

### Observacionales
1. **Ecos Doppler-retardados**: ~64ms ± δt_Doppler
2. **Correlaciones velocidad-shift**: v_peculiar vs Δf observado
3. **Asimetría direccional**: Diferencias approach vs recede
4. **Mejora denoising**: 20-50% reducción ruido subthreshold

### Falsificables
- Si correlación v-Doppler < 3σ → extensión incorrecta
- Si denoising empeora SNR → algoritmo defectuoso  
- Si elevación viola ε_max → física inconsistente

## 🔄 Relación con Framework Base

### Hereda de `teoria_refinada/`
- Constantes fundamentales (R₅D, f₀, ε_max)
- Escalado multi-escala α_grav, α_em, α_thermal
- Regímenes energéticos (thresholds extrema/relajada)
- Metodología estadística robusta

### Extiende con
- Segundo orden temporal (aceleración)
- Proyección 5D-4D (elevación h)
- Efectos relativistas (Doppler)
- Algoritmos aplicados (denoising)

### Compatible con
- Todos los análisis existentes
- Scripts de `teoria_refinada/scripts/`
- Datos de `teoria_refinada/datos/`
- Metodología MCMC/estadística

## ⚠️ Limitaciones y Consideraciones

### Computacionales
- Sistema 4D requiere más tiempo computacional
- ODE stiff puede necesitar tolerancias ajustadas
- Memoria para arrays extendidos [ε, dε/dt, h, dh/dt]

### Físicas
- Velocidades peculiares > 0.3c pueden violar aproximaciones
- Escalas L << R₅D o L >> 10⁶ R₅D pueden ser inestables
- Parámetros viscosos requieren calibración con data real

### Validación
- Extensión teóricamente consistente pero necesita validación observacional
- Algoritmo denoising es prototipo (no production-ready)
- Comparación con baseline necesaria para cada dataset

## 🎯 Próximos Pasos

### Desarrollo
1. **Optimización numérica**: Solver más robusto para sistema stiff
2. **Calibración parámetros**: η, g_topo con data real
3. **Extensión 3D**: Análisis espacial completo (no solo temporal)

### Validación
1. **Aplicar a GWTC-3 completo**: 70+ eventos BBH
2. **Cross-check con PTA**: NANOGrav 15-year real
3. **Búsqueda correlaciones**: v_peculiar en catálogos existentes

### Publicación
1. **Paper extensión**: "Doppler Effects in Klein Bottle Topology"
2. **Metodología denoising**: "Topological Mode Filtering for GW Data"
3. **Aplicaciones**: "Klein-Enhanced Subthreshold Event Detection"

## 📚 Referencias

### Framework Base
- `../teoria_refinada/RESUMEN_FINAL_REFINAMIENTO_KLEIN_THEORY.md`
- `../KLEIN_THEORY_UNIFIED_FRAMEWORK.md`

### Fundamentos Doppler
- `doppler_init_conv.md` - Conversación desarrollo
- Relatividad especial en 5D Klein
- Propagación ondas en medios discretos

### Topología Klein
- Klein bottle no-orientable: g_AB(x^μ, -y) = g_AB(x^μ, y)
- Modos par/impar de twist Möbius
- Proyección 5D → 4D temporal

---

**Status**: ✅ Extensión fundamental completada  
**Compatibilidad**: Klein Theory Framework v3.0+  
**Testing**: Tests básicos pasados, validación pendiente  
**Fecha**: 27 de julio de 2025  

*Desarrollado por Klein Theory Extension Team*