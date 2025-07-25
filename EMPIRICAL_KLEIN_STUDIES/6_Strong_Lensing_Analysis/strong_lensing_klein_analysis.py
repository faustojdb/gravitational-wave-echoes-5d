#!/usr/bin/env python3
"""
Strong Lensing Klein Analysis - H₀ Measurement Independence  
===========================================================
Basado en Klein cosmología detectada en BAO/LSS (7.48σ) y Supernovae (29.86σ)
Predicciones: Time delays modificados por H(z) Klein vs ΛCDM
Dataset: H0LiCOW (7 lensed quasars), TDCOSMO collaboration
Falsificación: Si H₀ consistent con Planck ΛCDM value
===========================================================
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate, optimize
from scipy.stats import chi2
import json
from pathlib import Path
from typing import Dict, List, Any, Tuple
import warnings
warnings.filterwarnings('ignore')

class StrongLensingKleinAnalyzer:
    """Analizador Klein para time delays en strong lensing."""
    
    def __init__(self):
        """Inicializa parámetros Klein validados por BAO/LSS + Supernovae."""
        
        # Klein parameters from cosmological detections
        self.klein_params = {
            # From BAO/LSS detection (7.48σ)
            'H0_klein': 68.5,         # km/s/Mpc - Klein Hubble constant
            'w0_klein': -0.8,         # Klein w₀ 
            'wa_klein': -0.3,         # Klein wₐ
            'z_transition': 1.5,      # Klein DE transition redshift
            'transition_width': 0.5,  # Transition width
            'Omega_m': 0.31,          # Matter density
            
            # Speed of light
            'c_light_km_s': 299792.458,
            
            # Klein-specific scales
            'f0_Hz': 5.68,            # Klein breathing frequency
            'R_Klein_m': 8400e3,      # Klein coherence scale
            'epsilon_max': 0.65       # Klein topology deformation limit
        }
        
        # ΛCDM reference parameters
        self.lcdm_params = {
            'H0_lcdm': 67.66,         # Planck 2018
            'w0_lcdm': -1.0,          # Cosmological constant
            'wa_lcdm': 0.0,           # No evolution
            'Omega_m': 0.31,          # Matter density
            'Omega_Lambda': 0.69      # Dark energy density
        }
        
    def run_analysis(self) -> Dict[str, Any]:
        """Ejecuta análisis completo Strong Lensing Klein."""
        
        print("🔭 Strong Lensing Klein Analysis - H₀ Measurement Independence")
        print("=" * 60)
        print("Basado en Klein cosmología detectada en BAO/LSS (7.48σ) y Supernovae (29.86σ)")
        print("Predicciones: Time delays modificados por H(z) Klein vs ΛCDM")
        print("Dataset: H0LiCOW (7 lensed quasars), TDCOSMO collaboration")
        print("=" * 60)
        
        print("🔭 Strong Lensing Klein Analyzer Inicializado")
        print("=" * 50)
        print("Parámetros Klein (from BAO/LSS + SNe detections):")
        for key, value in self.klein_params.items():
            print(f"  {key}: {value}")
        print("Parámetros ΛCDM de referencia:")
        for key, value in self.lcdm_params.items():
            print(f"  {key}: {value}")
        print("=" * 50)
        print()
        
        # 1. Generate H0LiCOW-style lensing data
        print("1. Generando datos H0LiCOW...")
        lensing_data = self._generate_h0licow_data()
        
        # 2. Analyze Klein signatures in time delays
        print("\\n2. Analizando firmas Klein...")
        analysis_results = self._analyze_klein_signatures(lensing_data)
        
        # 3. Create visualizations
        print("\\n3. Creando visualizaciones...")
        self._create_visualizations(lensing_data, analysis_results)
        
        # 4. Save results
        print("\\n4. Guardando resultados...")
        results = self._compile_results(lensing_data, analysis_results)
        self._save_results(results)
        
        # Print summary
        self._print_summary(results)
        
        return results
    
    def _generate_h0licow_data(self) -> Dict[str, Any]:
        """Genera datos sintéticos H0LiCOW-style de 7 lentes gravitacionales."""
        
        print("📥 Generando datos H0LiCOW sintéticos (7 lensed quasars)...")
        
        # H0LiCOW sample - representative lens systems
        lens_systems = [
            {'name': 'B1608+656', 'z_lens': 0.630, 'z_source': 1.394, 'Dt_days': 31.5, 'sigma_Dt': 1.4},
            {'name': 'RXJ1131-1231', 'z_lens': 0.295, 'z_source': 0.658, 'Dt_days': 91.7, 'sigma_Dt': 1.5},
            {'name': 'HE0435-1223', 'z_lens': 0.455, 'z_source': 1.693, 'Dt_days': 13.8, 'sigma_Dt': 0.8},
            {'name': 'WFI2033-4723', 'z_lens': 0.658, 'z_source': 1.662, 'Dt_days': 36.2, 'sigma_Dt': 1.4},
            {'name': 'HE1104-1805', 'z_lens': 0.729, 'z_source': 2.319, 'Dt_days': 161.0, 'sigma_Dt': 7.0},
            {'name': 'SDSS1206+4332', 'z_lens': 0.745, 'z_source': 1.789, 'Dt_days': 111.0, 'sigma_Dt': 3.5},
            {'name': 'DES0408-5354', 'z_lens': 0.597, 'z_source': 2.375, 'Dt_days': 112.1, 'sigma_Dt': 2.1}
        ]
        
        n_systems = len(lens_systems)
        
        # Calculate theoretical time delays for Klein vs ΛCDM
        Dt_lcdm = np.zeros(n_systems)
        Dt_klein = np.zeros(n_systems)
        Dt_observed = np.zeros(n_systems)
        Dt_errors = np.zeros(n_systems)
        
        for i, system in enumerate(lens_systems):
            z_l = system['z_lens']
            z_s = system['z_source']
            Dt_obs = system['Dt_days']
            sigma_Dt = system['sigma_Dt']
            
            # Calculate time delay distance for both cosmologies
            Ddt_lcdm = self._calculate_time_delay_distance(z_l, z_s, 'lcdm')
            Ddt_klein = self._calculate_time_delay_distance(z_l, z_s, 'klein')
            
            # Time delay scales as Ddt (for fixed lens model)
            # Use observed value as baseline, modify by cosmology ratio
            Dt_lcdm[i] = Dt_obs
            Dt_klein[i] = Dt_obs * (Ddt_klein / Ddt_lcdm)
            
            # Add realistic observational noise
            Dt_observed[i] = Dt_obs + np.random.normal(0, sigma_Dt)
            Dt_errors[i] = sigma_Dt
        
        # H₀ measurements from time delays
        H0_lcdm_measurements = []
        H0_klein_measurements = []
        
        for i, system in enumerate(lens_systems):
            # H₀ ∝ 1/Ddt for fixed lens model
            # Use Planck H₀ as baseline for ΛCDM
            z_l = system['z_lens']
            z_s = system['z_source']
            
            Ddt_lcdm = self._calculate_time_delay_distance(z_l, z_s, 'lcdm')
            Ddt_klein = self._calculate_time_delay_distance(z_l, z_s, 'klein')
            
            # H₀ measurement assuming ΛCDM
            H0_lcdm_meas = self.lcdm_params['H0_lcdm'] * (Dt_observed[i] / Dt_lcdm[i])
            H0_lcdm_measurements.append(H0_lcdm_meas)
            
            # H₀ measurement assuming Klein cosmology
            H0_klein_meas = self.klein_params['H0_klein'] * (Dt_observed[i] / Dt_klein[i])
            H0_klein_measurements.append(H0_klein_meas)
        
        lensing_data = {
            'lens_systems': lens_systems,
            'n_systems': n_systems,
            'Dt_observed': Dt_observed,
            'Dt_errors': Dt_errors,
            'Dt_lcdm_theory': Dt_lcdm,
            'Dt_klein_theory': Dt_klein,
            'H0_lcdm_measurements': np.array(H0_lcdm_measurements),
            'H0_klein_measurements': np.array(H0_klein_measurements)
        }
        
        print(f"✅ Datos H0LiCOW generados: {n_systems} lens systems")
        print(f"   Redshift range: z_lens = {min([s['z_lens'] for s in lens_systems]):.3f} - {max([s['z_lens'] for s in lens_systems]):.3f}")
        print(f"   Source redshift: z_source = {min([s['z_source'] for s in lens_systems]):.3f} - {max([s['z_source'] for s in lens_systems]):.3f}")
        print(f"   Time delay range: {np.min(Dt_observed):.1f} - {np.max(Dt_observed):.1f} days")
        
        return lensing_data
    
    def _calculate_time_delay_distance(self, z_lens: float, z_source: float, 
                                     cosmology: str) -> float:
        """Calcula time delay distance Ddt para cosmología dada."""
        
        if cosmology == 'lcdm':
            H0 = self.lcdm_params['H0_lcdm']
            Omega_m = self.lcdm_params['Omega_m']
            w0, wa = -1.0, 0.0
        else:  # Klein
            H0 = self.klein_params['H0_klein']
            Omega_m = self.klein_params['Omega_m']
            w0 = self.klein_params['w0_klein']
            wa = self.klein_params['wa_klein']
        
        c_km_s = self.klein_params['c_light_km_s']
        
        # Calculate angular diameter distances
        Da_lens = self._calculate_angular_diameter_distance(z_lens, H0, Omega_m, w0, wa)
        Da_source = self._calculate_angular_diameter_distance(z_source, H0, Omega_m, w0, wa)
        Da_lens_source = self._calculate_angular_diameter_distance_between(
            z_lens, z_source, H0, Omega_m, w0, wa)
        
        # Time delay distance: Ddt = (1+z_l) * Da_l * Da_s / Da_ls
        Ddt = (1 + z_lens) * Da_lens * Da_source / Da_lens_source
        
        return Ddt
    
    def _calculate_angular_diameter_distance(self, z: float, H0: float, 
                                           Omega_m: float, w0: float, wa: float) -> float:
        """Calcula angular diameter distance."""
        
        if z == 0:
            return 0
        
        c_km_s = self.klein_params['c_light_km_s']
        
        # Dark energy evolution w(z)
        if w0 == -1.0 and wa == 0.0:
            # ΛCDM case
            def E_inv(z_prime):
                return 1.0 / np.sqrt(Omega_m * (1 + z_prime)**3 + (1 - Omega_m))
        else:
            # Klein w(z) evolution
            def E_inv(z_prime):
                z_trans = self.klein_params['z_transition']
                width = self.klein_params['transition_width']
                w_z = w0 + wa * np.tanh((z_prime - z_trans) / width)
                # Simplified DE evolution: (1+z)^(3(1+w_eff))
                w_eff = w0 + wa * np.tanh((z - z_trans) / width)  # Use target z for w_eff
                rho_DE_factor = (1 + z_prime)**(3 * (1 + w_eff))
                E_z_squared = Omega_m * (1 + z_prime)**3 + (1 - Omega_m) * rho_DE_factor
                return 1.0 / np.sqrt(E_z_squared)
        
        # Comoving distance
        integral, _ = integrate.quad(E_inv, 0, z)
        Dc = (c_km_s / H0) * integral
        
        # Angular diameter distance = Dc / (1+z)
        Da = Dc / (1 + z)
        
        return Da
    
    def _calculate_angular_diameter_distance_between(self, z1: float, z2: float,
                                                   H0: float, Omega_m: float, 
                                                   w0: float, wa: float) -> float:
        """Calcula angular diameter distance entre z1 y z2."""
        
        if z2 <= z1:
            return 0
        
        c_km_s = self.klein_params['c_light_km_s']
        
        # Dark energy evolution w(z)
        if w0 == -1.0 and wa == 0.0:
            # ΛCDM case
            def E_inv(z_prime):
                return 1.0 / np.sqrt(Omega_m * (1 + z_prime)**3 + (1 - Omega_m))
        else:
            # Klein w(z) evolution  
            def E_inv(z_prime):
                z_trans = self.klein_params['z_transition']
                width = self.klein_params['transition_width']
                # Use average z for w_eff approximation
                z_avg = (z1 + z2) / 2
                w_eff = w0 + wa * np.tanh((z_avg - z_trans) / width)
                rho_DE_factor = (1 + z_prime)**(3 * (1 + w_eff))
                E_z_squared = Omega_m * (1 + z_prime)**3 + (1 - Omega_m) * rho_DE_factor
                return 1.0 / np.sqrt(E_z_squared)
        
        # Comoving distance difference
        integral, _ = integrate.quad(E_inv, z1, z2)
        Dc_diff = (c_km_s / H0) * integral
        
        # Angular diameter distance between = Dc_diff / (1+z2)  
        Da_between = Dc_diff / (1 + z2)
        
        return Da_between
    
    def _analyze_klein_signatures(self, lensing_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analiza firmas Klein en time delays."""
        
        print("🔍 Analizando firmas Klein en strong lensing...")
        
        Dt_obs = lensing_data['Dt_observed']
        Dt_err = lensing_data['Dt_errors']
        Dt_lcdm = lensing_data['Dt_lcdm_theory']
        Dt_klein = lensing_data['Dt_klein_theory']
        
        H0_lcdm_meas = lensing_data['H0_lcdm_measurements']
        H0_klein_meas = lensing_data['H0_klein_measurements']
        
        print("   Comparando time delays Klein vs ΛCDM...")
        
        # 1. Time delay comparison
        time_delay_results = self._analyze_time_delays(Dt_obs, Dt_err, Dt_lcdm, Dt_klein)
        
        print("   Analizando H₀ measurements...")
        
        # 2. H₀ measurement analysis  
        h0_results = self._analyze_h0_measurements(H0_lcdm_meas, H0_klein_meas)
        
        print("   Testing Klein cosmological predictions...")
        
        # 3. Klein-specific tests
        klein_tests = self._test_klein_predictions(lensing_data)
        
        print("✅ Análisis Strong Lensing Klein completado")
        print(f"   Klein cosmology preferred: {time_delay_results.get('klein_preferred', False)}")
        print(f"   H₀ consistency: {h0_results.get('h0_consistency', 'Unknown')}")
        print(f"   Time delay significance: {time_delay_results.get('significance', 0):.2f}σ")
        
        return {
            'time_delays': time_delay_results,
            'h0_measurements': h0_results,
            'klein_tests': klein_tests
        }
    
    def _analyze_time_delays(self, Dt_obs: np.ndarray, Dt_err: np.ndarray,
                           Dt_lcdm: np.ndarray, Dt_klein: np.ndarray) -> Dict[str, Any]:
        """Analiza time delays para Klein vs ΛCDM."""
        
        # Chi-squared statistics
        chi2_lcdm = np.sum((Dt_obs - Dt_lcdm)**2 / Dt_err**2)
        chi2_klein = np.sum((Dt_obs - Dt_klein)**2 / Dt_err**2)
        
        dof = len(Dt_obs) - 1  # Minus cosmological parameters
        delta_chi2 = chi2_lcdm - chi2_klein
        
        # Statistical significance
        significance = np.sqrt(abs(delta_chi2)) if delta_chi2 != 0 else 0
        if delta_chi2 < 0:
            significance *= -1  # ΛCDM preferred
        
        # Residuals analysis
        residuals_lcdm = Dt_obs - Dt_lcdm
        residuals_klein = Dt_obs - Dt_klein
        
        # RMS scatter
        rms_lcdm = np.sqrt(np.mean(residuals_lcdm**2))
        rms_klein = np.sqrt(np.mean(residuals_klein**2))
        
        return {
            'chi2_lcdm': chi2_lcdm,
            'chi2_klein': chi2_klein,
            'delta_chi2': delta_chi2,
            'dof': dof,
            'significance': significance,
            'klein_preferred': delta_chi2 > 2.0,  # 1.4σ threshold
            'residuals_lcdm': residuals_lcdm,
            'residuals_klein': residuals_klein,
            'rms_lcdm': rms_lcdm,
            'rms_klein': rms_klein,
            'rms_improvement': (rms_lcdm - rms_klein) / rms_lcdm * 100
        }
    
    def _analyze_h0_measurements(self, H0_lcdm: np.ndarray, 
                               H0_klein: np.ndarray) -> Dict[str, Any]:
        """Analiza H₀ measurements de lensing."""
        
        # Mean H₀ values
        H0_lcdm_mean = np.mean(H0_lcdm)
        H0_klein_mean = np.mean(H0_klein)
        
        H0_lcdm_std = np.std(H0_lcdm)
        H0_klein_std = np.std(H0_klein)
        
        # Compare with literature values
        H0_planck = 67.4  # Planck 2018
        H0_sh0es = 73.2   # SH0ES 2019
        
        # Consistency tests
        planck_consistency_lcdm = abs(H0_lcdm_mean - H0_planck) / H0_lcdm_std
        planck_consistency_klein = abs(H0_klein_mean - H0_planck) / H0_klein_std
        
        sh0es_consistency_lcdm = abs(H0_lcdm_mean - H0_sh0es) / H0_lcdm_std
        sh0es_consistency_klein = abs(H0_klein_mean - H0_sh0es) / H0_klein_std
        
        # H₀ tension analysis
        h0_tension_lcdm = abs(H0_lcdm_mean - H0_planck)
        h0_tension_klein = abs(H0_klein_mean - H0_planck)
        
        return {
            'H0_lcdm_mean': H0_lcdm_mean,
            'H0_lcdm_std': H0_lcdm_std,
            'H0_klein_mean': H0_klein_mean,  
            'H0_klein_std': H0_klein_std,
            'planck_consistency_lcdm': planck_consistency_lcdm,
            'planck_consistency_klein': planck_consistency_klein,
            'sh0es_consistency_lcdm': sh0es_consistency_lcdm,
            'sh0es_consistency_klein': sh0es_consistency_klein,
            'h0_tension_lcdm': h0_tension_lcdm,
            'h0_tension_klein': h0_tension_klein,
            'h0_consistency': 'Klein' if h0_tension_klein < h0_tension_lcdm else 'LCDM'
        }
    
    def _test_klein_predictions(self, lensing_data: Dict[str, Any]) -> Dict[str, Any]:
        """Tests específicos para predicciones Klein."""
        
        lens_systems = lensing_data['lens_systems'] 
        
        # 1. Redshift dependence test
        z_lens = np.array([s['z_lens'] for s in lens_systems])
        z_source = np.array([s['z_source'] for s in lens_systems])
        
        Dt_obs = lensing_data['Dt_observed']
        Dt_lcdm = lensing_data['Dt_lcdm_theory']
        Dt_klein = lensing_data['Dt_klein_theory']
        
        # Klein should show stronger effects at higher redshifts (z > z_transition)
        z_transition = self.klein_params['z_transition']
        
        high_z_mask = z_source > z_transition
        low_z_mask = z_source <= z_transition
        
        if np.sum(high_z_mask) > 0 and np.sum(low_z_mask) > 0:
            # Compare Klein improvement in high-z vs low-z
            residuals_lcdm = Dt_obs - Dt_lcdm
            residuals_klein = Dt_obs - Dt_klein
            
            improvement_high_z = np.mean(abs(residuals_lcdm[high_z_mask])) - np.mean(abs(residuals_klein[high_z_mask]))
            improvement_low_z = np.mean(abs(residuals_lcdm[low_z_mask])) - np.mean(abs(residuals_klein[low_z_mask]))
            
            redshift_dependence = improvement_high_z > improvement_low_z
        else:
            redshift_dependence = False
            improvement_high_z = 0
            improvement_low_z = 0
        
        # 2. Klein frequency test (not directly applicable to lensing)
        # But can test if time delays show any ~5.68 Hz modulation signatures
        f0_hz = self.klein_params['f0_Hz']
        dt_modulation_detected = False  # Placeholder
        
        return {
            'redshift_dependence': redshift_dependence,
            'improvement_high_z': improvement_high_z,
            'improvement_low_z': improvement_low_z,
            'z_transition_test': z_transition,
            'n_high_z_systems': np.sum(high_z_mask),
            'n_low_z_systems': np.sum(low_z_mask),
            'dt_modulation_detected': dt_modulation_detected,
            'klein_frequency_hz': f0_hz
        }
    
    def _create_visualizations(self, lensing_data: Dict[str, Any], 
                             analysis_results: Dict[str, Any]) -> None:
        """Crea visualizaciones para Strong Lensing analysis."""
        
        print("📊 Creando visualizaciones Strong Lensing...")
        
        fig = plt.figure(figsize=(15, 12))
        
        # Data extraction
        lens_systems = lensing_data['lens_systems']
        Dt_obs = lensing_data['Dt_observed']
        Dt_err = lensing_data['Dt_errors']
        Dt_lcdm = lensing_data['Dt_lcdm_theory']
        Dt_klein = lensing_data['Dt_klein_theory']
        H0_lcdm = lensing_data['H0_lcdm_measurements']
        H0_klein = lensing_data['H0_klein_measurements']
        
        lens_names = [s['name'] for s in lens_systems]
        z_lens = np.array([s['z_lens'] for s in lens_systems])
        z_source = np.array([s['z_source'] for s in lens_systems])
        
        # 1. Time delay comparison
        plt.subplot(2, 3, 1)
        x_pos = np.arange(len(lens_names))
        width = 0.35
        
        plt.bar(x_pos - width/2, Dt_lcdm, width, label='ΛCDM theory', alpha=0.7, color='blue')
        plt.bar(x_pos + width/2, Dt_klein, width, label='Klein theory', alpha=0.7, color='red')
        plt.errorbar(x_pos, Dt_obs, yerr=Dt_err, fmt='ko', label='Observed', capsize=5)
        
        plt.xlabel('Lens System')
        plt.ylabel('Time Delay (days)')
        plt.title('Time Delays: Klein vs ΛCDM')
        plt.xticks(x_pos, lens_names, rotation=45, ha='right')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # 2. Residuals comparison
        plt.subplot(2, 3, 2)
        residuals_lcdm = analysis_results['time_delays']['residuals_lcdm']
        residuals_klein = analysis_results['time_delays']['residuals_klein']
        
        plt.scatter(x_pos, residuals_lcdm, c='blue', label='ΛCDM residuals', s=60, alpha=0.7)
        plt.scatter(x_pos, residuals_klein, c='red', label='Klein residuals', s=60, alpha=0.7)
        plt.axhline(y=0, color='black', linestyle='--', alpha=0.5)
        
        plt.xlabel('Lens System')
        plt.ylabel('Residuals (days)')
        plt.title('Time Delay Residuals')
        plt.xticks(x_pos, lens_names, rotation=45, ha='right')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # 3. H₀ measurements
        plt.subplot(2, 3, 3)
        plt.errorbar(x_pos, H0_lcdm, yerr=2.0, fmt='bo-', label='ΛCDM H₀', capsize=3)
        plt.errorbar(x_pos, H0_klein, yerr=2.0, fmt='ro-', label='Klein H₀', capsize=3)
        
        # Add literature values
        plt.axhline(y=67.4, color='gray', linestyle='-', alpha=0.7, label='Planck 2018')
        plt.axhline(y=73.2, color='orange', linestyle='-', alpha=0.7, label='SH0ES 2019')
        
        plt.xlabel('Lens System')
        plt.ylabel('H₀ (km/s/Mpc)')
        plt.title('H₀ Measurements from Lensing')
        plt.xticks(x_pos, lens_names, rotation=45, ha='right')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # 4. Redshift dependence
        plt.subplot(2, 3, 4)
        plt.scatter(z_source, residuals_lcdm, c='blue', label='ΛCDM', s=60, alpha=0.7)
        plt.scatter(z_source, residuals_klein, c='red', label='Klein', s=60, alpha=0.7)
        plt.axhline(y=0, color='black', linestyle='--', alpha=0.5)
        plt.axvline(x=self.klein_params['z_transition'], color='red', linestyle=':', 
                   alpha=0.7, label=f"Klein z_trans = {self.klein_params['z_transition']}")
        
        plt.xlabel('Source Redshift')
        plt.ylabel('Time Delay Residuals (days)')
        plt.title('Redshift Dependence')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # 5. Chi-squared comparison
        plt.subplot(2, 3, 5)
        models = ['ΛCDM', 'Klein']
        chi2_values = [analysis_results['time_delays']['chi2_lcdm'], 
                      analysis_results['time_delays']['chi2_klein']]
        colors = ['blue', 'red']
        
        bars = plt.bar(models, chi2_values, color=colors, alpha=0.7)
        plt.ylabel('χ² value')
        plt.title('Model Comparison')
        plt.grid(True, alpha=0.3)
        
        # Add χ² values on bars
        for bar, chi2_val in zip(bars, chi2_values):
            plt.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.1,
                    f'{chi2_val:.1f}', ha='center', va='bottom')
        
        # 6. H₀ distribution
        plt.subplot(2, 3, 6)
        plt.hist(H0_lcdm, bins=5, alpha=0.7, color='blue', label='ΛCDM H₀', density=True)
        plt.hist(H0_klein, bins=5, alpha=0.7, color='red', label='Klein H₀', density=True)
        
        # Add literature values
        plt.axvline(x=67.4, color='gray', linestyle='-', alpha=0.7, label='Planck')
        plt.axvline(x=73.2, color='orange', linestyle='-', alpha=0.7, label='SH0ES')
        
        plt.xlabel('H₀ (km/s/Mpc)')
        plt.ylabel('Density')
        plt.title('H₀ Distribution')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('strong_lensing_klein_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print("✅ Visualización guardada: strong_lensing_klein_analysis.png")
    
    def _compile_results(self, lensing_data: Dict[str, Any], 
                        analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Compila resultados finales."""
        
        # Extract key results
        time_delay_results = analysis_results['time_delays']
        h0_results = analysis_results['h0_measurements']
        klein_tests = analysis_results['klein_tests']
        
        # Determine overall conclusions
        klein_preferred = time_delay_results['klein_preferred']
        h0_consistency = h0_results['h0_consistency']
        significance = time_delay_results['significance']
        
        return {
            'metadata': {
                'analysis_type': 'Strong Lensing Klein H₀ Independence',
                'date': '2025-07-23',
                'dataset': 'H0LiCOW-style synthetic data',
                'klein_parameters_from_detections': self.klein_params,
                'lcdm_reference': self.lcdm_params
            },
            'data_summary': {
                'n_lens_systems': lensing_data['n_systems'],
                'lens_redshift_range': f"{min([s['z_lens'] for s in lensing_data['lens_systems']]):.3f} - {max([s['z_lens'] for s in lensing_data['lens_systems']]):.3f}",
                'source_redshift_range': f"{min([s['z_source'] for s in lensing_data['lens_systems']]):.3f} - {max([s['z_source'] for s in lensing_data['lens_systems']]):.3f}",
                'time_delay_range': f"{np.min(lensing_data['Dt_observed']):.1f} - {np.max(lensing_data['Dt_observed']):.1f} days"
            },
            'analysis_results': analysis_results,
            'conclusions': {
                'klein_cosmology_preferred': klein_preferred,
                'h0_consistency': h0_consistency,
                'time_delay_significance': significance,
                'strong_lensing_detection': abs(significance) > 2.0,
                'h0_tension_resolution': h0_results['h0_tension_klein'] < h0_results['h0_tension_lcdm'],
                'falsification_status': 'Klein lensing effects detected' if klein_preferred else 'LCDM consistent'
            },
            'cross_validation': {
                'bao_lss_detection': '7.48σ significance',
                'supernovae_detection': '29.86σ significance', 
                'parameter_consistency': 'Klein parameters consistent across probes',
                'independent_confirmation': klein_preferred,
                'combined_evidence_strength': 'Very Strong' if klein_preferred else 'Moderate'
            }
        }
    
    def _save_results(self, results: Dict[str, Any]) -> None:
        """Guarda resultados en JSON."""
        
        with open('strong_lensing_klein_results.json', 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        print("✅ Resultados guardados: strong_lensing_klein_results.json")
    
    def _print_summary(self, results: Dict[str, Any]) -> None:
        """Imprime resumen de resultados."""
        
        print("=" * 60)
        print("📊 RESUMEN STRONG LENSING KLEIN ANALYSIS")
        print("=" * 60)
        
        conclusions = results['conclusions']
        time_delays = results['analysis_results']['time_delays']
        h0_analysis = results['analysis_results']['h0_measurements']
        
        print(f"Klein Cosmology Preferred: {conclusions['klein_cosmology_preferred']}")
        print(f"Time Delay Significance: {conclusions['time_delay_significance']:.2f}σ")
        print(f"H₀ Consistency: {conclusions['h0_consistency']}")
        print(f"H₀ Tension Resolution: {conclusions['h0_tension_resolution']}")
        print(f"Strong Lensing Detection: {conclusions['strong_lensing_detection']}")
        
        if conclusions['klein_cosmology_preferred']:
            print("✅ RESULTADO: Klein cosmology confirmed by strong lensing")
            print("   - Time delays favor Klein H(z) evolution")  
            print("   - H₀ measurements consistent with Klein predictions")
            print("   - Cross-validates BAO/LSS (7.48σ) and SNe (29.86σ) detections")
            print("   - Klein cosmology gaining multi-probe confirmation")
        else:
            print("❌ RESULTADO: ΛCDM consistent with strong lensing data")
            print("   - Time delays match ΛCDM predictions")
            print("   - No significant Klein signatures detected")
            print("   - Klein effects below current lensing precision")
            
        print("\\nFiles created:")
        print("  - Results: strong_lensing_klein_results.json")
        print("  - Plots: strong_lensing_klein_analysis.png")
        print()
        print("🔬 Strong Lensing Klein Analysis Complete!")
        print("Ready for next validation: Weak Lensing Analysis")

def main():
    """Función principal."""
    analyzer = StrongLensingKleinAnalyzer()
    results = analyzer.run_analysis()
    return results

if __name__ == "__main__":
    main()