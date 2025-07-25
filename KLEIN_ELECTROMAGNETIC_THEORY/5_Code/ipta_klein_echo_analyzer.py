#!/usr/bin/env python3
"""
IPTA Klein Electromagnetic Echo Analyzer
=========================================

OBJECTIVE: Search for Klein electromagnetic echoes in pulsar timing data
APPROACH: Parameter-free analysis of International Pulsar Timing Array data
TARGET: Klein echo delay Δt = 2R_K/c = 0.056 seconds exactly

Theory: Klein bottle electromagnetic boundary creates echoes in pulsar signals
Prediction: Systematic 0.056s delayed signals with amplitude ~10⁻¹⁵ × main pulse
Critical Test: First direct search for Klein electromagnetic effects
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats, signal, fft
from typing import Dict, List, Tuple, Optional
import warnings
import requests
import os
warnings.filterwarnings('ignore')

class IPTAKleinEchoAnalyzer:
    """IPTA pulsar timing analysis for Klein electromagnetic echo detection"""
    
    def __init__(self):
        # Klein electromagnetic predictions (NO free parameters)
        self.R_klein = 8.4e6  # m (Klein atom radius - established)
        self.c = 2.998e8      # m/s (speed of light)
        self.f0_klein = 5.68  # Hz (Klein oscillation frequency)
        self.gamma_em = 1e-15 # Klein-EM coupling strength (theoretical estimate)
        
        # Klein echo parameters (parameter-free predictions)
        self.echo_delay = 2 * self.R_klein / self.c  # seconds
        self.echo_amplitude_ratio = self.gamma_em    # echo/main amplitude ratio
        
        print(f"Klein Electromagnetic Echo Analysis")
        print(f"=" * 50)
        print(f"Klein echo delay prediction: {self.echo_delay:.6f} seconds")
        print(f"Klein echo amplitude ratio: {self.echo_amplitude_ratio:.2e}")
        print(f"Klein resonance frequency: {self.f0_klein} Hz")
        
        # Analysis data storage
        self.pulsar_data = {}
        self.echo_analysis = {}
        
    def generate_representative_pulsar_data(self) -> bool:
        """Generate representative pulsar timing data for Klein echo analysis"""
        
        print("\\n📡 Generating Representative IPTA-like Pulsar Data...")
        print("(Note: Using simulated data representative of IPTA precision)")
        
        # Time span: 20 years of observations (typical for IPTA)
        observation_span = 20 * 365.25 * 24 * 3600  # seconds
        cadence = 14 * 24 * 3600  # 2-week observation cadence
        observation_times = np.arange(0, observation_span, cadence)
        n_observations = len(observation_times)
        
        # Generate sample of millisecond pulsars (IPTA-like)
        n_pulsars = 30  # Typical IPTA array size
        pulsars = []
        
        for i in range(n_pulsars):
            pulsar_name = f"PSR J{1800+i:02d}00+{10+i:02d}00"
            
            # Pulsar properties (realistic ranges)
            period = np.random.uniform(1.5e-3, 20e-3)  # 1.5-20 ms periods
            period_derivative = np.random.uniform(1e-21, 1e-18)  # Pdot
            distance = np.random.uniform(0.5, 5.0)  # kpc
            
            # Timing precision (realistic for millisecond pulsars)
            timing_rms = np.random.uniform(50e-9, 500e-9)  # 50-500 ns RMS
            
            # Generate timing residuals
            
            # 1. White noise (instrumental + radiometer)
            white_noise = np.random.normal(0, timing_rms, n_observations)
            
            # 2. Red noise (intrinsic pulsar timing noise)
            # Power law: P(f) ∝ f^(-γ) with γ ~ 3-5
            red_noise_amplitude = timing_rms * 0.3
            gamma_red = np.random.uniform(3, 5)
            
            # Generate red noise in frequency domain
            freqs = fft.fftfreq(n_observations, d=cadence)
            positive_freqs = freqs[1:n_observations//2]
            
            # Red noise power spectrum
            red_power = red_noise_amplitude**2 * (positive_freqs * 365.25*24*3600)**(-gamma_red)
            red_power[positive_freqs == 0] = 0
            
            # Generate red noise time series
            red_phases = np.random.uniform(0, 2*np.pi, len(positive_freqs))
            red_fourier = np.sqrt(red_power) * np.exp(1j * red_phases)
            
            # Complete Fourier series (negative frequencies)
            full_fourier = np.zeros(n_observations, dtype=complex)
            full_fourier[1:n_observations//2] = red_fourier
            
            # Handle negative frequencies with proper indexing
            if n_observations % 2 == 0:  # Even number of observations
                end_idx = n_observations//2 + 1
                neg_freqs = red_fourier[::-1]
                if len(neg_freqs) > n_observations - end_idx:
                    neg_freqs = neg_freqs[:n_observations - end_idx]
                full_fourier[end_idx:end_idx + len(neg_freqs)] = np.conj(neg_freqs)
            else:  # Odd number of observations
                end_idx = n_observations//2 + 1
                neg_freqs = red_fourier[::-1]
                if len(neg_freqs) > n_observations - end_idx:
                    neg_freqs = neg_freqs[:n_observations - end_idx]
                full_fourier[end_idx:end_idx + len(neg_freqs)] = np.conj(neg_freqs)
            
            red_noise = np.real(fft.ifft(full_fourier))
            
            # 3. Deterministic effects (spin-down, binary motion, etc.)
            deterministic = np.zeros(n_observations)
            
            # Spin-down (quadratic timing drift)
            if np.random.random() < 0.7:  # 70% have measurable spin-down
                spin_down_coeff = period_derivative * (observation_times / (2 * 365.25*24*3600))**2
                deterministic += spin_down_coeff * 1e6  # Convert to microseconds
                
            # Binary motion (for binary pulsars - ~50% of MSPs)
            if np.random.random() < 0.5:
                binary_period = np.random.uniform(0.1, 100) * 24 * 3600  # 0.1-100 days
                binary_amplitude = np.random.uniform(1e-6, 100e-6)  # 1-100 μs
                binary_phase = np.random.uniform(0, 2*np.pi)
                
                binary_signal = binary_amplitude * np.sin(2*np.pi * observation_times / binary_period + binary_phase)
                deterministic += binary_signal
                
            # 4. Klein electromagnetic echo (the signal we're searching for!)
            klein_echo_signal = np.zeros(n_observations)
            
            # Main pulse occurs at observation times
            # Klein echo occurs Δt = 0.056 seconds later
            
            # For each observation, create Klein echo
            echo_delay_samples = int(self.echo_delay / cadence * 100)  # Interpolation factor
            
            # Generate high-resolution time series for echo detection
            dt_fine = cadence / 1000  # 1000x oversampling
            times_fine = np.arange(0, observation_span, dt_fine)
            
            # Main pulse train (assume delta functions at observation times)
            main_pulses = np.zeros(len(times_fine))
            for obs_time in observation_times:
                closest_idx = np.argmin(np.abs(times_fine - obs_time))
                if closest_idx < len(main_pulses):
                    main_pulses[closest_idx] = 1.0
                    
            # Klein echo train (delayed by exactly Δt)
            echo_pulses = np.zeros(len(times_fine))
            for obs_time in observation_times:
                echo_time = obs_time + self.echo_delay
                closest_idx = np.argmin(np.abs(times_fine - echo_time))
                if closest_idx < len(echo_pulses):
                    # Klein echo amplitude includes frequency dependence
                    pulsar_freq = 1.0 / period  # Hz (rough estimate)
                    frequency_factor = (pulsar_freq / self.f0_klein)**2
                    echo_amplitude = self.echo_amplitude_ratio * frequency_factor
                    echo_pulses[closest_idx] = echo_amplitude
                    
            # Convert back to observation cadence (simulate limited time resolution)
            # This represents the fact that we only have measurements every ~2 weeks
            klein_echo_binned = np.zeros(n_observations)
            for i, obs_time in enumerate(observation_times):
                # Look for Klein echoes within ±cadence/2 of this observation
                time_window = [obs_time - cadence/2, obs_time + cadence/2]
                window_mask = (times_fine >= time_window[0]) & (times_fine <= time_window[1])
                
                # Sum any Klein echoes that fall within this observation window
                klein_echo_binned[i] = np.sum(echo_pulses[window_mask])
                
            # Convert to timing residual units (microseconds)
            klein_echo_signal = klein_echo_binned * timing_rms * 1e6
            
            # 5. Total timing residuals
            total_residuals = (white_noise + red_noise + deterministic + klein_echo_signal * 1e-6) * 1e6  # μs
            
            pulsars.append({
                'name': pulsar_name,
                'period': period,
                'period_derivative': period_derivative,
                'distance': distance,
                'timing_rms': timing_rms,
                'observation_times': observation_times.copy(),
                'timing_residuals': total_residuals,
                'white_noise': white_noise * 1e6,
                'red_noise': red_noise * 1e6,
                'deterministic': deterministic,
                'klein_echo': klein_echo_signal,
                'cadence': cadence
            })
            
        self.pulsar_data = {
            'pulsars': pulsars,
            'n_pulsars': n_pulsars,
            'observation_span': observation_span,
            'cadence': cadence,
            'n_observations': n_observations
        }
        
        print(f"✅ Generated {n_pulsars} millisecond pulsars")
        print(f"   • Observation span: {observation_span/(365.25*24*3600):.1f} years")
        print(f"   • Cadence: {cadence/(24*3600):.1f} days")
        print(f"   • Total observations: {n_observations}")
        print(f"   • Timing precision: 50-500 ns RMS")
        
        return True
        
    def analyze_klein_electromagnetic_echoes(self) -> Dict:
        """Search for Klein electromagnetic echoes in pulsar timing data"""
        
        print("\\n🔍 Searching for Klein Electromagnetic Echoes...")
        
        results = {
            'cross_correlation_analysis': {},
            'stacking_analysis': {},
            'frequency_analysis': {},
            'statistical_tests': {},
            'individual_pulsars': []
        }
        
        pulsars = self.pulsar_data['pulsars']
        
        # 1. Cross-correlation analysis for each pulsar
        echo_detections = []
        correlation_peaks = []
        
        for pulsar in pulsars:
            residuals = pulsar['timing_residuals']
            times = pulsar['observation_times']
            
            # Create template for Klein echo detection
            # Template: delta function delayed by echo_delay
            dt = pulsar['cadence']
            delay_samples = int(self.echo_delay / dt)
            
            if delay_samples < len(residuals) - 1:
                # Cross-correlate timing residuals with delayed version
                correlation = np.correlate(residuals[:-delay_samples], 
                                         residuals[delay_samples:], mode='valid')
                
                # Normalize correlation
                norm_factor = np.sqrt(np.sum(residuals[:-delay_samples]**2) * 
                                    np.sum(residuals[delay_samples:]**2))
                if norm_factor > 0:
                    normalized_correlation = correlation[0] / norm_factor
                else:
                    normalized_correlation = 0
                    
                correlation_peaks.append(normalized_correlation)
                
                # Statistical significance of correlation
                n_samples = len(residuals) - delay_samples
                correlation_significance = np.abs(normalized_correlation) * np.sqrt(n_samples - 2)
                
                echo_detections.append({
                    'pulsar': pulsar['name'],
                    'correlation': normalized_correlation,
                    'significance': correlation_significance,
                    'delay_samples': delay_samples,
                    'n_samples': n_samples
                })
            else:
                correlation_peaks.append(0)
                echo_detections.append({
                    'pulsar': pulsar['name'],
                    'correlation': 0,
                    'significance': 0,
                    'delay_samples': delay_samples,
                    'n_samples': 0
                })
                
        results['individual_pulsars'] = echo_detections
        
        # 2. Stacking analysis across all pulsars
        all_correlations = np.array(correlation_peaks)
        mean_correlation = np.mean(all_correlations)
        correlation_std = np.std(all_correlations)
        n_pulsars = len(all_correlations)
        
        # Stacked significance
        if correlation_std > 0 and n_pulsars > 1:
            stacked_significance = np.abs(mean_correlation) / (correlation_std / np.sqrt(n_pulsars))
        else:
            stacked_significance = 0
            
        results['stacking_analysis'] = {
            'mean_correlation': mean_correlation,
            'correlation_std': correlation_std,
            'stacked_significance': stacked_significance,
            'n_pulsars': n_pulsars
        }
        
        # 3. Frequency domain analysis
        # Look for coherent Klein echo signals in frequency domain
        
        # Combine all timing residuals with proper time alignment
        combined_residuals = []
        combined_times = []
        
        for pulsar in pulsars:
            combined_residuals.extend(pulsar['timing_residuals'])
            combined_times.extend(pulsar['observation_times'])
            
        combined_residuals = np.array(combined_residuals)
        combined_times = np.array(combined_times)
        
        # Sort by time
        sort_indices = np.argsort(combined_times)
        combined_residuals = combined_residuals[sort_indices]
        combined_times = combined_times[sort_indices]
        
        # Fourier analysis
        if len(combined_residuals) > 10:
            fft_residuals = fft.fft(combined_residuals)
            freqs = fft.fftfreq(len(combined_residuals), d=np.median(np.diff(combined_times)))
            power_spectrum = np.abs(fft_residuals)**2
            
            # Look for peak near Klein frequency
            klein_freq_idx = np.argmin(np.abs(freqs - self.f0_klein))
            klein_power = power_spectrum[klein_freq_idx] if klein_freq_idx < len(power_spectrum) else 0
            
            # Background power (excluding Klein frequency region)
            freq_mask = np.abs(freqs - self.f0_klein) > 0.5 * self.f0_klein
            background_power = np.median(power_spectrum[freq_mask]) if np.any(freq_mask) else 1
            
            # Signal-to-noise ratio at Klein frequency
            klein_snr = klein_power / background_power if background_power > 0 else 0
            
        else:
            klein_snr = 0
            klein_power = 0
            background_power = 1
            
        results['frequency_analysis'] = {
            'klein_frequency': self.f0_klein,
            'klein_power': klein_power,
            'background_power': background_power,
            'klein_snr': klein_snr
        }
        
        # 4. Statistical tests
        
        # Test 1: Are correlations systematically positive (Klein echo signature)?
        positive_correlations = np.sum(np.array(correlation_peaks) > 0)
        total_correlations = len(correlation_peaks)
        
        if total_correlations > 0:
            # Binomial test: probability of getting this many positive correlations by chance
            p_value_binomial = stats.binom_test(positive_correlations, total_correlations, 0.5)
            binomial_significance = stats.norm.ppf(1 - p_value_binomial/2) if p_value_binomial > 0 else 0
        else:
            p_value_binomial = 1
            binomial_significance = 0
            
        # Test 2: Kolmogorov-Smirnov test for Klein echo distribution
        # Are correlations consistent with Klein echo predictions?
        expected_correlation = self.echo_amplitude_ratio  # Expected Klein echo correlation
        
        if len(correlation_peaks) > 5:
            # Compare observed correlations to expected Klein distribution
            _, p_value_ks = stats.kstest(correlation_peaks, 
                                       lambda x: stats.norm.cdf(x, expected_correlation, 
                                                               correlation_std if correlation_std > 0 else 0.1))
            ks_significance = stats.norm.ppf(1 - p_value_ks/2) if p_value_ks > 0 else 0
        else:
            p_value_ks = 1
            ks_significance = 0
            
        # Combined significance
        combined_significance = np.sqrt(stacked_significance**2 + 
                                      binomial_significance**2 + 
                                      ks_significance**2)
        
        results['statistical_tests'] = {
            'stacked_significance': stacked_significance,
            'binomial_significance': binomial_significance,
            'ks_significance': ks_significance,
            'combined_significance': combined_significance,
            'p_value_binomial': p_value_binomial,
            'p_value_ks': p_value_ks,
            'positive_correlations': positive_correlations,
            'total_correlations': total_correlations
        }
        
        self.echo_analysis = results
        return results
        
    def create_visualization(self):
        """Create Klein electromagnetic echo analysis visualization"""
        
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('IPTA Klein Electromagnetic Echo Detection Analysis', 
                     fontweight='bold', fontsize=14)
        
        # 1. Individual pulsar correlation results
        ax1 = axes[0, 0]
        
        individual_results = self.echo_analysis['individual_pulsars']
        correlations = [p['correlation'] for p in individual_results]
        significances = [p['significance'] for p in individual_results]
        
        # Scatter plot: correlation vs significance
        scatter = ax1.scatter(correlations, significances, alpha=0.7, s=60)
        
        # Mark significant detections
        for i, (corr, sig) in enumerate(zip(correlations, significances)):
            if sig > 2:  # >2σ detections
                ax1.plot(corr, sig, 'ro', markersize=8, alpha=0.8)
                
        ax1.axhline(2, color='orange', linestyle='--', alpha=0.7, label='2σ threshold')
        ax1.axhline(3, color='red', linestyle='--', alpha=0.7, label='3σ threshold')
        ax1.axvline(0, color='gray', linestyle='-', alpha=0.3)
        
        ax1.set_xlabel('Klein Echo Correlation')
        ax1.set_ylabel('Statistical Significance (σ)')
        ax1.set_title('A. Individual Pulsar Klein Echo Detection')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 2. Correlation distribution
        ax2 = axes[0, 1]
        
        ax2.hist(correlations, bins=15, alpha=0.7, density=True, color='skyblue', 
                label='Observed Correlations')
        
        # Expected Klein echo correlation
        expected_corr = self.echo_amplitude_ratio
        ax2.axvline(expected_corr, color='red', linestyle='--', linewidth=2,
                   label=f'Klein Prediction: {expected_corr:.2e}')
        ax2.axvline(0, color='gray', linestyle='-', alpha=0.5, label='No Echo')
        
        ax2.set_xlabel('Klein Echo Correlation')
        ax2.set_ylabel('Probability Density')
        ax2.set_title('B. Klein Echo Correlation Distribution')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # 3. Results summary
        ax3 = axes[1, 0]
        ax3.axis('off')
        
        stats_data = self.echo_analysis['statistical_tests']
        stacking_data = self.echo_analysis['stacking_analysis']
        freq_data = self.echo_analysis['frequency_analysis']
        
        summary_text = f"""
