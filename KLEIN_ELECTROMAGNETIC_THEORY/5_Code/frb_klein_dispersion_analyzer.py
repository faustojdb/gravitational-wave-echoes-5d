#!/usr/bin/env python3
"""
FRB Klein Dispersion Analyzer
==============================

OBJECTIVE: Search for Klein-modified dispersion in Fast Radio Burst data
APPROACH: Parameter-free analysis of Klein dispersion corrections
TARGET: Klein dispersion measure DM_Klein ≈ 10⁻¹⁵ pc cm⁻³ per Mpc

Theory: Klein electromagnetic coupling modifies radio wave propagation
Prediction: Additional frequency-dependent delay beyond standard DM law
Critical Test: Klein effects in radio wave propagation through cosmic distances
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats, optimize
from typing import Dict, List, Tuple
import warnings
warnings.filterwarnings('ignore')

class FRBKleinDispersionAnalyzer:
    """FRB catalog analysis for Klein electromagnetic dispersion detection"""
    
    def __init__(self):
        # Klein electromagnetic predictions (NO free parameters)
        self.f0_klein = 5.68  # Hz (Klein oscillation frequency)
        self.gamma_em = 1e-15  # Klein-EM coupling strength
        self.c = 2.998e8  # m/s
        
        # Klein dispersion prediction
        # Additional delay: Δt_Klein = DM_Klein × (f⁻² - f_ref⁻²)
        self.DM_klein_per_Mpc = self.gamma_em * 1e-15  # pc cm⁻³ per Mpc (rough estimate)
        
        print(f"FRB Klein Dispersion Analysis")
        print(f"=" * 35)
        print(f"Klein frequency: f₀ = {self.f0_klein} Hz")
        print(f"Klein-EM coupling: γ_EM = {self.gamma_em:.2e}")
        print(f"Klein DM per Mpc: {self.DM_klein_per_Mpc:.2e} pc cm⁻³/Mpc")
        
        # Analysis data
        self.frb_data = {}
        self.dispersion_analysis = {}
        
    def generate_representative_frb_data(self) -> bool:
        """Generate representative FRB catalog data"""
        
        print("\\n📡 Generating Representative FRB Catalog Data...")
        print("(Note: Using simulated data representative of CHIME/FRB precision)")
        
        # Generate sample of Fast Radio Bursts
        n_frbs = 500  # Representative FRB sample size
        frbs = []
        
        # Frequency coverage (typical for radio telescopes)
        freq_min = 400e6  # 400 MHz
        freq_max = 800e6  # 800 MHz
        n_freq_channels = 1024
        frequencies = np.linspace(freq_min, freq_max, n_freq_channels)
        
        for i in range(n_frbs):
            frb_name = f"FRB {20180101 + i}"
            
            # FRB properties
            # Distance (redshift-based rough estimate)
            redshift = np.random.uniform(0.1, 2.0)  # Cosmological FRBs
            distance_Mpc = redshift * self.c / (70e3)  # Rough Hubble distance
            
            # Standard dispersion measure (empirical relationship)
            # DM roughly scales with distance for extragalactic FRBs
            DM_host = np.random.uniform(10, 100)  # pc cm⁻³ (host galaxy)
            DM_IGM = distance_Mpc * np.random.uniform(50, 200)  # Intergalactic medium
            DM_MW = np.random.uniform(20, 60)  # Milky Way foreground
            DM_total_standard = DM_host + DM_IGM + DM_MW
            
            # Klein dispersion contribution
            DM_klein = distance_Mpc * self.DM_klein_per_Mpc
            DM_total_with_klein = DM_total_standard + DM_klein
            
            # Generate arrival times across frequency channels
            # Standard dispersion law: t ∝ DM × f⁻²
            reference_freq = np.max(frequencies)
            
            # Standard arrival times
            standard_delays = 4.149e-3 * DM_total_standard * (frequencies**(-2) - reference_freq**(-2))  # ms
            
            # Klein dispersion corrections
            klein_delays = 4.149e-3 * DM_klein * (frequencies**(-2) - reference_freq**(-2))  # ms
            
            # Add observational uncertainties
            timing_uncertainty = 0.1e-3  # 0.1 ms typical FRB timing precision
            noise = np.random.normal(0, timing_uncertainty, len(frequencies))
            
            # Total observed arrival times
            total_delays = standard_delays + klein_delays + noise
            
            # FRB properties for analysis
            frb_width = np.random.uniform(0.1, 10.0)  # ms
            flux_density = np.random.uniform(0.1, 100.0)  # Jy
            
            frbs.append({
                'name': frb_name,
                'redshift': redshift,
                'distance_Mpc': distance_Mpc,
                'DM_total_standard': DM_total_standard,
                'DM_klein': DM_klein,
                'DM_total_observed': DM_total_with_klein,
                'frequencies': frequencies.copy(),
                'arrival_delays': total_delays,
                'standard_delays': standard_delays,
                'klein_delays': klein_delays,
                'timing_uncertainty': timing_uncertainty,
                'width_ms': frb_width,
                'flux_Jy': flux_density
            })
            
        self.frb_data = {
            'frbs': frbs,
            'n_frbs': n_frbs,
            'frequency_range': [freq_min/1e6, freq_max/1e6],  # MHz
            'n_channels': n_freq_channels
        }
        
        print(f"✅ Generated {n_frbs} FRBs")
        print(f"   • Redshift range: 0.1 - 2.0")
        print(f"   • Distance range: {min(frb['distance_Mpc'] for frb in frbs):.0f} - {max(frb['distance_Mpc'] for frb in frbs):.0f} Mpc")
        print(f"   • Frequency range: {freq_min/1e6:.0f} - {freq_max/1e6:.0f} MHz")
        print(f"   • Timing precision: ±0.1 ms")
        
        return True
        
    def analyze_klein_dispersion(self) -> Dict:
        """Search for Klein dispersion signatures in FRB data"""
        
        print("\\n🔍 Searching for Klein Dispersion Signatures...")
        
        results = {
            'individual_dm_analysis': [],
            'distance_correlation': {},
            'frequency_dependence': {},
            'statistical_tests': {}
        }
        
        frbs = self.frb_data['frbs']
        
        # 1. Individual FRB dispersion analysis
        dm_residuals = []
        dm_klein_predictions = []
        distances = []
        
        for frb in frbs:
            frequencies = frb['frequencies']
            arrival_delays = frb['arrival_delays']
            distance_Mpc = frb['distance_Mpc']
            
            # Fit standard dispersion law to arrival times
            # t = t₀ + DM × K × (f⁻² - f_ref⁻²)
            # where K = 4.149e-3 ms·MHz²·pc⁻¹·cm³
            
            reference_freq = np.max(frequencies)
            freq_term = frequencies**(-2) - reference_freq**(-2)
            
            # Linear regression: arrival_delays vs freq_term
            if len(frequencies) > 5:
                slope, intercept, r_value, p_value, std_err = stats.linregress(freq_term, arrival_delays)
                
                # Convert slope to DM (slope = DM × 4.149e-3)
                DM_fitted = slope / 4.149e-3  # pc cm⁻³
                DM_uncertainty = std_err / 4.149e-3
                
                # Expected DM from distance
                DM_expected = frb['DM_total_standard']
                DM_klein_expected = frb['DM_klein']
                
                # Residual (observed - expected standard DM)
                DM_residual = DM_fitted - DM_expected
                
                dm_residuals.append(DM_residual)
                dm_klein_predictions.append(DM_klein_expected)
                distances.append(distance_Mpc)
                
                results['individual_dm_analysis'].append({
                    'frb_name': frb['name'],
                    'distance_Mpc': distance_Mpc,
                    'DM_fitted': DM_fitted,
                    'DM_expected': DM_expected,
                    'DM_residual': DM_residual,
                    'DM_klein_predicted': DM_klein_expected,
                    'DM_uncertainty': DM_uncertainty,
                    'fit_r_squared': r_value**2,
                    'fit_p_value': p_value
                })
            else:
                dm_residuals.append(0)
                dm_klein_predictions.append(0)
                distances.append(distance_Mpc)
                
        dm_residuals = np.array(dm_residuals)
        dm_klein_predictions = np.array(dm_klein_predictions)
        distances = np.array(distances)
        
        # 2. Distance correlation analysis
        # Klein DM should correlate with distance
        
        if len(distances) > 10:
            # Correlation between DM residuals and distance
            distance_correlation, distance_p_value = stats.pearsonr(distances, dm_residuals)
            
            # Correlation between DM residuals and Klein predictions
            klein_correlation, klein_p_value = stats.pearsonr(dm_klein_predictions, dm_residuals)
            
            # Linear regression: DM residuals vs distance
            slope_distance, intercept_distance, r_distance, p_distance, stderr_distance = stats.linregress(distances, dm_residuals)
            
            # Statistical significance of distance correlation
            if stderr_distance > 0:
                distance_significance = np.abs(slope_distance) / stderr_distance
            else:
                distance_significance = 0
                
        else:
            distance_correlation = 0
            klein_correlation = 0
            distance_significance = 0
            slope_distance = 0
            
        results['distance_correlation'] = {
            'correlation': distance_correlation,
            'p_value': distance_p_value if 'distance_p_value' in locals() else 1,
            'klein_correlation': klein_correlation,
            'klein_p_value': klein_p_value if 'klein_p_value' in locals() else 1,
            'slope_per_Mpc': slope_distance,
            'significance': distance_significance
        }
        
        # 3. Frequency dependence analysis
        # Stack all FRBs to look for systematic Klein frequency effects
        
        all_freq_terms = []
        all_residuals_normalized = []
        
        for frb in frbs:
            frequencies = frb['frequencies']
            arrival_delays = frb['arrival_delays']
            
            # Expected delays from standard DM
            reference_freq = np.max(frequencies)
            freq_term = frequencies**(-2) - reference_freq**(-2)
            expected_delays = 4.149e-3 * frb['DM_total_standard'] * freq_term
            
            # Residuals from expected
            delay_residuals = arrival_delays - expected_delays
            
            # Normalize by timing uncertainty
            normalized_residuals = delay_residuals / frb['timing_uncertainty']
            
            all_freq_terms.extend(freq_term)
            all_residuals_normalized.extend(normalized_residuals)
            
        all_freq_terms = np.array(all_freq_terms)
        all_residuals_normalized = np.array(all_residuals_normalized)
        
        # Look for systematic frequency dependence in residuals
        if len(all_freq_terms) > 50:
            freq_correlation, freq_p_value = stats.pearsonr(all_freq_terms, all_residuals_normalized)
            
            # Linear regression
            slope_freq, intercept_freq, r_freq, p_freq, stderr_freq = stats.linregress(all_freq_terms, all_residuals_normalized)
            
            # Statistical significance
            if stderr_freq > 0:
                freq_significance = np.abs(slope_freq) / stderr_freq
            else:
                freq_significance = 0
        else:
            freq_correlation = 0
            freq_significance = 0
            
        results['frequency_dependence'] = {
            'correlation': freq_correlation,
            'p_value': freq_p_value if 'freq_p_value' in locals() else 1,
            'slope': slope_freq if 'slope_freq' in locals() else 0,
            'significance': freq_significance
        }
        
        # 4. Statistical tests
        
        # Test 1: Are DM residuals systematically positive (Klein excess)?
        if len(dm_residuals) > 5:
            positive_residuals = np.sum(dm_residuals > 0)
            total_residuals = len(dm_residuals)
            
            # Binomial test
            try:
                result = stats.binomtest(positive_residuals, total_residuals, 0.5)
                binomial_p_value = result.pvalue
            except AttributeError:
                # Fallback for older scipy
                binomial_p_value = stats.binom_test(positive_residuals, total_residuals, 0.5)
                
            if binomial_p_value > 0:
                binomial_significance = stats.norm.ppf(1 - binomial_p_value/2)
            else:
                binomial_significance = 0
        else:
            binomial_significance = 0
            
        # Test 2: Is mean DM residual significantly > 0?
        if len(dm_residuals) > 1:
            mean_residual = np.mean(dm_residuals)
            residual_std = np.std(dm_residuals)
            
            if residual_std > 0:
                mean_significance = mean_residual / (residual_std / np.sqrt(len(dm_residuals)))
                mean_significance = max(0, mean_significance)  # Only positive excesses
            else:
                mean_significance = 0
        else:
            mean_significance = 0
            
        # Combined significance
        combined_significance = np.sqrt(distance_significance**2 + 
                                      freq_significance**2 + 
                                      binomial_significance**2 + 
                                      mean_significance**2)
        
        results['statistical_tests'] = {
            'distance_significance': distance_significance,
            'frequency_significance': freq_significance,
            'binomial_significance': binomial_significance,
            'mean_significance': mean_significance,
            'combined_significance': combined_significance,
            'binomial_p_value': binomial_p_value if 'binomial_p_value' in locals() else 1,
            'positive_residuals': positive_residuals if 'positive_residuals' in locals() else 0,
            'total_residuals': total_residuals if 'total_residuals' in locals() else 0
        }
        
        self.dispersion_analysis = results
        return results
        
    def create_visualization(self):
        """Create FRB Klein dispersion analysis visualization"""
        
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('FRB Klein Dispersion Detection Analysis', 
                     fontweight='bold', fontsize=14)
        
        # Prepare data for plotting
        individual_data = self.dispersion_analysis['individual_dm_analysis']
        
        if len(individual_data) > 0:
            distances = [frb['distance_Mpc'] for frb in individual_data]
            dm_residuals = [frb['DM_residual'] for frb in individual_data]
            dm_klein_predicted = [frb['DM_klein_predicted'] for frb in individual_data]
            
            # 1. Distance vs DM residuals
            ax1 = axes[0, 0]
            
            ax1.scatter(distances, dm_residuals, alpha=0.6, s=30, label='Observed Residuals')
            ax1.scatter(distances, dm_klein_predicted, alpha=0.8, s=20, color='red', 
                       label='Klein Prediction')
            
            # Trend lines
            if len(distances) > 5:
                # Fit line to residuals
                z_residuals = np.polyfit(distances, dm_residuals, 1)
                p_residuals = np.poly1d(z_residuals)
                dist_range = np.linspace(min(distances), max(distances), 100)
                ax1.plot(dist_range, p_residuals(dist_range), 'b--', alpha=0.7, 
                        label=f'Residual Trend (slope={z_residuals[0]:.2e})')
                
                # Klein prediction line
                klein_slope = self.DM_klein_per_Mpc
                ax1.plot(dist_range, klein_slope * dist_range, 'r--', linewidth=2,
                        label=f'Klein Theory (slope={klein_slope:.2e})')
            
            ax1.axhline(0, color='gray', linestyle='-', alpha=0.5)
            ax1.set_xlabel('Distance (Mpc)')
            ax1.set_ylabel('DM Residual (pc cm⁻³)')
            ax1.set_title('A. Distance vs DM Residuals')
            ax1.legend()
            ax1.grid(True, alpha=0.3)
            
            # 2. Predicted vs observed Klein DM
            ax2 = axes[0, 1]
            
            ax2.scatter(dm_klein_predicted, dm_residuals, alpha=0.6, s=30)
            
            # Perfect correlation line
            if len(dm_klein_predicted) > 0:
                min_val = min(min(dm_klein_predicted), min(dm_residuals))
                max_val = max(max(dm_klein_predicted), max(dm_residuals))
                ax2.plot([min_val, max_val], [min_val, max_val], 'r--', 
                        linewidth=2, label='Perfect Klein Correlation')
            
            ax2.set_xlabel('Predicted Klein DM (pc cm⁻³)')
            ax2.set_ylabel('Observed DM Residual (pc cm⁻³)')
            ax2.set_title('B. Predicted vs Observed Klein DM')
            ax2.legend()
            ax2.grid(True, alpha=0.3)
            
            # 3. Results summary
            ax3 = axes[1, 0]
            ax3.axis('off')
            
            stats_data = self.dispersion_analysis['statistical_tests']
            distance_data = self.dispersion_analysis['distance_correlation']
            freq_data = self.dispersion_analysis['frequency_dependence']
            
            summary_text = f"""
