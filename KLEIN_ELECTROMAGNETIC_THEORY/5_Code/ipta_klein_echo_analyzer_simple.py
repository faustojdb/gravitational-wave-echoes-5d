#!/usr/bin/env python3
"""
IPTA Klein Electromagnetic Echo Analyzer - SIMPLIFIED VERSION
============================================================

OBJECTIVE: Search for Klein electromagnetic echoes in pulsar timing data
APPROACH: Simplified analysis focusing on Klein echo signature detection
TARGET: Klein echo delay Δt = 2R_K/c = 0.056 seconds exactly

Simplified approach to avoid computational bottlenecks
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats
from typing import Dict, List, Tuple
import warnings
warnings.filterwarnings('ignore')

class IPTAKleinEchoAnalyzer:
    """Simplified IPTA pulsar timing analysis for Klein electromagnetic echo detection"""
    
    def __init__(self):
        # Klein electromagnetic predictions (NO free parameters)
        self.R_klein = 8.4e6  # m (Klein atom radius)
        self.c = 2.998e8      # m/s (speed of light)
        self.f0_klein = 5.68  # Hz (Klein oscillation frequency)
        self.gamma_em = 1e-15 # Klein-EM coupling strength
        
        # Klein echo parameters
        self.echo_delay = 2 * self.R_klein / self.c  # seconds
        self.echo_amplitude_ratio = self.gamma_em
        
        print(f"Klein Electromagnetic Echo Analysis (Simplified)")
        print(f"=" * 55)
        print(f"Klein echo delay prediction: {self.echo_delay:.6f} seconds")
        print(f"Klein echo amplitude ratio: {self.echo_amplitude_ratio:.2e}")
        
        # Analysis data
        self.pulsar_data = {}
        self.echo_analysis = {}
        
    def generate_simple_pulsar_data(self) -> bool:
        """Generate simplified pulsar timing data for Klein echo analysis"""
        
        print("\\n📡 Generating Simplified IPTA-like Pulsar Data...")
        
        # Simple time series: 20 years, weekly observations
        observation_span = 20 * 365.25 * 24 * 3600  # seconds
        cadence = 7 * 24 * 3600  # 1 week cadence
        observation_times = np.arange(0, observation_span, cadence)
        n_observations = len(observation_times)
        
        # Generate 20 simple pulsars
        n_pulsars = 20
        pulsars = []
        
        for i in range(n_pulsars):
            pulsar_name = f"PSR J{1800+i:02d}00+0000"
            
            # Simple pulsar properties
            timing_rms = np.random.uniform(100e-9, 1000e-9)  # 100-1000 ns
            
            # Simple timing residuals = white noise + Klein echo
            white_noise = np.random.normal(0, timing_rms * 1e6, n_observations)  # μs
            
            # Klein echo signal (simplified)
            klein_echo = np.zeros(n_observations)
            
            # Add Klein echoes at specific intervals
            echo_interval_samples = max(1, int(self.echo_delay / cadence))
            
            for j in range(echo_interval_samples, n_observations, echo_interval_samples):
                if j < n_observations:
                    # Klein echo amplitude (very small)
                    echo_amplitude = self.echo_amplitude_ratio * timing_rms * 1e6
                    # Add some random variation
                    echo_amplitude *= (1 + 0.1 * np.random.normal())
                    klein_echo[j] = echo_amplitude
                    
            # Total residuals
            total_residuals = white_noise + klein_echo
            
            pulsars.append({
                'name': pulsar_name,
                'timing_rms': timing_rms,
                'observation_times': observation_times.copy(),
                'timing_residuals': total_residuals,
                'white_noise': white_noise,
                'klein_echo': klein_echo,
                'cadence': cadence
            })
            
        self.pulsar_data = {
            'pulsars': pulsars,
            'n_pulsars': n_pulsars,
            'observation_span': observation_span,
            'cadence': cadence,
            'n_observations': n_observations
        }
        
        print(f"✅ Generated {n_pulsars} simplified pulsars")
        print(f"   • Observation span: {observation_span/(365.25*24*3600):.1f} years")
        print(f"   • Cadence: {cadence/(24*3600):.1f} days")
        print(f"   • Total observations per pulsar: {n_observations}")
        
        return True
        
    def analyze_klein_echoes(self) -> Dict:
        """Simplified Klein echo analysis"""
        
        print("\\n🔍 Searching for Klein Electromagnetic Echoes...")
        
        results = {
            'individual_detections': [],
            'stacking_analysis': {},
            'statistical_tests': {}
        }
        
        pulsars = self.pulsar_data['pulsars']
        
        # 1. Simple correlation analysis for each pulsar
        correlations = []
        echo_detections = []
        
        for pulsar in pulsars:
            residuals = pulsar['timing_residuals']
            echo_component = pulsar['klein_echo']
            
            # Cross-correlation between residuals and expected Klein echo
            if len(residuals) > 10 and np.std(residuals) > 0:
                correlation = np.corrcoef(residuals, echo_component)[0, 1]
                if np.isnan(correlation):
                    correlation = 0
            else:
                correlation = 0
                
            correlations.append(correlation)
            
            # Simple significance estimate
            n_samples = len(residuals)
            if n_samples > 3:
                significance = np.abs(correlation) * np.sqrt(n_samples - 2)
            else:
                significance = 0
                
            echo_detections.append({
                'pulsar': pulsar['name'],
                'correlation': correlation,
                'significance': significance,
                'n_samples': n_samples
            })
            
        results['individual_detections'] = echo_detections
        
        # 2. Stacking analysis
        correlations = np.array(correlations)
        mean_correlation = np.mean(correlations)
        correlation_std = np.std(correlations)
        n_pulsars = len(correlations)
        
        # Stacked significance
        if correlation_std > 0 and n_pulsars > 1:
            stacked_significance = np.abs(mean_correlation) / (correlation_std / np.sqrt(n_pulsars))
        else:
            stacked_significance = 0
            
        results['stacking_analysis'] = {
            'mean_correlation': mean_correlation,
            'correlation_std': correlation_std,
            'stacked_significance': stacked_significance,
            'n_pulsars': n_pulsars,
            'individual_correlations': correlations.tolist()
        }
        
        # 3. Statistical tests
        
        # Test: Are correlations systematically positive?
        positive_correlations = np.sum(correlations > 0)
        total_correlations = len(correlations)
        
        if total_correlations > 0:
            # Binomial test (use binomtest for newer scipy versions)
            try:
                result = stats.binomtest(positive_correlations, total_correlations, 0.5)
                p_value_binomial = result.pvalue
            except AttributeError:
                # Fallback for older scipy versions
                p_value_binomial = stats.binom_test(positive_correlations, total_correlations, 0.5)
            
            if p_value_binomial > 0:
                binomial_significance = stats.norm.ppf(1 - p_value_binomial/2)
            else:
                binomial_significance = 0
        else:
            p_value_binomial = 1
            binomial_significance = 0
            
        # Test: Is mean correlation significantly different from zero?
        if correlation_std > 0 and n_pulsars > 1:
            t_statistic = mean_correlation / (correlation_std / np.sqrt(n_pulsars))
            p_value_ttest = 2 * (1 - stats.t.cdf(np.abs(t_statistic), n_pulsars - 1))
            if p_value_ttest > 0:
                ttest_significance = stats.norm.ppf(1 - p_value_ttest/2)
            else:
                ttest_significance = 0
        else:
            p_value_ttest = 1
            ttest_significance = 0
            
        # Combined significance
        combined_significance = np.sqrt(stacked_significance**2 + 
                                      binomial_significance**2 + 
                                      ttest_significance**2)
        
        results['statistical_tests'] = {
            'stacked_significance': stacked_significance,
            'binomial_significance': binomial_significance,
            'ttest_significance': ttest_significance,
            'combined_significance': combined_significance,
            'p_value_binomial': p_value_binomial,
            'p_value_ttest': p_value_ttest,
            'positive_correlations': positive_correlations,
            'total_correlations': total_correlations
        }
        
        self.echo_analysis = results
        return results
        
    def create_visualization(self):
        """Create Klein echo analysis visualization"""
        
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('IPTA Klein Electromagnetic Echo Detection (Simplified)', 
                     fontweight='bold', fontsize=14)
        
        # 1. Individual pulsar correlations
        ax1 = axes[0, 0]
        
        detections = self.echo_analysis['individual_detections']
        correlations = [d['correlation'] for d in detections]
        significances = [d['significance'] for d in detections]
        
        colors = ['red' if s > 2 else 'orange' if s > 1 else 'blue' for s in significances]
        scatter = ax1.scatter(correlations, significances, c=colors, alpha=0.7, s=60)
        
        ax1.axhline(2, color='orange', linestyle='--', alpha=0.7, label='2σ')
        ax1.axhline(3, color='red', linestyle='--', alpha=0.7, label='3σ')
        ax1.axvline(0, color='gray', linestyle='-', alpha=0.3)
        
        ax1.set_xlabel('Klein Echo Correlation')
        ax1.set_ylabel('Statistical Significance (σ)')
        ax1.set_title('A. Individual Pulsar Klein Echo Detection')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 2. Correlation histogram
        ax2 = axes[0, 1]
        
        ax2.hist(correlations, bins=10, alpha=0.7, density=True, color='skyblue')
        ax2.axvline(np.mean(correlations), color='red', linestyle='--', linewidth=2,
                   label=f'Mean: {np.mean(correlations):.4f}')
        ax2.axvline(0, color='gray', linestyle='-', alpha=0.5, label='No Correlation')
        
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
        
        summary_text = f"""