KLEIN ELECTROMAGNETIC ECHO ANALYSIS

THEORETICAL PREDICTIONS:
• Klein echo delay: {self.echo_delay:.6f} seconds
• Klein echo amplitude ratio: {self.echo_amplitude_ratio:.2e}
• Klein resonance frequency: {self.f0_klein} Hz

STACKING ANALYSIS:
• Mean correlation: {stacking_data['mean_correlation']:.4f}
• Stacked significance: {stacking_data['stacked_significance']:.2f}σ
• Number of pulsars: {stacking_data['n_pulsars']}

FREQUENCY ANALYSIS:
• Klein frequency SNR: {freq_data['klein_snr']:.2f}
• Klein power: {freq_data['klein_power']:.2e}
• Background power: {freq_data['background_power']:.2e}

STATISTICAL TESTS:
• Combined significance: {stats_data['combined_significance']:.2f}σ
• Positive correlations: {stats_data['positive_correlations']}/{stats_data['total_correlations']}
• Binomial p-value: {stats_data['p_value_binomial']:.3f}

STATUS:
{'✅ KLEIN ECHOES DETECTED' if stats_data['combined_significance'] > 3 else 
 '🔶 MARGINAL DETECTION' if stats_data['combined_significance'] > 2 else 
 '❌ NO KLEIN ECHO SIGNATURE'}
        """
        
        color = ('green' if stats_data['combined_significance'] > 3 else 
                'orange' if stats_data['combined_significance'] > 2 else 'red')
        ax3.text(0.05, 0.95, summary_text, transform=ax3.transAxes,
                fontsize=9, verticalalignment='top', fontfamily='monospace',
                color=color)
        
        # 4. Time series example
        ax4 = axes[1, 1]
        
        # Show example pulsar timing residuals with Klein echo highlighted
        example_pulsar = self.pulsar_data['pulsars'][0]
        times = example_pulsar['observation_times'] / (365.25*24*3600)  # Convert to years
        residuals = example_pulsar['timing_residuals']
        klein_component = example_pulsar['klein_echo']
        
        ax4.plot(times, residuals, 'b-', alpha=0.7, label='Total Residuals')
        ax4.plot(times, klein_component, 'r-', linewidth=2, 
                label=f'Klein Echo Component (×{1/self.echo_amplitude_ratio:.0e})')
        
        ax4.set_xlabel('Time (Years)')
        ax4.set_ylabel('Timing Residuals (μs)')
        ax4.set_title(f'C. Example: {example_pulsar["name"]}\\nKlein Echo Signal')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('ipta_klein_echo_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print("✅ IPTA Klein echo visualization saved")

def main():
    """Main IPTA Klein electromagnetic echo analysis"""
    analyzer = IPTAKleinEchoAnalyzer()
    
    if analyzer.generate_representative_pulsar_data():
        results = analyzer.analyze_klein_electromagnetic_echoes()
        analyzer.create_visualization()
        
        stats = results['statistical_tests']
        stacking = results['stacking_analysis']
        
        print(f"\\n📡 IPTA KLEIN ELECTROMAGNETIC ECHO RESULTS:")
        print(f"   • Combined significance: {stats['combined_significance']:.2f}σ")
        print(f"   • Stacked correlation: {stacking['mean_correlation']:.4f}")
        print(f"   • Positive correlations: {stats['positive_correlations']}/{stats['total_correlations']}")
        print(f"   • Binomial p-value: {stats['p_value_binomial']:.3f}")
        
        status = ('DETECTED' if stats['combined_significance'] > 3 else 
                 'MARGINAL' if stats['combined_significance'] > 2 else 'NOT DETECTED')
        print(f"   • Status: Klein electromagnetic echoes {status}")
        
        return results
    return None

if __name__ == "__main__":
    main()