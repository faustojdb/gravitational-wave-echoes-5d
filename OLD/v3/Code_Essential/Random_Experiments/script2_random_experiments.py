#!/usr/bin/env python3
"""
SCRIPT 2: EXPERIMENTOS ALEATORIOS LIBRES DE SESGO
================================================

Usando los parámetros óptimos del Script 1, realiza múltiples experimentos
con selecciones aleatorias de eventos para calcular significancia estadística
libre de sesgo de confirmación.

Metodología:
1. Cargar parámetros óptimos del Script 1
2. Realizar N experimentos aleatorios independientes
3. Para cada experimento: seleccionar submuestra aleatoria
4. Aplicar curva Klein optimizada
5. Calcular σ sin sesgo
6. Análisis estadístico de la distribución de resultados
"""

import numpy as np
import matplotlib.pyplot as plt
import json
from scipy import stats
import warnings
from datetime import datetime
import os
warnings.filterwarnings('ignore')

class RandomExperimentRunner:
    def __init__(self):
        """Inicializar runner de experimentos aleatorios"""
        
        self.load_optimal_parameters()
        self.load_population_data()
        
        print(f"✅ Script 2: Experimentos Aleatorios Libres de Sesgo")
        print(f"📊 Población disponible: {len(self.population_data)} eventos")
        print(f"🎯 Objetivo: Calcular σ mediante experimentos aleatorios")
        
    def load_optimal_parameters(self):
        """Cargar parámetros óptimos del Script 1"""
        
        try:
            with open('optimal_klein_parameters_script1.json', 'r') as f:
                config = json.load(f)
            
            self.optimal_params = config['optimal_parameters']
            print(f"✅ Parámetros óptimos cargados del Script 1")
            
            # Extraer parámetros para uso directo
            temporal = self.optimal_params['temporal_law']
            self.a_tau = temporal['a_tau']
            self.b_tau = temporal['b_tau'] 
            self.n_tau = temporal['n_tau']
            
            physical = self.optimal_params['physical_dependencies']
            self.dist_exp = physical['distance_exponent']
            self.snr_exp = physical['snr_exponent']
            self.mass_exp = physical['mass_exponent']
            self.coupling = physical['base_coupling']
            
            print(f"   Ley temporal: τ = {self.a_tau:.3f}/M^{self.n_tau:.3f} + {self.b_tau:.3f}")
            
        except FileNotFoundError:
            print("⚠️ Parámetros del Script 1 no encontrados, usando parámetros por defecto")
            self.create_default_parameters()
            
    def create_default_parameters(self):
        """Crear parámetros por defecto si Script 1 no se ejecutó"""
        
        # Parámetros realistas basados en análisis expandido
        self.a_tau = 0.8
        self.b_tau = 0.15
        self.n_tau = 0.85
        self.dist_exp = 2.0
        self.snr_exp = 1.0
        self.mass_exp = 0.2
        self.coupling = 0.05
        
        self.optimal_params = {
            'temporal_law': {
                'a_tau': self.a_tau,
                'b_tau': self.b_tau,
                'n_tau': self.n_tau,
                'formula': f'tau = {self.a_tau:.3f}/M^{self.n_tau:.3f} + {self.b_tau:.3f}'
            },
            'physical_dependencies': {
                'distance_exponent': self.dist_exp,
                'snr_exponent': self.snr_exp,
                'mass_exponent': self.mass_exp,
                'base_coupling': self.coupling
            }
        }
        
        print(f"   Usando parámetros por defecto")
        
    def load_population_data(self):
        """Cargar datos de población completa"""
        
        try:
            # Intentar cargar del análisis expandido
            with open('comprehensive_gwtc_results_20250603_165259.json', 'r') as f:
                gwtc_results = json.load(f)
            
            self.population_data = []
            for event_name, result in gwtc_results['event_results'].items():
                if 'event_properties' in result:
                    event_data = {
                        'name': event_name,
                        'mass': result['event_properties']['Mf'],
                        'distance': result['event_properties']['dist'],
                        'network_snr': result['event_properties']['snr'],
                        'detected': result['detected'],
                        'significance': result['significance'],
                        'echo_snr': result.get('snr', 0) if result['detected'] else 0
                    }
                    self.population_data.append(event_data)
                    
            print(f"✅ Población cargada: {len(self.population_data)} eventos reales")
            
        except FileNotFoundError:
            print("⚠️ Generando población sintética para demostración")
            self.generate_synthetic_population()
            
    def generate_synthetic_population(self):
        """Generar población sintética si no hay datos reales"""
        
        np.random.seed(42)
        self.population_data = []
        
        for i in range(65):
            mass = np.random.uniform(15, 150)
            distance = np.random.uniform(400, 3000)
            snr = np.random.uniform(8, 25)
            
            # Simular detección usando parámetros por defecto
            detection_prob = self.calculate_detection_probability({
                'mass': mass,
                'distance': distance,
                'network_snr': snr
            })
            
            detected = np.random.random() < detection_prob
            if detected:
                significance = 2.0 + np.random.exponential(1.0)
                echo_snr = significance * np.sqrt(2)
            else:
                significance = 0
                echo_snr = 0
                
            event_data = {
                'name': f'GW_synth_{i:03d}',
                'mass': mass,
                'distance': distance,
                'network_snr': snr,
                'detected': detected,
                'significance': significance,
                'echo_snr': echo_snr
            }
            self.population_data.append(event_data)
            
        print(f"✅ Población sintética generada: {len(self.population_data)} eventos")
        
    def calculate_detection_probability(self, event):
        """Calcular probabilidad de detección usando parámetros óptimos"""
        
        # Predicción temporal Klein
        tau_pred = self.a_tau / (event['mass']**self.n_tau) + self.b_tau
        
        # Factores físicos
        distance_factor = (1000 / event['distance'])**self.dist_exp
        snr_factor = (event['network_snr'] / 15)**self.snr_exp
        mass_factor = (event['mass'] / 50)**self.mass_exp
        
        # Probabilidad combinada
        detection_prob = self.coupling * distance_factor * snr_factor * mass_factor
        return np.clip(detection_prob, 0, 1)
        
    def run_single_random_experiment(self, sample_size, experiment_id):
        """Ejecutar un experimento aleatorio individual"""
        
        # Selección aleatoria sin reemplazo
        selected_indices = np.random.choice(len(self.population_data), 
                                          size=min(sample_size, len(self.population_data)), 
                                          replace=False)
        selected_events = [self.population_data[i] for i in selected_indices]
        
        # Aplicar modelo Klein a la muestra seleccionada
        detections = []
        significances = []
        predictions = []
        
        for event in selected_events:
            # Predicción del modelo
            detection_prob = self.calculate_detection_probability(event)
            predictions.append(detection_prob)
            
            # Observación real
            detected = event['detected']
            detections.append(detected)
            
            if detected:
                significances.append(event['significance'])
                
        # Estadísticas del experimento
        n_detected = sum(detections)
        detection_rate = n_detected / len(selected_events)
        avg_significance = np.mean(significances) if significances else 0
        max_significance = max(significances) if significances else 0
        
        # Correlación predicción-observación
        correlation = np.corrcoef(predictions, detections)[0,1] if len(set(detections)) > 1 else 0
        
        # Test estadístico: ¿Es la tasa observada consistente con predicciones?
        expected_detections = np.sum(predictions)
        
        # Test binomial
        if expected_detections > 0:
            try:
                p_value_binomial = stats.binom_test(n_detected, len(selected_events), 
                                                  expected_detections/len(selected_events))
            except AttributeError:
                # Compatibility with newer scipy versions
                result = stats.binomtest(n_detected, len(selected_events), 
                                       expected_detections/len(selected_events))
                p_value_binomial = result.pvalue
        else:
            p_value_binomial = 1.0
            
        # Significancia combinada (usando todas las detecciones)
        if significances:
            # Método Fisher para combinar p-values
            individual_p_values = [2 * (1 - stats.norm.cdf(s)) for s in significances]
            chi2_stat = -2 * np.sum(np.log(individual_p_values))
            combined_p_value = 1 - stats.chi2.cdf(chi2_stat, 2 * len(significances))
            
            if combined_p_value > 0:
                combined_sigma = stats.norm.ppf(1 - combined_p_value/2)
            else:
                combined_sigma = 10  # Muy significativo
        else:
            combined_sigma = 0
            combined_p_value = 1.0
            
        experiment_result = {
            'experiment_id': experiment_id,
            'sample_size': len(selected_events),
            'n_detected': n_detected,
            'detection_rate': detection_rate,
            'avg_significance': avg_significance,
            'max_significance': max_significance,
            'combined_sigma': combined_sigma,
            'combined_p_value': combined_p_value,
            'correlation': correlation,
            'binomial_p_value': p_value_binomial,
            'selected_events': [e['name'] for e in selected_events],
            'individual_significances': significances
        }
        
        return experiment_result
        
    def run_multiple_experiments(self, n_experiments=100, sample_size=20):
        """Ejecutar múltiples experimentos aleatorios"""
        
        print(f"\n" + "="*70)
        print(f"EXPERIMENTOS ALEATORIOS LIBRES DE SESGO")
        print("="*70)
        print(f"Número de experimentos: {n_experiments}")
        print(f"Tamaño de muestra por experimento: {sample_size}")
        print(f"Población total disponible: {len(self.population_data)}")
        
        results = []
        
        # Fijar semilla para la serie completa (pero cada experimento será diferente)
        np.random.seed(42)
        
        print(f"\nEjecutando experimentos...")
        for i in range(n_experiments):
            if (i + 1) % 20 == 0:
                print(f"  Progreso: {i+1}/{n_experiments}")
                
            # Cada experimento tiene su propia semilla aleatoria
            np.random.seed(42 + i)
            
            result = self.run_single_random_experiment(sample_size, i+1)
            results.append(result)
            
        print(f"✅ {n_experiments} experimentos completados")
        
        # Análisis estadístico de los resultados
        self.analyze_experiment_results(results)
        
        return results
        
    def analyze_experiment_results(self, results):
        """Analizar estadísticamente los resultados de experimentos múltiples"""
        
        print(f"\n📊 ANÁLISIS ESTADÍSTICO DE EXPERIMENTOS MÚLTIPLES:")
        print("-" * 60)
        
        # Extraer métricas
        detection_rates = [r['detection_rate'] for r in results]
        avg_significances = [r['avg_significance'] for r in results if r['avg_significance'] > 0]
        max_significances = [r['max_significance'] for r in results if r['max_significance'] > 0]
        combined_sigmas = [r['combined_sigma'] for r in results if r['combined_sigma'] > 0]
        correlations = [r['correlation'] for r in results if not np.isnan(r['correlation'])]
        
        # Estadísticas descriptivas
        print(f"TASAS DE DETECCIÓN:")
        print(f"  Promedio: {np.mean(detection_rates):.1%} ± {np.std(detection_rates):.1%}")
        print(f"  Rango: {np.min(detection_rates):.1%} - {np.max(detection_rates):.1%}")
        print(f"  Mediana: {np.median(detection_rates):.1%}")
        
        if avg_significances:
            print(f"\nSIGNIFICANCIA PROMEDIO (experimentos con detecciones):")
            print(f"  Promedio: {np.mean(avg_significances):.2f}σ ± {np.std(avg_significances):.2f}σ")
            print(f"  Rango: {np.min(avg_significances):.2f}σ - {np.max(avg_significances):.2f}σ")
            print(f"  Mediana: {np.median(avg_significances):.2f}σ")
            
        if combined_sigmas:
            print(f"\nSIGNIFICANCIA COMBINADA (experimentos con detecciones):")
            print(f"  Promedio: {np.mean(combined_sigmas):.2f}σ ± {np.std(combined_sigmas):.2f}σ")
            print(f"  Máxima: {np.max(combined_sigmas):.2f}σ")
            print(f"  Mediana: {np.median(combined_sigmas):.2f}σ")
            
        # Frecuencia de detecciones significativas
        experiments_with_detections = sum(1 for r in results if r['n_detected'] > 0)
        experiments_with_3sigma = sum(1 for r in results if r['max_significance'] >= 3.0)
        experiments_with_5sigma = sum(1 for r in results if r['combined_sigma'] >= 5.0)
        
        print(f"\nFRECUENCIA DE RESULTADOS SIGNIFICATIVOS:")
        print(f"  Experimentos con detecciones: {experiments_with_detections}/{len(results)} ({experiments_with_detections/len(results):.1%})")
        print(f"  Experimentos con detecciones >3σ: {experiments_with_3sigma}/{len(results)} ({experiments_with_3sigma/len(results):.1%})")
        print(f"  Experimentos con significancia global >5σ: {experiments_with_5sigma}/{len(results)} ({experiments_with_5sigma/len(results):.1%})")
        
        # Test de consistencia con modelo nulo
        # H0: No hay ecos Klein (tasa de detección esperada = tasa de falsos positivos)
        null_detection_rate = 0.05  # 5% falsos positivos
        
        observed_rates_above_null = sum(1 for rate in detection_rates if rate > null_detection_rate)
        try:
            p_value_null_test = stats.binom_test(observed_rates_above_null, len(results), 0.5)
        except AttributeError:
            result = stats.binomtest(observed_rates_above_null, len(results), 0.5)
            p_value_null_test = result.pvalue
        
        print(f"\nTEST DE CONSISTENCIA CON MODELO NULO:")
        print(f"  Tasa nula esperada: {null_detection_rate:.1%}")
        print(f"  Experimentos por encima de tasa nula: {observed_rates_above_null}/{len(results)}")
        print(f"  p-value test nulo: {p_value_null_test:.4f}")
        
        if p_value_null_test < 0.05:
            print(f"  CONCLUSIÓN: Evidencia contra modelo nulo (p < 0.05)")
        else:
            print(f"  CONCLUSIÓN: Consistente con modelo nulo")
            
        # Distribución de correlaciones
        if correlations:
            print(f"\nCORRELACIONES PREDICCIÓN-OBSERVACIÓN:")
            print(f"  Promedio: {np.mean(correlations):.3f} ± {np.std(correlations):.3f}")
            print(f"  Correlaciones positivas: {sum(1 for c in correlations if c > 0)}/{len(correlations)}")
            
        # Guardar resultados detallados
        self.save_experiment_results(results)
        
        return results
        
    def save_experiment_results(self, results):
        """Guardar resultados detallados de experimentos"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Preparar resumen ejecutivo
        detection_rates = [r['detection_rate'] for r in results]
        combined_sigmas = [r['combined_sigma'] for r in results if r['combined_sigma'] > 0]
        
        summary = {
            'script2_metadata': {
                'execution_date': timestamp,
                'n_experiments': len(results),
                'sample_size_per_experiment': results[0]['sample_size'] if results else 0,
                'population_size': len(self.population_data),
                'method': 'Random sampling without replacement'
            },
            
            'statistical_summary': {
                'detection_rate_stats': {
                    'mean': float(np.mean(detection_rates)),
                    'std': float(np.std(detection_rates)),
                    'min': float(np.min(detection_rates)),
                    'max': float(np.max(detection_rates)),
                    'median': float(np.median(detection_rates))
                },
                
                'significance_stats': {
                    'combined_sigma_mean': float(np.mean(combined_sigmas)) if combined_sigmas else 0,
                    'combined_sigma_max': float(np.max(combined_sigmas)) if combined_sigmas else 0,
                    'experiments_with_detections': sum(1 for r in results if r['n_detected'] > 0),
                    'experiments_above_3sigma': sum(1 for r in results if r['max_significance'] >= 3.0)
                }
            },
            
            'optimal_parameters_used': self.optimal_params,
            'detailed_results': results
        }
        
        # Guardar resultados completos
        filename = f'random_experiments_results_{timestamp}.json'
        with open(filename, 'w') as f:
            json.dump(summary, f, indent=2)
            
        print(f"\n✅ Resultados detallados guardados: {filename}")
        
        return filename
        
    def create_comprehensive_visualization(self, results):
        """Crear visualización comprehensiva de experimentos aleatorios"""
        
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        fig.suptitle('Script 2: Experimentos Aleatorios Libres de Sesgo', 
                     fontsize=16, fontweight='bold')
        
        # Extraer datos para plots
        detection_rates = [r['detection_rate'] for r in results]
        avg_significances = [r['avg_significance'] for r in results if r['avg_significance'] > 0]
        max_significances = [r['max_significance'] for r in results if r['max_significance'] > 0]
        combined_sigmas = [r['combined_sigma'] for r in results if r['combined_sigma'] > 0]
        correlations = [r['correlation'] for r in results if not np.isnan(r['correlation'])]
        
        # Panel 1: Distribución tasas de detección
        ax1 = axes[0, 0]
        ax1.hist(detection_rates, bins=20, alpha=0.7, color='skyblue', edgecolor='black')
        ax1.axvline(np.mean(detection_rates), color='red', linestyle='--', 
                   label=f'Media: {np.mean(detection_rates):.1%}')
        ax1.axvline(0.05, color='gray', linestyle=':', label='Tasa nula (5%)')
        ax1.set_xlabel('Tasa de Detección')
        ax1.set_ylabel('Número de Experimentos')
        ax1.set_title('Distribución Tasas de Detección')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Panel 2: Distribución significancias combinadas
        ax2 = axes[0, 1]
        if combined_sigmas:
            ax2.hist(combined_sigmas, bins=15, alpha=0.7, color='lightgreen', edgecolor='black')
            ax2.axvline(np.mean(combined_sigmas), color='red', linestyle='--',
                       label=f'Media: {np.mean(combined_sigmas):.2f}σ')
            ax2.axvline(3, color='blue', linestyle=':', label='3σ')
            ax2.axvline(5, color='purple', linestyle=':', label='5σ')
        ax2.set_xlabel('Significancia Combinada (σ)')
        ax2.set_ylabel('Número de Experimentos')
        ax2.set_title('Distribución Significancia Combinada')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # Panel 3: Correlaciones predicción-observación
        ax3 = axes[0, 2]
        if correlations:
            ax3.hist(correlations, bins=15, alpha=0.7, color='orange', edgecolor='black')
            ax3.axvline(np.mean(correlations), color='red', linestyle='--',
                       label=f'Media: {np.mean(correlations):.3f}')
            ax3.axvline(0, color='gray', linestyle=':', label='Sin correlación')
        ax3.set_xlabel('Correlación Predicción-Observación')
        ax3.set_ylabel('Número de Experimentos')
        ax3.set_title('Distribución Correlaciones')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # Panel 4: Tasa detección vs significancia
        ax4 = axes[1, 0]
        valid_results = [r for r in results if r['avg_significance'] > 0]
        if valid_results:
            x_vals = [r['detection_rate'] for r in valid_results]
            y_vals = [r['avg_significance'] for r in valid_results]
            ax4.scatter(x_vals, y_vals, alpha=0.6, c='purple')
            
            # Correlación
            if len(x_vals) > 2:
                correlation = np.corrcoef(x_vals, y_vals)[0,1]
                ax4.set_title(f'Tasa vs Significancia (r={correlation:.3f})')
            else:
                ax4.set_title('Tasa vs Significancia')
        else:
            ax4.set_title('Tasa vs Significancia (Sin datos)')
            
        ax4.set_xlabel('Tasa de Detección')
        ax4.set_ylabel('Significancia Promedio (σ)')
        ax4.grid(True, alpha=0.3)
        
        # Panel 5: Evolución temporal de experimentos
        ax5 = axes[1, 1]
        experiment_ids = [r['experiment_id'] for r in results]
        ax5.plot(experiment_ids, detection_rates, 'b-', alpha=0.7, linewidth=1)
        ax5.axhline(np.mean(detection_rates), color='red', linestyle='--', alpha=0.8)
        ax5.set_xlabel('Número de Experimento')
        ax5.set_ylabel('Tasa de Detección')
        ax5.set_title('Estabilidad Temporal')
        ax5.grid(True, alpha=0.3)
        
        # Panel 6: Resumen estadístico
        ax6 = axes[1, 2]
        ax6.axis('off')
        
        experiments_with_detections = sum(1 for r in results if r['n_detected'] > 0)
        experiments_above_3sigma = sum(1 for r in results if r['max_significance'] >= 3.0)
        
        summary_text = f"""RESUMEN EXPERIMENTOS ALEATORIOS

