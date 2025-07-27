#!/usr/bin/env python3
"""
RIGOROUS BAO & LSS ANALYSIS - KLEIN THEORY VALIDATION
====================================================

Análisis no sesgado de Oscilaciones Acústicas de Bariones (BAO) y Estructura
a Gran Escala (LSS) para detectar modificaciones Klein en correlaciones
espaciales y escalas características.

Author: Klein Theory Validation Team
Date: July 26, 2025  
Status: Empirical validation module
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit, minimize
from scipy.stats import chi2
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from klein_stats_utils import p_value_to_sigma, model_comparison_stats
from scipy.interpolate import interp1d
# astropy not available
import json
import os
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Cosmología simple sin astropy
class SimpleFlatLambdaCDM:
    def __init__(self, H0=67.4, Om0=0.315):
        self.H0 = H0
        self.Om0 = Om0

class RigorousBAOLSSAnalysis:
    """
    Análisis riguroso de BAO y LSS para efectos Klein.
    Enfoque en función de correlación y espectro de potencia.
    """
    
    def __init__(self, data_path=None):
        self.data_path = data_path
        self.results = {}
        self.analysis_timestamp = datetime.now().isoformat()
        
    def load_bao_lss_data(self):
        """Carga datos BAO/LSS desde archivo o simula datos sintéticos."""
        
        if self.data_path and os.path.exists(self.data_path):
            try:
                df = pd.read_csv(self.data_path)
                
                # Para función de correlación
                if all(col in df.columns for col in ['r', 'xi', 'err_xi']):
                    self.r = df['r'].values
                    self.xi_obs = df['xi'].values
                    self.err_xi = df['err_xi'].values
                    self.data_type = "correlation_function"
                    
                # Para espectro de potencia
                elif all(col in df.columns for col in ['k', 'Pk', 'err_Pk']):
                    self.k = df['k'].values
                    self.Pk_obs = df['Pk'].values
                    self.err_Pk = df['err_Pk'].values
                    self.data_type = "power_spectrum"
                    
                else:
                    raise ValueError("Formato de datos no reconocido")
                    
                self.data_source = "real_data"
                print(f"✓ Datos BAO/LSS cargados: {len(df)} puntos ({self.data_type})")
                
            except Exception as e:
                print(f"Error cargando datos: {e}")
                self._simulate_bao_lss_data()
        else:
            self._simulate_bao_lss_data()
            
    def _simulate_bao_lss_data(self):
        """Simula datos BAO/LSS sintéticos."""
        print("⚠ Simulando datos BAO/LSS sintéticos para testing")
        
        # Simular función de correlación
        self.r = np.logspace(0, 2.5, 50)  # 1-300 Mpc/h
        
        # Parámetros cosmológicos fiduciales
        cosmo = SimpleFlatLambdaCDM(H0=67.4, Om0=0.315)
        
        # Escala BAO (horizonte sonido)
        r_s = 147.78  # Mpc/h
        
        # Función de correlación teórica simplificada
        xi_theory = self._bao_correlation_template(self.r, r_s)
        
        # Añadir ruido realista
        noise_level = 0.1
        self.err_xi = noise_level * np.abs(xi_theory) + 0.001
        self.xi_obs = xi_theory + np.random.normal(0, self.err_xi)
        
        self.data_type = "correlation_function"
        self.data_source = "simulated_data"
        
    def _bao_correlation_template(self, r, r_s, alpha=1.0):
        """Plantilla de función de correlación BAO."""
        
        # Parte continua (decaimiento exponencial)
        xi_smooth = 10 * np.exp(-r/100) / (r/10)**1.8
        
        # Oscilación BAO
        bao_osc = 5 * np.exp(-r/200) * np.sin(2*np.pi * r / (alpha * r_s)) / (r/r_s)
        
        return xi_smooth + bao_osc
        
    def model_standard_bao(self, r, A_smooth, gamma, r_s, A_bao, alpha):
        """
        Modelo estándar BAO para función de correlación.
        
        Parámetros:
        -----------
        r : array
            Separaciones [Mpc/h]
        A_smooth : float
            Amplitud componente lisa
        gamma : float  
            Índice de decaimiento
        r_s : float
            Escala BAO (horizonte sonido)
        A_bao : float
            Amplitud oscilación BAO
        alpha : float
            Factor de escala BAO (≈1 para ΛCDM)
        """
        # Componente lisa
        xi_smooth = A_smooth * np.exp(-r/100) / (r/10)**gamma
        
        # Oscilación BAO
        xi_bao = A_bao * np.exp(-r/200) * np.sin(2*np.pi * r / (alpha * r_s)) / (r/r_s)
        
        return xi_smooth + xi_bao
        
    def model_klein_bao(self, r, A_smooth, gamma, r_s, A_bao, alpha, R4_scale):
        """
        Modelo Klein para función de correlación BAO.
        Introduce modificación dependiente de escala R4.
        
        Parámetros adicionales:
        ----------------------
        R4_scale : float
            Escala Klein característica [Mpc/h]
        """
        # Modelo estándar base
        xi_standard = self.model_standard_bao(r, A_smooth, gamma, r_s, A_bao, alpha)
        
        # Corrección Klein: modificación de escala dependiente de r
        klein_correction = 1 + 0.01 * np.exp(-r/R4_scale) * np.log(r/R4_scale + 1)
        
        return xi_standard * klein_correction
        
    def fit_bao_models(self):
        """Ajusta modelos estándar y Klein a datos BAO."""
        
        if self.data_type != "correlation_function":
            print("⚠ Análisis actual solo soporta función de correlación")
            return False
            
        print("🔄 Ajustando modelo estándar BAO...")
        
        # Parámetros iniciales estándar
        p0_standard = [10.0, 1.8, 147.78, 5.0, 1.0]  # A_smooth, gamma, r_s, A_bao, alpha
        bounds_standard = ([0.1, 0.5, 140, 0.1, 0.8], [100, 3.0, 155, 50, 1.2])
        
        try:
            popt_standard, pcov_standard = curve_fit(
                self.model_standard_bao,
                self.r,
                self.xi_obs,
                sigma=self.err_xi,
                p0=p0_standard,
                bounds=bounds_standard,
                maxfev=5000
            )
            
            xi_fit_standard = self.model_standard_bao(self.r, *popt_standard)
            chi2_standard = np.sum(((self.xi_obs - xi_fit_standard) / self.err_xi)**2)
            dof_standard = len(self.r) - len(popt_standard)
            chi2_red_standard = chi2_standard / dof_standard
            
            self.results['standard_fit'] = {
                'parameters': {
                    'A_smooth': popt_standard[0],
                    'gamma': popt_standard[1], 
                    'r_s': popt_standard[2],
                    'A_bao': popt_standard[3],
                    'alpha': popt_standard[4]
                },
                'parameter_errors': np.sqrt(np.diag(pcov_standard)).tolist(),
                'chi2': chi2_standard,
                'dof': dof_standard,
                'chi2_reduced': chi2_red_standard
            }
            
            print(f"✓ Ajuste estándar: χ²/dof = {chi2_red_standard:.3f}, α = {popt_standard[4]:.3f}")
            
        except Exception as e:
            print(f"✗ Error en ajuste estándar: {e}")
            return False
            
        print("🔄 Ajustando modelo Klein...")
        
        # Parámetros iniciales Klein (añade R4_scale)
        p0_klein = list(p0_standard) + [50.0]  # R4_scale inicial = 50 Mpc/h
        bounds_klein = (list(bounds_standard[0]) + [1.0], 
                       list(bounds_standard[1]) + [500.0])
        
        try:
            popt_klein, pcov_klein = curve_fit(
                self.model_klein_bao,
                self.r,
                self.xi_obs,
                sigma=self.err_xi,
                p0=p0_klein,
                bounds=bounds_klein,
                maxfev=5000
            )
            
            xi_fit_klein = self.model_klein_bao(self.r, *popt_klein)
            chi2_klein = np.sum(((self.xi_obs - xi_fit_klein) / self.err_xi)**2)
            dof_klein = len(self.r) - len(popt_klein)
            chi2_red_klein = chi2_klein / dof_klein
            
            self.results['klein_fit'] = {
                'parameters': {
                    'A_smooth': popt_klein[0],
                    'gamma': popt_klein[1],
                    'r_s': popt_klein[2], 
                    'A_bao': popt_klein[3],
                    'alpha': popt_klein[4],
                    'R4_scale': popt_klein[5]
                },
                'parameter_errors': np.sqrt(np.diag(pcov_klein)).tolist(),
                'chi2': chi2_klein,
                'dof': dof_klein,
                'chi2_reduced': chi2_red_klein
            }
            
            print(f"✓ Ajuste Klein: χ²/dof = {chi2_red_klein:.3f}, R4 = {popt_klein[5]:.1f} Mpc/h")
            
        except Exception as e:
            print(f"✗ Error en ajuste Klein: {e}")
            return False
            
        return True
        
    def calculate_significance(self):
        """Calcula significancia estadística del modelo Klein vs estándar."""
        
        if 'standard_fit' not in self.results or 'klein_fit' not in self.results:
            print("✗ Falta información de ajustes")
            return
            
        # Test de razón de verosimilitudes
        delta_chi2 = self.results['standard_fit']['chi2'] - self.results['klein_fit']['chi2']
        delta_dof = self.results['standard_fit']['dof'] - self.results['klein_fit']['dof']
        
        if delta_chi2 > 0:
            p_value = chi2.sf(delta_chi2, delta_dof)
            sigma_level = p_value_to_sigma(p_value) if 0 < p_value < 1 else 0.0
        else:
            p_value = 1.0
            sigma_level = 0.0
            
        # Criterios de información
        aic_standard = self.results['standard_fit']['chi2'] + 2 * len(self.results['standard_fit']['parameters'])
        aic_klein = self.results['klein_fit']['chi2'] + 2 * len(self.results['klein_fit']['parameters'])
        delta_aic = aic_klein - aic_standard
        
        bic_standard = self.results['standard_fit']['chi2'] + np.log(len(self.r)) * len(self.results['standard_fit']['parameters'])
        bic_klein = self.results['klein_fit']['chi2'] + np.log(len(self.r)) * len(self.results['klein_fit']['parameters'])
        delta_bic = bic_klein - bic_standard
        
        self.results['significance'] = {
            'delta_chi2': delta_chi2,
            'delta_dof': delta_dof,
            'p_value': p_value,
            'sigma_level': sigma_level,
            'delta_aic': delta_aic,
            'delta_bic': delta_bic,
            'interpretation': self._interpret_bao_significance(sigma_level, delta_aic, delta_bic)
        }
        
        print(f"📊 Δχ² = {delta_chi2:.2f}, p = {p_value:.2e}, σ = {sigma_level:.2f}")
        print(f"📊 ΔAIC = {delta_aic:.2f}, ΔBIC = {delta_bic:.2f}")
        
    def _interpret_bao_significance(self, sigma_level, delta_aic, delta_bic):
        """Interpreta significancia para análisis BAO."""
        
        interpretation = []
        
        # Significancia estadística
        if sigma_level >= 5.0:
            interpretation.append("DETECCIÓN ALTAMENTE SIGNIFICATIVA (≥5σ)")
        elif sigma_level >= 3.0:
            interpretation.append("EVIDENCIA SIGNIFICATIVA (≥3σ)")
        elif sigma_level >= 1.0:
            interpretation.append("EVIDENCIA MARGINAL (≥1σ)")
        else:
            interpretation.append("NO EVIDENCIA SIGNIFICATIVA (<1σ)")
            
        # Selección de modelo (AIC)
        if delta_aic < -10:
            interpretation.append("Modelo Klein fuertemente preferido (ΔAIC < -10)")
        elif delta_aic < -2:
            interpretation.append("Modelo Klein preferido (ΔAIC < -2)")
        elif delta_aic > 10:
            interpretation.append("Modelo estándar fuertemente preferido (ΔAIC > 10)")
        elif delta_aic > 2:
            interpretation.append("Modelo estándar preferido (ΔAIC > 2)")
        else:
            interpretation.append("Modelos estadísticamente equivalentes (AIC)")
            
        # Validación adicional (BIC más conservativo)
        if delta_bic < -10:
            interpretation.append("Klein confirmado por criterio BIC conservativo")
        elif delta_bic > 10:
            interpretation.append("Estándar confirmado por criterio BIC conservativo")
            
        return interpretation
        
    def analyze_bao_scale_shift(self):
        """Analiza desplazamiento en escala BAO característica."""
        
        if 'standard_fit' not in self.results or 'klein_fit' not in self.results:
            return
            
        # Escala BAO teórica
        r_s_theory = 147.78  # Mpc/h para cosmología fiducial
        
        # Escalas ajustadas
        alpha_standard = self.results['standard_fit']['parameters']['alpha']
        alpha_klein = self.results['klein_fit']['parameters']['alpha']
        
        # Desplazamientos respecto a teoría
        shift_standard = (alpha_standard - 1.0) * 100  # Porcentaje
        shift_klein = (alpha_klein - 1.0) * 100
        
        # Error en alfa
        alpha_err_std = self.results['standard_fit']['parameter_errors'][4]
        alpha_err_klein = self.results['klein_fit']['parameter_errors'][4]
        
        self.results['bao_scale_analysis'] = {
            'theoretical_rs': r_s_theory,
            'alpha_standard': alpha_standard,
            'alpha_klein': alpha_klein,
            'shift_standard_percent': shift_standard,
            'shift_klein_percent': shift_klein,
            'alpha_error_standard': alpha_err_std,
            'alpha_error_klein': alpha_err_klein,
            'significant_shift': abs(shift_klein/100) > 2 * alpha_err_klein
        }
        
        print(f"📏 Desplazamiento BAO estándar: {shift_standard:.2f}% ± {alpha_err_std*100:.2f}%")
        print(f"📏 Desplazamiento BAO Klein: {shift_klein:.2f}% ± {alpha_err_klein*100:.2f}%")
        
    def create_diagnostic_plots(self, output_dir):
        """Genera plots diagnósticos del análisis BAO/LSS."""
        
        if 'standard_fit' not in self.results or 'klein_fit' not in self.results:
            print("✗ No hay ajustes disponibles para plotting")
            return
            
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        
        # Plot 1: Función de correlación con ajustes
        ax1.errorbar(self.r, self.xi_obs, yerr=self.err_xi,
                    fmt='o', color='black', alpha=0.7, markersize=4, label='Datos observados')
        
        # Modelo estándar
        xi_standard = self.model_standard_bao(self.r, 
                                            *list(self.results['standard_fit']['parameters'].values()))
        ax1.plot(self.r, xi_standard, 'b-', linewidth=2, label='Modelo estándar BAO')
        
        # Modelo Klein
        xi_klein = self.model_klein_bao(self.r,
                                      *list(self.results['klein_fit']['parameters'].values()))
        ax1.plot(self.r, xi_klein, 'r--', linewidth=2, label='Modelo Klein')
        
        ax1.set_xlabel('Separación r [Mpc/h]')
        ax1.set_ylabel('ξ(r)')
        ax1.set_xscale('log')
        ax1.legend()
        ax1.set_title('Función de Correlación BAO')
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Residuales multiplicados por r²
        res_standard = (self.xi_obs - xi_standard) / self.err_xi
        res_klein = (self.xi_obs - xi_klein) / self.err_xi
        
        ax2.plot(self.r, res_standard, 'bo-', alpha=0.7, label='Residuales estándar')
        ax2.plot(self.r, res_klein, 'ro-', alpha=0.7, label='Residuales Klein')
        ax2.axhline(y=0, color='k', linestyle='-', alpha=0.5)
        ax2.axhline(y=2, color='k', linestyle='--', alpha=0.3, label='±2σ')
        ax2.axhline(y=-2, color='k', linestyle='--', alpha=0.3)
        ax2.set_xlabel('Separación r [Mpc/h]')
        ax2.set_ylabel('Residuales normalizados')
        ax2.set_xscale('log')
        ax2.legend()
        ax2.set_title('Análisis de Residuales')
        ax2.grid(True, alpha=0.3)
        
        # Plot 3: r²·ξ(r) para resaltar oscilaciones BAO
        r2_xi_obs = self.r**2 * self.xi_obs
        r2_xi_err = self.r**2 * self.err_xi
        r2_xi_standard = self.r**2 * xi_standard
        r2_xi_klein = self.r**2 * xi_klein
        
        ax3.errorbar(self.r, r2_xi_obs, yerr=r2_xi_err,
                    fmt='o', color='black', alpha=0.7, markersize=3, label='Datos × r²')
        ax3.plot(self.r, r2_xi_standard, 'b-', linewidth=2, label='Estándar × r²')
        ax3.plot(self.r, r2_xi_klein, 'r--', linewidth=2, label='Klein × r²')
        
        # Marcar escala BAO
        r_s = self.results['standard_fit']['parameters']['r_s']
        ax3.axvline(x=r_s, color='gray', linestyle=':', alpha=0.7, label=f'r_s = {r_s:.1f} Mpc/h')
        
        ax3.set_xlabel('Separación r [Mpc/h]')
        ax3.set_ylabel('r² ξ(r)')
        ax3.legend()
        ax3.set_title('Función de Correlación × r² (resalta BAO)')
        ax3.grid(True, alpha=0.3)
        
        # Plot 4: Información estadística
        ax4.axis('off')
        
        # Obtener parámetros Klein
        R4_scale = self.results['klein_fit']['parameters']['R4_scale']
        R4_error = self.results['klein_fit']['parameter_errors'][5]
        
        stats_text = f"""