FRB KLEIN DISPERSION ANALYSIS

THEORETICAL PREDICTIONS:
• Klein DM per Mpc: {self.DM_klein_per_Mpc:.2e} pc cm⁻³/Mpc
• Klein-EM coupling: γ_EM = {self.gamma_em:.2e}
• Additional frequency-dependent delay

DISTANCE CORRELATION:
• DM-distance correlation: {distance_data['correlation']:.4f}
• Klein correlation: {distance_data['klein_correlation']:.4f}
• Slope significance: {distance_data['significance']:.2f}σ

FREQUENCY ANALYSIS:
• Frequency correlation: {freq_data['correlation']:.4f}
• Frequency significance: {freq_data['significance']:.2f}σ

STATISTICAL TESTS:
• Positive residuals: {stats_data['positive_residuals']}/{stats_data['total_residuals']}
• Mean excess significance: {stats_data['mean_significance']:.2f}σ
• Combined significance: {stats_data['combined_significance']:.2f}σ

STATUS:
{'✅ KLEIN DISPERSION DETECTED' if stats_data['combined_significance'] > 3 else 
 '🔶 MARGINAL DETECTION' if stats_data['combined_significance'] > 2 else 
 '❌ NO DISPERSION SIGNATURE'}
            """
            
            color = ('green' if stats_data['combined_significance'] > 3 else 
                    'orange' if stats_data['combined_significance'] > 2 else 'red')
            ax3.text(0.05, 0.95, summary_text, transform=ax3.transAxes,
                    fontsize=9, verticalalignment='top', fontfamily='monospace',
                    color=color)
            
            # 4. DM residual histogram
            ax4 = axes[1, 1]
            
            ax4.hist(dm_residuals, bins=20, alpha=0.7, density=True, color='skyblue')
            ax4.axvline(np.mean(dm_residuals), color='red', linestyle='--', linewidth=2,
                       label=f'Mean: {np.mean(dm_residuals):.2e}')
            ax4.axvline(0, color='gray', linestyle='-', alpha=0.5, label='No Excess')
            
            # Klein prediction distribution
            if len(dm_klein_predicted) > 0:
                ax4.axvline(np.mean(dm_klein_predicted), color='orange', linestyle='--', 
                           linewidth=2, label=f'Klein: {np.mean(dm_klein_predicted):.2e}')
            
            ax4.set_xlabel('DM Residual (pc cm⁻³)')
            ax4.set_ylabel('Probability Density')
            ax4.set_title('C. DM Residual Distribution')
            ax4.legend()
            ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('frb_klein_dispersion_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print("✅ FRB Klein dispersion visualization saved")

def main():
    """Main FRB Klein dispersion analysis"""
    analyzer = FRBKleinDispersionAnalyzer()
    
    if analyzer.generate_representative_frb_data():
        results = analyzer.analyze_klein_dispersion()
        analyzer.create_visualization()
        
        stats = results['statistical_tests']
        distance = results['distance_correlation']
        
        print(f"\\n📡 FRB KLEIN DISPERSION RESULTS:")
        print(f"   • Combined significance: {stats['combined_significance']:.2f}σ")
        print(f"   • Distance correlation: {distance['correlation']:.4f}")
        print(f"   • Klein correlation: {distance['klein_correlation']:.4f}")
        print(f"   • Positive residuals: {stats['positive_residuals']}/{stats['total_residuals']}")
        
        status = ('DETECTED' if stats['combined_significance'] > 3 else 
                 'MARGINAL' if stats['combined_significance'] > 2 else 'NOT DETECTED')
        print(f"   • Status: Klein dispersion {status}")
        
        return results
    return None

if __name__ == "__main__":
    main()