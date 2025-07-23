"""
Análisis de Velocidades de Degradación Klein - Predicciones Específicas
====================================================================
Basado en el mecanismo nuclear-Klein elucidado, calcula velocidades
de degradación específicas para elementos radioactivos y estables.

HIPÓTESIS: La frecuencia Klein nuclear determina la velocidad
de degradación de elementos a través de oscilaciones 5D.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import hbar, c, m_e, e
from typing import Dict, List, Tuple
import json

# Importar funciones Klein desarrolladas
from FORMULAS_Y_PARAMETROS_CLAVE import (
    nuclear_klein_oscillation, 
    nuclear_degradation_rate_prediction,
    klein_5d_propagation_factor
)

class KleinDegradationAnalyzer:
    """
    Analizador de velocidades de degradación basado en teoría Klein.
    
    Calcula cómo los elementos se degradan según oscilaciones Klein 5D.
    """
    
    def __init__(self):
        """Inicializar con datos nucleares expandidos."""
        self.nuclear_database = self._load_comprehensive_nuclear_data()
        
        # Constantes Klein para degradación
        self.KLEIN_DEGRADATION_CONSTANTS = {
            'topological_factor': 2 * np.pi,  # Factor Klein universal
            'coherence_time': 1e-15,          # Tiempo coherencia nuclear (s)
            'coupling_strength': 1.0,         # Acoplamiento Klein 5D
            'dimensional_factor': 0.5         # Factor reducción dimensional 5D→4D
        }
    
    def _load_comprehensive_nuclear_data(self) -> Dict:
        """Carga base datos nucleares completa para análisis degradación."""
        
        nuclear_data = {
            # Elementos estables (degradación nula teórica)
            'H-1': {
                'Z': 1, 'A': 1, 'N': 0,
                'half_life_years': 'stable',
                'Q_value_keV': 0,
                'binding_energy_MeV': 0,
                'decay_mode': 'stable',
                'element_type': 'stable_light'
            },
            'He-4': {
                'Z': 2, 'A': 4, 'N': 2,
                'half_life_years': 'stable',
                'Q_value_keV': 0,
                'binding_energy_MeV': 28.3,
                'decay_mode': 'stable',
                'element_type': 'stable_light'
            },
            'C-12': {
                'Z': 6, 'A': 12, 'N': 6,
                'half_life_years': 'stable',
                'Q_value_keV': 0,
                'binding_energy_MeV': 92.16,
                'decay_mode': 'stable',
                'element_type': 'stable_medium'
            },
            'Fe-56': {
                'Z': 26, 'A': 56, 'N': 30,
                'half_life_years': 'stable',
                'Q_value_keV': 0,
                'binding_energy_MeV': 492.3,
                'decay_mode': 'stable',
                'element_type': 'stable_heavy'
            },
            
            # Isotópos radioactivos de vida corta (degradación rápida)
            'Tc-99m': {
                'Z': 43, 'A': 99, 'N': 56,
                'half_life_years': 6.9e-6,  # 6 horas
                'Q_value_keV': 140,
                'binding_energy_MeV': 861.1,
                'decay_mode': 'isomeric_transition',
                'element_type': 'medical_isotope'
            },
            'F-18': {
                'Z': 9, 'A': 18, 'N': 9,
                'half_life_years': 1.25e-4,  # 110 minutos
                'Q_value_keV': 633.5,
                'binding_energy_MeV': 137.37,
                'decay_mode': 'beta+',
                'element_type': 'medical_isotope'
            },
            'I-131': {
                'Z': 53, 'A': 131, 'N': 78,
                'half_life_years': 9.12e-3,  # 8 días
                'Q_value_keV': 970.8,
                'binding_energy_MeV': 1072.8,
                'decay_mode': 'beta-',
                'element_type': 'medical_isotope'
            },
            
            # Isotópos radioactivos de vida media (degradación moderada)
            'C-14': {
                'Z': 6, 'A': 14, 'N': 8,
                'half_life_years': 5730,
                'Q_value_keV': 156.5,
                'binding_energy_MeV': 105.29,
                'decay_mode': 'beta-',
                'element_type': 'dating_isotope'
            },
            'K-40': {
                'Z': 19, 'A': 40, 'N': 21,
                'half_life_years': 1.25e9,
                'Q_value_keV': 1311,
                'binding_energy_MeV': 341.5,
                'decay_mode': 'beta- + electron_capture',
                'element_type': 'geological_isotope'
            },
            
            # Isotópos radioactivos de vida larga (degradación lenta)
            'U-238': {
                'Z': 92, 'A': 238, 'N': 146,
                'half_life_years': 4.47e9,
                'Q_value_keV': 4270,
                'binding_energy_MeV': 1801.7,
                'decay_mode': 'alpha',
                'element_type': 'geological_heavy'
            },
            'U-235': {
                'Z': 92, 'A': 235, 'N': 143,
                'half_life_years': 7.04e8,
                'Q_value_keV': 4678,
                'binding_energy_MeV': 1783.9,
                'decay_mode': 'alpha + fission',
                'element_type': 'fissile_material'
            },
            'Pu-239': {
                'Z': 94, 'A': 239, 'N': 145,
                'half_life_years': 24110,
                'Q_value_keV': 5244,
                'binding_energy_MeV': 1806.5,
                'decay_mode': 'alpha',
                'element_type': 'fissile_material'
            },
            
            # Elementos transuránicos sintéticos
            'Es-252': {
                'Z': 99, 'A': 252, 'N': 153,
                'half_life_years': 1.29,  # 472 días
                'Q_value_keV': 6760,
                'binding_energy_MeV': 1860.2,
                'decay_mode': 'alpha + spontaneous_fission',
                'element_type': 'synthetic_transuranic'
            },
            'Fm-257': {
                'Z': 100, 'A': 257, 'N': 157,
                'half_life_years': 1.15e-1,  # 100.5 días
                'Q_value_keV': 7010,
                'binding_energy_MeV': 1881.6,
                'decay_mode': 'alpha',
                'element_type': 'synthetic_transuranic'
            }
        }
        
        return nuclear_data
    
    def calculate_klein_degradation_rates(self) -> Dict:
        """
        Calcula velocidades degradación Klein para todos los elementos.
        
        Aplica mecanismo nuclear-Klein a predicción de degradación específica.
        """
        print("=" * 80)
        print("ANÁLISIS VELOCIDADES DEGRADACIÓN KLEIN")
        print("=" * 80)
        
        print("\nHIPÓTESIS:")
        print("• Elementos estables: degradación Klein nula (ω = 0)")
        print("• Elementos inestables: degradación ∝ frecuencia oscilación Klein")
        print("• Constante degradación universal Klein: λ = ω_Klein")
        print("• Tiempo característico: τ = 1/λ")
        
        degradation_results = {}
        
        print(f"\n{'Elemento':<10} {'Vida Media':<12} {'λ_Klein(Hz)':<12} {'τ_Klein(años)':<15} {'Categoría':<15}")
        print("-" * 75)
        
        for element_name, data in self.nuclear_database.items():
            half_life = data['half_life_years']
            
            if half_life == 'stable':
                # Elementos estables: degradación Klein teóricamente nula
                degradation_data = {
                    'degradation_constant_hz': 0.0,
                    'characteristic_time_years': float('inf'),
                    'degradation_category': 'stable',
                    'klein_effect': 'none'
                }
                
                lifetime_str = "∞"
                lambda_str = "0.0"
                tau_str = "∞"
                
            else:
                # Elementos inestables: calcular degradación Klein
                oscillation_data = nuclear_klein_oscillation(
                    half_life, data['Q_value_keV'], 
                    data['binding_energy_MeV'], data['decay_mode']
                )
                
                degradation_data = nuclear_degradation_rate_prediction(
                    half_life, oscillation_data
                )
                
                # Clasificar categoría degradación
                tau_years = degradation_data['characteristic_time_years']
                if tau_years < 1:
                    degradation_data['degradation_category'] = 'very_fast'
                    degradation_data['klein_effect'] = 'strong'
                elif tau_years < 1000:
                    degradation_data['degradation_category'] = 'fast'
                    degradation_data['klein_effect'] = 'moderate'
                elif tau_years < 1e6:
                    degradation_data['degradation_category'] = 'medium'
                    degradation_data['klein_effect'] = 'weak'
                else:
                    degradation_data['degradation_category'] = 'slow'
                    degradation_data['klein_effect'] = 'minimal'
                
                # Formatear strings
                if half_life > 1e6:
                    lifetime_str = f"{half_life/1e6:.1f}Ma"
                elif half_life > 1e3:
                    lifetime_str = f"{half_life/1e3:.1f}ka"
                elif half_life > 1:
                    lifetime_str = f"{half_life:.1f}a"
                else:
                    lifetime_str = f"{half_life*365:.1f}d"
                
                lambda_klein = degradation_data['degradation_constant_hz']
                lambda_str = f"{lambda_klein:.2e}"
                
                tau_klein = degradation_data['characteristic_time_years']
                if tau_klein > 1e6:
                    tau_str = f"{tau_klein/1e6:.1f}Ma"
                elif tau_klein > 1e3:
                    tau_str = f"{tau_klein/1e3:.1f}ka"
                elif tau_klein > 1:
                    tau_str = f"{tau_klein:.1f}a"
                else:
                    tau_str = f"{tau_klein*365:.1f}d"
            
            degradation_results[element_name] = degradation_data
            degradation_results[element_name]['element_data'] = data
            
            category = degradation_data['degradation_category']
            print(f"{element_name:<10} {lifetime_str:<12} {lambda_str:<12} {tau_str:<15} {category:<15}")
        
        return degradation_results
    
    def analyze_degradation_patterns(self, degradation_results: Dict) -> Dict:
        """Analiza patrones en velocidades degradación Klein."""
        
        print("\n" + "=" * 80)
        print("PATRONES DEGRADACIÓN KLEIN")
        print("=" * 80)
        
        # Agrupar por categoría degradación
        categories = {}
        for element, data in degradation_results.items():
            category = data['degradation_category']
            if category not in categories:
                categories[category] = []
            categories[category].append((element, data))
        
        print(f"\n🔬 ANÁLISIS POR CATEGORÍA:")
        print("-" * 30)
        
        category_analysis = {}
        for category, elements in categories.items():
            print(f"\n{category.upper()}:")
            print(f"  Elementos: {len(elements)}")
            
            # Calcular estadísticas
            if category != 'stable':
                lambdas = [data['degradation_constant_hz'] for _, data in elements]
                taus = [data['characteristic_time_years'] for _, data in elements if data['characteristic_time_years'] != float('inf')]
                
                avg_lambda = np.mean(lambdas) if lambdas else 0
                avg_tau = np.mean(taus) if taus else float('inf')
                
                print(f"  λ promedio: {avg_lambda:.2e} Hz")
                print(f"  τ promedio: {avg_tau:.1e} años")
                
                # Elementos específicos
                element_names = [elem for elem, _ in elements]
                print(f"  Ejemplos: {', '.join(element_names[:3])}")
                
                category_analysis[category] = {
                    'count': len(elements),
                    'avg_lambda': avg_lambda,
                    'avg_tau': avg_tau,
                    'elements': element_names
                }
            else:
                print(f"  λ Klein: 0.0 Hz (sin degradación)")
                print(f"  τ Klein: ∞ años (estables)")
                
                category_analysis[category] = {
                    'count': len(elements),
                    'avg_lambda': 0.0,
                    'avg_tau': float('inf'),
                    'elements': [elem for elem, _ in elements]
                }
        
        return category_analysis
    
    def predict_universal_degradation_constant(self, degradation_results: Dict) -> Dict:
        """
        Busca constante universal degradación Klein.
        
        HIPÓTESIS: Existe una constante Klein que relaciona
        frecuencia nuclear con velocidad degradación universal.
        """
        print("\n" + "=" * 80)
        print("BÚSQUEDA CONSTANTE UNIVERSAL DEGRADACIÓN KLEIN")
        print("=" * 80)
        
        print("\nHIPÓTESIS CONSTANTE UNIVERSAL:")
        print("λ_degradación = G_Klein × ω_nuclear × f(Z, A, tipo_decaimiento)")
        print("donde G_Klein = constante topológica Klein universal")
        
        # Extraer datos para análisis
        unstable_elements = []
        for element, data in degradation_results.items():
            if data['degradation_category'] != 'stable':
                element_data = data['element_data']
                
                # Calcular frecuencia nuclear Klein
                half_life = element_data['half_life_years']
                omega_nuclear = 2 * np.pi / (half_life * 365.25 * 24 * 3600)
                
                lambda_degradation = data['degradation_constant_hz']
                
                # Ratio λ/ω para buscar constante
                if omega_nuclear > 0:
                    ratio = lambda_degradation / omega_nuclear
                else:
                    ratio = 0
                
                unstable_elements.append({
                    'element': element,
                    'omega_nuclear': omega_nuclear,
                    'lambda_degradation': lambda_degradation,
                    'ratio_lambda_omega': ratio,
                    'Z': element_data['Z'],
                    'A': element_data['A'],
                    'decay_mode': element_data['decay_mode'],
                    'half_life': half_life
                })
        
        # Analizar ratios para encontrar constante
        ratios = [elem['ratio_lambda_omega'] for elem in unstable_elements if elem['ratio_lambda_omega'] > 0]
        
        if ratios:
            G_klein_mean = np.mean(ratios)
            G_klein_std = np.std(ratios)
            G_klein_median = np.median(ratios)
            
            print(f"\n📊 ANÁLISIS CONSTANTE G_Klein:")
            print(f"  Elementos analizados: {len(ratios)}")
            print(f"  G_Klein promedio: {G_klein_mean:.3f}")
            print(f"  G_Klein mediana: {G_klein_median:.3f}")
            print(f"  Desviación estándar: {G_klein_std:.3f}")
            print(f"  Coeficiente variación: {G_klein_std/G_klein_mean*100:.1f}%")
            
            # Constante teórica Klein esperada
            G_klein_theoretical = self.KLEIN_DEGRADATION_CONSTANTS['topological_factor'] / (2 * np.pi)
            print(f"  G_Klein teórico: {G_klein_theoretical:.3f}")
            print(f"  Diferencia experimental: {abs(G_klein_mean - G_klein_theoretical):.3f}")
            
            # Validación constante por tipo decaimiento
            print(f"\n🔬 VALIDACIÓN POR TIPO DECAIMIENTO:")
            decay_types = {}
            for elem in unstable_elements:
                decay_mode = elem['decay_mode']
                if decay_mode not in decay_types:
                    decay_types[decay_mode] = []
                decay_types[decay_mode].append(elem['ratio_lambda_omega'])
            
            for decay_mode, ratios_mode in decay_types.items():
                if ratios_mode:
                    avg_ratio = np.mean(ratios_mode)
                    print(f"  {decay_mode}: G_Klein = {avg_ratio:.3f} (n={len(ratios_mode)})")
            
            universal_constant = {
                'G_klein_experimental': G_klein_mean,
                'G_klein_theoretical': G_klein_theoretical,
                'uncertainty': G_klein_std,
                'validation_score': 1.0 - abs(G_klein_mean - G_klein_theoretical),
                'decay_mode_consistency': decay_types,
                'is_universal': G_klein_std / G_klein_mean < 0.5  # <50% variación
            }
        else:
            universal_constant = {
                'G_klein_experimental': None,
                'G_klein_theoretical': 1.0,
                'uncertainty': None,
                'validation_score': 0.0,
                'is_universal': False
            }
        
        return universal_constant
    
    def plot_degradation_analysis(self, degradation_results: Dict, universal_constant: Dict):
        """Genera gráficas del análisis degradación Klein."""
        
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        fig.suptitle('Análisis Velocidades Degradación Klein', fontsize=16, fontweight='bold')
        
        # Extraer datos para gráficas
        elements = []
        half_lives = []
        lambdas = []
        taus = []
        categories = []
        element_types = []
        
        for element, data in degradation_results.items():
            if data['degradation_category'] != 'stable':
                elements.append(element)
                element_data = data['element_data']
                half_lives.append(element_data['half_life_years'])
                lambdas.append(data['degradation_constant_hz'])
                taus.append(data['characteristic_time_years'])
                categories.append(data['degradation_category'])
                element_types.append(element_data['element_type'])
        
        # Plot 1: Vida media vs constante degradación
        ax1 = axes[0, 0]
        
        if half_lives and lambdas:
            ax1.loglog(half_lives, lambdas, 'bo', markersize=8, alpha=0.7)
            
            # Línea teórica λ = ω = 2π/τ
            x_theory = np.logspace(min(np.log10(half_lives)), max(np.log10(half_lives)), 100)
            y_theory = 2 * np.pi / (x_theory * 365.25 * 24 * 3600)
            ax1.plot(x_theory, y_theory, 'r-', linewidth=2, label='λ = 2π/τ teórica')
            
            # Etiquetas
            for i, elem in enumerate(elements):
                ax1.annotate(elem, (half_lives[i], lambdas[i]),
                            xytext=(5, 5), textcoords='offset points', fontsize=8)
            
            ax1.set_xlabel('Vida Media (años)')
            ax1.set_ylabel('Constante Degradación Klein (Hz)')
            ax1.set_title('Vida Media vs Constante Degradación')
            ax1.legend()
            ax1.grid(True, alpha=0.3)
        
        # Plot 2: Tiempo característico vs vida media
        ax2 = axes[0, 1]
        
        if half_lives and taus:
            # Filtrar infinitos
            finite_indices = [i for i, tau in enumerate(taus) if tau != float('inf')]
            half_lives_finite = [half_lives[i] for i in finite_indices]
            taus_finite = [taus[i] for i in finite_indices]
            
            if half_lives_finite and taus_finite:
                ax2.loglog(half_lives_finite, taus_finite, 'go', markersize=8, alpha=0.7)
                
                # Línea τ = τ_vida_media / ln(2)
                x_theory = np.logspace(min(np.log10(half_lives_finite)), max(np.log10(half_lives_finite)), 100)
                y_theory = x_theory / np.log(2)
                ax2.plot(x_theory, y_theory, 'r-', linewidth=2, label='τ = τ_vida/ln(2)')
                
                ax2.set_xlabel('Vida Media (años)')
                ax2.set_ylabel('Tiempo Característico Klein (años)')
                ax2.set_title('Vida Media vs Tiempo Característico')
                ax2.legend()
                ax2.grid(True, alpha=0.3)
        
        # Plot 3: Distribución por categoría
        ax3 = axes[0, 2]
        
        category_counts = {}
        for cat in categories:
            category_counts[cat] = category_counts.get(cat, 0) + 1
        
        if category_counts:
            cats = list(category_counts.keys())
            counts = list(category_counts.values())
            colors = ['red', 'orange', 'yellow', 'green'][:len(cats)]
            
            bars = ax3.bar(cats, counts, color=colors, alpha=0.7)
            ax3.set_ylabel('Número Elementos')
            ax3.set_title('Distribución por Categoría Degradación')
            ax3.tick_params(axis='x', rotation=45)
            
            # Valores en barras
            for bar, count in zip(bars, counts):
                ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                        str(count), ha='center', va='bottom', fontweight='bold')
        
        # Plot 4: Constante universal G_Klein
        ax4 = axes[1, 0]
        
        if universal_constant['G_klein_experimental'] is not None:
            G_exp = universal_constant['G_klein_experimental']
            G_theo = universal_constant['G_klein_theoretical']
            uncertainty = universal_constant['uncertainty']
            
            categories_plot = ['Experimental', 'Teórico']
            values = [G_exp, G_theo]
            errors = [uncertainty, 0]
            colors = ['blue', 'red']
            
            bars = ax4.bar(categories_plot, values, yerr=errors, capsize=5, 
                          color=colors, alpha=0.7)
            ax4.set_ylabel('Constante G_Klein')
            ax4.set_title('Constante Universal Klein')
            
            # Valores en barras
            for bar, val in zip(bars, values):
                ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                        f'{val:.3f}', ha='center', va='bottom', fontweight='bold')
        
        # Plot 5: Análisis por tipo elemento
        ax5 = axes[1, 1]
        
        type_counts = {}
        for elem_type in element_types:
            type_counts[elem_type] = type_counts.get(elem_type, 0) + 1
        
        if type_counts:
            types = list(type_counts.keys())
            counts = list(type_counts.values())
            
            # Crear gráfica circular
            ax5.pie(counts, labels=types, autopct='%1.1f%%', startangle=90)
            ax5.set_title('Distribución por Tipo Elemento')
        
        # Plot 6: Resumen insights
        ax6 = axes[1, 2]
        ax6.axis('off')
        
        # Texto resumen
        if universal_constant['G_klein_experimental'] is not None:
            G_exp = universal_constant['G_klein_experimental']
            is_universal = universal_constant['is_universal']
            
            insights_text = f"""
