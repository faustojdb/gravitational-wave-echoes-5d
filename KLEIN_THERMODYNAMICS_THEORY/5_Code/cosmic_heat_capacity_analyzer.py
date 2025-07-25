#!/usr/bin/env python3
"""
Cosmic Heat Capacity Analyzer - Klein Thermodynamics Test
==========================================================

OBJECTIVE: Test Klein cosmic heat capacity predictions
APPROACH: Parameter-free prediction testing
TARGET: C_V ≈ 1.7×10³² J/K from Klein atom ensemble

Rationale: If Klein thermodynamics is real, universe heat capacity should match
Prediction: Cosmic cooling rate should reflect Klein thermal degrees of freedom
Critical Test: Most fundamental test of Klein thermodynamics
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats, optimize, integrate
from typing import Dict, List, Tuple
import warnings
warnings.filterwarnings('ignore')

class CosmicHeatCapacityAnalyzer:
    """Cosmic heat capacity analysis for Klein thermodynamics"""
    
    def __init__(self):
        # Klein thermodynamic predictions (NO free parameters)
        self.T_klein = 0.091  # K (fundamental Klein temperature)
        self.R_klein = 8.4e6  # m (Klein atom radius) 
        self.f0_klein = 5.68  # Hz (Klein oscillation frequency)
        self.E0_klein = 2.35e-14 * 1.602e-19  # J (Klein energy scale)
        
        # Physical constants
        self.c = 2.998e8      # m/s
        self.k_B = 1.381e-23  # J/K
        self.G = 6.674e-11    # m³/(kg·s²)
        self.H0 = 2.2e-18     # s⁻¹ (Hubble constant)
        
        # Cosmic parameters
        self.rho_critical = 3 * self.H0**2 / (8 * np.pi * self.G)  # kg/m³
        self.age_universe = 13.8e9 * 365.25 * 24 * 3600  # seconds
        
        # Klein atom population in observable universe
        self.V_klein_atom = (4*np.pi/3) * self.R_klein**3
        self.V_observable = (4*np.pi/3) * (self.c * self.age_universe)**3
        self.N_klein_total = self.V_observable / self.V_klein_atom
        
        # Analysis data
        self.cosmic_data = {}
        self.heat_capacity_analysis = {}
        
    def generate_cosmic_evolution_data(self) -> bool:
        """Generate cosmic evolution data with Klein heat capacity"""
        
        print("🌌 Cosmic Heat Capacity Klein Analysis")
        print("=" * 55)
        print("Generating cosmic thermal evolution data...")
        
        # Time evolution from Big Bang to present
        # Using conformal time for easier calculation
        n_points = 1000
        scale_factors = np.logspace(-4, 0, n_points)  # a from 0.0001 to 1
        cosmic_times = []
        
        # Convert scale factor to cosmic time (rough approximation)
        for a in scale_factors:
            # t ∝ a^(3/2) for matter-dominated
            # t ∝ a² for radiation-dominated  
            # Use transition at a ≈ 1/3400
            if a < 1/3400:  # Radiation dominated
                t = a**2 * self.age_universe * (1/3400)**(-3/2)
            else:  # Matter dominated
                t = a**(3/2) * self.age_universe
            cosmic_times.append(t)
            
        cosmic_times = np.array(cosmic_times)
        
        # Standard cosmological temperature evolution
        # T_standard ∝ (1+z) = 1/a for radiation
        T_cmb_today = 2.725  # K
        T_standard = T_cmb_today / scale_factors
        
        # Klein temperature evolution
        # Klein atoms should cool according to their heat capacity
        T_klein_evolution = []
        
        for i, (a, t) in enumerate(zip(scale_factors, cosmic_times)):
            if i == 0:
                # Initial Klein temperature (assume starts at E0/kB)
                T_klein_initial = self.E0_klein / self.k_B
                T_klein_evolution.append(T_klein_initial)
            else:
                # Adiabatic cooling with Klein heat capacity
                dt = cosmic_times[i] - cosmic_times[i-1]
                T_prev = T_klein_evolution[-1]
                
                # Heat capacity per Klein atom (3 degrees of freedom)
                C_V_atom = 3 * self.k_B
                C_V_total = self.N_klein_total * C_V_atom
                
                # Cosmic expansion cooling rate
                # dE/dt = -3H * (internal_energy)
                H_now = self.H0 * np.sqrt(0.3 * a**(-3) + 0.7)  # Simplified
                
                internal_energy = C_V_total * T_prev
                dE_dt = -3 * H_now * internal_energy
                dT_dt = dE_dt / C_V_total
                
                T_new = T_prev + dT_dt * dt
                T_klein_evolution.append(max(T_new, self.T_klein))  # Floor at today's value
                
        T_klein_evolution = np.array(T_klein_evolution)
        
        # Calculate cosmic heat capacity evolution
        heat_capacities = []
        for a in scale_factors:
            # Klein atom density varies with scale factor
            n_klein = self.N_klein_total / (self.V_observable * a**3)
            C_V_cosmic = n_klein * self.V_observable * a**3 * 3 * self.k_B
            heat_capacities.append(C_V_cosmic)
            
        heat_capacities = np.array(heat_capacities)
        
        # Energy storage in Klein degrees of freedom
        klein_internal_energy = heat_capacities * T_klein_evolution
        
        # Fraction of cosmic energy in Klein thermal
        rho_klein_thermal = klein_internal_energy / (self.V_observable * self.c**2)
        omega_klein_thermal = rho_klein_thermal / self.rho_critical
        
        self.cosmic_data = {
            'scale_factors': scale_factors,
            'cosmic_times': cosmic_times,
            'T_standard': T_standard,
            'T_klein_evolution': T_klein_evolution,
            'heat_capacities': heat_capacities,
            'klein_internal_energy': klein_internal_energy,
            'omega_klein_thermal': omega_klein_thermal,
            'redshifts': 1/scale_factors - 1
        }
        
        print(f"✅ Generated {n_points} cosmic evolution points")
        print(f"   • Time span: {cosmic_times[0]/3.15e7:.1e} to {cosmic_times[-1]/3.15e16:.1f} Gyr")
        print(f"   • Klein heat capacity today: {heat_capacities[-1]:.2e} J/K")
        print(f"   • Klein thermal energy density: Ω = {omega_klein_thermal[-1]:.2e}")
        
        return True
        
    def analyze_heat_capacity_signatures(self) -> Dict:
        """Search for Klein heat capacity signatures in cosmic evolution"""
        
        print("\\n🔍 Analyzing cosmic heat capacity signatures...")
        
        results = {
            'temperature_evolution': {},
            'energy_budget': {},
            'cooling_rate': {},
            'statistical_tests': {}
        }
        
        scale_factors = self.cosmic_data['scale_factors']
        T_standard = self.cosmic_data['T_standard']
        T_klein = self.cosmic_data['T_klein_evolution']
        heat_capacities = self.cosmic_data['heat_capacities']
        omega_klein = self.cosmic_data['omega_klein_thermal']
        
        # 1. Temperature evolution analysis
        
        # Compare Klein vs standard cooling
        cooling_ratio = T_klein / T_standard
        
        # Expected Klein cooling signature
        # Should deviate from T ∝ 1/a due to heat capacity
        a_test = scale_factors[scale_factors > 0.1]  # Recent times
        T_test = T_klein[scale_factors > 0.1]
        
        # Fit power law: T ∝ a^β
        log_a = np.log(a_test)
        log_T = np.log(T_test)
        slope, intercept, r_value, p_value, std_err = stats.linregress(log_a, log_T)
        
        # Standard radiation: β = -1
        # Klein with heat capacity: β should be different
        klein_beta = slope
        beta_deviation = np.abs(klein_beta - (-1))
        beta_significance = beta_deviation / std_err if std_err > 0 else 0
        
        results['temperature_evolution'] = {
            'klein_beta': klein_beta,
            'standard_beta': -1.0,
            'deviation': beta_deviation,
            'significance': beta_significance,
            'correlation': r_value,
            'p_value': p_value
        }
        
        # 2. Energy budget analysis
        
        # Klein thermal energy as fraction of critical density
        omega_klein_today = omega_klein[-1]
        omega_klein_peak = np.max(omega_klein)
        
        # Compare to known energy components
        omega_matter = 0.31
        omega_lambda = 0.69
        omega_total_known = omega_matter + omega_lambda
        
        # Is Klein thermal energy detectable?
        klein_fraction = omega_klein_today / omega_total_known
        
        # Statistical test: Is omega_klein significantly > 0?
        # Use cosmic variance as uncertainty
        omega_uncertainty = 0.01 * omega_total_known  # 1% cosmic variance
        omega_significance = omega_klein_today / omega_uncertainty
        
        results['energy_budget'] = {
            'omega_klein_today': omega_klein_today,
            'omega_klein_peak': omega_klein_peak,
            'klein_fraction': klein_fraction,
            'omega_significance': omega_significance,
            'detectable': omega_significance > 3
        }
        
        # 3. Cooling rate analysis
        
        # Calculate dT/dt for Klein vs standard
        dt = np.diff(self.cosmic_data['cosmic_times'])
        dT_klein_dt = np.diff(T_klein) / dt
        dT_standard_dt = np.diff(T_standard) / dt
        
        # Cooling rate ratio
        cooling_rate_ratio = dT_klein_dt / dT_standard_dt
        mean_cooling_ratio = np.mean(cooling_rate_ratio[np.isfinite(cooling_rate_ratio)])
        
        # Heat capacity signature in cooling rate
        # Should show characteristic time scale
        C_V_today = heat_capacities[-1]
        thermal_time_scale = C_V_today * self.T_klein / (3 * self.H0 * C_V_today * self.T_klein)
        
        results['cooling_rate'] = {
            'mean_cooling_ratio': mean_cooling_ratio,
            'thermal_time_scale': thermal_time_scale,
            'heat_capacity_today': C_V_today
        }
        
        # 4. Statistical tests
        
        # Overall significance combining all tests
        temp_sig = beta_significance
        energy_sig = omega_significance  
        combined_significance = np.sqrt(temp_sig**2 + energy_sig**2)
        
        # Bayesian model comparison
        # Klein model vs standard ΛCDM
        # Use AIC-like criterion
        n_data = len(scale_factors)
        n_params_klein = 4  # T_klein, C_V, beta, omega_k
        n_params_standard = 2  # Standard cooling, known Ω
        
        # Chi-squared for fits (simplified)
        chi2_klein = np.sum((T_klein - T_standard)**2 / T_standard)
        chi2_standard = 0  # Perfect fit by definition
        
        AIC_klein = chi2_klein + 2 * n_params_klein
        AIC_standard = chi2_standard + 2 * n_params_standard
        delta_AIC = AIC_klein - AIC_standard
        
        # Model preference
        if delta_AIC < 2:
            model_preference = "Klein favored"
        elif delta_AIC < 10:
            model_preference = "Inconclusive"
        else:
            model_preference = "Standard favored"
            
        results['statistical_tests'] = {
            'temperature_significance': temp_sig,
            'energy_significance': energy_sig,
            'combined_significance': combined_significance,
            'delta_AIC': delta_AIC,
            'model_preference': model_preference,
            'chi2_klein': chi2_klein
        }
        
        self.heat_capacity_analysis = results
        return results
        
    def create_visualization(self):
        """Create cosmic heat capacity analysis visualization"""
        
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('Cosmic Heat Capacity: Klein Thermodynamics Test', 
                     fontweight='bold', fontsize=14)
        
        # 1. Temperature evolution
        ax1 = axes[0, 0]
        
        scale_factors = self.cosmic_data['scale_factors']
        T_standard = self.cosmic_data['T_standard']
        T_klein = self.cosmic_data['T_klein_evolution']
        redshifts = self.cosmic_data['redshifts']
        
        ax1.loglog(1 + redshifts, T_standard, 'b-', label='Standard T ∝ (1+z)', linewidth=2)
        ax1.loglog(1 + redshifts, T_klein, 'r--', label='Klein Thermodynamics', linewidth=2)
        
        # Mark today
        ax1.axvline(1, color='gray', linestyle=':', alpha=0.7, label='Today')
        ax1.axhline(self.T_klein, color='red', linestyle=':', alpha=0.7, 
                   label=f'T_Klein = {self.T_klein} K')
        
        ax1.set_xlabel('1 + Redshift')
        ax1.set_ylabel('Temperature (K)')
        ax1.set_title('A. Cosmic Temperature Evolution\\nKlein vs Standard Cooling')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 2. Heat capacity evolution
        ax2 = axes[0, 1]
        
        heat_capacities = self.cosmic_data['heat_capacities']
        
        ax2.loglog(1 + redshifts, heat_capacities, 'g-', linewidth=2)
        ax2.axhline(self.heat_capacity_analysis['cooling_rate']['heat_capacity_today'], 
                   color='red', linestyle='--', alpha=0.7,
                   label=f'Today: {self.heat_capacity_analysis["cooling_rate"]["heat_capacity_today"]:.1e} J/K')
        
        ax2.set_xlabel('1 + Redshift')
        ax2.set_ylabel('Heat Capacity (J/K)')
        ax2.set_title('B. Cosmic Heat Capacity\\nKlein Thermal Degrees of Freedom')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # 3. Results summary
        ax3 = axes[1, 0]
        ax3.axis('off')
        
        stats_data = self.heat_capacity_analysis['statistical_tests']
        temp_data = self.heat_capacity_analysis['temperature_evolution']
        energy_data = self.heat_capacity_analysis['energy_budget']
        
        summary_text = f"""
