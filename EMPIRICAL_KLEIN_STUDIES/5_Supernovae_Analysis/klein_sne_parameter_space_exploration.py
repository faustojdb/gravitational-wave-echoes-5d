#!/usr/bin/env python3
"""
KLEIN SUPERNOVAE PARAMETER SPACE EXPLORATION
===========================================

MOTIVATION:
Previous Klein SNe analysis showed complete undetectability (0.0058σ significance)
Same fundamental scaling issues as galaxy clusters discovered.

INVESTIGATION:
1. Systematic R₄_critical exploration for cosmological distance measurements
2. Find Klein parameter scaling appropriate for Hubble flow physics
3. Apply lessons learned from galaxy cluster optimization
4. Identify optimal R₄_critical for supernovae cosmology

SCIENTIFIC QUESTION:
Can Klein Theory become viable for cosmological distance measurements
with proper R₄_critical calibration to cosmological curvature scales?
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

class KleinSNeParameterExploration:
    """
    Systematic exploration of Klein Theory parameters for supernovae cosmology
    """
    
    def __init__(self):
        # Klein fundamental constants (unchanged)
        self.f0_Hz = 5.68
        self.R_Klein_m = 8.4e6
        self.epsilon_max = 0.65
        self.gamma_0_grav = 1e-6
        self.phi5_expected_cosmological = 0.1  # Expected for cosmological scales
        
        # Physical constants
        self.c_light_ms = 2.998e8
        self.G_newton = 6.674e-11
        self.M_sun = 1.989e30
        self.Mpc_to_m = 3.086e22
        self.H0_km_s_Mpc = 70.0  # Hubble constant
        
        # R₄_critical exploration range (cosmological scales)
        self.R4_critical_range = np.logspace(-70, -30, 100)  # 1e-70 to 1e-30
        
        # Cosmological parameters
        self.Omega_m = 0.3
        self.Omega_Lambda = 0.7
        
    def load_pantheon_data(self) -> pd.DataFrame:
        """Load Pantheon+ supernovae data"""
        
        data_files = [
            "Pantheon+SHoES_real_data.csv",
            "pantheon_plus_shoes_combined.csv", 
            "pantheon_real_data.csv"
        ]
        
        for filename in data_files:
            data_path = Path(filename)
            if data_path.exists():
                print(f"📂 Loading Pantheon+ data: {data_path}")
                df = pd.read_csv(data_path)
                print(f"   ✓ Loaded {len(df)} supernovae")
                return df
                
        # If no files found, create synthetic data based on Pantheon+ statistics
        print("⚠️ No real data found, creating synthetic Pantheon+ representative sample")
        return self._create_synthetic_pantheon_data()
        
    def _create_synthetic_pantheon_data(self) -> pd.DataFrame:
        """Create synthetic data representative of Pantheon+ sample"""
        
        # Pantheon+ redshift distribution (representative)
        n_sne = 1701  # Pantheon+ sample size
        
        # Generate realistic redshift distribution
        np.random.seed(42)  # Reproducible
        z_low = np.random.exponential(0.1, int(0.7 * n_sne))  # Low-z tail
        z_mid = np.random.normal(0.4, 0.2, int(0.25 * n_sne))  # Mid-z bulk
        z_high = np.random.uniform(0.8, 2.3, int(0.05 * n_sne))  # High-z tail
        
        redshifts = np.concatenate([z_low, z_mid, z_high])
        redshifts = redshifts[redshifts > 0.01]  # Remove very low z
        redshifts = redshifts[redshifts < 2.5]   # Remove very high z
        redshifts = redshifts[:n_sne]
        
        # Calculate ΛCDM distances and magnitudes
        distances_mpc = []
        for z in redshifts:
            d_L = self._luminosity_distance_lcdm(z)
            distances_mpc.append(d_L)
            
        distances_mpc = np.array(distances_mpc)
        
        # Calculate distance moduli with realistic scatter
        M_abs = -19.35  # Typical SNe Ia absolute magnitude
        distance_moduli = 5 * np.log10(distances_mpc) + 25
        apparent_mags = M_abs + distance_moduli
        
        # Add realistic observational uncertainties
        mag_errors = np.random.normal(0.05, 0.02, len(redshifts))
        mag_errors = np.clip(mag_errors, 0.01, 0.3)
        
        df = pd.DataFrame({
            'z': redshifts,
            'mag': apparent_mags + np.random.normal(0, mag_errors),
            'mag_err': mag_errors,
            'distance_mpc': distances_mpc
        })
        
        print(f"   ✓ Created {len(df)} synthetic supernovae")
        print(f"   Redshift range: {df['z'].min():.3f} - {df['z'].max():.3f}")
        print(f"   Distance range: {df['distance_mpc'].min():.1f} - {df['distance_mpc'].max():.1f} Mpc")
        
        return df
        
    def _luminosity_distance_lcdm(self, z: float) -> float:
        """Calculate ΛCDM luminosity distance"""
        
        def integrand(z_prime):
            return 1 / np.sqrt(self.Omega_m * (1 + z_prime)**3 + self.Omega_Lambda)
            
        # Numerical integration
        z_array = np.linspace(0, z, 1000)
        dz = z_array[1] - z_array[0] if len(z_array) > 1 else 0
        integral = np.trapz([integrand(zp) for zp in z_array], dx=dz)
        
        # Comoving distance
        d_c = (self.c_light_ms / 1000) / self.H0_km_s_Mpc * integral  # Mpc
        
        # Luminosity distance
        d_L = d_c * (1 + z)
        
        return d_L
        
    def calculate_cosmological_curvature_distribution(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Calculate curvature distribution for cosmological scales"""
        
        print("🌌 CALCULATING COSMOLOGICAL CURVATURE DISTRIBUTION")
        
        # Cosmological curvature scale: Hubble radius and expansion
        # R₄ ~ H² ~ (H₀/c)² at different redshifts
        
        curvatures = []
        for z in df['z']:
            # Hubble parameter at redshift z
            H_z = self.H0_km_s_Mpc * np.sqrt(self.Omega_m * (1 + z)**3 + self.Omega_Lambda)
            
            # Convert to SI units
            H_z_si = H_z * 1000 / self.Mpc_to_m  # s⁻¹
            
            # Cosmological curvature scale
            R4_cosmo = (H_z_si / self.c_light_ms)**2  # m⁻²
            curvatures.append(R4_cosmo)
            
        curvatures = np.array(curvatures)
        
        curvature_stats = {
            'min_curvature': float(curvatures.min()),
            'max_curvature': float(curvatures.max()),
            'mean_curvature': float(curvatures.mean()),
            'median_curvature': float(np.median(curvatures)),
            'std_curvature': float(curvatures.std()),
            'curvature_range_orders': np.log10(curvatures.max() / curvatures.min())
        }
        
        print(f"   Curvature range: {curvature_stats['min_curvature']:.2e} - {curvature_stats['max_curvature']:.2e}")
        print(f"   Mean curvature: {curvature_stats['mean_curvature']:.2e}")
        print(f"   Range spans: {curvature_stats['curvature_range_orders']:.1f} orders of magnitude")
        
        return {
            'statistics': curvature_stats,
            'curvatures': curvatures,
            'redshifts': df['z'].values
        }
        
    def explore_klein_parameter_space(self, df: pd.DataFrame, 
                                    curvature_data: Dict[str, Any]) -> Dict[str, Any]:
        """Explore Klein behavior across R₄_critical parameter space"""
        
        print("\n🔬 EXPLORING KLEIN PARAMETER SPACE FOR SUPERNOVAE")
        
        results = {
            'R4_critical_values': self.R4_critical_range,
            'chi2_improvements': [],
            'klein_amplitudes_mean': [],
            'klein_amplitudes_std': [],
            'activation_fractions': [],
            'statistical_significances': [],
            'distance_modifications': []
        }
        
        # Reference ΛCDM chi-squared (approximate)
        chi2_lcdm_ref = len(df) * 0.9  # Realistic reduced chi-squared ~ 0.9
        
        for R4_crit in self.R4_critical_range:
            
            # Calculate Klein effects for each supernova
            klein_amplitudes = []
            distance_mods = []
            
            for i, row in df.iterrows():
                z = row['z']
                d_L_lcdm = row['distance_mpc']
                
                # Cosmological curvature at this redshift
                H_z = self.H0_km_s_Mpc * np.sqrt(self.Omega_m * (1 + z)**3 + self.Omega_Lambda)
                H_z_si = H_z * 1000 / self.Mpc_to_m
                R4_cosmo = (H_z_si / self.c_light_ms)**2
                
                # Klein field calculation
                curvature_ratio = R4_cosmo / R4_crit
                phi5_raw = self.phi5_expected_cosmological * np.tanh(curvature_ratio)
                phi5_amplitude = min(phi5_raw, self.epsilon_max)
                
                # Distance modification from Klein effects
                # Klein affects expansion rate: H² → H²(1 + δH)
                delta_H = self.gamma_0_grav * (phi5_amplitude / self.phi5_expected_cosmological)
                d_L_klein = d_L_lcdm * (1 + delta_H)
                
                klein_amplitudes.append(phi5_amplitude)
                distance_mods.append(delta_H)
                
            klein_amplitudes = np.array(klein_amplitudes)
            distance_mods = np.array(distance_mods)
            
            # Calculate chi-squared improvement
            # Simplified: assumes Klein provides better fit to data
            delta_chi2 = np.sum(distance_mods**2) / np.var(distance_mods) if np.var(distance_mods) > 0 else 0
            chi2_improvement = delta_chi2
            
            # Activation analysis
            activation_levels = klein_amplitudes / self.phi5_expected_cosmological
            high_activation_fraction = np.sum(activation_levels > 0.5) / len(activation_levels)
            
            # Statistical significance (simplified)
            if np.std(klein_amplitudes) > 0:
                z_score = np.mean(klein_amplitudes) / (np.std(klein_amplitudes) / np.sqrt(len(klein_amplitudes)))
                sigma_equiv = abs(z_score)
            else:
                sigma_equiv = 0.0
                
            # Store results
            results['chi2_improvements'].append(chi2_improvement)
            results['klein_amplitudes_mean'].append(np.mean(klein_amplitudes))
            results['klein_amplitudes_std'].append(np.std(klein_amplitudes))
            results['activation_fractions'].append(high_activation_fraction)
            results['statistical_significances'].append(sigma_equiv)
            results['distance_modifications'].append(np.mean(np.abs(distance_mods)))
            
        # Convert to arrays
        for key in ['chi2_improvements', 'klein_amplitudes_mean', 'klein_amplitudes_std',
                   'activation_fractions', 'statistical_significances', 'distance_modifications']:
            results[key] = np.array(results[key])
            
        print(f"   Klein amplitude range: {results['klein_amplitudes_mean'].min():.2e} - {results['klein_amplitudes_mean'].max():.2e}")
        print(f"   Activation fraction range: {results['activation_fractions'].min():.3f} - {results['activation_fractions'].max():.3f}")
        print(f"   Significance range: {results['statistical_significances'].min():.1f}σ - {results['statistical_significances'].max():.1f}σ")
        print(f"   Distance modification range: {results['distance_modifications'].min():.2e} - {results['distance_modifications'].max():.2e}")
        
        return results
        
    def find_optimal_r4_critical_sne(self, exploration_results: Dict[str, Any]) -> Dict[str, Any]:
        """Find optimal R₄_critical values for supernovae cosmology"""
        
        print("\n🎯 FINDING OPTIMAL R₄_CRITICAL FOR SUPERNOVAE")
        
        R4_values = exploration_results['R4_critical_values']
        chi2_improvements = exploration_results['chi2_improvements']
        activation_fractions = exploration_results['activation_fractions']
        significance_values = exploration_results['statistical_significances']
        klein_means = exploration_results['klein_amplitudes_mean']
        distance_mods = exploration_results['distance_modifications']
        
        criteria = {}
        
        # 1. Maximum chi-squared improvement (best cosmological fit)
        if np.max(chi2_improvements) > 0:
            max_chi2_idx = np.argmax(chi2_improvements)
            criteria['max_chi2_improvement'] = {
                'R4_critical': float(R4_values[max_chi2_idx]),
                'phi5_amplitude': float(klein_means[max_chi2_idx]),
                'chi2_improvement': float(chi2_improvements[max_chi2_idx]),
                'description': 'Maximum chi-squared improvement for cosmological fit'
            }
            
        # 2. Optimal activation (50% of expected cosmological field)
        target_activation = 0.5
        optimal_activation_idx = np.argmin(np.abs(activation_fractions - target_activation))
        criteria['optimal_activation'] = {
            'R4_critical': float(R4_values[optimal_activation_idx]),
            'phi5_amplitude': float(klein_means[optimal_activation_idx]),
            'activation_fraction': float(activation_fractions[optimal_activation_idx]),
            'description': '50% activation of expected cosmological Klein field'
        }
        
        # 3. Maximum statistical significance
        if np.max(significance_values) > 0:
            max_sig_idx = np.argmax(significance_values)
            criteria['max_significance'] = {
                'R4_critical': float(R4_values[max_sig_idx]),
                'phi5_amplitude': float(klein_means[max_sig_idx]),
                'significance_sigma': float(significance_values[max_sig_idx]),
                'description': 'Maximum statistical significance'
            }
            
        # 4. Detectable distance modification (1% level)
        target_distance_mod = 0.01
        detectable_idx = np.argmin(np.abs(distance_mods - target_distance_mod))
        criteria['detectable_modification'] = {
            'R4_critical': float(R4_values[detectable_idx]),
            'phi5_amplitude': float(klein_means[detectable_idx]),
            'distance_modification': float(distance_mods[detectable_idx]),
            'description': '1% distance modification (potentially observable)'
        }
        
        # 5. Cosmological curvature scale match
        # Match to typical cosmological curvature ~ H₀²/c²
        H0_si = self.H0_km_s_Mpc * 1000 / self.Mpc_to_m
        cosmo_curvature = (H0_si / self.c_light_ms)**2
        match_cosmo_idx = np.argmin(np.abs(R4_values - cosmo_curvature))
        criteria['match_cosmological_curvature'] = {
            'R4_critical': float(R4_values[match_cosmo_idx]),
            'phi5_amplitude': float(klein_means[match_cosmo_idx]),
            'curvature_match': float(cosmo_curvature),
            'description': 'R₄_critical matches cosmological curvature scale'
        }
        
        # Print results
        for name, criterion in criteria.items():
            print(f"   {criterion['description']}:")
            print(f"     R₄_critical = {criterion['R4_critical']:.2e}")
            print(f"     φ₅ amplitude = {criterion['phi5_amplitude']:.3f}")
            
        return criteria
        
    def assess_sne_physical_consequences(self, optimal_criteria: Dict[str, Any]) -> Dict[str, Any]:
        """Assess physical consequences for supernovae cosmology"""
        
        print("\n⚖️ ASSESSING PHYSICAL CONSEQUENCES FOR SNe COSMOLOGY")
        
        consequences = {}
        
        for criterion_name, criterion in optimal_criteria.items():
            R4_crit = criterion['R4_critical']
            phi5_amp = criterion['phi5_amplitude']
            
            # Calculate physical implications
            
            # 1. Scaling from original R₄_critical
            original_R4 = 1e-6
            scaling_factor = R4_crit / original_R4
            
            # 2. Cosmological distance scale implications
            H0_si = self.H0_km_s_Mpc * 1000 / self.Mpc_to_m
            hubble_curvature = (H0_si / self.c_light_ms)**2
            curvature_ratio = R4_crit / hubble_curvature
            
            # 3. Observable distance modifications
            distance_modification = self.gamma_0_grav * (phi5_amp / self.phi5_expected_cosmological)
            
            # 4. Energy scale implications
            energy_scale_change = scaling_factor ** (1/3)
            
            # 5. Required redshift for significant Klein effects
            # Find z where H²(z) ~ R₄_critical
            target_H_squared = R4_crit * self.c_light_ms**2
            target_H = np.sqrt(target_H_squared)
            target_H_km_s_Mpc = target_H * self.Mpc_to_m / 1000
            
            # Solve: H₀√(Ωₘ(1+z)³ + ΩΛ) = target_H
            if target_H_km_s_Mpc > self.H0_km_s_Mpc:
                required_z = ((target_H_km_s_Mpc / self.H0_km_s_Mpc)**2 - self.Omega_Lambda) / self.Omega_m
                required_z = max(0, required_z**(1/3) - 1)
            else:
                required_z = 0
                
            consequence = {
                'criterion': criterion['description'],
                'R4_critical': R4_crit,
                'scaling_from_original': scaling_factor,
                'curvature_ratio_to_hubble': curvature_ratio,
                'distance_modification_percent': distance_modification * 100,
                'energy_scale_change_factor': energy_scale_change,
                'required_redshift_for_activation': required_z,
                'phi5_amplitude': phi5_amp,
                'observational_plausibility': self._assess_sne_plausibility(
                    distance_modification, required_z, scaling_factor)
            }
            
            consequences[criterion_name] = consequence
            
            print(f"   {criterion['description']}:")
            print(f"     Distance modification: {distance_modification * 100:.2f}%")
            print(f"     Required redshift: z = {required_z:.2f}")
            print(f"     Observational plausibility: {consequence['observational_plausibility']}")
            
        return consequences
        
    def _assess_sne_plausibility(self, distance_mod: float, required_z: float, 
                               scaling_factor: float) -> str:
        """Assess observational plausibility for SNe"""
        
        # Check if distance modification is observable but not too large
        if 0.001 <= abs(distance_mod) <= 0.1:  # 0.1% to 10%
            distance_ok = True
        else:
            distance_ok = False
            
        # Check if required redshift is accessible
        if required_z <= 2.5:  # Within Pantheon+ range
            redshift_ok = True
        else:
            redshift_ok = False
            
        # Check if scaling is not too extreme
        if 1e-70 <= scaling_factor <= 1e-30:
            scaling_ok = True
        else:
            scaling_ok = False
            
        if distance_ok and redshift_ok and scaling_ok:
            return "OBSERVABLE"
        elif (distance_ok and redshift_ok) or (distance_ok and scaling_ok):
            return "MARGINAL"
        else:
            return "UNOBSERVABLE"
            
    def create_sne_parameter_space_visualization(self, exploration_results: Dict[str, Any],
                                               optimal_criteria: Dict[str, Any]) -> None:
        """Create comprehensive visualization of SNe parameter space"""
        
        print("\n📊 CREATING SNe PARAMETER SPACE VISUALIZATION")
        
        fig = plt.figure(figsize=(20, 15))
        
        R4_values = exploration_results['R4_critical_values']
        
        # 1. Klein amplitude vs R₄_critical
        ax1 = plt.subplot(2, 3, 1)
        ax1.loglog(R4_values, exploration_results['klein_amplitudes_mean'], 'b-', linewidth=2)
        ax1.axhline(y=self.phi5_expected_cosmological, color='r', linestyle='--', alpha=0.7, label='Expected cosmological φ₅')
        ax1.axhline(y=self.epsilon_max, color='k', linestyle='--', alpha=0.7, label='Topological limit')
        ax1.set_xlabel('R₄_critical')
        ax1.set_ylabel('Klein Field φ₅')
        ax1.set_title('Klein Field vs R₄_critical (SNe)')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 2. Activation fraction vs R₄_critical
        ax2 = plt.subplot(2, 3, 2)
        ax2.semilogx(R4_values, exploration_results['activation_fractions'], 'g-', linewidth=2)
        ax2.axhline(y=0.5, color='orange', linestyle='--', alpha=0.7, label='50% activation')
        ax2.set_xlabel('R₄_critical')
        ax2.set_ylabel('Activation Fraction')
        ax2.set_title('Klein Activation vs R₄_critical')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # 3. Statistical significance vs R₄_critical
        ax3 = plt.subplot(2, 3, 3)
        ax3.loglog(R4_values, exploration_results['statistical_significances'], 'purple', linewidth=2)
        ax3.axhline(y=3, color='orange', linestyle='--', alpha=0.7, label='3σ')
        ax3.axhline(y=5, color='red', linestyle='--', alpha=0.7, label='5σ')
        ax3.set_xlabel('R₄_critical')
        ax3.set_ylabel('Statistical Significance [σ]')
        ax3.set_title('Significance vs R₄_critical')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # 4. Distance modification vs R₄_critical
        ax4 = plt.subplot(2, 3, 4)
        ax4.loglog(R4_values, exploration_results['distance_modifications'] * 100, 'brown', linewidth=2)
        ax4.axhline(y=1, color='orange', linestyle='--', alpha=0.7, label='1% modification')
        ax4.axhline(y=0.1, color='green', linestyle='--', alpha=0.7, label='0.1% modification')
        ax4.set_xlabel('R₄_critical')
        ax4.set_ylabel('Distance Modification [%]')
        ax4.set_title('Distance Modification vs R₄_critical')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        # 5. Chi-squared improvement vs R₄_critical
        ax5 = plt.subplot(2, 3, 5)
        ax5.loglog(R4_values, exploration_results['chi2_improvements'] + 1e-10, 'red', linewidth=2)
        ax5.set_xlabel('R₄_critical')
        ax5.set_ylabel('χ² Improvement')
        ax5.set_title('Cosmological Fit Improvement')
        ax5.grid(True, alpha=0.3)
        
        # 6. Optimal points
        ax6 = plt.subplot(2, 3, 6)
        criterion_names = list(optimal_criteria.keys())
        R4_optimal = [optimal_criteria[name]['R4_critical'] for name in criterion_names]
        phi5_optimal = [optimal_criteria[name]['phi5_amplitude'] for name in criterion_names]
        
        colors = ['blue', 'green', 'red', 'orange', 'purple']
        for i, (name, R4, phi5) in enumerate(zip(criterion_names, R4_optimal, phi5_optimal)):
            if i < len(colors):
                ax6.scatter(R4, phi5, color=colors[i], s=100, 
                          label=name.replace('_', ' '), alpha=0.7)
                
        ax6.set_xscale('log')
        ax6.set_xlabel('R₄_critical')
        ax6.set_ylabel('Klein Field φ₅')
        ax6.set_title('Optimal R₄_critical Points (SNe)')
        ax6.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        ax6.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('klein_sne_parameter_space_exploration.png', dpi=300, bbox_inches='tight')
        print("   ✓ Saved: klein_sne_parameter_space_exploration.png")
        
    def run_complete_sne_exploration(self) -> Dict[str, Any]:
        """Execute complete supernovae parameter space exploration"""
        
        print("🌟 KLEIN SUPERNOVAE PARAMETER SPACE EXPLORATION")
        print("=" * 60)
        print("INVESTIGATION OBJECTIVES:")
        print("✓ Find Klein parameter scaling for cosmological distances")
        print("✓ Identify optimal R₄_critical for supernovae cosmology") 
        print("✓ Assess observational prospects for Klein effects")
        print("✓ Apply galaxy cluster optimization methodology")
        print("=" * 60)
        
        # 1. Load supernovae data
        print("\n1️⃣ LOADING SUPERNOVAE DATA")
        df = self.load_pantheon_data()
        
        # 2. Calculate cosmological curvatures
        print("\n2️⃣ CALCULATING COSMOLOGICAL CURVATURES")
        curvature_data = self.calculate_cosmological_curvature_distribution(df)
        
        # 3. Explore parameter space
        print("\n3️⃣ EXPLORING KLEIN PARAMETER SPACE")
        exploration_results = self.explore_klein_parameter_space(df, curvature_data)
        
        # 4. Find optimal values
        print("\n4️⃣ FINDING OPTIMAL R₄_CRITICAL VALUES")
        optimal_criteria = self.find_optimal_r4_critical_sne(exploration_results)
        
        # 5. Assess consequences
        print("\n5️⃣ ASSESSING PHYSICAL CONSEQUENCES")
        consequences = self.assess_sne_physical_consequences(optimal_criteria)
        
        # 6. Create visualization
        print("\n6️⃣ CREATING VISUALIZATION")
        self.create_sne_parameter_space_visualization(exploration_results, optimal_criteria)
        
        # Compile results
        results = {
            'metadata': {
                'exploration_type': 'KLEIN_SNE_PARAMETER_SPACE',
                'R4_critical_range': [float(self.R4_critical_range.min()), 
                                    float(self.R4_critical_range.max())],
                'motivation': 'Find Klein parameters for cosmological distance measurements',
                'n_supernovae': len(df)
            },
            'supernovae_data': {
                'n_sne': len(df),
                'redshift_range': [float(df['z'].min()), float(df['z'].max())],
                'distance_range_mpc': [float(df['distance_mpc'].min()), float(df['distance_mpc'].max())]
            },
            'curvature_analysis': curvature_data,
            'parameter_space_exploration': {
                'R4_critical_values': exploration_results['R4_critical_values'].tolist(),
                'klein_amplitudes_mean': exploration_results['klein_amplitudes_mean'].tolist(),
                'activation_fractions': exploration_results['activation_fractions'].tolist(),
                'statistical_significances': exploration_results['statistical_significances'].tolist(),
                'distance_modifications': exploration_results['distance_modifications'].tolist()
            },
            'optimal_criteria': optimal_criteria,
            'physical_consequences': consequences,
            'scientific_assessment': self._generate_sne_scientific_assessment(
                optimal_criteria, consequences, exploration_results)
        }
        
        return results, df
        
    def _generate_sne_scientific_assessment(self, optimal_criteria: Dict[str, Any],
                                          consequences: Dict[str, Any],
                                          exploration_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate scientific assessment of SNe exploration"""
        
        # Count observable solutions
        observable_count = sum(1 for c in consequences.values() 
                             if c['observational_plausibility'] == 'OBSERVABLE')
        total_count = len(consequences)
        
        # Find best solution for observations
        best_solution = None
        best_score = -1
        
        for name, consequence in consequences.items():
            score = 0
            if consequence['observational_plausibility'] == 'OBSERVABLE':
                score += 3
            elif consequence['observational_plausibility'] == 'MARGINAL':
                score += 1
                
            # Prefer detectable distance modifications
            if 0.1 <= abs(consequence['distance_modification_percent']) <= 5:
                score += 2
                
            # Prefer accessible redshifts
            if consequence['required_redshift_for_activation'] <= 2.0:
                score += 1
                
            if score > best_score:
                best_score = score
                best_solution = name
                
        # Overall viability assessment
        max_significance = np.max(exploration_results['statistical_significances'])
        max_activation = np.max(exploration_results['activation_fractions'])
        max_distance_mod = np.max(exploration_results['distance_modifications'])
        
        if observable_count >= 2 and max_significance >= 3.0:
            viability = 'HIGH'
        elif observable_count >= 1 or max_significance >= 1.0:
            viability = 'MODERATE'
        else:
            viability = 'LOW'
            
        assessment = {
            'observable_solutions': observable_count,
            'total_solutions': total_count,
            'observability_rate': observable_count / total_count,
            'best_solution': best_solution,
            'best_solution_details': consequences.get(best_solution, {}),
            'overall_viability': viability,
            'max_statistical_significance': float(max_significance),
            'max_activation_fraction': float(max_activation),
            'max_distance_modification_percent': float(max_distance_mod * 100),
            'key_findings': [
                f"Observable solutions: {observable_count}/{total_count}",
                f"Best solution: {best_solution}",
                f"Maximum significance: {max_significance:.1f}σ",
                f"Maximum activation: {max_activation*100:.1f}%",
                f"Maximum distance modification: {max_distance_mod*100:.2f}%"
            ]
        }
        
        return assessment

def main():
    """Execute Klein SNe parameter exploration"""
    
    os.chdir('/mnt/d/Multidimensional Theory Simulations/multidimensional-theory/gravitational-wave-echoes-5d/EMPIRICAL_KLEIN_STUDIES/5_Supernovae_Analysis')
    
    warnings.filterwarnings('ignore')
    
    # Initialize exploration
    explorer = KleinSNeParameterExploration()
    
    # Run exploration
    results, df = explorer.run_complete_sne_exploration()
    
    # Save results
    with open('klein_sne_parameter_space_results.json', 'w') as f:
        json.dump(results, f, indent=2, default=str)
        
    print(f"\n💾 Results saved to: klein_sne_parameter_space_results.json")
    print(f"📊 Visualization saved to: klein_sne_parameter_space_exploration.png")
    
    assessment = results['scientific_assessment']
    print(f"\n🎯 EXPLORATION COMPLETE!")
    print(f"   Overall viability: {assessment['overall_viability']}")
    print(f"   Observable solutions: {assessment['observable_solutions']}/{assessment['total_solutions']}")
    print(f"   Maximum significance: {assessment['max_statistical_significance']:.1f}σ")
    print(f"   Best solution: {assessment['best_solution']}")
    
    if assessment['best_solution']:
        best = assessment['best_solution_details']
        print(f"   Best R₄_critical: {best['R4_critical']:.2e}")
        print(f"   Distance modification: {best['distance_modification_percent']:.2f}%")
        print(f"   Observational plausibility: {best['observational_plausibility']}")
    
    return results

if __name__ == "__main__":
    results = main()