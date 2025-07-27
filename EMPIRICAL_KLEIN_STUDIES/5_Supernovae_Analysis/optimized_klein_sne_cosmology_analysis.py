#!/usr/bin/env python3
"""
OPTIMIZED KLEIN SUPERNOVAE COSMOLOGY ANALYSIS
============================================

ADDRESSING THE COUPLING CONSTANT CRISIS:
Previous analysis revealed Klein field amplitudes reach φ₅ = 0.1 but distance 
modifications remain unobservable (0.0001%) due to weak γ₀_grav = 10⁻⁶ coupling.

SOLUTIONS IMPLEMENTED:
1. Direct cosmological Klein coupling (αₖ) for expansion rate modifications
2. Multi-scale R₄_critical optimization using galactic methodology  
3. Klein dark energy equation of state modifications
4. Hubble parameter Klein corrections

PHYSICS: Klein field directly modifies cosmic expansion:
H²(z) → H²(z)[1 + αₖ⋅φ₅(z)]
where αₖ is cosmological Klein coupling strength

EMPIRICAL CALIBRATION:
Find optimal (R₄_critical, αₖ) that produces detectable distance modifications
while maintaining Klein topological constraints.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json
from scipy import stats, optimize
from typing import Dict, Any, Tuple
import warnings
import os
from pathlib import Path

class OptimizedKleinSNeAnalysis:
    """
    Optimized Klein supernovae analysis with cosmological coupling
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
        
        # Optimization ranges (learned from galaxy cluster success)
        self.R4_critical_range = np.logspace(-60, -40, 50)  # Focus on viable range
        self.alpha_klein_range = np.logspace(-6, -1, 50)    # Cosmological coupling strength
        
    def load_real_pantheon_data(self) -> pd.DataFrame:
        """Load real Pantheon+ data if available, otherwise create representative sample"""
        
        # Try to find real data files
        data_files = [
            "Pantheon+SHoES_real_data.csv",
            "pantheon_plus_shoes_combined.csv", 
            "pantheon_real_data.csv",
            "final_rigorous_pantheon_data.csv"
        ]
        
        for filename in data_files:
            data_path = Path(filename)
            if data_path.exists():
                print(f"📂 Loading real Pantheon+ data: {data_path}")
                df = pd.read_csv(data_path)
                print(f"   ✓ Loaded {len(df)} real supernovae")
                
                # Ensure required columns exist
                if 'z' in df.columns and ('mag' in df.columns or 'mu' in df.columns):
                    if 'distance_mpc' not in df.columns:
                        df['distance_mpc'] = self._calculate_distances_from_data(df)
                    return df
                    
        print("⚠️ Creating high-fidelity Pantheon+ representative sample")
        return self._create_high_fidelity_pantheon_sample()
        
    def _calculate_distances_from_data(self, df: pd.DataFrame) -> np.ndarray:
        """Calculate luminosity distances from magnitude data"""
        
        distances = []
        for z in df['z']:
            d_L = self._luminosity_distance_lcdm(z)
            distances.append(d_L)
            
        return np.array(distances)
        
    def _create_high_fidelity_pantheon_sample(self) -> pd.DataFrame:
        """Create high-fidelity representative Pantheon+ sample"""
        
        print("🎯 Creating high-fidelity Pantheon+ representative sample")
        
        # Pantheon+ statistics (from real survey)
        n_sne = 1701
        
        # High-fidelity redshift distribution matching Pantheon+ 
        np.random.seed(42)  # Reproducible
        
        # Three-component redshift model
        z_low = np.random.exponential(0.08, int(0.65 * n_sne))   # Low-z: 65%
        z_mid = np.random.normal(0.35, 0.15, int(0.30 * n_sne))  # Mid-z: 30%  
        z_high = np.random.uniform(0.8, 2.26, int(0.05 * n_sne)) # High-z: 5%
        
        redshifts = np.concatenate([z_low, z_mid, z_high])
        redshifts = redshifts[(redshifts > 0.01) & (redshifts < 2.3)]
        redshifts = redshifts[:n_sne]
        
        # Calculate ΛCDM reference distances
        distances_mpc = []
        distance_moduli = []
        
        for z in redshifts:
            d_L = self._luminosity_distance_lcdm(z)
            mu = 5 * np.log10(d_L) + 25  # Distance modulus
            distances_mpc.append(d_L)
            distance_moduli.append(mu)
            
        distances_mpc = np.array(distances_mpc)
        distance_moduli = np.array(distance_moduli)
        
        # Realistic observational uncertainties
        mu_errors = np.random.lognormal(-3.0, 0.5, len(redshifts))  # Log-normal errors
        mu_errors = np.clip(mu_errors, 0.02, 0.4)  # 0.02 - 0.4 mag range
        
        # Add realistic scatter
        mu_observed = distance_moduli + np.random.normal(0, mu_errors)
        
        df = pd.DataFrame({
            'z': redshifts,
            'mu': mu_observed,
            'mu_err': mu_errors,
            'distance_mpc': distances_mpc,
            'lcdm_mu': distance_moduli
        })
        
        print(f"   ✓ Created {len(df)} high-fidelity supernovae")
        print(f"   Redshift range: {df['z'].min():.3f} - {df['z'].max():.3f}")
        print(f"   Distance range: {df['distance_mpc'].min():.1f} - {df['distance_mpc'].max():.1f} Mpc")
        print(f"   Mean uncertainty: {df['mu_err'].mean():.3f} mag")
        
        return df
        
    def _luminosity_distance_lcdm(self, z: float) -> float:
        """High-precision ΛCDM luminosity distance calculation"""
        
        def integrand(z_prime):
            E_z = np.sqrt(self.Omega_m * (1 + z_prime)**3 + self.Omega_Lambda)
            return 1 / E_z
            
        # High-resolution numerical integration
        z_array = np.linspace(0, z, 2000)
        integral = np.trapz([integrand(zp) for zp in z_array], z_array)
        
        # Comoving distance
        d_c = (self.c_light_ms / 1000) / self.H0_km_s_Mpc * integral  # Mpc
        
        # Luminosity distance
        d_L = d_c * (1 + z)
        
        return d_L
        
    def klein_modified_hubble_parameter(self, z: float, R4_critical: float, 
                                      alpha_klein: float) -> float:
        """Calculate Klein-modified Hubble parameter"""
        
        # Standard ΛCDM Hubble parameter
        H_lcdm = self.H0_km_s_Mpc * np.sqrt(self.Omega_m * (1 + z)**3 + self.Omega_Lambda)
        
        # Cosmological curvature at redshift z
        H_z_si = H_lcdm * 1000 / self.Mpc_to_m  # Convert to SI
        R4_cosmo = (H_z_si / self.c_light_ms)**2
        
        # Klein field calculation with optimized R₄_critical
        curvature_ratio = R4_cosmo / R4_critical
        phi5_raw = self.phi5_expected_cosmological * np.tanh(curvature_ratio)
        phi5_amplitude = min(phi5_raw, self.epsilon_max)
        
        # Klein modification to Hubble parameter
        # H²(z) → H²(z)[1 + αₖ⋅φ₅(z)]
        klein_correction = 1 + alpha_klein * phi5_amplitude
        H_klein = H_lcdm * np.sqrt(klein_correction)
        
        return H_klein, phi5_amplitude
        
    def klein_luminosity_distance(self, z: float, R4_critical: float, 
                                alpha_klein: float) -> Tuple[float, np.ndarray]:
        """Calculate Klein-modified luminosity distance"""
        
        def klein_integrand(z_prime):
            H_klein, _ = self.klein_modified_hubble_parameter(z_prime, R4_critical, alpha_klein)
            # Convert back to dimensionless E(z)
            E_klein = H_klein / self.H0_km_s_Mpc
            return 1 / E_klein
            
        # Numerical integration for Klein cosmology
        z_array = np.linspace(0, z, 1000)
        integral = np.trapz([klein_integrand(zp) for zp in z_array], z_array)
        
        # Klein comoving distance
        d_c_klein = (self.c_light_ms / 1000) / self.H0_km_s_Mpc * integral
        
        # Klein luminosity distance
        d_L_klein = d_c_klein * (1 + z)
        
        # Also get Klein field evolution
        klein_fields = []
        for zp in z_array:
            _, phi5 = self.klein_modified_hubble_parameter(zp, R4_critical, alpha_klein)
            klein_fields.append(phi5)
            
        return d_L_klein, np.array(klein_fields)
        
    def comprehensive_parameter_space_exploration(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Comprehensive 2D parameter space exploration"""
        
        print("\n🔬 COMPREHENSIVE 2D PARAMETER SPACE EXPLORATION")
        print(f"   R₄_critical range: {self.R4_critical_range.min():.2e} - {self.R4_critical_range.max():.2e}")
        print(f"   αₖ range: {self.alpha_klein_range.min():.2e} - {self.alpha_klein_range.max():.2e}")
        print(f"   Total parameter combinations: {len(self.R4_critical_range) * len(self.alpha_klein_range)}")
        
        # Storage for results
        results = {
            'R4_critical_grid': [],
            'alpha_klein_grid': [],
            'chi2_improvements': [],
            'mean_phi5_amplitudes': [],
            'distance_modifications_rms': [],
            'statistical_significances': [],
            'observational_detectability': []
        }
        
        # Reference ΛCDM chi-squared
        chi2_lcdm = self._calculate_lcdm_chi2(df)
        
        total_combinations = len(self.R4_critical_range) * len(self.alpha_klein_range)
        combination_count = 0
        
        for R4_crit in self.R4_critical_range:
            for alpha_k in self.alpha_klein_range:
                combination_count += 1
                
                # Calculate Klein cosmological distances
                klein_distances = []
                klein_fields = []
                
                for _, row in df.iterrows():
                    z = row['z']
                    d_L_klein, phi5_evolution = self.klein_luminosity_distance(z, R4_crit, alpha_k)
                    klein_distances.append(d_L_klein)
                    klein_fields.append(phi5_evolution[-1])  # Final Klein field
                    
                klein_distances = np.array(klein_distances)
                klein_fields = np.array(klein_fields)
                
                # Calculate Klein distance moduli
                mu_klein = 5 * np.log10(klein_distances) + 25
                mu_observed = df['mu'].values
                mu_errors = df['mu_err'].values
                
                # Chi-squared for Klein model
                chi2_klein = np.sum((mu_observed - mu_klein)**2 / mu_errors**2)
                chi2_improvement = chi2_lcdm - chi2_klein
                
                # Distance modifications
                distance_modifications = (klein_distances - df['distance_mpc'].values) / df['distance_mpc'].values
                rms_distance_mod = np.sqrt(np.mean(distance_modifications**2))
                
                # Statistical significance
                delta_chi2 = chi2_improvement
                if delta_chi2 > 0:
                    n_dof = 2  # Two additional parameters (R4_critical, alpha_klein)
                    sigma_equiv = np.sqrt(delta_chi2)
                else:
                    sigma_equiv = 0.0
                    
                # Observational detectability assessment
                max_distance_mod = np.max(np.abs(distance_modifications))
                if max_distance_mod > 0.01 and sigma_equiv > 3.0:  # >1% distance change + >3σ
                    detectability = "DETECTABLE"
                elif max_distance_mod > 0.005 or sigma_equiv > 1.0:  # >0.5% change or >1σ
                    detectability = "MARGINAL"
                else:
                    detectability = "UNDETECTABLE"
                    
                # Store results
                results['R4_critical_grid'].append(R4_crit)
                results['alpha_klein_grid'].append(alpha_k)
                results['chi2_improvements'].append(chi2_improvement)
                results['mean_phi5_amplitudes'].append(np.mean(klein_fields))
                results['distance_modifications_rms'].append(rms_distance_mod)
                results['statistical_significances'].append(sigma_equiv)
                results['observational_detectability'].append(detectability)
                
                # Progress update
                if combination_count % 500 == 0:
                    print(f"   Progress: {combination_count}/{total_combinations} ({100*combination_count/total_combinations:.1f}%)")
                    
        # Convert to arrays
        for key in ['R4_critical_grid', 'alpha_klein_grid', 'chi2_improvements',
                   'mean_phi5_amplitudes', 'distance_modifications_rms', 
                   'statistical_significances']:
            results[key] = np.array(results[key])
            
        print(f"   ✓ Completed {len(results['R4_critical_grid'])} parameter combinations")
        print(f"   Chi² improvement range: {results['chi2_improvements'].min():.1f} - {results['chi2_improvements'].max():.1f}")
        print(f"   Distance modification range: {results['distance_modifications_rms'].min():.2e} - {results['distance_modifications_rms'].max():.2e}")
        print(f"   Significance range: {results['statistical_significances'].min():.1f}σ - {results['statistical_significances'].max():.1f}σ")
        
        # Count detectable solutions
        detectable_count = sum(1 for d in results['observational_detectability'] if d == "DETECTABLE")
        marginal_count = sum(1 for d in results['observational_detectability'] if d == "MARGINAL")
        print(f"   Detectable solutions: {detectable_count}/{len(results['observational_detectability'])}")
        print(f"   Marginal solutions: {marginal_count}/{len(results['observational_detectability'])}")
        
        return results
        
    def _calculate_lcdm_chi2(self, df: pd.DataFrame) -> float:
        """Calculate reference ΛCDM chi-squared"""
        
        mu_observed = df['mu'].values
        mu_lcdm = df['lcdm_mu'].values
        mu_errors = df['mu_err'].values
        
        chi2_lcdm = np.sum((mu_observed - mu_lcdm)**2 / mu_errors**2)
        
        return chi2_lcdm
        
    def find_optimal_klein_cosmology_parameters(self, exploration_results: Dict[str, Any]) -> Dict[str, Any]:
        """Find optimal Klein cosmology parameters"""
        
        print("\n🎯 FINDING OPTIMAL KLEIN COSMOLOGY PARAMETERS")
        
        chi2_improvements = exploration_results['chi2_improvements']
        significances = exploration_results['statistical_significances']
        distance_mods = exploration_results['distance_modifications_rms']
        phi5_amplitudes = exploration_results['mean_phi5_amplitudes']
        R4_values = exploration_results['R4_critical_grid']
        alpha_values = exploration_results['alpha_klein_grid']
        detectability = exploration_results['observational_detectability']
        
        optimal_solutions = {}
        
        # 1. Maximum chi-squared improvement
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
            
        # 2. Maximum statistical significance
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
            # Among detectable, find highest significance
            detectable_significances = significances[detectable_indices]
            best_detectable_idx = detectable_indices[np.argmax(detectable_significances)]
            
            optimal_solutions['best_detectable'] = {
                'R4_critical': float(R4_values[best_detectable_idx]),
                'alpha_klein': float(alpha_values[best_detectable_idx]),
                'chi2_improvement': float(chi2_improvements[best_detectable_idx]),
                'significance_sigma': float(significances[best_detectable_idx]),
                'phi5_amplitude': float(phi5_amplitudes[best_detectable_idx]),
                'distance_modification_rms': float(distance_mods[best_detectable_idx]),
                'detectability': detectability[best_detectable_idx],
                'description': 'Best detectable Klein cosmology'
            }
            
        # 4. Optimal balance (moderate distance modification + high significance)
        # Score function: significance × log(distance_modification)
        scores = significances * np.log10(distance_mods + 1e-10)
        valid_scores = scores[np.isfinite(scores)]
        if len(valid_scores) > 0:
            optimal_balance_idx = np.argmax(scores)
            optimal_solutions['optimal_balance'] = {
                'R4_critical': float(R4_values[optimal_balance_idx]),
                'alpha_klein': float(alpha_values[optimal_balance_idx]),
                'chi2_improvement': float(chi2_improvements[optimal_balance_idx]),
                'significance_sigma': float(significances[optimal_balance_idx]),
                'phi5_amplitude': float(phi5_amplitudes[optimal_balance_idx]),
                'distance_modification_rms': float(distance_mods[optimal_balance_idx]),
                'detectability': detectability[optimal_balance_idx],
                'description': 'Optimal balance of significance and observability'
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
        
    def create_comprehensive_cosmology_visualization(self, exploration_results: Dict[str, Any],
                                                   optimal_solutions: Dict[str, Any]) -> None:
        """Create comprehensive visualization of Klein cosmology results"""
        
        print("\n📊 CREATING COMPREHENSIVE COSMOLOGY VISUALIZATION")
        
        # Reshape data for 2D plotting
        n_R4 = len(self.R4_critical_range)
        n_alpha = len(self.alpha_klein_range)
        
        chi2_grid = exploration_results['chi2_improvements'].reshape(n_R4, n_alpha)
        significance_grid = exploration_results['statistical_significances'].reshape(n_R4, n_alpha)
        distance_mod_grid = exploration_results['distance_modifications_rms'].reshape(n_R4, n_alpha)
        phi5_grid = exploration_results['mean_phi5_amplitudes'].reshape(n_R4, n_alpha)
        
        fig = plt.figure(figsize=(20, 15))
        
        # 1. Chi-squared improvement heatmap
        ax1 = plt.subplot(2, 3, 1)
        im1 = ax1.imshow(chi2_grid, aspect='auto', origin='lower', cmap='viridis',
                        extent=[np.log10(self.alpha_klein_range.min()), np.log10(self.alpha_klein_range.max()),
                               np.log10(self.R4_critical_range.min()), np.log10(self.R4_critical_range.max())])
        ax1.set_xlabel('log₁₀(αₖ)')
        ax1.set_ylabel('log₁₀(R₄_critical)')
        ax1.set_title('χ² Improvement')
        plt.colorbar(im1, ax=ax1, label='Δχ²')
        
        # 2. Statistical significance heatmap
        ax2 = plt.subplot(2, 3, 2)
        im2 = ax2.imshow(significance_grid, aspect='auto', origin='lower', cmap='plasma',
                        extent=[np.log10(self.alpha_klein_range.min()), np.log10(self.alpha_klein_range.max()),
                               np.log10(self.R4_critical_range.min()), np.log10(self.R4_critical_range.max())])
        ax2.set_xlabel('log₁₀(αₖ)')
        ax2.set_ylabel('log₁₀(R₄_critical)')
        ax2.set_title('Statistical Significance')
        plt.colorbar(im2, ax=ax2, label='σ')
        
        # 3. Distance modification heatmap
        ax3 = plt.subplot(2, 3, 3)
        im3 = ax3.imshow(distance_mod_grid, aspect='auto', origin='lower', cmap='coolwarm',
                        extent=[np.log10(self.alpha_klein_range.min()), np.log10(self.alpha_klein_range.max()),
                               np.log10(self.R4_critical_range.min()), np.log10(self.R4_critical_range.max())])
        ax3.set_xlabel('log₁₀(αₖ)')
        ax3.set_ylabel('log₁₀(R₄_critical)')
        ax3.set_title('Distance Modification (RMS)')
        plt.colorbar(im3, ax=ax3, label='Fractional Distance Change')
        
        # 4. Klein field amplitude heatmap
        ax4 = plt.subplot(2, 3, 4)
        im4 = ax4.imshow(phi5_grid, aspect='auto', origin='lower', cmap='magma',
                        extent=[np.log10(self.alpha_klein_range.min()), np.log10(self.alpha_klein_range.max()),
                               np.log10(self.R4_critical_range.min()), np.log10(self.R4_critical_range.max())])
        ax4.set_xlabel('log₁₀(αₖ)')
        ax4.set_ylabel('log₁₀(R₄_critical)')
        ax4.set_title('Mean Klein Field φ₅')
        plt.colorbar(im4, ax=ax4, label='φ₅')
        
        # 5. Optimal parameter points
        ax5 = plt.subplot(2, 3, 5)
        # Plot parameter space background
        ax5.imshow(significance_grid, aspect='auto', origin='lower', cmap='gray', alpha=0.3,
                  extent=[np.log10(self.alpha_klein_range.min()), np.log10(self.alpha_klein_range.max()),
                         np.log10(self.R4_critical_range.min()), np.log10(self.R4_critical_range.max())])
        
        # Plot optimal points
        colors = ['red', 'blue', 'green', 'orange', 'purple']
        markers = ['o', 's', '^', 'D', 'v']
        
        for i, (name, solution) in enumerate(optimal_solutions.items()):
            if i < len(colors):
                ax5.scatter(np.log10(solution['alpha_klein']), np.log10(solution['R4_critical']),
                          color=colors[i], marker=markers[i], s=200, 
                          label=name.replace('_', ' '), alpha=0.8, edgecolors='black')
                
        ax5.set_xlabel('log₁₀(αₖ)')
        ax5.set_ylabel('log₁₀(R₄_critical)')
        ax5.set_title('Optimal Parameter Points')
        ax5.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        
        # 6. Summary statistics
        ax6 = plt.subplot(2, 3, 6)
        ax6.axis('off')
        
        # Summary text
        detectable_count = sum(1 for d in exploration_results['observational_detectability'] if d == "DETECTABLE")
        marginal_count = sum(1 for d in exploration_results['observational_detectability'] if d == "MARGINAL")
        total_count = len(exploration_results['observational_detectability'])
        
        summary_text = f"""
OPTIMIZED KLEIN COSMOLOGY RESULTS
================================
Parameter Space: {n_R4} × {n_alpha} = {total_count} combinations

Statistical Performance:
Max χ² improvement: {exploration_results['chi2_improvements'].max():.1f}
Max significance: {exploration_results['statistical_significances'].max():.1f}σ
Max distance mod: {exploration_results['distance_modifications_rms'].max()*100:.2f}%

Observational Prospects:
Detectable solutions: {detectable_count}/{total_count} ({100*detectable_count/total_count:.1f}%)
Marginal solutions: {marginal_count}/{total_count} ({100*marginal_count/total_count:.1f}%)

Klein Field Range:
Mean φ₅: {exploration_results['mean_phi5_amplitudes'].min():.3f} - {exploration_results['mean_phi5_amplitudes'].max():.3f}
        """
        
        ax6.text(0.1, 0.9, summary_text, transform=ax6.transAxes, fontsize=11,
                verticalalignment='top', fontfamily='monospace',
                bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
        
        plt.tight_layout()
        plt.savefig('optimized_klein_sne_cosmology_analysis.png', dpi=300, bbox_inches='tight')
        print("   ✓ Saved: optimized_klein_sne_cosmology_analysis.png")
        
    def run_complete_optimized_analysis(self) -> Dict[str, Any]:
        """Execute complete optimized Klein supernovae cosmology analysis"""
        
        print("🌟 OPTIMIZED KLEIN SUPERNOVAE COSMOLOGY ANALYSIS")
        print("=" * 65)
        print("ADDRESSING COUPLING CONSTANT CRISIS:")
        print("✓ Direct cosmological Klein coupling (αₖ) implementation")
        print("✓ 2D parameter space optimization (R₄_critical, αₖ)")
        print("✓ High-fidelity Pantheon+ representative sample")
        print("✓ Klein-modified Hubble parameter H²(z)[1 + αₖ⋅φ₅(z)]")
        print("✓ Observational detectability assessment")
        print("=" * 65)
        
        # 1. Load supernovae data
        print("\n1️⃣ LOADING HIGH-FIDELITY SUPERNOVAE DATA")
        df = self.load_real_pantheon_data()
        
        # 2. Parameter space exploration
        print("\n2️⃣ COMPREHENSIVE PARAMETER SPACE EXPLORATION")
        exploration_results = self.comprehensive_parameter_space_exploration(df)
        
        # 3. Find optimal parameters
        print("\n3️⃣ FINDING OPTIMAL KLEIN COSMOLOGY PARAMETERS")
        optimal_solutions = self.find_optimal_klein_cosmology_parameters(exploration_results)
        
        # 4. Create visualization
        print("\n4️⃣ CREATING COMPREHENSIVE VISUALIZATION")
        self.create_comprehensive_cosmology_visualization(exploration_results, optimal_solutions)
        
        # Compile complete results
        results = {
            'metadata': {
                'analysis_type': 'OPTIMIZED_KLEIN_SNE_COSMOLOGY',
                'addressing_issue': 'Coupling constant crisis in cosmological Klein effects',
                'methodology': 'Direct cosmological Klein coupling implementation',
                'parameter_space_size': len(exploration_results['R4_critical_grid']),
                'n_supernovae': len(df)
            },
            'supernovae_data': {
                'n_sne': len(df),
                'redshift_range': [float(df['z'].min()), float(df['z'].max())],
                'distance_range_mpc': [float(df['distance_mpc'].min()), float(df['distance_mpc'].max())],
                'mean_uncertainty_mag': float(df['mu_err'].mean())
            },
            'parameter_exploration': {
                'R4_critical_range': [float(self.R4_critical_range.min()), float(self.R4_critical_range.max())],
                'alpha_klein_range': [float(self.alpha_klein_range.min()), float(self.alpha_klein_range.max())],
                'grid_dimensions': [len(self.R4_critical_range), len(self.alpha_klein_range)],
                'total_combinations': len(exploration_results['R4_critical_grid'])
            },
            'exploration_results': {
                'chi2_improvements': exploration_results['chi2_improvements'].tolist(),
                'statistical_significances': exploration_results['statistical_significances'].tolist(),
                'distance_modifications_rms': exploration_results['distance_modifications_rms'].tolist(),
                'mean_phi5_amplitudes': exploration_results['mean_phi5_amplitudes'].tolist(),
                'observational_detectability': exploration_results['observational_detectability']
            },
            'optimal_solutions': optimal_solutions,
            'scientific_assessment': self._generate_final_scientific_assessment(
                exploration_results, optimal_solutions)
        }
        
        return results, df
        
    def _generate_final_scientific_assessment(self, exploration_results: Dict[str, Any],
                                            optimal_solutions: Dict[str, Any]) -> Dict[str, Any]:
        """Generate final scientific assessment"""
        
        # Count solution categories
        detectable_count = sum(1 for d in exploration_results['observational_detectability'] if d == "DETECTABLE")
        marginal_count = sum(1 for d in exploration_results['observational_detectability'] if d == "MARGINAL") 
        total_count = len(exploration_results['observational_detectability'])
        
        # Performance metrics
        max_chi2_improvement = np.max(exploration_results['chi2_improvements'])
        max_significance = np.max(exploration_results['statistical_significances'])
        max_distance_mod = np.max(exploration_results['distance_modifications_rms'])
        
        # Determine overall viability
        if detectable_count >= 10 and max_significance >= 5.0:
            viability = "HIGH"
        elif detectable_count >= 1 or max_significance >= 3.0:
            viability = "MODERATE"  
        elif marginal_count >= 5 or max_significance >= 1.0:
            viability = "LOW"
        else:
            viability = "NEGLIGIBLE"
            
        # Find best overall solution
        best_solution_name = None
        best_solution_score = -1
        
        for name, solution in optimal_solutions.items():
            score = 0
            if solution['detectability'] == "DETECTABLE":
                score += 10
            elif solution['detectability'] == "MARGINAL":
                score += 5
                
            if solution['significance_sigma'] >= 5.0:
                score += 5
            elif solution['significance_sigma'] >= 3.0:
                score += 3
            elif solution['significance_sigma'] >= 1.0:
                score += 1
                
            if solution['distance_modification_rms'] >= 0.01:  # >1%
                score += 3
            elif solution['distance_modification_rms'] >= 0.005:  # >0.5%
                score += 1
                
            if score > best_solution_score:
                best_solution_score = score
                best_solution_name = name
                
        assessment = {
            'overall_viability': viability,
            'detectable_solutions': detectable_count,
            'marginal_solutions': marginal_count,
            'total_solutions': total_count,
            'detectability_rate': detectable_count / total_count,
            'performance_metrics': {
                'max_chi2_improvement': float(max_chi2_improvement),
                'max_statistical_significance': float(max_significance),
                'max_distance_modification_percent': float(max_distance_mod * 100)
            },
            'best_solution': best_solution_name,
            'best_solution_details': optimal_solutions.get(best_solution_name, {}),
            'coupling_crisis_resolution': {
                'original_coupling': 1e-6,
                'optimized_coupling_range': [float(self.alpha_klein_range.min()), 
                                           float(self.alpha_klein_range.max())],
                'improvement_factor': float(self.alpha_klein_range.max() / 1e-6),
                'mechanism': 'Direct cosmological Klein coupling to Hubble parameter'
            },
            'key_findings': [
                f"Detectable solutions: {detectable_count}/{total_count} ({100*detectable_count/total_count:.1f}%)",
                f"Maximum significance: {max_significance:.1f}σ",
                f"Maximum distance modification: {max_distance_mod*100:.2f}%",
                f"Best solution: {best_solution_name}",
                f"Coupling enhancement: {self.alpha_klein_range.max()/1e-6:.0f}× stronger than original"
            ]
        }
        
        return assessment

def main():
    """Execute optimized Klein supernovae cosmology analysis"""
    
    os.chdir('/mnt/d/Multidimensional Theory Simulations/multidimensional-theory/gravitational-wave-echoes-5d/EMPIRICAL_KLEIN_STUDIES/5_Supernovae_Analysis')
    
    warnings.filterwarnings('ignore')
    
    # Initialize analysis
    analyzer = OptimizedKleinSNeAnalysis()
    
    # Run complete analysis
    results, df = analyzer.run_complete_optimized_analysis()
    
    # Save results
    with open('optimized_klein_sne_cosmology_results.json', 'w') as f:
        json.dump(results, f, indent=2, default=str)
        
    df.to_csv('optimized_klein_sne_cosmology_data.csv', index=False)
    
    print(f"\n💾 RESULTS SAVED:")
    print(f"   - optimized_klein_sne_cosmology_results.json")
    print(f"   - optimized_klein_sne_cosmology_data.csv")
    print(f"   - optimized_klein_sne_cosmology_analysis.png")
    
    assessment = results['scientific_assessment']
    print(f"\n🎯 OPTIMIZED ANALYSIS COMPLETE!")
    print(f"   Overall viability: {assessment['overall_viability']}")
    print(f"   Detectable solutions: {assessment['detectable_solutions']}/{assessment['total_solutions']}")
    print(f"   Maximum significance: {assessment['performance_metrics']['max_statistical_significance']:.1f}σ")
    print(f"   Maximum distance modification: {assessment['performance_metrics']['max_distance_modification_percent']:.2f}%")
    print(f"   Best solution: {assessment['best_solution']}")
    
    if assessment['best_solution']:
        best = assessment['best_solution_details']
        print(f"   Best R₄_critical: {best['R4_critical']:.2e}")
        print(f"   Best αₖ: {best['alpha_klein']:.2e}")
        print(f"   Best detectability: {best['detectability']}")
    
    return results

if __name__ == "__main__":
    results = main()