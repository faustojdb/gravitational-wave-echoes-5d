"""
Klein Teoría Atómica Comprehensiva - Aspectos Faltantes Incluidos
===============================================================
Incorpora aspectos fundamentales de estructura atómica que faltaban
en la teoría Klein básica para mejorar la precisión del 67% al 90%+.

ASPECTOS NUEVOS INCLUIDOS:
1. Estructura nuclear detallada (números mágicos, apareamiento)
2. Efectos relativistas (acoplamiento spin-órbita) 
3. Correlaciones electrón-electrón
4. Interacciones hiperfinas
5. Jerarquía Klein multi-escala
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import hbar, c, m_e, e, alpha, m_p
from typing import Dict, List, Tuple
import math

class ComprehensiveKleinAtomicTheory:
    """
    Teoría Klein atómica comprehensiva incluyendo aspectos faltantes.
    
    MEJORAS IMPLEMENTADAS:
    - Estructura nuclear cuántica (shell model)
    - Efectos relativistas sistemáticos
    - Correlaciones electrónicas
    - Interacciones multi-cuerpo
    - Dinámica Klein coherente
    """
    
    def __init__(self):
        """Inicializar con constantes físicas y parámetros Klein refinados."""
        self.hbar = hbar
        self.c = c
        self.m_e = m_e
        self.e = e
        self.alpha = alpha
        self.m_p = m_p
        
        # Constantes Klein fundamentales
        self.G_KLEIN_TOPOLOGICAL = 2.0  # Factor topológico Klein
        self.KLEIN_DEGRADATION_CONSTANT = 1.0  # G_universal derivado
        
        # Base datos nuclear expandida con números mágicos
        self.nuclear_magic_numbers = {
            'proton': [2, 8, 20, 28, 50, 82, 114],
            'neutron': [2, 8, 20, 28, 50, 82, 126, 184]
        }
        
        # Parámetros Klein base (del trabajo previo)
        self.klein_base_params = {
            'A': 0.001662, 'B': 1.851519, 'C': 1.503983, 'D': 0.100000,
            'alpha': 1.223767, 'beta': -0.336689
        }
        
        print("=" * 80)
        print("TEORÍA KLEIN ATÓMICA COMPREHENSIVA")
        print("Incorporando aspectos faltantes para mayor precisión")
        print("=" * 80)
    
    def analyze_nuclear_shell_structure(self, Z: int, A: int) -> Dict:
        """
        Analiza estructura de capas nucleares y su impacto en Klein.
        
        NUEVA INCORPORACIÓN: Números mágicos afectan oscilaciones Klein.
        """
        N = A - Z  # Número neutrones
        
        # Determinar proximidad a números mágicos
        def proximity_to_magic(number, magic_list):
            distances = [abs(number - magic) for magic in magic_list]
            min_distance = min(distances)
            return min_distance, number in magic_list
        
        proton_distance, is_magic_Z = proximity_to_magic(Z, self.nuclear_magic_numbers['proton'])
        neutron_distance, is_magic_N = proximity_to_magic(N, self.nuclear_magic_numbers['neutron'])
        
        # Factor estabilidad nuclear
        if is_magic_Z and is_magic_N:
            stability_factor = 1.0  # Doblemente mágico - máxima estabilidad
            shell_description = "doubly_magic"
        elif is_magic_Z or is_magic_N:
            stability_factor = 0.8  # Semi-mágico
            shell_description = "semi_magic"
        else:
            # Factor dependiente de distancia a números mágicos
            avg_distance = (proton_distance + neutron_distance) / 2
            stability_factor = 0.5 + 0.3 * np.exp(-avg_distance / 4)
            shell_description = "normal"
        
        # Energía de apareamiento
        pairing_energy = 0.0
        if Z % 2 == 0 and N % 2 == 0:
            pairing_energy = 11.2 / np.sqrt(A)  # MeV para núcleos par-par
            pairing_description = "even_even"
        elif Z % 2 == 1 and N % 2 == 1:
            pairing_energy = -11.2 / np.sqrt(A)  # MeV para núcleos impar-impar
            pairing_description = "odd_odd"
        else:
            pairing_energy = 0.0  # Sin apareamiento para impar-par
            pairing_description = "odd_even"
        
        return {
            'Z': Z, 'A': A, 'N': N,
            'proton_magic_distance': proton_distance,
            'neutron_magic_distance': neutron_distance,
            'is_doubly_magic': is_magic_Z and is_magic_N,
            'nuclear_stability_factor': stability_factor,
            'shell_description': shell_description,
            'pairing_energy_MeV': pairing_energy,
            'pairing_description': pairing_description
        }
    
    def calculate_relativistic_corrections(self, Z: int, electron_config: str) -> Dict:
        """
        Calcula correcciones relativistas sistemáticas.
        
        NUEVA INCORPORACIÓN: Efectos relativistas son cruciales para Z>30.
        """
        # Parámetro relativista
        xi = Z * self.alpha  # Parámetro relativista efectivo
        
        # Corrección energética relativista principal
        # ΔE_rel = -mc²(Zα)²[1/n - 3/4n] para s1/2
        relativistic_correction = {}
        
        # Analizar configuración electrónica para correcciones específicas
        corrections_by_orbital = {}
        
        # Niveles principales con acoplamiento spin-órbita fuerte
        heavy_element_orbitals = {
            '6s': {'j': 0.5, 'correction_factor': 1.2},
            '6p1/2': {'j': 0.5, 'correction_factor': 1.5},
            '6p3/2': {'j': 1.5, 'correction_factor': 0.8},
            '5d3/2': {'j': 1.5, 'correction_factor': 0.9},
            '5d5/2': {'j': 2.5, 'correction_factor': 0.7},
            '4f5/2': {'j': 2.5, 'correction_factor': 0.6},
            '4f7/2': {'j': 3.5, 'correction_factor': 0.5}
        }
        
        # Corrección global relativista
        if Z <= 20:
            relativistic_factor = 1.0  # Mínima corrección
        elif Z <= 50:
            relativistic_factor = 1.0 - 0.1 * (xi)**2  # Corrección cuadrática
        elif Z <= 80:
            relativistic_factor = 1.0 - 0.2 * (xi)**2 - 0.05 * (xi)**4
        else:
            relativistic_factor = 1.0 - 0.3 * (xi)**2 - 0.1 * (xi)**4  # Altamente relativista
        
        # Contracción relativista de orbitales s y p1/2
        s_orbital_contraction = 1.0 + Z * self.alpha**2 / 2
        p_orbital_expansion = 1.0 - Z * self.alpha**2 / 4  # Expansión p3/2
        
        return {
            'Z': Z,
            'relativistic_parameter': xi,
            'global_relativistic_factor': relativistic_factor,
            's_orbital_contraction': s_orbital_contraction,
            'p_orbital_expansion': p_orbital_expansion,
            'is_highly_relativistic': Z > 50,
            'correction_magnitude': abs(1.0 - relativistic_factor)
        }
    
    def calculate_electron_correlation_effects(self, Z: int, electron_config: str) -> Dict:
        """
        Calcula efectos de correlación electrón-electrón.
        
        NUEVA INCORPORACIÓN: Correlaciones dinámicas entre electrones.
        """
        # Número de electrones
        n_electrons = Z
        
        # Energía de correlación aproximada (Wigner formula)
        # E_corr ≈ -0.44 Ry × Z^(1/3) para átomo neutro
        correlation_energy_per_electron = -0.44 * 13.6 * (Z**(1/3)) / Z  # eV por electrón
        total_correlation_energy = correlation_energy_per_electron * n_electrons
        
        # Factor de reducción de correlación para diferentes configuraciones
        config_correlation_factors = {
            'noble_gas': 0.8,      # Correlación reducida (capas cerradas)
            'alkali': 1.2,         # Correlación aumentada (electrón desapareado)
            'transition_metal': 1.5,  # Correlación fuerte (orbitales d)
            'lanthanide': 1.8,     # Correlación muy fuerte (orbitales f)
            'actinide': 2.0        # Correlación extrema (orbitales f + relativismo)
        }
        
        # Clasificar elemento
        if Z in [2, 10, 18, 36, 54, 86, 118]:
            element_type = 'noble_gas'
        elif Z in [3, 11, 19, 37, 55, 87]:
            element_type = 'alkali'
        elif 21 <= Z <= 30 or 39 <= Z <= 48 or 57 <= Z <= 80:
            element_type = 'transition_metal'
        elif 57 <= Z <= 71:
            element_type = 'lanthanide'
        elif 89 <= Z <= 103:
            element_type = 'actinide'
        else:
            element_type = 'main_group'
        
        correlation_factor = config_correlation_factors.get(element_type, 1.0)
        
        # Corrección al radio atómico por correlación
        # Correlación típicamente reduce tamaño atómico
        correlation_radius_correction = 1.0 - 0.05 * correlation_factor
        
        return {
            'Z': Z,
            'n_electrons': n_electrons,
            'correlation_energy_eV': total_correlation_energy,
            'correlation_energy_per_electron': correlation_energy_per_electron,
            'element_type': element_type,
            'correlation_factor': correlation_factor,
            'radius_correction_factor': correlation_radius_correction
        }
    
    def calculate_hyperfine_klein_coupling(self, Z: int, A: int, nuclear_data: Dict) -> Dict:
        """
        Calcula acoplamiento hiperfino modulado por oscilaciones Klein.
        
        NUEVA INCORPORACIÓN: Interacción núcleo-electrón via Klein.
        """
        # Momento magnético nuclear (aproximado)
        nuclear_magneton = 5.051e-27  # J/T
        
        # Interacción hiperfina magnética dipolar
        # A_hf = (2μ₀/3) × μ_nuclear × μ_electrón × |ψ(0)|²
        
        # Densidad electrónica en el núcleo |ψ(0)|²
        bohr_radius = 5.29e-11  # m
        electron_density_at_nucleus = 1.0 / (np.pi * (bohr_radius / Z)**3)
        
        # Constante hiperfina base
        hyperfine_constant_base = (2e-7 * nuclear_magneton * 9.274e-24 * 
                                 electron_density_at_nucleus)  # Hz
        
        # Modulación Klein de interacción hiperfina
        if nuclear_data.get('half_life_years', 'stable') != 'stable':
            # Núcleos inestables: oscilación Klein modula acoplamiento hiperfino
            half_life = nuclear_data['half_life_years']
            omega_klein = 2 * np.pi / (half_life * 365.25 * 24 * 3600)
            
            # Amplitud modulación proporcional a Q/binding_energy
            Q_value = nuclear_data.get('Q_value_keV', 0)
            binding_energy = nuclear_data.get('binding_energy_MeV', 8 * A) * 1000
            modulation_amplitude = Q_value / binding_energy if binding_energy > 0 else 0
            
            # Acoplamiento hiperfino time-dependent
            klein_modulated_hyperfine = {
                'base_frequency_Hz': hyperfine_constant_base,
                'klein_modulation_frequency_Hz': omega_klein,
                'modulation_amplitude': modulation_amplitude,
                'time_dependent': True,
                'formula': "A_hf(t) = A₀[1 + δ·cos(ω_Klein·t)]"
            }
        else:
            # Núcleos estables: acoplamiento hiperfino constante
            klein_modulated_hyperfine = {
                'base_frequency_Hz': hyperfine_constant_base,
                'klein_modulation_frequency_Hz': 0.0,
                'modulation_amplitude': 0.0,
                'time_dependent': False,
                'formula': "A_hf = A₀ (constant)"
            }
        
        return klein_modulated_hyperfine
    
    def develop_multi_scale_klein_hierarchy(self, Z: int, A: int) -> Dict:
        """
        Desarrolla jerarquía Klein multi-escala coherente.
        
        NUEVA INCORPORACIÓN: Klein bottles a diferentes escalas energéticas.
        """
        # Escalas Klein identificadas
        scales = {
            'cosmic': {
                'radius_m': 8.4e6,  # 8400 km
                'frequency_hz': 5.68,
                'energy_scale_eV': 2.3e-15  # ℏω
            },
            'atomic': {
                'radius_m': 50e-12,  # ~50 pm típico
                'frequency_hz': None,  # Calculado abajo
                'energy_scale_eV': 10.0  # Ionización típica
            },
            'nuclear': {
                'radius_m': 1.2e-15 * (A**(1/3)),  # Radio nuclear
                'frequency_hz': None,  # Calculado para núcleo específico
                'energy_scale_eV': 8e6 * A  # Energía enlace nuclear típica
            },
            'nucleon': {
                'radius_m': 0.8e-15,  # Radio protón/neutrón
                'frequency_hz': None,
                'energy_scale_eV': 938e6  # Masa protón en eV
            }
        }
        
        # Calcular frecuencias Klein para cada escala
        for scale_name, scale_data in scales.items():
            if scale_data['frequency_hz'] is None:
                # Usar relación Klein: ω = 2E/(ℏc) × c/R = 2E/(ℏR)
                energy_joules = scale_data['energy_scale_eV'] * self.e
                frequency = energy_joules / (self.hbar * 2 * np.pi)
                scale_data['frequency_hz'] = frequency
        
        # Ratios entre escalas
        ratios = {}
        scale_names = list(scales.keys())
        for i, scale1 in enumerate(scale_names):
            for scale2 in scale_names[i+1:]:
                ratio_freq = scales[scale1]['frequency_hz'] / scales[scale2]['frequency_hz']
                ratio_size = scales[scale1]['radius_m'] / scales[scale2]['radius_m']
                ratios[f"{scale1}_{scale2}"] = {
                    'frequency_ratio': ratio_freq,
                    'size_ratio': ratio_size,
                    'scale_hierarchy': ratio_freq * ratio_size  # Product should be constant
                }
        
        # Test jerarquía Klein coherente
        # Para topología Klein: ω₁R₁ = ω₂R₂ = constante
        klein_constants = []
        for scale_name, scale_data in scales.items():
            klein_constant = scale_data['frequency_hz'] * scale_data['radius_m']
            klein_constants.append(klein_constant)
            scale_data['klein_constant'] = klein_constant
        
        # Verificar universalidad
        klein_constant_avg = np.mean(klein_constants)
        klein_constant_std = np.std(klein_constants)
        universality_score = 1.0 - (klein_constant_std / klein_constant_avg)
        
        return {
            'scales': scales,
            'scale_ratios': ratios,
            'klein_constants': klein_constants,
            'universal_klein_constant': klein_constant_avg,
            'universality_score': universality_score,
            'is_coherent_hierarchy': universality_score > 0.8
        }
    
    def calculate_comprehensive_klein_prediction(self, Z: int, A: int, 
                                                ionization_eV: float, 
                                                electron_config: str,
                                                nuclear_data: Dict = None) -> Dict:
        """
        Calcula predicción Klein comprehensiva incorporando todos los aspectos nuevos.
        
        RESULTADO: Predicción refinada con >90% precisión esperada.
        """
        print(f"\n🔬 ANÁLISIS COMPREHENSIVO Klein para Z={Z}, A={A}")
        
        # 1. Análisis estructura nuclear
        nuclear_structure = self.analyze_nuclear_shell_structure(Z, A)
        
        # 2. Correcciones relativistas
        relativistic = self.calculate_relativistic_corrections(Z, electron_config)
        
        # 3. Correlaciones electrónicas
        electron_correlation = self.calculate_electron_correlation_effects(Z, electron_config)
        
        # 4. Interacciones hiperfinas (si hay datos nucleares)
        if nuclear_data:
            hyperfine = self.calculate_hyperfine_klein_coupling(Z, A, nuclear_data)
        else:
            hyperfine = None
        
        # 5. Jerarquía Klein multi-escala
        klein_hierarchy = self.develop_multi_scale_klein_hierarchy(Z, A)
        
        # 6. Predicción Klein base (del trabajo anterior)
        base_klein_prediction = self.calculate_base_klein_radius(Z, ionization_eV, electron_config)
        
        # 7. APLICAR TODAS LAS CORRECCIONES
        comprehensive_corrections = {
            'nuclear_shell_correction': nuclear_structure['nuclear_stability_factor'],
            'relativistic_correction': relativistic['global_relativistic_factor'],
            'correlation_correction': electron_correlation['radius_correction_factor'],
            'pairing_correction': 1.0 + nuclear_structure['pairing_energy_MeV'] * 0.001  # Pequeña corrección
        }
        
        # Factor de corrección total
        total_correction_factor = 1.0
        for correction_name, factor in comprehensive_corrections.items():
            total_correction_factor *= factor
        
        # Predicción final Klein comprehensiva
        comprehensive_radius_pm = base_klein_prediction * total_correction_factor
        
        print(f"  Base Klein: {base_klein_prediction:.1f} pm")
        print(f"  Nuclear shell: ×{comprehensive_corrections['nuclear_shell_correction']:.3f}")
        print(f"  Relativistic: ×{comprehensive_corrections['relativistic_correction']:.3f}")
        print(f"  Correlation: ×{comprehensive_corrections['correlation_correction']:.3f}")
        print(f"  Pairing: ×{comprehensive_corrections['pairing_correction']:.3f}")
        print(f"  → FINAL: {comprehensive_radius_pm:.1f} pm")
        
        return {
            'Z': Z, 'A': A,
            'base_klein_prediction_pm': base_klein_prediction,
            'nuclear_structure': nuclear_structure,
            'relativistic_effects': relativistic,
            'electron_correlation': electron_correlation,
            'hyperfine_coupling': hyperfine,
            'klein_hierarchy': klein_hierarchy,
            'comprehensive_corrections': comprehensive_corrections,
            'total_correction_factor': total_correction_factor,
            'final_radius_prediction_pm': comprehensive_radius_pm,
            'theory_version': 'comprehensive_v2.0'
        }
    
    def calculate_base_klein_radius(self, Z: int, ionization_eV: float, electron_config: str) -> float:
        """Calcula radio Klein base usando fórmula establecida."""
        
        # Usar parámetros Klein calibrados
        A = self.klein_base_params['A']
        B = self.klein_base_params['B']
        C = self.klein_base_params['C']
        D = self.klein_base_params['D']
        alpha = self.klein_base_params['alpha']
        beta = self.klein_base_params['beta']
        
        # Energía en Joules
        E_joules = ionization_eV * self.e
        
        # Escala Klein base
        R_klein_base = self.hbar * self.c / E_joules  # metros
        
        # Términos Klein
        N_e = Z
        permanent_term = np.log(N_e + 1)
        transient_term = B / N_e
        exponential_term = C * np.exp(-N_e / D)
        
        # Radio base
        R_base = A * R_klein_base * (permanent_term + transient_term + exponential_term)
        
        # Factor inclinación orbital
        inclination_rad = self.calculate_orbital_inclination(electron_config, Z)
        inclination_factor = alpha * np.cos(inclination_rad) + beta * np.sin(inclination_rad)
        
        # Radio final en pm
        R_final_pm = R_base * inclination_factor * 1e12
        
        return R_final_pm
    
    def calculate_orbital_inclination(self, electron_config: str, Z: int) -> float:
        """Calcula inclinación orbital (del trabajo anterior)."""
        inclinations = {
            's_only': 10.0,
            'p_present': 25.0,
            'p3_half': 33.2,
            'd_present': 35.0,
            'f_present': 40.0
        }
        
        if 'f' in electron_config:
            base_inclination = inclinations['f_present']
        elif 'd' in electron_config:
            base_inclination = inclinations['d_present']
        elif 'p3' in electron_config:
            base_inclination = inclinations['p3_half']
        elif 'p' in electron_config:
            base_inclination = inclinations['p_present']
        else:
            base_inclination = inclinations['s_only']
        
        return base_inclination * np.pi / 180


def test_comprehensive_klein_theory():
    """Prueba la teoría Klein comprehensiva en elementos clave."""
    
    print("\n" + "🧪" * 50)
    print("TEST TEORÍA KLEIN COMPREHENSIVA")
    print("🧪" * 50)
    
    # Crear analizador comprehensivo
    analyzer = ComprehensiveKleinAtomicTheory()
    
    # Elementos de prueba con datos experimentales
    test_elements = [
        {
            'Z': 1, 'A': 1, 'symbol': 'H',
            'ionization_eV': 13.6, 'config': '1s',
            'experimental_radius_pm': 53.0,
            'nuclear_data': None
        },
        {
            'Z': 2, 'A': 4, 'symbol': 'He',
            'ionization_eV': 24.6, 'config': '1s2',
            'experimental_radius_pm': 31.0,
            'nuclear_data': None
        },
        {
            'Z': 26, 'A': 56, 'symbol': 'Fe',
            'ionization_eV': 7.9, 'config': '[Ar]3d6_4s2',
            'experimental_radius_pm': 156.0,
            'nuclear_data': None
        },
        {
            'Z': 79, 'A': 197, 'symbol': 'Au',
            'ionization_eV': 9.2, 'config': '[Xe]4f14_5d10_6s',
            'experimental_radius_pm': 174.0,
            'nuclear_data': None
        },
        {
            'Z': 43, 'A': 99, 'symbol': 'Tc-99m',
            'ionization_eV': 7.3, 'config': '[Kr]4d6_5s',
            'experimental_radius_pm': 183.0,
            'nuclear_data': {
                'half_life_years': 6.9e-6,
                'Q_value_keV': 140,
                'binding_energy_MeV': 861.1,
                'decay_mode': 'isomeric_transition'
            }
        }
    ]
    
    results = []
    print(f"\n{'Elemento':<8} {'Base':<8} {'Compreh':<8} {'Exp':<8} {'Prec_Base':<10} {'Prec_Comp':<10} {'Mejora':<8}")
    print("-" * 75)
    
    for element in test_elements:
        # Análisis comprehensivo
        comprehensive_result = analyzer.calculate_comprehensive_klein_prediction(
            element['Z'], element['A'], element['ionization_eV'], 
            element['config'], element.get('nuclear_data')
        )
        
        # Precisiones
        base_pred = comprehensive_result['base_klein_prediction_pm']
        comp_pred = comprehensive_result['final_radius_prediction_pm']
        exp_value = element['experimental_radius_pm']
        
        base_precision = 100 * (1 - abs(base_pred - exp_value) / exp_value)
        comp_precision = 100 * (1 - abs(comp_pred - exp_value) / exp_value)
        improvement = comp_precision - base_precision
        
        results.append({
            'element': element,
            'comprehensive_result': comprehensive_result,
            'base_precision': base_precision,
            'comprehensive_precision': comp_precision,
            'improvement': improvement
        })
        
        print(f"{element['symbol']:<8} {base_pred:<8.1f} {comp_pred:<8.1f} {exp_value:<8.1f} "
              f"{base_precision:<10.1f} {comp_precision:<10.1f} {improvement:<8.1f}")
    
    # Estadísticas generales
    base_precisions = [r['base_precision'] for r in results]
    comp_precisions = [r['comprehensive_precision'] for r in results]
    
    avg_base = np.mean(base_precisions)
    avg_comp = np.mean(comp_precisions)
    avg_improvement = avg_comp - avg_base
    
    print(f"\n📊 ESTADÍSTICAS GENERALES:")
    print(f"  Precisión base promedio: {avg_base:.1f}%")
    print(f"  Precisión comprehensiva: {avg_comp:.1f}%")
    print(f"  Mejora promedio: {avg_improvement:.1f}%")
    
    if avg_comp > 90:
        print(f"\n🎉 ¡OBJETIVO LOGRADO! Precisión >90%")
        print(f"   Teoría Klein comprehensiva exitosamente validada")
    elif avg_improvement > 10:
        print(f"\n✅ MEJORA SIGNIFICATIVA lograda")
        print(f"   Aspectos incorporados mejoran sustancialmente la teoría")
    else:
        print(f"\n🔧 Mejora modesta - necesario más trabajo")
    
    return results


if __name__ == "__main__":
    # Ejecutar test comprehensivo
    test_results = test_comprehensive_klein_theory()
    
    print("\n" + "=" * 80)
    print("TEORÍA KLEIN ATÓMICA COMPREHENSIVA DESARROLLADA")
    print("Incorporando estructura nuclear, relativismo, correlaciones e hiperfina")
    print("=" * 80)