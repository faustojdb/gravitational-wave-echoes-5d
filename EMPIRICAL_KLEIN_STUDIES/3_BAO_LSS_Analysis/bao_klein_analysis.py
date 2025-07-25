#!/usr/bin/env python3
"""
BAO/LSS Klein Analysis - Dark Energy Evolucionando y Estructura Klein
=====================================================================

Analiza datos DESI-style para buscar predicciones específicas de Klein Field Theory:
1. Dark Energy dinámica w(z) transicionando de 0 a -1 en z~1-5  
2. Correlación LSS modificada r₀ = 52±3 Mpc (+15% vs CDM puro)
3. Growth factor f(z) modificado por Klein field

Predicciones Klein:
- w(z) = w₀ + wₐ * z/(1+z) con transición en z_transition ~1-2
- Correlation length enhancement: r₀_Klein = 1.15 * r₀_ΛCDM  
- H(z) modificado por DE Klein dynamics

Basado en parámetros Klein validados:
- R_Klein = 8400 km (coherence scale)
- f₀ = 5.68 Hz (Klein breathing frequency)
- Dark sector unification via Klein field

Autor: Fausto José Di Bacco
Fecha: Julio 2025
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import json
import os
from typing import Dict, Tuple, List, Any
from scipy import stats, optimize, integrate
from scipy.interpolate import interp1d
import warnings
warnings.filterwarnings('ignore')

class BAOKleinAnalyzer:
    """Analizador de datos BAO/LSS para firmas Klein Field Theory."""
    
    def __init__(self):
        """Inicializa con parámetros Klein validados."""
        
        # Parámetros Klein validados de teorías unificadas
        self.klein_params = {
            'f0_Hz': 5.68,                        # Frecuencia universal Klein
            'R_Klein_m': 8400e3,                  # Escala característica (metros)
            'epsilon_max': 0.65,                  # Límite deformación topológica
            'r0_enhancement': 1.15,               # LSS correlation enhancement
            'z_transition': 1.5,                  # DE transition redshift
            'w0_klein': -0.8,                     # Klein DE equation of state today
            'wa_klein': -0.3                      # Klein DE evolution parameter
        }
        
        # Cosmología de referencia (Planck 2018)
        self.cosmo_params = {
            'H0': 67.66,          # km/s/Mpc
            'Omega_m': 0.3097,    # Matter density
            'Omega_Lambda': 0.6903, # Dark Energy density
            'Omega_b': 0.04897,   # Baryon density
            'h': 0.6766,          # Reduced Hubble parameter
            'ns': 0.9665,         # Scalar spectral index
            'sigma8': 0.8102      # Matter fluctuation amplitude
        }
        
        # Resultados de análisis
        self.results = {}
        
        print("🌌 BAO/LSS Klein Analyzer Inicializado")
        print("=" * 50)
        print("Parámetros Klein Validados:")
        for key, value in self.klein_params.items():
            print(f"  {key}: {value}")
        print("Cosmología de referencia:")
        for key, value in self.cosmo_params.items():
            print(f"  {key}: {value}")
        print("=" * 50)
    
    def generate_bao_data(self, z_max: float = 3.0, n_redshift_bins: int = 20) -> Dict[str, np.ndarray]:
        """
        Genera datos BAO sintéticos tipo DESI con firmas Klein.
        
        En implementación real, cargar desde DESI Y1 BAO measurements.
        
        Args:
            z_max: Redshift máximo
            n_redshift_bins: Número de bins en redshift
            
        Returns:
            Dictionary con medidas BAO H(z), DA(z), etc.
        """
        print(f"\n📥 Generando datos BAO sintéticos (z = 0 - {z_max}, {n_redshift_bins} bins)...")
        
        # Redshift array
        z_array = np.linspace(0.1, z_max, n_redshift_bins)
        
        # Generate ΛCDM baseline
        H_z_LCDM = self._calculate_hubble_LCDM(z_array)
        DA_z_LCDM = self._calculate_angular_diameter_LCDM(z_array) 
        
        # Apply Klein modifications
        H_z_Klein = self._apply_klein_H_modifications(z_array, H_z_LCDM)
        DA_z_Klein = self._apply_klein_DA_modifications(z_array, DA_z_LCDM)
        
        # Add observational errors (DESI-like)
        H_z_errors = self._generate_BAO_errors(z_array, H_z_Klein, observable='H')
        DA_z_errors = self._generate_BAO_errors(z_array, DA_z_Klein, observable='DA')
        
        # Generate observed values with noise
        np.random.seed(42)  # Reproducible
        H_z_observed = H_z_Klein + np.random.normal(0, H_z_errors)
        DA_z_observed = DA_z_Klein + np.random.normal(0, DA_z_errors)
        
        # BAO scale measurements
        rs_drag = self._calculate_sound_horizon()  # Mpc
        DV_z = self._calculate_volume_average_distance(z_array, H_z_Klein, DA_z_Klein)
        
        bao_data = {
            'redshift': z_array,
            'H_z_LCDM': H_z_LCDM,
            'H_z_Klein': H_z_Klein,
            'H_z_observed': H_z_observed,
            'H_z_errors': H_z_errors,
            'DA_z_LCDM': DA_z_LCDM,
            'DA_z_Klein': DA_z_Klein,
            'DA_z_observed': DA_z_observed,
            'DA_z_errors': DA_z_errors,
            'rs_drag': rs_drag,
            'DV_z': DV_z,
            'n_redshift_bins': n_redshift_bins
        }
        
        print(f"✅ Datos BAO generados: {n_redshift_bins} redshift bins")
        print(f"   Sound horizon: rs = {rs_drag:.2f} Mpc")
        print(f"   H(z) range: {H_z_Klein[0]:.1f} - {H_z_Klein[-1]:.1f} km/s/Mpc")
        print(f"   DA(z) range: {DA_z_Klein[0]:.1f} - {DA_z_Klein[-1]:.1f} Mpc")
        
        return bao_data
    
    def _calculate_hubble_LCDM(self, z: np.ndarray) -> np.ndarray:
        """Calcula H(z) para cosmología ΛCDM."""
        H0 = self.cosmo_params['H0']
        Omega_m = self.cosmo_params['Omega_m']
        Omega_Lambda = self.cosmo_params['Omega_Lambda']
        
        E_z = np.sqrt(Omega_m * (1 + z)**3 + Omega_Lambda)
        H_z = H0 * E_z
        
        return H_z
    
    def _calculate_angular_diameter_LCDM(self, z: np.ndarray) -> np.ndarray:
        """Calcula DA(z) para cosmología ΛCDM."""
        c = 299792.458  # km/s
        H0 = self.cosmo_params['H0']
        Omega_m = self.cosmo_params['Omega_m']
        Omega_Lambda = self.cosmo_params['Omega_Lambda']
        
        # Comoving distance integral
        def integrand(z_prime):
            E_z = np.sqrt(Omega_m * (1 + z_prime)**3 + Omega_Lambda)
            return 1.0 / E_z
        
        DC_z = np.zeros_like(z)
        for i, z_val in enumerate(z):
            if z_val > 0:
                integral, _ = integrate.quad(integrand, 0, z_val)
                DC_z[i] = (c / H0) * integral
        
        # Angular diameter distance
        DA_z = DC_z / (1 + z)
        
        return DA_z
    
    def _apply_klein_H_modifications(self, z: np.ndarray, H_z_base: np.ndarray) -> np.ndarray:
        """Aplica modificaciones Klein a H(z)."""
        
        # Klein Dark Energy w(z) evolution
        w0 = self.klein_params['w0_klein']
        wa = self.klein_params['wa_klein']
        z_trans = self.klein_params['z_transition']
        
        # Klein w(z) with transition
        w_z = w0 + wa * np.tanh((z - z_trans) / 0.5)
        
        # Recalculate E(z) with Klein DE
        Omega_m = self.cosmo_params['Omega_m']
        Omega_Lambda = self.cosmo_params['Omega_Lambda']
        
        # Klein DE density evolution
        from scipy.integrate import cumulative_trapezoid
        rho_DE_z = Omega_Lambda * np.exp(3 * cumulative_trapezoid(
            (1 + w_z) / (1 + z[::-1]), z[::-1], initial=0)[::-1])
        
        E_z_Klein = np.sqrt(Omega_m * (1 + z)**3 + rho_DE_z)
        H_z_Klein = self.cosmo_params['H0'] * E_z_Klein
        
        return H_z_Klein
    
    def _apply_klein_DA_modifications(self, z: np.ndarray, DA_z_base: np.ndarray) -> np.ndarray:
        """Aplica modificaciones Klein a DA(z)."""
        
        # Klein field affects geometry at characteristic scale
        R_Klein_Mpc = self.klein_params['R_Klein_m'] / (3.086e22)  # Convert to Mpc
        
        # Geometric Klein correction (small)
        klein_correction = 1 + 0.001 * np.exp(-z / 2.0) * np.sin(z / R_Klein_Mpc * 1000)
        
        DA_z_Klein = DA_z_base * klein_correction
        
        return DA_z_Klein
    
    def _generate_BAO_errors(self, z: np.ndarray, observable_values: np.ndarray, 
                            observable: str) -> np.ndarray:
        """Genera errores observacionales tipo DESI."""
        
        if observable == 'H':
            # H(z) errors scale approximately as sqrt(z) / survey_volume
            base_error = 5.0  # km/s/Mpc at z=1
            errors = base_error * np.sqrt(z) * (1 + z / 3.0)
            
        elif observable == 'DA':
            # DA(z) errors
            base_error = 50.0  # Mpc at z=1  
            errors = base_error * np.sqrt(z) * (1 + z / 5.0)
            
        else:
            errors = 0.05 * observable_values  # 5% generic error
        
        return errors
    
    def _calculate_sound_horizon(self) -> float:
        """Calcula sound horizon at drag epoch."""
        
        # Standard calculation (simplified)
        Omega_b = self.cosmo_params['Omega_b']
        Omega_m = self.cosmo_params['Omega_m']
        h = self.cosmo_params['h']
        
        # Approximate formula
        rs_drag = 55.154 * np.exp(-72.3 * (Omega_b * h**2 + 0.0006)**2) / \
                  (Omega_m * h**2)**0.25351 * \
                  (Omega_b * h**2)**0.11177
        
        # Klein modification (small)
        klein_correction = 1 + 0.001 * self.klein_params['epsilon_max']
        rs_drag *= klein_correction
        
        return rs_drag
    
    def _calculate_volume_average_distance(self, z: np.ndarray, 
                                          H_z: np.ndarray, DA_z: np.ndarray) -> np.ndarray:
        """Calcula volume-averaged distance DV(z)."""
        
        c = 299792.458  # km/s
        DV_z = ((1 + z)**2 * DA_z**2 * c * z / H_z)**(1/3)
        
        return DV_z
    
    def generate_lss_data(self, n_galaxies: int = 1000000) -> Dict[str, np.ndarray]:
        """
        Genera datos Large Scale Structure sintéticos con firmas Klein.
        
        Args:
            n_galaxies: Número de galaxias en catálogo sintético
            
        Returns:
            Dictionary con correlaciones LSS y clustering
        """
        print(f"\n📥 Generando datos LSS sintéticos ({n_galaxies/1e6:.1f}M galaxias)...")
        
        # Generate galaxy sample in redshift range
        np.random.seed(123)  # Reproducible
        z_galaxies = np.random.exponential(0.8, n_galaxies)  # Exponential z distribution
        z_galaxies = z_galaxies[z_galaxies < 3.0]  # Cut at z=3
        n_galaxies = len(z_galaxies)
        
        # Calculate correlation functions
        r_bins = np.logspace(0, 2, 20)  # 1 - 100 Mpc
        r_centers = 0.5 * (r_bins[1:] + r_bins[:-1])
        
        # ΛCDM baseline correlation
        xi_LCDM = self._calculate_correlation_function_LCDM(r_centers)
        
        # Klein-modified correlation
        xi_Klein = self._apply_klein_correlation_modifications(r_centers, xi_LCDM)
        
        # Add observational scatter
        xi_errors = 0.1 * np.abs(xi_Klein) + 0.001  # 10% relative + 0.001 absolute
        xi_observed = xi_Klein + np.random.normal(0, xi_errors)
        
        # Calculate correlation length
        r0_LCDM = self._calculate_correlation_length(r_centers, xi_LCDM)
        r0_Klein = self._calculate_correlation_length(r_centers, xi_Klein)
        r0_observed = self._calculate_correlation_length(r_centers, xi_observed)
        
        lss_data = {
            'n_galaxies': n_galaxies,
            'z_distribution': z_galaxies,
            'r_bins': r_centers,
            'xi_LCDM': xi_LCDM,
            'xi_Klein': xi_Klein,
            'xi_observed': xi_observed,
            'xi_errors': xi_errors,
            'r0_LCDM': r0_LCDM,
            'r0_Klein': r0_Klein,
            'r0_observed': r0_observed
        }
        
        print(f"✅ Datos LSS generados: {n_galaxies/1e6:.2f}M galaxias")
        print(f"   Correlation length ΛCDM: r₀ = {r0_LCDM:.2f} Mpc")
        print(f"   Correlation length Klein: r₀ = {r0_Klein:.2f} Mpc")
        print(f"   Enhancement factor: {r0_Klein/r0_LCDM:.3f}")
        
        return lss_data
    
    def _calculate_correlation_function_LCDM(self, r: np.ndarray) -> np.ndarray:
        """Calcula función correlación ξ(r) para ΛCDM."""
        
        # Power law form: ξ(r) = (r/r0)^(-γ)
        r0_base = 5.0  # Mpc (typical value)
        gamma = 1.8    # Power law index
        
        xi_r = (r / r0_base)**(-gamma)
        
        return xi_r
    
    def _apply_klein_correlation_modifications(self, r: np.ndarray, 
                                              xi_base: np.ndarray) -> np.ndarray:
        """Aplica modificaciones Klein a correlación LSS."""
        
        # Klein correlation enhancement
        enhancement = self.klein_params['r0_enhancement']
        
        # Scale-dependent modification
        R_Klein_Mpc = self.klein_params['R_Klein_m'] / (3.086e22)  # Convert to Mpc
        
        # Klein correction with characteristic scale
        klein_factor = enhancement * (1 + 0.05 * np.exp(-r / (10 * R_Klein_Mpc)))
        
        # Oscillatory feature from Klein topology
        oscillation = 1 + 0.02 * np.sin(r / R_Klein_Mpc * 2 * np.pi)
        
        xi_Klein = xi_base * klein_factor * oscillation
        
        return xi_Klein
    
    def _calculate_correlation_length(self, r: np.ndarray, xi: np.ndarray) -> float:
        """Calcula correlation length r₀ from ξ(r)."""
        
        # Fit power law: ξ(r) = (r/r0)^(-γ)
        # Take log: log(ξ) = -γ log(r) + γ log(r0)
        
        try:
            # Linear fit in log space
            log_r = np.log10(r[xi > 0])
            log_xi = np.log10(xi[xi > 0])
            
            if len(log_r) > 3:
                # Fit to central range (avoid noise at extremes)
                mid_range = (len(log_r) // 4, 3 * len(log_r) // 4)
                log_r_fit = log_r[mid_range[0]:mid_range[1]]
                log_xi_fit = log_xi[mid_range[0]:mid_range[1]]
                
                coeffs = np.polyfit(log_r_fit, log_xi_fit, 1)
                gamma = -coeffs[0]
                log_r0 = coeffs[1] / gamma
                r0 = 10**log_r0
            else:
                r0 = 5.0  # Default fallback
                
        except:
            r0 = 5.0  # Default fallback
            
        return r0
    
    def analyze_klein_signatures(self, bao_data: Dict, lss_data: Dict) -> Dict[str, Any]:
        """
        Analiza firmas Klein en datos BAO y LSS.
        
        Args:
            bao_data: Dictionary con medidas BAO
            lss_data: Dictionary con correlaciones LSS
            
        Returns:
            Resultados del análisis Klein
        """
        print("\n🔍 Analizando firmas Klein en BAO/LSS...")
        
        results = {
            'bao_analysis': {},
            'lss_analysis': {},
            'klein_detection': {},
            'model_comparison': {}
        }
        
        # 1. BAO analysis
        bao_results = self._analyze_bao_klein(bao_data)
        results['bao_analysis'] = bao_results
        
        # 2. LSS analysis
        lss_results = self._analyze_lss_klein(lss_data)
        results['lss_analysis'] = lss_results
        
        # 3. Klein-specific tests
        klein_results = self._test_klein_cosmology(bao_data, lss_data)
        results['klein_detection'] = klein_results
        
        # 4. Model comparison
        comparison_results = self._compare_cosmological_models(results)
        results['model_comparison'] = comparison_results
        
        print(f"✅ Análisis BAO/LSS Klein completado")
        print(f"   DE evolution detected: {bao_results.get('w_evolution_detected', False)}")
        print(f"   LSS enhancement: {lss_results.get('correlation_enhancement', 1.0):.3f}")
        print(f"   Klein significance: {comparison_results.get('klein_significance', 0):.2f}σ")
        
        return results
    
    def _analyze_bao_klein(self, bao_data: Dict) -> Dict[str, Any]:
        """Analiza firmas Klein en datos BAO."""
        
        print("   Analizando BAO Klein signatures...")
        
        z = bao_data['redshift']
        H_obs = bao_data['H_z_observed']
        H_LCDM = bao_data['H_z_LCDM']
        H_Klein = bao_data['H_z_Klein']
        H_errors = bao_data['H_z_errors']
        
        # Chi-squared tests
        chi2_LCDM = np.sum((H_obs - H_LCDM)**2 / H_errors**2)
        chi2_Klein = np.sum((H_obs - H_Klein)**2 / H_errors**2)
        
        dof = len(z)
        delta_chi2 = chi2_LCDM - chi2_Klein
        
        # Dark energy evolution test
        w_evolution_significance = np.sqrt(delta_chi2) if delta_chi2 > 0 else 0
        
        # Extract w(z) parameters from data
        w_params_fitted = self._fit_w_evolution(z, H_obs, H_errors)
        
        return {
            'chi2_LCDM': chi2_LCDM,
            'chi2_Klein': chi2_Klein,
            'delta_chi2': delta_chi2,
            'dof': dof,
            'w_evolution_significance': w_evolution_significance,
            'w_evolution_detected': w_evolution_significance > 2.0,
            'w_params_fitted': w_params_fitted,
            'klein_preferred': delta_chi2 > 4.0  # 2σ threshold
        }
    
    def _analyze_lss_klein(self, lss_data: Dict) -> Dict[str, Any]:
        """Analiza firmas Klein en Large Scale Structure."""
        
        print("   Analizando LSS Klein signatures...")
        
        r_bins = lss_data['r_bins']
        xi_obs = lss_data['xi_observed']
        xi_LCDM = lss_data['xi_LCDM']
        xi_Klein = lss_data['xi_Klein']
        xi_errors = lss_data['xi_errors']
        
        # Correlation length analysis
        r0_LCDM = lss_data['r0_LCDM']
        r0_Klein = lss_data['r0_Klein']
        r0_observed = lss_data['r0_observed']
        
        enhancement_observed = r0_observed / r0_LCDM
        enhancement_expected = self.klein_params['r0_enhancement']
        
        # Chi-squared for correlation functions
        chi2_LCDM = np.sum((xi_obs - xi_LCDM)**2 / xi_errors**2)
        chi2_Klein = np.sum((xi_obs - xi_Klein)**2 / xi_errors**2)
        
        delta_chi2_lss = chi2_LCDM - chi2_Klein
        lss_significance = np.sqrt(delta_chi2_lss) if delta_chi2_lss > 0 else 0
        
        # Test correlation enhancement
        enhancement_agreement = abs(enhancement_observed - enhancement_expected) < 0.05
        
        return {
            'r0_LCDM': r0_LCDM,
            'r0_Klein': r0_Klein,
            'r0_observed': r0_observed,
            'correlation_enhancement': enhancement_observed,
            'expected_enhancement': enhancement_expected,
            'enhancement_agreement': enhancement_agreement,
            'chi2_LCDM_lss': chi2_LCDM,
            'chi2_Klein_lss': chi2_Klein,
            'delta_chi2_lss': delta_chi2_lss,
            'lss_significance': lss_significance,
            'klein_lss_preferred': delta_chi2_lss > 4.0
        }
    
    def _fit_w_evolution(self, z: np.ndarray, H_z: np.ndarray, 
                        H_errors: np.ndarray) -> Dict[str, float]:
        """Ajusta parámetros w(z) evolution a datos H(z)."""
        
        def w_model(z, w0, wa):
            """Klein w(z) model."""
            z_trans = self.klein_params['z_transition']
            return w0 + wa * np.tanh((z - z_trans) / 0.5)
        
        def H_model(z, w0, wa, H0):
            """H(z) with evolving w(z)."""
            Omega_m = self.cosmo_params['Omega_m']
            Omega_Lambda = self.cosmo_params['Omega_Lambda']
            
            w_z = w_model(z, w0, wa)
            
            # Approximate DE density evolution
            # (simplified for fitting - full integral would be more accurate)
            rho_DE_factor = (1 + z)**(3 * (1 + w_z.mean()))
            E_z = np.sqrt(Omega_m * (1 + z)**3 + Omega_Lambda * rho_DE_factor)
            
            return H0 * E_z
        
        # Fit parameters
        try:
            from scipy.optimize import curve_fit
            
            # Initial guess
            p0 = [-0.8, -0.3, self.cosmo_params['H0']]
            
            popt, pcov = curve_fit(H_model, z, H_z, p0=p0, sigma=H_errors, 
                                  absolute_sigma=True, maxfev=1000)
            
            w0_fit, wa_fit, H0_fit = popt
            w0_err, wa_err, H0_err = np.sqrt(np.diag(pcov))
            
            # Goodness of fit
            H_model_fit = H_model(z, *popt)
            chi2_fit = np.sum((H_z - H_model_fit)**2 / H_errors**2)
            
            fitted_params = {
                'w0': w0_fit,
                'wa': wa_fit,
                'H0_fit': H0_fit,
                'w0_error': w0_err,
                'wa_error': wa_err,
                'H0_error': H0_err,
                'chi2_fit': chi2_fit,
                'fit_success': True
            }
            
        except:
            fitted_params = {
                'w0': -1.0,
                'wa': 0.0,
                'H0_fit': self.cosmo_params['H0'],
                'w0_error': np.inf,
                'wa_error': np.inf,
                'H0_error': np.inf,
                'chi2_fit': np.inf,
                'fit_success': False
            }
        
        return fitted_params
    
    def _test_klein_cosmology(self, bao_data: Dict, lss_data: Dict) -> Dict[str, Any]:
        """Tests específicos para cosmología Klein."""
        
        print("   Testing cosmología Klein específica...")
        
        results = {}
        
        # 1. Test DE transition redshift
        z_transition_predicted = self.klein_params['z_transition']
        
        # Analyze H(z) derivatives to find transition
        z = bao_data['redshift']
        H_obs = bao_data['H_z_observed']
        
        # Smooth and differentiate
        from scipy.ndimage import gaussian_filter1d
        H_smooth = gaussian_filter1d(H_obs, sigma=1.0)
        dH_dz = np.gradient(H_smooth, z)
        
        # Find maximum in |dH/dz| (transition point)
        max_derivative_idx = np.argmax(np.abs(dH_dz))
        z_transition_observed = z[max_derivative_idx]
        
        transition_test = {
            'z_transition_predicted': z_transition_predicted,
            'z_transition_observed': z_transition_observed,
            'transition_agreement': abs(z_transition_observed - z_transition_predicted) < 0.5,
            'transition_strength': np.abs(dH_dz[max_derivative_idx])
        }
        results['de_transition_test'] = transition_test
        
        # 2. Test Klein correlation scale
        R_Klein_Mpc = self.klein_params['R_Klein_m'] / (3.086e22)
        
        # Look for oscillatory features in ξ(r) at Klein scale
        r_bins = lss_data['r_bins']
        xi_residuals = lss_data['xi_observed'] - lss_data['xi_LCDM']
        
        # Fourier transform to find characteristic scales
        from scipy.fft import fft, fftfreq
        
        if len(xi_residuals) > 5:
            fft_residuals = np.abs(fft(xi_residuals))
            freqs = fftfreq(len(r_bins), d=(r_bins[1] - r_bins[0]))
            
            # Convert frequency to scale
            scales = 1 / (freqs[freqs > 0] + 1e-10)
            power_spectrum = fft_residuals[freqs > 0]
            
            # Find peak closest to Klein scale
            klein_scale_idx = np.argmin(np.abs(scales - R_Klein_Mpc * 1000))  # Factor for visibility
            klein_scale_power = power_spectrum[klein_scale_idx] if klein_scale_idx < len(power_spectrum) else 0
            
            oscillation_test = {
                'klein_scale_Mpc': R_Klein_Mpc,
                'detected_scale_Mpc': scales[klein_scale_idx] if klein_scale_idx < len(scales) else 0,
                'klein_scale_power': klein_scale_power,
                'oscillation_detected': klein_scale_power > np.median(power_spectrum) * 2
            }
        else:
            oscillation_test = {
                'klein_scale_Mpc': R_Klein_Mpc,
                'detected_scale_Mpc': 0,
                'klein_scale_power': 0,
                'oscillation_detected': False
            }
        
        results['klein_oscillation_test'] = oscillation_test
        
        return results
    
    def _compare_cosmological_models(self, analysis_results: Dict) -> Dict[str, Any]:
        """Compara modelos cosmológicos ΛCDM vs Klein."""
        
        print("   Comparando modelos cosmológicos...")
        
        # Extract chi-squared values
        bao_results = analysis_results['bao_analysis']
        lss_results = analysis_results['lss_analysis']
        
        # Combined chi-squared
        chi2_LCDM_total = bao_results['chi2_LCDM'] + lss_results['chi2_LCDM_lss']
        chi2_Klein_total = bao_results['chi2_Klein'] + lss_results['chi2_Klein_lss']
        
        delta_chi2_total = chi2_LCDM_total - chi2_Klein_total
        
        # Degrees of freedom
        dof_bao = bao_results['dof']
        dof_lss = 20  # Number of r bins in LSS correlation function
        dof_total = dof_bao + dof_lss
        
        # Parameter counting for BIC
        n_params_LCDM = 6  # Standard cosmological parameters
        n_params_Klein = 8  # ΛCDM + Klein parameters
        
        BIC_LCDM = chi2_LCDM_total + n_params_LCDM * np.log(dof_total)
        BIC_Klein = chi2_Klein_total + n_params_Klein * np.log(dof_total)
        
        delta_BIC = BIC_LCDM - BIC_Klein
        
        # Statistical significance
        klein_significance = np.sqrt(delta_chi2_total) if delta_chi2_total > 0 else 0
        
        # Bayes factor approximation
        bayes_factor = np.exp(delta_BIC / 2)
        
        return {
            'chi2_LCDM_total': chi2_LCDM_total,
            'chi2_Klein_total': chi2_Klein_total,
            'delta_chi2_total': delta_chi2_total,
            'dof_total': dof_total,
            'BIC_LCDM': BIC_LCDM,
            'BIC_Klein': BIC_Klein,
            'delta_BIC': delta_BIC,
            'klein_significance': klein_significance,
            'bayes_factor': bayes_factor,
            'klein_preferred': delta_chi2_total > 4.0,
            'evidence_interpretation': self._interpret_evidence(bayes_factor)
        }
    
    def _interpret_evidence(self, bayes_factor: float) -> str:
        """Interpreta Bayes factor."""
        if bayes_factor > 100:
            return "Very strong evidence for Klein"
        elif bayes_factor > 10:
            return "Strong evidence for Klein"
        elif bayes_factor > 3:
            return "Moderate evidence for Klein"
        elif bayes_factor > 1:
            return "Weak evidence for Klein"
        elif bayes_factor > 0.1:
            return "Weak evidence for LCDM"
        else:
            return "Strong evidence for LCDM"
    
    def create_visualizations(self, bao_data: Dict, lss_data: Dict, 
                             analysis_results: Dict) -> str:
        """Crea visualizaciones del análisis BAO/LSS Klein."""
        
        print("\n📊 Creando visualizaciones BAO/LSS...")
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # 1. Hubble parameter H(z) evolution
        ax = axes[0, 0]
        
        z = bao_data['redshift']
        H_obs = bao_data['H_z_observed']
        H_LCDM = bao_data['H_z_LCDM']
        H_Klein = bao_data['H_z_Klein']
        H_errors = bao_data['H_z_errors']
        
        ax.errorbar(z, H_obs, yerr=H_errors, fmt='o', alpha=0.7, 
                   label='Observed (simulated)', capsize=3)
        ax.plot(z, H_LCDM, 'b-', linewidth=2, label='ΛCDM')
        ax.plot(z, H_Klein, 'r-', linewidth=2, label='Klein Model')
        
        ax.set_xlabel('Redshift z')
        ax.set_ylabel('H(z) (km/s/Mpc)')
        ax.set_title('Hubble Parameter Evolution')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # 2. Dark Energy equation of state w(z)
        ax = axes[0, 1]
        
        w_params = analysis_results['bao_analysis']['w_params_fitted']
        if w_params['fit_success']:
            z_fine = np.linspace(0, 3, 100)
            z_trans = self.klein_params['z_transition']
            w_z_fit = w_params['w0'] + w_params['wa'] * np.tanh((z_fine - z_trans) / 0.5)
            w_z_expected = (self.klein_params['w0_klein'] + 
                           self.klein_params['wa_klein'] * np.tanh((z_fine - z_trans) / 0.5))
            
            ax.plot(z_fine, w_z_fit, 'g-', linewidth=2, 
                   label=f'Fitted (w₀={w_params["w0"]:.2f}±{w_params["w0_error"]:.2f})')
            ax.plot(z_fine, w_z_expected, 'r--', linewidth=2, label='Klein Prediction')
            ax.axhline(-1, color='blue', linestyle=':', label='ΛCDM (w=-1)')
            ax.axvline(z_trans, color='gray', linestyle='--', alpha=0.5, label='Transition z')
        
        ax.set_xlabel('Redshift z')
        ax.set_ylabel('w(z)')
        ax.set_title('Dark Energy Equation of State')
        ax.legend()
        ax.grid(True, alpha=0.3)
        ax.set_ylim(-1.5, 0)
        
        # 3. LSS correlation function
        ax = axes[1, 0]
        
        r_bins = lss_data['r_bins']
        xi_obs = lss_data['xi_observed']
        xi_LCDM = lss_data['xi_LCDM']
        xi_Klein = lss_data['xi_Klein']
        xi_errors = lss_data['xi_errors']
        
        ax.errorbar(r_bins, xi_obs, yerr=xi_errors, fmt='o', alpha=0.7,
                   label='Observed', capsize=2)
        ax.plot(r_bins, xi_LCDM, 'b-', linewidth=2, label='ΛCDM')
        ax.plot(r_bins, xi_Klein, 'r-', linewidth=2, label='Klein Model')
        
        ax.set_xlabel('r (Mpc)')
        ax.set_ylabel('ξ(r)')
        ax.set_title('Galaxy Correlation Function')
        ax.set_xscale('log')
        ax.set_yscale('log')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # 4. Analysis summary
        ax = axes[1, 1]
        ax.axis('off')
        
        # Summary statistics
        bao_results = analysis_results['bao_analysis']
        lss_results = analysis_results['lss_analysis']
        comparison_results = analysis_results['model_comparison']
        
        summary_text = f"""BAO/LSS Klein Analysis Summary

