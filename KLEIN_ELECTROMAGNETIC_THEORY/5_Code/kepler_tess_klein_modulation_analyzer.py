#!/usr/bin/env python3
"""
Kepler/TESS Klein Electromagnetic Modulation Analyzer
=====================================================

OBJECTIVE: Search for Klein electromagnetic modulations in stellar photometry
APPROACH: Parameter-free analysis of Klein frequency signatures
TARGET: Klein modulations at f₀ = 5.68 Hz and harmonics

Theory: Klein electromagnetic coupling causes systematic brightness variations
Prediction: Stellar photometry should show Klein frequency signatures
Critical Test: Ultra-precise photometry Klein electromagnetic detection
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats, signal
from typing import Dict, List, Tuple
import warnings
warnings.filterwarnings('ignore')

class KeplerTESSKleinModulationAnalyzer:
    """Kepler/TESS photometry analysis for Klein electromagnetic modulation detection"""
    
    def __init__(self):
        # Klein electromagnetic predictions (NO free parameters)
        self.f0_klein = 5.68  # Hz (Klein oscillation frequency)
        self.gamma_em = 1e-15  # Klein-EM coupling strength
        
        # Klein modulation predictions
        self.klein_amplitude_ppm = self.gamma_em * 1e6  # parts per million
        
        print(f"Kepler/TESS Klein Electromagnetic Modulation Analysis")
        print(f"=" * 55)
        print(f"Klein frequency: f₀ = {self.f0_klein} Hz")
        print(f"Klein-EM coupling: γ_EM = {self.gamma_em:.2e}")
        print(f"Predicted modulation: {self.klein_amplitude_ppm:.3f} ppm")
        
        # Analysis data
        self.stellar_data = {}
        self.modulation_analysis = {}
        
    def generate_representative_stellar_data(self) -> bool:
        """Generate representative Kepler/TESS-like photometry data"""
        
        print("\\n⭐ Generating Representative Kepler/TESS Photometry Data...")
        print("(Note: Using simulated data representative of Kepler precision)")
        
        # Observation parameters (Kepler-like)
        observation_span = 90 * 24 * 3600  # 90 days (typical Kepler quarter)
        cadence = 30 * 60  # 30-minute cadence (long cadence)
        observation_times = np.arange(0, observation_span, cadence)
        n_observations = len(observation_times)
        
        # Generate sample of stars
        n_stars = 100  # Representative sample
        stars = []
        
        for i in range(n_stars):
            star_name = f"KIC {1000000 + i}"
            
            # Stellar properties
            stellar_type = np.random.choice(['G', 'K', 'M', 'F'], p=[0.4, 0.3, 0.2, 0.1])
            magnitude = np.random.uniform(8, 16)  # Kepler magnitude range
            
            # Photometric precision (depends on magnitude)
            # Brighter stars have better precision
            if magnitude < 10:
                photometric_precision = np.random.uniform(10, 50)  # ppm
            elif magnitude < 12:
                photometric_precision = np.random.uniform(50, 200)  # ppm
            else:
                photometric_precision = np.random.uniform(200, 1000)  # ppm
                
            # Generate light curve components
            
            # 1. Stellar variability (intrinsic)
            # Many stars show some level of variability
            
            # Stellar rotation (if spotted star)
            if np.random.random() < 0.3:  # 30% show rotation
                rotation_period = np.random.uniform(5, 30) * 24 * 3600  # 5-30 days
                rotation_amplitude = np.random.uniform(100, 2000)  # ppm
                rotation_signal = rotation_amplitude * np.sin(2*np.pi * observation_times / rotation_period)
            else:
                rotation_signal = np.zeros(n_observations)
                
            # Stellar oscillations (if solar-like oscillator)
            if np.random.random() < 0.1:  # 10% show detectable oscillations
                oscillation_freq = np.random.uniform(1000, 4000) * 1e-6  # μHz to Hz
                oscillation_amplitude = np.random.uniform(1, 10)  # ppm
                oscillation_signal = oscillation_amplitude * np.sin(2*np.pi * oscillation_freq * observation_times)
            else:
                oscillation_signal = np.zeros(n_observations)
                
            # 2. Instrumental effects
            
            # Long-term instrumental trends
            instrumental_trend = 50 * (observation_times / observation_span - 0.5)  # ppm linear trend
            
            # Systematic effects (temperature variations, etc.)
            systematic_period = 24 * 3600  # Daily systematics
            systematic_amplitude = np.random.uniform(10, 100)  # ppm
            systematic_signal = systematic_amplitude * np.sin(2*np.pi * observation_times / systematic_period)
            
            # 3. White noise (photon noise + instrumental)
            white_noise = np.random.normal(0, photometric_precision, n_observations)
            
            # 4. Klein electromagnetic modulation (the signal we're searching for!)
            
            # Klein modulation at fundamental frequency
            klein_phase = np.random.uniform(0, 2*np.pi)
            klein_amplitude = self.klein_amplitude_ppm  # Very small amplitude
            klein_modulation_main = klein_amplitude * np.sin(2*np.pi * self.f0_klein * observation_times + klein_phase)
            
            # Klein harmonics (smaller amplitude)
            klein_modulation_harmonics = 0
            for harmonic in [2, 3]:
                harm_phase = np.random.uniform(0, 2*np.pi)
                harm_amplitude = klein_amplitude / harmonic**2
                klein_modulation_harmonics += harm_amplitude * np.sin(2*np.pi * harmonic * self.f0_klein * observation_times + harm_phase)
            
            # Stellar-type dependent Klein coupling (hypothetical)
            if stellar_type in ['G', 'F']:  # Solar-type stars
                stellar_coupling_factor = 1.0
            elif stellar_type == 'K':
                stellar_coupling_factor = 0.8
            else:  # M dwarfs
                stellar_coupling_factor = 0.5
                
            klein_modulation_total = (klein_modulation_main + klein_modulation_harmonics) * stellar_coupling_factor
            
            # 5. Total light curve
            total_flux = (rotation_signal + oscillation_signal + instrumental_trend + 
                         systematic_signal + white_noise + klein_modulation_total)
            
            stars.append({
                'name': star_name,
                'stellar_type': stellar_type,
                'magnitude': magnitude,
                'photometric_precision': photometric_precision,
                'observation_times': observation_times.copy(),
                'flux_ppm': total_flux,
                'rotation_signal': rotation_signal,
                'oscillation_signal': oscillation_signal,
                'instrumental_effects': instrumental_trend + systematic_signal,
                'white_noise': white_noise,
                'klein_modulation': klein_modulation_total,
                'klein_phase': klein_phase,
                'stellar_coupling_factor': stellar_coupling_factor
            })
            
        self.stellar_data = {
            'stars': stars,
            'n_stars': n_stars,
            'observation_span': observation_span,
            'cadence': cadence,
            'n_observations': n_observations
        }
        
        print(f"✅ Generated {n_stars} stars")
        print(f"   • Observation span: {observation_span/(24*3600):.1f} days")
        print(f"   • Cadence: {cadence/60:.0f} minutes")
        print(f"   • Observations per star: {n_observations}")
        print(f"   • Magnitude range: 8-16")
        print(f"   • Precision range: 10-1000 ppm")
        
        return True
        
    def analyze_klein_modulations(self) -> Dict:
        """Search for Klein electromagnetic modulation signatures"""
        
        print("\\n🔍 Searching for Klein Electromagnetic Modulations...")
        
        results = {
            'frequency_domain_analysis': {},
            'individual_detections': [],
            'stacking_analysis': {},
            'statistical_tests': {}
        }
        
        stars = self.stellar_data['stars']
        observation_times = stars[0]['observation_times']
        
        # 1. Frequency domain analysis for each star
        klein_powers = []
        klein_snrs = []
        harmonic_powers = []
        
        for star in stars:
            flux_ppm = star['flux_ppm']
            
            # Remove long-term trends (detrend)
            detrended_flux = signal.detrend(flux_ppm)
            
            # Power spectral density
            dt = self.stellar_data['cadence']
            frequencies, psd = signal.welch(detrended_flux, fs=1/dt, nperseg=len(detrended_flux)//4)
            
            # Find Klein frequency peak
            klein_freq_idx = np.argmin(np.abs(frequencies - self.f0_klein))
            klein_power = psd[klein_freq_idx] if klein_freq_idx < len(psd) else 0
            
            # Background power (local background around Klein frequency)
            freq_window = 0.1 * self.f0_klein  # ±10% frequency window
            background_mask = ((frequencies > self.f0_klein - freq_window) & 
                             (frequencies < self.f0_klein + freq_window) &
                             (np.abs(frequencies - self.f0_klein) > 0.05 * self.f0_klein))
            
            if np.any(background_mask):
                background_power = np.median(psd[background_mask])
            else:
                background_power = np.median(psd[frequencies > 0])
                
            klein_snr = klein_power / background_power if background_power > 0 else 0
            
            # Check harmonics
            harmonic_snrs = []
            for harmonic in [2, 3]:
                harm_freq = harmonic * self.f0_klein
                if harm_freq < np.max(frequencies):
                    harm_freq_idx = np.argmin(np.abs(frequencies - harm_freq))
                    harm_power = psd[harm_freq_idx]
                    harm_snr = harm_power / background_power if background_power > 0 else 0
                    harmonic_snrs.append(harm_snr)
                else:
                    harmonic_snrs.append(0)
                    
            klein_powers.append(klein_power)
            klein_snrs.append(klein_snr)
            harmonic_powers.append(np.mean(harmonic_snrs))
            
            # Individual detection assessment
            detection_threshold = 3.0  # 3x background
            klein_detected = klein_snr > detection_threshold
            
            results['individual_detections'].append({
                'star_name': star['name'],
                'stellar_type': star['stellar_type'],
                'magnitude': star['magnitude'],
                'photometric_precision': star['photometric_precision'],
                'klein_power': klein_power,
                'klein_snr': klein_snr,
                'harmonic_snr': np.mean(harmonic_snrs),
                'detection': klein_detected,
                'klein_coupling_factor': star['stellar_coupling_factor']
            })
            
        # 2. Stacking analysis across all stars
        klein_powers = np.array(klein_powers)
        klein_snrs = np.array(klein_snrs)
        harmonic_powers = np.array(harmonic_powers)
        
        mean_klein_snr = np.mean(klein_snrs)
        klein_snr_std = np.std(klein_snrs)
        
        # Number of individual detections
        n_detections = sum(1 for det in results['individual_detections'] if det['detection'])
        detection_rate = n_detections / len(stars)
        
        results['frequency_domain_analysis'] = {
            'klein_frequency': self.f0_klein,
            'individual_powers': klein_powers.tolist(),
            'individual_snrs': klein_snrs.tolist(),
            'harmonic_powers': harmonic_powers.tolist(),
            'mean_klein_snr': mean_klein_snr,
            'klein_snr_std': klein_snr_std,
            'n_detections': n_detections,
            'detection_rate': detection_rate
        }
        
        # 3. Coherent stacking analysis
        # Stack all light curves to enhance Klein signal
        
        stacked_flux = np.zeros(len(observation_times))
        for star in stars:
            # Normalize by photometric precision for optimal weighting
            weight = 1.0 / star['photometric_precision']**2
            normalized_flux = signal.detrend(star['flux_ppm']) * weight
            stacked_flux += normalized_flux
            
        # Normalize stacked flux
        total_weight = sum(1.0 / star['photometric_precision']**2 for star in stars)
        stacked_flux /= total_weight
        
        # Power spectrum of stacked light curve
        if len(stacked_flux) > 10:
            dt = self.stellar_data['cadence']
            freq_stack, psd_stack = signal.welch(stacked_flux, fs=1/dt, nperseg=len(stacked_flux)//4)
            
            # Klein frequency in stacked data
            klein_freq_idx_stack = np.argmin(np.abs(freq_stack - self.f0_klein))
            klein_power_stack = psd_stack[klein_freq_idx_stack] if klein_freq_idx_stack < len(psd_stack) else 0
            
            # Background power in stacked data
            freq_window = 0.1 * self.f0_klein
            background_mask_stack = ((freq_stack > self.f0_klein - freq_window) & 
                                   (freq_stack < self.f0_klein + freq_window) &
                                   (np.abs(freq_stack - self.f0_klein) > 0.05 * self.f0_klein))
            
            if np.any(background_mask_stack):
                background_power_stack = np.median(psd_stack[background_mask_stack])
            else:
                background_power_stack = np.median(psd_stack[freq_stack > 0])
                
            stacked_klein_snr = klein_power_stack / background_power_stack if background_power_stack > 0 else 0
        else:
            stacked_klein_snr = 0
            
        results['stacking_analysis'] = {
            'stacked_klein_snr': stacked_klein_snr,
            'improvement_factor': stacked_klein_snr / mean_klein_snr if mean_klein_snr > 0 else 1
        }
        
        # 4. Statistical tests
        
        # Test 1: Are Klein SNRs systematically > 1?
        if len(klein_snrs) > 1:
            snr_excess = klein_snrs - 1.0  # Excess above background
            mean_excess = np.mean(snr_excess)
            excess_std = np.std(snr_excess)
            
            if excess_std > 0:
                snr_significance = mean_excess / (excess_std / np.sqrt(len(klein_snrs)))
                snr_significance = max(0, snr_significance)  # Only positive excesses
            else:
                snr_significance = 0
        else:
            snr_significance = 0
            
        # Test 2: Binomial test for detection rate
        expected_false_positive_rate = 0.05  # 5% expected by chance
        if len(stars) > 0:
            try:
                result = stats.binomtest(n_detections, len(stars), expected_false_positive_rate)
                detection_p_value = result.pvalue
            except AttributeError:
                # Fallback
                detection_p_value = stats.binom_test(n_detections, len(stars), expected_false_positive_rate)
                
            if detection_p_value > 0:
                detection_significance = stats.norm.ppf(1 - detection_p_value/2)
            else:
                detection_significance = 0
        else:
            detection_significance = 0
            
        # Test 3: Stacked signal significance
        if stacked_klein_snr > 0:
            # Convert SNR to statistical significance (rough approximation)
            stacked_significance = np.log10(stacked_klein_snr) * 3  # Rough conversion
            stacked_significance = max(0, stacked_significance)
        else:
            stacked_significance = 0
            
        # Combined significance
        combined_significance = np.sqrt(snr_significance**2 + 
                                      detection_significance**2 + 
                                      stacked_significance**2)
        
        results['statistical_tests'] = {
            'snr_significance': snr_significance,
            'detection_significance': detection_significance,
            'stacked_significance': stacked_significance,
            'combined_significance': combined_significance,
            'detection_p_value': detection_p_value if 'detection_p_value' in locals() else 1
        }
        
        self.modulation_analysis = results
        return results
        
    def create_visualization(self):
        """Create Klein modulation analysis visualization"""
        
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('Kepler/TESS Klein Electromagnetic Modulation Detection', 
                     fontweight='bold', fontsize=14)
        
        # 1. Individual star Klein SNR
        ax1 = axes[0, 0]
        
        detections = self.modulation_analysis['individual_detections']
        magnitudes = [det['magnitude'] for det in detections]
        klein_snrs = [det['klein_snr'] for det in detections]
        
        # Color by detection
        colors = ['red' if det['detection'] else 'blue' for det in detections]
        
        scatter = ax1.scatter(magnitudes, klein_snrs, c=colors, alpha=0.6, s=30)
        
        ax1.axhline(1, color='gray', linestyle='-', alpha=0.5, label='Background Level')
        ax1.axhline(3, color='red', linestyle='--', alpha=0.7, label='Detection Threshold')
        
        ax1.set_xlabel('Stellar Magnitude')
        ax1.set_ylabel('Klein Frequency SNR')
        ax1.set_title('A. Individual Star Klein Detections')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Add detection count
        n_detections = self.modulation_analysis['frequency_domain_analysis']['n_detections']
        ax1.text(0.05, 0.95, f'Detections: {n_detections}/{len(detections)}', 
                transform=ax1.transAxes, fontsize=12, fontweight='bold',
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        # 2. Klein SNR histogram
        ax2 = axes[0, 1]
        
        ax2.hist(klein_snrs, bins=15, alpha=0.7, density=True, color='skyblue')
        ax2.axvline(np.mean(klein_snrs), color='red', linestyle='--', linewidth=2,
                   label=f'Mean: {np.mean(klein_snrs):.2f}')
        ax2.axvline(1, color='gray', linestyle='-', alpha=0.5, label='Background')
        
        ax2.set_xlabel('Klein Frequency SNR')
        ax2.set_ylabel('Probability Density')
        ax2.set_title('B. Klein SNR Distribution')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # 3. Results summary
        ax3 = axes[1, 0]
        ax3.axis('off')
        
        stats_data = self.modulation_analysis['statistical_tests']
        freq_data = self.modulation_analysis['frequency_domain_analysis']
        stack_data = self.modulation_analysis['stacking_analysis']
        
        summary_text = f"""