INSIGHTS DEGRADACIÓN KLEIN:

• Constante Universal G_Klein:
  Experimental: {G_exp:.3f}
  Teórico: {universal_constant['G_klein_theoretical']:.3f}
  
• Universalidad: {'SÍ' if is_universal else 'NO'}

• Elementos analizados: {len(elements)}

• Categorías identificadas:
  - Degradación muy rápida
  - Degradación rápida  
  - Degradación media
  - Degradación lenta

• Predicción: λ = G_Klein × ω
            """
        else:
            insights_text = """
ANÁLISIS DEGRADACIÓN KLEIN:

• Insuficientes datos para
  constante universal
  
• Necesario más elementos
  radioactivos
  
• Patrones identificados en
  categorías degradación
  
• Framework establecido
  para predicciones
            """
        
        ax6.text(0.05, 0.95, insights_text, transform=ax6.transAxes, fontsize=10,
                verticalalignment='top', fontfamily='monospace',
                bbox=dict(boxstyle='round', facecolor='lightcyan', alpha=0.8))
        
        plt.tight_layout()
        plt.savefig('klein_degradation_rate_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def save_degradation_results(self, degradation_results: Dict, universal_constant: Dict):
        """Guarda resultados análisis degradación."""
        
        # Preparar datos para guardar
        results_to_save = {
            'analysis_type': 'klein_degradation_rates',
            'timestamp': '2025-01-08',
            'elements_analyzed': len(degradation_results),
            'universal_constant': universal_constant,
            'degradation_data': {}
        }
        
        # Simplificar datos para JSON
        for element, data in degradation_results.items():
            results_to_save['degradation_data'][element] = {
                'degradation_constant_hz': data['degradation_constant_hz'],
                'characteristic_time_years': data['characteristic_time_years'] if data['characteristic_time_years'] != float('inf') else 'infinite',
                'degradation_category': data['degradation_category'],
                'klein_effect': data['klein_effect'],
                'element_type': data['element_data']['element_type'],
                'decay_mode': data['element_data']['decay_mode']
            }
        
        # Guardar
        with open('klein_degradation_analysis_results.json', 'w') as f:
            json.dump(results_to_save, f, indent=2)
        
        print(f"\n💾 Resultados guardados: klein_degradation_analysis_results.json")
        return results_to_save


def run_klein_degradation_analysis():
    """Ejecuta análisis completo velocidades degradación Klein."""
    
    print("\n" + "⚛️" * 40)
    print("ANÁLISIS VELOCIDADES DEGRADACIÓN KLEIN")
    print("Predicciones basadas en mecanismo nuclear-Klein elucidado")
    print("⚛️" * 40)
    
    # Crear analizador
    analyzer = KleinDegradationAnalyzer()
    
    # Calcular velocidades degradación
    degradation_results = analyzer.calculate_klein_degradation_rates()
    
    # Analizar patrones
    patterns = analyzer.analyze_degradation_patterns(degradation_results)
    
    # Buscar constante universal
    universal_constant = analyzer.predict_universal_degradation_constant(degradation_results)
    
    # Generar gráficas
    print("\nGenerando gráficas análisis degradación...")
    analyzer.plot_degradation_analysis(degradation_results, universal_constant)
    
    # Guardar resultados
    saved_results = analyzer.save_degradation_results(degradation_results, universal_constant)
    
    # Resumen final
    print("\n" + "=" * 80)
    print("RESUMEN ANÁLISIS DEGRADACIÓN KLEIN")
    print("=" * 80)
    
    stable_count = sum(1 for data in degradation_results.values() if data['degradation_category'] == 'stable')
    unstable_count = len(degradation_results) - stable_count
    
    print(f"\n📊 ELEMENTOS ANALIZADOS:")
    print(f"  Total: {len(degradation_results)}")
    print(f"  Estables: {stable_count}")
    print(f"  Inestables: {unstable_count}")
    
    print(f"\n🔬 CATEGORÍAS DEGRADACIÓN:")
    for category, data in patterns.items():
        if category != 'stable':
            print(f"  {category.upper()}: {data['count']} elementos, τ={data['avg_tau']:.1e} años")
        else:
            print(f"  {category.upper()}: {data['count']} elementos, sin degradación")
    
    if universal_constant['G_klein_experimental'] is not None:
        print(f"\n📐 CONSTANTE UNIVERSAL KLEIN:")
        print(f"  G_Klein experimental: {universal_constant['G_klein_experimental']:.3f}")
        print(f"  G_Klein teórico: {universal_constant['G_klein_theoretical']:.3f}")
        print(f"  Universalidad: {'CONFIRMADA' if universal_constant['is_universal'] else 'PARCIAL'}")
        print(f"  Precisión: {universal_constant['validation_score']*100:.1f}%")
    else:
        print(f"\n📐 CONSTANTE UNIVERSAL KLEIN: Datos insuficientes")
    
    print(f"\n🎯 APLICACIONES PRÁCTICAS:")
    print(f"  • Predicción vida útil materiales radioactivos")
    print(f"  • Optimización isotópos médicos")
    print(f"  • Planificación almacenamiento residuos nucleares")
    print(f"  • Diseño elementos sintéticos estables")
    
    print(f"\n📈 Gráficas: klein_degradation_rate_analysis.png")
    
    return {
        'degradation_results': degradation_results,
        'patterns': patterns,
        'universal_constant': universal_constant,
        'saved_results': saved_results
    }


if __name__ == "__main__":
    # Ejecutar análisis completo
    results = run_klein_degradation_analysis()
    
    print("\n" + "=" * 80)
    print("¡ANÁLISIS DEGRADACIÓN KLEIN COMPLETADO!")
    print("Velocidades degradación calculadas según mecanismo nuclear-Klein")
    print("=" * 80)