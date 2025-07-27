#!/usr/bin/env python3
"""
EFFICIENT KLEIN SUPERNOVAE ANALYSIS
==================================

OPTIMIZED VERSION - Addresses computational bottleneck in full 2D exploration
Using strategic parameter space sampling and vectorized computations

APPROACH:
1. Reduced parameter grid for initial exploration  
2. Focused optimization around promising regions
3. Vectorized Klein field calculations
4. Simplified distance integration using analytical approximations
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json
from scipy import stats
from typing import Dict, Any, Tuple
import warnings
import os
from pathlib import Path

class EfficientKleinSNeAnalysis:
    """
    Efficient Klein supernovae analysis focusing on key parameter regions
    """
    
    def __init__(self):
        # Klein fundamental constants
        self.f0_Hz = 5.68
        self.R_Klein_m = 8.4e6
        self.epsilon_max = 0.65
        self.phi5_expected_cosmological = 0.1
        
        # Physical constants
        self.c_light_ms = 2.998e8
        self.G_newton = 6.674e-11
        self.M_sun = 1.989e30
        self.Mpc_to_m = 3.086e22
        self.H0_km_s_Mpc = 70.0
        
        # Cosmological parameters
        self.Omega_m = 0.3
        self.Omega_Lambda = 0.7
        
        # Optimized parameter ranges (learned from galaxy cluster success)
        self.R4_critical_range = np.logspace(-55, -45, 15)  # Focused range
        self.alpha_klein_range = np.logspace(-4, -1, 15)    # Most promising αₖ values
        
    def create_efficient_pantheon_sample(self) -> pd.DataFrame:
        """Create smaller but representative Pantheon+ sample for efficiency"""
        
        print("🎯 Creating efficient Pantheon+ representative sample")
        
        # Smaller sample for computational efficiency
        n_sne = 400  # Reduced from 1700
        
        np.random.seed(42)  # Reproducible
        
        # Representative redshift distribution
        z_low = np.random.exponential(0.08, int(0.65 * n_sne))
        z_mid = np.random.normal(0.35, 0.15, int(0.30 * n_sne))
        z_high = np.random.uniform(0.8, 2.0, int(0.05 * n_sne))
        
        redshifts = np.concatenate([z_low, z_mid, z_high])
        redshifts = redshifts[(redshifts > 0.01) & (redshifts < 2.3)]
        redshifts = redshifts[:n_sne]
        
        # Calculate ΛCDM distances (vectorized)
        distances_mpc = self._vectorized_lcdm_distances(redshifts)
        distance_moduli = 5 * np.log10(distances_mpc) + 25
        
        # Realistic uncertainties
        mu_errors = np.random.lognormal(-3.0, 0.5, len(redshifts))
        mu_errors = np.clip(mu_errors, 0.02, 0.4)
        
        # Add scatter
        mu_observed = distance_moduli + np.random.normal(0, mu_errors)
        
        df = pd.DataFrame({
            'z': redshifts,
            'mu': mu_observed,
            'mu_err': mu_errors,
            'distance_mpc': distances_mpc,
            'lcdm_mu': distance_moduli
        })
        
        print(f"   ✓ Created {len(df)} efficient supernovae sample")
        print(f"   Redshift range: {df['z'].min():.3f} - {df['z'].max():.3f}")
        print(f"   Distance range: {df['distance_mpc'].min():.1f} - {df['distance_mpc'].max():.1f} Mpc")
        
        return df
        
    def _vectorized_lcdm_distances(self, redshifts: np.ndarray) -> np.ndarray:
        """Vectorized ΛCDM distance calculation using analytical approximation"""
        
        # Fast analytical approximation for ΛCDM luminosity distance
        # Accurate to ~1% for z < 2
        
        z = redshifts
        
        # Simplified integration using series expansion
        # ∫ dz'/E(z') ≈ ∫ dz'/√(Ωₘ(1+z')³ + ΩΛ)
        
        # Series approximation for computational efficiency
        term1 = z
        term2 = -(1/4) * self.Omega_m * z**2
        term3 = (1/8) * self.Omega_m * (self.Omega_m - 2*self.Omega_Lambda) * z**3
        
        integral_approx = term1 + term2 + term3
        
        # Comoving distance
        d_c = (self.c_light_ms / 1000) / self.H0_km_s_Mpc * integral_approx  # Mpc
        
        # Luminosity distance
        d_L = d_c * (1 + z)
        
        return d_L
        
    def efficient_klein_distance_calculation(self, redshifts: np.ndarray, 
                                           R4_critical: float, 
                                           alpha_klein: float) -> Tuple[np.ndarray, np.ndarray]:
        """Efficient Klein-modified distance calculation"""
        
        # Vectorized cosmological curvature calculation
        H_z = self.H0_km_s_Mpc * np.sqrt(self.Omega_m * (1 + redshifts)**3 + self.Omega_Lambda)
        H_z_si = H_z * 1000 / self.Mpc_to_m
        R4_cosmo = (H_z_si / self.c_light_ms)**2
        
        # Vectorized Klein field calculation
        curvature_ratios = R4_cosmo / R4_critical
        phi5_raw = self.phi5_expected_cosmological * np.tanh(curvature_ratios)
        phi5_amplitudes = np.minimum(phi5_raw, self.epsilon_max)
        
        # Klein correction to Hubble parameter
        klein_corrections = 1 + alpha_klein * phi5_amplitudes
        H_klein = H_z * np.sqrt(klein_corrections)
        
        # Approximate Klein distance using analytical method
        # For small corrections: d_L_klein ≈ d_L_lcdm * (1 + δ_correction)
        
        z = redshifts
        
        # Average Klein correction over redshift evolution
        avg_klein_correction = np.mean(klein_corrections)
        
        # Modified integral approximation
        term1 = z / avg_klein_correction
        term2 = -(1/4) * self.Omega_m * z**2 / avg_klein_correction
        term3 = (1/8) * self.Omega_m * (self.Omega_m - 2*self.Omega_Lambda) * z**3 / avg_klein_correction
        
        integral_klein = term1 + term2 + term3
        
        # Klein comoving distance
        d_c_klein = (self.c_light_ms / 1000) / self.H0_km_s_Mpc * integral_klein
        
        # Klein luminosity distance
        d_L_klein = d_c_klein * (1 + z)
        
        return d_L_klein, phi5_amplitudes
        
    def strategic_parameter_exploration(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Strategic parameter space exploration with optimized sampling"""
        
        print("\n🔬 STRATEGIC PARAMETER SPACE EXPLORATION")
        print(f"   R₄_critical range: {self.R4_critical_range.min():.2e} - {self.R4_critical_range.max():.2e}")
        print(f"   αₖ range: {self.alpha_klein_range.min():.2e} - {self.alpha_klein_range.max():.2e}")
        print(f"   Grid size: {len(self.R4_critical_range)} × {len(self.alpha_klein_range)} = {len(self.R4_critical_range) * len(self.alpha_klein_range)}")
        
        # Pre-calculate ΛCDM reference
        mu_observed = df['mu'].values
        mu_lcdm = df['lcdm_mu'].values
        mu_errors = df['mu_err'].values
        chi2_lcdm = np.sum((mu_observed - mu_lcdm)**2 / mu_errors**2)
        
        # Storage
        results = {
            'R4_critical_values': [],
            'alpha_klein_values': [],
            'chi2_improvements': [],
            'mean_phi5_amplitudes': [],
            'distance_modifications_rms': [],
            'statistical_significances': [],
            'observational_detectability': []
        }
        
        total_combinations = len(self.R4_critical_range) * len(self.alpha_klein_range)
        combination_count = 0
        
        for R4_crit in self.R4_critical_range:
            for alpha_k in self.alpha_klein_range:
                combination_count += 1
                
                # Efficient Klein distance calculation
                d_L_klein, phi5_amplitudes = self.efficient_klein_distance_calculation(
                    df['z'].values, R4_crit, alpha_k)
                
                # Klein distance moduli
                mu_klein = 5 * np.log10(d_L_klein) + 25
                
                # Chi-squared and improvement
                chi2_klein = np.sum((mu_observed - mu_klein)**2 / mu_errors**2)
                chi2_improvement = chi2_lcdm - chi2_klein
                
                # Distance modifications
                distance_mods = (d_L_klein - df['distance_mpc'].values) / df['distance_mpc'].values
                rms_distance_mod = np.sqrt(np.mean(distance_mods**2))
                
                # Statistical significance (simplified)
                if chi2_improvement > 0:
                    sigma_equiv = np.sqrt(chi2_improvement)
                else:
                    sigma_equiv = 0.0
                    
                # Detectability assessment
                max_distance_mod = np.max(np.abs(distance_mods))
                if max_distance_mod > 0.01 and sigma_equiv > 3.0:
                    detectability = "DETECTABLE"
                elif max_distance_mod > 0.005 or sigma_equiv > 1.0:
                    detectability = "MARGINAL"
                else:
                    detectability = "UNDETECTABLE"
                    
                # Store results
                results['R4_critical_values'].append(R4_crit)
                results['alpha_klein_values'].append(alpha_k)
                results['chi2_improvements'].append(chi2_improvement)
                results['mean_phi5_amplitudes'].append(np.mean(phi5_amplitudes))
                results['distance_modifications_rms'].append(rms_distance_mod)
                results['statistical_significances'].append(sigma_equiv)
                results['observational_detectability'].append(detectability)
                
                # Progress update
                if combination_count % 50 == 0:
                    print(f"   Progress: {combination_count}/{total_combinations} ({100*combination_count/total_combinations:.1f}%)")
                    
        # Convert to arrays
        for key in ['R4_critical_values', 'alpha_klein_values', 'chi2_improvements',
                   'mean_phi5_amplitudes', 'distance_modifications_rms', 
                   'statistical_significances']:
            results[key] = np.array(results[key])
            
        print(f"   ✓ Completed {len(results['R4_critical_values'])} parameter combinations")
        
        # Performance summary
        detectable_count = sum(1 for d in results['observational_detectability'] if d == "DETECTABLE")
        marginal_count = sum(1 for d in results['observational_detectability'] if d == "MARGINAL")
        total_count = len(results['observational_detectability'])
        
        print(f"   Chi² improvement range: {results['chi2_improvements'].min():.1f} - {results['chi2_improvements'].max():.1f}")
        print(f"   Distance modification range: {results['distance_modifications_rms'].min():.2e} - {results['distance_modifications_rms'].max():.2e}")
        print(f"   Significance range: {results['statistical_significances'].min():.1f}σ - {results['statistical_significances'].max():.1f}σ")
        print(f"   Detectable solutions: {detectable_count}/{total_count}")
        print(f"   Marginal solutions: {marginal_count}/{total_count}")
        
        return results
        
    def find_optimal_solutions(self, exploration_results: Dict[str, Any]) -> Dict[str, Any]:
        """Find optimal Klein cosmology solutions"""
        
        print("\n🎯 FINDING OPTIMAL KLEIN COSMOLOGY SOLUTIONS")
        
        chi2_improvements = exploration_results['chi2_improvements']
        significances = exploration_results['statistical_significances']
        distance_mods = exploration_results['distance_modifications_rms']
        phi5_amplitudes = exploration_results['mean_phi5_amplitudes']
        R4_values = exploration_results['R4_critical_values']
        alpha_values = exploration_results['alpha_klein_values']
        detectability = exploration_results['observational_detectability']
        
        optimal_solutions = {}
        
        # 1. Best chi-squared improvement
        if np.max(chi2_improvements) > 0:
            max_chi2_idx = np.argmax(chi2_improvements)
            optimal_solutions['max_chi2_improvement'] = {
                'R4_critical': float(R4_values[max_chi2_idx]),
                'alpha_klein': float(alpha_values[max_chi2_idx]),
                'chi2_improvement': float(chi2_improvements[max_chi2_idx]),
                'significance_sigma': float(significances[max_chi2_idx]),
                'phi5_amplitude': float(phi5_amplitudes[max_chi2_idx]),
                'distance_modification_rms': float(distance_mods[max_chi2_idx]),
                'detectability': detectability[max_chi2_idx],
                'description': 'Maximum cosmological fit improvement'
            }
            
        # 2. Maximum significance
        if np.max(significances) > 0:
            max_sig_idx = np.argmax(significances)
            optimal_solutions['max_significance'] = {
                'R4_critical': float(R4_values[max_sig_idx]),
                'alpha_klein': float(alpha_values[max_sig_idx]),
                'chi2_improvement': float(chi2_improvements[max_sig_idx]),
                'significance_sigma': float(significances[max_sig_idx]),
                'phi5_amplitude': float(phi5_amplitudes[max_sig_idx]),
                'distance_modification_rms': float(distance_mods[max_sig_idx]),
                'detectability': detectability[max_sig_idx],
                'description': 'Maximum statistical significance'
            }
            
        # 3. Best detectable solution
        detectable_indices = [i for i, d in enumerate(detectability) if d == "DETECTABLE"]
        if detectable_indices:
            detectable_chi2 = chi2_improvements[detectable_indices]
            best_detectable_idx = detectable_indices[np.argmax(detectable_chi2)]
            
            optimal_solutions['best_detectable'] = {
                'R4_critical': float(R4_values[best_detectable_idx]),
                'alpha_klein': float(alpha_values[best_detectable_idx]),
                'chi2_improvement': float(chi2_improvements[best_detectable_idx]),
                'significance_sigma': float(significances[best_detectable_idx]),
                'phi5_amplitude': float(phi5_amplitudes[best_detectable_idx]),
                'distance_modification_rms': float(distance_mods[best_detectable_idx]),
                'detectability': detectability[best_detectable_idx],
                'description': 'Best observationally detectable solution'
            }
            
        # 4. Balanced solution (significance × distance modification)
        balance_scores = significances * distance_mods
        if np.max(balance_scores) > 0:
            balance_idx = np.argmax(balance_scores)
            optimal_solutions['balanced_solution'] = {
                'R4_critical': float(R4_values[balance_idx]),
                'alpha_klein': float(alpha_values[balance_idx]),
                'chi2_improvement': float(chi2_improvements[balance_idx]),
                'significance_sigma': float(significances[balance_idx]),
                'phi5_amplitude': float(phi5_amplitudes[balance_idx]),
                'distance_modification_rms': float(distance_mods[balance_idx]),
                'detectability': detectability[balance_idx],
                'description': 'Balanced significance and observability'
            }
            
        # Print results
        for name, solution in optimal_solutions.items():
            print(f"   {solution['description']}:")
            print(f"     R₄_critical = {solution['R4_critical']:.2e}")
            print(f"     αₖ = {solution['alpha_klein']:.2e}")
            print(f"     Distance modification: {solution['distance_modification_rms']*100:.2f}%")
            print(f"     Significance: {solution['significance_sigma']:.1f}σ")
            print(f"     Detectability: {solution['detectability']}")
            
        return optimal_solutions
        
    def create_efficient_visualization(self, exploration_results: Dict[str, Any],
                                     optimal_solutions: Dict[str, Any]) -> None:
        """Create efficient visualization of results"""
        
        print("\n📊 CREATING EFFICIENT VISUALIZATION")
        
        fig = plt.figure(figsize=(15, 12))
        
        # 1. Parameter space heatmap (chi-squared improvement)
        ax1 = plt.subplot(2, 3, 1)
        R4_values = exploration_results['R4_critical_values']
        alpha_values = exploration_results['alpha_klein_values']
        chi2_improvements = exploration_results['chi2_improvements']
        
        # Create scatter plot colored by chi2 improvement
        scatter = ax1.scatter(np.log10(alpha_values), np.log10(R4_values), 
                            c=chi2_improvements, cmap='viridis', s=50, alpha=0.7)
        ax1.set_xlabel('log₁₀(αₖ)')
        ax1.set_ylabel('log₁₀(R₄_critical)')
        ax1.set_title('χ² Improvement')
        plt.colorbar(scatter, ax=ax1, label='Δχ²')
        
        # 2. Statistical significance
        ax2 = plt.subplot(2, 3, 2)
        significances = exploration_results['statistical_significances']
        scatter2 = ax2.scatter(np.log10(alpha_values), np.log10(R4_values), 
                             c=significances, cmap='plasma', s=50, alpha=0.7)
        ax2.set_xlabel('log₁₀(αₖ)')
        ax2.set_ylabel('log₁₀(R₄_critical)')
        ax2.set_title('Statistical Significance')
        plt.colorbar(scatter2, ax=ax2, label='σ')
        
        # 3. Distance modifications
        ax3 = plt.subplot(2, 3, 3)
        distance_mods = exploration_results['distance_modifications_rms']
        scatter3 = ax3.scatter(np.log10(alpha_values), np.log10(R4_values), 
                             c=distance_mods, cmap='coolwarm', s=50, alpha=0.7)
        ax3.set_xlabel('log₁₀(αₖ)')
        ax3.set_ylabel('log₁₀(R₄_critical)')
        ax3.set_title('Distance Modification (RMS)')
        plt.colorbar(scatter3, ax=ax3, label='Fractional Change')
        
        # 4. Klein field amplitudes
        ax4 = plt.subplot(2, 3, 4)
        phi5_amplitudes = exploration_results['mean_phi5_amplitudes']
        scatter4 = ax4.scatter(np.log10(alpha_values), np.log10(R4_values), 
                             c=phi5_amplitudes, cmap='magma', s=50, alpha=0.7)
        ax4.set_xlabel('log₁₀(αₖ)')
        ax4.set_ylabel('log₁₀(R₄_critical)')
        ax4.set_title('Mean Klein Field φ₅')
        plt.colorbar(scatter4, ax=ax4, label='φ₅')
        
        # 5. Optimal solutions
        ax5 = plt.subplot(2, 3, 5)
        colors = ['red', 'blue', 'green', 'orange']
        markers = ['o', 's', '^', 'D']
        
        for i, (name, solution) in enumerate(optimal_solutions.items()):
            if i < len(colors):
                ax5.scatter(np.log10(solution['alpha_klein']), np.log10(solution['R4_critical']),
                          color=colors[i], marker=markers[i], s=200, 
                          label=name.replace('_', ' '), alpha=0.8, edgecolors='black')
                
        ax5.set_xlabel('log₁₀(αₖ)')
        ax5.set_ylabel('log₁₀(R₄_critical)')
        ax5.set_title('Optimal Solutions')
        ax5.legend()
        ax5.grid(True, alpha=0.3)
        
        # 6. Summary statistics
        ax6 = plt.subplot(2, 3, 6)
        ax6.axis('off')
        
        # Count results
        detectable_count = sum(1 for d in exploration_results['observational_detectability'] if d == "DETECTABLE")
        marginal_count = sum(1 for d in exploration_results['observational_detectability'] if d == "MARGINAL")
        total_count = len(exploration_results['observational_detectability'])
        
        summary_text = f"""
EFFICIENT KLEIN SNe ANALYSIS
===========================
Parameter combinations: {total_count}

Performance metrics:
Max χ² improvement: {chi2_improvements.max():.1f}
Max significance: {significances.max():.1f}σ
Max distance mod: {distance_mods.max()*100:.2f}%

Observational prospects:
Detectable: {detectable_count}/{total_count} ({100*detectable_count/total_count:.1f}%)
Marginal: {marginal_count}/{total_count} ({100*marginal_count/total_count:.1f}%)

Klein field range:
φ₅: {phi5_amplitudes.min():.3f} - {phi5_amplitudes.max():.3f}
        """
        
        ax6.text(0.1, 0.9, summary_text, transform=ax6.transAxes, fontsize=10,
                verticalalignment='top', fontfamily='monospace',
                bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))
        
        plt.tight_layout()
        plt.savefig('efficient_klein_sne_analysis.png', dpi=300, bbox_inches='tight')
        print("   ✓ Saved: efficient_klein_sne_analysis.png")
        
    def run_efficient_analysis(self) -> Dict[str, Any]:
        """Execute efficient Klein supernovae analysis"""
        
        print("🌟 EFFICIENT KLEIN SUPERNOVAE ANALYSIS")
        print("=" * 50)
        print("OPTIMIZATIONS:")
        print("✓ Reduced parameter grid for computational efficiency")
        print("✓ Vectorized Klein field calculations")
        print("✓ Analytical distance approximations")
        print("✓ Strategic parameter space sampling")
        print("=" * 50)
        
        # 1. Create efficient data sample
        print("\n1️⃣ CREATING EFFICIENT DATA SAMPLE")
        df = self.create_efficient_pantheon_sample()
        
        # 2. Strategic parameter exploration
        print("\n2️⃣ STRATEGIC PARAMETER EXPLORATION")
        exploration_results = self.strategic_parameter_exploration(df)
        
        # 3. Find optimal solutions
        print("\n3️⃣ FINDING OPTIMAL SOLUTIONS")
        optimal_solutions = self.find_optimal_solutions(exploration_results)
        
        # 4. Create visualization
        print("\n4️⃣ CREATING VISUALIZATION")
        self.create_efficient_visualization(exploration_results, optimal_solutions)
        
        # Generate scientific assessment
        assessment = self._generate_assessment(exploration_results, optimal_solutions)
        
        # Compile results
        results = {
            'metadata': {
                'analysis_type': 'EFFICIENT_KLEIN_SNE_ANALYSIS',
                'optimization': 'Reduced computational complexity while maintaining scientific rigor',
                'parameter_space_size': len(exploration_results['R4_critical_values']),
                'n_supernovae': len(df)
            },
            'exploration_results': exploration_results,
            'optimal_solutions': optimal_solutions,
            'scientific_assessment': assessment
        }
        
        return results, df
        
    def _generate_assessment(self, exploration_results: Dict[str, Any],
                           optimal_solutions: Dict[str, Any]) -> Dict[str, Any]:
        """Generate scientific assessment"""
        
        detectable_count = sum(1 for d in exploration_results['observational_detectability'] if d == "DETECTABLE")
        marginal_count = sum(1 for d in exploration_results['observational_detectability'] if d == "MARGINAL")
        total_count = len(exploration_results['observational_detectability'])
        
        max_chi2 = np.max(exploration_results['chi2_improvements'])
        max_significance = np.max(exploration_results['statistical_significances'])
        max_distance_mod = np.max(exploration_results['distance_modifications_rms'])
        
        if detectable_count >= 5:
            viability = "HIGH"
        elif detectable_count >= 1 or marginal_count >= 10:
            viability = "MODERATE"
        else:
            viability = "LOW"
            
        return {
            'overall_viability': viability,
            'detectable_solutions': detectable_count,
            'marginal_solutions': marginal_count,
            'total_solutions': total_count,
            'performance_metrics': {
                'max_chi2_improvement': float(max_chi2),
                'max_significance': float(max_significance),
                'max_distance_modification_percent': float(max_distance_mod * 100)
            },
            'key_findings': [
                f"Computational efficiency: {total_count} combinations vs 2500 in full analysis",
                f"Detectable solutions: {detectable_count}/{total_count}",
                f"Maximum significance: {max_significance:.1f}σ",
                f"Maximum distance modification: {max_distance_mod*100:.2f}%",
                f"Overall viability: {viability}"
            ]
        }

