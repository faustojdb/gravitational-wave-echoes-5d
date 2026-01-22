#!/usr/bin/env python3
"""
ANÁLISIS NUMÉRICO DEL RADIO FUNDAMENTAL KLEIN
Investigación de coincidencias y relaciones numéricas para R ≈ 8400 km
"""

import numpy as np
import json
from typing import Dict, List, Tuple
import matplotlib.pyplot as plt

# ============================================================================
# CONSTANTES FUNDAMENTALES
# ============================================================================

# Valor problemático Klein
R_KLEIN_KM = 8400  # km
R_KLEIN_M = 8.4e6  # metros
R_KLEIN_VALUE = 8.4  # número puro para análisis

# Constantes físicas fundamentales (SI units)
CONSTANTS = {
    # Escalas de longitud fundamentales
    'l_Planck': 1.616255e-35,  # m
    'r_Bohr': 5.29177210903e-11,  # m
    'lambda_Compton_e': 2.42631023867e-12,  # m (electrón)
    'lambda_Compton_p': 1.32140985539e-15,  # m (protón)
    'r_electron_classical': 2.8179403262e-15,  # m
    
    # Otras constantes
    'c': 299792458,  # m/s
    'h': 6.62607015e-34,  # J⋅s
    'hbar': 1.054571817e-34,  # J⋅s
    'G': 6.67430e-11,  # m³/(kg⋅s²)
    'k_B': 1.380649e-23,  # J/K
    'e': 1.602176634e-19,  # C
    
    # Masas
    'm_electron': 9.1093837015e-31,  # kg
    'm_proton': 1.67262192369e-27,  # kg
    
    # Escalas cosmológicas
    'R_Hubble': 4.4e26,  # m (radio del universo observable)
    'H_0': 2.2e-18,  # Hz (constante de Hubble)
    'Lambda': 1.1e-52,  # m^-2 (constante cosmológica)
}

# Constantes matemáticas
MATH_CONSTANTS = {
    'pi': np.pi,
    'e': np.e,
    'phi': (1 + np.sqrt(5))/2,  # golden ratio
    'sqrt_2': np.sqrt(2),
    'sqrt_3': np.sqrt(3),
    'alpha': 1/137.035999084,  # constante de estructura fina
}

# ============================================================================
# FUNCIONES DE ANÁLISIS
# ============================================================================

def analyze_direct_ratios():
    """Analiza ratios directos entre R_Klein y constantes fundamentales."""
    
    print("\n" + "="*70)
    print("ANÁLISIS DE RATIOS DIRECTOS")
    print("="*70)
    
    results = {}
    
    for name, value in CONSTANTS.items():
        if 'l_' in name or 'r_' in name or 'lambda' in name or 'R_' in name:
            ratio = R_KLEIN_M / value
            log_ratio = np.log10(ratio) if ratio > 0 else None
            
            results[name] = {
                'value': value,
                'ratio': ratio,
                'log_ratio': log_ratio
            }
            
            print(f"\n{name}:")
            print(f"  Valor: {value:.3e} m")
            print(f"  R_Klein/{name} = {ratio:.3e}")
            if log_ratio:
                print(f"  log₁₀(ratio) = {log_ratio:.2f}")
                
                # Buscar si el logaritmo está cerca de un entero
                nearest_int = round(log_ratio)
                diff = abs(log_ratio - nearest_int)
                if diff < 0.1:
                    print(f"  ⚠️  Cerca de 10^{nearest_int} (diff: {diff:.3f})")
    
    return results