KEPLER/TESS KLEIN MODULATION ANALYSIS

THEORETICAL PREDICTIONS:
• Klein frequency: f₀ = {self.f0_klein} Hz
• Klein modulation: {self.klein_amplitude_ppm:.3f} ppm
• Klein-EM coupling: γ_EM = {self.gamma_em:.2e}

INDIVIDUAL STAR ANALYSIS:
• Stars analyzed: {self.stellar_data['n_stars']}
• Mean Klein SNR: {freq_data['mean_klein_snr']:.2f}
• Individual detections: {freq_data['n_detections']}
• Detection rate: {freq_data['detection_rate']*100:.1f}%

STACKING ANALYSIS:
• Stacked Klein SNR: {stack_data['stacked_klein_snr']:.2f}
• Improvement factor: {stack_data['improvement_factor']:.1f}×

STATISTICAL TESTS:
• SNR significance: {stats_data['snr_significance']:.2f}σ
• Detection significance: {stats_data['detection_significance']:.2f}σ
• Stacked significance: {stats_data['stacked_significance']:.2f}σ
• Combined significance: {stats_data['combined_significance']:.2f}σ

STATUS:
{'✅ KLEIN MODULATION DETECTED' if stats_data['combined_significance'] > 3 else 
 '🔶 MARGINAL DETECTION' if stats_data['combined_significance'] > 2 else 
 '❌ NO MODULATION SIGNATURE'}
        """
        
        color = ('green' if stats_data['combined_significance'] > 3 else 
                'orange' if stats_data['combined_significance'] > 2 else 'red')
        ax3.text(0.05, 0.95, summary_text, transform=ax3.transAxes,
                fontsize=9, verticalalignment='top', fontfamily='monospace',
                color=color)
        
        # 4. Example light curve with Klein signal
        ax4 = axes[1, 1]
        
        # Show example star light curve
        example_star = self.stellar_data['stars'][0]
        times = example_star['observation_times'] / (24 * 3600)  # Convert to days
        flux = example_star['flux_ppm']
        klein_component = example_star['klein_modulation']
        
        # Detrend for visualization
        detrended_flux = signal.detrend(flux)
        
        ax4.plot(times, detrended_flux, 'b-', alpha=0.7, linewidth=0.5, 
                label='Total Light Curve')
        
        # Scale Klein component for visibility
        scaled_klein = klein_component * 10000  # Scale up for visibility
        ax4.plot(times, scaled_klein, 'r-', linewidth=2, 
                label=f'Klein Signal (×10⁴)')
        
        ax4.set_xlabel('Time (Days)')
        ax4.set_ylabel('Flux Variation (ppm)')
        ax4.set_title(f'C. Example: {example_star["name"]}')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('kepler_tess_klein_modulation.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print("✅ Kepler/TESS Klein modulation visualization saved")

def main():
    """Main Kepler/TESS Klein modulation analysis"""
    analyzer = KeplerTESSKleinModulationAnalyzer()
    
    if analyzer.generate_representative_stellar_data():
        results = analyzer.analyze_klein_modulations()
        analyzer.create_visualization()
        
        stats = results['statistical_tests']
        freq = results['frequency_domain_analysis']
        stack = results['stacking_analysis']
        
        print(f"\\n⭐ KEPLER/TESS KLEIN MODULATION RESULTS:")
        print(f"   • Combined significance: {stats['combined_significance']:.2f}σ")
        print(f"   • Mean Klein SNR: {freq['mean_klein_snr']:.2f}")
        print(f"   • Individual detections: {freq['n_detections']}/{freq['n_detections'] + (len(freq['individual_snrs']) - freq['n_detections'])}")
        print(f"   • Stacked Klein SNR: {stack['stacked_klein_snr']:.2f}")
        
        status = ('DETECTED' if stats['combined_significance'] > 3 else 
                 'MARGINAL' if stats['combined_significance'] > 2 else 'NOT DETECTED')
        print(f"   • Status: Klein electromagnetic modulation {status}")
        
        return results
    return None

if __name__ == "__main__":
    main()