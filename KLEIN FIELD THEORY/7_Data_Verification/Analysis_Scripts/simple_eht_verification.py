#!/usr/bin/env python3
"""
Simplified EHT Klein Verification Analysis
No external dependencies required - uses only standard Python libraries
"""

import json
import math
import os
from datetime import datetime

class SimpleEHTVerifier:
    """Simplified EHT verification using only standard Python."""
    
    def __init__(self, data_dir="../EHT_Data"):
        self.data_dir = data_dir
        self.klein_enhancement = 1.193  # +19.3% Klein prediction
        
        # Create data directory
        os.makedirs(data_dir, exist_ok=True)
        
    def get_eht_measurements(self):
        """EHT shadow measurements from published papers."""
        
        measurements = {
            'M87_2019': {
                'shadow_diameter_uas': 42.0,
                'uncertainty_uas': 3.0,
                'reference': 'EHT Collaboration 2019, ApJ 875, L1',
                'date': '2019-04-10',
                'mass_msun': 6.5e9,
                'distance_mpc': 16.8,
                'source_type': 'supermassive'
            },
            'M87_2021': {
                'shadow_diameter_uas': 41.5,
                'uncertainty_uas': 2.8,
                'reference': 'EHT Collaboration 2021, ApJ 910, L12',  
                'date': '2018-04-11',
                'mass_msun': 6.5e9,
                'distance_mpc': 16.8,
                'source_type': 'supermassive'
            },
            'SgrA_2022': {
                'shadow_diameter_uas': 52.0,
                'uncertainty_uas': 2.3,
                'reference': 'EHT Collaboration 2022, ApJ 930, L12',
                'date': '2017-04-06-11',
                'mass_msun': 4.15e6,
                'distance_mpc': 0.008,  # 8.15 kpc
                'source_type': 'supermassive'
            }
        }
        
        return measurements
    
    def calculate_theoretical_predictions(self, measurements):
        """Calculate GR and Klein theoretical predictions."""
        
        # Physical constants
        G = 6.674e-11  # m³/kg/s²
        c = 2.998e8    # m/s
        msun = 1.989e30  # kg
        mpc_to_m = 3.086e22  # meters per Mpc
        uas_per_radian = 206265e6  # microarcseconds per radian
        
        predictions = {}
        
        for source, data in measurements.items():
            # Calculate Schwarzschild radius
            mass_kg = data['mass_msun'] * msun
            rs_m = 2 * G * mass_kg / (c**2)
            
            # Distance in meters
            distance_m = data['distance_mpc'] * mpc_to_m
            
            # Angular Schwarzschild radius in microarcseconds
            rs_uas = (rs_m / distance_m) * uas_per_radian
            
            # Shadow radius is approximately 2.6 Rs for Schwarzschild BH
            shadow_gr_uas = 2.6 * rs_uas
            
            # Klein prediction: 19.3% larger
            shadow_klein_uas = shadow_gr_uas * self.klein_enhancement
            
            # Calculate deviations
            observed = data['shadow_diameter_uas']
            uncertainty = data['uncertainty_uas']
            
            deviation_gr = (observed - shadow_gr_uas) / uncertainty
            deviation_klein = (observed - shadow_klein_uas) / uncertainty
            
            predictions[source] = {
                'observed_uas': observed,
                'uncertainty_uas': uncertainty,
                'gr_prediction_uas': shadow_gr_uas,
                'klein_prediction_uas': shadow_klein_uas,
                'schwarzschild_radius_uas': rs_uas,
                'deviation_from_gr_sigma': deviation_gr,
                'deviation_from_klein_sigma': deviation_klein,
                'better_fit': 'Klein' if abs(deviation_klein) < abs(deviation_gr) else 'GR',
                'enhancement_factor_observed': observed / shadow_gr_uas,
                'enhancement_factor_predicted': self.klein_enhancement
            }
            
        return predictions
    
    def perform_statistical_analysis(self, predictions):
        """Perform chi-squared and statistical analysis."""
        
        # Extract deviations
        gr_deviations = [p['deviation_from_gr_sigma'] for p in predictions.values()]
        klein_deviations = [p['deviation_from_klein_sigma'] for p in predictions.values()]
        
        # Calculate chi-squared
        chi2_gr = sum([dev**2 for dev in gr_deviations])
        chi2_klein = sum([dev**2 for dev in klein_deviations])
        
        n_measurements = len(predictions)
        dof = n_measurements - 1
        
        # Basic statistics
        mean_abs_gr = sum([abs(dev) for dev in gr_deviations]) / n_measurements
        mean_abs_klein = sum([abs(dev) for dev in klein_deviations]) / n_measurements
        
        rms_gr = math.sqrt(sum([dev**2 for dev in gr_deviations]) / n_measurements)
        rms_klein = math.sqrt(sum([dev**2 for dev in klein_deviations]) / n_measurements)
        
        # Count better fits
        klein_better = sum([1 for p in predictions.values() if p['better_fit'] == 'Klein'])
        gr_better = sum([1 for p in predictions.values() if p['better_fit'] == 'GR'])
        
        statistics = {
            'n_measurements': n_measurements,
            'degrees_of_freedom': dof,
            'chi2_gr': chi2_gr,
            'chi2_klein': chi2_klein,
            'chi2_reduced_gr': chi2_gr / dof if dof > 0 else float('inf'),
            'chi2_reduced_klein': chi2_klein / dof if dof > 0 else float('inf'),
            'delta_chi2': chi2_gr - chi2_klein,
            'preferred_model_chi2': 'Klein' if chi2_klein < chi2_gr else 'GR',
            'mean_abs_deviation_gr': mean_abs_gr,
            'mean_abs_deviation_klein': mean_abs_klein,
            'rms_deviation_gr': rms_gr,
            'rms_deviation_klein': rms_klein,
            'klein_better_fits': klein_better,
            'gr_better_fits': gr_better,
            'klein_success_rate': klein_better / n_measurements
        }
        
        return statistics
    
    def generate_summary_report(self, measurements, predictions, stats):
        """Generate text-based summary report."""
        
        report = f"""
{'='*80}
EHT KLEIN VERIFICATION ANALYSIS SUMMARY
{'='*80}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

KLEIN PREDICTION: Black hole shadows should be {(self.klein_enhancement-1)*100:.1f}% larger than GR

DATA SUMMARY:
- Total measurements: {stats['n_measurements']}
- Sources: M87* (2019, 2021), Sgr A* (2022)
- All measurements from EHT Collaboration papers

STATISTICAL RESULTS:
{'='*40}
Model Comparison (Chi-squared):
- GR χ²: {stats['chi2_gr']:.3f}
- Klein χ²: {stats['chi2_klein']:.3f}
- Δχ² (GR - Klein): {stats['delta_chi2']:.3f}
- Preferred model: {stats['preferred_model_chi2']}

Deviation Analysis:
- Mean |deviation| from GR: {stats['mean_abs_deviation_gr']:.2f}σ
- Mean |deviation| from Klein: {stats['mean_abs_deviation_klein']:.2f}σ
- RMS deviation from GR: {stats['rms_deviation_gr']:.2f}σ  
- RMS deviation from Klein: {stats['rms_deviation_klein']:.2f}σ

Individual Fit Quality:
- Klein fits better: {stats['klein_better_fits']}/{stats['n_measurements']} ({stats['klein_success_rate']:.1%})
- GR fits better: {stats['gr_better_fits']}/{stats['n_measurements']} ({1-stats['klein_success_rate']:.1%})

DETAILED RESULTS:
{'='*40}
"""
        
        for source, pred in predictions.items():
            source_name = source.replace('_', ' ')
            report += f"""
{source_name}:
- Observed: {pred['observed_uas']:.1f} ± {pred['uncertainty_uas']:.1f} μas
- GR prediction: {pred['gr_prediction_uas']:.1f} μas
- Klein prediction: {pred['klein_prediction_uas']:.1f} μas
- Deviation from GR: {pred['deviation_from_gr_sigma']:.2f}σ
- Deviation from Klein: {pred['deviation_from_klein_sigma']:.2f}σ
- Better fit: {pred['better_fit']}
- Enhancement factor: {pred['enhancement_factor_observed']:.3f} (observed) vs {pred['enhancement_factor_predicted']:.3f} (Klein)
"""
        
        # Conclusions
        report += f"""
CONCLUSIONS:
{'='*40}
"""
        
        if stats['preferred_model_chi2'] == 'Klein':
            if stats['delta_chi2'] > 2:
                strength = "STRONG"
            elif stats['delta_chi2'] > 1:
                strength = "MODERATE"  
            else:
                strength = "WEAK"
                
            report += f"""
✅ KLEIN MODEL FAVORED ({strength} EVIDENCE)
- Klein provides better statistical fit to EHT data
- Δχ² = {stats['delta_chi2']:.3f} in favor of Klein
- {stats['klein_better_fits']}/{stats['n_measurements']} individual measurements favor Klein
"""
        else:
            if stats['delta_chi2'] < -2:
                strength = "STRONG"
            elif stats['delta_chi2'] < -1:
                strength = "MODERATE"
            else:
                strength = "WEAK"
                
            report += f"""
❌ GR MODEL FAVORED ({strength} EVIDENCE)
- Standard GR provides better fit to EHT data  
- Δχ² = {-stats['delta_chi2']:.3f} in favor of GR
- {stats['gr_better_fits']}/{stats['n_measurements']} individual measurements favor GR
"""
        
        # Assessment of Klein enhancement
        enhancement_factors = [p['enhancement_factor_observed'] for p in predictions.values()]
        mean_enhancement = sum(enhancement_factors) / len(enhancement_factors)
        
        report += f"""
KLEIN ENHANCEMENT ANALYSIS:
- Predicted enhancement: {self.klein_enhancement:.3f} (+{(self.klein_enhancement-1)*100:.1f}%)
- Observed mean enhancement: {mean_enhancement:.3f} (+{(mean_enhancement-1)*100:.1f}%)
- Difference: {abs(mean_enhancement - self.klein_enhancement):.3f} ({abs(mean_enhancement - self.klein_enhancement)/self.klein_enhancement*100:.1f}%)

"""
        
        if abs(mean_enhancement - self.klein_enhancement) / self.klein_enhancement < 0.1:
            report += "🎯 Observed enhancement within 10% of Klein prediction - EXCELLENT AGREEMENT\n"
        elif abs(mean_enhancement - self.klein_enhancement) / self.klein_enhancement < 0.2:
            report += "✅ Observed enhancement within 20% of Klein prediction - GOOD AGREEMENT\n"
        else:
            report += "⚠️ Observed enhancement deviates >20% from Klein prediction - TENSION\n"
        
        report += f"""
LIMITATIONS:
- Small sample size (n={stats['n_measurements']}) limits statistical power
- Systematic uncertainties in shadow measurements not fully characterized
- Klein breathing (temporal variations) not yet detected
- Need polarization analysis for complete Klein test

FUTURE PROSPECTS:
- Next-generation EHT observations with higher time/spatial resolution
- Detection of Klein breathing at f₀ = 5.68 Hz
- More black hole shadow measurements for larger statistical sample
- Multi-wavelength Klein signature analysis

REFERENCES:
"""
        
        for source, data in measurements.items():
            report += f"- {data['reference']}\n"
        
        report += f"\n{'='*80}\n"
        
        return report
    
    def save_results(self, measurements, predictions, stats, report):
        """Save all results to files."""
        
        # Save JSON data
        results = {
            'measurements': measurements,
            'predictions': predictions,
            'statistics': stats,
            'analysis_date': datetime.now().isoformat(),
            'klein_enhancement_predicted': self.klein_enhancement
        }
        
        with open(f"{self.data_dir}/eht_klein_results.json", 'w') as f:
            json.dump(results, f, indent=2)
        
        # Save report
        with open(f"{self.data_dir}/eht_klein_report.txt", 'w') as f:
            f.write(report)
        
        print(f"✅ Results saved to {self.data_dir}/")
        
        return results
    
    def run_analysis(self):
        """Run complete simplified EHT analysis."""
        
        print("🚀 Starting EHT Klein Verification Analysis...")
        print("📊 Using published EHT shadow measurements")
        
        # Get measurements
        measurements = self.get_eht_measurements()
        print(f"📈 Loaded {len(measurements)} EHT measurements")
        
        # Calculate predictions
        predictions = self.calculate_theoretical_predictions(measurements)
        print("🔬 Calculated GR and Klein predictions")
        
        # Statistical analysis
        stats = self.perform_statistical_analysis(predictions)
        print("📊 Performed statistical analysis")
        
        # Generate report
        report = self.generate_summary_report(measurements, predictions, stats)
        
        # Save results
        results = self.save_results(measurements, predictions, stats, report)
        
        # Print report
        print(report)
        
        return results

if __name__ == "__main__":
    verifier = SimpleEHTVerifier()
    results = verifier.run_analysis()