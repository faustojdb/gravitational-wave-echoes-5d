#!/usr/bin/env python3
"""
Atomic Clock Klein Timing Analyzer
===================================

OBJECTIVE: Search for Klein electromagnetic timing variations in atomic clock data
APPROACH: Parameter-free analysis of systematic frequency variations
TARGET: Klein timing variations Δf/f ≈ γ_EM ≈ 10⁻¹⁵

Theory: Klein electromagnetic coupling causes systematic atomic clock frequency shifts
Prediction: Correlated timing variations across global atomic clock network
Critical Test: Most sensitive electromagnetic precision measurement
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats, signal
from typing import Dict, List, Tuple
import warnings
warnings.filterwarnings('ignore')

class AtomicClockKleinTimingAnalyzer:
    """Atomic clock network analysis for Klein electromagnetic timing detection"""
    
    def __init__(self):
        # Klein electromagnetic predictions (NO free parameters)
        self.f0_klein = 5.68  # Hz (Klein oscillation frequency)
        self.gamma_em = 1e-15  # Klein-EM coupling strength
        self.predicted_frequency_variation = self.gamma_em  # Δf/f
        
        print(f"Atomic Clock Klein Timing Analysis")
        print(f"=" * 40)
        print(f"Klein frequency: f₀ = {self.f0_klein} Hz")
        print(f"Klein-EM coupling: γ_EM = {self.gamma_em:.2e}")
        print(f"Predicted frequency variation: Δf/f ≈ {self.predicted_frequency_variation:.2e}")
        
        # Analysis data
        self.clock_data = {}
        self.timing_analysis = {}
        
    def generate_representative_clock_data(self) -> bool:
        """Generate representative atomic clock network data"""
        
        print("\\n⏰ Generating Representative Atomic Clock Network Data...")
        print("(Note: Using simulated data representative of TAI network precision)")
        
        # Time span: 10 years of atomic clock comparisons
        observation_span = 10 * 365.25 * 24 * 3600  # seconds
        measurement_interval = 24 * 3600  # Daily measurements
        measurement_times = np.arange(0, observation_span, measurement_interval)
        n_measurements = len(measurement_times)
        
        # Generate global atomic clock network (representative of TAI)
        clock_locations = [
            {'name': 'NIST_USA', 'lat': 40.0, 'lon': -105.0},
            {'name': 'PTB_Germany', 'lat': 52.3, 'lon': 10.5},
            {'name': 'INRIM_Italy', 'lat': 45.0, 'lon': 7.7},
            {'name': 'NMIJ_Japan', 'lat': 36.0, 'lon': 140.1},
            {'name': 'NRC_Canada', 'lat': 45.4, 'lon': -75.7},
            {'name': 'NPL_UK', 'lat': 51.4, 'lon': -0.3},
            {'name': 'LNE_France', 'lat': 48.8, 'lon': 2.3},
            {'name': 'KRISS_Korea', 'lat': 37.5, 'lon': 127.0},
            {'name': 'NIM_China', 'lat': 39.9, 'lon': 116.4},
            {'name': 'VNIIFTRI_Russia', 'lat': 55.8, 'lon': 38.0}
        ]
        
        clocks = []
        
        for clock_info in clock_locations:
            # Clock properties
            clock_name = clock_info['name']
            
            # Atomic clock stability (realistic values)
            short_term_stability = np.random.uniform(1e-16, 5e-16)  # Allan deviation at 1 day
            long_term_drift = np.random.uniform(-1e-17, 1e-17) / (365.25 * 24 * 3600)  # per second
            
            # Generate frequency measurements relative to TAI
            
            # 1. White frequency noise
            white_noise = np.random.normal(0, short_term_stability, n_measurements)
            
            # 2. Random walk frequency noise (typical for atomic clocks)
            random_walk_coefficient = short_term_stability * 0.1
            random_walk = np.cumsum(np.random.normal(0, random_walk_coefficient / np.sqrt(measurement_interval), n_measurements))
            
            # 3. Linear drift
            linear_drift = long_term_drift * measurement_times
            
            # 4. Environmental effects (temperature, magnetic field, etc.)
            daily_cycle = 1e-16 * np.sin(2*np.pi * measurement_times / (24*3600))
            annual_cycle = 5e-17 * np.sin(2*np.pi * measurement_times / (365.25*24*3600))
            
            # 5. Klein electromagnetic timing variations (the signal we're searching for!)
            # Klein coupling should cause correlated variations across the network
            
            # Global Klein electromagnetic field variations
            klein_global_phase = np.random.uniform(0, 2*np.pi)
            klein_amplitude = self.predicted_frequency_variation
            
            # Klein timing variation at fundamental frequency
            klein_timing_main = klein_amplitude * np.sin(2*np.pi * self.f0_klein * measurement_times + klein_global_phase)
            
            # Klein harmonics (smaller amplitude)
            klein_timing_harmonics = 0
            for harmonic in [2, 3]:
                harm_phase = np.random.uniform(0, 2*np.pi)
                harm_amplitude = klein_amplitude / harmonic**2
                klein_timing_harmonics += harm_amplitude * np.sin(2*np.pi * harmonic * self.f0_klein * measurement_times + harm_phase)
            
            # Location-dependent Klein coupling (geographic variation)
            latitude = clock_info['lat']
            longitude = clock_info['lon']
            
            # Klein field strength varies with location (hypothetical pattern)
            location_factor = 1 + 0.1 * np.sin(np.radians(latitude)) * np.cos(np.radians(longitude))
            
            klein_timing_total = (klein_timing_main + klein_timing_harmonics) * location_factor
            
            # 6. Total frequency variations
            total_frequency_variations = (white_noise + random_walk + linear_drift + 
                                        daily_cycle + annual_cycle + klein_timing_total)
            
            clocks.append({
                'name': clock_name,
                'latitude': latitude,
                'longitude': longitude,
                'short_term_stability': short_term_stability,
                'long_term_drift': long_term_drift,
                'measurement_times': measurement_times.copy(),
                'frequency_variations': total_frequency_variations,
                'white_noise': white_noise,
                'random_walk': random_walk,
                'linear_drift': linear_drift,
                'environmental': daily_cycle + annual_cycle,
                'klein_component': klein_timing_total,
                'klein_global_phase': klein_global_phase,
                'location_factor': location_factor
            })
            
        self.clock_data = {
            'clocks': clocks,
            'n_clocks': len(clocks),
            'observation_span': observation_span,
            'measurement_interval': measurement_interval,
            'n_measurements': n_measurements
        }
        
        print(f"✅ Generated {len(clocks)} atomic clocks")
        print(f"   • Observation span: {observation_span/(365.25*24*3600):.1f} years")
        print(f"   • Measurement interval: {measurement_interval/(24*3600):.1f} days")
        print(f"   • Total measurements per clock: {n_measurements}")
        print(f"   • Clock stability: 10⁻¹⁶ level (TAI-representative)")
        
        return True
        
    def analyze_klein_timing_signatures(self) -> Dict:
        """Search for Klein electromagnetic timing signatures"""
        
        print("\\n🔍 Searching for Klein Electromagnetic Timing Signatures...")
        
        results = {
            'frequency_domain_analysis': {},
            'cross_correlation_analysis': {},
            'network_coherence': {},
            'statistical_tests': {}
        }
        
        clocks = self.clock_data['clocks']
        measurement_times = clocks[0]['measurement_times']  # All clocks have same times
        
        # 1. Frequency domain analysis
        # Look for peaks at Klein frequency f₀ = 5.68 Hz
        
        klein_powers = []
        klein_snrs = []
        
        for clock in clocks:
            freq_variations = clock['frequency_variations']
            
            # Power spectral density
            dt = self.clock_data['measurement_interval']
            frequencies, psd = signal.welch(freq_variations, fs=1/dt, nperseg=len(freq_variations)//4)
            
            # Find Klein frequency peak
            klein_freq_idx = np.argmin(np.abs(frequencies - self.f0_klein))
            klein_power = psd[klein_freq_idx] if klein_freq_idx < len(psd) else 0
            
            # Background power (excluding Klein frequency region)
            freq_mask = np.abs(frequencies - self.f0_klein) > 0.5 * self.f0_klein
            background_power = np.median(psd[freq_mask]) if np.any(freq_mask) else 1
            
            klein_snr = klein_power / background_power if background_power > 0 else 0
            
            klein_powers.append(klein_power)
            klein_snrs.append(klein_snr)
            
        # Average Klein signal across network
        mean_klein_snr = np.mean(klein_snrs)
        klein_snr_std = np.std(klein_snrs)
        
        results['frequency_domain_analysis'] = {
            'klein_frequency': self.f0_klein,
            'individual_powers': klein_powers,
            'individual_snrs': klein_snrs,
            'mean_klein_snr': mean_klein_snr,
            'klein_snr_std': klein_snr_std
        }
        
        # 2. Cross-correlation analysis
        # Klein signals should be correlated across the network
        
        all_correlations = []
        klein_template = np.sin(2*np.pi * self.f0_klein * measurement_times)
        
        # Correlate each clock with Klein template
        template_correlations = []
        for clock in clocks:
            freq_variations = clock['frequency_variations']
            
            # Cross-correlation with Klein frequency template
            correlation = np.corrcoef(freq_variations, klein_template)[0, 1]
            if not np.isnan(correlation):
                template_correlations.append(correlation)
            else:
                template_correlations.append(0)
                
        # Cross-correlations between clocks (Klein should be coherent)
        inter_clock_correlations = []
        for i in range(len(clocks)):
            for j in range(i+1, len(clocks)):
                freq_i = clocks[i]['frequency_variations']
                freq_j = clocks[j]['frequency_variations']
                
                correlation = np.corrcoef(freq_i, freq_j)[0, 1]
                if not np.isnan(correlation):
                    inter_clock_correlations.append(correlation)
                    
        mean_template_correlation = np.mean(template_correlations)
        mean_inter_correlation = np.mean(inter_clock_correlations) if inter_clock_correlations else 0
        
        results['cross_correlation_analysis'] = {
            'template_correlations': template_correlations,
            'inter_clock_correlations': inter_clock_correlations,
            'mean_template_correlation': mean_template_correlation,
            'mean_inter_correlation': mean_inter_correlation
        }
        
        # 3. Network coherence analysis
        # Test for global Klein electromagnetic field
        
        # Stack all clock measurements
        stacked_variations = np.zeros(len(measurement_times))
        for clock in clocks:
            stacked_variations += clock['frequency_variations']
        stacked_variations /= len(clocks)
        
        # Correlation of stacked signal with Klein template
        stacked_correlation = np.corrcoef(stacked_variations, klein_template)[0, 1]
        if np.isnan(stacked_correlation):
            stacked_correlation = 0
            
        # Network coherence: variance reduction from stacking
        individual_variances = [np.var(clock['frequency_variations']) for clock in clocks]
        mean_individual_variance = np.mean(individual_variances)
        stacked_variance = np.var(stacked_variations)
        
        # Coherence factor (should be ~1/N_clocks if purely uncorrelated)
        expected_stacked_variance = mean_individual_variance / len(clocks)
        coherence_factor = stacked_variance / expected_stacked_variance if expected_stacked_variance > 0 else 1
        
        results['network_coherence'] = {
            'stacked_correlation': stacked_correlation,
            'coherence_factor': coherence_factor,
            'stacked_variance': stacked_variance,
            'expected_variance': expected_stacked_variance
        }
        
        # 4. Statistical tests
        
        # Test 1: Is mean Klein SNR significantly > 1?
        if len(klein_snrs) > 1:
            snr_significance = (mean_klein_snr - 1) / (klein_snr_std / np.sqrt(len(klein_snrs)))
            snr_significance = max(0, snr_significance)  # Only positive excesses
        else:
            snr_significance = 0
            
        # Test 2: Are template correlations systematically positive?
        if len(template_correlations) > 0:
            try:
                result = stats.binomtest(sum(1 for c in template_correlations if c > 0), 
                                       len(template_correlations), 0.5)
                template_p_value = result.pvalue
            except AttributeError:
                # Fallback for older scipy
                positive_count = sum(1 for c in template_correlations if c > 0)
                total_count = len(template_correlations)
                template_p_value = stats.binom_test(positive_count, total_count, 0.5)
                
            if template_p_value > 0:
                template_significance = stats.norm.ppf(1 - template_p_value/2)
            else:
                template_significance = 0
        else:
            template_significance = 0
            
        # Test 3: Is stacked correlation significant?
        n_measurements = len(measurement_times)
        if n_measurements > 3:
            stacked_significance = np.abs(stacked_correlation) * np.sqrt(n_measurements - 2)
        else:
            stacked_significance = 0
            
        # Combined significance
        combined_significance = np.sqrt(snr_significance**2 + 
                                      template_significance**2 + 
                                      stacked_significance**2)
        
        results['statistical_tests'] = {
            'snr_significance': snr_significance,
            'template_significance': template_significance,
            'stacked_significance': stacked_significance,
            'combined_significance': combined_significance,
            'template_p_value': template_p_value if 'template_p_value' in locals() else 1
        }
        
        self.timing_analysis = results
        return results
        
    def create_visualization(self):
        """Create Klein timing analysis visualization"""
        
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('Atomic Clock Network: Klein Electromagnetic Timing Detection', 
                     fontweight='bold', fontsize=14)
        
        # 1. Individual clock Klein SNR
        ax1 = axes[0, 0]
        
        freq_data = self.timing_analysis['frequency_domain_analysis']
        snrs = freq_data['individual_snrs']
        clock_names = [clock['name'] for clock in self.clock_data['clocks']]
        
        colors = ['red' if snr > 3 else 'orange' if snr > 2 else 'blue' for snr in snrs]
        bars = ax1.bar(range(len(snrs)), snrs, color=colors, alpha=0.7)
        
        ax1.axhline(1, color='gray', linestyle='-', alpha=0.5, label='Background Level')
        ax1.axhline(2, color='orange', linestyle='--', alpha=0.7, label='2× Background')
        ax1.axhline(3, color='red', linestyle='--', alpha=0.7, label='3× Background')
        
        ax1.set_xticks(range(len(clock_names)))
        ax1.set_xticklabels([name.split('_')[0] for name in clock_names], rotation=45)
        ax1.set_ylabel('Klein Frequency SNR')
        ax1.set_title('A. Individual Clock Klein Signal')
        ax1.legend()
        ax1.grid(True, alpha=0.3, axis='y')
        
        # 2. Template correlation distribution
        ax2 = axes[0, 1]
        
        corr_data = self.timing_analysis['cross_correlation_analysis']
        template_corrs = corr_data['template_correlations']
        
        ax2.hist(template_corrs, bins=10, alpha=0.7, density=True, color='skyblue')
        ax2.axvline(np.mean(template_corrs), color='red', linestyle='--', linewidth=2,
                   label=f'Mean: {np.mean(template_corrs):.4f}')
        ax2.axvline(0, color='gray', linestyle='-', alpha=0.5, label='No Correlation')
        
        ax2.set_xlabel('Klein Template Correlation')
        ax2.set_ylabel('Probability Density')
        ax2.set_title('B. Klein Template Correlations')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # 3. Results summary
        ax3 = axes[1, 0]
        ax3.axis('off')
        
        stats_data = self.timing_analysis['statistical_tests']
        freq_data = self.timing_analysis['frequency_domain_analysis']
        coherence_data = self.timing_analysis['network_coherence']
        
        summary_text = f"""
