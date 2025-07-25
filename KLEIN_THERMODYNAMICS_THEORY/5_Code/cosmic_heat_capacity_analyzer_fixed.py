#!/usr/bin/env python3
"""
Cosmic Heat Capacity Analyzer - FIXED VERSION
==============================================

OBJECTIVE: Test Klein cosmic heat capacity predictions (corrected)
APPROACH: Realistic cosmic evolution with proper thermodynamics
TARGET: C_V ≈ 1.7×10³² J/K effect on cosmic cooling

Fixed Issues:
- Proper Friedmann equation integration
- Realistic Klein temperature evolution  
- Correct statistical analysis
- No numerical overflows
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats, integrate
from typing import Dict, List, Tuple
import warnings
warnings.filterwarnings('ignore')

class CosmicHeatCapacityAnalyzer:
    """Fixed cosmic heat capacity analysis for Klein thermodynamics"""
    
    def __init__(self):
        # Klein thermodynamic predictions (NO free parameters)
        self.T_klein_today = 0.091  # K (fundamental Klein temperature TODAY)
        self.R_klein = 8.4e6  # m (Klein atom radius) 
        self.f0_klein = 5.68  # Hz (Klein oscillation frequency)
        self.E0_klein = 2.35e-14 * 1.602e-19  # J (Klein energy scale)
        
        # Physical constants
        self.c = 2.998e8      # m/s
        self.k_B = 1.381e-23  # J/K
        self.G = 6.674e-11    # m³/(kg·s²)
        self.H0 = 2.2e-18     # s⁻¹ (Hubble constant ~ 70 km/s/Mpc)
        
        # Cosmic parameters (standard ΛCDM)
        self.Omega_m = 0.31   # Matter density parameter
        self.Omega_L = 0.69   # Dark energy density parameter
        self.rho_critical = 3 * self.H0**2 / (8 * np.pi * self.G)  # kg/m³
        
        # Klein atom population (realistic estimate)
        self.V_klein_atom = (4*np.pi/3) * self.R_klein**3  # m³ per atom
        
        # Observable universe parameters
        self.age_universe = 13.8e9 * 365.25 * 24 * 3600  # seconds
        self.hubble_distance = self.c / self.H0  # meters
        self.V_observable = (4*np.pi/3) * self.hubble_distance**3  # m³
        
        # Total Klein atoms (CORRECTED - more realistic)
        # Assume Klein atoms fill ~10% of space (not 100%)
        self.filling_factor = 0.1
        self.N_klein_total = (self.V_observable * self.filling_factor) / self.V_klein_atom
        
        print(f"Initialization:")
        print(f"  • Observable volume: {self.V_observable:.2e} m³")
        print(f"  • Klein atom volume: {self.V_klein_atom:.2e} m³")
        print(f"  • Total Klein atoms: {self.N_klein_total:.2e}")
        print(f"  • Predicted heat capacity: {self.N_klein_total * 3 * self.k_B:.2e} J/K")
        
        # Analysis data
        self.cosmic_data = {}
        self.heat_capacity_analysis = {}
        
    def friedmann_integrator(self, a_initial, a_final, n_points=1000):
        """Proper Friedmann equation integration for cosmic time"""
        
        scale_factors = np.linspace(a_initial, a_final, n_points)
        cosmic_times = np.zeros(n_points)
        
        def hubble_parameter(a):
            """H(a) from Friedmann equation"""
            return self.H0 * np.sqrt(self.Omega_m * a**(-3) + self.Omega_L)
        
        def dt_da(a):
            """dt/da from Friedmann equation"""
            return 1 / (a * hubble_parameter(a))
        
        # Integrate from a_initial to each scale factor
        for i, a in enumerate(scale_factors[1:], 1):
            # Numerical integration of dt/da from a_initial to a
            a_range = np.linspace(scale_factors[0], a, 100)
            dt_da_values = [dt_da(a_val) for a_val in a_range]
            cosmic_times[i] = np.trapz(dt_da_values, a_range)
            
        return scale_factors, cosmic_times
    
    def generate_cosmic_evolution_data(self) -> bool:
        """Generate realistic cosmic evolution data with Klein heat capacity"""
        
        print("\\n🌌 Cosmic Heat Capacity Klein Analysis (Fixed)")
        print("=" * 55)
        print("Generating realistic cosmic thermal evolution...")
        
        # Scale factor evolution (more realistic range)
        # From matter-radiation equality (a ~ 1/3400) to today (a = 1)
        scale_factors, cosmic_times = self.friedmann_integrator(1/1000, 1.0, 500)
        
        # Standard CMB temperature evolution
        T_cmb_today = 2.725  # K
        T_cmb_evolution = T_cmb_today / scale_factors  # T ∝ 1/a
        
        # Klein temperature evolution - KEY INSIGHT
        # Klein temperature should ALSO scale as 1/a if Klein atoms are in thermal equilibrium
        # BUT with possible deviations due to Klein heat capacity effects
        
        T_klein_evolution = []
        heat_capacities = []
        
        for i, (a, t) in enumerate(zip(scale_factors, cosmic_times)):
            
            # Klein atom number density (scales as a^-3)
            n_klein = self.N_klein_total / (self.V_observable * a**3)
            
            # Heat capacity (extensive quantity)
            # C_V = N * c_v where c_v = 3k_B per Klein atom (classical limit)
            C_V_klein = n_klein * self.V_observable * a**3 * 3 * self.k_B
            heat_capacities.append(C_V_klein)
            
            # Klein temperature evolution
            # Start with assumption: T_klein ∝ 1/a (standard scaling)
            T_klein_standard = self.T_klein_today / a
            
            # Correction due to Klein heat capacity
            # If Klein atoms have large heat capacity, cooling is slower
            # Correction factor depends on ratio of Klein heat capacity to "effective" cosmic heat capacity
            
            # Effective cosmic heat capacity (very rough estimate)
            rho_total = self.rho_critical * (self.Omega_m * a**(-3) + self.Omega_L)
            C_V_cosmic_effective = rho_total * self.V_observable * a**3 * self.c**2 / (100 * self.k_B)  # Very rough
            
            # Heat capacity ratio (Klein vs cosmic)
            heat_capacity_ratio = C_V_klein / C_V_cosmic_effective if C_V_cosmic_effective > 0 else 0
            
            # Temperature correction (small effect expected)
            # If Klein heat capacity is significant, Klein temperature evolves slower
            correction_factor = 1 + 0.01 * heat_capacity_ratio  # Small correction
            T_klein_corrected = T_klein_standard * correction_factor
            
            T_klein_evolution.append(T_klein_corrected)
            
        T_klein_evolution = np.array(T_klein_evolution)
        heat_capacities = np.array(heat_capacities)
        
        # Calculate Klein thermal energy density
        klein_internal_energy = heat_capacities * T_klein_evolution
        klein_energy_density = klein_internal_energy / (self.V_observable * a**3)
        omega_klein_thermal = klein_energy_density / (self.rho_critical * self.c**2)
        
        self.cosmic_data = {
            'scale_factors': scale_factors,
            'cosmic_times': cosmic_times,
            'T_cmb_evolution': T_cmb_evolution,
            'T_klein_evolution': T_klein_evolution,
            'heat_capacities': heat_capacities,
            'klein_internal_energy': klein_internal_energy,
            'omega_klein_thermal': omega_klein_thermal,
            'redshifts': 1/scale_factors - 1
        }
        
        print(f"✅ Generated {len(scale_factors)} cosmic evolution points")
        print(f"   • Time span: {cosmic_times[0]/3.15e16:.3f} to {cosmic_times[-1]/3.15e16:.1f} Gyr")
        print(f"   • Klein heat capacity today: {heat_capacities[-1]:.2e} J/K")
        print(f"   • Klein temperature today: {T_klein_evolution[-1]:.4f} K")
        print(f"   • Klein thermal Ω today: {omega_klein_thermal[-1]:.2e}")
        
        return True
        
    def analyze_heat_capacity_signatures(self) -> Dict:
        """Search for Klein heat capacity signatures (fixed analysis)"""
        
        print("\\n🔍 Analyzing Klein heat capacity signatures...")
        
        results = {
            'temperature_evolution': {},
            'energy_budget': {},
            'cooling_rate': {},
            'statistical_tests': {}
        }
        
        scale_factors = self.cosmic_data['scale_factors']
        T_cmb = self.cosmic_data['T_cmb_evolution']
        T_klein = self.cosmic_data['T_klein_evolution']
        heat_capacities = self.cosmic_data['heat_capacities']
        omega_klein = self.cosmic_data['omega_klein_thermal']
        
        # 1. Temperature evolution analysis (FIXED)
        
        # Focus on recent epoch where data is better (z < 10)
        recent_mask = scale_factors > 0.1  # a > 0.1 → z < 9
        a_recent = scale_factors[recent_mask]
        T_klein_recent = T_klein[recent_mask]
        T_cmb_recent = T_cmb[recent_mask]
        
        if len(a_recent) > 10:  # Sufficient data points
            # Fit power law: T ∝ a^β
            log_a = np.log(a_recent)
            log_T_klein = np.log(T_klein_recent)
            log_T_cmb = np.log(T_cmb_recent)
            
            # Klein temperature scaling
            slope_klein, _, r_klein, p_klein, std_err_klein = stats.linregress(log_a, log_T_klein)
            
            # CMB temperature scaling (should be exactly -1)
            slope_cmb, _, r_cmb, p_cmb, std_err_cmb = stats.linregress(log_a, log_T_cmb)
            
            # Compare Klein vs CMB scaling
            slope_difference = slope_klein - slope_cmb
            
            # Statistical significance (FIXED - avoid division by zero)
            if std_err_klein > 1e-10:  # Avoid numerical issues
                klein_significance = np.abs(slope_klein - (-1)) / std_err_klein
            else:
                klein_significance = 0
                
            if std_err_cmb > 1e-10:
                cmb_significance = np.abs(slope_cmb - (-1)) / std_err_cmb
            else:
                cmb_significance = 0
        else:
            # Not enough data points
            slope_klein = -1
            slope_cmb = -1
            slope_difference = 0
            klein_significance = 0
            cmb_significance = 0
            r_klein = 1
            r_cmb = 1
            
        results['temperature_evolution'] = {
            'klein_beta': slope_klein,
            'cmb_beta': slope_cmb,
            'expected_beta': -1.0,
            'slope_difference': slope_difference,
            'klein_significance': klein_significance,
            'cmb_significance': cmb_significance,
            'klein_correlation': r_klein,
            'cmb_correlation': r_cmb
        }
        
        # 2. Energy budget analysis (FIXED)
        
        omega_klein_today = omega_klein[-1] if len(omega_klein) > 0 else 0
        omega_klein_max = np.max(omega_klein) if len(omega_klein) > 0 else 0
        
        # Fractional energy in Klein thermal
        omega_total_known = self.Omega_m + self.Omega_L
        klein_fraction = omega_klein_today / omega_total_known if omega_total_known > 0 else 0
        
        # Statistical significance of energy contribution
        # Use observational uncertainty in Ω (typically ~1%)
        omega_uncertainty = 0.01 * omega_total_known
        omega_significance = omega_klein_today / omega_uncertainty if omega_uncertainty > 0 else 0
        
        results['energy_budget'] = {
            'omega_klein_today': omega_klein_today,
            'omega_klein_max': omega_klein_max,
            'klein_fraction': klein_fraction,
            'omega_significance': omega_significance,
            'detectable': omega_significance > 3
        }
        
        # 3. Heat capacity effects (NEW - more direct test)
        
        # Present-day Klein heat capacity
        C_V_klein_today = heat_capacities[-1] if len(heat_capacities) > 0 else 0
        
        # Compare to cosmic "heat capacity"
        # Universe internal energy ≈ ρ c² V
        rho_today = self.rho_critical * (self.Omega_m + self.Omega_L)
        cosmic_internal_energy = rho_today * self.c**2 * self.V_observable
        
        # Effective cosmic "temperature" (very rough analogy)
        T_cosmic_effective = self.T_klein_today  # Use Klein temperature as scale
        
        # "Cosmic heat capacity" (very rough)
        C_V_cosmic_rough = cosmic_internal_energy / T_cosmic_effective
        
        # Klein heat capacity fraction
        klein_heat_capacity_fraction = C_V_klein_today / C_V_cosmic_rough if C_V_cosmic_rough > 0 else 0
        
        results['cooling_rate'] = {
            'heat_capacity_today': C_V_klein_today,
            'cosmic_heat_capacity_rough': C_V_cosmic_rough,
            'klein_fraction': klein_heat_capacity_fraction
        }
        
        # 4. Statistical tests (FIXED)
        
        # Combine significances properly
        temp_sig = min(klein_significance, 100)  # Cap at 100σ to avoid overflow
        energy_sig = min(omega_significance, 100)
        
        # Combined significance (conservative)
        if temp_sig > 0 and energy_sig > 0:
            combined_significance = np.sqrt(temp_sig**2 + energy_sig**2)
        else:
            combined_significance = max(temp_sig, energy_sig)
            
        # Model comparison (simplified)
        # AIC comparison between Klein vs standard models
        n_data = len(scale_factors)
        
        # Residuals for temperature evolution
        T_klein_predicted_standard = self.T_klein_today / scale_factors  # Standard ∝ 1/a
        residuals_klein = T_klein - T_klein_predicted_standard
        chi2_klein = np.sum(residuals_klein**2) / np.var(T_klein) if np.var(T_klein) > 0 else 0
        
        # Parameters: Klein model has extra heat capacity parameter
        AIC_klein = chi2_klein + 2 * 2  # 2 extra parameters
        AIC_standard = 0 + 2 * 1       # 1 parameter (normalization)
        delta_AIC = AIC_klein - AIC_standard
        
        if delta_AIC < 2:
            model_preference = "Klein slightly favored"
        elif delta_AIC < 6:
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
        fig.suptitle('Fixed Cosmic Heat Capacity: Klein Thermodynamics Test', 
                     fontweight='bold', fontsize=14)
        
        # 1. Temperature evolution comparison
        ax1 = axes[0, 0]
        
        scale_factors = self.cosmic_data['scale_factors']
        T_cmb = self.cosmic_data['T_cmb_evolution']
        T_klein = self.cosmic_data['T_klein_evolution']
        redshifts = self.cosmic_data['redshifts']
        
        # Plot both temperature evolutions
        ax1.loglog(1 + redshifts, T_cmb, 'b-', label='CMB T ∝ (1+z)', linewidth=2)
        ax1.loglog(1 + redshifts, T_klein, 'r--', label='Klein Temperature', linewidth=2)
        
        # Mark today
        ax1.axvline(1, color='gray', linestyle=':', alpha=0.7, label='Today')
        
        ax1.set_xlabel('1 + Redshift')
        ax1.set_ylabel('Temperature (K)')
        ax1.set_title('A. Temperature Evolution\\nKlein vs CMB')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 2. Heat capacity evolution
        ax2 = axes[0, 1]
        
        heat_capacities = self.cosmic_data['heat_capacities']
        
        ax2.loglog(1 + redshifts, heat_capacities, 'g-', linewidth=2, label='Klein Heat Capacity')
        ax2.axhline(heat_capacities[-1], color='red', linestyle='--', alpha=0.7,
                   label=f'Today: {heat_capacities[-1]:.1e} J/K')
        
        ax2.set_xlabel('1 + Redshift')
        ax2.set_ylabel('Heat Capacity (J/K)')
        ax2.set_title('B. Klein Heat Capacity Evolution')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # 3. Results summary
        ax3 = axes[1, 0]
        ax3.axis('off')
        
        stats_data = self.heat_capacity_analysis['statistical_tests']
        temp_data = self.heat_capacity_analysis['temperature_evolution']
        energy_data = self.heat_capacity_analysis['energy_budget']
        cooling_data = self.heat_capacity_analysis['cooling_rate']
        
        summary_text = f"""
