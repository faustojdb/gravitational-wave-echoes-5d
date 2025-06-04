#!/usr/bin/env python3
"""
SCRIPT 1: OPTIMIZACIÓN POBLACIONAL COMPLETA
==========================================

Optimiza parámetros Klein bottle usando TODOS los 65 eventos disponibles.
Sin cherry-picking, sin sesgo de confirmación.

Objetivo: Encontrar los parámetros que mejor explican el patrón de 
detecciones/no-detecciones en toda la población LIGO.
"""

import numpy as np
import matplotlib.pyplot as plt
import json
from scipy.optimize import differential_evolution, minimize
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

class PopulationOptimizer:
    def __init__(self):
        """Inicializar optimizador poblacional"""
        
        # Cargar resultados del análisis expandido
        self.load_gwtc_data()
        
        print(f"✅ Script 1: Optimización Poblacional Completa")
        print(f"📊 Población total: {len(self.events_data)} eventos")
        print(f"🎯 Objetivo: Encontrar parámetros Klein óptimos sin sesgo")
        
    def load_gwtc_data(self):
        """Cargar datos GWTC del análisis expandido"""
        
        try:
            with open('comprehensive_gwtc_results_20250603_165259.json', 'r') as f:
                gwtc_results = json.load(f)
            
            # Extraer datos de eventos
            self.events_data = []
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
                    self.events_data.append(event_data)
                    
            print(f"✅ Cargados {len(self.events_data)} eventos del análisis expandido")
            
        except FileNotFoundError:
            print("⚠️ Archivo de resultados no encontrado, generando datos sintéticos")
            self.generate_synthetic_population()
            
    def generate_synthetic_population(self):
        """Generar población sintética para demostración"""
        
        np.random.seed(42)
        self.events_data = []
        
        for i in range(65):
            # Propiedades físicas realistas basadas en GWTC
            mass = np.random.uniform(15, 150)  # M☉
            distance = np.random.uniform(400, 3000)  # Mpc
            snr = np.random.uniform(8, 25)
            
            # Simular detección Klein con patrón realista
            # Basado en análisis expandido: ~4.6% detecciones con 2.77σ promedio
            detection_prob = 0.1 * np.exp(-distance/1500) * (mass/100)**0.3 * (snr/15)
            detected = np.random.random() < detection_prob
            
            if detected:
                significance = 2.0 + np.random.exponential(1.0)  # Promedio ~3σ
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
            self.events_data.append(event_data)
            
        print(f"✅ Generados {len(self.events_data)} eventos sintéticos")
        
    def population_likelihood(self, params):
        """
        Función de likelihood poblacional
        
        Parámetros:
        - params[0:3]: Ley temporal τ = a/M^n + b
        - params[3:6]: Dependencias físicas (distancia, SNR, masa)
        - params[6]: Coupling base
        """
        
        a_tau, b_tau, n_tau = params[0:3]
        dist_exp, snr_exp, mass_exp = params[3:6]  
        coupling = params[6]
        
        # Validar parámetros físicos
        if a_tau <= 0 or b_tau < 0 or n_tau <= 0 or coupling <= 0:
            return -1e10  # Likelihood muy baja para parámetros no físicos
            
        total_log_likelihood = 0
        
        for event in self.events_data:
            # Predicción Klein bottle
            tau_pred = a_tau / (event['mass']**n_tau) + b_tau
            
            # Verificar tau físico
            if tau_pred <= 0 or tau_pred > 1.0:  # Eco debe ser positivo y razonable
                return -1e10
                
            # Probabilidad de detección basada en parámetros físicos
            distance_factor = (1000 / event['distance'])**dist_exp
            snr_factor = (event['network_snr'] / 15)**snr_exp
            mass_factor = (event['mass'] / 50)**mass_exp
            
            # Probabilidad combinada
            detection_prob = coupling * distance_factor * snr_factor * mass_factor
            detection_prob = np.clip(detection_prob, 1e-6, 1-1e-6)  # Evitar log(0)
            
            # Likelihood para este evento
            if event['detected']:
                # Evento detectado: queremos alta probabilidad
                likelihood = detection_prob
                # Bonus por alta significancia observada
                if event['significance'] > 2:
                    likelihood *= (1 + event['significance']/10)
            else:
                # Evento no detectado: queremos baja probabilidad
                likelihood = (1 - detection_prob)
                
            total_log_likelihood += np.log(likelihood)
            
        return total_log_likelihood
        
    def optimize_population_parameters(self):
        """Optimizar parámetros sobre toda la población"""
        
        print(f"\n" + "="*70)
        print("OPTIMIZACIÓN POBLACIONAL - TODOS LOS EVENTOS")
        print("="*70)
        
        # Límites de búsqueda amplios y físicamente realistas
        bounds = [
            (0.1, 3.0),      # a_tau (coeficiente temporal)
            (0.0, 0.5),      # b_tau (offset temporal)
            (0.3, 1.5),      # n_tau (exponente masa)
            (0.5, 3.0),      # dist_exp (dependencia distancia)
            (0.5, 2.0),      # snr_exp (dependencia SNR)
            (-1.0, 1.0),     # mass_exp (dependencia masa)
            (0.001, 0.3),    # coupling (acoplamiento base)
        ]
        
        print(f"Optimizando 7 parámetros sobre {len(self.events_data)} eventos...")
        print("Método: Maximum Likelihood Estimation")
        
        # Múltiples intentos para evitar mínimos locales
        best_result = None
        best_likelihood = -1e10
        
        for attempt in range(3):
            print(f"\nIntento {attempt + 1}/3...")
            
            result = differential_evolution(
                lambda x: -self.population_likelihood(x),  # Minimizar -log_likelihood
                bounds,
                maxiter=200,
                popsize=20,
                disp=True,
                seed=42 + attempt,
                atol=1e-6,
                tol=1e-6
            )
            
            likelihood = -result.fun
            print(f"Likelihood obtenido: {likelihood:.2f}")
            
            if likelihood > best_likelihood:
                best_likelihood = likelihood
                best_result = result
                
        if best_result is None:
            print("❌ Optimización falló")
            return None
            
        # Extraer parámetros óptimos
        params = best_result.x
        a_tau, b_tau, n_tau, dist_exp, snr_exp, mass_exp, coupling = params
        
        print(f"\n🎯 PARÁMETROS POBLACIONALES ÓPTIMOS:")
        print(f"   Ley temporal: τ = {a_tau:.3f}/M^{n_tau:.3f} + {b_tau:.3f}")
        print(f"   Exponente distancia: {dist_exp:.3f}")
        print(f"   Exponente SNR: {snr_exp:.3f}")
        print(f"   Exponente masa: {mass_exp:.3f}")
        print(f"   Acoplamiento base: {coupling:.4f}")
        print(f"   Log-likelihood: {best_likelihood:.2f}")
        
        # Evaluar ajuste
        self.evaluate_population_fit(params)
        
        # Guardar parámetros para Script 2
        self.save_optimal_parameters(params)
        
        return params
        
    def evaluate_population_fit(self, params):
        """Evaluar calidad del ajuste poblacional"""
        
        a_tau, b_tau, n_tau, dist_exp, snr_exp, mass_exp, coupling = params
        
        print(f"\n📊 EVALUACIÓN DEL AJUSTE POBLACIONAL:")
        
        # Calcular predicciones vs observaciones
        predictions = []
        observations = []
        tau_predictions = []
        
        for event in self.events_data:
            # Predicciones del modelo
            tau_pred = a_tau / (event['mass']**n_tau) + b_tau
            tau_predictions.append(tau_pred)
            
            distance_factor = (1000 / event['distance'])**dist_exp
            snr_factor = (event['network_snr'] / 15)**snr_exp
            mass_factor = (event['mass'] / 50)**mass_exp
            
            detection_prob = coupling * distance_factor * snr_factor * mass_factor
            detection_prob = np.clip(detection_prob, 0, 1)
            
            predictions.append(detection_prob)
            observations.append(1 if event['detected'] else 0)
            
        predictions = np.array(predictions)
        observations = np.array(observations)
        
        # Estadísticas de ajuste
        correlation = np.corrcoef(predictions, observations)[0,1]
        predicted_rate = np.mean(predictions)
        observed_rate = np.mean(observations)
        
        print(f"   Correlación predicción-observación: {correlation:.4f}")
        print(f"   Tasa predicha: {predicted_rate:.1%}")
        print(f"   Tasa observada: {observed_rate:.1%}")
        print(f"   Error absoluto: {abs(predicted_rate - observed_rate):.1%}")
        
        # Eventos detectados - estadísticas
        detected_events = [i for i, obs in enumerate(observations) if obs == 1]
        if len(detected_events) > 0:
            detected_probs = predictions[detected_events]
            detected_sigs = [self.events_data[i]['significance'] for i in detected_events]
            
            print(f"\n📈 ESTADÍSTICAS DE DETECCIONES:")
            print(f"   Eventos detectados: {len(detected_events)}")
            print(f"   Probabilidad promedio (detectados): {np.mean(detected_probs):.3f}")
            print(f"   Significancia promedio: {np.mean(detected_sigs):.2f}σ")
            print(f"   Significancia máxima: {np.max(detected_sigs):.2f}σ")
            
        # Distribución de tiempos de eco
        tau_detected = [tau_predictions[i] for i in detected_events]
        if len(tau_detected) > 0:
            print(f"\n⏱️ TIEMPOS DE ECO (detecciones):")
            print(f"   Rango: {np.min(tau_detected):.3f} - {np.max(tau_detected):.3f} s")
            print(f"   Promedio: {np.mean(tau_detected):.3f} s")
            
        # Test de bondad de ajuste
        self.goodness_of_fit_tests(predictions, observations)
        
        return predictions, observations
        
    def goodness_of_fit_tests(self, predictions, observations):
        """Tests estadísticos de bondad de ajuste"""
        
        print(f"\n🔍 TESTS DE BONDAD DE AJUSTE:")
        
        # 1. Kolmogorov-Smirnov test
        detected_probs = predictions[observations == 1]
        undetected_probs = predictions[observations == 0]
        
        if len(detected_probs) > 0 and len(undetected_probs) > 0:
            ks_stat, ks_pvalue = stats.ks_2samp(detected_probs, undetected_probs)
            print(f"   K-S test (separación poblaciones): D = {ks_stat:.3f}, p = {ks_pvalue:.4f}")
            
        # 2. Brier score (calibración probabilística)
        brier_score = np.mean((predictions - observations)**2)
        print(f"   Brier score (calibración): {brier_score:.4f} (menor = mejor)")
        
        # 3. AUC-ROC simulado
        thresholds = np.linspace(0, 1, 101)
        tpr_values = []
        fpr_values = []
        
        for threshold in thresholds:
            predicted_detections = predictions > threshold
            
            tp = np.sum((predicted_detections == 1) & (observations == 1))
            fp = np.sum((predicted_detections == 1) & (observations == 0))
            tn = np.sum((predicted_detections == 0) & (observations == 0))
            fn = np.sum((predicted_detections == 0) & (observations == 1))
            
            tpr = tp / (tp + fn) if (tp + fn) > 0 else 0
            fpr = fp / (fp + tn) if (fp + tn) > 0 else 0
            
            tpr_values.append(tpr)
            fpr_values.append(fpr)
            
        # Calcular AUC aproximado
        auc = np.trapz(tpr_values, fpr_values)
        print(f"   AUC-ROC: {auc:.4f} (0.5 = azar, 1.0 = perfecto)")
        
        # 4. Calibración por bins
        n_bins = 5
        bin_boundaries = np.linspace(0, 1, n_bins + 1)
        bin_lowers = bin_boundaries[:-1]
        bin_uppers = bin_boundaries[1:]
        
        print(f"   Calibración por bins:")
        for i in range(n_bins):
            in_bin = (predictions > bin_lowers[i]) & (predictions <= bin_uppers[i])
            if np.sum(in_bin) > 0:
                bin_confidence = np.mean(predictions[in_bin])
                bin_accuracy = np.mean(observations[in_bin])
                print(f"     Bin {i+1}: Confianza = {bin_confidence:.3f}, Precisión = {bin_accuracy:.3f}")
                
    def save_optimal_parameters(self, params):
        """Guardar parámetros óptimos para Script 2"""
        
        a_tau, b_tau, n_tau, dist_exp, snr_exp, mass_exp, coupling = params
        
        optimal_config = {
            'script1_metadata': {
                'method': 'Maximum Likelihood Estimation',
                'population_size': len(self.events_data),
                'optimization_date': '2025-01-03',
                'objective': 'Population-wide Klein bottle parameter optimization'
            },
            
            'optimal_parameters': {
                'temporal_law': {
                    'a_tau': float(a_tau),
                    'b_tau': float(b_tau),
                    'n_tau': float(n_tau),
                    'formula': f'tau = {a_tau:.3f}/M^{n_tau:.3f} + {b_tau:.3f}'
                },
                'physical_dependencies': {
                    'distance_exponent': float(dist_exp),
                    'snr_exponent': float(snr_exp),  
                    'mass_exponent': float(mass_exp),
                    'base_coupling': float(coupling)
                }
            },
            
            'population_statistics': {
                'total_events': len(self.events_data),
                'detected_events': sum(1 for e in self.events_data if e['detected']),
                'detection_rate': sum(1 for e in self.events_data if e['detected']) / len(self.events_data),
                'avg_significance': np.mean([e['significance'] for e in self.events_data if e['significance'] > 0])
            }
        }
        
        # Guardar configuración
        filename = 'optimal_klein_parameters_script1.json'
        with open(filename, 'w') as f:
            json.dump(optimal_config, f, indent=2)
            
        print(f"\n✅ Parámetros óptimos guardados: {filename}")
        print(f"   Estos parámetros serán usados por Script 2 para experimentos aleatorios")
        
        return filename
        
    def create_visualization(self, params, predictions, observations):
        """Crear visualización del ajuste poblacional"""
        
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        fig.suptitle('Script 1: Optimización Poblacional Completa (65 Eventos)', 
                     fontsize=16, fontweight='bold')
        
        a_tau, b_tau, n_tau = params[0:3]
        
        # Datos para plots
        masses = [e['mass'] for e in self.events_data]
        distances = [e['distance'] for e in self.events_data]
        snrs = [e['network_snr'] for e in self.events_data]
        detections = [e['detected'] for e in self.events_data]
        significances = [e['significance'] for e in self.events_data]
        
        # Panel 1: Predicciones vs Observaciones
        ax1 = axes[0, 0]
        colors = ['red' if obs else 'blue' for obs in observations]
        sizes = [60 if obs else 30 for obs in observations]
        ax1.scatter(predictions, observations, c=colors, s=sizes, alpha=0.7, edgecolors='black')
        ax1.plot([0, 1], [0, 1], 'k--', alpha=0.5, label='Predicción perfecta')
        
        correlation = np.corrcoef(predictions, observations)[0,1]
        ax1.set_xlabel('Probabilidad Predicha')
        ax1.set_ylabel('Detección Observada (0/1)')
        ax1.set_title(f'Calibración Modelo (r = {correlation:.3f})')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Panel 2: Nueva ley temporal
        ax2 = axes[0, 1]
        tau_predictions = [a_tau / (m**n_tau) + b_tau for m in masses]
        colors = ['red' if d else 'blue' for d in detections]
        ax2.scatter(masses, tau_predictions, c=colors, alpha=0.7)
        
        # Curva del modelo
        M_range = np.linspace(min(masses), max(masses), 100)
        tau_curve = a_tau / (M_range**n_tau) + b_tau
        ax2.plot(M_range, tau_curve, 'g-', linewidth=3, 
                label=f'τ = {a_tau:.3f}/M^{{{n_tau:.3f}}} + {b_tau:.3f}')
        
        # Comparar con modelo original
        tau_original = 0.752 / (M_range**0.80) + 0.200
        ax2.plot(M_range, tau_original, 'k--', linewidth=2, alpha=0.7,
                label='Original: τ = 0.752/M^0.80 + 0.200')
        
        ax2.set_xlabel('Masa Final (M☉)')
        ax2.set_ylabel('Tiempo de Eco τ (s)')
        ax2.set_title('Ley Temporal Optimizada')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # Panel 3: Distribución significancias
        ax3 = axes[0, 2]
        detected_sigs = [s for s, d in zip(significances, detections) if d and s > 0]
        if len(detected_sigs) > 0:
            ax3.hist(detected_sigs, bins=max(3, len(detected_sigs)//2), 
                    alpha=0.7, color='green', edgecolor='black')
            ax3.axvline(np.mean(detected_sigs), color='red', linestyle='--',
                       label=f'Media: {np.mean(detected_sigs):.2f}σ')
        ax3.axvline(3, color='blue', linestyle='--', label='3σ')
        ax3.set_xlabel('Significancia (σ)')
        ax3.set_ylabel('Número de Detecciones')
        ax3.set_title('Distribución de Significancia')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # Panel 4: Probabilidad vs masa
        ax4 = axes[1, 0]
        ax4.scatter(masses, predictions, c=colors, alpha=0.7)
        
        # Tendencia
        try:
            z = np.polyfit(masses, predictions, 2)
            p = np.poly1d(z)
            ax4.plot(sorted(masses), p(sorted(masses)), "r--", alpha=0.8, linewidth=2)
        except:
            pass
            
        ax4.set_xlabel('Masa Final (M☉)')
        ax4.set_ylabel('Probabilidad de Detección')
        ax4.set_title('Dependencia con Masa')
        ax4.grid(True, alpha=0.3)
        
        # Panel 5: Probabilidad vs distancia
        ax5 = axes[1, 1]
        ax5.scatter(distances, predictions, c=colors, alpha=0.7)
        ax5.set_xlabel('Distancia (Mpc)')
        ax5.set_ylabel('Probabilidad de Detección')
        ax5.set_title('Dependencia con Distancia')
        ax5.set_yscale('log')
        ax5.grid(True, alpha=0.3)
        
        # Panel 6: Resumen estadístico
        ax6 = axes[1, 2]
        ax6.axis('off')
        
        n_detected = sum(detections)
        detection_rate = n_detected / len(detections)
        
        summary_text = f"""RESULTADOS SCRIPT 1

POBLACIÓN COMPLETA:
• {len(self.events_data)} eventos analizados
• {n_detected} detecciones ({detection_rate:.1%})
• Sin cherry-picking

PARÁMETROS ÓPTIMOS:
• τ = {a_tau:.3f}/M^{{{n_tau:.3f}}} + {b_tau:.3f}
• Correlación: {correlation:.3f}

SIGNIFICANCIA:
• Promedio: {np.mean(detected_sigs) if detected_sigs else 0:.2f}σ
• Máxima: {max(detected_sigs) if detected_sigs else 0:.2f}σ

SIGUIENTE PASO:
Script 2 usará estos parámetros
para experimentos aleatorios
libres de sesgo.
"""
        
        ax6.text(0.05, 0.95, summary_text, transform=ax6.transAxes,
                fontsize=11, verticalalignment='top', fontfamily='monospace',
                bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
        
        plt.tight_layout()
        plt.savefig('script1_population_optimization.png', dpi=300, bbox_inches='tight')
        print(f"✅ Visualización guardada: script1_population_optimization.png")
        plt.show()

def main():
    """Ejecutar Script 1: Optimización poblacional completa"""
    
    print("🚀 SCRIPT 1: OPTIMIZACIÓN POBLACIONAL COMPLETA")
    print("=" * 60)
    print("Objetivo: Encontrar parámetros Klein óptimos usando TODA la población")
    print("Método: Maximum Likelihood Estimation sin cherry-picking")
    
    optimizer = PopulationOptimizer()
    
    # Optimizar parámetros
    optimal_params = optimizer.optimize_population_parameters()
    
    if optimal_params is not None:
        # Evaluar ajuste
        predictions, observations = optimizer.evaluate_population_fit(optimal_params)
        
        # Crear visualización
        optimizer.create_visualization(optimal_params, predictions, observations)
        
        print(f"\n✅ SCRIPT 1 COMPLETADO")
        print(f"Parámetros óptimos guardados para uso en Script 2")
        print(f"Próximo paso: Ejecutar Script 2 para experimentos aleatorios")
        
    else:
        print(f"\n❌ SCRIPT 1 FALLÓ")
        print(f"No se pudieron optimizar parámetros")
        
    return optimizer

if __name__ == "__main__":
    optimizer = main()