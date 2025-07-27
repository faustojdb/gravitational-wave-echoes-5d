#!/usr/bin/env python3
"""
KLEIN PARAMETER SPACE STUDY
===========================

SYSTEMATIC INVESTIGATION OF KLEIN FIELD BEHAVIOR:
1. Map Klein field vs physical scales (mass, radius, density)
2. Study statistical significance vs parameters  
3. Identify divergence regions (σ → ∞)
4. Determine optimal physical scales from first principles
5. NO AD HOC FIXES - Pure parameter space exploration

GOAL: Understand where Klein theory is well-behaved vs pathological
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats
from typing import Dict, Any, Tuple
import warnings
import json

class KleinParameterSpaceStudy:
    """
    Systematic study of Klein parameter space behavior
    """
    
    def __init__(self):
        # Klein fundamental constants
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
        
        # Parameter ranges to explore
        self.mass_range_msun = np.logspace(12, 16, 50)  # 10¹² to 10¹⁶ M☉
        self.radius_range_kpc = np.logspace(-1, 4, 50)  # 0.1 to 10⁴ kpc
        self.R4_critical_range = np.logspace(-12, 0, 50)  # 10⁻¹² to 1
        
    def calculate_klein_field_grid(self, masses_msun: np.ndarray, 
                                  radii_kpc: np.ndarray,
                                  R4_critical: float = 1e-6) -> Dict[str, np.ndarray]:
        """
        Calculate Klein field on parameter grid
        """
        
        # Create meshgrids
        M_grid, R_grid = np.meshgrid(masses_msun, radii_kpc)
        
        # Convert to physical units
        M_kg = M_grid * self.M_sun
        R_m = R_grid * self.kpc_to_m
        
        # Calculate spacetime curvature
        curvature_4d = (self.G_newton * M_kg) / (self.c_light_ms**2 * R_m**3)
        
        # Klein field amplitude with saturation
        curvature_ratio = curvature_4d / R4_critical
        phi5_amplitude = self.phi5_expected_galactic * np.tanh(curvature_ratio)
        phi5_amplitude = np.minimum(phi5_amplitude, self.epsilon_max)
        
        # Gravitational modification
        grav_modification = self.gamma_0_grav * (phi5_amplitude / self.phi5_expected_galactic)
        
        return {
            'mass_grid': M_grid,
            'radius_grid': R_grid,
            'curvature_4d': curvature_4d,
            'curvature_ratio': curvature_ratio,
            'phi5_amplitude': phi5_amplitude,
            'grav_modification': grav_modification
        }
        
    def calculate_statistical_significance_grid(self, phi5_grid: np.ndarray, 
                                              n_clusters: int = 1000) -> np.ndarray:
        """
        Calculate statistical significance for each point in parameter grid
        """
        
        significance_grid = np.zeros_like(phi5_grid)
        
        for i in range(phi5_grid.shape[0]):
            for j in range(phi5_grid.shape[1]):
                phi5_value = phi5_grid[i, j]
                
                # Simulate measurement with realistic scatter
                phi5_expected = self.phi5_expected_galactic
                phi5_std = 0.1 * phi5_expected  # 10% measurement uncertainty
                
                # Calculate z-score
                if phi5_std > 0:
                    z_score = abs(phi5_value - phi5_expected) / (phi5_std / np.sqrt(n_clusters))
                    significance_grid[i, j] = z_score
                else:
                    # Handle perfect measurements (leads to infinite significance)
                    significance_grid[i, j] = np.inf if phi5_value != phi5_expected else 0
                    
        return significance_grid
        
    def study_R4_critical_dependence(self) -> Dict[str, Any]:
        """
        Study how Klein behavior depends on R₄_critical parameter
        """
        
        print("🔬 STUDYING R₄_CRITICAL DEPENDENCE")
        
        # Fixed test case: typical cluster
        test_mass_msun = 1e14
        test_radius_kpc = 1000  # 1 Mpc
        
        results = {
            'R4_critical_values': self.R4_critical_range,
            'phi5_amplitudes': [],
            'curvature_ratios': [],
            'significances': []
        }
        
        for R4_crit in self.R4_critical_range:
            # Calculate for test cluster
            M_kg = test_mass_msun * self.M_sun
            R_m = test_radius_kpc * self.kpc_to_m
            
            curvature_4d = (self.G_newton * M_kg) / (self.c_light_ms**2 * R_m**3)
            curvature_ratio = curvature_4d / R4_crit
            
            phi5_amplitude = self.phi5_expected_galactic * np.tanh(curvature_ratio)
            phi5_amplitude = min(phi5_amplitude, self.epsilon_max)
            
            # Statistical significance
            phi5_std = 0.1 * self.phi5_expected_galactic
            z_score = abs(phi5_amplitude - self.phi5_expected_galactic) / (phi5_std / np.sqrt(1000))
            
            results['phi5_amplitudes'].append(phi5_amplitude)
            results['curvature_ratios'].append(curvature_ratio)
            results['significances'].append(z_score)
            
        results['phi5_amplitudes'] = np.array(results['phi5_amplitudes'])
        results['curvature_ratios'] = np.array(results['curvature_ratios'])
        results['significances'] = np.array(results['significances'])
        
        print(f"   φ₅ range: {results['phi5_amplitudes'].min():.2e} - {results['phi5_amplitudes'].max():.2e}")
        print(f"   Curvature ratio range: {results['curvature_ratios'].min():.2e} - {results['curvature_ratios'].max():.2e}")
        print(f"   Significance range: {results['significances'].min():.2e} - {results['significances'].max():.2e}")
        
        return results
        
    def identify_pathological_regions(self, grid_data: Dict[str, np.ndarray],
                                    significance_grid: np.ndarray) -> Dict[str, Any]:
        """
        Identify regions where Klein theory becomes pathological
        """
        
        print("⚠️ IDENTIFYING PATHOLOGICAL REGIONS")
        
        # Define pathology criteria
        criteria = {
            'infinite_significance': significance_grid == np.inf,
            'zero_field': grid_data['phi5_amplitude'] == 0.0,
            'saturated_field': grid_data['phi5_amplitude'] >= self.epsilon_max * 0.99,
            'extreme_curvature': grid_data['curvature_4d'] > 1e-40,
            'extreme_significance': significance_grid > 1000  # > 1000σ
        }
        
        # Count pathological points
        pathology_stats = {}
        total_points = significance_grid.size
        
        for name, mask in criteria.items():
            count = np.sum(mask)
            percentage = count / total_points * 100
            pathology_stats[name] = {
                'count': int(count),
                'percentage': percentage
            }
            print(f"   {name}: {count}/{total_points} ({percentage:.1f}%)")
            
        # Find well-behaved regions
        well_behaved = (
            (significance_grid > 2) & (significance_grid < 100) &  # 2σ < significance < 100σ
            (grid_data['phi5_amplitude'] > 0.01) &  # Non-zero field
            (grid_data['phi5_amplitude'] < self.epsilon_max * 0.9)  # Not saturated
        )
        
        well_behaved_count = np.sum(well_behaved)
        well_behaved_percentage = well_behaved_count / total_points * 100
        
        print(f"   WELL-BEHAVED REGIONS: {well_behaved_count}/{total_points} ({well_behaved_percentage:.1f}%)")
        
        return {
            'pathology_statistics': pathology_stats,
            'well_behaved_count': int(well_behaved_count),
            'well_behaved_percentage': well_behaved_percentage,
            'well_behaved_mask': well_behaved
        }
        
    def find_optimal_physical_scales(self, grid_data: Dict[str, np.ndarray],
                                    significance_grid: np.ndarray,
                                    well_behaved_mask: np.ndarray) -> Dict[str, Any]:
        """
        Find optimal physical scales from well-behaved regions
        """
        
        print("🎯 FINDING OPTIMAL PHYSICAL SCALES")
        
        if not np.any(well_behaved_mask):
            print("   ⚠️ NO WELL-BEHAVED REGIONS FOUND!")
            return {'status': 'NO_SOLUTION'}
            
        # Extract well-behaved points
        wb_masses = grid_data['mass_grid'][well_behaved_mask]
        wb_radii = grid_data['radius_grid'][well_behaved_mask]
        wb_phi5 = grid_data['phi5_amplitude'][well_behaved_mask]
        wb_significance = significance_grid[well_behaved_mask]
        
        # Find optimal ranges
        optimal_scales = {
            'mass_range_msun': [float(wb_masses.min()), float(wb_masses.max())],
            'radius_range_kpc': [float(wb_radii.min()), float(wb_radii.max())],
            'phi5_range': [float(wb_phi5.min()), float(wb_phi5.max())],
            'significance_range': [float(wb_significance.min()), float(wb_significance.max())],
            'n_solutions': len(wb_masses)
        }
        
        # Find peak significance point
        max_sig_idx = np.argmax(wb_significance)
        optimal_point = {
            'mass_msun': float(wb_masses[max_sig_idx]),
            'radius_kpc': float(wb_radii[max_sig_idx]),
            'phi5_amplitude': float(wb_phi5[max_sig_idx]),
            'significance_sigma': float(wb_significance[max_sig_idx])
        }
        
        print(f"   Optimal mass range: {optimal_scales['mass_range_msun'][0]:.2e} - {optimal_scales['mass_range_msun'][1]:.2e} M☉")
        print(f"   Optimal radius range: {optimal_scales['radius_range_kpc'][0]:.2f} - {optimal_scales['radius_range_kpc'][1]:.2f} kpc")
        print(f"   Peak significance point: M={optimal_point['mass_msun']:.2e} M☉, R={optimal_point['radius_kpc']:.2f} kpc")
        print(f"   Peak significance: {optimal_point['significance_sigma']:.1f}σ")
        
        return {
            'status': 'SUCCESS',
            'optimal_scales': optimal_scales,
            'optimal_point': optimal_point
        }
        
    def create_visualization(self, grid_data: Dict[str, np.ndarray],
                           significance_grid: np.ndarray,
                           R4_dependence: Dict[str, Any],
                           pathology_data: Dict[str, Any]) -> None:
        """
        Create comprehensive visualization of parameter space
        """
        
        print("📊 CREATING PARAMETER SPACE VISUALIZATION")
        
        fig = plt.figure(figsize=(20, 15))
        
        # 1. Klein field amplitude map
        ax1 = plt.subplot(2, 3, 1)
        im1 = ax1.contourf(grid_data['mass_grid'], grid_data['radius_grid'], 
                          grid_data['phi5_amplitude'], levels=50, cmap='viridis')
        ax1.set_xscale('log')
        ax1.set_yscale('log')
        ax1.set_xlabel('Mass [M☉]')
        ax1.set_ylabel('Radius [kpc]')
        ax1.set_title('Klein Field Amplitude φ₅')
        plt.colorbar(im1, ax=ax1)
        
        # 2. Statistical significance map
        ax2 = plt.subplot(2, 3, 2)
        # Cap significance for visualization
        sig_plot = np.minimum(significance_grid, 1000)
        im2 = ax2.contourf(grid_data['mass_grid'], grid_data['radius_grid'], 
                          sig_plot, levels=50, cmap='plasma')
        ax2.set_xscale('log')
        ax2.set_yscale('log')
        ax2.set_xlabel('Mass [M☉]')
        ax2.set_ylabel('Radius [kpc]')
        ax2.set_title('Statistical Significance [σ]')
        plt.colorbar(im2, ax=ax2)
        
        # 3. Curvature map
        ax3 = plt.subplot(2, 3, 3)
        im3 = ax3.contourf(grid_data['mass_grid'], grid_data['radius_grid'], 
                          np.log10(grid_data['curvature_4d'] + 1e-100), levels=50, cmap='coolwarm')
        ax3.set_xscale('log')
        ax3.set_yscale('log')
        ax3.set_xlabel('Mass [M☉]')
        ax3.set_ylabel('Radius [kpc]')
        ax3.set_title('log₁₀(Spacetime Curvature)')
        plt.colorbar(im3, ax=ax3)
        
        # 4. R₄_critical dependence
        ax4 = plt.subplot(2, 3, 4)
        ax4.loglog(R4_dependence['R4_critical_values'], R4_dependence['phi5_amplitudes'], 'b-', linewidth=2)
        ax4.set_xlabel('R₄_critical')
        ax4.set_ylabel('Klein Field φ₅')
        ax4.set_title('Klein Field vs R₄_critical')
        ax4.grid(True)
        
        # 5. Significance vs R₄_critical  
        ax5 = plt.subplot(2, 3, 5)
        ax5.loglog(R4_dependence['R4_critical_values'], R4_dependence['significances'], 'r-', linewidth=2)
        ax5.set_xlabel('R₄_critical')
        ax5.set_ylabel('Statistical Significance [σ]')
        ax5.set_title('Significance vs R₄_critical')
        ax5.grid(True)
        
        # 6. Well-behaved regions
        ax6 = plt.subplot(2, 3, 6)
        if 'well_behaved_mask' in pathology_data:
            ax6.contourf(grid_data['mass_grid'], grid_data['radius_grid'], 
                        pathology_data['well_behaved_mask'].astype(int), 
                        levels=[0, 0.5, 1], colors=['red', 'green'], alpha=0.7)
        ax6.set_xscale('log')
        ax6.set_yscale('log')
        ax6.set_xlabel('Mass [M☉]')
        ax6.set_ylabel('Radius [kpc]')
        ax6.set_title('Well-Behaved Regions (Green)')
        
        plt.tight_layout()
        plt.savefig('klein_parameter_space_study.png', dpi=300, bbox_inches='tight')
        print("   ✓ Saved: klein_parameter_space_study.png")
        
    def run_complete_study(self) -> Dict[str, Any]:
        """
        Execute complete Klein parameter space study
        """
        
        print("🔬 KLEIN PARAMETER SPACE STUDY")
        print("=" * 50)
        print("SYSTEMATIC INVESTIGATION:")
        print("✓ Map Klein field vs physical scales")
        print("✓ Study statistical significance vs parameters")
        print("✓ Identify divergence regions")
        print("✓ Find optimal scales from first principles")
        print("=" * 50)
        
        # 1. Calculate Klein field on parameter grid
        print("\n1️⃣ CALCULATING KLEIN FIELD GRID")
        grid_data = self.calculate_klein_field_grid(self.mass_range_msun, self.radius_range_kpc)
        
        # 2. Calculate statistical significance grid
        print("\n2️⃣ CALCULATING SIGNIFICANCE GRID")
        significance_grid = self.calculate_statistical_significance_grid(grid_data['phi5_amplitude'])
        
        # 3. Study R₄_critical dependence
        print("\n3️⃣ STUDYING R₄_CRITICAL DEPENDENCE")
        R4_dependence = self.study_R4_critical_dependence()
        
        # 4. Identify pathological regions
        print("\n4️⃣ IDENTIFYING PATHOLOGICAL REGIONS")
        pathology_data = self.identify_pathological_regions(grid_data, significance_grid)
        
        # 5. Find optimal physical scales
        print("\n5️⃣ FINDING OPTIMAL SCALES")
        optimal_scales = self.find_optimal_physical_scales(grid_data, significance_grid, 
                                                          pathology_data['well_behaved_mask'])
        
        # 6. Create visualization
        print("\n6️⃣ CREATING VISUALIZATION")
        self.create_visualization(grid_data, significance_grid, R4_dependence, pathology_data)
        
        # Compile results
        results = {
            'metadata': {
                'study_type': 'KLEIN_PARAMETER_SPACE_EXPLORATION',
                'parameter_ranges': {
                    'mass_range_msun': [float(self.mass_range_msun.min()), float(self.mass_range_msun.max())],
                    'radius_range_kpc': [float(self.radius_range_kpc.min()), float(self.radius_range_kpc.max())],
                    'R4_critical_range': [float(self.R4_critical_range.min()), float(self.R4_critical_range.max())]
                },
                'grid_resolution': f"{len(self.mass_range_msun)} × {len(self.radius_range_kpc)}"
            },
            'klein_fundamentals': {
                'f0_Hz': self.f0_Hz,
                'R_Klein_m': self.R_Klein_m,
                'epsilon_max': self.epsilon_max,
                'gamma_0_grav': self.gamma_0_grav,
                'phi5_expected_galactic': self.phi5_expected_galactic
            },
            'grid_statistics': {
                'phi5_range': [float(grid_data['phi5_amplitude'].min()), float(grid_data['phi5_amplitude'].max())],
                'significance_range': [float(significance_grid.min()), float(significance_grid.max())],
                'curvature_range': [float(grid_data['curvature_4d'].min()), float(grid_data['curvature_4d'].max())]
            },
            'R4_critical_study': R4_dependence,
            'pathology_analysis': pathology_data,
            'optimal_scales': optimal_scales,
            'conclusions': {
                'well_behaved_percentage': pathology_data['well_behaved_percentage'],
                'optimal_solution_exists': optimal_scales.get('status') == 'SUCCESS',
                'divergence_regions_identified': True,
                'key_findings': [
                    f"Well-behaved regions: {pathology_data['well_behaved_percentage']:.1f}% of parameter space",
                    f"Klein field range: {grid_data['phi5_amplitude'].min():.2e} - {grid_data['phi5_amplitude'].max():.2e}",
                    f"Significance range: {significance_grid.min():.2e} - {significance_grid.max():.2e}σ"
                ]
            }
        }
        
        return results

def main():
    """Execute Klein parameter space study"""
    
    import os
    os.chdir('/mnt/d/Multidimensional Theory Simulations/multidimensional-theory/gravitational-wave-echoes-5d/EMPIRICAL_KLEIN_STUDIES/10_Galaxy_Clusters_Analysis')
    
    # Suppress warnings for cleaner output
    warnings.filterwarnings('ignore')
    
    # Initialize study
    study = KleinParameterSpaceStudy()
    
    # Run complete study
    results = study.run_complete_study()
    
    # Save results
    with open('klein_parameter_space_study_results.json', 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\n💾 Results saved to: klein_parameter_space_study_results.json")
    print(f"📊 Visualization saved to: klein_parameter_space_study.png")
    
    print(f"\n🎯 PARAMETER SPACE STUDY COMPLETE!")
    print(f"   Well-behaved regions: {results['pathology_analysis']['well_behaved_percentage']:.1f}%")
    if results['optimal_scales']['status'] == 'SUCCESS':
        optimal = results['optimal_scales']['optimal_point']
        print(f"   Optimal scales found: M={optimal['mass_msun']:.2e} M☉, R={optimal['radius_kpc']:.2f} kpc")
        print(f"   Peak significance: {optimal['significance_sigma']:.1f}σ")
    else:
        print(f"   ⚠️ No optimal scales found in parameter space")
    
    return results

if __name__ == "__main__":
    results = main()