#!/usr/bin/env python3
"""
RIGOROUS SUPERNOVAE ANALYSIS - KLEIN THEORY VALIDATION
=====================================================

Análisis no sesgado de supernovas Tipo Ia para efectos Klein en cosmología.

Author: Klein Theory Validation Team
Date: July 26, 2025
Status: Empirical validation module
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.stats import chi2
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from klein_stats_utils import p_value_to_sigma
import json
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Cosmología simple sin astropy
class SimpleFlatLambdaCDM:
    """Cosmología ΛCDM plana simple sin dependencias externas."""
    
    def __init__(self, H0=70, Om0=0.3):
        self.H0 = H0
        self.Om0 = Om0
        self.OL0 = 1 - Om0
        
    def E(self, z):
        """Factor de expansión E(z) = H(z)/H0."""
        return np.sqrt(self.Om0 * (1+z)**3 + self.OL0)
        
    def comoving_distance(self, z):
        """Distancia comóvil en Mpc."""
        from scipy.integrate import quad
        
        def integrand(zp):
            return 1.0 / self.E(zp)
            
        c_km_s = 299792.458  # km/s
        
        # Handle both scalar and array inputs
        if np.isscalar(z):
            result, _ = quad(integrand, 0, z)
            return c_km_s / self.H0 * result
        else:
            # For arrays, integrate each element
            distances = []
            for z_val in z:
                result, _ = quad(integrand, 0, z_val)
                distances.append(c_km_s / self.H0 * result)
            return np.array(distances)
        
    def luminosity_distance(self, z):
        """Distancia de luminosidad en Mpc."""
        return self.comoving_distance(z) * (1 + z)
        
    def distmod(self, z):
        """Módulo de distancia."""
        DL = self.luminosity_distance(z)
        return 5 * np.log10(DL) + 25

class RigorousSupernovaAnalysis:
    """Análisis riguroso de supernovas Tipo Ia para efectos Klein en cosmología."""
    
    def __init__(self, data_path=None):
        self.data_path = data_path
        self.results = {}
        self.analysis_timestamp = datetime.now().isoformat()
        
    def load_supernova_data(self):
        """Carga datos de supernovas desde archivo o simula datos sintéticos."""
        
        # Buscar datos Pantheon+ reales
        pantheon_data_dir = "/mnt/d/Multidimensional Theory Simulations/multidimensional-theory/gravitational-wave-echoes-5d/EMPIRICAL_KLEIN_STUDIES/5_Supernovae_Analysis"
        pantheon_file = os.path.join(pantheon_data_dir, "pantheon_plus_processed.json")
        
        if os.path.exists(pantheon_file):
            print("🔍 Cargando datos reales Pantheon+...")
            self._load_pantheon_plus_data(pantheon_file)
        else:
            print("⚠ Simulando datos de supernovas sintéticos")
            self._simulate_supernova_data()
            
    def _load_pantheon_plus_data(self, pantheon_file):
        """Carga datos reales Pantheon+."""
        try:
            import json
            with open(pantheon_file, 'r') as f:
                pantheon_data = json.load(f)
            
            print(f"✓ Datos Pantheon+ cargados: {len(pantheon_data)} SNe Ia")
            
            # Extraer redshifts, magnitudes y errores
            redshifts = []
            magnitudes = []
            mag_errors = []
            
            for sn in pantheon_data:
                if sn['redshift'] > 0.01 and sn['redshift'] < 2.0:  # Filtrar rango válido
                    redshifts.append(sn['redshift'])
                    magnitudes.append(sn['magnitude'])
                    mag_errors.append(sn['magnitude_error'])
            
            self.z = np.array(redshifts)
            self.mu_obs = np.array(magnitudes)
            self.err_mu = np.array(mag_errors)
            
            # Ordenar por redshift
            sort_idx = np.argsort(self.z)
            self.z = self.z[sort_idx]
            self.mu_obs = self.mu_obs[sort_idx]
            self.err_mu = self.err_mu[sort_idx]
            
            self.data_source = "pantheon_plus_real_data"
            print(f"✓ {len(self.z)} SNe Ia válidas cargadas de Pantheon+")
            
        except Exception as e:
            print(f"✗ Error cargando Pantheon+: {e}")
            self._simulate_supernova_data()
            
    def _simulate_supernova_data(self):
        """Simula datos sintéticos de supernovas."""
        print("⚠ Simulando datos de supernovas sintéticos")
        
        # Redshifts típicos de Pantheon+
        n_sne = 100
        self.z = np.random.uniform(0.01, 1.0, n_sne)
        self.z = np.sort(self.z)
        
        # Cosmología fiducial
        cosmo_fid = SimpleFlatLambdaCDM(H0=70, Om0=0.3)
        
        # Módulos de distancia teóricos
        mu_theory = cosmo_fid.distmod(self.z)
        
        # Errores observacionales
        self.err_mu = np.random.uniform(0.05, 0.15, n_sne)
        
        # Posible señal Klein (dependiente de redshift)
        klein_correction = 0.001 * np.sin(2*np.pi * self.z / 0.5)
        
        self.mu_obs = mu_theory + klein_correction + np.random.normal(0, self.err_mu)
        
        self.data_source = "simulated_supernova_data"
        print(f"✓ Datos supernovas simulados: {len(self.z)} SNe Ia")
        
    def model_standard_cosmology(self, z, H0, Om0):
        """Modelo cosmológico estándar ΛCDM."""
        cosmo = SimpleFlatLambdaCDM(H0=H0, Om0=Om0)
        return cosmo.distmod(z)
        
    def model_klein_cosmology(self, z, H0, Om0, gamma_klein):
        """Modelo cosmológico con modificaciones Klein."""
        mu_standard = self.model_standard_cosmology(z, H0, Om0)
        klein_correction = gamma_klein * np.sin(2*np.pi * z / 0.5)
        return mu_standard + klein_correction
        
    def fit_cosmological_models(self):
        """Ajusta modelos cosmológicos estándar y Klein."""
        
        print("🔄 Ajustando modelo cosmológico estándar...")
        
        try:
            popt_standard, pcov_standard = curve_fit(
                self.model_standard_cosmology,
                self.z, self.mu_obs, sigma=self.err_mu,
                p0=[70.0, 0.3], bounds=([60, 0.2], [80, 0.4])
            )
            
            mu_fit_standard = self.model_standard_cosmology(self.z, *popt_standard)
            chi2_standard = np.sum(((self.mu_obs - mu_fit_standard) / self.err_mu)**2)
            dof_standard = len(self.z) - len(popt_standard)
            
            self.results['standard_fit'] = {
                'parameters': {'H0': popt_standard[0], 'Om0': popt_standard[1]},
                'chi2': chi2_standard,
                'dof': dof_standard,
                'chi2_reduced': chi2_standard / dof_standard
            }
            
            print(f"✓ ΛCDM: H0 = {popt_standard[0]:.1f}, Ωm = {popt_standard[1]:.3f}")
            
        except Exception as e:
            print(f"✗ Error ajuste estándar: {e}")
            return False
            
        print("🔄 Ajustando modelo Klein...")
        
        try:
            popt_klein, pcov_klein = curve_fit(
                self.model_klein_cosmology,
                self.z, self.mu_obs, sigma=self.err_mu,
                p0=[70.0, 0.3, 0.001], bounds=([60, 0.2, -0.01], [80, 0.4, 0.01])
            )
            
            mu_fit_klein = self.model_klein_cosmology(self.z, *popt_klein)
            chi2_klein = np.sum(((self.mu_obs - mu_fit_klein) / self.err_mu)**2)
            dof_klein = len(self.z) - len(popt_klein)
            
            self.results['klein_fit'] = {
                'parameters': {
                    'H0': popt_klein[0],
                    'Om0': popt_klein[1], 
                    'gamma_klein': popt_klein[2]
                },
                'chi2': chi2_klein,
                'dof': dof_klein,
                'chi2_reduced': chi2_klein / dof_klein
            }
            
            print(f"✓ Klein: γ = {popt_klein[2]:.4f}")
            
        except Exception as e:
            print(f"✗ Error ajuste Klein: {e}")
            return False
            
        return True
        
    def calculate_significance(self):
        """Calcula significancia del modelo Klein vs ΛCDM estándar."""
        
        delta_chi2 = self.results['standard_fit']['chi2'] - self.results['klein_fit']['chi2']
        delta_dof = self.results['standard_fit']['dof'] - self.results['klein_fit']['dof']
        
        if delta_chi2 > 0:
            p_value = chi2.sf(delta_chi2, delta_dof)
            sigma_level = p_value_to_sigma(p_value) if 0 < p_value < 1 else 0
        else:
            p_value = 1.0
            sigma_level = 0.0
            
        self.results['significance'] = {
            'delta_chi2': delta_chi2,
            'p_value': p_value,
            'sigma_level': sigma_level
        }
        
        print(f"📊 Δχ² = {delta_chi2:.2f}, σ = {sigma_level:.2f}")
        
    def save_results(self, output_dir):
        """Guarda resultados."""
        
        self.results['metadata'] = {
            'analysis_type': 'Supernovae_Klein_Rigorous',
            'timestamp': self.analysis_timestamp,
            'data_source': self.data_source,
            'n_supernovae': len(self.z)
        }
        
        results_path = os.path.join(output_dir, 'rigorous_supernovae_klein_results.json')
        with open(results_path, 'w') as f:
            json.dump(self.results, f, indent=2, default=str)
        print(f"✓ Resultados guardados: {results_path}")
        
    def run_complete_analysis(self, output_dir):
        """Ejecuta análisis completo."""
        
        print("💫 INICIANDO ANÁLISIS RIGUROSO SUPERNOVAS - KLEIN THEORY")
        print("="*60)
        
        os.makedirs(output_dir, exist_ok=True)
        
        self.load_supernova_data()
        
        if self.fit_cosmological_models():
            self.calculate_significance()
            self.save_results(output_dir)
            
            sigma = self.results['significance']['sigma_level']
            print(f"\n📋 RESULTADO: {sigma:.2f}σ evidencia para efectos Klein")
            
            return True
        else:
            print("✗ Análisis falló")
            return False

def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    analyzer = RigorousSupernovaAnalysis()
    success = analyzer.run_complete_analysis(current_dir)
    
    return success

if __name__ == "__main__":
    main()