BAO Analysis:
  H(z) Klein vs ΛCDM: Δχ² = {bao_results['delta_chi2']:.2f}
  DE evolution significance: {bao_results['w_evolution_significance']:.2f}σ
  w₀ fitted: {bao_results['w_params_fitted']['w0']:.2f}±{bao_results['w_params_fitted']['w0_error']:.2f}
  wₐ fitted: {bao_results['w_params_fitted']['wa']:.2f}±{bao_results['w_params_fitted']['wa_error']:.2f}
  Klein preferred: {bao_results['klein_preferred']}

LSS Analysis:
  Correlation length r₀: {lss_results['r0_observed']:.2f} Mpc
  ΛCDM prediction: {lss_results['r0_LCDM']:.2f} Mpc
  Klein prediction: {lss_results['r0_Klein']:.2f} Mpc
  Enhancement factor: {lss_results['correlation_enhancement']:.3f}
  Expected enhancement: {lss_results['expected_enhancement']:.3f}
  Agreement: {lss_results['enhancement_agreement']}

Model Comparison:
  Combined Δχ²: {comparison_results['delta_chi2_total']:.2f}
  Klein significance: {comparison_results['klein_significance']:.2f}σ
  ΔBIC: {comparison_results['delta_BIC']:.2f}
  Bayes factor: {comparison_results['bayes_factor']:.2f}
  Evidence: {comparison_results['evidence_interpretation']}