def analyze_mathematical_patterns():
    """Busca patrones matemáticos en el valor 8.4."""
    
    print("\n" + "="*70)
    print("PATRONES MATEMÁTICOS EN 8.4")
    print("="*70)
    
    patterns = {}
    
    # Relaciones con constantes matemáticas
    for name, const in MATH_CONSTANTS.items():
        patterns[f"8.4/{name}"] = R_KLEIN_VALUE / const
        patterns[f"8.4*{name}"] = R_KLEIN_VALUE * const
        patterns[f"{name}/8.4"] = const / R_KLEIN_VALUE
        
    # Potencias y raíces
    patterns['8.4²'] = R_KLEIN_VALUE ** 2
    patterns['√8.4'] = np.sqrt(R_KLEIN_VALUE)
    patterns['8.4³'] = R_KLEIN_VALUE ** 3
    patterns['∛8.4'] = R_KLEIN_VALUE ** (1/3)
    
    # Logaritmos
    patterns['ln(8.4)'] = np.log(R_KLEIN_VALUE)
    patterns['log₁₀(8.4)'] = np.log10(R_KLEIN_VALUE)
    
    # Imprimir resultados interesantes
    for expr, value in patterns.items():
        print(f"{expr:20s} = {value:15.10f}", end="")
        
        # Verificar si está cerca de un número simple
        for simple in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 
                       0.5, 1.5, 2.5, 3.5, 4.5,
                       1/2, 1/3, 2/3, 1/4, 3/4]:
            if abs(value - simple) < 0.01:
                print(f"  ≈ {simple} ⚠️")
                break
        else:
            # Verificar si está cerca de una constante conocida
            for const_name, const_val in MATH_CONSTANTS.items():
                if abs(value - const_val) < 0.01:
                    print(f"  ≈ {const_name} ⚠️")
                    break
            else:
                print()
    
    return patterns


def check_scale_transformations():
    """Verifica si 8.4 aparece en otras escalas con transformación."""
    
    print("\n" + "="*70)
    print("TRANSFORMACIONES DE ESCALA")
    print("="*70)
    
    findings = []
    
    # Para cada escala fundamental
    for scale_name, scale_value in CONSTANTS.items():
        if not any(x in scale_name for x in ['l_', 'r_', 'lambda']):
            continue
            
        # Probar diferentes transformaciones
        for n in range(-50, 50):
            test_value = scale_value * (10 ** n)
            
            # Verificar si coincide con 8.4 en alguna forma
            for multiplier in [1, 2*np.pi, np.pi, np.e, 137, 1/137]:
                for mult_name in ['', '2π', 'π', 'e', '137', '1/137']:
                    result = test_value * multiplier
                    
                    # Verificar coincidencia en diferentes órdenes de magnitud
                    for m in range(-10, 10):
                        target = 8.4 * (10 ** m)
                        
                        if abs(result - target) / target < 0.001:  # 0.1% tolerancia
                            findings.append({
                                'scale': scale_name,
                                'transformation': f"{scale_name} × 10^{n} × {mult_name if mult_name else '1'}",
                                'result': result,
                                'target_scale': f"8.4 × 10^{m}",
                                'error': abs(result - target) / target
                            })
    
    # Imprimir hallazgos significativos
    if findings:
        print("\n🎯 COINCIDENCIAS ENCONTRADAS:")
        for f in findings[:10]:  # Limitar a 10 resultados
            print(f"\n{f['transformation']}")
            print(f"  = {f['result']:.3e} ≈ {f['target_scale']} m")
            print(f"  Error: {f['error']*100:.3f}%")
    else:
        print("\nNo se encontraron coincidencias directas significativas.")
    
    return findings


