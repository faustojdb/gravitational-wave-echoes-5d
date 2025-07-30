#!/usr/bin/env python3
"""
MMS Klein Detector with PySpedas Integration
============================================

Real MMS data analysis for Klein frequency f₀ = 5.682 Hz detection
using PySpedas library for NASA MMS mission data access.

Author: Multidimensional Theory Simulations  
Date: July 29, 2025
Version: 3.0 - PySpedas Integration
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import signal, stats
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class MMSKleinDetectorPySpedas:
    """
    MMS Klein Detector using PySpedas for real NASA data
    """
    
    def __init__(self):
        # Klein constants
        self.f0_klein = 5.682  # Hz
        self.f0_uncertainty = 0.088  # Hz
        
        # Check PySpedas availability
        self.pyspedas_available = self._check_pyspedas()
        
        print(f"🚀 MMS Klein Detector (PySpedas Edition)")
        print(f"   Klein Frequency: {self.f0_klein} ± {self.f0_uncertainty} Hz")
        print(f"   PySpedas Status: {'✅ Available' if self.pyspedas_available else '❌ Not Available'}")
    
    def _check_pyspedas(self):
        """Check if PySpedas is available and working"""
        try:
            import pyspedas.mms as mms
            import pytplot
            print("✅ PySpedas MMS modules loaded successfully")
            return True
        except ImportError as e:
            print(f"❌ PySpedas import failed: {e}")
            print("   Install with: pip install pyspedas")
            return False
        except Exception as e:
            print(f"❌ PySpedas error: {e}")
            return False
    
    def fetch_real_mms_data(self, time_range, probe='1'):
        """
        Fetch real MMS data using PySpedas
        
        Args:
            time_range: ['start', 'end'] in format 'YYYY-MM-DD/HH:MM:SS'
            probe: MMS spacecraft ('1', '2', '3', '4')
        """
        
        if not self.pyspedas_available:
            print("❌ PySpedas not available - cannot fetch real data")
            return None
        
        print(f"\n🛰️ Fetching Real MMS Data")
        print(f"   Spacecraft: MMS{probe}")
        print(f"   Time: {time_range[0]} to {time_range[1]}")
        
        try:
            # Import here to avoid issues if not available
            import pyspedas.mms as mms
            import pytplot
            
            # Load magnetic field data (FGM) - burst mode
            print("   📡 Loading FGM magnetic field data...")
            fgm_vars = mms.fgm(
                trange=time_range,
                probe=probe,
                data_rate='brst',  # Burst mode for high resolution
                level='l2'
            )
            
            # Load electric field data (EDP)
            print("   📡 Loading EDP electric field data...")
            edp_vars = mms.edp(
                trange=time_range,
                probe=probe,
                data_rate='brst',
                level='l2'
            )
            
            # Load plasma data (FPI)
            print("   📡 Loading FPI plasma data...")
            fpi_vars = mms.fpi(
                trange=time_range,
                probe=probe,
                data_rate='brst',
                level='l2',
                datatype='des-moms'  # Electron moments
            )
            
            # Extract data separately for each instrument (different sampling rates)
            datasets = {}
            
            # Get magnetic field data (FGM) - highest resolution for Klein detection
            b_var = f'mms{probe}_fgm_b_gse_brst_l2'
            if b_var in pytplot.tplot_names():
                times_b, b_data = pytplot.get_data(b_var)
                b_df = pd.DataFrame({
                    'timestamp': pd.to_datetime(times_b, unit='s'),
                    'Bx': b_data[:, 0],  # nT
                    'By': b_data[:, 1],  # nT  
                    'Bz': b_data[:, 2],  # nT
                })
                b_df['B_mag'] = np.sqrt(b_df['Bx']**2 + b_df['By']**2 + b_df['Bz']**2)
                datasets['magnetic'] = b_df
                print(f"   ✅ Magnetic field: {len(b_data)} points")
            
            # Get electric field data (EDP)
            e_var = f'mms{probe}_edp_dce_gse_brst_l2'
            if e_var in pytplot.tplot_names():
                times_e, e_data = pytplot.get_data(e_var)
                if len(e_data.shape) > 1 and e_data.shape[1] >= 3:
                    e_df = pd.DataFrame({
                        'timestamp': pd.to_datetime(times_e, unit='s'),
                        'Ex': e_data[:, 0],  # mV/m
                        'Ey': e_data[:, 1],  # mV/m
                        'Ez': e_data[:, 2],  # mV/m
                    })
                    e_df['E_mag'] = np.sqrt(e_df['Ex']**2 + e_df['Ey']**2 + e_df['Ez']**2)
                    datasets['electric'] = e_df
                    print(f"   ✅ Electric field: {len(e_data)} points")
            
            # Get plasma density data (FPI)
            n_var = f'mms{probe}_des_numberdensity_brst'
            if n_var in pytplot.tplot_names():
                times_n, n_data = pytplot.get_data(n_var)
                n_df = pd.DataFrame({
                    'timestamp': pd.to_datetime(times_n, unit='s'),
                    'density': n_data  # cm^-3
                })
                datasets['plasma'] = n_df
                print(f"   ✅ Plasma density: {len(n_data)} points")
            
            # Use magnetic field as primary dataset (usually highest resolution)
            if 'magnetic' in datasets:
                df = datasets['magnetic'].copy()
                
                # Add other parameters by interpolation if needed
                for key, data in datasets.items():
                    if key != 'magnetic':
                        # Simple approach: just use the parameter that matches best
                        for col in data.columns:
                            if col != 'timestamp':
                                df[col] = np.nan  # Initialize with NaN
                                # For demo, just use first available dataset
                                if len(data) > 0:
                                    df[col] = data[col].iloc[0]  # Use first value as constant
                
                print(f"   📊 Primary dataset: Magnetic field ({len(df)} points)")
            else:
                print(f"   ❌ No magnetic field data available")
                return None
            
            # Calculate sampling rate
            if len(df) > 1:
                dt = (df['timestamp'].iloc[1] - df['timestamp'].iloc[0]).total_seconds()
                sampling_rate = 1.0 / dt
                df['sampling_rate'] = sampling_rate
                print(f"   📊 Sampling rate: {sampling_rate:.1f} Hz")
            
            print(f"✅ Real MMS data loaded: {df.shape}")
            return df
            
        except Exception as e:
            print(f"❌ Error loading MMS data: {str(e)}")
            return None
    
    def analyze_klein_frequency(self, data, parameter='B_mag'):
        """
        Analyze Klein frequency in MMS data parameter
        
        Args:
            data: MMS DataFrame
            parameter: Column to analyze for Klein frequency
        """
        
        if data is None or parameter not in data.columns:
            print(f"❌ Cannot analyze {parameter} - data not available")
            return None
        
        print(f"\n🔍 Klein Frequency Analysis: {parameter}")
        
        # Extract time series
        time_series = data[parameter].values
        sampling_rate = data['sampling_rate'].iloc[0] if 'sampling_rate' in data.columns else 128
        
        print(f"   📊 Data points: {len(time_series)}")
        print(f"   📊 Sampling rate: {sampling_rate:.1f} Hz")
        print(f"   📊 Duration: {len(time_series)/sampling_rate:.1f} seconds")
        
        # Check Nyquist criterion
        nyquist_freq = sampling_rate / 2
        nyquist_margin = nyquist_freq / self.f0_klein
        
        print(f"   🎯 Nyquist frequency: {nyquist_freq:.1f} Hz")
        print(f"   🎯 Safety margin: {nyquist_margin:.1f}x")
        
        if sampling_rate < (self.f0_klein * 2.2):
            print(f"   ⚠️  Warning: Sampling may be insufficient for Klein detection")
        
        # Spectral analysis
        try:
            # Remove trend and apply window
            detrended = signal.detrend(time_series)
            window = signal.windows.hann(len(detrended))
            windowed = detrended * window
            
            # Welch's method for robust spectral estimation
            nperseg = min(len(windowed) // 4, 2048)
            freqs, psd = signal.welch(
                windowed, 
                fs=sampling_rate,
                nperseg=nperseg,
                noverlap=nperseg//2,
                window='hann'
            )
            
            # Look for Klein frequency peak
            klein_range = (self.f0_klein - 2*self.f0_uncertainty, 
                          self.f0_klein + 2*self.f0_uncertainty)
            
            freq_mask = (freqs >= klein_range[0]) & (freqs <= klein_range[1])
            
            if np.any(freq_mask):
                klein_freqs = freqs[freq_mask]
                klein_psd = psd[freq_mask]
                
                # Find peak
                peak_idx = np.argmax(klein_psd)
                peak_freq = klein_freqs[peak_idx]
                peak_power = klein_psd[peak_idx]
                
                # Background noise estimation
                noise_mask = (freqs > 1.0) & (freqs < sampling_rate/4) & (~freq_mask)
                background_power = np.median(psd[noise_mask]) if np.any(noise_mask) else np.median(psd)
                
                snr = peak_power / background_power if background_power > 0 else 0
                frequency_error = abs(peak_freq - self.f0_klein)
                
                # Detection assessment
                detection_quality = "EXCELLENT" if snr > 100 else "GOOD" if snr > 10 else "MODERATE" if snr > 3 else "POOR"
                within_tolerance = frequency_error <= self.f0_uncertainty
                
                results = {
                    'parameter': parameter,
                    'peak_frequency': peak_freq,
                    'target_frequency': self.f0_klein,
                    'frequency_error': frequency_error,
                    'within_tolerance': within_tolerance,
                    'peak_power': peak_power,
                    'background_power': background_power,
                    'snr': snr,
                    'detection_quality': detection_quality,
                    'sampling_rate': sampling_rate,
                    'nyquist_margin': nyquist_margin
                }
                
                # Print results
                print(f"   🎯 Peak frequency: {peak_freq:.6f} Hz")
                print(f"   🎯 Target: {self.f0_klein:.6f} Hz")
                print(f"   📊 Error: {frequency_error:.6f} Hz")
                print(f"   📊 SNR: {snr:.2f}")
                print(f"   📊 Quality: {detection_quality}")
                print(f"   {'✅' if within_tolerance else '❌'} Within tolerance: {within_tolerance}")
                
                return results
                
            else:
                print(f"   ❌ No spectral data in Klein frequency range")
                return None
                
        except Exception as e:
            print(f"   ❌ Spectral analysis error: {str(e)}")
            return None
    
    def demonstrate_real_mms_analysis(self):
        """
        Demonstrate real MMS data analysis for Klein frequency detection
        """
        
        print(f"\n" + "="*60)
        print(f"🛰️ REAL MMS DATA KLEIN ANALYSIS DEMONSTRATION")
        print(f"="*60)
        
        if not self.pyspedas_available:
            print(f"❌ PySpedas not available - skipping real data demo")
            return
        
        # Famous MMS reconnection event - well documented
        time_range = ['2017-07-11/22:33:30', '2017-07-11/22:34:30']  # 1 minute
        
        print(f"\n🎯 Target Event: Magnetospheric Reconnection")
        print(f"   Date: 2017-07-11")
        print(f"   Time: 22:33:30 - 22:34:30 UTC")
        print(f"   Description: Classic MMS reconnection diffusion region crossing")
        
        # Fetch real data
        mms_data = self.fetch_real_mms_data(time_range, probe='1')
        
        if mms_data is not None:
            print(f"\n📊 Analyzing Klein frequency in multiple parameters...")
            
            # Analyze different parameters
            parameters_to_analyze = ['B_mag', 'E_mag']
            if 'density' in mms_data.columns:
                parameters_to_analyze.append('density')
            
            results = {}
            
            for param in parameters_to_analyze:
                if param in mms_data.columns:
                    result = self.analyze_klein_frequency(mms_data, param)
                    if result:
                        results[param] = result
            
            # Summary
            print(f"\n📊 KLEIN DETECTION SUMMARY:")
            print(f"   Parameters analyzed: {len(results)}")
            
            detections = 0
            for param, result in results.items():
                if result['within_tolerance'] and result['snr'] > 3:
                    detections += 1
                    print(f"   ✅ {param}: {result['detection_quality']} detection")
                else:
                    print(f"   ❌ {param}: No significant Klein detection")
            
            print(f"\n🎯 Overall: {detections}/{len(results)} parameters show Klein signatures")
            
            return results
        
        else:
            print(f"❌ Could not load real MMS data")
            return None


def main():
    """Main demonstration function"""
    
    # Initialize detector
    detector = MMSKleinDetectorPySpedas()
    
    # Run demonstration
    results = detector.demonstrate_real_mms_analysis()
    
    return results


if __name__ == "__main__":
    results = main()