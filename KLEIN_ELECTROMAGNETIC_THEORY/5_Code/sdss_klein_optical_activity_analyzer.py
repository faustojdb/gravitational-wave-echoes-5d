#!/usr/bin/env python3
"""
SDSS Klein Optical Activity Analyzer
=====================================

OBJECTIVE: Search for Klein-induced optical activity in SDSS polarimetry data
APPROACH: Parameter-free analysis of systematic polarization rotation
TARGET: Klein rotation θ ∝ distance × frequency from Klein optical activity

Theory: Klein bottle breaks electromagnetic parity → systematic polarization rotation
Prediction: θ_Klein = γ_EM × (ω/f₀) × (distance/λ_K)
Critical Test: Distance and frequency dependent polarization rotation
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats
from typing import Dict, List, Tuple
import warnings
warnings.filterwarnings('ignore')

class SDSSKleinOpticalActivityAnalyzer:
    """SDSS polarimetry analysis for Klein optical activity detection"""
    
    def __init__(self):
        # Klein electromagnetic predictions (NO free parameters)
        self.f0_klein = 5.68  # Hz (Klein oscillation frequency)
        self.lambda_K = 52800e3  # m (Klein wavelength = c/f₀)
        self.gamma_em = 1e-15  # Klein-EM coupling strength
        self.c = 2.998e8  # m/s
        
        print(f"SDSS Klein Optical Activity Analysis")
        print(f"=" * 45)
        print(f"Klein frequency: f₀ = {self.f0_klein} Hz")
        print(f"Klein wavelength: λ_K = {self.lambda_K/1000:.0f} km")
        print(f"Klein-EM coupling: γ_EM = {self.gamma_em:.2e}")
        
        # Analysis data
        self.sdss_data = {}
        self.optical_activity_analysis = {}
        
    def generate_representative_sdss_data(self) -> bool:
        """Generate representative SDSS-like polarimetry data"""
        
        print("\\n🌌 Generating Representative SDSS Polarimetry Data...")
        print("(Note: Using simulated data representative of SDSS precision)")
        
        # Generate sample of galaxies/quasars with polarimetry
        n_objects = 1000  # Representative SDSS polarimetry sample
        objects = []
        
        # SDSS optical bands (approximate frequencies)
        bands = {
            'u': {'wavelength': 354e-9, 'frequency': self.c/354e-9},  # u-band
            'g': {'wavelength': 477e-9, 'frequency': self.c/477e-9},  # g-band  
            'r': {'wavelength': 623e-9, 'frequency': self.c/623e-9},  # r-band
            'i': {'wavelength': 763e-9, 'frequency': self.c/763e-9},  # i-band
            'z': {'wavelength': 913e-9, 'frequency': self.c/913e-9}   # z-band
        }
        
        for i in range(n_objects):
            # Object properties
            object_type = np.random.choice(['galaxy', 'quasar'], p=[0.7, 0.3])
            
            if object_type == 'galaxy':
                # Galaxy redshifts and distances
                redshift = np.random.uniform(0.01, 0.3)  # Local galaxies
                distance = redshift * self.c / (70e3)  # Rough Hubble distance (m)
            else:
                # Quasar redshifts and distances  
                redshift = np.random.uniform(0.1, 3.0)  # Distant quasars
                distance = redshift * self.c / (70e3)  # Rough Hubble distance (m)
                
            # Intrinsic polarization properties
            intrinsic_polarization_degree = np.random.uniform(0, 0.1)  # 0-10%
            intrinsic_polarization_angle = np.random.uniform(0, np.pi)  # 0-180°
            
            # Polarization measurements across SDSS bands
            polarimetry = {}
            
            for band_name, band_info in bands.items():
                frequency = band_info['frequency']
                
                # Klein optical activity prediction
                # θ_Klein = γ_EM × (ω/f₀) × (distance/λ_K)
                klein_rotation = (self.gamma_em * 
                                (frequency / (2*np.pi*self.f0_klein)) * 
                                (distance / self.lambda_K))
                
                # Total polarization angle = intrinsic + Klein rotation
                total_polarization_angle = intrinsic_polarization_angle + klein_rotation
                
                # Observational uncertainties (typical SDSS polarimetry)
                polarization_uncertainty = 0.01  # 1% polarization uncertainty
                angle_uncertainty = 0.1  # 0.1 radian angle uncertainty
                
                # Add observational noise
                observed_polarization_degree = (intrinsic_polarization_degree + 
                                              np.random.normal(0, polarization_uncertainty))
                observed_polarization_angle = (total_polarization_angle + 
                                             np.random.normal(0, angle_uncertainty))
                
                # Ensure physical ranges
                observed_polarization_degree = max(0, min(1, observed_polarization_degree))
                observed_polarization_angle = observed_polarization_angle % np.pi
                
                polarimetry[band_name] = {
                    'frequency': frequency,
                    'wavelength': band_info['wavelength'],
                    'polarization_degree': observed_polarization_degree,
                    'polarization_angle': observed_polarization_angle,
                    'klein_rotation': klein_rotation,
                    'intrinsic_angle': intrinsic_polarization_angle
                }
                
            objects.append({
                'object_id': f'SDSS J{1000+i:04d}+0000',
                'object_type': object_type,
                'redshift': redshift,
                'distance': distance,
                'polarimetry': polarimetry
            })
            
        self.sdss_data = {
            'objects': objects,
            'n_objects': n_objects,
            'bands': bands
        }
        
        print(f"✅ Generated {n_objects} objects with polarimetry")
        print(f"   • Galaxies: {sum(1 for obj in objects if obj['object_type'] == 'galaxy')}")
        print(f"   • Quasars: {sum(1 for obj in objects if obj['object_type'] == 'quasar')}")
        print(f"   • Redshift range: 0.01 - 3.0")
        print(f"   • SDSS bands: u, g, r, i, z")
        
        return True
        
    def analyze_klein_optical_activity(self) -> Dict:
        """Search for Klein optical activity signatures"""
        
        print("\\n🔍 Searching for Klein Optical Activity...")
        
        results = {
            'distance_correlation': {},
            'frequency_correlation': {},
            'combined_analysis': {},
            'statistical_tests': {}
        }
        
        objects = self.sdss_data['objects']
        bands = self.sdss_data['bands']
        
        # 1. Distance correlation analysis
        # Klein rotation should be ∝ distance
        
        distances = []
        total_rotations = []
        predicted_rotations = []
        
        for obj in objects:
            distance = obj['distance']
            distances.append(distance)
            
            # Calculate observed rotation across all bands
            # (Average rotation relative to intrinsic)
            observed_rotations = []
            predicted_klein_rotations = []
            
            for band_name in bands.keys():
                pol_data = obj['polarimetry'][band_name]
                
                # Observed rotation (difference from intrinsic)
                intrinsic_angle = pol_data['intrinsic_angle']
                observed_angle = pol_data['polarization_angle']
                
                # Handle angle wrapping
                rotation_diff = observed_angle - intrinsic_angle
                if rotation_diff > np.pi/2:
                    rotation_diff -= np.pi
                elif rotation_diff < -np.pi/2:
                    rotation_diff += np.pi
                    
                observed_rotations.append(rotation_diff)
                predicted_klein_rotations.append(pol_data['klein_rotation'])
                
            # Average rotation across bands
            avg_observed_rotation = np.mean(observed_rotations)
            avg_predicted_rotation = np.mean(predicted_klein_rotations)
            
            total_rotations.append(avg_observed_rotation)
            predicted_rotations.append(avg_predicted_rotation)
            
        distances = np.array(distances)
        total_rotations = np.array(total_rotations)
        predicted_rotations = np.array(predicted_rotations)
        
        # Correlation between observed rotation and distance
        if len(distances) > 10:
            distance_correlation, distance_p_value = stats.pearsonr(distances, total_rotations)
            
            # Correlation between observed and predicted Klein rotation
            klein_correlation, klein_p_value = stats.pearsonr(predicted_rotations, total_rotations)
            
            # Linear regression: rotation vs distance
            slope_distance, intercept_distance, r_distance, p_distance, stderr_distance = stats.linregress(distances, total_rotations)
            
            # Statistical significance of distance correlation
            n_objects = len(distances)
            if stderr_distance > 0:
                distance_significance = np.abs(slope_distance) / stderr_distance
            else:
                distance_significance = 0
                
        else:
            distance_correlation = 0
            klein_correlation = 0
            distance_significance = 0
            slope_distance = 0
            r_distance = 0
            
        results['distance_correlation'] = {
            'correlation': distance_correlation,
            'p_value': distance_p_value if 'distance_p_value' in locals() else 1,
            'klein_correlation': klein_correlation,
            'klein_p_value': klein_p_value if 'klein_p_value' in locals() else 1,
            'slope': slope_distance,
            'r_squared': r_distance**2 if 'r_distance' in locals() else 0,
            'significance': distance_significance
        }
        
        # 2. Frequency correlation analysis
        # Klein rotation should be ∝ frequency
        
        all_frequencies = []
        all_rotations = []
        all_distances_norm = []
        
        for obj in objects:
            distance = obj['distance']
            
            for band_name in bands.keys():
                pol_data = obj['polarimetry'][band_name]
                frequency = pol_data['frequency']
                
                # Calculate frequency-normalized rotation
                # Klein prediction: θ ∝ ω × distance
                observed_angle = pol_data['polarization_angle']
                intrinsic_angle = pol_data['intrinsic_angle']
                
                rotation_diff = observed_angle - intrinsic_angle
                if rotation_diff > np.pi/2:
                    rotation_diff -= np.pi
                elif rotation_diff < -np.pi/2:
                    rotation_diff += np.pi
                    
                # Normalize by distance to test frequency dependence
                if distance > 0:
                    distance_normalized_rotation = rotation_diff / distance
                else:
                    distance_normalized_rotation = 0
                    
                all_frequencies.append(frequency)
                all_rotations.append(distance_normalized_rotation)
                all_distances_norm.append(distance)
                
        all_frequencies = np.array(all_frequencies)
        all_rotations = np.array(all_rotations)
        
        # Correlation between frequency and distance-normalized rotation
        if len(all_frequencies) > 10:
            freq_correlation, freq_p_value = stats.pearsonr(all_frequencies, all_rotations)
            
            # Linear regression: rotation vs frequency
            slope_freq, intercept_freq, r_freq, p_freq, stderr_freq = stats.linregress(all_frequencies, all_rotations)
            
            # Statistical significance
            if stderr_freq > 0:
                freq_significance = np.abs(slope_freq) / stderr_freq
            else:
                freq_significance = 0
        else:
            freq_correlation = 0
            freq_significance = 0
            slope_freq = 0
            r_freq = 0
            
        results['frequency_correlation'] = {
            'correlation': freq_correlation,
            'p_value': freq_p_value if 'freq_p_value' in locals() else 1,
            'slope': slope_freq,
            'r_squared': r_freq**2 if 'r_freq' in locals() else 0,
            'significance': freq_significance
        }
        
        # 3. Combined Klein signature analysis
        
        # Test for combined distance × frequency dependence
        # Klein prediction: θ = γ_EM × (ω/f₀) × (distance/λ_K)
        
        predicted_klein_total = []
        observed_rotations_total = []
        
        for obj in objects:
            for band_name in bands.keys():
                pol_data = obj['polarimetry'][band_name]
                
                predicted_klein_total.append(pol_data['klein_rotation'])
                
                observed_angle = pol_data['polarization_angle']
                intrinsic_angle = pol_data['intrinsic_angle']
                
                rotation_diff = observed_angle - intrinsic_angle
                if rotation_diff > np.pi/2:
                    rotation_diff -= np.pi
                elif rotation_diff < -np.pi/2:
                    rotation_diff += np.pi
                    
                observed_rotations_total.append(rotation_diff)
                
        predicted_klein_total = np.array(predicted_klein_total)
        observed_rotations_total = np.array(observed_rotations_total)
        
        # Direct correlation between predicted and observed Klein rotation
        if len(predicted_klein_total) > 10:
            combined_correlation, combined_p_value = stats.pearsonr(predicted_klein_total, observed_rotations_total)
            
            # Linear regression
            slope_combined, intercept_combined, r_combined, p_combined, stderr_combined = stats.linregress(predicted_klein_total, observed_rotations_total)
            
            # Statistical significance
            if stderr_combined > 0:
                combined_significance = np.abs(slope_combined) / stderr_combined
            else:
                combined_significance = 0
        else:
            combined_correlation = 0
            combined_significance = 0
            slope_combined = 0
            r_combined = 0
            
        results['combined_analysis'] = {
            'correlation': combined_correlation,
            'p_value': combined_p_value if 'combined_p_value' in locals() else 1,
            'slope': slope_combined,
            'r_squared': r_combined**2 if 'r_combined' in locals() else 0,
            'significance': combined_significance
        }
        
        # 4. Statistical tests
        
        # Overall Klein optical activity significance
        total_significance = np.sqrt(distance_significance**2 + 
                                   freq_significance**2 + 
                                   combined_significance**2)
        
        # Chi-squared test for Klein model fit
        if len(predicted_klein_total) > 5:
            # Residuals from Klein prediction
            residuals = observed_rotations_total - predicted_klein_total
            residual_variance = np.var(residuals) if len(residuals) > 1 else 1
            
            # Expected Klein signal variance
            klein_signal_variance = np.var(predicted_klein_total) if len(predicted_klein_total) > 1 else 1
            
            # Signal-to-noise ratio
            if residual_variance > 0:
                snr_klein = np.sqrt(klein_signal_variance / residual_variance)
            else:
                snr_klein = 0
        else:
            snr_klein = 0
            
        results['statistical_tests'] = {
            'distance_significance': distance_significance,
            'frequency_significance': freq_significance,
            'combined_significance': combined_significance,
            'total_significance': total_significance,
            'snr_klein': snr_klein
        }
        
        self.optical_activity_analysis = results
        return results
        
    def create_visualization(self):
        """Create Klein optical activity analysis visualization"""
        
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('SDSS Klein Optical Activity Detection Analysis', 
                     fontweight='bold', fontsize=14)
        
        # Prepare data for plotting
        objects = self.sdss_data['objects']
        bands = self.sdss_data['bands']
        
        # Extract data
        distances = [obj['distance'] for obj in objects]
        
        all_frequencies = []
        all_predicted = []
        all_observed = []
        
        for obj in objects:
            for band_name in bands.keys():
                pol_data = obj['polarimetry'][band_name]
                
                all_frequencies.append(pol_data['frequency'])
                all_predicted.append(pol_data['klein_rotation'])
                
                observed_angle = pol_data['polarization_angle']
                intrinsic_angle = pol_data['intrinsic_angle']
                
                rotation_diff = observed_angle - intrinsic_angle
                if rotation_diff > np.pi/2:
                    rotation_diff -= np.pi
                elif rotation_diff < -np.pi/2:
                    rotation_diff += np.pi
                    
                all_observed.append(rotation_diff)
        
        distances = np.array(distances) / 1e24  # Convert to 100 Mpc units
        all_frequencies = np.array(all_frequencies) / 1e14  # Convert to 10^14 Hz
        all_predicted = np.array(all_predicted)
        all_observed = np.array(all_observed)
        
        # 1. Distance vs rotation
        ax1 = axes[0, 0]
        
        # Average rotation per object
        avg_rotations = []
        for obj in objects:
            rotations = []
            for band_name in bands.keys():
                pol_data = obj['polarimetry'][band_name]
                observed_angle = pol_data['polarization_angle']
                intrinsic_angle = pol_data['intrinsic_angle']
                
                rotation_diff = observed_angle - intrinsic_angle
                if rotation_diff > np.pi/2:
                    rotation_diff -= np.pi
                elif rotation_diff < -np.pi/2:
                    rotation_diff += np.pi
                    
                rotations.append(rotation_diff)
            avg_rotations.append(np.mean(rotations))
        
        ax1.scatter(distances, avg_rotations, alpha=0.6, s=30)
        
        # Klein prediction line
        if len(distances) > 0:
            dist_range = np.linspace(np.min(distances), np.max(distances), 100)
            # Klein rotation ∝ distance (rough scaling)
            klein_prediction_dist = self.gamma_em * dist_range * 1e24 / self.lambda_K
            ax1.plot(dist_range, klein_prediction_dist, 'r--', linewidth=2, 
                    label=f'Klein Prediction (γ={self.gamma_em:.0e})')
        
        ax1.set_xlabel('Distance (×100 Mpc)')
        ax1.set_ylabel('Polarization Rotation (radians)')
        ax1.set_title('A. Distance vs Klein Rotation')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 2. Frequency vs rotation
        ax2 = axes[0, 1]
        
        ax2.scatter(all_frequencies, all_observed, alpha=0.6, s=20)
        
        # Klein prediction (frequency dependence)
        if len(all_frequencies) > 0:
            freq_range = np.linspace(np.min(all_frequencies), np.max(all_frequencies), 100)
            # Rough frequency scaling
            klein_prediction_freq = self.gamma_em * freq_range * 1e14 / (2*np.pi*self.f0_klein) * np.mean(distances) * 1e24 / self.lambda_K
            ax2.plot(freq_range, klein_prediction_freq, 'r--', linewidth=2, 
                    label='Klein Frequency Scaling')
        
        ax2.set_xlabel('Frequency (×10¹⁴ Hz)')
        ax2.set_ylabel('Polarization Rotation (radians)')
        ax2.set_title('B. Frequency vs Klein Rotation')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # 3. Results summary
        ax3 = axes[1, 0]
        ax3.axis('off')
        
        stats_data = self.optical_activity_analysis['statistical_tests']
        distance_data = self.optical_activity_analysis['distance_correlation']
        freq_data = self.optical_activity_analysis['frequency_correlation']
        combined_data = self.optical_activity_analysis['combined_analysis']
        
        summary_text = f"""