def analyze_compound_relations():
    """Busca relaciones compuestas entre constantes que den ~8.4."""
    
    print("\n" + "="*70)
    print("RELACIONES COMPUESTAS")
    print("="*70)
    
    # Algunas combinaciones físicamente motivadas
    tests = {
        'c²/G': CONSTANTS['c']**2 / CONSTANTS['G'],
        'c³/G': CONSTANTS['c']**3 / CONSTANTS['G'],
        'c⁴/G': CONSTANTS['c']**4 / CONSTANTS['G'],
        'c⁵/G': CONSTANTS['c']**5 / CONSTANTS['G'],
        'ℏc/G': CONSTANTS['hbar'] * CONSTANTS['c'] / CONSTANTS['G'],
        'ℏc³/G': CONSTANTS['hbar'] * CONSTANTS['c']**3 / CONSTANTS['G'],
        'e²/(4πε₀ℏc)': MATH_CONSTANTS['alpha'],  # estructura fina
        'mₑc²': CONSTANTS['m_electron'] * CONSTANTS['c']**2,
        'mₚc²': CONSTANTS['m_proton'] * CONSTANTS['c']**2,
        'ℏ/mₑc': CONSTANTS['hbar'] / (CONSTANTS['m_electron'] * CONSTANTS['c']),
        'Gm²/ℏc': CONSTANTS['G'] * CONSTANTS['m_proton']**2 / (CONSTANTS['hbar'] * CONSTANTS['c']),
    }
    
    for name, value in tests.items():
        # Buscar orden de magnitud que coincida con 8.4e6
        log_ratio = np.log10(R_KLEIN_M / value) if value > 0 else None
        
        if log_ratio is not None:
            print(f"\n{name}:")
            print(f"  Valor: {value:.3e}")
            print(f"  R_Klein/({name}) = {R_KLEIN_M/value:.3e}")
            print(f"  log₁₀(ratio) = {log_ratio:.2f}")
            
            # Verificar si está cerca de un número simple
            if abs(log_ratio - round(log_ratio)) < 0.1:
                print(f"  ⚠️  ≈ 10^{round(log_ratio)}")


def search_cosmological_connections():
    """Busca conexiones con escalas cosmológicas."""
    
    print("\n" + "="*70)
    print("CONEXIONES COSMOLÓGICAS")
    print("="*70)
    
    # Fracción del radio de Hubble
    fraction_hubble = R_KLEIN_M / CONSTANTS['R_Hubble']
    print(f"\nR_Klein / R_Hubble = {fraction_hubble:.3e}")
    print(f"log₁₀(fracción) = {np.log10(fraction_hubble):.2f}")
    
    # Relación con constante cosmológica
    Lambda_length = 1 / np.sqrt(CONSTANTS['Lambda'])
    print(f"\nEscala cosmológica Λ⁻¹/² = {Lambda_length:.3e} m")
    print(f"R_Klein / Λ⁻¹/² = {R_KLEIN_M / Lambda_length:.3e}")
    
    # Tiempo de Hubble
    t_Hubble = 1 / CONSTANTS['H_0']
    c_t_Hubble = CONSTANTS['c'] * t_Hubble
    print(f"\nc × t_Hubble = {c_t_Hubble:.3e} m")
    print(f"R_Klein / (c×t_H) = {R_KLEIN_M / c_t_Hubble:.3e}")
    
    # Verificar si 8400 km es alguna fracción significativa
    for n in range(1, 20):
        for m in range(1, 20):
            fraction = n / m
            test_length = CONSTANTS['R_Hubble'] * fraction
            if abs(test_length - R_KLEIN_M) / R_KLEIN_M < 0.01:
                print(f"\n⚠️  R_Klein ≈ ({n}/{m}) × R_Hubble")


def check_kpc_confusion():
    """Verifica si hay confusión entre km y kpc."""
    
    print("\n" + "="*70)
    print("VERIFICACIÓN DE UNIDADES")
    print("="*70)
    
    # Conversiones
    R_Klein_kpc = 8.4  # si fuera kpc
    kpc_to_m = 3.0857e19  # metros en un kiloparsec
    
    R_if_kpc = R_Klein_kpc * kpc_to_m
    
    print(f"\nSi R_Klein = 8.4 kpc (no km):")
    print(f"  R_Klein = {R_if_kpc:.3e} m")
    print(f"  R_Klein / R_Hubble = {R_if_kpc / CONSTANTS['R_Hubble']:.3e}")
    
    # Verificar si esto tiene más sentido físico
    print(f"\n8.4 kpc es una escala:")
    print(f"  - Galáctica (radio típico de galaxias pequeñas)")
    print(f"  - {R_if_kpc / CONSTANTS['l_Planck']:.3e} × longitud de Planck")
    
    print(f"\n8.4 × 10⁶ m = 8400 km es una escala:")
    print(f"  - Planetaria (diámetro terrestre ≈ 12,742 km)")
    print(f"  - {R_KLEIN_M / CONSTANTS['l_Planck']:.3e} × longitud de Planck")


