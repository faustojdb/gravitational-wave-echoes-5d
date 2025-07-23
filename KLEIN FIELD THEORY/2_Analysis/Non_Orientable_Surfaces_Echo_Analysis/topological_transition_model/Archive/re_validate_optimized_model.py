#!/usr/bin/env python3
"""
Re-validación del Modelo Optimizado con Catálogo Completo
=========================================================

Este script toma los parámetros optimizados del motor de refinamiento
y re-ejecuta el análisis del catálogo completo para validar las mejoras
en el acuerdo teoría-observación.

Objetivo: Verificar si el acuerdo mejora de 35.5% a >70%

Autor: Fausto José Di Bacco
Fecha: Diciembre 2024
"""

import numpy as np
import matplotlib.pyplot as plt
import json
import os
from datetime import datetime
from typing import Dict, List, Optional
import warnings

# Importar módulos del proyecto
from model_refinement_engine import (
    EnhancedTopologicalModel, 
    EnhancedAnalysisPipeline,
    ModelParameters,
    DetectionParameters
)
from ligo_data_analyzer import LIGODataDownloader, LIGOCatalogEvent, LIGOCatalogAnalyzer
from ligo_analysis_pipeline import LIGOEvent
from topological_transition_implementation import TopologicalTransitionModel
from ligo_analysis_pipeline import TopologicalAnalysisPipeline

warnings.filterwarnings('ignore')


