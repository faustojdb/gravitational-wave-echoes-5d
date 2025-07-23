#!/usr/bin/env python3
"""
Optimización Parámetros Klein Elástica
======================================

Optimiza parámetros del modelo Klein elástica para maximizar:
1. Correlación energía-deformación (objetivo: r > 0.7)
2. Diversidad de estados de deformación
3. Acuerdo con supresión modal observacional

Autor: Fausto José Di Bacco
Fecha: Diciembre 2024
"""

import numpy as np
from scipy.optimize import minimize, differential_evolution
from scipy.stats import pearsonr
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple
import json
from datetime import datetime

from elastic_klein_model import ElasticKleinModel, ElasticKleinParameters, ElasticKleinAnalyzer


class ElasticKleinOptimizer:
    """Optimizador para parámetros Klein elástica."""
    
    def __init__(self, target_events: List[Dict]):
        """
        Inicializa optimizador.
        
        Parameters
        ----------
        target_events : List[Dict]
            Eventos objetivo para optimización
        """
        self.target_events = target_events
        self.optimization_history = []
        
        print(f"Optimizador Klein Elástica inicializado")
        print(f"Eventos objetivo: {len(target_events)}")
    
    def objective_function(self, param_array: np.ndarray) -> float:
        """
        Función objetivo para optimización.
        
        Minimiza costo basado en:
        1. Correlación energía-deformación (peso 50%)
        2. Diversidad estados deformación (peso 30%) 
        3. Rango supresión modal realista (peso 20%)
        
        Parameters
        ---------- 
        param_array : np.ndarray
            Array de parámetros a optimizar
            
        Returns
        -------
        cost : float
            Costo total (menor es mejor)
        """
        try:
            # Crear parámetros desde array
            params = self._array_to_params(param_array)
            
            # Crear modelo con parámetros actuales
            model = ElasticKleinModel(params)
            analyzer = ElasticKleinAnalyzer(model)
            
            # Analizar eventos objetivo
            energies = []
            deformations = []
            suppressions = []
            states = []
            
            for event in self.target_events:
                analysis = analyzer.analyze_event_elastic(
                    event['energy'], event['mass'], event['name']
                )
                
                energies.append(analysis['parameters']['energy'])
                deformations.append(analysis['indicators']['max_deformation'])
                suppressions.append(analysis['indicators']['suppression_max'])
                states.append(analysis['indicators']['deformation_class'])
            
            # 1. COSTO CORRELACIÓN ENERGÍA-DEFORMACIÓN (peso 50%)
            if len(energies) > 2:
                correlation, p_value = pearsonr(energies, deformations)
                correlation_cost = max(0, 0.8 - correlation)  # Objetivo r > 0.8
            else:
                correlation_cost = 1.0
            
            # 2. COSTO DIVERSIDAD ESTADOS (peso 30%)
            from collections import Counter
            state_counts = Counter(states)
            n_states = len(state_counts)
            
            # Penalizar falta de diversidad
            if n_states < 2:
                diversity_cost = 1.0
            else:
                # Calcular entropía de distribución (máximo para distribución uniforme)
                total = len(states)
                entropy = -sum((count/total) * np.log(count/total) for count in state_counts.values())
                max_entropy = np.log(n_states)
                diversity_cost = 1.0 - (entropy / max_entropy) if max_entropy > 0 else 1.0
            
            # 3. COSTO RANGO SUPRESIÓN MODAL (peso 20%)
            # Objetivo: rango 20:1 a 60:1 (observacionalmente realista)
            supp_min, supp_max = min(suppressions), max(suppressions)
            
            if supp_min < 15 or supp_max > 80:
                suppression_cost = 0.5  # Fuera de rango físico
            elif supp_min < 20 or supp_max > 60:
                suppression_cost = 0.2  # Límites del rango objetivo
            else:
                # Dentro del rango objetivo
                range_ratio = (supp_max - supp_min) / 40  # Normalizar a rango 40
                suppression_cost = max(0, 0.2 - range_ratio)  # Premiar rango amplio
            
            # COSTO TOTAL PONDERADO
            total_cost = (0.5 * correlation_cost + 
                         0.3 * diversity_cost + 
                         0.2 * suppression_cost)
            
            # Guardar en historial
            self.optimization_history.append({
                'params': param_array.copy(),
                'cost': total_cost,
                'correlation': correlation if len(energies) > 2 else 0,
                'correlation_cost': correlation_cost,
                'diversity_cost': diversity_cost,
                'suppression_cost': suppression_cost,
                'n_states': n_states,
                'suppression_range': (supp_min, supp_max)
            })
            
            return total_cost
            
        except Exception as e:
            print(f"Error en función objetivo: {e}")
            return 10.0  # Costo penalizante
    
    def _array_to_params(self, param_array: np.ndarray) -> ElasticKleinParameters:
        """Convierte array a parámetros Klein elástica."""
        return ElasticKleinParameters(
            # Conservar escalas fundamentales
            R_5D=8.4e6,
            c=2.99792458e8,
            f_0=5.7,
            
            # Parámetros elásticos optimizables
            gamma_elastic=param_array[0],      # [10, 100] 1/s
            epsilon_max=param_array[1],        # [0.3, 0.8] 
            K_elastic=1e45,                    # Fijo (escala cosmológica)
            E_critical=param_array[2],         # [0.5, 3.0] M☉c²
            
            # Parámetros supresión modal optimizables
            R_base=param_array[3],             # [15, 30] supresión base
            A_elastic=param_array[4],          # [30, 80] amplificación
            alpha_modulation=param_array[5]    # [0.1, 0.6] respiración
        )
    
    def optimize_parameters(self, method: str = 'differential_evolution') -> ElasticKleinParameters:
        """
        Optimiza parámetros Klein elástica.
        
        Parameters
        ----------
        method : str
            Método de optimización
            
        Returns
        -------
        optimal_params : ElasticKleinParameters
            Parámetros optimizados
        """
        print(f"\nOptimizando parámetros Klein elástica...")
        print(f"Método: {method}")
        
        # Parámetros iniciales
        initial_params = np.array([
            35.7,  # gamma_elastic
            0.5,   # epsilon_max
            1.0,   # E_critical  
            20.0,  # R_base
            50.0,  # A_elastic
            0.3    # alpha_modulation
        ])
        
        # Límites de búsqueda
        bounds = [
            (10, 100),    # gamma_elastic [1/s]
            (0.3, 0.8),   # epsilon_max
            (0.5, 3.0),   # E_critical [M☉c²]
            (15, 30),     # R_base
            (30, 80),     # A_elastic
            (0.1, 0.6)    # alpha_modulation
        ]
        
        # Costo inicial
        initial_cost = self.objective_function(initial_params)
        print(f"Costo inicial: {initial_cost:.3f}")
        
        if method == 'differential_evolution':
            result = differential_evolution(
                self.objective_function,
                bounds,
                seed=42,
                maxiter=50,  # Suficiente para convergencia
                popsize=15,
                atol=1e-3,
                tol=1e-3
            )
            optimal_array = result.x
            final_cost = result.fun
            
        else:
            result = minimize(
                self.objective_function,
                initial_params,
                method='L-BFGS-B',
                bounds=bounds
            )
            optimal_array = result.x
            final_cost = result.fun
        
        # Crear parámetros optimizados
        optimal_params = self._array_to_params(optimal_array)
        
        # Calcular mejora
        improvement = ((initial_cost - final_cost) / initial_cost) * 100
        
        print(f"Optimización completada:")
        print(f"  Costo final: {final_cost:.3f}")
        print(f"  Mejora: {improvement:.1f}%")
        
        return optimal_params
    
    def validate_optimized_model(self, optimal_params: ElasticKleinParameters) -> Dict:
        """
        Valida modelo con parámetros optimizados.
        
        Parameters
        ----------
        optimal_params : ElasticKleinParameters
            Parámetros optimizados
            
        Returns
        -------
        validation : Dict
            Resultados de validación
        """
        print(f"\nValidando modelo optimizado...")
        
        # Crear modelo optimizado
        model = ElasticKleinModel(optimal_params)
        analyzer = ElasticKleinAnalyzer(model)
        
        # Analizar con parámetros optimizados
        catalog_analysis = analyzer.analyze_catalog_elastic(self.target_events)
        
        # Extraer métricas clave
        global_stats = catalog_analysis['global_statistics']
        correlation = global_stats['energy_deformation_correlation']
        correlation_significant = global_stats['correlation_significant']
        
        # Distribución de estados
        deform_dist = catalog_analysis['deformation_distribution']
        n_unique_states = len(deform_dist)
        
        # Rango de supresión
        suppression_range = global_stats['suppression_range']
        
        # Conservación topológica
        topology_conservation = catalog_analysis['topology_conservation']['all_klein_bottle']
        
        validation = {
            'correlation': {
                'value': correlation,
                'significant': correlation_significant,
                'target_achieved': correlation > 0.7
            },
            'diversity': {
                'n_states': n_unique_states,
                'distribution': deform_dist,
                'adequate_diversity': n_unique_states >= 2
            },
            'suppression_range': {
                'min_max': suppression_range,
                'realistic_range': 15 <= suppression_range[0] <= 30 and 40 <= suppression_range[1] <= 80
            },
            'topology_conservation': {
                'all_klein': topology_conservation,
                'conservation_rate': 1.0 if topology_conservation else 0.0
            },
            'overall_success': (
                correlation > 0.7 and
                correlation_significant and 
                n_unique_states >= 2 and
                topology_conservation
            )
        }
        
        print(f"Validación completada:")
        print(f"  Correlación E-ε: {correlation:.3f} ({'✅' if correlation > 0.7 else '❌'})")
        print(f"  Estados únicos: {n_unique_states} ({'✅' if n_unique_states >= 2 else '❌'})")
        print(f"  Conservación topológica: {'✅' if topology_conservation else '❌'}")
        print(f"  Éxito general: {'✅' if validation['overall_success'] else '❌'}")
        
        return validation, catalog_analysis
    
    def plot_optimization_results(self, save_path: str = None):
        """Visualiza resultados de optimización."""
        if not self.optimization_history:
            print("No hay historial de optimización")
            return
        
        history = self.optimization_history
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))
        
        # 1. Evolución del costo
        iterations = range(len(history))
        costs = [h['cost'] for h in history]
        correlations = [h['correlation'] for h in history]
        
        ax1.plot(iterations, costs, 'b-', linewidth=2, label='Costo total')
        ax1.set_xlabel('Iteración')
        ax1.set_ylabel('Costo')
        ax1.set_title('A. Evolución del Costo')
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        
        # 2. Evolución correlación
        ax2.plot(iterations, correlations, 'r-', linewidth=2, label='Correlación E-ε')
        ax2.axhline(0.7, color='green', linestyle='--', alpha=0.7, label='Objetivo')
        ax2.set_xlabel('Iteración')
        ax2.set_ylabel('Correlación')
        ax2.set_title('B. Correlación Energía-Deformación')
        ax2.set_ylim(0, 1)
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        
        # 3. Componentes del costo
        corr_costs = [h['correlation_cost'] for h in history]
        div_costs = [h['diversity_cost'] for h in history]
        supp_costs = [h['suppression_cost'] for h in history]
        
        ax3.plot(iterations, corr_costs, label='Correlación (50%)', linewidth=2)
        ax3.plot(iterations, div_costs, label='Diversidad (30%)', linewidth=2)
        ax3.plot(iterations, supp_costs, label='Supresión (20%)', linewidth=2)
        ax3.set_xlabel('Iteración')
        ax3.set_ylabel('Costo Componente')
        ax3.set_title('C. Componentes del Costo')
        ax3.grid(True, alpha=0.3)
        ax3.legend()
        
        # 4. Convergencia
        if len(costs) > 10:
            window = 5
            moving_avg = []
            for i in range(window, len(costs)):
                avg = np.mean(costs[i-window:i])
                moving_avg.append(avg)
            
            ax4.plot(range(window, len(costs)), moving_avg, 'purple', linewidth=3)
            ax4.set_xlabel('Iteración')
            ax4.set_ylabel('Costo (promedio móvil)')
            ax4.set_title('D. Convergencia')
            ax4.grid(True, alpha=0.3)
        
        plt.suptitle('Optimización Parámetros Klein Elástica', fontsize=14, fontweight='bold')
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Gráfico guardado: {save_path}")
        
        return fig


