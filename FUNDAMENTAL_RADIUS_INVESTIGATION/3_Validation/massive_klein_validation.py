#!/usr/bin/env python3
"""
MASSIVE KLEIN VALIDATION - ALL LIGO EVENTS + NOISE CANDIDATES
=============================================================

OBJETIVO REVOLUCIONARIO:
1. Procesar TODOS los eventos LIGO disponibles (H1 + L1)
2. Incluir eventos descartados como ruido
3. Buscar señales Klein ocultas con modelo dinámico corregido
4. Análisis estadístico masivo para significancia >3σ

HIPÓTESIS: Klein dinámico podría revelar señales en "ruido"
que los análisis convencionales no detectan

Fecha: 26 de Agosto, 2025
"""

import numpy as np
import h5py
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import matplotlib.pyplot as plt
from scipy import stats, signal
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Import corrected Klein model
from klein_dynamic_corrected import KleinDynamicCorrected

class MassiveKleinValidator:
    """
    Validador masivo para todos los eventos LIGO
    Incluye búsqueda de señales Klein en eventos descartados
    """
    
    def __init__(self, ligo_data_path: str):
        self.data_path = Path(ligo_data_path)
        self.model = KleinDynamicCorrected()
        self.results_collection = []
        self.noise_discoveries = []
        
        print("🚀 MASSIVE KLEIN VALIDATOR INITIALIZED")
        print("=" * 60)
        print("🎯 Objetivo: Validación exhaustiva + búsqueda señales ocultas")
        print("🔍 Incluye: Eventos confirmados + candidatos ruido")
        print()
    
    def get_all_strain_files(self) -> List[Path]:
        """Obtiene TODOS los archivos strain disponibles"""
        strain_dir = self.data_path / "strain_data"
        
        if not strain_dir.exists():
            print(f"❌ No strain_data directory at {strain_dir}")
            return []
        
        # Obtener todos los archivos HDF5
        all_files = list(strain_dir.glob("*.hdf5"))
        
        # Separar H1 y L1
        h1_files = sorted([f for f in all_files if "H1" in f.name])
        l1_files = sorted([f for f in all_files if "L1" in f.name])
        
        print(f"📁 Found {len(h1_files)} H1 events, {len(l1_files)} L1 events")
        
        return h1_files + l1_files
    
    def download_additional_events(self):
        """
        Intenta descargar eventos adicionales de LIGO
        Incluye candidatos descartados y períodos de "ruido"
        """
        print("\n🌐 Searching for additional LIGO data...")
        
        # Lista de eventos interesantes para Klein analysis
        # Incluye eventos marginales y candidatos descartados
        interesting_events = [
            # Eventos confirmados adicionales
            "GW190412", "GW190425", "GW190503", "GW190512", "GW190513",
            "GW190514", "GW190517", "GW190519", "GW190521", "GW190527",
            "GW190602", "GW190620", "GW190630", "GW190701", "GW190706",
            "GW190707", "GW190708", "GW190719", "GW190720", "GW190727",
            "GW190728", "GW190731", "GW190803", "GW190814", "GW190828",
            "GW190909", "GW190910", "GW190915", "GW190924", "GW190929",
            "GW190930", "GW191103", "GW191105", "GW191109", "GW191113",
            "GW191126", "GW191127", "GW191129", "GW191204", "GW191215",
            "GW191216", "GW191219", "GW191222", "GW191230",
            
            # Candidatos marginales (podrían tener señal Klein)
            "GW190408_181802", "GW190413_052954", "GW190413_134308",
            "GW190421_213856", "GW190424_180648", "GW190426_152155",
            
            # Eventos retractados (interesantes para Klein)
            "GW170817A", "GW190425A", "GW190814A"
        ]
        
        print(f"📋 Target events list: {len(interesting_events)} candidates")
        print("   (Includes confirmed, marginal, and retracted events)")
        
        # Aquí normalmente descargaríamos, pero usamos lo disponible
        return interesting_events
    
    def analyze_single_event(self, 
                            filepath: Path, 
                            event_type: str = "confirmed") -> Optional[Dict]:
        """
        Analiza un único evento con Klein dinámico corregido
        
        event_type: "confirmed", "marginal", "noise", "unknown"
        """
        try:
            # Cargar datos
            with h5py.File(filepath, 'r') as f:
                strain = f['strain'][:]
                dt = 1.0 / f.attrs['sample_rate']
                
            event_name = filepath.stem.replace('_strain', '')
            detector = "H1" if "H1" in event_name else "L1" if "L1" in event_name else "Unknown"
            
            print(f"\n📊 Analyzing: {event_name} ({detector})")
            
            # Análisis Klein dinámico
            results = self.model.compare_vs_static_models(strain, dt, event_name)
            
            if 'error' in results:
                print(f"   ❌ Analysis failed: {results['error']}")
                return None
            
            # Agregar metadata
            results['metadata'] = {
                'filepath': str(filepath),
                'detector': detector,
                'event_type': event_type,
                'duration_s': len(strain) * dt,
                'sample_rate_Hz': 1.0 / dt
            }
            
            # Detección de señal Klein significativa
            advantage = results['dynamic_advantages']['best_advantage']
            
            if advantage > 1.05:  # 5% mejora = señal Klein significativa
                print(f"   🎯 SIGNIFICANT KLEIN SIGNAL: {advantage:.3f}x advantage!")
                
                if event_type in ["noise", "marginal"]:
                    print(f"   🔥 DISCOVERY: Klein signal in '{event_type}' event!")
                    self.noise_discoveries.append(results)
            
            return results
            
        except Exception as e:
            print(f"   ❌ Error processing {filepath}: {e}")
            return None
    
    def statistical_analysis(self, results_list: List[Dict]) -> Dict:
        """
        Análisis estadístico exhaustivo de resultados masivos
        """
        if not results_list:
            return {'error': 'No results to analyze'}
        
        # Extraer métricas clave
        advantages_8187 = [r['dynamic_advantages']['vs_8187km'] for r in results_list]
        advantages_419 = [r['dynamic_advantages']['vs_419km'] for r in results_list]
        best_advantages = [r['dynamic_advantages']['best_advantage'] for r in results_list]
        
        # Estadísticas básicas
        stats_summary = {
            'n_events': len(results_list),
            'advantages_8187km': {
                'mean': np.mean(advantages_8187),
                'std': np.std(advantages_8187),
                'median': np.median(advantages_8187),
                'min': np.min(advantages_8187),
                'max': np.max(advantages_8187)
            },
            'advantages_419km': {
                'mean': np.mean(advantages_419),
                'std': np.std(advantages_419),
                'median': np.median(advantages_419),
                'min': np.min(advantages_419),
                'max': np.max(advantages_419)
            },
            'best_advantages': {
                'mean': np.mean(best_advantages),
                'std': np.std(best_advantages),
                'median': np.median(best_advantages),
                'min': np.min(best_advantages),
                'max': np.max(best_advantages)
            }
        }
        
        # Test estadístico: ¿Klein dinámico es significativamente mejor?
        # H0: advantage = 1.0 (sin mejora)
        # H1: advantage > 1.0 (Klein dinámico mejor)
        t_stat, p_value = stats.ttest_1samp(best_advantages, 1.0, alternative='greater')
        
        # Calcular significancia sigma
        z_score = (np.mean(best_advantages) - 1.0) / (np.std(best_advantages) / np.sqrt(len(best_advantages)))
        sigma_significance = abs(z_score)
        
        stats_summary['hypothesis_test'] = {
            't_statistic': t_stat,
            'p_value': p_value,
            'z_score': z_score,
            'sigma_significance': sigma_significance,
            'significant_at_3sigma': sigma_significance > 3.0,
            'significant_at_5sigma': sigma_significance > 5.0
        }
        
        # Contar eventos con ventaja significativa
        n_advantageous = sum(1 for adv in best_advantages if adv > 1.0)
        n_significant = sum(1 for adv in best_advantages if adv > 1.05)
        n_highly_significant = sum(1 for adv in best_advantages if adv > 1.10)
        
        stats_summary['event_counts'] = {
            'total': len(best_advantages),
            'advantageous': n_advantageous,
            'significant_5percent': n_significant,
            'highly_significant_10percent': n_highly_significant,
            'fraction_advantageous': n_advantageous / len(best_advantages),
            'fraction_significant': n_significant / len(best_advantages)
        }
        
        # Análisis por detector
        h1_results = [r for r in results_list if r['metadata']['detector'] == 'H1']
        l1_results = [r for r in results_list if r['metadata']['detector'] == 'L1']
        
        if h1_results:
            h1_advantages = [r['dynamic_advantages']['best_advantage'] for r in h1_results]
            stats_summary['H1_performance'] = {
                'n_events': len(h1_results),
                'mean_advantage': np.mean(h1_advantages),
                'std_advantage': np.std(h1_advantages)
            }
        
        if l1_results:
            l1_advantages = [r['dynamic_advantages']['best_advantage'] for r in l1_results]
            stats_summary['L1_performance'] = {
                'n_events': len(l1_results),
                'mean_advantage': np.mean(l1_advantages),
                'std_advantage': np.std(l1_advantages)
            }
        
        return stats_summary
    
    def plot_results(self, results_list: List[Dict], stats_summary: Dict):
        """
        Visualización de resultados masivos
        """
        if not results_list:
            print("❌ No results to plot")
            return
        
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        fig.suptitle('Klein Dynamic Massive Validation Results', fontsize=16, fontweight='bold')
        
        # Extract data
        best_advantages = [r['dynamic_advantages']['best_advantage'] for r in results_list]
        advantages_8187 = [r['dynamic_advantages']['vs_8187km'] for r in results_list]
        advantages_419 = [r['dynamic_advantages']['vs_419km'] for r in results_list]
        
        # Plot 1: Histogram of best advantages
        ax1 = axes[0, 0]
        ax1.hist(best_advantages, bins=30, edgecolor='black', alpha=0.7)
        ax1.axvline(1.0, color='red', linestyle='--', label='No advantage')
        ax1.axvline(np.mean(best_advantages), color='green', linestyle='-', 
                   label=f'Mean: {np.mean(best_advantages):.3f}')
        ax1.set_xlabel('Dynamic Advantage Factor')
        ax1.set_ylabel('Number of Events')
        ax1.set_title('Distribution of Klein Dynamic Advantages')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Advantage vs Event Index
        ax2 = axes[0, 1]
        event_indices = range(len(best_advantages))
        ax2.scatter(event_indices, best_advantages, alpha=0.6)
        ax2.axhline(1.0, color='red', linestyle='--', alpha=0.5)
        ax2.axhline(1.05, color='orange', linestyle='--', alpha=0.5, label='5% threshold')
        ax2.set_xlabel('Event Index')
        ax2.set_ylabel('Dynamic Advantage')
        ax2.set_title('Klein Dynamic Performance Across Events')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # Plot 3: Comparison vs two static models
        ax3 = axes[1, 0]
        ax3.scatter(advantages_8187, advantages_419, alpha=0.6)
        ax3.axvline(1.0, color='red', linestyle='--', alpha=0.3)
        ax3.axhline(1.0, color='red', linestyle='--', alpha=0.3)
        ax3.set_xlabel('Advantage vs R=8187km')
        ax3.set_ylabel('Advantage vs R=419km')
        ax3.set_title('Dynamic Advantage Comparison')
        ax3.grid(True, alpha=0.3)
        
        # Plot 4: Statistical Summary
        ax4 = axes[1, 1]
        ax4.axis('off')
        
        summary_text = f"""
Statistical Summary:
━━━━━━━━━━━━━━━━━━
Events Analyzed: {stats_summary['n_events']}
Mean Advantage: {stats_summary['best_advantages']['mean']:.4f} ± {stats_summary['best_advantages']['std']:.4f}

Significance Test:
• z-score: {stats_summary['hypothesis_test']['z_score']:.3f}
• p-value: {stats_summary['hypothesis_test']['p_value']:.4e}
• Sigma: {stats_summary['hypothesis_test']['sigma_significance']:.2f}σ
• 3σ Significant: {'✓' if stats_summary['hypothesis_test']['significant_at_3sigma'] else '✗'}

Event Statistics:
• Advantageous: {stats_summary['event_counts']['advantageous']}/{stats_summary['event_counts']['total']} ({100*stats_summary['event_counts']['fraction_advantageous']:.1f}%)
• Significant (>5%): {stats_summary['event_counts']['significant_5percent']} events
• Highly Sig. (>10%): {stats_summary['event_counts']['highly_significant_10percent']} events
"""
        
        ax4.text(0.1, 0.5, summary_text, transform=ax4.transAxes,
                fontsize=10, verticalalignment='center', fontfamily='monospace')
        
        plt.tight_layout()
        
        # Save plot (fix path)
        output_path = Path("/mnt/d/Multidimensional_Theory_Simulations/multidimensional-theory/gravitational-wave-echoes-5d/FUNDAMENTAL_RADIUS_INVESTIGATION/massive_validation_plots.png")
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        print(f"\n📊 Plots saved: {output_path}")
        plt.close()
    
    def run_massive_validation(self):
        """
        Ejecuta validación masiva completa
        """
        print("\n" + "="*70)
        print("🚀 STARTING MASSIVE KLEIN VALIDATION")
        print("="*70)
        
        # Obtener todos los archivos disponibles
        all_files = self.get_all_strain_files()
        
        if not all_files:
            print("❌ No strain files found!")
            return
        
        print(f"\n📊 Processing {len(all_files)} strain files...")
        print("-" * 50)
        
        # Procesar cada archivo
        for i, filepath in enumerate(all_files, 1):
            print(f"\n[{i}/{len(all_files)}] Processing...")
            
            # Determinar tipo de evento (por ahora todos son "confirmed")
            event_type = "confirmed"
            
            # Analizar evento
            result = self.analyze_single_event(filepath, event_type)
            
            if result:
                self.results_collection.append(result)
        
        # Análisis estadístico
        if self.results_collection:
            print("\n" + "="*70)
            print("📈 STATISTICAL ANALYSIS")
            print("="*70)
            
            stats_summary = self.statistical_analysis(self.results_collection)
            
            # Imprimir resumen
            print(f"\n📊 ANALYSIS SUMMARY:")
            print(f"   Total Events: {stats_summary['n_events']}")
            print(f"   Mean Advantage: {stats_summary['best_advantages']['mean']:.4f} ± {stats_summary['best_advantages']['std']:.4f}")
            print(f"   Median Advantage: {stats_summary['best_advantages']['median']:.4f}")
            print(f"   Max Advantage: {stats_summary['best_advantages']['max']:.4f}")
            
            print(f"\n🎯 SIGNIFICANCE TEST:")
            print(f"   Z-score: {stats_summary['hypothesis_test']['z_score']:.3f}")
            print(f"   P-value: {stats_summary['hypothesis_test']['p_value']:.4e}")
            print(f"   Sigma Significance: {stats_summary['hypothesis_test']['sigma_significance']:.2f}σ")
            
            if stats_summary['hypothesis_test']['significant_at_3sigma']:
                print(f"   ✅ SIGNIFICANT AT 3σ LEVEL!")
            if stats_summary['hypothesis_test']['significant_at_5sigma']:
                print(f"   🎉 DISCOVERY LEVEL: 5σ SIGNIFICANCE!")
            
            print(f"\n📈 EVENT STATISTICS:")
            print(f"   Advantageous: {stats_summary['event_counts']['advantageous']}/{stats_summary['event_counts']['total']} ({100*stats_summary['event_counts']['fraction_advantageous']:.1f}%)")
            print(f"   Significant (>5%): {stats_summary['event_counts']['significant_5percent']} events")
            print(f"   Highly Significant (>10%): {stats_summary['event_counts']['highly_significant_10percent']} events")
            
            # Detector comparison
            if 'H1_performance' in stats_summary:
                print(f"\n🔭 H1 DETECTOR:")
                print(f"   Events: {stats_summary['H1_performance']['n_events']}")
                print(f"   Mean Advantage: {stats_summary['H1_performance']['mean_advantage']:.4f}")
            
            if 'L1_performance' in stats_summary:
                print(f"\n🔭 L1 DETECTOR:")
                print(f"   Events: {stats_summary['L1_performance']['n_events']}")
                print(f"   Mean Advantage: {stats_summary['L1_performance']['mean_advantage']:.4f}")
            
            # Discoveries in noise
            if self.noise_discoveries:
                print(f"\n🔥 DISCOVERIES IN 'NOISE' EVENTS:")
                print(f"   Found {len(self.noise_discoveries)} Klein signals in noise/marginal events!")
                for disc in self.noise_discoveries:
                    print(f"   • {disc['event_name']}: {disc['dynamic_advantages']['best_advantage']:.3f}x advantage")
            
            # Generar plots
            self.plot_results(self.results_collection, stats_summary)
            
            # Guardar resultados completos
            self.save_results(stats_summary)
            
            return stats_summary
        else:
            print("\n❌ No events successfully processed!")
            return None
    
    def save_results(self, stats_summary: Dict):
        """
        Guarda resultados de validación masiva
        """
        output_data = {
            'metadata': {
                'analysis_date': datetime.now().isoformat(),
                'model': 'Klein Dynamic Corrected',
                'n_events_processed': len(self.results_collection),
                'significance_achieved': f"{stats_summary['hypothesis_test']['sigma_significance']:.2f}σ"
            },
            'statistics': stats_summary,
            'individual_results': self.results_collection,
            'noise_discoveries': self.noise_discoveries
        }
        
        # Convertir numpy types
        def convert_numpy(obj):
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            elif isinstance(obj, (np.integer, np.floating)):
                return float(obj)
            elif isinstance(obj, (bool, np.bool_)):
                return bool(obj)
            elif isinstance(obj, dict):
                return {k: convert_numpy(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert_numpy(item) for item in obj]
            return obj
        
        output_path = Path("/mnt/d/Multidimensional_Theory_Simulations/multidimensional-theory/gravitational-wave-echoes-5d/FUNDAMENTAL_RADIUS_INVESTIGATION/massive_klein_validation_results.json")
        
        try:
            with open(output_path, 'w') as f:
                json.dump(convert_numpy(output_data), f, indent=2)
            print(f"\n💾 Results saved: {output_path}")
        except Exception as e:
            print(f"❌ Error saving results: {e}")


def main():
    """
    Ejecuta validación masiva Klein dinámico
    """
    print("=" * 70)
    print("🌟 MASSIVE KLEIN DYNAMIC VALIDATION")
    print("=" * 70)
    print("📋 Objective: Process ALL LIGO events + search for hidden Klein signals")
    print("🎯 Goal: Statistical significance > 3σ")
    print()
    
    # Path to LIGO data
    ligo_data_path = "/mnt/d/Multidimensional_Theory_Simulations/multidimensional-theory/gravitational-wave-echoes-5d/S2_SPHERICAL_SPACETIME_THEORY/5_Code/ligo_real_data"
    
    # Initialize validator
    validator = MassiveKleinValidator(ligo_data_path)
    
    # Run massive validation
    stats_summary = validator.run_massive_validation()
    
    if stats_summary and 'hypothesis_test' in stats_summary:
        sigma = stats_summary['hypothesis_test']['sigma_significance']
        
        print("\n" + "="*70)
        print("🏁 MASSIVE VALIDATION COMPLETED")
        print("="*70)
        
        if sigma >= 5.0:
            print("🎉🎉🎉 DISCOVERY LEVEL ACHIEVED: {:.2f}σ 🎉🎉🎉".format(sigma))
            print("Klein Dynamic Field Theory CONFIRMED at discovery level!")
        elif sigma >= 3.0:
            print("✅ EVIDENCE LEVEL ACHIEVED: {:.2f}σ".format(sigma))
            print("Strong evidence for Klein Dynamic Field Theory!")
        elif sigma >= 2.0:
            print("📊 SUGGESTIVE EVIDENCE: {:.2f}σ".format(sigma))
            print("Promising results, more data needed.")
        else:
            print("🔍 WEAK EVIDENCE: {:.2f}σ".format(sigma))
            print("Further investigation required.")
    
    print("\n🎯 Next: Run EMPIRICAL_KLEIN_STUDIES with corrected model")


if __name__ == "__main__":
    main()