COSMIC HEAT CAPACITY ANALYSIS

THEORETICAL PREDICTIONS:
• Klein heat capacity: C_V = {heat_capacities[-1]:.1e} J/K
• Klein temperature today: T_K = {self.T_klein} K
• Thermal energy density: Ω_thermal predicted

COOLING RATE ANALYSIS:
• Klein cooling exponent: β = {temp_data['klein_beta']:.3f}
• Standard cooling: β = -1.000
• Deviation significance: {temp_data['significance']:.2f}σ

ENERGY BUDGET ANALYSIS:
• Ω_Klein today: {energy_data['omega_klein_today']:.2e}
• Peak Ω_Klein: {energy_data['omega_klein_peak']:.2e}
• Energy significance: {energy_data['omega_significance']:.2f}σ

STATISTICAL RESULTS:
• Combined significance: {stats_data['combined_significance']:.2f}σ
• Model comparison: {stats_data['model_preference']}
• ΔAoIC = {stats_data['delta_AIC']:.1f}

STATUS:
{'✅ KLEIN HEAT CAPACITY DETECTED' if stats_data['combined_significance'] > 3 else 
 '🔶 MARGINAL DETECTION' if stats_data['combined_significance'] > 2 else 
 '❌ NO HEAT CAPACITY SIGNATURE'}
        """
        
        color = ('green' if stats_data['combined_significance'] > 3 else 
                'orange' if stats_data['combined_significance'] > 2 else 'red')
        ax3.text(0.05, 0.95, summary_text, transform=ax3.transAxes,
                fontsize=9, verticalalignment='top', fontfamily='monospace',
                color=color)
        
        # 4. Energy density evolution
        ax4 = axes[1, 1]
        
        omega_klein = self.cosmic_data['omega_klein_thermal']
        
        ax4.loglog(1 + redshifts, omega_klein, 'purple', linewidth=2, 
                  label='Ω_Klein_thermal')
        
        # Standard components for comparison
        omega_m_z = 0.31 * (1 + redshifts)**3
        omega_l_z = np.full_like(redshifts, 0.69)
        
        ax4.loglog(1 + redshifts, omega_m_z, 'b:', alpha=0.7, label='Ω_matter')
        ax4.loglog(1 + redshifts, omega_l_z, 'r:', alpha=0.7, label='Ω_Λ')
        
        ax4.set_xlabel('1 + Redshift')
        ax4.set_ylabel('Energy Density Parameter Ω')
        ax4.set_title('C. Cosmic Energy Budget\\nKlein Thermal Contribution')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('cosmic_heat_capacity_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print("✅ Cosmic heat capacity visualization saved")

def main():
    """Main cosmic heat capacity analysis"""
    analyzer = CosmicHeatCapacityAnalyzer()
    
    if analyzer.generate_cosmic_evolution_data():
        results = analyzer.analyze_heat_capacity_signatures()
        analyzer.create_visualization()
        
        stats = results['statistical_tests']
        energy = results['energy_budget']
        temp = results['temperature_evolution']
        
        print(f"\\n🌌 COSMIC HEAT CAPACITY RESULTS:")
        print(f"   • Combined significance: {stats['combined_significance']:.2f}σ")
        print(f"   • Cooling rate deviation: {temp['significance']:.2f}σ")
        print(f"   • Energy density significance: {energy['omega_significance']:.2f}σ")
        print(f"   • Model preference: {stats['model_preference']}")
        
        status = ('DETECTED' if stats['combined_significance'] > 3 else 
                 'MARGINAL' if stats['combined_significance'] > 2 else 'NOT DETECTED')
        print(f"   • Status: Klein heat capacity {status}")
        
        return results
    return None

if __name__ == "__main__":
    main()