def create_expanded_test_catalog() -> List[Dict]:
    """Crea catálogo expandido para optimización robusta."""
    
    print("Creando catálogo expandido para optimización...")
    
    # Eventos más diversos para optimización robusta
    test_events = [
        # Ultra alta energía
        {'name': 'GW_Ultra_High_1', 'energy': 5.0, 'mass': 150.0},
        {'name': 'GW_Ultra_High_2', 'energy': 4.5, 'mass': 140.0},
        
        # Alta energía
        {'name': 'GW_High_1', 'energy': 3.0, 'mass': 100.0},
        {'name': 'GW_High_2', 'energy': 2.5, 'mass': 90.0},
        {'name': 'GW_High_3', 'energy': 2.0, 'mass': 80.0},
        
        # Media energía
        {'name': 'GW_Medium_1', 'energy': 1.5, 'mass': 60.0},
        {'name': 'GW_Medium_2', 'energy': 1.0, 'mass': 50.0},
        {'name': 'GW_Medium_3', 'energy': 0.8, 'mass': 40.0},
        {'name': 'GW_Medium_4', 'energy': 0.6, 'mass': 35.0},
        
        # Baja energía
        {'name': 'GW_Low_1', 'energy': 0.4, 'mass': 30.0},
        {'name': 'GW_Low_2', 'energy': 0.3, 'mass': 25.0},
        {'name': 'GW_Low_3', 'energy': 0.2, 'mass': 20.0},
        {'name': 'GW_Low_4', 'energy': 0.1, 'mass': 15.0},
        
        # Ultra baja energía
        {'name': 'GW_Ultra_Low_1', 'energy': 0.05, 'mass': 10.0},
        {'name': 'GW_Ultra_Low_2', 'energy': 0.02, 'mass': 8.0}
    ]
    
    print(f"Catálogo expandido: {len(test_events)} eventos")
    return test_events