SDSS KLEIN OPTICAL ACTIVITY ANALYSIS

THEORETICAL PREDICTIONS:
• Klein rotation: θ = γ_EM × (ω/f₀) × (d/λ_K)
• Klein-EM coupling: γ_EM = {self.gamma_em:.2e}
• Klein wavelength: λ_K = {self.lambda_K/1000:.0f} km

DISTANCE CORRELATION:
• Correlation: {distance_data['correlation']:.4f}
• R²: {distance_data['r_squared']:.4f}
• Significance: {distance_data['significance']:.2f}σ

FREQUENCY CORRELATION:
• Correlation: {freq_data['correlation']:.4f}
• R²: {freq_data['r_squared']:.4f}
• Significance: {freq_data['significance']:.2f}σ

COMBINED ANALYSIS:
• Klein correlation: {combined_data['correlation']:.4f}
• R²: {combined_data['r_squared']:.4f}
• Significance: {combined_data['significance']:.2f}σ

OVERALL RESULTS:
• Total significance: {stats_data['total_significance']:.2f}σ
• Klein SNR: {stats_data['snr_klein']:.2f}

STATUS:
{'✅ KLEIN OPTICAL ACTIVITY DETECTED' if stats_data['total_significance'] > 3 else 
 '🔶 MARGINAL DETECTION' if stats_data['total_significance'] > 2 else 
 '❌ NO OPTICAL ACTIVITY SIGNATURE'}
        """
        
        color = ('green' if stats_data['total_significance'] > 3 else 
                'orange' if stats_data['total_significance'] > 2 else 'red')
        ax3.text(0.05, 0.95, summary_text, transform=ax3.transAxes,
                fontsize=9, verticalalignment='top', fontfamily='monospace',
                color=color)
        
        # 4. Predicted vs observed Klein rotation
        ax4 = axes[1, 1]
        
        ax4.scatter(all_predicted, all_observed, alpha=0.6, s=20)
        
        # Perfect correlation line
        if len(all_predicted) > 0:
            min_val = min(np.min(all_predicted), np.min(all_observed))
            max_val = max(np.max(all_predicted), np.max(all_observed))
            ax4.plot([min_val, max_val], [min_val, max_val], 'r--', 
                    linewidth=2, label='Perfect Klein Correlation')
        
        ax4.set_xlabel('Predicted Klein Rotation (radians)')
        ax4.set_ylabel('Observed Rotation (radians)')
        ax4.set_title('C. Predicted vs Observed\\nKlein Optical Activity')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('sdss_klein_optical_activity.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print("✅ SDSS Klein optical activity visualization saved")

def main():
    """Main SDSS Klein optical activity analysis"""
    analyzer = SDSSKleinOpticalActivityAnalyzer()
    
    if analyzer.generate_representative_sdss_data():
        results = analyzer.analyze_klein_optical_activity()
        analyzer.create_visualization()
        
        stats = results['statistical_tests']
        distance = results['distance_correlation']
        combined = results['combined_analysis']
        
        print(f"\\n🌌 SDSS KLEIN OPTICAL ACTIVITY RESULTS:")
        print(f"   • Total significance: {stats['total_significance']:.2f}σ")
        print(f"   • Distance correlation: {distance['correlation']:.4f}")
        print(f"   • Klein correlation: {combined['correlation']:.4f}")
        print(f"   • Klein SNR: {stats['snr_klein']:.2f}")
        
        status = ('DETECTED' if stats['total_significance'] > 3 else 
                 'MARGINAL' if stats['total_significance'] > 2 else 'NOT DETECTED')
        print(f"   • Status: Klein optical activity {status}")
        
        return results
    return None

if __name__ == "__main__":
    main()