ATOMIC CLOCK KLEIN TIMING ANALYSIS

THEORETICAL PREDICTIONS:
• Klein frequency: f₀ = {self.f0_klein} Hz
• Klein-EM coupling: γ_EM = {self.gamma_em:.2e}
• Frequency variation: Δf/f ≈ {self.predicted_frequency_variation:.2e}

FREQUENCY DOMAIN:
• Mean Klein SNR: {freq_data['mean_klein_snr']:.2f}
• SNR significance: {stats_data['snr_significance']:.2f}σ
• Network clocks: {self.clock_data['n_clocks']}

CORRELATION ANALYSIS:
• Mean template correlation: {corr_data['mean_template_correlation']:.4f}
• Template significance: {stats_data['template_significance']:.2f}σ
• Stacked correlation: {coherence_data['stacked_correlation']:.4f}

NETWORK COHERENCE:
• Stacked significance: {stats_data['stacked_significance']:.2f}σ
• Coherence factor: {coherence_data['coherence_factor']:.2f}

COMBINED RESULTS:
• Total significance: {stats_data['combined_significance']:.2f}σ

STATUS:
{'✅ KLEIN TIMING DETECTED' if stats_data['combined_significance'] > 3 else 
 '🔶 MARGINAL DETECTION' if stats_data['combined_significance'] > 2 else 
 '❌ NO TIMING SIGNATURE'}
        """
        
        color = ('green' if stats_data['combined_significance'] > 3 else 
                'orange' if stats_data['combined_significance'] > 2 else 'red')
        ax3.text(0.05, 0.95, summary_text, transform=ax3.transAxes,
                fontsize=9, verticalalignment='top', fontfamily='monospace',
                color=color)
        
        # 4. Time series example
        ax4 = axes[1, 1]
        
        # Show stacked frequency variations vs Klein template
        measurement_times = self.clock_data['measurement_times']
        time_years = measurement_times / (365.25 * 24 * 3600)
        
        # Stacked variations
        stacked_variations = np.zeros(len(measurement_times))
        for clock in self.clock_data['clocks']:
            stacked_variations += clock['frequency_variations']
        stacked_variations /= len(self.clock_data['clocks'])
        
        # Klein template
        klein_template = self.predicted_frequency_variation * np.sin(2*np.pi * self.f0_klein * measurement_times)
        
        ax4.plot(time_years, stacked_variations * 1e15, 'b-', alpha=0.8, 
                label='Stacked Network (×10¹⁵)')
        ax4.plot(time_years, klein_template * 1e15, 'r--', linewidth=2,
                label='Klein Template (×10¹⁵)')
        
        ax4.set_xlabel('Time (Years)')
        ax4.set_ylabel('Frequency Variation (×10⁻¹⁵)')
        ax4.set_title('C. Network vs Klein Template')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('atomic_clock_klein_timing.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print("✅ Atomic clock Klein timing visualization saved")

def main():
    """Main atomic clock Klein timing analysis"""
    analyzer = AtomicClockKleinTimingAnalyzer()
    
    if analyzer.generate_representative_clock_data():
        results = analyzer.analyze_klein_timing_signatures()
        analyzer.create_visualization()
        
        stats = results['statistical_tests']
        freq = results['frequency_domain_analysis']
        coherence = results['network_coherence']
        
        print(f"\\n⏰ ATOMIC CLOCK KLEIN TIMING RESULTS:")
        print(f"   • Combined significance: {stats['combined_significance']:.2f}σ")
        print(f"   • Mean Klein SNR: {freq['mean_klein_snr']:.2f}")
        print(f"   • Stacked correlation: {coherence['stacked_correlation']:.4f}")
        print(f"   • Network coherence: {coherence['coherence_factor']:.2f}")
        
        status = ('DETECTED' if stats['combined_significance'] > 3 else 
                 'MARGINAL' if stats['combined_significance'] > 2 else 'NOT DETECTED')
        print(f"   • Status: Klein electromagnetic timing {status}")
        
        return results
    return None

if __name__ == "__main__":
    main()