"""
Klein Teoría Atómica Refinada v2.1 - Correcciones Calibradas
==========================================================
Versión refinada con correcciones sutiles calibradas empíricamente.
Los parámetros Klein base ya capturan muchos efectos implícitamente.

FILOSOFÍA v2.1:
- Correcciones pequeñas (~5-10%) en lugar de grandes (~30-50%)
- Efectos relativistas solo para Z>50 (elementos muy pesados)
- Correlaciones nucleares sutiles
- Validar que cada corrección realmente mejore la precisión
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import hbar, c, m_e, e, alpha, m_p
from typing import Dict, List, Tuple
import math

class RefinedKleinAtomicTheory:
    """
    Teoría Klein atómica refinada v2.1 con correcciones calibradas.
    
    PRINCIPIO: Los parámetros Klein base (A, B, C, D, α, β) ya fueron
    optimizados empíricamente y capturan la mayoría de efectos físicos.
    Las correcciones deben ser perturbaciones pequeñas, no cambios drásticos.
    """
    
    def __init__(self):
        """Inicializar con correcciones calibradas sutiles."""
        self.hbar = hbar
        self.c = c
        self.m_e = m_e
        self.e = e
        self.alpha = alpha
        self.m_p = m_p
        
        # Parámetros Klein base (ya optimizados)
        self.klein_base_params = {
            'A': 0.001662, 'B': 1.851519, 'C': 1.503983, 'D': 0.100000,
            'alpha': 1.223767, 'beta': -0.336689
        }
        
        # CORRECCIONES CALIBRADAS SUTILES
        self.refined_corrections = {
            # Estructura nuclear: correcciones pequeñas basadas en números mágicos
            'nuclear_shell': {
                'doubly_magic_bonus': 1.03,      # +3% para núcleos doblemente mágicos
                'semi_magic_bonus': 1.015,       # +1.5% para semi-mágicos
                'normal_factor': 1.0,            # Sin corrección para normales
                'pairing_factor_per_MeV': 0.002  # 0.2% por MeV de apareamiento
            },
            
            # Efectos relativistas: solo elementos muy pesados
            'relativistic': {
                'onset_Z': 50,                   # Comenzar correcciones en Z=50
                'light_elements_factor': 1.0,   # Sin corrección para Z<50
                'correction_per_Z_unit': 0.0015, # 0.15% por unidad Z>50
                'max_correction': 0.15          # Máximo 15% corrección
            },
            
            # Correlaciones electrónicas: efectos sutiles
            'electron_correlation': {
                'base_correction': 0.98,        # -2% base para todos
                'noble_gas_bonus': 1.02,        # +2% extra para gases nobles
                'transition_metal_penalty': 0.97, # -3% extra para metales transición
                'lanthanide_penalty': 0.96,    # -4% extra para lantánidos
                'actinide_penalty': 0.95       # -5% extra para actínidos
            },
            
            # Configuración electrónica: efectos específicos
            'electron_configuration': {
                'half_filled_bonus': 1.025,     # +2.5% para semi-llenos
                'closed_shell_bonus': 1.02,    # +2% para capas cerradas
                'open_d_penalty': 0.98,        # -2% para d parcialmente llenos
                'open_f_penalty': 0.97         # -3% para f parcialmente llenos
            }
        }
        
        print("=" * 80)
        print("TEORÍA KLEIN ATÓMICA REFINADA v2.1")
        print("Correcciones sutiles calibradas empíricamente")
        print("=" * 80)
    
    def analyze_refined_nuclear_structure(self, Z: int, A: int) -> Dict:
        """
        Analiza estructura nuclear con correcciones sutiles calibradas.
        
        REFINAMIENTO: Correcciones pequeñas basadas en física nuclear.
        """
        N = A - Z
        
        # Números mágicos
        magic_protons = [2, 8, 20, 28, 50, 82, 114]
        magic_neutrons = [2, 8, 20, 28, 50, 82, 126, 184]
        
        # Determinar tipo nuclear
        is_magic_Z = Z in magic_protons
        is_magic_N = N in magic_neutrons
        
        # Factor estructura nuclear (correcciones sutiles)
        corrections = self.refined_corrections['nuclear_shell']
        
        if is_magic_Z and is_magic_N:
            nuclear_factor = corrections['doubly_magic_bonus']
            description = "doubly_magic"
        elif is_magic_Z or is_magic_N:
            nuclear_factor = corrections['semi_magic_bonus']
            description = "semi_magic"
        else:
            nuclear_factor = corrections['normal_factor']
            description = "normal"
        
        # Corrección por apareamiento (muy sutil)
        pairing_energy = 0.0
        if Z % 2 == 0 and N % 2 == 0:
            pairing_energy = 11.2 / np.sqrt(A)  # MeV
            pairing_description = "even_even"
        elif Z % 2 == 1 and N % 2 == 1:
            pairing_energy = -11.2 / np.sqrt(A)  # MeV
            pairing_description = "odd_odd"
        else:
            pairing_energy = 0.0
            pairing_description = "odd_even"
        
        # Aplicar corrección sutil de apareamiento
        pairing_correction = 1.0 + pairing_energy * corrections['pairing_factor_per_MeV']
        total_nuclear_factor = nuclear_factor * pairing_correction
        
        return {
            'Z': Z, 'A': A, 'N': N,
            'nuclear_structure_factor': total_nuclear_factor,
            'structure_type': description,
            'pairing_energy_MeV': pairing_energy,
            'pairing_type': pairing_description,
            'correction_magnitude': abs(total_nuclear_factor - 1.0)
        }
    
    def calculate_refined_relativistic_corrections(self, Z: int) -> Dict:
        """
        Calcula correcciones relativistas refinadas - solo elementos muy pesados.
        
        REFINAMIENTO: Efectos solo para Z>50, correcciones graduales.
        """
        corrections = self.refined_corrections['relativistic']
        
        if Z < corrections['onset_Z']:
            # Elementos ligeros: sin corrección relativista
            relativistic_factor = corrections['light_elements_factor']
            is_relativistic = False
            correction_magnitude = 0.0
        else:
            # Elementos pesados: corrección gradual
            Z_excess = Z - corrections['onset_Z']
            correction_fraction = min(
                Z_excess * corrections['correction_per_Z_unit'],
                corrections['max_correction']
            )
            relativistic_factor = 1.0 - correction_fraction  # Contracción relativista
            is_relativistic = True
            correction_magnitude = correction_fraction
        
        return {
            'Z': Z,
            'relativistic_factor': relativistic_factor,
            'is_relativistic': is_relativistic,
            'correction_magnitude': correction_magnitude,
            'onset_threshold': corrections['onset_Z']
        }
    
    def calculate_refined_correlation_effects(self, Z: int, electron_config: str) -> Dict:
        """
        Calcula efectos de correlación electrónica refinados.
        
        REFINAMIENTO: Correcciones base pequeñas con ajustes por tipo de elemento.
        """
        corrections = self.refined_corrections['electron_correlation']
        
        # Corrección base para todos los elementos
        correlation_factor = corrections['base_correction']
        
        # Clasificar elemento y aplicar corrección específica
        if Z in [2, 10, 18, 36, 54, 86, 118]:  # Gases nobles
            correlation_factor *= corrections['noble_gas_bonus']
            element_class = "noble_gas"
        elif 21 <= Z <= 30 or 39 <= Z <= 48 or 72 <= Z <= 80:  # Metales transición
            correlation_factor *= corrections['transition_metal_penalty']
            element_class = "transition_metal"
        elif 57 <= Z <= 71:  # Lantánidos
            correlation_factor *= corrections['lanthanide_penalty']
            element_class = "lanthanide"
        elif 89 <= Z <= 103:  # Actínidos
            correlation_factor *= corrections['actinide_penalty']
            element_class = "actinide"
        else:
            element_class = "main_group"
        
        return {
            'Z': Z,
            'correlation_factor': correlation_factor,
            'element_class': element_class,
            'correction_magnitude': abs(correlation_factor - 1.0)
        }
    
    def analyze_electron_configuration_effects(self, Z: int, electron_config: str) -> Dict:
        """
        Analiza efectos específicos de configuración electrónica.
        
        REFINAMIENTO: Efectos sutiles para configuraciones especiales.
        """
        corrections = self.refined_corrections['electron_configuration']
        
        # Factor base
        config_factor = 1.0
        config_effects = []
        
        # Detectar configuraciones especiales
        
        # Semi-llenos: N (p³), P (p³), Mn (d⁵), etc.
        if Z in [7, 15, 25]:  # N, P, Mn (ejemplos conocidos)
            config_factor *= corrections['half_filled_bonus']
            config_effects.append("half_filled")
        
        # Capas cerradas: gases nobles
        if Z in [2, 10, 18, 36, 54, 86, 118]:
            config_factor *= corrections['closed_shell_bonus']
            config_effects.append("closed_shell")
        
        # Orbitales d parcialmente llenos
        if 21 <= Z <= 30 or 39 <= Z <= 48 or 72 <= Z <= 80:
            if Z not in [24, 29, 47, 79]:  # Excepto configuraciones especiales
                config_factor *= corrections['open_d_penalty']
                config_effects.append("open_d")
        
        # Orbitales f parcialmente llenos
        if 57 <= Z <= 71 or 89 <= Z <= 103:
            config_factor *= corrections['open_f_penalty']
            config_effects.append("open_f")
        
        return {
            'Z': Z,
            'configuration_factor': config_factor,
            'special_effects': config_effects,
            'correction_magnitude': abs(config_factor - 1.0)
        }
    
    def calculate_comprehensive_refined_prediction(self, Z: int, A: int, 
                                                 ionization_eV: float, 
                                                 electron_config: str) -> Dict:
        """
        Calcula predicción Klein refinada con correcciones sutiles calibradas.
        
        OBJETIVO: Mejorar precisión sin sobrecorregir.
        """
        print(f"\n🔬 ANÁLISIS REFINADO v2.1 para Z={Z} ({electron_config})")
        
        # 1. Predicción Klein base (sin modificar - ya optimizada)
        base_prediction = self.calculate_base_klein_radius(Z, ionization_eV, electron_config)
        
        # 2. Correcciones refinadas sutiles
        nuclear_analysis = self.analyze_refined_nuclear_structure(Z, A)
        relativistic_analysis = self.calculate_refined_relativistic_corrections(Z)
        correlation_analysis = self.calculate_refined_correlation_effects(Z, electron_config)
        config_analysis = self.analyze_electron_configuration_effects(Z, electron_config)
        
        # 3. Aplicar correcciones sutiles
        refined_corrections = {
            'nuclear_structure': nuclear_analysis['nuclear_structure_factor'],
            'relativistic': relativistic_analysis['relativistic_factor'], 
            'electron_correlation': correlation_analysis['correlation_factor'],
            'electron_configuration': config_analysis['configuration_factor']
        }
        
        # Factor de corrección total (cercano a 1.0)
        total_correction_factor = 1.0
        for correction_name, factor in refined_corrections.items():
            total_correction_factor *= factor
        
        # Predicción final refinada
        refined_prediction = base_prediction * total_correction_factor
        
        # Mostrar correcciones aplicadas
        print(f"  Base Klein: {base_prediction:.1f} pm")
        for name, factor in refined_corrections.items():
            print(f"  {name}: ×{factor:.4f} ({(factor-1)*100:+.1f}%)")
        print(f"  Total: ×{total_correction_factor:.4f} ({(total_correction_factor-1)*100:+.1f}%)")
        print(f"  → REFINADO: {refined_prediction:.1f} pm")
        
        return {
            'Z': Z, 'A': A, 'electron_config': electron_config,
            'base_prediction_pm': base_prediction,
            'nuclear_analysis': nuclear_analysis,
            'relativistic_analysis': relativistic_analysis,
            'correlation_analysis': correlation_analysis,
            'configuration_analysis': config_analysis,
            'refined_corrections': refined_corrections,
            'total_correction_factor': total_correction_factor,
            'final_refined_prediction_pm': refined_prediction,
            'theory_version': 'refined_v2.1'
        }
    
    def validate_correction_effectiveness(self, test_elements: List[Dict]) -> Dict:
        """
        Valida que cada corrección realmente mejore la precisión.
        
        METODOLOGÍA: Comparar precisión con/sin cada corrección.
        """
        print(f"\n📊 VALIDACIÓN EFECTIVIDAD CORRECCIONES")
        print("-" * 50)
        
        validation_results = {
            'no_corrections': [],
            'nuclear_only': [],
            'relativistic_only': [],
            'correlation_only': [],
            'config_only': [],
            'all_corrections': []
        }
        
        for element in test_elements:
            Z = element['Z']
            A = element['A'] 
            ionization_eV = element['ionization_eV']
            config = element['config']
            exp_radius = element['experimental_radius_pm']
            
            # Predicción base (sin correcciones)
            base_pred = self.calculate_base_klein_radius(Z, ionization_eV, config)
            base_precision = 100 * (1 - abs(base_pred - exp_radius) / exp_radius)
            validation_results['no_corrections'].append(base_precision)
            
            # Análisis de correcciones individuales
            nuclear = self.analyze_refined_nuclear_structure(Z, A)
            relativistic = self.calculate_refined_relativistic_corrections(Z)
            correlation = self.calculate_refined_correlation_effects(Z, config)
            configuration = self.analyze_electron_configuration_effects(Z, config)
            
            # Test cada corrección por separado
            nuclear_pred = base_pred * nuclear['nuclear_structure_factor']
            nuclear_precision = 100 * (1 - abs(nuclear_pred - exp_radius) / exp_radius)
            validation_results['nuclear_only'].append(nuclear_precision)
            
            rel_pred = base_pred * relativistic['relativistic_factor']
            rel_precision = 100 * (1 - abs(rel_pred - exp_radius) / exp_radius)
            validation_results['relativistic_only'].append(rel_precision)
            
            corr_pred = base_pred * correlation['correlation_factor']
            corr_precision = 100 * (1 - abs(corr_pred - exp_radius) / exp_radius)
            validation_results['correlation_only'].append(corr_precision)
            
            config_pred = base_pred * configuration['configuration_factor']
            config_precision = 100 * (1 - abs(config_pred - exp_radius) / exp_radius)
            validation_results['config_only'].append(config_precision)
            
            # Todas las correcciones juntas
            total_factor = (nuclear['nuclear_structure_factor'] * 
                          relativistic['relativistic_factor'] *
                          correlation['correlation_factor'] *
                          configuration['configuration_factor'])
            all_pred = base_pred * total_factor
            all_precision = 100 * (1 - abs(all_pred - exp_radius) / exp_radius)
            validation_results['all_corrections'].append(all_precision)
        
        # Calcular precisiones promedio
        avg_precisions = {}
        improvements = {}
        base_avg = np.mean(validation_results['no_corrections'])
        
        for correction_type, precisions in validation_results.items():
            avg_precision = np.mean(precisions)
            avg_precisions[correction_type] = avg_precision
            improvements[correction_type] = avg_precision - base_avg
        
        print(f"{'Corrección':<20} {'Precisión':<10} {'Mejora':<10}")
        print("-" * 45)
        for correction_type, avg_prec in avg_precisions.items():
            improvement = improvements[correction_type]
            print(f"{correction_type:<20} {avg_prec:<10.1f} {improvement:<10.1f}")
        
        return {
            'validation_results': validation_results,
            'average_precisions': avg_precisions,
            'improvements': improvements,
            'best_correction': max(improvements, key=improvements.get),
            'final_precision': avg_precisions['all_corrections'],
            'total_improvement': improvements['all_corrections']
        }
    
    def calculate_base_klein_radius(self, Z: int, ionization_eV: float, electron_config: str) -> float:
        """Calcula radio Klein base usando parámetros optimizados (sin cambios)."""
        
        A = self.klein_base_params['A']
        B = self.klein_base_params['B']
        C = self.klein_base_params['C']
        D = self.klein_base_params['D']
        alpha = self.klein_base_params['alpha']
        beta = self.klein_base_params['beta']
        
        # Energía en Joules
        E_joules = ionization_eV * self.e
        
        # Escala Klein base
        R_klein_base = self.hbar * self.c / E_joules
        
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
        """Calcula inclinación orbital (sin cambios)."""
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


def test_refined_klein_theory():
    """Prueba la teoría Klein refinada v2.1."""
    
    print("\n" + "🧪" * 50)
    print("TEST TEORÍA KLEIN REFINADA v2.1")
    print("🧪" * 50)
    
    # Crear analizador refinado
    analyzer = RefinedKleinAtomicTheory()
    
    # Elementos de prueba expandidos
    test_elements = [
        {'Z': 1, 'A': 1, 'symbol': 'H', 'ionization_eV': 13.6, 'config': '1s', 'experimental_radius_pm': 53.0},
        {'Z': 2, 'A': 4, 'symbol': 'He', 'ionization_eV': 24.6, 'config': '1s2', 'experimental_radius_pm': 31.0},
        {'Z': 3, 'A': 7, 'symbol': 'Li', 'ionization_eV': 5.4, 'config': '1s2_2s', 'experimental_radius_pm': 167.0},
        {'Z': 6, 'A': 12, 'symbol': 'C', 'ionization_eV': 11.3, 'config': '1s2_2s2_2p2', 'experimental_radius_pm': 67.0},
        {'Z': 7, 'A': 14, 'symbol': 'N', 'ionization_eV': 14.5, 'config': '1s2_2s2_2p3', 'experimental_radius_pm': 56.0},
        {'Z': 10, 'A': 20, 'symbol': 'Ne', 'ionization_eV': 21.6, 'config': '1s2_2s2_2p6', 'experimental_radius_pm': 38.0},
        {'Z': 26, 'A': 56, 'symbol': 'Fe', 'ionization_eV': 7.9, 'config': '[Ar]3d6_4s2', 'experimental_radius_pm': 156.0},
        {'Z': 79, 'A': 197, 'symbol': 'Au', 'ionization_eV': 9.2, 'config': '[Xe]4f14_5d10_6s', 'experimental_radius_pm': 174.0},
        {'Z': 92, 'A': 238, 'symbol': 'U', 'ionization_eV': 6.2, 'config': '[Rn]5f3_6d_7s2', 'experimental_radius_pm': 196.0}
    ]
    
    # Validar efectividad de correcciones
    validation = analyzer.validate_correction_effectiveness(test_elements)
    
    print(f"\n🎯 RESULTADO VALIDACIÓN:")
    print(f"  Precisión base: {validation['average_precisions']['no_corrections']:.1f}%")
    print(f"  Precisión refinada: {validation['final_precision']:.1f}%") 
    print(f"  Mejora total: {validation['total_improvement']:.1f}%")
    print(f"  Mejor corrección individual: {validation['best_correction']}")
    
    # Test comprehensivo en elementos clave
    print(f"\n{'Elemento':<8} {'Base':<8} {'Refinado':<8} {'Exp':<8} {'Prec_Base':<10} {'Prec_Ref':<10} {'Mejora':<8}")
    print("-" * 75)
    
    total_improvements = []
    
    for element in test_elements:
        result = analyzer.calculate_comprehensive_refined_prediction(
            element['Z'], element['A'], element['ionization_eV'], element['config']
        )
        
        base_pred = result['base_prediction_pm']
        refined_pred = result['final_refined_prediction_pm']
        exp_value = element['experimental_radius_pm']
        
        base_precision = 100 * (1 - abs(base_pred - exp_value) / exp_value)
        refined_precision = 100 * (1 - abs(refined_pred - exp_value) / exp_value)
        improvement = refined_precision - base_precision
        
        total_improvements.append(improvement)
        
        print(f"{element['symbol']:<8} {base_pred:<8.1f} {refined_pred:<8.1f} {exp_value:<8.1f} "
              f"{base_precision:<10.1f} {refined_precision:<10.1f} {improvement:<8.1f}")
    
    # Estadísticas finales
    avg_improvement = np.mean(total_improvements)
    successful_improvements = sum(1 for imp in total_improvements if imp > 0)
    
    print(f"\n📊 ESTADÍSTICAS FINALES:")
    print(f"  Mejora promedio: {avg_improvement:.1f}%")
    print(f"  Elementos mejorados: {successful_improvements}/{len(test_elements)}")
    print(f"  Precisión final promedio: {validation['final_precision']:.1f}%")
    
    if validation['final_precision'] > 85 and avg_improvement > 0:
        print(f"\n🎉 ¡ÉXITO! Teoría Klein refinada v2.1 validada")
        print(f"   Correcciones sutiles mejoran precisión sin sobrecorregir")
    elif avg_improvement > 5:
        print(f"\n✅ MEJORA SUSTANCIAL - teoría en buen camino")
    else:
        print(f"\n🔧 Necesario más refinamiento en correcciones")
    
    return validation


if __name__ == "__main__":
    # Ejecutar test refinado
    results = test_refined_klein_theory()
    
    print("\n" + "=" * 80)
    print("TEORÍA KLEIN ATÓMICA REFINADA v2.1 COMPLETADA")
    print("Correcciones sutiles calibradas para mayor precisión")
    print("=" * 80)