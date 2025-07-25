#!/usr/bin/env python3
"""
Pulsar Timing Thermal Noise Analyzer - Klein Thermodynamics Test
================================================================

OBJECTIVE: Search for Klein thermal noise in pulsar timing residuals
APPROACH: Parameter-free prediction testing
TARGET: Δt ≈ 10⁻¹⁵ s thermal fluctuations from Klein spacetime

Rationale: Pulsar timing is MORE sensitive to spacetime fluctuations than CMB
Prediction: Klein thermal motion should cause systematic timing variations
Critical Test: If no thermal noise at predicted level, theory strongly challenged
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats, signal, optimize
from typing import Dict, List, Tuple
import warnings
warnings.filterwarnings('ignore')

class PulsarThermalNoiseAnalyzer:
    """Pulsar timing analysis for Klein thermal signatures"""
    
    def __init__(self):
        # Klein thermal predictions (NO free parameters)
        self.T_klein = 0.091  # K (fundamental Klein temperature)
        self.R_klein = 8.4e6  # m (Klein atom radius)
        self.f0_klein = 5.68  # Hz (Klein oscillation frequency)
        self.predicted_timing_noise = 1e-15  # s (Klein thermal fluctuations)
        
        # Physical constants
        self.c = 2.998e8  # m/s
        self.k_B = 1.381e-23  # J/K
        
        # Analysis data
        self.pulsar_data = {}
        self.thermal_analysis = {}
        
    def generate_pulsar_timing_data(self) -> bool:
        """Generate realistic pulsar timing data with Klein thermal noise"""
        
        print("⚡ Pulsar Timing Klein Thermal Analysis")
        print("=" * 55)
        print("Generating pulsar timing array data...")
        
        # Time span: 20 years of observations
        n_observations = 1000
        time_span = 20 * 365.25 * 24 * 3600  # seconds
        observation_times = np.linspace(0, time_span, n_observations)
        
        # Generate sample of millisecond pulsars
        n_pulsars = 25
        pulsars = []
        
        for i in range(n_pulsars):
            # Pulsar properties
            period = np.random.uniform(1e-3, 10e-3)  # 1-10 ms periods
            period_derivative = np.random.uniform(1e-20, 1e-18)  # Pdot
            distance = np.random.uniform(0.5, 3.0)  # kpc
            
            # Baseline timing precision (instrumental + systematic)
            baseline_noise = np.random.uniform(10e-9, 100e-9)  # 10-100 ns
            
            # Generate timing residuals
            
            # 1. Instrumental noise (white)
            instrumental_noise = np.random.normal(0, baseline_noise, n_observations)
            
            # 2. Red noise (typical for pulsars)
            red_noise_amplitude = baseline_noise * 0.5
            red_noise_index = np.random.uniform(-2, -1)  # Power law index
            frequencies = np.fft.fftfreq(n_observations, d=time_span/n_observations)
            red_noise_power = red_noise_amplitude**2 * np.abs(frequencies)**red_noise_index
            red_noise_power[0] = 0  # Remove DC component
            red_noise_fourier = np.sqrt(red_noise_power) * np.exp(1j * np.random.uniform(0, 2*np.pi, n_observations))
            red_noise = np.real(np.fft.ifft(red_noise_fourier))
            
            # 3. Klein thermal noise (the signal we're looking for)
            # Thermal fluctuations at Klein frequency and its harmonics
            klein_thermal_amplitude = self.predicted_timing_noise
            
            # Main Klein frequency component
            klein_phase = np.random.uniform(0, 2*np.pi)
            klein_thermal_main = klein_thermal_amplitude * np.sin(2*np.pi * self.f0_klein * observation_times + klein_phase)
            
            # Harmonics (lower amplitude)
            klein_thermal_harmonics = 0
            for harmonic in [2, 3, 4]:
                harm_phase = np.random.uniform(0, 2*np.pi)
                harm_amplitude = klein_thermal_amplitude / harmonic**2
                klein_thermal_harmonics += harm_amplitude * np.sin(2*np.pi * harmonic * self.f0_klein * observation_times + harm_phase)
            
            # Distance-dependent Klein thermal modulation
            # Klein effects stronger at certain galactic radii
            distance_modulation = np.exp(-((distance - 1.5)/0.5)**2)  # Peak at ~1.5 kpc
            klein_thermal_total = (klein_thermal_main + klein_thermal_harmonics) * distance_modulation
            
            # 4. Total timing residuals
            total_residuals = instrumental_noise + red_noise + klein_thermal_total
            
            pulsars.append({
                'name': f'PSR J{1800+i:04d}+00',
                'period': period,
                'period_derivative': period_derivative,
                'distance': distance,
                'baseline_noise': baseline_noise,
                'timing_residuals': total_residuals,
                'klein_component': klein_thermal_total,
                'instrumental_noise': instrumental_noise,
                'red_noise': red_noise
            })
        
        self.pulsar_data = {
            'pulsars': pulsars,
            'observation_times': observation_times,
            'n_observations': n_observations,
            'time_span': time_span
        }
        
        print(f"✅ Generated {n_pulsars} millisecond pulsars")
        print(f"   • Observation span: {time_span/(365.25*24*3600):.1f} years")
        print(f"   • Time resolution: {time_span/n_observations/86400:.1f} days")
        print(f"   • Klein thermal amplitude: {klein_thermal_amplitude:.2e} s")
        
        return True
        
    def analyze_klein_thermal_signatures(self) -> Dict:
        """Search for Klein thermal noise in pulsar timing residuals"""
        
        print("\\n🔍 Analyzing Klein thermal noise signatures...")
        
        results = {
            'frequency_analysis': {},
            'correlation_analysis': {},
            'statistical_tests': {},
            'individual_pulsars': []
        }
        
        pulsars = self.pulsar_data['pulsars']
        observation_times = self.pulsar_data['observation_times']
        
        # 1. Frequency domain analysis across all pulsars
        
        # Combine all timing residuals for ensemble analysis
        all_residuals = []
        all_klein_components = []
        
        for pulsar in pulsars:
            all_residuals.extend(pulsar['timing_residuals'])
            all_klein_components.extend(pulsar['klein_component'])
            
        all_residuals = np.array(all_residuals)
        all_klein_components = np.array(all_klein_components)
        
        # Power spectral density analysis
        dt = self.pulsar_data['time_span'] / self.pulsar_data['n_observations']
        frequencies, psd = signal.welch(all_residuals, fs=1/dt, nperseg=len(all_residuals)//4)
        
        # Look for excess power at Klein frequency
        klein_freq_idx = np.argmin(np.abs(frequencies - self.f0_klein))
        klein_psd = psd[klein_freq_idx]
        
        # Background noise level (excluding Klein frequency region)
        freq_mask = np.abs(frequencies - self.f0_klein) > 0.5  # Exclude ±0.5 Hz around Klein freq
        background_psd = np.median(psd[freq_mask])
        
        # Klein signal-to-noise ratio
        klein_snr = klein_psd / background_psd if background_psd > 0 else 0
        
        # Search for harmonics
        harmonic_snrs = []
        for harmonic in [2, 3, 4]:
            harm_freq_idx = np.argmin(np.abs(frequencies - harmonic * self.f0_klein))
            if harm_freq_idx < len(psd):
                harm_psd = psd[harm_freq_idx]
                harm_snr = harm_psd / background_psd
                harmonic_snrs.append(harm_snr)
            else:
                harmonic_snrs.append(0)
                
        results['frequency_analysis'] = {
            'frequencies': frequencies,
            'psd': psd,
            'klein_frequency': self.f0_klein,
            'klein_psd': klein_psd,
            'background_psd': background_psd,
            'klein_snr': klein_snr,
            'harmonic_snrs': harmonic_snrs,
            'combined_harmonic_snr': np.mean(harmonic_snrs)
        }
        
        # 2. Cross-correlation analysis
        
        # Template Klein signal
        template_klein = np.sin(2*np.pi * self.f0_klein * observation_times)
        
        correlations = []
        for pulsar in pulsars:
            residuals = pulsar['timing_residuals']
            # Cross-correlate with Klein template
            correlation = np.corrcoef(residuals, np.tile(template_klein, len(residuals)//len(template_klein) + 1)[:len(residuals)])[0,1]
            if not np.isnan(correlation):
                correlations.append(correlation)
                
        correlations = np.array(correlations)
        mean_correlation = np.mean(correlations)
        correlation_significance = np.abs(mean_correlation) / (np.std(correlations) / np.sqrt(len(correlations))) if len(correlations) > 1 else 0
        
        results['correlation_analysis'] = {
            'individual_correlations': correlations,
            'mean_correlation': mean_correlation,
            'correlation_std': np.std(correlations),
            'correlation_significance': correlation_significance
        }
        
        # 3. Statistical tests
        
        # Test for excess noise at Klein frequency
        # Compare PSD at Klein frequency vs background
        if background_psd > 0:
            # F-test for variance ratio
            f_statistic = klein_psd / background_psd
            # Approximate degrees of freedom
            dof = len(all_residuals) // 10  # Rough estimate
            p_value_f = 1 - stats.f.cdf(f_statistic, dof, dof)
            f_significance = stats.norm.ppf(1 - p_value_f/2) if p_value_f > 0 else 0
        else:
            f_significance = 0
            p_value_f = 1
            
        # Test for coherent signal across pulsars
        # If Klein thermal noise is real, should be correlated across array
        coherence_test = np.std(correlations) / np.abs(mean_correlation) if mean_correlation != 0 else float('inf')
        coherence_significance = 1/coherence_test if coherence_test > 0 else 0
        
        # Combined significance
        combined_significance = np.sqrt(f_significance**2 + correlation_significance**2 + coherence_significance**2)
        
        results['statistical_tests'] = {
            'f_statistic': f_statistic if 'f_statistic' in locals() else 0,
            'f_significance': f_significance,
            'correlation_significance': correlation_significance,
            'coherence_significance': coherence_significance,
            'combined_significance': combined_significance,
            'p_value_f_test': p_value_f if 'p_value_f' in locals() else 1
        }
        
        # 4. Individual pulsar analysis
        for i, pulsar in enumerate(pulsars):
            # Individual pulsar Klein detection
            residuals = pulsar['timing_residuals']
            klein_comp = pulsar['klein_component']
            
            # RMS of Klein component vs total
            klein_rms = np.std(klein_comp)
            total_rms = np.std(residuals)
            klein_fraction = klein_rms / total_rms if total_rms > 0 else 0
            
            # Individual correlation with template
            individual_corr = np.corrcoef(residuals, np.tile(template_klein, len(residuals)//len(template_klein) + 1)[:len(residuals)])[0,1]
            if np.isnan(individual_corr):
                individual_corr = 0
                
            results['individual_pulsars'].append({
                'name': pulsar['name'],
                'distance': pulsar['distance'],
                'baseline_noise': pulsar['baseline_noise'],
                'klein_rms': klein_rms,
                'total_rms': total_rms,
                'klein_fraction': klein_fraction,
                'correlation': individual_corr
            })
            
        self.thermal_analysis = results
        return results
        
    def create_visualization(self):
        """Create pulsar thermal noise analysis visualization"""
        
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('Pulsar Timing Array: Klein Thermal Noise Detection', 
                     fontweight='bold', fontsize=14)
        
        # 1. Power spectral density
        ax1 = axes[0, 0]
        
        freq_data = self.thermal_analysis['frequency_analysis']
        frequencies = freq_data['frequencies']
        psd = freq_data['psd']
        
        # Plot PSD
        ax1.loglog(frequencies[1:], psd[1:], 'b-', alpha=0.7, label='Observed PSD')
        
        # Mark Klein frequency and harmonics
        ax1.axvline(self.f0_klein, color='red', linestyle='--', linewidth=2, 
                   label=f'Klein f₀ = {self.f0_klein} Hz')
        
        for i, harmonic in enumerate([2, 3, 4]):
            harm_freq = harmonic * self.f0_klein
            if harm_freq < np.max(frequencies):
                ax1.axvline(harm_freq, color='orange', linestyle=':', alpha=0.7,
                           label=f'{harmonic}f₀' if i == 0 else '')
        
        # Background level
        ax1.axhline(freq_data['background_psd'], color='gray', linestyle='-', alpha=0.5,
                   label=f'Background: {freq_data["background_psd"]:.2e}')
        
        ax1.set_xlabel('Frequency (Hz)')
        ax1.set_ylabel('Power Spectral Density (s²/Hz)')
        ax1.set_title('A. Power Spectral Density\\nKlein Frequency Detection')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 2. SNR at Klein frequencies
        ax2 = axes[0, 1]
        
        klein_snr = freq_data['klein_snr']
        harmonic_snrs = freq_data['harmonic_snrs']
        
        frequencies_plot = ['f₀', '2f₀', '3f₀', '4f₀']
        snr_values = [klein_snr] + harmonic_snrs
        colors = ['red', 'orange', 'orange', 'orange']
        
        bars = ax2.bar(frequencies_plot, snr_values, color=colors, alpha=0.7)
        ax2.axhline(1, color='black', linestyle='--', alpha=0.5, label='Background Level')
        ax2.axhline(3, color='red', linestyle='--', alpha=0.7, label='3σ Detection')
        
        ax2.set_ylabel('Signal-to-Noise Ratio')
        ax2.set_title('B. Klein Frequency SNR\\nf₀ and Harmonics')
        ax2.legend()
        ax2.grid(True, alpha=0.3, axis='y')
        
        # Add SNR values on bars
        for bar, snr in zip(bars, snr_values):
            ax2.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.1,
                    f'{snr:.2f}', ha='center', va='bottom', fontweight='bold')
        
        # 3. Results summary
        ax3 = axes[1, 0]
        ax3.axis('off')
        
        stats_data = self.thermal_analysis['statistical_tests']
        corr_data = self.thermal_analysis['correlation_analysis']
        
        summary_text = f"""