def save_results(results: Dict):
    """Guarda los resultados en archivo JSON."""
    
    output_file = "/mnt/d/Multidimensional_Theory_Simulations/multidimensional-theory/gravitational-wave-echoes-5d/FUNDAMENTAL_RADIUS_INVESTIGATION/results/findings.json"
    
    # Convertir arrays numpy a listas para JSON
    def convert_numpy(obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, np.generic):
            return obj.item()
        elif isinstance(obj, dict):
            return {k: convert_numpy(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [convert_numpy(item) for item in obj]
        return obj
    
    results_clean = convert_numpy(results)
    
    with open(output_file, 'w') as f:
        json.dump(results_clean, f, indent=2)
    
    print(f"\nResultados guardados en: {output_file}")


# ============================================================================
# PROGRAMA PRINCIPAL
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("INVESTIGACIÓN DEL RADIO FUNDAMENTAL KLEIN")
    print(f"Valor problemático: R = {R_KLEIN_KM} km = {R_KLEIN_M:.3e} m")
    print("="*70)
    
    # Ejecutar análisis
    results = {}
    
    results['direct_ratios'] = analyze_direct_ratios()
    results['mathematical_patterns'] = analyze_mathematical_patterns()
    results['scale_transformations'] = check_scale_transformations()
    
    analyze_compound_relations()
    search_cosmological_connections()
    check_kpc_confusion()
    
    # Análisis especial: buscar si 8.4 surge de alguna relación fundamental
    print("\n" + "="*70)
    print("BÚSQUEDA DE ORIGEN FUNDAMENTAL DE 8.4")
    print("="*70)
    
    # Verificar algunas hipótesis específicas
    print("\n¿Podría 8.4 venir de...?")
    
    # Hipótesis 1: Relación con estructura fina
    alpha = MATH_CONSTANTS['alpha']
    print(f"\n1) Estructura fina (α = 1/137):")
    print(f"   8.4 / α = {R_KLEIN_VALUE / alpha:.3f}")
    print(f"   8.4 × α = {R_KLEIN_VALUE * alpha:.6f}")
    print(f"   8.4 × 137 = {R_KLEIN_VALUE * 137:.1f}")
    print(f"   8.4 / 137 = {R_KLEIN_VALUE / 137:.6f}")
    
    # Hipótesis 2: Potencias de 2 o factores geométricos
    print(f"\n2) Factores geométricos:")
    print(f"   8.4 / 2π = {R_KLEIN_VALUE / (2*np.pi):.6f}")
    print(f"   8.4 / 4π = {R_KLEIN_VALUE / (4*np.pi):.6f}")
    print(f"   8.4 × π = {R_KLEIN_VALUE * np.pi:.6f}")
    print(f"   8.4 / e = {R_KLEIN_VALUE / np.e:.6f}")
    
    # Hipótesis 3: Números cercanos
    print(f"\n3) Números cercanos a 8.4:")
    for n in [8.0, 8.33, 8.37, 8.38, 8.39, 8.41, 8.42, 8.43, 8.5]:
        diff = n - R_KLEIN_VALUE
        print(f"   {n:4.2f}: diferencia = {diff:+.2f} ({diff/R_KLEIN_VALUE*100:+.1f}%)")
    
    print("\n" + "="*70)
    print("ANÁLISIS COMPLETADO")
    print("="*70)