def main():
    """Ejecuta optimización completa Klein elástica."""
    
    print("OPTIMIZACIÓN PARÁMETROS KLEIN ELÁSTICA")
    print("="*80)
    
    # 1. Crear catálogo de prueba expandido
    test_catalog = create_expanded_test_catalog()
    
    # 2. Crear optimizador
    optimizer = ElasticKleinOptimizer(test_catalog)
    
    # 3. Optimizar parámetros
    optimal_params = optimizer.optimize_parameters(method='differential_evolution')
    
    # 4. Validar modelo optimizado
    validation, catalog_analysis = optimizer.validate_optimized_model(optimal_params)
    
    # 5. Crear visualizaciones
    results_dir = f"elastic_klein_optimization_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    import os
    os.makedirs(results_dir, exist_ok=True)
    
    optimizer.plot_optimization_results(f"{results_dir}/optimization_evolution.png")
    
    # 6. Guardar resultados
    results = {
        'optimal_parameters': optimal_params.to_dict() if hasattr(optimal_params, 'to_dict') else optimal_params.__dict__,
        'validation_results': validation,
        'catalog_analysis': catalog_analysis,
        'optimization_history': optimizer.optimization_history[-10:]  # Últimas 10 iteraciones
    }
    
    with open(f"{results_dir}/optimization_results.json", 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    # 7. Resumen final
    print(f"\n{'='*80}")
    print("RESUMEN OPTIMIZACIÓN KLEIN ELÁSTICA")
    print(f"{'='*80}")
    
    if validation['overall_success']:
        print("🎉 OPTIMIZACIÓN EXITOSA!")
        print(f"   Correlación E-ε: {validation['correlation']['value']:.3f} (objetivo: >0.7)")
        print(f"   Estados diversos: {validation['diversity']['n_states']} tipos")
        print(f"   Topología conservada: 100%")
        
        print(f"\n📋 PARÁMETROS OPTIMIZADOS:")
        print(f"   γ_elastic = {optimal_params.gamma_elastic:.1f} 1/s")
        print(f"   ε_max = {optimal_params.epsilon_max:.3f}")
        print(f"   E_critical = {optimal_params.E_critical:.2f} M☉c²")
        print(f"   R_base = {optimal_params.R_base:.1f}")
        print(f"   A_elastic = {optimal_params.A_elastic:.1f}")
        
    else:
        print("⚠️  Optimización parcial")
        issues = []
        if not validation['correlation']['target_achieved']:
            issues.append(f"Correlación insuficiente: {validation['correlation']['value']:.3f}")
        if not validation['diversity']['adequate_diversity']:
            issues.append(f"Diversidad limitada: {validation['diversity']['n_states']} estados")
        if not validation['topology_conservation']['all_klein']:
            issues.append("Conservación topológica violada")
        
        for issue in issues:
            print(f"   ❌ {issue}")
    
    print(f"\n📁 Resultados completos en: {results_dir}/")
    
    return optimal_params, validation, catalog_analysis


if __name__ == "__main__":
    main()