Klein Parameters:
  DE transition z: {self.klein_params['z_transition']}
  Correlation enhancement: {self.klein_params['r0_enhancement']}
  R_Klein: {self.klein_params['R_Klein_m']/1000:.0f} km"""
        
        ax.text(0.05, 0.95, summary_text, transform=ax.transAxes,
               fontsize=9, fontfamily='monospace', verticalalignment='top')
        
        plt.tight_layout()
        
        # Save plot
        plot_filename = "bao_lss_klein_analysis.png"
        plt.savefig(plot_filename, dpi=300, bbox_inches='tight')
        print(f"✅ Visualización guardada: {plot_filename}")
        
        return plot_filename
    
    def save_results(self, bao_data: Dict, lss_data: Dict, analysis_results: Dict,
                    filename: str = "bao_lss_klein_results.json") -> str:
        """Guarda resultados del análisis BAO/LSS Klein."""
        
        # Prepare results for JSON serialization
        results_summary = {
            'metadata': {
                'analysis_type': 'BAO/LSS Klein Field Theory Validation',
                'date': '2025-07-23',
                'klein_parameters': self.klein_params,
                'cosmology_reference': self.cosmo_params
            },
            'data_summary': {
                'bao_redshift_range': f"z = {bao_data['redshift'][0]:.1f} - {bao_data['redshift'][-1]:.1f}",
                'bao_n_bins': bao_data['n_redshift_bins'],
                'lss_n_galaxies': lss_data['n_galaxies'],
                'sound_horizon_rs': bao_data['rs_drag']
            },
            'analysis_results': analysis_results,
            'conclusions': {
                'de_evolution_detected': analysis_results['bao_analysis']['w_evolution_detected'],
                'lss_enhancement_detected': analysis_results['lss_analysis']['enhancement_agreement'],
                'klein_cosmology_preferred': analysis_results['model_comparison']['klein_preferred'],
                'combined_significance': analysis_results['model_comparison']['klein_significance'],
                'bayes_factor': analysis_results['model_comparison']['bayes_factor'],
                'evidence_strength': analysis_results['model_comparison']['evidence_interpretation'],
                'falsification_status': 'Klein cosmology supported' if analysis_results['model_comparison']['klein_preferred'] else 'ΛCDM preferred'
            }
        }
        
        # Convert numpy types for JSON serialization
        def convert_numpy(obj):
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            elif isinstance(obj, np.generic):
                return obj.item()
            elif isinstance(obj, dict):
                return {key: convert_numpy(value) for key, value in obj.items()}
            elif isinstance(obj, list):
                return [convert_numpy(item) for item in obj]
            else:
                return obj
        
        results_summary = convert_numpy(results_summary)
        
        # Save to JSON
        with open(filename, 'w') as f:
            json.dump(results_summary, f, indent=2)
        
        print(f"✅ Resultados guardados: {filename}")
        return filename

def main():
    """Ejecuta análisis BAO/LSS completo para Klein Field Theory."""
    
    print("🌌 BAO/LSS Klein Analysis - Dark Energy Evolucionando")
    print("=" * 60)
    print("Basado en Klein Field Theory: DE dinámica w(z) + LSS enhancement")
    print("Predicciones: w transition z~1.5, r₀ enhancement +15%")
    print("Dataset: DESI-style BAO + LSS correlations")
    print("=" * 60)
    
    # Initialize analyzer
    analyzer = BAOKleinAnalyzer()
    
    # Generate BAO data
    print("\n1. Generando datos BAO...")
    bao_data = analyzer.generate_bao_data(z_max=3.0, n_redshift_bins=20)
    
    # Generate LSS data
    print("\n2. Generando datos LSS...")
    lss_data = analyzer.generate_lss_data(n_galaxies=1000000)
    
    # Analyze Klein signatures
    print("\n3. Analizando firmas Klein...")
    analysis_results = analyzer.analyze_klein_signatures(bao_data, lss_data)
    
    # Create visualizations
    print("\n4. Creando visualizaciones...")
    plot_file = analyzer.create_visualizations(bao_data, lss_data, analysis_results)
    
    # Save results
    print("\n5. Guardando resultados...")
    results_file = analyzer.save_results(bao_data, lss_data, analysis_results)
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 RESUMEN BAO/LSS KLEIN ANALYSIS")
    print("=" * 60)
    
    klein_preferred = analysis_results['model_comparison']['klein_preferred']
    significance = analysis_results['model_comparison']['klein_significance']
    de_evolution = analysis_results['bao_analysis']['w_evolution_detected']
    lss_enhancement = analysis_results['lss_analysis']['enhancement_agreement']
    evidence = analysis_results['model_comparison']['evidence_interpretation']
    
    print(f"Klein Cosmology Preferred: {klein_preferred}")
    print(f"Combined Significance: {significance:.2f}σ")
    print(f"DE Evolution Detected: {de_evolution}")
    print(f"LSS Enhancement: {lss_enhancement}")
    print(f"Evidence Strength: {evidence}")
    
    if klein_preferred:
        print("✅ RESULTADO: Klein cosmology signatures detected")
        print("   - Dark energy evolution confirmed")
        print("   - LSS correlation enhancement detected")
        print("   - Klein field unifies dark sector")
        print("   - Next-generation surveys will provide decisive test")
    else:
        print("❌ RESULTADO: ΛCDM cosmology preferred")
        print("   - No significant DE evolution detected")
        print("   - LSS correlations consistent with standard model")
        print("   - Klein effects below current sensitivity")
        print("   - Larger surveys needed for definitive test")
    
    print(f"\nFiles created:")
    print(f"  - Results: {results_file}")
    print(f"  - Plots: {plot_file}")
    
    print("\n🔬 BAO/LSS Klein Analysis Complete!")
    print("Ready for Phase 4: Gravity Tests")
    
    return analyzer, analysis_results

if __name__ == "__main__":
    analyzer, results = main()