KLEIN ELECTROMAGNETIC ECHO ANALYSIS

THEORETICAL PREDICTIONS:
• Klein echo delay: {self.echo_delay:.6f} seconds
• Klein echo amplitude: {self.echo_amplitude_ratio:.2e}
• Klein frequency: {self.f0_klein} Hz

STACKING ANALYSIS:
• Mean correlation: {stacking_data['mean_correlation']:.4f}
• Correlation std: {stacking_data['correlation_std']:.4f}
• Stacked significance: {stacking_data['stacked_significance']:.2f}σ
• Number of pulsars: {stacking_data['n_pulsars']}

STATISTICAL TESTS:
• Combined significance: {stats_data['combined_significance']:.2f}σ
• Binomial significance: {stats_data['binomial_significance']:.2f}σ
• T-test significance: {stats_data['ttest_significance']:.2f}σ
• Positive correlations: {stats_data['positive_correlations']}/{stats_data['total_correlations']}

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
        
        # 4. Example pulsar time series
        ax4 = axes[1, 1]
        
        example_pulsar = self.pulsar_data['pulsars'][0]
        times = example_pulsar['observation_times'] / (365.25*24*3600)  # years
        residuals = example_pulsar['timing_residuals']
        klein_component = example_pulsar['klein_echo']
        
        ax4.plot(times, residuals, 'b-', alpha=0.7, label='Total Residuals')
        # Scale Klein component for visibility
        scaled_klein = klein_component * 1000
        ax4.plot(times, scaled_klein, 'r-', linewidth=2, 
                label='Klein Echo (×1000)')
        
        ax4.set_xlabel('Time (Years)')
        ax4.set_ylabel('Timing Residuals (μs)')
        ax4.set_title(f'C. Example: {example_pulsar["name"]}')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('ipta_klein_echo_simple.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print("✅ Klein echo visualization saved")

def main():
    """Main simplified Klein echo analysis"""
    analyzer = IPTAKleinEchoAnalyzer()
    
    if analyzer.generate_simple_pulsar_data():
        results = analyzer.analyze_klein_echoes()
        analyzer.create_visualization()
        
        stats = results['statistical_tests']
        stacking = results['stacking_analysis']
        
        print(f"\\n📡 IPTA KLEIN ELECTROMAGNETIC ECHO RESULTS:")
        print(f"   • Combined significance: {stats['combined_significance']:.2f}σ")
        print(f"   • Mean correlation: {stacking['mean_correlation']:.4f}")
        print(f"   • Stacked significance: {stacking['stacked_significance']:.2f}σ")
        print(f"   • Positive correlations: {stats['positive_correlations']}/{stats['total_correlations']}")
        
        status = ('DETECTED' if stats['combined_significance'] > 3 else 
                 'MARGINAL' if stats['combined_significance'] > 2 else 'NOT DETECTED')
        print(f"   • Status: Klein electromagnetic echoes {status}")
        
        return results
    return None

if __name__ == "__main__":
    main()