#!/usr/bin/env python3
"""
CALCULADORA DE SIGNIFICANCIA ESTADÍSTICA - KLEIN THEORY GWTC-3
===============================================================

Calcula significancia estadística (sigma) de Klein Theory aplicada a datos reales GWTC-3,
considerando correlaciones múltiples y correcciones estadísticas apropiadas.

Author: Klein Theory Extension Team
Date: July 27, 2025
"""

import numpy as np
import json
import os
from scipy import stats
from scipy.stats import chi2, pearsonr
import matplotlib.pyplot as plt

class KleinSignificanceCalculator:
    """
    Calculadora de significancia estadística para validación Klein Theory.
    """
    
    def __init__(self, results_file="results/gwtc3_klein_analysis.json"):
        self.results_file = results_file
        self.load_results()
    
    def load_results(self):
        """
        Carga resultados del análisis GWTC-3.
        """
        if not os.path.exists(self.results_file):
            raise FileNotFoundError(f"No se encontró archivo de resultados: {self.results_file}")
        
        with open(self.results_file, 'r') as f:
            self.data = json.load(f)
        
        self.n_events = self.data['analysis_metadata']['n_events_total']
        self.correlations = self.data['correlations']
        self.detailed_results = self.data['detailed_results']
        
        print(f"✓ Resultados cargados: {self.n_events} eventos GWTC-3")
    
    def extract_observables(self):
        """
        Extrae observables para análisis estadístico.
        """
        # Extraer métricas Klein
        energies = [r['energy_initial'] for r in self.detailed_results]
        max_epsilons = [r['max_epsilon'] for r in self.detailed_results]
        max_elevations = [r['max_elevation'] for r in self.detailed_results]
        doppler_factors = [r['doppler_factor'] for r in self.detailed_results]
        velocities = [r['peculiar_velocity'] for r in self.detailed_results]
        
        # Extraer observables LIGO
        masses = [r['mass_total'] for r in self.detailed_results]
        redshifts = [r['redshift_obs'] for r in self.detailed_results]
        snrs = [r['snr_obs'] for r in self.detailed_results]
        
        # Estados finales
        states = [r['final_state'] for r in self.detailed_results]
        
        return {
            'klein_observables': {
                'energies': np.array(energies),
                'deformations': np.array(max_epsilons),
                'elevations': np.array(max_elevations),
                'doppler_factors': np.array(doppler_factors),
                'velocities': np.array(velocities),
                'states': states
            },
            'ligo_observables': {
                'masses': np.array(masses),
                'redshifts': np.array(redshifts),
                'snrs': np.array(snrs)
            }
        }
    
    def calculate_chi_squared_statistics(self, obs):
        """
        Calcula estadísticas χ² para diferentes hipótesis.
        """
        klein_obs = obs['klein_observables']
        ligo_obs = obs['ligo_observables']
        
        print("\n📊 ANÁLISIS CHI-CUADRADO")
        print("=" * 50)
        
        chi2_stats = {}
        
        # 1. Hipótesis nula: Klein predictions vs observaciones
        print("\n1. Klein Theory vs Datos LIGO:")
        
        # Test energía-masa (Klein predice E ∝ M)
        predicted_energy = ligo_obs['masses'] * 0.04  # 4% efficiency típica
        chi2_energy = np.sum((klein_obs['energies'] - predicted_energy)**2 / predicted_energy)
        dof_energy = len(klein_obs['energies']) - 1
        p_energy = 1 - chi2.cdf(chi2_energy, dof_energy)
        
        print(f"   Energía-Masa: χ²={chi2_energy:.2f}, dof={dof_energy}, p={p_energy:.2e}")
        chi2_stats['energy_mass'] = {'chi2': chi2_energy, 'dof': dof_energy, 'p_value': p_energy}
        
        # 2. Distribución estados Klein
        state_counts = {}
        for state in klein_obs['states']:
            state_counts[state] = state_counts.get(state, 0) + 1
        
        # Predicción Klein: mayoría relajada para energías bajas
        expected_relajada = len(klein_obs['states']) * 0.7  # 70% esperado relajada
        observed_relajada = state_counts.get('Klein_relajada', 0)
        
        chi2_states = (observed_relajada - expected_relajada)**2 / expected_relajada
        p_states = 1 - chi2.cdf(chi2_states, 1)
        
        print(f"   Estados Klein: χ²={chi2_states:.2f}, dof=1, p={p_states:.2e}")
        print(f"     Esperado relajada: {expected_relajada:.1f}, Observado: {observed_relajada}")
        chi2_stats['states'] = {'chi2': chi2_states, 'dof': 1, 'p_value': p_states}
        
        return chi2_stats
    
    def calculate_correlation_significance(self):
        """
        Calcula significancia de correlaciones con correcciones múltiples.
        """
        print("\n📈 SIGNIFICANCIA CORRELACIONES")
        print("=" * 50)
        
        correlations_data = []
        correlation_names = []
        
        for name, corr_data in self.correlations.items():
            r = corr_data['correlation']
            p = corr_data['p_value']
            
            correlations_data.append((name, r, p))
            correlation_names.append(name)
        
        # Corrección Bonferroni para múltiples tests
        n_tests = len(correlations_data)
        bonferroni_alpha = 0.05 / n_tests
        
        print(f"Número de correlaciones testadas: {n_tests}")
        print(f"Umbral Bonferroni (α={0.05}/{n_tests}): {bonferroni_alpha:.2e}")
        print()
        
        significant_correlations = []
        
        for name, r, p in correlations_data:
            # Convertir p-value a σ (sigmas)
            if p > 0:
                z_score = abs(stats.norm.ppf(p/2))  # Two-tailed
                sigma = z_score
            else:
                sigma = 10.0  # Cap para p muy pequeños
            
            bonferroni_significant = p < bonferroni_alpha
            regular_significant = p < 0.05
            
            print(f"{name:25}: r={r:6.3f}, p={p:.2e}, σ={sigma:.1f}")
            print(f"{'':27} Significativo (α=0.05): {'✓' if regular_significant else '✗'}")
            print(f"{'':27} Significativo (Bonferroni): {'✓' if bonferroni_significant else '✗'}")
            print()
            
            if bonferroni_significant:
                significant_correlations.append((name, r, p, sigma))
        
        return significant_correlations, bonferroni_alpha
    
    def calculate_combined_significance(self, sig_correlations, chi2_stats):
        """
        Calcula significancia combinada del framework Klein.
        """
        print("\n🎯 SIGNIFICANCIA COMBINADA KLEIN THEORY")
        print("=" * 60)
        
        # 1. Combinar p-values usando Fisher's method
        all_p_values = []
        
        # P-values de correlaciones significativas
        for name, r, p, sigma in sig_correlations:
            all_p_values.append(p)
        
        # P-values de tests χ²
        for test_name, stats_data in chi2_stats.items():
            all_p_values.append(stats_data['p_value'])
        
        # Fisher's combined test
        if all_p_values:
            fisher_stat = -2 * np.sum(np.log(np.array(all_p_values) + 1e-100))  # Evitar log(0)
            fisher_dof = 2 * len(all_p_values)
            fisher_p = 1 - chi2.cdf(fisher_stat, fisher_dof)
            
            # Convertir a sigmas
            if fisher_p > 0:
                combined_sigma = abs(stats.norm.ppf(fisher_p/2))
            else:
                combined_sigma = 10.0
        else:
            fisher_stat = 0
            fisher_dof = 0
            fisher_p = 1.0
            combined_sigma = 0
        
        print(f"Fisher's combined test:")
        print(f"  Estadística: {fisher_stat:.2f}")
        print(f"  Grados libertad: {fisher_dof}")
        print(f"  P-value: {fisher_p:.2e}")
        print(f"  Significancia: {combined_sigma:.1f}σ")
        
        # 2. Significancia por categoría
        print(f"\nSignificancia por categoría:")
        
        # Doppler effects (correlaciones más fuertes)
        doppler_correlations = [c for c in sig_correlations if 'doppler' in c[0]]
        if doppler_correlations:
            best_doppler = min(doppler_correlations, key=lambda x: x[2])  # Menor p-value
            print(f"  Efectos Doppler: {best_doppler[3]:.1f}σ ({best_doppler[0]})")
        
        # Energy scaling
        energy_correlations = [c for c in sig_correlations if 'energy' in c[0]]
        if energy_correlations:
            best_energy = min(energy_correlations, key=lambda x: x[2])
            print(f"  Escalado energético: {best_energy[3]:.1f}σ ({best_energy[0]})")
        
        # 3. Assessment final
        print(f"\n🏆 ASSESSMENT FINAL:")
        print(f"   Eventos analizados: {self.n_events}")
        print(f"   Correlaciones significativas: {len(sig_correlations)}")
        print(f"   Significancia combinada: {combined_sigma:.1f}σ")
        
        if combined_sigma >= 5.0:
            assessment = "🎉 DESCOBRIMIENTO (≥5σ)"
        elif combined_sigma >= 3.0:
            assessment = "✨ EVIDENCIA FUERTE (≥3σ)"
        elif combined_sigma >= 2.0:
            assessment = "⭐ EVIDENCIA MARGINAL (≥2σ)"
        else:
            assessment = "📝 NO SIGNIFICATIVO (<2σ)"
        
        print(f"   {assessment}")
        
        return {
            'combined_sigma': combined_sigma,
            'fisher_p': fisher_p,
            'n_significant_correlations': len(sig_correlations),
            'assessment': assessment
        }
    
    def create_significance_plot(self, sig_correlations, combined_stats):
        """
        Crea plot de significancias.
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        # Plot 1: Correlaciones significativas
        if sig_correlations:
            names = [c[0].replace('_', ' ').title() for c in sig_correlations]
            sigmas = [c[3] for c in sig_correlations]
            colors = ['red' if s >= 5 else 'orange' if s >= 3 else 'blue' for s in sigmas]
            
            bars = ax1.barh(names, sigmas, color=colors, alpha=0.7)
            ax1.axvline(x=3, color='orange', linestyle='--', alpha=0.8, label='3σ evidencia')
            ax1.axvline(x=5, color='red', linestyle='--', alpha=0.8, label='5σ descobrimiento')
            ax1.set_xlabel('Significancia (σ)')
            ax1.set_title('Significancia por Correlación')
            ax1.legend()
            ax1.grid(True, alpha=0.3)
            
            # Añadir valores en barras
            for bar, sigma in zip(bars, sigmas):
                width = bar.get_width()
                ax1.text(width + 0.1, bar.get_y() + bar.get_height()/2, 
                        f'{sigma:.1f}σ', ha='left', va='center')
        
        # Plot 2: Distribución p-values
        all_p_values = [c[2] for c in sig_correlations]
        if all_p_values:
            ax2.hist(np.log10(all_p_values), bins=10, alpha=0.7, color='skyblue', edgecolor='black')
            ax2.axvline(x=np.log10(0.05), color='orange', linestyle='--', label='α=0.05')
            ax2.axvline(x=np.log10(0.001), color='red', linestyle='--', label='α=0.001')
            ax2.set_xlabel('log₁₀(p-value)')
            ax2.set_ylabel('Frecuencia')
            ax2.set_title('Distribución P-values')
            ax2.legend()
            ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # Guardar
        plot_path = "results/klein_significance_analysis.png"
        plt.savefig(plot_path, dpi=300, bbox_inches='tight')
        print(f"\n✅ Plot significancia guardado: {plot_path}")
        plt.show()
        
        return plot_path

def main():
    """
    Ejecuta análisis completo de significancia.
    """
    print("📊 ANÁLISIS DE SIGNIFICANCIA ESTADÍSTICA - KLEIN THEORY")
    print("=" * 70)
    
    try:
        # Inicializar calculadora
        calc = KleinSignificanceCalculator()
        
        # Extraer observables
        observables = calc.extract_observables()
        
        # Tests χ²
        chi2_stats = calc.calculate_chi_squared_statistics(observables)
        
        # Significancia correlaciones
        sig_correlations, bonferroni_alpha = calc.calculate_correlation_significance()
        
        # Significancia combinada
        combined_stats = calc.calculate_combined_significance(sig_correlations, chi2_stats)
        
        # Crear plots
        plot_path = calc.create_significance_plot(sig_correlations, combined_stats)
        
        # Guardar reporte
        report = {
            'summary': combined_stats,
            'significant_correlations': sig_correlations,
            'chi2_tests': chi2_stats,
            'bonferroni_correction': bonferroni_alpha,
            'n_events': calc.n_events
        }
        
        report_path = "results/klein_significance_report.json"
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        print(f"\n💾 Reporte guardado: {report_path}")
        
        return combined_stats['combined_sigma']
        
    except Exception as e:
        print(f"❌ Error en análisis de significancia: {e}")
        return 0

if __name__ == "__main__":
    final_sigma = main()
    print(f"\n🎯 SIGNIFICANCIA FINAL KLEIN THEORY: {final_sigma:.1f}σ")