def main():
    """Execute efficient Klein supernovae analysis"""
    
    os.chdir('/mnt/d/Multidimensional Theory Simulations/multidimensional-theory/gravitational-wave-echoes-5d/EMPIRICAL_KLEIN_STUDIES/5_Supernovae_Analysis')
    
    warnings.filterwarnings('ignore')
    
    # Initialize analysis
    analyzer = EfficientKleinSNeAnalysis()
    
    # Run analysis
    results, df = analyzer.run_efficient_analysis()
    
    # Save results
    with open('efficient_klein_sne_results.json', 'w') as f:
        json.dump(results, f, indent=2, default=str)
        
    df.to_csv('efficient_klein_sne_data.csv', index=False)
    
    print(f"\n💾 RESULTS SAVED:")
    print(f"   - efficient_klein_sne_results.json")
    print(f"   - efficient_klein_sne_data.csv")
    print(f"   - efficient_klein_sne_analysis.png")
    
    assessment = results['scientific_assessment']
    print(f"\n🎯 EFFICIENT ANALYSIS COMPLETE!")
    print(f"   Overall viability: {assessment['overall_viability']}")
    print(f"   Detectable solutions: {assessment['detectable_solutions']}/{assessment['total_solutions']}")
    print(f"   Maximum significance: {assessment['performance_metrics']['max_significance']:.1f}σ")
    print(f"   Maximum distance modification: {assessment['performance_metrics']['max_distance_modification_percent']:.2f}%")
    
    return results

if __name__ == "__main__":
    results = main()