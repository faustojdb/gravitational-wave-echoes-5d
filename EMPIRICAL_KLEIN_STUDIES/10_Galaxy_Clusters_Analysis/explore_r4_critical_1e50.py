#!/usr/bin/env python3
"""
EXPLORATION OF R₄_CRITICAL ~ 1e-50
==================================

MOTIVATION: 
Previous analysis showed galactic curvatures ~ 5e-56 to 5e-37
while theoretical R₄_critical = 1e-6 creates 45-order gap

INVESTIGATION:
1. Explore R₄_critical in range 1e-60 to 1e-30 
2. Find alignment with real galactic curvatures
3. Assess physical consequences of adjusted R₄_critical
4. Map Klein behavior in physically relevant regime
5. Determine if this creates well-behaved Klein physics

SCIENTIFIC QUESTION:
Can R₄_critical ~ 1e-50 produce physically meaningful Klein effects
without violating fundamental constraints?
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats
from typing import Dict, Any, Tuple
import warnings
import json

class R4CriticalExploration:
    """
    Systematic exploration of R₄_critical in galactic curvature regime
    """
    
    def __init__(self):
        # Klein fundamental constants (unchanged)
        self.f0_Hz = 5.68
        self.R_Klein_m = 8.4e6
        self.epsilon_max = 0.65
        self.gamma_0_grav = 1e-6
        self.phi5_expected_galactic = 0.3
        
        # Physical constants
        self.c_light_ms = 2.998e8
        self.G_newton = 6.674e-11
        self.M_sun = 1.989e30
        self.Mpc_to_m = 3.086e22
        self.kpc_to_m = 3.086e19
        
        # R₄_critical exploration range (around galactic curvatures)
        self.R4_critical_range = np.logspace(-65, -25, 100)  # 1e-65 to 1e-25
        
        # Representative cluster parameters
        self.typical_cluster = {
            'mass_msun': 1e14,
            'radius_kpc': 1000,  # 1 Mpc
            'name': 'Typical Galaxy Cluster'
        }
        
        # Range of cluster parameters for comprehensive study
        self.cluster_masses = np.logspace(13, 15.5, 20)  # 10¹³ to 3×10¹⁵ M☉
        self.cluster_radii = np.logspace(2, 3.5, 20)     # 100 to 3000 kpc
        
    def calculate_galactic_curvature_distribution(self) -> Dict[str, Any]:
        """
        Calculate actual curvature distribution for real galaxy clusters
        """
        print("🌌 CALCULATING REAL GALACTIC CURVATURE DISTRIBUTION")
        
        # Create parameter grid
        M_grid, R_grid = np.meshgrid(self.cluster_masses, self.cluster_radii)
        
        # Convert to physical units
        M_kg = M_grid * self.M_sun
        R_m = R_grid * self.kpc_to_m
        
        # Calculate curvatures
        curvatures = (self.G_newton * M_kg) / (self.c_light_ms**2 * R_m**3)
        
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
            'curvature_grid': curvatures,
            'mass_grid': M_grid,
            'radius_grid': R_grid
        }
        
    def explore_klein_vs_r4_critical(self, curvature_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Explore Klein field behavior across R₄_critical range
        """
        print("\n🔬 EXPLORING KLEIN FIELD vs R₄_CRITICAL")
        
        # Use typical cluster for systematic study
        M_kg = self.typical_cluster['mass_msun'] * self.M_sun
        R_m = self.typical_cluster['radius_kpc'] * self.kpc_to_m
        cluster_curvature = (self.G_newton * M_kg) / (self.c_light_ms**2 * R_m**3)
        
        print(f"   Typical cluster curvature: {cluster_curvature:.2e}")
        
        results = {
            'R4_critical_values': self.R4_critical_range,
            'cluster_curvature': cluster_curvature,
            'curvature_ratios': [],
            'phi5_amplitudes': [],
            'grav_modifications': [],
            'activation_levels': [],  # How "activated" Klein field is
            'statistical_significances': []
        }
        
        for R4_crit in self.R4_critical_range:
            # Calculate curvature ratio
            curvature_ratio = cluster_curvature / R4_crit
            
            # Klein field amplitude with saturation
            phi5_raw = self.phi5_expected_galactic * np.tanh(curvature_ratio)
            phi5_amplitude = min(phi5_raw, self.epsilon_max)
            
            # Gravitational modification
            grav_mod = self.gamma_0_grav * (phi5_amplitude / self.phi5_expected_galactic)
            
            # Activation level (how close to full activation)
            activation = phi5_amplitude / self.phi5_expected_galactic
            
            # Statistical significance (simplified model)
            phi5_std = 0.1 * self.phi5_expected_galactic
            z_score = abs(phi5_amplitude - self.phi5_expected_galactic) / (phi5_std / np.sqrt(1000))
            
            results['curvature_ratios'].append(curvature_ratio)
            results['phi5_amplitudes'].append(phi5_amplitude)
            results['grav_modifications'].append(grav_mod)
            results['activation_levels'].append(activation)
            results['statistical_significances'].append(z_score)
            
        # Convert to arrays
        for key in ['curvature_ratios', 'phi5_amplitudes', 'grav_modifications', 
                   'activation_levels', 'statistical_significances']:
            results[key] = np.array(results[key])
            
        print(f"   φ₅ amplitude range: {results['phi5_amplitudes'].min():.2e} - {results['phi5_amplitudes'].max():.2e}")
        print(f"   Activation level range: {results['activation_levels'].min():.3f} - {results['activation_levels'].max():.3f}")
        print(f"   Significance range: {results['statistical_significances'].min():.1f}σ - {results['statistical_significances'].max():.1f}σ")
        
        return results
        
    def find_optimal_r4_critical(self, klein_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Find optimal R₄_critical values for different criteria
        """
        print("\n🎯 FINDING OPTIMAL R₄_CRITICAL VALUES")
        
        R4_values = klein_results['R4_critical_values']
        phi5_values = klein_results['phi5_amplitudes']
        activation_values = klein_results['activation_levels']
        significance_values = klein_results['statistical_significances']
        
        # Criteria for "optimal" R₄_critical
        criteria = {}
        
        # 1. Maximum Klein field (but not saturated)
        non_saturated = phi5_values < self.epsilon_max * 0.95
        if np.any(non_saturated):
            max_field_idx = np.argmax(phi5_values[non_saturated])
            max_field_R4 = R4_values[non_saturated][max_field_idx]
            criteria['max_field'] = {
                'R4_critical': float(max_field_R4),
                'phi5_amplitude': float(phi5_values[non_saturated][max_field_idx]),
                'description': 'Maximum Klein field without saturation'
            }
            
        # 2. Half-activation (50% of expected galactic field)
        half_activation_target = 0.5
        half_act_idx = np.argmin(np.abs(activation_values - half_activation_target))
        criteria['half_activation'] = {
            'R4_critical': float(R4_values[half_act_idx]),
            'phi5_amplitude': float(phi5_values[half_act_idx]),
            'activation_level': float(activation_values[half_act_idx]),
            'description': '50% activation of expected galactic field'
        }
        
        # 3. Full activation (90% of expected galactic field) 
        full_activation_target = 0.9
        full_act_idx = np.argmin(np.abs(activation_values - full_activation_target))
        criteria['full_activation'] = {
            'R4_critical': float(R4_values[full_act_idx]),
            'phi5_amplitude': float(phi5_values[full_act_idx]),
            'activation_level': float(activation_values[full_act_idx]),
            'description': '90% activation of expected galactic field'
        }
        
        # 4. Optimal statistical significance (around 5σ)
        target_significance = 5.0
        optimal_sig_idx = np.argmin(np.abs(significance_values - target_significance))
        criteria['optimal_significance'] = {
            'R4_critical': float(R4_values[optimal_sig_idx]),
            'phi5_amplitude': float(phi5_values[optimal_sig_idx]),
            'significance_sigma': float(significance_values[optimal_sig_idx]),
            'description': 'Closest to 5σ statistical significance'
        }
        
        # 5. Match cluster curvature scale (curvature_ratio ~ 1)
        target_ratio = 1.0
        curvature_ratios = klein_results['curvature_ratios']
        match_curvature_idx = np.argmin(np.abs(curvature_ratios - target_ratio))
        criteria['match_curvature'] = {
            'R4_critical': float(R4_values[match_curvature_idx]),
            'phi5_amplitude': float(phi5_values[match_curvature_idx]),
            'curvature_ratio': float(curvature_ratios[match_curvature_idx]),
            'description': 'R₄_critical matches cluster curvature scale'
        }
        
        # Print results
        for name, criterion in criteria.items():
            print(f"   {criterion['description']}:")
            print(f"     R₄_critical = {criterion['R4_critical']:.2e}")
            print(f"     φ₅ amplitude = {criterion['phi5_amplitude']:.3f}")
            
        return criteria
        
    def assess_physical_consequences(self, optimal_criteria: Dict[str, Any]) -> Dict[str, Any]:
        """
        Assess physical consequences of adjusted R₄_critical values
        """
        print("\n⚖️ ASSESSING PHYSICAL CONSEQUENCES")
        
        consequences = {}
        
        for criterion_name, criterion in optimal_criteria.items():
            R4_crit = criterion['R4_critical']
            phi5_amp = criterion['phi5_amplitude']
            
            # Calculate physical implications
            
            # 1. Scaling from original R₄_critical
            original_R4 = 1e-6  # From Klein framework
            scaling_factor = R4_crit / original_R4
            
            # 2. Energy scale implications
            # If R₄ ~ GM/(c²r³), then scaling affects fundamental energy scale
            energy_scale_change = scaling_factor ** (1/3)  # Dimensional analysis
            
            # 3. Klein correlation length change
            # If Klein effects scale with R₄, correlation length changes
            original_correlation_kpc = 8.4  # kpc
            new_correlation_kpc = original_correlation_kpc * np.sqrt(scaling_factor)
            
            # 4. Required cluster properties for activation
            # What cluster mass/radius needed for curvature ~ R₄_critical?
            target_curvature = R4_crit
            # Solve: GM/(c²r³) = R₄_crit for typical cluster
            typical_mass_kg = 1e14 * self.M_sun
            required_radius_m = ((self.G_newton * typical_mass_kg) / 
                               (self.c_light_ms**2 * target_curvature)) ** (1/3)
            required_radius_kpc = required_radius_m / self.kpc_to_m
            
            consequence = {
                'criterion': criterion['description'],
                'R4_critical': R4_crit,
                'scaling_from_original': scaling_factor,
                'energy_scale_change_factor': energy_scale_change,
                'new_correlation_length_kpc': new_correlation_kpc,
                'required_cluster_radius_kpc': required_radius_kpc,
                'phi5_amplitude': phi5_amp,
                'physical_plausibility': self._assess_plausibility(R4_crit, required_radius_kpc)
            }
            
            consequences[criterion_name] = consequence
            
            print(f"   {criterion['description']}:")
            print(f"     R₄_critical scaling: {scaling_factor:.2e}× original")
            print(f"     Required cluster radius: {required_radius_kpc:.1f} kpc")
            print(f"     New correlation length: {new_correlation_kpc:.1f} kpc")
            print(f"     Physical plausibility: {consequence['physical_plausibility']}")
            
        return consequences
        
    def _assess_plausibility(self, R4_critical: float, required_radius_kpc: float) -> str:
        """
        Assess physical plausibility of R₄_critical value
        """
        
        # Check if required radius is in reasonable range for clusters
        if 10 <= required_radius_kpc <= 5000:  # 10 kpc to 5 Mpc
            radius_ok = True
        else:
            radius_ok = False
            
        # Check if R₄_critical is in reasonable range (not too extreme)
        if 1e-60 <= R4_critical <= 1e-20:
            R4_ok = True
        else:
            R4_ok = False
            
        if radius_ok and R4_ok:
            return "PLAUSIBLE"
        elif radius_ok or R4_ok:
            return "MARGINAL"
        else:
            return "IMPLAUSIBLE"
            
    def create_comprehensive_visualization(self, curvature_data: Dict[str, Any],
                                         klein_results: Dict[str, Any],
                                         optimal_criteria: Dict[str, Any],
                                         consequences: Dict[str, Any]) -> None:
        """
        Create comprehensive visualization of R₄_critical exploration
        """
        print("\n📊 CREATING COMPREHENSIVE VISUALIZATION")
        
        fig = plt.figure(figsize=(20, 15))
        
        # 1. Klein field vs R₄_critical
        ax1 = plt.subplot(2, 3, 1)
        ax1.loglog(klein_results['R4_critical_values'], klein_results['phi5_amplitudes'], 'b-', linewidth=2)
        ax1.axhline(y=self.phi5_expected_galactic, color='r', linestyle='--', alpha=0.7, label='Expected galactic φ₅')
        ax1.axhline(y=self.epsilon_max, color='k', linestyle='--', alpha=0.7, label='Topological limit')
        ax1.set_xlabel('R₄_critical')
        ax1.set_ylabel('Klein Field φ₅')
        ax1.set_title('Klein Field vs R₄_critical')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 2. Activation level vs R₄_critical
        ax2 = plt.subplot(2, 3, 2)
        ax2.semilogx(klein_results['R4_critical_values'], klein_results['activation_levels'], 'g-', linewidth=2)
        ax2.axhline(y=0.5, color='orange', linestyle='--', alpha=0.7, label='50% activation')
        ax2.axhline(y=0.9, color='red', linestyle='--', alpha=0.7, label='90% activation')
        ax2.set_xlabel('R₄_critical')
        ax2.set_ylabel('Activation Level')
        ax2.set_title('Klein Field Activation vs R₄_critical')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # 3. Statistical significance vs R₄_critical
        ax3 = plt.subplot(2, 3, 3)
        ax3.loglog(klein_results['R4_critical_values'], klein_results['statistical_significances'], 'purple', linewidth=2)
        ax3.axhline(y=3, color='orange', linestyle='--', alpha=0.7, label='3σ')
        ax3.axhline(y=5, color='red', linestyle='--', alpha=0.7, label='5σ')
        ax3.set_xlabel('R₄_critical')
        ax3.set_ylabel('Statistical Significance [σ]')
        ax3.set_title('Significance vs R₄_critical')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # 4. Curvature ratio vs R₄_critical
        ax4 = plt.subplot(2, 3, 4)
        ax4.loglog(klein_results['R4_critical_values'], klein_results['curvature_ratios'], 'brown', linewidth=2)
        ax4.axhline(y=1, color='black', linestyle='--', alpha=0.7, label='Curvature match')
        ax4.set_xlabel('R₄_critical')
        ax4.set_ylabel('Curvature Ratio')
        ax4.set_title('Curvature Ratio vs R₄_critical')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        # 5. Real curvature distribution
        ax5 = plt.subplot(2, 3, 5)
        curvatures_flat = curvature_data['curvature_grid'].flatten()
        ax5.hist(np.log10(curvatures_flat), bins=30, alpha=0.7, color='skyblue', edgecolor='black')
        ax5.set_xlabel('log₁₀(Curvature)')
        ax5.set_ylabel('Frequency')
        ax5.set_title('Real Cluster Curvature Distribution')
        ax5.grid(True, alpha=0.3)
        
        # 6. Optimal R₄_critical values
        ax6 = plt.subplot(2, 3, 6)
        criterion_names = list(optimal_criteria.keys())
        R4_values = [optimal_criteria[name]['R4_critical'] for name in criterion_names]
        phi5_values = [optimal_criteria[name]['phi5_amplitude'] for name in criterion_names]
        
        colors = ['blue', 'green', 'red', 'orange', 'purple']
        for i, (name, R4, phi5) in enumerate(zip(criterion_names, R4_values, phi5_values)):
            ax6.scatter(R4, phi5, color=colors[i], s=100, label=name.replace('_', ' '), alpha=0.7)
            
        ax6.set_xscale('log')
        ax6.set_xlabel('R₄_critical')
        ax6.set_ylabel('Klein Field φ₅')
        ax6.set_title('Optimal R₄_critical Points')
        ax6.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        ax6.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('r4_critical_exploration_1e50.png', dpi=300, bbox_inches='tight')
        print("   ✓ Saved: r4_critical_exploration_1e50.png")
        
    def run_complete_exploration(self) -> Dict[str, Any]:
        """
        Execute complete R₄_critical exploration
        """
        print("🔬 R₄_CRITICAL ~ 1e-50 EXPLORATION")
        print("=" * 50)
        print("INVESTIGATION SCOPE:")
        print("✓ Map Klein behavior in galactic curvature regime")
        print("✓ Find optimal R₄_critical for cluster physics")
        print("✓ Assess physical consequences of adjustment")
        print("✓ Determine viability of Klein in clusters")
        print("=" * 50)
        
        # 1. Calculate real curvature distribution
        print("\n1️⃣ CALCULATING REAL GALACTIC CURVATURES")
        curvature_data = self.calculate_galactic_curvature_distribution()
        
        # 2. Explore Klein vs R₄_critical
        print("\n2️⃣ EXPLORING KLEIN vs R₄_CRITICAL")
        klein_results = self.explore_klein_vs_r4_critical(curvature_data)
        
        # 3. Find optimal values
        print("\n3️⃣ FINDING OPTIMAL R₄_CRITICAL")
        optimal_criteria = self.find_optimal_r4_critical(klein_results)
        
        # 4. Assess consequences
        print("\n4️⃣ ASSESSING PHYSICAL CONSEQUENCES")
        consequences = self.assess_physical_consequences(optimal_criteria)
        
        # 5. Create visualization
        print("\n5️⃣ CREATING VISUALIZATION")
        self.create_comprehensive_visualization(curvature_data, klein_results, 
                                             optimal_criteria, consequences)
        
        # Compile results
        results = {
            'metadata': {
                'exploration_type': 'R4_CRITICAL_GALACTIC_REGIME',
                'R4_critical_range': [float(self.R4_critical_range.min()), float(self.R4_critical_range.max())],
                'motivation': 'Align Klein theory with real galactic curvatures',
                'typical_cluster': self.typical_cluster
            },
            'curvature_analysis': curvature_data,
            'klein_behavior': {
                'R4_critical_values': klein_results['R4_critical_values'].tolist(),
                'phi5_amplitudes': klein_results['phi5_amplitudes'].tolist(),
                'activation_levels': klein_results['activation_levels'].tolist(),
                'statistical_significances': klein_results['statistical_significances'].tolist()
            },
            'optimal_criteria': optimal_criteria,
            'physical_consequences': consequences,
            'scientific_assessment': self._generate_scientific_assessment(optimal_criteria, consequences)
        }
        
        return results
        
    def _generate_scientific_assessment(self, optimal_criteria: Dict[str, Any],
                                       consequences: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate scientific assessment of exploration results
        """
        
        # Count plausible solutions
        plausible_count = sum(1 for c in consequences.values() 
                            if c['physical_plausibility'] == 'PLAUSIBLE')
        total_count = len(consequences)
        
        # Find best overall solution
        best_solution = None
        best_score = -1
        
        for name, consequence in consequences.items():
            score = 0
            if consequence['physical_plausibility'] == 'PLAUSIBLE':
                score += 3
            elif consequence['physical_plausibility'] == 'MARGINAL':
                score += 1
                
            # Prefer reasonable cluster sizes
            if 100 <= consequence['required_cluster_radius_kpc'] <= 2000:
                score += 2
                
            # Prefer moderate scaling factors
            if 1e-60 <= consequence['scaling_from_original'] <= 1e-30:
                score += 1
                
            if score > best_score:
                best_score = score
                best_solution = name
                
        assessment = {
            'plausible_solutions': plausible_count,
            'total_solutions': total_count,
            'plausibility_rate': plausible_count / total_count,
            'best_solution': best_solution,
            'best_solution_details': consequences.get(best_solution, {}),
            'overall_viability': 'HIGH' if plausible_count >= 3 else 'MODERATE' if plausible_count >= 1 else 'LOW',
            'key_findings': [
                f"Plausible solutions: {plausible_count}/{total_count}",
                f"Best solution: {best_solution}",
                f"R₄_critical scaling range: {min(c['scaling_from_original'] for c in consequences.values()):.2e} - {max(c['scaling_from_original'] for c in consequences.values()):.2e}"
            ]
        }
        
        return assessment

def main():
    """Execute R₄_critical exploration"""
    
    import os
    os.chdir('/mnt/d/Multidimensional Theory Simulations/multidimensional-theory/gravitational-wave-echoes-5d/EMPIRICAL_KLEIN_STUDIES/10_Galaxy_Clusters_Analysis')
    
    # Suppress warnings
    warnings.filterwarnings('ignore')
    
    # Initialize exploration
    explorer = R4CriticalExploration()
    
    # Run exploration
    results = explorer.run_complete_exploration()
    
    # Save results
    with open('r4_critical_exploration_1e50_results.json', 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\n💾 Results saved to: r4_critical_exploration_1e50_results.json")
    print(f"📊 Visualization saved to: r4_critical_exploration_1e50.png")
    
    assessment = results['scientific_assessment']
    print(f"\n🎯 EXPLORATION COMPLETE!")
    print(f"   Overall viability: {assessment['overall_viability']}")
    print(f"   Plausible solutions: {assessment['plausible_solutions']}/{assessment['total_solutions']}")
    print(f"   Best solution: {assessment['best_solution']}")
    
    if assessment['best_solution']:
        best = assessment['best_solution_details']
        print(f"   Best R₄_critical: {best['R4_critical']:.2e}")
        print(f"   Required cluster radius: {best['required_cluster_radius_kpc']:.1f} kpc")
        print(f"   Physical plausibility: {best['physical_plausibility']}")
    
    return results

if __name__ == "__main__":
    results = main()