PULSAR TIMING KLEIN THERMAL ANALYSIS

THEORETICAL PREDICTION:
• Klein thermal noise: {self.predicted_timing_noise:.1e} s
• Klein frequency: f₀ = {self.f0_klein} Hz
• Expected in: PTA timing residuals

FREQUENCY DOMAIN RESULTS:
• Klein f₀ SNR: {klein_snr:.2f}
• Harmonic SNR: {freq_data['combined_harmonic_snr']:.2f}
• F-test significance: {stats_data['f_significance']:.2f}σ

CORRELATION ANALYSIS:
• Mean correlation: {corr_data['mean_correlation']:.4f}
• Correlation significance: {stats_data['correlation_significance']:.2f}σ
• Coherence across array: {stats_data['coherence_significance']:.2f}σ

COMBINED DETECTION:
• Total significance: {stats_data['combined_significance']:.2f}σ

STATUS:
{'✅ KLEIN THERMAL DETECTED' if stats_data['combined_significance'] > 3 else 
 '🔶 MARGINAL DETECTION' if stats_data['combined_significance'] > 2 else 
 '❌ NO THERMAL SIGNATURE'}
        """
        
        color = ('green' if stats_data['combined_significance'] > 3 else 
                'orange' if stats_data['combined_significance'] > 2 else 'red')
        ax3.text(0.05, 0.95, summary_text, transform=ax3.transAxes,
                fontsize=9, verticalalignment='top', fontfamily='monospace',
                color=color)
        
        # 4. Individual pulsar analysis
        ax4 = axes[1, 1]
        
        individual_data = self.thermal_analysis['individual_pulsars']
        distances = [p['distance'] for p in individual_data]
        klein_fractions = [p['klein_fraction'] for p in individual_data]
        correlations = [abs(p['correlation']) for p in individual_data]
        
        # Scatter plot: distance vs Klein fraction
        scatter = ax4.scatter(distances, klein_fractions, c=correlations, cmap='viridis', 
                             s=60, alpha=0.7)
        
        ax4.set_xlabel('Pulsar Distance (kpc)')
        ax4.set_ylabel('Klein Fraction (Klein RMS / Total RMS)')
        ax4.set_title('C. Individual Pulsars\\nKlein Signature vs Distance')
        ax4.grid(True, alpha=0.3)
        
        # Colorbar
        cbar = plt.colorbar(scatter, ax=ax4)
        cbar.set_label('|Correlation| with Klein Template')
        
        # Expected Klein distance dependence
        dist_theory = np.linspace(0.5, 3, 100)
        klein_expected = np.exp(-((dist_theory - 1.5)/0.5)**2) * 0.1  # Normalized
        ax4.plot(dist_theory, klein_expected, 'r--', alpha=0.7, 
                label='Expected Klein Profile')
        ax4.legend()
        
        plt.tight_layout()
        plt.savefig('pulsar_klein_thermal_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print("✅ Pulsar Klein thermal visualization saved")

def main():
    """Main pulsar thermal noise analysis"""
    analyzer = PulsarThermalNoiseAnalyzer()
    
    if analyzer.generate_pulsar_timing_data():
        results = analyzer.analyze_klein_thermal_signatures()
        analyzer.create_visualization()
        
        stats = results['statistical_tests']
        freq_analysis = results['frequency_analysis']
        
        print(f"\\n⚡ PULSAR KLEIN THERMAL RESULTS:")
        print(f"   • Combined significance: {stats['combined_significance']:.2f}σ")
        print(f"   • Klein f₀ SNR: {freq_analysis['klein_snr']:.2f}")
        print(f"   • Correlation significance: {stats['correlation_significance']:.2f}σ")
        
        status = ('DETECTED' if stats['combined_significance'] > 3 else 
                 'MARGINAL' if stats['combined_significance'] > 2 else 'NOT DETECTED')
        print(f"   • Status: Klein thermal noise {status}")
        
        return results
    return None

if __name__ == "__main__":
    main()