ANÁLISIS BAO/LSS RIGUROSO

Datos: {self.data_source}
Puntos: {len(self.r)}
Rango: {self.r.min():.1f} - {self.r.max():.1f} Mpc/h

MODELO ESTÁNDAR:
χ²/dof = {self.results['standard_fit']['chi2_reduced']:.3f}
α = {self.results['standard_fit']['parameters']['alpha']:.3f}
r_s = {self.results['standard_fit']['parameters']['r_s']:.1f} Mpc/h

MODELO KLEIN:
χ²/dof = {self.results['klein_fit']['chi2_reduced']:.3f}
α = {self.results['klein_fit']['parameters']['alpha']:.3f}
R4_scale = {R4_scale:.1f} ± {R4_error:.1f} Mpc/h

SIGNIFICANCIA:
Δχ² = {self.results['significance']['delta_chi2']:.2f}
Nivel σ = {self.results['significance']['sigma_level']:.2f}
ΔAIC = {self.results['significance']['delta_aic']:.2f}
        """
        
        ax4.text(0.05, 0.95, stats_text, transform=ax4.transAxes,
                fontsize=10, verticalalignment='top', fontfamily='monospace')
        
        plt.tight_layout()
        
        # Guardar plot
        plot_path = os.path.join(output_dir, 'rigorous_bao_lss_klein_analysis.png')
        plt.savefig(plot_path, dpi=300, bbox_inches='tight')
        print(f"✓ Plot guardado: {plot_path}")
        plt.show()
        
    def save_results(self, output_dir):
        """Guarda resultados en archivo JSON."""
        
        # Añadir metadatos
        self.results['metadata'] = {
            'analysis_type': 'BAO_LSS_Klein_Rigorous',
            'timestamp': self.analysis_timestamp,
            'data_source': self.data_source,
            'data_type': self.data_type,
            'data_points': len(self.r) if hasattr(self, 'r') else 0,
            'methodology': 'Chi-square minimization with model comparison',
            'software': 'Python scipy.optimize + astropy.cosmology'
        }
        
        # Guardar archivo
        results_path = os.path.join(output_dir, 'rigorous_bao_lss_klein_results.json')
        with open(results_path, 'w') as f:
            json.dump(self.results, f, indent=2, default=str)
            
        print(f"✓ Resultados guardados: {results_path}")
        
    def run_complete_analysis(self, output_dir):
        """Ejecuta análisis completo BAO/LSS Klein."""
        
        print("🌌 INICIANDO ANÁLISIS RIGUROSO BAO/LSS - KLEIN THEORY")
        print("="*60)
        
        # Asegurar directorio de salida
        os.makedirs(output_dir, exist_ok=True)
        
        # Pipeline de análisis
        self.load_bao_lss_data()
        
        if self.fit_bao_models():
            self.calculate_significance()
            self.analyze_bao_scale_shift()
            self.create_diagnostic_plots(output_dir)
            self.save_results(output_dir)
            
            print("\n📋 RESUMEN EJECUTIVO BAO/LSS:")
            print("="*40)
            for interpretation in self.results['significance']['interpretation']:
                print(f"• {interpretation}")
                
            if 'bao_scale_analysis' in self.results:
                bao = self.results['bao_scale_analysis']
                print(f"• Escala Klein R4: {self.results['klein_fit']['parameters']['R4_scale']:.1f} Mpc/h")
                print(f"• Desplazamiento BAO: {bao['shift_klein_percent']:.2f}%")
            
            return True
        else:
            print("✗ Análisis falló en etapa de ajuste")
            return False

def main():
    """Función principal para ejecutar análisis BAO/LSS."""
    
    # Configurar paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = current_dir
    
    # Buscar datos BAO/LSS existentes
    parent_dir = os.path.dirname(current_dir)
    possible_data_files = [
        os.path.join(parent_dir, 'correlation_function.csv'),
        os.path.join(parent_dir, 'bao_data.csv'),
        os.path.join(parent_dir, 'lss_data.csv'),
        os.path.join(parent_dir, 'power_spectrum.csv')
    ]
    
    data_path = None
    for path in possible_data_files:
        if os.path.exists(path):
            data_path = path
            break
    
    # Ejecutar análisis
    analyzer = RigorousBAOLSSAnalysis(data_path=data_path)
    success = analyzer.run_complete_analysis(output_dir)
    
    if success:
        print("\n✅ ANÁLISIS BAO/LSS COMPLETADO EXITOSAMENTE")
    else:
        print("\n❌ ANÁLISIS BAO/LSS FALLÓ")
    
    return success

if __name__ == "__main__":
    main()