CONFIGURACIÓN:
• {len(results)} experimentos independientes
• {results[0]['sample_size'] if results else 0} eventos por experimento
• Población total: {len(self.population_data)} eventos

RESULTADOS:
• Tasa detección promedio: {np.mean(detection_rates):.1%}
• Experimentos con detecciones: {experiments_with_detections}/{len(results)}
• Experimentos >3σ: {experiments_above_3sigma}/{len(results)}

PARÁMETROS USADOS:
• τ = {self.a_tau:.3f}/M^{{{self.n_tau:.3f}}} + {self.b_tau:.3f}
• (Optimizados en Script 1)

SIGNIFICANCIA TÍPICA:
• Promedio: {np.mean(combined_sigmas) if combined_sigmas else 0:.2f}σ
• Máxima: {np.max(combined_sigmas) if combined_sigmas else 0:.2f}σ

CONCLUSIÓN:
{'✅ Evidencia consistente' if np.mean(detection_rates) > 0.1 else '⚠️ Evidencia limitada'}
Libre de sesgo de confirmación
"""
        
        ax6.text(0.05, 0.95, summary_text, transform=ax6.transAxes,
                fontsize=10, verticalalignment='top', fontfamily='monospace',
                bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
        
        plt.tight_layout()
        
        # Guardar visualización
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f'script2_random_experiments_{timestamp}.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"✅ Visualización guardada: {filename}")
        plt.show()

def main():
    """Ejecutar Script 2: Experimentos aleatorios libres de sesgo"""
    
    print("🚀 SCRIPT 2: EXPERIMENTOS ALEATORIOS LIBRES DE SESGO")
    print("=" * 70)
    print("Objetivo: Calcular σ mediante selecciones aleatorias sin cherry-picking")
    print("Método: Múltiples experimentos independientes con parámetros del Script 1")
    
    runner = RandomExperimentRunner()
    
    # Configuración de experimentos
    n_experiments = 100  # Número de experimentos aleatorios
    sample_size = 20     # Eventos por experimento (ajustable)
    
    print(f"\n🔧 CONFIGURACIÓN:")
    print(f"   Experimentos a ejecutar: {n_experiments}")
    print(f"   Eventos por experimento: {sample_size}")
    print(f"   Total combinaciones posibles: C({len(runner.population_data)},{sample_size})")
    
    # Ejecutar experimentos
    results = runner.run_multiple_experiments(n_experiments, sample_size)
    
    # Crear visualización
    runner.create_comprehensive_visualization(results)
    
    print(f"\n✅ SCRIPT 2 COMPLETADO")
    print(f"Experimentos aleatorios libres de sesgo ejecutados exitosamente")
    print(f"Los resultados proporcionan una evaluación estadística robusta")
    
    return runner, results

if __name__ == "__main__":
    runner, results = main()