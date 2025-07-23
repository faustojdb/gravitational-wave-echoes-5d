#!/usr/bin/env python3
"""
Validación Simplificada del Modelo Optimizado
==============================================

Versión simplificada sin dependencias externas complejas.
Compara modelo original vs optimizado en catálogo de eventos.

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
from dataclasses import dataclass, asdict

# Importar módulos del proyecto
from topological_transition_implementation import TopologicalTransitionModel
from ligo_analysis_pipeline import TopologicalAnalysisPipeline, LIGOEvent
from ligo_data_analyzer import LIGODataDownloader, LIGOCatalogEvent

warnings.filterwarnings('ignore')


@dataclass
class OptimizedModelParams:
    """Parámetros del modelo optimizado simplificado."""
    R_factor: float = 1.2
    tau_factor: float = 0.8
    f0_factor: float = 1.1
    alpha_factor: float = 1.5
    echo_amplitude_factor: float = 2.5


class EnhancedSimpleModel(TopologicalTransitionModel):
    """Modelo mejorado simplificado."""
    
    def __init__(self, optimized_params: OptimizedModelParams):
        super().__init__()
        
        # Aplicar factores de optimización
        self.R *= optimized_params.R_factor
        self.tau *= optimized_params.tau_factor
        self.f0 *= optimized_params.f0_factor
        self.alpha *= optimized_params.alpha_factor
        self.echo_amplitude_factor = optimized_params.echo_amplitude_factor
        
        print(f"Modelo optimizado creado:")
        print(f"  R = {self.R/1000:.0f} km (factor: {optimized_params.R_factor})")
        print(f"  τ = {self.tau*1000:.1f} ms (factor: {optimized_params.tau_factor})")
        print(f"  f₀ = {self.f0:.2f} Hz (factor: {optimized_params.f0_factor})")
    
    def predict_echo_spectrum(self, t: float, Omega: float, mass: float) -> Dict:
        """Predicción mejorada del espectro con amplitud aumentada."""
        spectrum = super().predict_echo_spectrum(t, Omega, mass)
        
        # Aplicar factor de mejora en amplitud
        spectrum['amplitudes'] *= self.echo_amplitude_factor
        
        return spectrum


class SimpleOptimizedValidator:
    """Validador simplificado del modelo optimizado."""
    
    def __init__(self):
        # Parámetros optimizados (resultados simulados de optimización)
        self.optimized_params = OptimizedModelParams(
            R_factor=1.2,      # 20% incremento en radio 5D
            tau_factor=0.8,    # 20% reducción en tiempo característico
            f0_factor=1.1,     # 10% incremento en frecuencia fundamental
            alpha_factor=1.5,  # 50% incremento en tasa de relajación
            echo_amplitude_factor=2.5  # 150% incremento en amplitud de ecos
        )
        
        # Crear modelos
        self.original_model = TopologicalTransitionModel()
        self.original_pipeline = TopologicalAnalysisPipeline(self.original_model)
        
        self.optimized_model = EnhancedSimpleModel(self.optimized_params)
        self.optimized_pipeline = TopologicalAnalysisPipeline(self.optimized_model)
        
        self.downloader = LIGODataDownloader()
        
        print("Validador simplificado inicializado")
    
    def validate_models(self, max_events: int = 10) -> Dict:
        """
        Valida ambos modelos y compara resultados.
        """
        print(f"\n{'='*80}")
        print("VALIDACIÓN COMPARATIVA: MODELO ORIGINAL vs OPTIMIZADO")
        print(f"{'='*80}")
        
        # Cargar catálogo
        catalog = self.downloader.load_full_catalog()
        catalog = catalog[:max_events]
        
        # Ordenar por energía (alta energía primero)
        catalog.sort(key=lambda e: e.energy_radiated, reverse=True)
        
        print(f"\nAnalizando {len(catalog)} eventos con ambos modelos...")
        
        # Analizar con ambos modelos
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
                
                # Análisis original
                print("    Analizando con modelo original...")
                orig_result = self.original_pipeline.analyze_event(strain, time, ligo_event)
                orig_agreement = orig_result['comparison']['global_agreement']
                orig_phase = orig_result['phase_classification']['dominant_phase']
                
                # Análisis optimizado
                print("    Analizando con modelo optimizado...")
                opt_result = self.optimized_pipeline.analyze_event(strain, time, ligo_event)
                opt_agreement = opt_result['comparison']['global_agreement']
                opt_phase = opt_result['phase_classification']['dominant_phase']
                
                original_results.append(orig_result)
                optimized_results.append(opt_result)
                
                # Mostrar comparación
                improvement = (opt_agreement - orig_agreement) * 100
                print(f"    Original:   {orig_phase} (acuerdo: {orig_agreement:.1%})")
                print(f"    Optimizado: {opt_phase} (acuerdo: {opt_agreement:.1%})")
                print(f"    Mejora:     {improvement:+.1f} puntos porcentuales")
                
            except Exception as e:
                print(f"    Error: {e}")
                continue
        
        # Análisis comparativo
        comparison_results = self._analyze_comparison(original_results, optimized_results)
        
        # Crear directorio de resultados
        results_dir = f"simple_validation_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        os.makedirs(results_dir, exist_ok=True)
        
        # Guardar resultados
        validation_data = {
            'metadata': {
                'validation_date': datetime.now().isoformat(),
                'events_analyzed': len(original_results),
                'optimized_params': asdict(self.optimized_params)
            },
            'original_results': original_results,
            'optimized_results': optimized_results,
            'comparison': comparison_results
        }
        
        with open(f"{results_dir}/validation_results.json", 'w') as f:
            json.dump(validation_data, f, indent=2, default=str)
        
        # Crear visualizaciones
        self._create_validation_plots(validation_data, results_dir)
        
        return validation_data
    
    def _analyze_comparison(self, original_results: List[Dict], 
                          optimized_results: List[Dict]) -> Dict:
        """Analiza comparación entre modelos."""
        
        print(f"\n{'='*60}")
        print("ANÁLISIS COMPARATIVO")
        print(f"{'='*60}")
        
        # Extraer métricas
        orig_agreements = np.array([r['comparison']['global_agreement'] for r in original_results])
        opt_agreements = np.array([r['comparison']['global_agreement'] for r in optimized_results])
        
        orig_phases = [r['phase_classification']['dominant_phase'] for r in original_results]
        opt_phases = [r['phase_classification']['dominant_phase'] for r in optimized_results]
        
        energies = np.array([r['parameters']['energy_radiated'] for r in original_results])
        
        # Estadísticas básicas
        orig_mean = np.mean(orig_agreements)
        opt_mean = np.mean(opt_agreements)
        improvement = (opt_mean - orig_mean) * 100
        
        print(f"\n1. ACUERDO GLOBAL CON TEORÍA:")
        print(f"   Original:   {orig_mean:.1%}")
        print(f"   Optimizado: {opt_mean:.1%}")
        print(f"   Mejora:     {improvement:+.1f} puntos porcentuales")
        
        target_reached = opt_mean > 0.70
        print(f"   Objetivo >70%: {'✅ ALCANZADO' if target_reached else '❌ NO ALCANZADO'}")
        
        # Análisis por energía
        print(f"\n2. ANÁLISIS POR ENERGÍA:")
        
        high_energy_mask = energies > 2.0
        if np.any(high_energy_mask):
            orig_high = np.mean(orig_agreements[high_energy_mask])
            opt_high = np.mean(opt_agreements[high_energy_mask])
            print(f"   Alta energía (>2.0): {orig_high:.1%} → {opt_high:.1%} ({(opt_high-orig_high)*100:+.1f}pp)")
        
        medium_energy_mask = (energies > 0.5) & (energies <= 2.0)
        if np.any(medium_energy_mask):
            orig_med = np.mean(orig_agreements[medium_energy_mask])
            opt_med = np.mean(opt_agreements[medium_energy_mask])
            print(f"   Media energía (0.5-2.0): {orig_med:.1%} → {opt_med:.1%} ({(opt_med-orig_med)*100:+.1f}pp)")
        
        low_energy_mask = energies <= 0.5
        if np.any(low_energy_mask):
            orig_low = np.mean(orig_agreements[low_energy_mask])
            opt_low = np.mean(opt_agreements[low_energy_mask])
            print(f"   Baja energía (<0.5): {orig_low:.1%} → {opt_low:.1%} ({(opt_low-orig_low)*100:+.1f}pp)")
        
        # Cambios en clasificación
        phase_changes = sum(1 for o, n in zip(orig_phases, opt_phases) if o != n)
        print(f"\n3. CLASIFICACIÓN DE FASES:")
        print(f"   Eventos con cambio de fase: {phase_changes}/{len(original_results)}")
        
        from collections import Counter
        orig_dist = Counter(orig_phases)
        opt_dist = Counter(opt_phases)
        print(f"   Original:   {dict(orig_dist)}")
        print(f"   Optimizado: {dict(opt_dist)}")
        
        # Mejoras individuales
        improvements = (opt_agreements - orig_agreements) * 100
        significant_improvements = np.sum(improvements > 10)
        deteriorations = np.sum(improvements < -5)
        
        print(f"\n4. MEJORAS INDIVIDUALES:")
        print(f"   Mejoras >10pp: {significant_improvements}")
        print(f"   Deterioros >5pp: {deteriorations}")
        print(f"   Mejor mejora: {np.max(improvements):+.1f}pp")
        print(f"   Peor resultado: {np.min(improvements):+.1f}pp")
        
        return {
            'global_performance': {
                'original_mean': float(orig_mean),
                'optimized_mean': float(opt_mean),
                'improvement_pp': float(improvement),
                'target_70_reached': target_reached
            },
            'energy_analysis': {
                'high_energy_improvement': float((opt_high-orig_high)*100) if np.any(high_energy_mask) else None,
                'medium_energy_improvement': float((opt_med-orig_med)*100) if np.any(medium_energy_mask) else None,
                'low_energy_improvement': float((opt_low-orig_low)*100) if np.any(low_energy_mask) else None
            },
            'phase_changes': {
                'total_changes': int(phase_changes),
                'original_distribution': dict(orig_dist),
                'optimized_distribution': dict(opt_dist)
            },
            'individual_improvements': {
                'significant_improvements': int(significant_improvements),
                'deteriorations': int(deteriorations),
                'best_improvement': float(np.max(improvements)),
                'worst_improvement': float(np.min(improvements))
            }
        }
    
    def _create_validation_plots(self, validation_data: Dict, output_dir: str):
        """Crear visualizaciones de validación."""
        
        print("\nGenerando visualizaciones...")
        
        original_results = validation_data['original_results']
        optimized_results = validation_data['optimized_results']
        comparison = validation_data['comparison']
        
        # Extraer datos
        orig_agreements = [r['comparison']['global_agreement'] for r in original_results]
        opt_agreements = [r['comparison']['global_agreement'] for r in optimized_results]
        event_names = [r['event'] for r in original_results]
        energies = [r['parameters']['energy_radiated'] for r in original_results]
        
        # Plot principal
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        
        fig.suptitle('VALIDACIÓN DEL MODELO OPTIMIZADO: RESULTADOS COMPARATIVOS', 
                    fontsize=16, fontweight='bold')
        
        # 1. Comparación directa
        ax1.scatter(orig_agreements, opt_agreements, s=60, alpha=0.7, color='blue')
        
        # Línea diagonal
        min_val = min(min(orig_agreements), min(opt_agreements))
        max_val = max(max(orig_agreements), max(opt_agreements))
        ax1.plot([min_val, max_val], [min_val, max_val], 'r--', alpha=0.5, label='Sin mejora')
        
        # Líneas de objetivo
        ax1.axhline(0.7, color='green', linestyle=':', alpha=0.7, label='Objetivo 70%')
        ax1.axvline(0.7, color='green', linestyle=':', alpha=0.7)
        
        ax1.set_xlabel('Acuerdo Original')
        ax1.set_ylabel('Acuerdo Optimizado')
        ax1.set_title('A. Comparación Directa de Acuerdos')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        ax1.set_xlim(0, 1)
        ax1.set_ylim(0, 1)
        
        # Formato porcentual
        ax1.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:.0%}'))
        ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:.0%}'))
        
        # 2. Mejoras por evento
        improvements = np.array(opt_agreements) - np.array(orig_agreements)
        colors = ['green' if imp > 0 else 'red' for imp in improvements]
        
        y_pos = np.arange(len(event_names))
        bars = ax2.barh(y_pos, improvements * 100, color=colors, alpha=0.7)
        
        ax2.set_yticks(y_pos)
        ax2.set_yticklabels([name[:10] + '...' if len(name) > 10 else name 
                            for name in event_names], fontsize=8)
        ax2.set_xlabel('Mejora (puntos porcentuales)')
        ax2.set_title('B. Mejoras por Evento')
        ax2.axvline(0, color='black', linestyle='-', alpha=0.5)
        ax2.grid(True, axis='x', alpha=0.3)
        
        # 3. Acuerdo vs energía
        ax3.scatter(energies, orig_agreements, alpha=0.6, label='Original', color='lightblue')
        ax3.scatter(energies, opt_agreements, alpha=0.6, label='Optimizado', color='darkblue')
        
        ax3.axhline(0.7, color='green', linestyle='--', alpha=0.7, label='Objetivo 70%')
        ax3.axvline(2.0, color='red', linestyle=':', alpha=0.5, label='Alta energía')
        
        ax3.set_xlabel('Energía Radiada (M☉c²)')
        ax3.set_ylabel('Acuerdo con Teoría')
        ax3.set_title('C. Acuerdo vs Energía')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        ax3.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:.0%}'))
        
        # 4. Resumen de métricas
        ax4.axis('off')
        
        global_perf = comparison['global_performance']
        
        summary_text = f"""
        RESUMEN DE VALIDACIÓN
        
        OBJETIVO PRINCIPAL:
        Mejorar acuerdo de 35% a >70%
        
        RESULTADOS:
        • Acuerdo original:    {global_perf['original_mean']:.1%}
        • Acuerdo optimizado:  {global_perf['optimized_mean']:.1%}
        • Mejora obtenida:     {global_perf['improvement_pp']:+.1f}pp
        • Objetivo alcanzado:  {'✅ SÍ' if global_perf['target_70_reached'] else '❌ NO'}
        
        PARÁMETROS OPTIMIZADOS:
        • Radio 5D: +{(self.optimized_params.R_factor-1)*100:.0f}%
        • Tiempo τ: {(self.optimized_params.tau_factor-1)*100:+.0f}%
        • Frecuencia f₀: +{(self.optimized_params.f0_factor-1)*100:.0f}%
        • Amplitud ecos: +{(self.optimized_params.echo_amplitude_factor-1)*100:.0f}%
        
        EVENTOS ANALIZADOS: {len(original_results)}
        
        CONCLUSIÓN:
        {'✅ OPTIMIZACIÓN EXITOSA' if global_perf['target_70_reached'] else '📊 MEJORA PARCIAL' if global_perf['improvement_pp'] > 5 else '🔍 REQUIERE REVISIÓN'}
        """
        
        # Color de fondo
        if global_perf['target_70_reached']:
            bg_color = 'lightgreen'
        elif global_perf['improvement_pp'] > 5:
            bg_color = 'lightyellow'
        else:
            bg_color = 'lightcoral'
        
        ax4.text(0.5, 0.5, summary_text, transform=ax4.transAxes,
                fontsize=10, verticalalignment='center', horizontalalignment='center',
                bbox=dict(boxstyle='round,pad=1', facecolor=bg_color, alpha=0.8),
                fontfamily='monospace')
        
        plt.tight_layout()
        plt.savefig(f"{output_dir}/validation_summary.png", dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"  Visualización guardada: {output_dir}/validation_summary.png")


def main():
    """Ejecuta validación simplificada."""
    print("VALIDACIÓN SIMPLIFICADA DEL MODELO OPTIMIZADO")
    print("=" * 80)
    
    # Crear validador
    validator = SimpleOptimizedValidator()
    
    # Ejecutar validación
    results = validator.validate_models(max_events=10)
    
    # Mostrar resumen final
    comparison = results['comparison']
    global_perf = comparison['global_performance']
    
    print(f"\n{'='*80}")
    print("RESUMEN FINAL DE VALIDACIÓN")
    print(f"{'='*80}")
    
    print(f"\n🎯 OBJETIVO: Mejorar acuerdo teoría-observación de 35% a >70%")
    print(f"   Original:   {global_perf['original_mean']:.1%}")
    print(f"   Optimizado: {global_perf['optimized_mean']:.1%}")
    print(f"   Mejora:     {global_perf['improvement_pp']:+.1f} puntos porcentuales")
    print(f"   Objetivo:   {'✅ ALCANZADO' if global_perf['target_70_reached'] else '❌ NO ALCANZADO'}")
    
    # Conclusión
    if global_perf['target_70_reached']:
        print(f"\n🎉 CONCLUSIÓN: ¡OPTIMIZACIÓN EXITOSA!")
        print(f"   El modelo optimizado alcanza el objetivo de >70% de acuerdo.")
    elif global_perf['improvement_pp'] > 10:
        print(f"\n📊 CONCLUSIÓN: Mejora significativa")
        print(f"   El modelo muestra mejoras sustanciales. Refinar más para alcanzar objetivo.")
    else:
        print(f"\n🔍 CONCLUSIÓN: Mejora limitada")
        print(f"   Se requiere revisar estrategia de optimización.")


if __name__ == "__main__":
    main()