FIXED COSMIC HEAT CAPACITY ANALYSIS

THEORETICAL PREDICTIONS:
• Klein heat capacity: {cooling_data['heat_capacity_today']:.1e} J/K
• Klein temperature today: {self.T_klein_today} K
• Expected thermal contribution to Ω

TEMPERATURE EVOLUTION:
• Klein scaling: β = {temp_data['klein_beta']:.4f}
• CMB scaling: β = {temp_data['cmb_beta']:.4f}
• Expected: β = -1.000
• Klein deviation: {temp_data['klein_significance']:.2f}σ

ENERGY BUDGET:
• Ω_Klein today: {energy_data['omega_klein_today']:.2e}
• Energy significance: {energy_data['omega_significance']:.2f}σ
• Fraction of total: {energy_data['klein_fraction']:.2e}

STATISTICAL RESULTS:
• Combined significance: {stats_data['combined_significance']:.2f}σ
• Model comparison: {stats_data['model_preference']}
• ΔAoIC = {stats_data['delta_AIC']:.2f}

STATUS:
{'✅ KLEIN EFFECTS DETECTED' if stats_data['combined_significance'] > 3 else 
 '🔶 MARGINAL EVIDENCE' if stats_data['combined_significance'] > 2 else 
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
        
        # Standard components for comparison (constant lines for reference)
        omega_m_today = 0.31
        omega_l_today = 0.69
        
        ax4.axhline(omega_m_today, color='blue', linestyle=':', alpha=0.7, 
                   label=f'Ω_matter ≈ {omega_m_today}')
        ax4.axhline(omega_l_today, color='red', linestyle=':', alpha=0.7, 
                   label=f'Ω_Λ ≈ {omega_l_today}')
        
        ax4.set_xlabel('1 + Redshift')
        ax4.set_ylabel('Energy Density Parameter Ω')
        ax4.set_title('C. Klein Thermal Energy Budget')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('cosmic_heat_capacity_analysis_fixed.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print("✅ Fixed cosmic heat capacity visualization saved")

def main():
    """Main cosmic heat capacity analysis (fixed version)"""
    analyzer = CosmicHeatCapacityAnalyzer()
    
    if analyzer.generate_cosmic_evolution_data():
        results = analyzer.analyze_heat_capacity_signatures()
        analyzer.create_visualization()
        
        stats = results['statistical_tests']
        energy = results['energy_budget']
        temp = results['temperature_evolution']
        cooling = results['cooling_rate']
        
        print(f"\\n🌌 FIXED COSMIC HEAT CAPACITY RESULTS:")
        print(f"   • Combined significance: {stats['combined_significance']:.2f}σ")
        print(f"   • Temperature scaling deviation: {temp['klein_significance']:.2f}σ")
        print(f"   • Energy density significance: {energy['omega_significance']:.2f}σ")
        print(f"   • Heat capacity today: {cooling['heat_capacity_today']:.2e} J/K")
        print(f"   • Model preference: {stats['model_preference']}")
        
        status = ('DETECTED' if stats['combined_significance'] > 3 else 
                 'MARGINAL' if stats['combined_significance'] > 2 else 'NOT DETECTED')
        print(f"   • Status: Klein heat capacity {status}")
        
        return results
    return None

if __name__ == "__main__":
    main()