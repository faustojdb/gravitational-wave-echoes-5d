#!/usr/bin/env python3
"""
Cosmological Expansion Effects on Extra-Dimensional Topologies
============================================================

This analysis addresses a critical missing component: How does the expansion
of spacetime affect extra-dimensional geometries and their gravitational
wave echo signatures?

Key considerations:
1. Hubble parameter H₀ = 67.4 ± 0.5 km/s/Mpc (Planck 2018)
2. Do extra dimensions expand with 4D spacetime?
3. Time-dependent geometric factors
4. Redshift effects on echo frequencies
5. Evolution of coupling strength over cosmic time

Physical scenarios:
A) Extra dimensions expand with 4D space → R(t) ∝ a(t)
B) Extra dimensions are stabilized → R(t) = constant
C) Mixed expansion → different scaling laws
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from typing import Dict, List, Tuple
import json
from datetime import datetime

class CosmologicalExpansionAnalysis:
    """
    Analyze how cosmic expansion affects extra-dimensional echo signatures.
    """
    
    def __init__(self):
        """Initialize with current cosmological parameters."""
        
        # Planck 2018 cosmological parameters
        self.H0 = 67.4  # km/s/Mpc (Hubble constant today)
        self.H0_si = self.H0 * 1000 / (3.086e22)  # Convert to SI (1/s)
        
        self.Omega_m = 0.315  # Matter density parameter
        self.Omega_lambda = 0.685  # Dark energy density parameter
        self.Omega_r = 9.2e-5  # Radiation density parameter
        
        # Age of universe
        self.t_universe = 13.8e9 * 365.25 * 24 * 3600  # seconds
        
        # GW event parameters
        self.z_gw150914 = 0.09  # Redshift of GW150914
        self.z_typical = 0.1  # Typical GW event redshift
        
        print("COSMOLOGICAL EXPANSION ANALYSIS")
        print("="*60)
        print(f"H₀ = {self.H0:.1f} ± 0.5 km/s/Mpc (Planck 2018)")
        print(f"Ωₘ = {self.Omega_m:.3f}")
        print(f"Ωₗ = {self.Omega_lambda:.3f}")
        print(f"Age of universe = {self.t_universe/(365.25*24*3600*1e9):.1f} Gyr")
        
    def hubble_parameter(self, z: float) -> float:
        """
        Calculate Hubble parameter H(z) at redshift z.
        
        H(z) = H₀ √[Ωₘ(1+z)³ + Ωₗ + Ωᵣ(1+z)⁴]
        """
        factor = (self.Omega_m * (1 + z)**3 + 
                 self.Omega_lambda + 
                 self.Omega_r * (1 + z)**4)
        
        return self.H0 * np.sqrt(factor)
    
    def scale_factor_evolution(self, z_max: float = 5.0) -> Tuple[np.ndarray, np.ndarray]:
        """
        Calculate scale factor evolution a(t) from z=z_max to z=0.
        """
        z_values = np.linspace(z_max, 0, 1000)
        a_values = 1 / (1 + z_values)
        
        # Calculate lookback times
        def integrand(z):
            return 1 / ((1 + z) * self.hubble_parameter(z))
        
        # Numerical integration for cosmic time
        times = np.zeros_like(z_values)
        for i, z in enumerate(z_values):
            if z > 0:
                # Lookback time integral
                z_int = np.linspace(0, z, 100)
                integrand_vals = [integrand(zi) for zi in z_int]
                times[i] = np.trapz(integrand_vals, z_int) * (3.086e22 / 1000)  # Convert to seconds
        
        times = self.t_universe - times  # Convert lookback to cosmic time
        
        return times, a_values
    
    def extra_dimension_scenarios(self) -> Dict[str, callable]:
        """
        Define different scenarios for extra-dimensional evolution.
        """
        
        scenarios = {
            'coexpanding': lambda a: a,  # R_5D(t) ∝ a(t)
            'stabilized': lambda a: np.ones_like(a),  # R_5D = constant  
            'logarithmic': lambda a: np.log(a + 1) + 1,  # Slow expansion
            'power_law_half': lambda a: np.sqrt(a),  # R_5D ∝ √a(t)
            'inverse': lambda a: 1/np.sqrt(a),  # Contracting extra dimensions
        }
        
        return scenarios
    
    def calculate_geometric_factor_evolution(self, scenario: str = 'coexpanding') -> Dict[str, any]:
        """
        Calculate how geometric factors evolve with cosmic expansion.
        """
        print(f"\nCalculating factor evolution for scenario: {scenario}")
        
        # Get scale factor evolution
        times, a_values = self.scale_factor_evolution()
        
        # Get scenario function
        scenarios = self.extra_dimension_scenarios()
        R_evolution = scenarios[scenario](a_values)
        
        # Current geometric factors (rigorous)
        current_factors = {
            'Klein_Bottle': 3.142,  # π
            'Twisted_Torus': 1.061,
            'Mobius_Band': 0.916,
            'Real_Projective_Plane': 0.707,
            'String_Orientifold': 0.417
        }
        
        # Factor evolution depends on how R_5D changes
        evolution_data = {}
        
        for topology, current_factor in current_factors.items():
            
            if scenario == 'coexpanding':
                # If R_5D ∝ a(t), then frequencies scale as f ∝ 1/a(t)
                # Geometric factor might scale as R_5D itself
                factor_evolution = current_factor * R_evolution
                
            elif scenario == 'stabilized':
                # R_5D constant → factors constant
                factor_evolution = current_factor * np.ones_like(a_values)
                
            elif scenario == 'logarithmic':
                # Slow expansion
                factor_evolution = current_factor * R_evolution
                
            elif scenario == 'power_law_half':
                # R_5D ∝ √a(t)
                factor_evolution = current_factor * R_evolution
                
            elif scenario == 'inverse':
                # Contracting extra dimensions
                factor_evolution = current_factor * R_evolution
                
            evolution_data[topology] = {
                'times': times,
                'scale_factors': a_values,
                'R_5D_evolution': R_evolution,
                'factor_evolution': factor_evolution,
                'current_factor': current_factor,
                'final_factor': factor_evolution[-1]
            }
        
        return evolution_data
    
    def redshift_effects_on_echoes(self, z: float) -> Dict[str, float]:
        """
        Calculate how redshift affects observed echo properties.
        """
        print(f"\nCalculating redshift effects for z = {z:.3f}")
        
        # Frequency redshift: f_observed = f_emitted / (1 + z)
        frequency_redshift = 1 / (1 + z)
        
        # Time dilation: Δt_observed = Δt_emitted × (1 + z)
        time_dilation = 1 + z
        
        # Luminosity distance effects on amplitude
        # d_L ∝ (1+z) for small z, affects amplitude as A ∝ 1/d_L
        d_L_factor = 1 + z  # Simplified for small z
        amplitude_suppression = 1 / d_L_factor
        
        # Volume expansion between emission and observation
        volume_expansion = (1 + z)**3
        
        return {
            'frequency_redshift': frequency_redshift,
            'time_dilation': time_dilation,
            'amplitude_suppression': amplitude_suppression,
            'volume_expansion': volume_expansion,
            'hubble_at_z': self.hubble_parameter(z)
        }
    
    def corrected_echo_predictions(self, topology: str, mass: float, 
                                 redshift: float, scenario: str = 'stabilized') -> Dict[str, float]:
        """
        Calculate echo predictions including cosmological corrections.
        """
        
        # Base geometric factors (current epoch)
        base_factors = {
            'Klein_Bottle': 3.142,
            'Twisted_Torus': 1.061,
            'Mobius_Band': 0.916,
            'Real_Projective_Plane': 0.707,
            'String_Orientifold': 0.417
        }
        
        # Get redshift effects
        z_effects = self.redshift_effects_on_echoes(redshift)
        
        # Get factor evolution for this scenario
        evolution = self.calculate_geometric_factor_evolution(scenario)
        
        # Factor at emission redshift (approximate)
        # For small z, can use linear approximation
        if scenario == 'coexpanding':
            factor_at_emission = base_factors[topology] / (1 + redshift)
        elif scenario == 'stabilized':
            factor_at_emission = base_factors[topology]
        else:
            # Use current factor as approximation
            factor_at_emission = base_factors[topology]
        
        # Base echo time (local, no cosmological effects)
        if topology == 'Klein_Bottle':
            tau_local = 2.574 * mass**(-0.826) + 0.273
        else:
            # Scale from Klein bottle
            factor_ratio = factor_at_emission / base_factors['Klein_Bottle']
            tau_klein = 2.574 * mass**(-0.826) + 0.273
            tau_local = tau_klein * factor_ratio
        
        # Apply cosmological corrections
        tau_observed = tau_local * z_effects['time_dilation']
        
        # Frequency corrections
        if topology == 'Klein_Bottle':
            f_local = 6.65  # Hz
        elif topology == 'Real_Projective_Plane':
            f_local = 4.19
        elif topology == 'Mobius_Band':
            f_local = 8.2
        elif topology == 'Twisted_Torus':
            f_local = 5.68
        elif topology == 'String_Orientifold':
            f_local = 6.8
        
        f_observed = f_local * z_effects['frequency_redshift']
        
        # Amplitude corrections
        amplitude_factor = (factor_at_emission / base_factors[topology]) * z_effects['amplitude_suppression']
        
        return {
            'tau_local': tau_local,
            'tau_observed': tau_observed,
            'f_local': f_local,
            'f_observed': f_observed,
            'factor_at_emission': factor_at_emission,
            'amplitude_factor': amplitude_factor,
            'redshift_effects': z_effects
        }
    
    def compare_expansion_scenarios(self) -> Dict[str, any]:
        """
        Compare different expansion scenarios for their observational impact.
        """
        print("\n" + "="*60)
        print("COMPARING EXPANSION SCENARIOS")
        print("="*60)
        
        scenarios = ['stabilized', 'coexpanding', 'logarithmic', 'power_law_half']
        test_masses = [30, 62, 100]  # Solar masses
        test_redshifts = [0.01, 0.1, 0.5]  # Range of GW event redshifts
        
        comparison = {}
        
        for scenario in scenarios:
            print(f"\nScenario: {scenario}")
            
            scenario_data = {
                'description': self.get_scenario_description(scenario),
                'predictions': {}
            }
            
            for topology in ['Klein_Bottle', 'Real_Projective_Plane']:
                
                topology_predictions = {}
                
                for z in test_redshifts:
                    for M in test_masses:
                        
                        prediction = self.corrected_echo_predictions(
                            topology, M, z, scenario
                        )
                        
                        key = f'z_{z}_M_{M}'
                        topology_predictions[key] = {
                            'tau_observed': prediction['tau_observed'],
                            'f_observed': prediction['f_observed'],
                            'amplitude_factor': prediction['amplitude_factor']
                        }
                
                scenario_data['predictions'][topology] = topology_predictions
            
            comparison[scenario] = scenario_data
        
        return comparison
    
    def get_scenario_description(self, scenario: str) -> str:
        """Get physical description of expansion scenario."""
        
        descriptions = {
            'stabilized': 'Extra dimensions stabilized by moduli fields (R_5D = constant)',
            'coexpanding': 'Extra dimensions expand with 4D space (R_5D ∝ a(t))',
            'logarithmic': 'Slow extra-dimensional expansion (R_5D ∝ ln(a))',
            'power_law_half': 'Moderate expansion (R_5D ∝ √a(t))',
            'inverse': 'Contracting extra dimensions (R_5D ∝ 1/√a(t))'
        }
        
        return descriptions.get(scenario, 'Unknown scenario')
    
    def plot_expansion_effects(self, save_path: str = None):
        """
        Visualize cosmological expansion effects.
        """
        print("\nGenerating expansion effects plot...")
        
        # Get evolution for different scenarios
        scenarios = ['stabilized', 'coexpanding', 'logarithmic']
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
        
        colors = ['blue', 'red', 'green']
        
        # Plot 1: Scale factor evolution
        times, a_values = self.scale_factor_evolution()
        times_gyr = times / (365.25 * 24 * 3600 * 1e9)  # Convert to Gyr
        
        ax1.plot(times_gyr, a_values, 'k-', linewidth=2, label='4D scale factor a(t)')
        ax1.set_xlabel('Cosmic time (Gyr)')
        ax1.set_ylabel('Scale factor')
        ax1.set_title('4D Scale Factor Evolution')
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        
        # Plot 2: Extra dimension evolution
        for i, scenario in enumerate(scenarios):
            evolution = self.calculate_geometric_factor_evolution(scenario)
            klein_data = evolution['Klein_Bottle']
            
            ax2.plot(times_gyr, klein_data['R_5D_evolution'], 
                    color=colors[i], linewidth=2, label=f'{scenario} R_5D(t)')
        
        ax2.set_xlabel('Cosmic time (Gyr)')
        ax2.set_ylabel('Extra dimension size (normalized)')
        ax2.set_title('Extra Dimension Evolution Scenarios')
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        
        # Plot 3: Klein bottle factor evolution
        for i, scenario in enumerate(scenarios):
            evolution = self.calculate_geometric_factor_evolution(scenario)
            klein_data = evolution['Klein_Bottle']
            
            ax3.plot(times_gyr, klein_data['factor_evolution'], 
                    color=colors[i], linewidth=2, label=f'{scenario}')
        
        ax3.axhline(y=3.142, color='black', linestyle='--', alpha=0.7, label='π (current)')
        ax3.set_xlabel('Cosmic time (Gyr)')
        ax3.set_ylabel('Klein Bottle Geometric Factor')
        ax3.set_title('Geometric Factor Evolution')
        ax3.grid(True, alpha=0.3)
        ax3.legend()
        
        # Plot 4: Redshift effects on observables
        redshifts = np.linspace(0, 1, 100)
        freq_factors = [self.redshift_effects_on_echoes(z)['frequency_redshift'] for z in redshifts]
        time_factors = [self.redshift_effects_on_echoes(z)['time_dilation'] for z in redshifts]
        
        ax4.plot(redshifts, freq_factors, 'b-', linewidth=2, label='Frequency: f_obs/f_emit')
        ax4.plot(redshifts, time_factors, 'r-', linewidth=2, label='Time: τ_obs/τ_emit')
        ax4.set_xlabel('Redshift z')
        ax4.set_ylabel('Correction factor')
        ax4.set_title('Redshift Effects on Observables')
        ax4.grid(True, alpha=0.3)
        ax4.legend()
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Plot saved to: {save_path}")
        
        plt.close()
        return True

def main():
    """
    Analyze cosmological expansion effects on extra-dimensional echoes.
    """
    print("COSMOLOGICAL EXPANSION EFFECTS ON EXTRA-DIMENSIONAL ECHOES")
    print("="*80)
    
    # Initialize analysis
    cosmo = CosmologicalExpansionAnalysis()
    
    # Compare expansion scenarios
    scenario_comparison = cosmo.compare_expansion_scenarios()
    
    # Calculate specific predictions for GW150914
    print("\n" + "="*60)
    print("GW150914 CORRECTED PREDICTIONS")
    print("="*60)
    
    gw150914_mass = 62.0  # Solar masses
    gw150914_redshift = 0.09
    
    for scenario in ['stabilized', 'coexpanding']:
        print(f"\nScenario: {scenario}")
        
        for topology in ['Klein_Bottle', 'Real_Projective_Plane']:
            prediction = cosmo.corrected_echo_predictions(
                topology, gw150914_mass, gw150914_redshift, scenario
            )
            
            print(f"  {topology}:")
            print(f"    τ_local = {prediction['tau_local']:.3f} s")
            print(f"    τ_observed = {prediction['tau_observed']:.3f} s")
            print(f"    f_local = {prediction['f_local']:.1f} Hz")
            print(f"    f_observed = {prediction['f_observed']:.1f} Hz")
            print(f"    Factor at emission = {prediction['factor_at_emission']:.3f}")
    
    # Generate visualization
    plot_path = "../Results/cosmological_expansion_effects.png"
    cosmo.plot_expansion_effects(save_path=plot_path)
    
    # Save comprehensive results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    output = {
        'analysis_type': 'Cosmological Expansion Effects on Extra-Dimensional Echoes',
        'timestamp': timestamp,
        'cosmological_parameters': {
            'H0_km_s_Mpc': cosmo.H0,
            'Omega_m': cosmo.Omega_m,
            'Omega_lambda': cosmo.Omega_lambda,
            'universe_age_Gyr': cosmo.t_universe / (365.25 * 24 * 3600 * 1e9)
        },
        'scenario_comparison': scenario_comparison,
        'key_findings': [
            'Stabilized extra dimensions: Most conservative scenario',
            'Coexpanding dimensions: Factors scale with cosmic expansion', 
            'Redshift effects: Time dilation increases observed echo times',
            'Frequency effects: Observed frequencies decreased by (1+z)',
            'GW150914 corrections: Modest for z=0.09 but important for precision'
        ]
    }
    
    results_file = f"../Results/cosmological_expansion_analysis_{timestamp}.json"
    with open(results_file, 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"\n✅ Cosmological analysis complete!")
    print(f"Results saved to: {results_file}")
    print(f"Plot saved to: {plot_path}")
    
    print(f"\n🌌 KEY COSMOLOGICAL INSIGHTS:")
    print(f"1. Stabilized extra dimensions → factors remain constant")
    print(f"2. Coexpanding dimensions → factors evolve as a(t)")
    print(f"3. Redshift effects → observable corrections for z > 0.1")
    print(f"4. Time dilation → echo times increased by (1+z)")
    print(f"5. Frequency redshift → search frequencies need z-correction")
    
    return output

if __name__ == "__main__":
    main()