class OptimizedModelValidator:
    """
    Validador del modelo optimizado con catálogo completo.
    """
    
    def __init__(self, optimized_model_params: Optional[ModelParameters] = None,
                 optimized_detection_params: Optional[DetectionParameters] = None):
        """
        Inicializa validador con parámetros optimizados.
        
        Parameters
        ----------
        optimized_model_params : ModelParameters, optional
            Parámetros del modelo optimizados
        optimized_detection_params : DetectionParameters, optional
            Parámetros de detección optimizados
        """
        # Usar parámetros optimizados o por defecto
        self.optimized_model_params = optimized_model_params or self._get_default_optimized_model_params()
        self.optimized_detection_params = optimized_detection_params or self._get_default_optimized_detection_params()
        
        # Crear modelos
        self.original_model = TopologicalTransitionModel()
        self.original_pipeline = TopologicalAnalysisPipeline(self.original_model)
        
        self.optimized_model = EnhancedTopologicalModel(self.optimized_model_params)
        self.optimized_pipeline = EnhancedAnalysisPipeline(self.optimized_model, self.optimized_detection_params)
        
        self.downloader = LIGODataDownloader()
        
        print("Validador del modelo optimizado inicializado")
        print(f"Parámetros del modelo optimizado cargados")
        print(f"Parámetros de detección optimizados cargados")
    
    def _get_default_optimized_model_params(self) -> ModelParameters:
        """Parámetros del modelo optimizados por defecto (resultados de optimización simulada)."""
        return ModelParameters(
            R=8.4e6 * 1.2,              # 20% incremento en radio 5D
            kappa=1.5,                   # Incremento en constante gravitacional
            alpha_relax=1.8,             # Mayor tasa de relajación
            beta_coupling=0.15,          # Mayor acoplamiento modo-topología
            tau_scale_factor=0.8,        # Tiempo característico más rápido
            omega_damping=0.05,          # Menor amortiguamiento para preservar oscilaciones
            f0_scale_factor=1.1,         # Ligero incremento en frecuencia fundamental
            harmonic_coupling=0.08,      # Mayor acoplamiento armónico
            echo_amplitude_scale=0.025,  # Amplitud de ecos incrementada
            mass_scaling_exponent=0.3,   # Escalamiento de masa optimizado
            nonlinear_threshold=1.5,     # Umbral no-lineal más sensible
            nonlinear_strength=0.15      # Efectos no-lineales más fuertes
        )
    
    def _get_default_optimized_detection_params(self) -> DetectionParameters:
        """Parámetros de detección optimizados por defecto."""
        return DetectionParameters(
            klein_window_end=0.018,          # Ventana Klein extendida
            transition_window_end=0.035,     # Ventana transición extendida
            torus_window_end=0.065,          # Ventana toroide extendida
            highpass_freq=15.0,              # Frecuencia pasa-altas menor
            bandpass_low=25.0,               # Banda baja optimizada
            bandpass_high=400.0,             # Banda alta incrementada
            freq_search_bandwidth=0.8,       # Mayor ancho de banda de búsqueda
            omega_threshold_klein=-0.3,      # Umbral Klein más permisivo
            omega_threshold_torus=0.3,       # Umbral toroide más permisivo
            suppression_threshold_klein=3.0, # Umbral supresión más sensible
            adaptive_window_scaling=True,    # Escalamiento adaptativo activado
            mass_dependent_thresholds=True   # Umbrales dependientes de masa
        )
    
    def validate_optimized_model(self, max_events: Optional[int] = None) -> Dict:
        """
        Valida modelo optimizado con catálogo completo.
        
        Parameters
        ----------
        max_events : int, optional
            Máximo número de eventos a analizar
            
        Returns
        -------
        validation_results : Dict
            Resultados de validación comparando original vs optimizado
        """
        print("\n" + "="*80)
        print("VALIDACIÓN DEL MODELO OPTIMIZADO")
        print("="*80)
        
        # Cargar catálogo
        catalog = self.downloader.load_full_catalog()
        
        if max_events:
            catalog = catalog[:max_events]
            print(f"\nLimitando validación a primeros {max_events} eventos")
        
        # Ordenar por energía radiada (alta energía primero para validación crítica)
        catalog.sort(key=lambda e: e.energy_radiated, reverse=True)
        
        print(f"\nAnalizando {len(catalog)} eventos con:")
        print(f"  - Modelo original (baseline)")
        print(f"  - Modelo optimizado (enhanced)")
        
        # Crear directorio de resultados
        results_dir = f"optimized_validation_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        os.makedirs(results_dir, exist_ok=True)
        
        # Analizar eventos
        original_results = []
        optimized_results = []
        
        for i, catalog_event in enumerate(catalog):
            print(f"\n--- Evento {i+1}/{len(catalog)}: {catalog_event.name} ---")
            print(f"    Masa: {catalog_event.total_mass_source:.1f} M☉")
            print(f"    Energía: {catalog_event.energy_radiated:.2f} M☉c²")
            
            try:
                # Generar strain data
                strain, time = self.downloader.generate_realistic_strain(catalog_event)
                
                # Convertir a formato LIGOEvent
                ligo_event = LIGOEvent(
                    name=catalog_event.name,
                    mass_1=catalog_event.mass_1_source,
                    mass_2=catalog_event.mass_2_source,
                    total_mass=catalog_event.total_mass_source,
                    chirp_mass=catalog_event.chirp_mass_source,
                    final_spin=catalog_event.final_spin,
                    luminosity_distance=catalog_event.luminosity_distance,
                    merger_time=0.0,
                    energy_radiated=catalog_event.energy_radiated
                )
                
                # Análisis con modelo original
                print("    Analizando con modelo original...")
                original_result = self.original_pipeline.analyze_event(strain, time, ligo_event)
                original_agreement = original_result['comparison']['global_agreement']
                original_phase = original_result['phase_classification']['dominant_phase']
                
                # Análisis con modelo optimizado
                print("    Analizando con modelo optimizado...")
                optimized_result = self.optimized_pipeline.analyze_event_enhanced(strain, time, ligo_event)
                optimized_agreement = optimized_result['comparison']['global_agreement']
                optimized_phase = optimized_result['phase_classification']['dominant_phase']
                
                # Añadir metadata
                for result in [original_result, optimized_result]:
                    result['catalog_metadata'] = {
                        'run': catalog_event.run,
                        'network_snr': catalog_event.network_snr,
                        'far': catalog_event.far,
                        'p_astro': catalog_event.p_astro,
                        'detectors': catalog_event.detectors
                    }
                
                original_results.append(original_result)
                optimized_results.append(optimized_result)
                
                # Mostrar comparación inmediata
                improvement = (optimized_agreement - original_agreement) * 100
                print(f"    Original:   {original_phase} (acuerdo: {original_agreement:.1%})")
                print(f"    Optimizado: {optimized_phase} (acuerdo: {optimized_agreement:.1%})")
                print(f"    Mejora:     {improvement:+.1f} puntos porcentuales")
                
            except Exception as e:
                print(f"    Error procesando evento: {e}")
                continue
        
        print(f"\nProcesamiento completado: {len(original_results)} eventos analizados")
        
        # Análisis comparativo
        comparison_analysis = self._compare_model_performance(
            original_results, optimized_results
        )
        
        # Compilar resultados de validación
        validation_results = {
            'metadata': {
                'validation_date': datetime.now().isoformat(),
                'total_events': len(catalog),
                'events_analyzed': len(original_results),
                'original_model_params': {
                    'R_km': self.original_model.R / 1000,
                    'tau_ms': self.original_model.tau * 1000,
                    'f0_Hz': self.original_model.f0
                },
                'optimized_model_params': self.optimized_model_params.to_dict(),
                'optimized_detection_params': self.optimized_detection_params.to_dict()
            },
            'original_results': original_results,
            'optimized_results': optimized_results,
            'comparison_analysis': comparison_analysis
        }
        
        # Guardar resultados
        results_file = f"{results_dir}/optimized_validation_results.json"
        with open(results_file, 'w') as f:
            json.dump(validation_results, f, indent=2, default=str)
        
        # Crear visualizaciones de validación
        self._create_validation_plots(validation_results, results_dir)
        
        # Mostrar resumen de validación
        self._print_validation_summary(comparison_analysis)
        
        print(f"\n✅ VALIDACIÓN COMPLETADA")
        print(f"📁 Resultados guardados en: {results_dir}/")
        
        return validation_results
    
    def _compare_model_performance(self, original_results: List[Dict], 
                                 optimized_results: List[Dict]) -> Dict:
        """
        Compara rendimiento entre modelo original y optimizado.
        """
        print(f"\n{'='*60}")
        print("ANÁLISIS COMPARATIVO DE RENDIMIENTO")
        print(f"{'='*60}")
        
        # Extraer métricas
        original_agreements = np.array([r['comparison']['global_agreement'] for r in original_results])
        optimized_agreements = np.array([r['comparison']['global_agreement'] for r in optimized_results])
        
        original_phases = [r['phase_classification']['dominant_phase'] for r in original_results]
        optimized_phases = [r['phase_classification']['dominant_phase'] for r in optimized_results]
        
        energies = np.array([r['parameters']['energy_radiated'] for r in original_results])
        
        # 1. MEJORA EN ACUERDO CON TEORÍA
        print("\n1. ACUERDO CON TEORÍA:")
        
        original_mean = np.mean(original_agreements)
        optimized_mean = np.mean(optimized_agreements)
        improvement = (optimized_mean - original_mean) * 100
        
        print(f"   Original:   {original_mean:.1%}")
        print(f"   Optimizado: {optimized_mean:.1%}")
        print(f"   Mejora:     {improvement:+.1f} puntos porcentuales")
        
        # Verificar si alcanzamos objetivo de >70%
        target_achievement = optimized_mean > 0.70
        print(f"   Objetivo >70%: {'✓ ALCANZADO' if target_achievement else '✗ NO ALCANZADO'}")
        
        # 2. MEJORA POR CATEGORÍA DE ENERGÍA
        print("\n2. MEJORA POR CATEGORÍA DE ENERGÍA:")
        
        # Alta energía (>2.0 M☉c²)
        high_energy_mask = energies > 2.0
        if np.any(high_energy_mask):
            orig_high = np.mean(original_agreements[high_energy_mask])
            opt_high = np.mean(optimized_agreements[high_energy_mask])
            improvement_high = (opt_high - orig_high) * 100
            print(f"   Alta energía:   {orig_high:.1%} → {opt_high:.1%} ({improvement_high:+.1f}pp)")
        
        # Media energía (0.5-2.0 M☉c²)
        medium_energy_mask = (energies > 0.5) & (energies <= 2.0)
        if np.any(medium_energy_mask):
            orig_med = np.mean(original_agreements[medium_energy_mask])
            opt_med = np.mean(optimized_agreements[medium_energy_mask])
            improvement_med = (opt_med - orig_med) * 100
            print(f"   Media energía:  {orig_med:.1%} → {opt_med:.1%} ({improvement_med:+.1f}pp)")
        
        # Baja energía (<0.5 M☉c²)
        low_energy_mask = energies <= 0.5
        if np.any(low_energy_mask):
            orig_low = np.mean(original_agreements[low_energy_mask])
            opt_low = np.mean(optimized_agreements[low_energy_mask])
            improvement_low = (opt_low - orig_low) * 100
            print(f"   Baja energía:   {orig_low:.1%} → {opt_low:.1%} ({improvement_low:+.1f}pp)")
        
        # 3. CONSISTENCIA EN CLASIFICACIÓN DE FASES
        print("\n3. CLASIFICACIÓN DE FASES:")
        
        # Contar cambios en clasificación
        phase_changes = sum(1 for orig, opt in zip(original_phases, optimized_phases) if orig != opt)
        consistency_rate = (len(original_results) - phase_changes) / len(original_results)
        
        print(f"   Eventos con cambio de fase: {phase_changes}/{len(original_results)}")
        print(f"   Tasa de consistencia: {consistency_rate:.1%}")
        
        # Distribución de fases optimizada
        from collections import Counter
        orig_phase_dist = Counter(original_phases)
        opt_phase_dist = Counter(optimized_phases)
        
        print(f"   Distribución original:   {dict(orig_phase_dist)}")
        print(f"   Distribución optimizada: {dict(opt_phase_dist)}")
        
        # 4. EVENTOS CON MEJORA SIGNIFICATIVA
        print("\n4. MEJORAS INDIVIDUALES:")
        
        improvements = (optimized_agreements - original_agreements) * 100
        
        significant_improvements = np.sum(improvements > 10)  # >10 puntos porcentuales
        print(f"   Eventos con mejora >10pp: {significant_improvements}/{len(original_results)}")
        
        deteriorations = np.sum(improvements < -5)  # >5 puntos porcentuales de deterioro
        print(f"   Eventos con deterioro >5pp: {deteriorations}/{len(original_results)}")
        
        # Top mejoras
        if len(improvements) > 0:
            best_improvement_idx = np.argmax(improvements)
            worst_improvement_idx = np.argmin(improvements)
            
            print(f"   Mejor mejora: {original_results[best_improvement_idx]['event']} ({improvements[best_improvement_idx]:+.1f}pp)")
            print(f"   Peor resultado: {original_results[worst_improvement_idx]['event']} ({improvements[worst_improvement_idx]:+.1f}pp)")
        
        # 5. ANÁLISIS ESTADÍSTICO
        print("\n5. ANÁLISIS ESTADÍSTICO:")
        
        # Test de significancia para la mejora
        from scipy.stats import ttest_rel, wilcoxon
        
        try:
            # T-test pareado
            t_stat, p_value_t = ttest_rel(optimized_agreements, original_agreements)
            print(f"   T-test pareado: t = {t_stat:.3f}, p = {p_value_t:.3e}")
            
            # Wilcoxon test (no paramétrico)
            w_stat, p_value_w = wilcoxon(optimized_agreements, original_agreements)
            print(f"   Wilcoxon test: W = {w_stat:.3f}, p = {p_value_w:.3e}")
            
            significant_improvement = p_value_t < 0.05
            print(f"   Mejora estadísticamente significativa: {'✓' if significant_improvement else '✗'}")
            
        except Exception as e:
            print(f"   Error en análisis estadístico: {e}")
            significant_improvement = False
        
        # Compilar análisis comparativo
        comparison_analysis = {
            'overall_performance': {
                'original_mean_agreement': float(original_mean),
                'optimized_mean_agreement': float(optimized_mean),
                'improvement_percentage_points': float(improvement),
                'target_70_percent_achieved': target_achievement
            },
            'energy_category_analysis': {
                'high_energy': {
                    'original': float(orig_high) if np.any(high_energy_mask) else None,
                    'optimized': float(opt_high) if np.any(high_energy_mask) else None,
                    'improvement': float(improvement_high) if np.any(high_energy_mask) else None
                },
                'medium_energy': {
                    'original': float(orig_med) if np.any(medium_energy_mask) else None,
                    'optimized': float(opt_med) if np.any(medium_energy_mask) else None,
                    'improvement': float(improvement_med) if np.any(medium_energy_mask) else None
                },
                'low_energy': {
                    'original': float(orig_low) if np.any(low_energy_mask) else None,
                    'optimized': float(opt_low) if np.any(low_energy_mask) else None,
                    'improvement': float(improvement_low) if np.any(low_energy_mask) else None
                }
            },
            'phase_classification': {
                'phase_changes': int(phase_changes),
                'consistency_rate': float(consistency_rate),
                'original_distribution': dict(orig_phase_dist),
                'optimized_distribution': dict(opt_phase_dist)
            },
            'individual_improvements': {
                'significant_improvements': int(significant_improvements),
                'deteriorations': int(deteriorations),
                'best_improvement_pp': float(np.max(improvements)) if len(improvements) > 0 else 0,
                'worst_improvement_pp': float(np.min(improvements)) if len(improvements) > 0 else 0
            },
            'statistical_significance': {
                'statistically_significant': significant_improvement,
                't_test_p_value': float(p_value_t) if 'p_value_t' in locals() else None,
                'wilcoxon_p_value': float(p_value_w) if 'p_value_w' in locals() else None
            }
        }
        
        return comparison_analysis
    
    def _create_validation_plots(self, validation_results: Dict, output_dir: str):
        """
        Crea visualizaciones de validación del modelo optimizado.
        """
        print("\nGenerando visualizaciones de validación...")
        
        plots_dir = f"{output_dir}/validation_plots"
        os.makedirs(plots_dir, exist_ok=True)
        
        # Plot 1: Comparación de acuerdos antes vs después
        self._plot_agreement_comparison(validation_results, f"{plots_dir}/agreement_comparison.png")
        
        # Plot 2: Mejoras por evento
        self._plot_individual_improvements(validation_results, f"{plots_dir}/individual_improvements.png")
        
        # Plot 3: Análisis por categoría de energía
        self._plot_energy_category_analysis(validation_results, f"{plots_dir}/energy_category_analysis.png")
        
        # Plot 4: Resumen ejecutivo de validación
        self._plot_validation_executive_summary(validation_results, f"{plots_dir}/validation_executive_summary.png")
        
        print(f"  Visualizaciones guardadas en: {plots_dir}/")
    
    def _plot_agreement_comparison(self, results: Dict, filename: str):
        """Plot comparación de acuerdos original vs optimizado."""
        original_results = results['original_results']
        optimized_results = results['optimized_results']
        
        original_agreements = [r['comparison']['global_agreement'] for r in original_results]
        optimized_agreements = [r['comparison']['global_agreement'] for r in optimized_results]
        event_names = [r['event'] for r in original_results]
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        # Subplot 1: Scatter plot comparativo
        ax1.scatter(original_agreements, optimized_agreements, alpha=0.7, s=60)
        
        # Línea diagonal (sin mejora)
        min_val = min(min(original_agreements), min(optimized_agreements))
        max_val = max(max(original_agreements), max(optimized_agreements))
        ax1.plot([min_val, max_val], [min_val, max_val], 'r--', alpha=0.5, label='Sin mejora')
        
        # Líneas de objetivo
        ax1.axhline(0.7, color='green', linestyle=':', alpha=0.7, label='Objetivo 70%')
        ax1.axvline(0.7, color='green', linestyle=':', alpha=0.7)
        
        ax1.set_xlabel('Acuerdo Original (%)')
        ax1.set_ylabel('Acuerdo Optimizado (%)')
        ax1.set_title('A. Comparación de Acuerdos Teoría-Observación')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Formato porcentual
        ax1.set_xlim(0, 1)
        ax1.set_ylim(0, 1)
        ax1.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:.0%}'))
        ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:.0%}'))
        
        # Subplot 2: Histograma de mejoras
        improvements = np.array(optimized_agreements) - np.array(original_agreements)
        
        ax2.hist(improvements * 100, bins=15, alpha=0.7, color='blue', edgecolor='black')
        ax2.axvline(0, color='red', linestyle='--', linewidth=2, label='Sin cambio')
        ax2.axvline(np.mean(improvements) * 100, color='green', linestyle='-', linewidth=2,
                   label=f'Mejora promedio: {np.mean(improvements)*100:.1f}pp')
        
        ax2.set_xlabel('Mejora en Acuerdo (puntos porcentuales)')
        ax2.set_ylabel('Número de Eventos')
        ax2.set_title('B. Distribución de Mejoras')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
    
    def _plot_individual_improvements(self, results: Dict, filename: str):
        """Plot mejoras individuales por evento."""
        original_results = results['original_results']
        optimized_results = results['optimized_results']
        
        original_agreements = np.array([r['comparison']['global_agreement'] for r in original_results])
        optimized_agreements = np.array([r['comparison']['global_agreement'] for r in optimized_results])
        event_names = [r['event'] for r in original_results]
        energies = [r['parameters']['energy_radiated'] for r in original_results]
        
        improvements = (optimized_agreements - original_agreements) * 100
        
        # Ordenar por mejora
        sorted_indices = np.argsort(improvements)[::-1]  # Mayor a menor
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
        
        # Subplot 1: Mejoras por evento (top 20)
        n_show = min(20, len(event_names))
        y_pos = np.arange(n_show)
        
        colors = ['green' if imp > 0 else 'red' for imp in improvements[sorted_indices[:n_show]]]
        
        bars = ax1.barh(y_pos, improvements[sorted_indices[:n_show]], color=colors, alpha=0.7)
        ax1.set_yticks(y_pos)
        ax1.set_yticklabels([event_names[i][:12] + '...' if len(event_names[i]) > 12 else event_names[i] 
                            for i in sorted_indices[:n_show]], fontsize=9)
        ax1.set_xlabel('Mejora en Acuerdo (puntos porcentuales)')
        ax1.set_title('A. Mejoras Individuales por Evento (Top 20)')
        ax1.axvline(0, color='black', linestyle='-', alpha=0.5)
        ax1.grid(True, axis='x', alpha=0.3)
        
        # Añadir valores en las barras
        for bar, improvement in zip(bars, improvements[sorted_indices[:n_show]]):
            width = bar.get_width()
            ax1.text(width + (1 if width >= 0 else -1), bar.get_y() + bar.get_height()/2,
                    f'{improvement:.1f}', ha='left' if width >= 0 else 'right', va='center', fontsize=8)
        
        # Subplot 2: Mejoras vs energía
        scatter = ax2.scatter(energies, improvements, c=energies, s=60, alpha=0.7, 
                             cmap='viridis', edgecolors='black', linewidth=0.5)
        
        # Línea de tendencia
        z = np.polyfit(energies, improvements, 1)
        p = np.poly1d(z)
        ax2.plot(energies, p(energies), "r--", alpha=0.8, linewidth=2)
        
        ax2.axhline(0, color='black', linestyle='-', alpha=0.5, label='Sin mejora')
        ax2.axhline(10, color='green', linestyle=':', alpha=0.7, label='Mejora significativa (>10pp)')
        
        ax2.set_xlabel('Energía Radiada (M☉c²)')
        ax2.set_ylabel('Mejora en Acuerdo (puntos porcentuales)')
        ax2.set_title('B. Mejoras vs Energía del Evento')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # Colorbar
        cbar = plt.colorbar(scatter, ax=ax2)
        cbar.set_label('Energía Radiada (M☉c²)')
        
        plt.tight_layout()
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
    
    def _plot_energy_category_analysis(self, results: Dict, filename: str):
        """Plot análisis por categoría de energía."""
        comparison = results['comparison_analysis']
        
        categories = ['high_energy', 'medium_energy', 'low_energy']
        category_labels = ['Alta Energía\n(>2.0 M☉c²)', 'Media Energía\n(0.5-2.0 M☉c²)', 'Baja Energía\n(<0.5 M☉c²)']
        
        original_values = []
        optimized_values = []
        improvements = []
        
        for cat in categories:
            cat_data = comparison['energy_category_analysis'][cat]
            if cat_data['original'] is not None:
                original_values.append(cat_data['original'])
                optimized_values.append(cat_data['optimized'])
                improvements.append(cat_data['improvement'])
            else:
                original_values.append(0)
                optimized_values.append(0)
                improvements.append(0)
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        # Subplot 1: Comparación antes vs después
        x = np.arange(len(category_labels))
        width = 0.35
        
        bars1 = ax1.bar(x - width/2, original_values, width, label='Original', alpha=0.7, color='lightblue')
        bars2 = ax1.bar(x + width/2, optimized_values, width, label='Optimizado', alpha=0.7, color='darkblue')
        
        # Línea de objetivo
        ax1.axhline(0.7, color='green', linestyle='--', alpha=0.7, label='Objetivo 70%')
        
        ax1.set_xlabel('Categoría de Energía')
        ax1.set_ylabel('Acuerdo con Teoría')
        ax1.set_title('A. Acuerdo por Categoría de Energía')
        ax1.set_xticks(x)
        ax1.set_xticklabels(category_labels)
        ax1.legend()
        ax1.grid(True, axis='y', alpha=0.3)
        ax1.set_ylim(0, 1)
        ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:.0%}'))
        
        # Añadir valores en las barras
        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                if height > 0:
                    ax1.text(bar.get_x() + bar.get_width()/2., height + 0.02,
                            f'{height:.1%}', ha='center', va='bottom', fontsize=9)
        
        # Subplot 2: Mejoras por categoría
        colors = ['green' if imp > 0 else 'red' if imp < 0 else 'gray' for imp in improvements]
        bars = ax2.bar(category_labels, improvements, color=colors, alpha=0.7)
        
        ax2.axhline(0, color='black', linestyle='-', alpha=0.5)
        ax2.set_xlabel('Categoría de Energía')
        ax2.set_ylabel('Mejora (puntos porcentuales)')
        ax2.set_title('B. Mejoras por Categoría')
        ax2.grid(True, axis='y', alpha=0.3)
        
        # Añadir valores en las barras
        for bar, improvement in zip(bars, improvements):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + (0.5 if height >= 0 else -0.5),
                    f'{improvement:.1f}pp', ha='center', va='bottom' if height >= 0 else 'top', 
                    fontsize=10, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
    
    def _plot_validation_executive_summary(self, results: Dict, filename: str):
        """Plot resumen ejecutivo de validación."""
        comparison = results['comparison_analysis']
        
        fig = plt.figure(figsize=(16, 10))
        gs = fig.add_gridspec(2, 3, hspace=0.3, wspace=0.3)
        
        fig.suptitle('VALIDACIÓN DEL MODELO OPTIMIZADO: RESUMEN EJECUTIVO', 
                    fontsize=16, fontweight='bold')
        
        # Panel 1: Mejora global
        ax1 = fig.add_subplot(gs[0, 0])
        
        original_mean = comparison['overall_performance']['original_mean_agreement']
        optimized_mean = comparison['overall_performance']['optimized_mean_agreement']
        
        categories = ['Original', 'Optimizado']
        values = [original_mean, optimized_mean]
        colors = ['lightcoral', 'lightgreen']
        
        bars = ax1.bar(categories, values, color=colors, alpha=0.8, edgecolor='black')
        ax1.axhline(0.7, color='red', linestyle='--', linewidth=2, label='Objetivo 70%')
        
        ax1.set_ylabel('Acuerdo Promedio con Teoría')
        ax1.set_title('Mejora Global del Modelo', fontweight='bold')
        ax1.set_ylim(0, 1)
        ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:.0%}'))
        ax1.legend()
        ax1.grid(True, axis='y', alpha=0.3)
        
        # Añadir valores y mejora
        for bar, value in zip(bars, values):
            ax1.text(bar.get_x() + bar.get_width()/2., value + 0.02,
                    f'{value:.1%}', ha='center', va='bottom', fontweight='bold', fontsize=12)
        
        improvement = comparison['overall_performance']['improvement_percentage_points']
        ax1.text(0.5, 0.85, f'Mejora:\n{improvement:+.1f}pp', transform=ax1.transAxes,
                ha='center', va='center', fontsize=14, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.8))
        
        # Panel 2: Objetivo alcanzado
        ax2 = fig.add_subplot(gs[0, 1])
        
        target_achieved = comparison['overall_performance']['target_70_percent_achieved']
        
        # Gauge de objetivo
        theta = np.linspace(0, np.pi, 100)
        r = 1
        
        # Background semicírculo
        ax2.plot(r * np.cos(theta), r * np.sin(theta), 'k-', linewidth=4)
        
        # Secciones coloreadas
        if target_achieved:
            ax2.fill_between(r * np.cos(theta), 0, r * np.sin(theta), color='green', alpha=0.7)
            needle_color = 'darkgreen'
            status_text = '✅ OBJETIVO\nALCANZADO'
            status_color = 'lightgreen'
        else:
            ax2.fill_between(r * np.cos(theta), 0, r * np.sin(theta), color='red', alpha=0.7)
            needle_color = 'darkred'
            status_text = '❌ OBJETIVO\nNO ALCANZADO'
            status_color = 'lightcoral'
        
        # Aguja
        needle_pos = optimized_mean * np.pi  # Posición proporcional
        ax2.arrow(0, 0, 0.8 * np.cos(needle_pos), 0.8 * np.sin(needle_pos),
                 head_width=0.08, head_length=0.08, fc=needle_color, ec=needle_color, linewidth=3)
        
        ax2.set_xlim(-1.2, 1.2)
        ax2.set_ylim(-0.2, 1.2)
        ax2.set_aspect('equal')
        ax2.axis('off')
        ax2.set_title('Objetivo >70%', fontweight='bold')
        
        # Texto de estado
        ax2.text(0, -0.1, status_text, ha='center', va='top', fontsize=12, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.5', facecolor=status_color, alpha=0.8))
        
        # Panel 3: Significancia estadística
        ax3 = fig.add_subplot(gs[0, 2])
        
        statistically_significant = comparison['statistical_significance']['statistically_significant']
        p_value = comparison['statistical_significance']['t_test_p_value']
        
        if p_value is not None:
            # Calcular significancia en sigmas
            from scipy.stats import norm
            if p_value > 0:
                significance = abs(norm.ppf(p_value / 2))
            else:
                significance = 5.0
        else:
            significance = 0
        
        # Gauge de significancia
        sections = [
            (0, np.pi/5, 'red', '<1σ'),
            (np.pi/5, 2*np.pi/5, 'orange', '1-2σ'),
            (2*np.pi/5, 3*np.pi/5, 'yellow', '2-3σ'),
            (3*np.pi/5, 4*np.pi/5, 'lightgreen', '3-4σ'),
            (4*np.pi/5, np.pi, 'green', '>4σ')
        ]
        
        for start, end, color, label in sections:
            theta_section = np.linspace(start, end, 50)
            ax3.fill_between(r * np.cos(theta_section), 0, r * np.sin(theta_section),
                           color=color, alpha=0.7)
        
        # Aguja de significancia
        needle_angle = min(significance * np.pi / 5, np.pi)
        ax3.arrow(0, 0, 0.8 * np.cos(needle_angle), 0.8 * np.sin(needle_angle),
                 head_width=0.08, head_length=0.08, fc='black', ec='black', linewidth=3)
        
        ax3.set_xlim(-1.2, 1.2)
        ax3.set_ylim(-0.2, 1.2)
        ax3.set_aspect('equal')
        ax3.axis('off')
        ax3.set_title(f'Significancia\nEstadística\n{significance:.1f}σ', fontweight='bold', ha='center')
        
        # Panel 4: Mejoras por categoría
        ax4 = fig.add_subplot(gs[1, :])
        
        # Tabla de resultados
        ax4.axis('off')
        
        summary_text = f"""
        RESUMEN DE VALIDACIÓN DEL MODELO OPTIMIZADO
        
        RENDIMIENTO GLOBAL:
        • Acuerdo original:              {original_mean:.1%}
        • Acuerdo optimizado:            {optimized_mean:.1%}
        • Mejora absoluta:               {improvement:+.1f} puntos porcentuales
        • Objetivo >70% alcanzado:       {'✅ SÍ' if target_achieved else '❌ NO'}
        
        MEJORAS POR CATEGORÍA DE ENERGÍA:
        • Alta energía (>2.0 M☉c²):      {comparison['energy_category_analysis']['high_energy']['improvement']:+.1f}pp
        • Media energía (0.5-2.0 M☉c²):  {comparison['energy_category_analysis']['medium_energy']['improvement']:+.1f}pp
        • Baja energía (<0.5 M☉c²):      {comparison['energy_category_analysis']['low_energy']['improvement']:+.1f}pp
        
        ANÁLISIS ESTADÍSTICO:
        • Mejora estadísticamente significativa: {'✅ SÍ' if statistically_significant else '❌ NO'}
        • p-value (t-test pareado):             {p_value:.2e if p_value else 'N/A'}
        • Significancia:                        {significance:.1f}σ
        
        EVENTOS INDIVIDUALES:
        • Eventos con mejora significativa (>10pp): {comparison['individual_improvements']['significant_improvements']}
        • Eventos con deterioro (>5pp):             {comparison['individual_improvements']['deteriorations']}
        • Mejor mejora individual:                  {comparison['individual_improvements']['best_improvement_pp']:+.1f}pp
        
        CONCLUSIÓN: {'✅ MODELO OPTIMIZADO EXITOSAMENTE VALIDADO' if target_achieved and statistically_significant else '⚠️ MODELO REQUIERE REFINAMIENTO ADICIONAL' if improvement > 5 else '❌ OPTIMIZACIÓN NO EFECTIVA'}
        """
        
        # Color de fondo basado en éxito
        if target_achieved and statistically_significant:
            bg_color = 'lightgreen'
        elif improvement > 5:
            bg_color = 'lightyellow'
        else:
            bg_color = 'lightcoral'
        
        ax4.text(0.5, 0.5, summary_text, transform=ax4.transAxes,
                fontsize=11, verticalalignment='center', horizontalalignment='center',
                bbox=dict(boxstyle='round,pad=1', facecolor=bg_color, alpha=0.8),
                fontfamily='monospace')
        
        plt.tight_layout()
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
    
    def _print_validation_summary(self, comparison_analysis: Dict):
        """Imprime resumen de validación."""
        print(f"\n{'='*80}")
        print("RESUMEN DE VALIDACIÓN DEL MODELO OPTIMIZADO")
        print(f"{'='*80}")
        
        overall = comparison_analysis['overall_performance']
        
        print(f"\n🎯 OBJETIVO PRINCIPAL: Mejorar acuerdo teoría-observación de 35% a >70%")
        print(f"   Resultado original:   {overall['original_mean_agreement']:.1%}")
        print(f"   Resultado optimizado: {overall['optimized_mean_agreement']:.1%}")
        print(f"   Mejora obtenida:      {overall['improvement_percentage_points']:+.1f} puntos porcentuales")
        print(f"   Objetivo alcanzado:   {'✅ SÍ' if overall['target_70_percent_achieved'] else '❌ NO'}")
        
        print(f"\n📊 SIGNIFICANCIA ESTADÍSTICA:")
        stats = comparison_analysis['statistical_significance']
        print(f"   Mejora significativa: {'✅ SÍ' if stats['statistically_significant'] else '❌ NO'}")
        if stats['t_test_p_value']:
            print(f"   p-value (t-test):     {stats['t_test_p_value']:.2e}")
        
        print(f"\n🔍 ANÁLISIS POR ENERGÍA:")
        energy_analysis = comparison_analysis['energy_category_analysis']
        for category, label in [('high_energy', 'Alta energía'), ('medium_energy', 'Media energía'), ('low_energy', 'Baja energía')]:
            cat_data = energy_analysis[category]
            if cat_data['improvement'] is not None:
                print(f"   {label}: {cat_data['improvement']:+.1f}pp")
        
        print(f"\n📈 EVENTOS INDIVIDUALES:")
        individual = comparison_analysis['individual_improvements']
        print(f"   Mejoras significativas: {individual['significant_improvements']} eventos")
        print(f"   Deterioros notables:    {individual['deteriorations']} eventos")
        print(f"   Mejor mejora:          {individual['best_improvement_pp']:+.1f}pp")
        
        # Conclusión final
        if overall['target_70_percent_achieved'] and stats['statistically_significant']:
            print(f"\n🎉 CONCLUSIÓN: ¡VALIDACIÓN EXITOSA!")
            print(f"   El modelo optimizado alcanza el objetivo y es estadísticamente significativo.")
        elif overall['improvement_percentage_points'] > 5:
            print(f"\n📊 CONCLUSIÓN: Validación parcial")
            print(f"   El modelo muestra mejoras sustanciales pero requiere refinamiento adicional.")
        else:
            print(f"\n🔍 CONCLUSIÓN: Optimización requiere revisión")
            print(f"   Las mejoras son limitadas. Considerar enfoques alternativos.")


def main():
    """
    Ejecuta validación del modelo optimizado.
    """
    print("VALIDACIÓN DEL MODELO TOPOLÓGICO OPTIMIZADO")
    print("="*80)
    print("\nEste script valida las mejoras del modelo optimizado")
    print("comparando rendimiento antes vs después de la optimización.")
    
    # Crear validador con parámetros optimizados por defecto
    validator = OptimizedModelValidator()
    
    # Ejecutar validación completa
    # Para demo, limitar a 20 eventos
    validation_results = validator.validate_optimized_model(max_events=20)
    
    # El resumen se imprime automáticamente
    
    print(f"\n✅ VALIDACIÓN COMPLETADA")
    print(f"📊 Resultados disponibles para análisis posterior")


if __name__ == "__main__":
    main()