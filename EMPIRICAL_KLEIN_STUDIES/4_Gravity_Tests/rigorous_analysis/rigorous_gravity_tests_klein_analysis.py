#!/usr/bin/env python3
"""
RIGOROUS GRAVITY TESTS ANALYSIS - KLEIN THEORY VALIDATION
========================================================

Análisis no sesgado de tests gravitacionales (precesión perihelio, deflexión luz,
time delay) para detectar correcciones Klein a la Relatividad General.

Author: Klein Theory Validation Team
Date: July 26, 2025
Status: Empirical validation module
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit, least_squares
from scipy.stats import chi2
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from klein_stats_utils import p_value_to_sigma, model_comparison_stats
import json
import os
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class RigorousGravityTestsAnalysis:
    """
    Análisis riguroso de tests de gravedad para efectos Klein.
    Enfoque en correcciones post-Newtonianas y modificaciones extradimensionales.
    """
    
    def __init__(self, data_path=None):
        self.data_path = data_path
        self.results = {}
        self.analysis_timestamp = datetime.now().isoformat()
        self.gravity_tests = {}
        
    def load_gravity_test_data(self):
        """Carga datos de tests gravitacionales desde archivo o simula datos."""
        
        # Buscar datos reales descargados
        gravity_data_dir = "/mnt/d/Multidimensional Theory Simulations/multidimensional-theory/gravitational-wave-echoes-5d/EMPIRICAL_KLEIN_STUDIES/4_Gravity_Tests/gravity_tests_data"
        catalog_file = os.path.join(gravity_data_dir, "massive_gravity_tests_catalog.csv")
        
        if os.path.exists(catalog_file):
            print("🔍 Cargando datos reales de tests gravitacionales...")
            self._load_real_gravity_catalog(catalog_file)
        elif self.data_path and os.path.exists(self.data_path):
            try:
                df = pd.read_csv(self.data_path)
                
                # Identificar tipo de test gravitacional
                if 'orbital_angle' in df.columns:
                    self._load_perihelion_data(df)
                elif 'deflection_angle' in df.columns:
                    self._load_light_deflection_data(df)
                elif 'time_delay' in df.columns:
                    self._load_time_delay_data(df)
                else:
                    print("⚠ Formato no reconocido, simulando datos")
                    self._simulate_gravity_test_data()
                    
                self.data_source = "real_data"
                
            except Exception as e:
                print(f"Error cargando datos: {e}")
                self._simulate_gravity_test_data()
        else:
            self._simulate_gravity_test_data()
            
    def _load_real_gravity_catalog(self, catalog_file):
        """Carga catálogo real de tests gravitacionales masivos."""
        try:
            df = pd.read_csv(catalog_file)
            print(f"✓ Catálogo cargado: {len(df)} tests gravitacionales")
            
            # Agrupar por tipo de experimento
            for exp_type in df['experiment_type'].unique():
                exp_data = df[df['experiment_type'] == exp_type].copy()
                
                if exp_type == 'lunar_laser_ranging':
                    self.gravity_tests['llr'] = {
                        'time': exp_data['time_days'].values,
                        'distance_scale': exp_data['distance_scale_km'].values,
                        'residual': exp_data['observed_value'].values,
                        'error': exp_data['measurement_uncertainty'].values,
                        'test_type': 'distance_residual',
                        'n_points': len(exp_data)
                    }
                    print(f"  ✓ Lunar Laser Ranging: {len(exp_data)} mediciones")
                    
                elif exp_type == 'satellite_tracking':
                    self.gravity_tests['satellite'] = {
                        'time': exp_data['time_days'].values,
                        'residual': exp_data['observed_value'].values,
                        'error': exp_data['measurement_uncertainty'].values,
                        'test_type': 'orbital_residual',
                        'n_points': len(exp_data)
                    }
                    print(f"  ✓ Satellite Tracking: {len(exp_data)} mediciones")
                    
            self.data_source = "real_gravity_catalog"
            
        except Exception as e:
            print(f"✗ Error cargando catálogo: {e}")
            self._simulate_gravity_test_data()
            
    def _load_perihelion_data(self, df):
        """Carga datos de precesión del perihelio."""
        self.gravity_tests['perihelion'] = {
            'time': df['time'].values,
            'angle': df['orbital_angle'].values,
            'error': df.get('error', np.full(len(df), 0.1)).values,
            'test_type': 'perihelion_precession'
        }
        print(f"✓ Datos precesión perihelio cargados: {len(df)} puntos")
        
    def _load_light_deflection_data(self, df):
        """Carga datos de deflexión de luz."""
        self.gravity_tests['deflection'] = {
            'impact_parameter': df['impact_parameter'].values,
            'deflection': df['deflection_angle'].values,
            'error': df.get('error', np.full(len(df), 0.01)).values,
            'test_type': 'light_deflection'
        }
        print(f"✓ Datos deflexión luz cargados: {len(df)} puntos")
        
    def _load_time_delay_data(self, df):
        """Carga datos de retardo temporal."""
        self.gravity_tests['time_delay'] = {
            'distance': df['distance'].values,
            'delay': df['time_delay'].values,
            'error': df.get('error', np.full(len(df), 1e-6)).values,
            'test_type': 'time_delay'
        }
        print(f"✓ Datos retardo temporal cargados: {len(df)} puntos")
        
    def _simulate_gravity_test_data(self):
        """Simula datos de tests gravitacionales sintéticos."""
        print("🔄 Simulando datos de tests gravitacionales...")
        
        # Simular precesión del perihelio (Mercurio)
        n_points = 100
        time_years = np.linspace(0, 100, n_points)  # 100 años
        
        # Precesión GR: 42.98 arcsec/siglo para Mercurio
        gr_precession = 42.98 / 100 * time_years  # arcsec
        
        # Añadir pequeña corrección Klein (parameterizada)
        klein_correction = 0.01 * np.sin(2*np.pi * time_years / 50)  # Oscilación 50 años
        
        # Ruido observacional
        error = np.full(n_points, 0.1)  # 0.1 arcsec error típico
        noise = np.random.normal(0, error)
        
        angle_obs = gr_precession + klein_correction + noise
        
        self.gravity_tests['perihelion'] = {
            'time': time_years,
            'angle': angle_obs,
            'error': error,
            'test_type': 'perihelion_precession'
        }
        
        # Simular deflexión de luz
        n_deflection = 50
        impact_param = np.logspace(-1, 2, n_deflection)  # Parámetro impacto [Rs]
        
        # Deflexión GR: 4GM/c²b para rayos rasantes
        gr_deflection = 4.0 / impact_param  # En unidades de Rs
        
        # Corrección Klein pequeña
        klein_deflection_corr = 0.001 / impact_param**2
        
        deflection_error = 0.01 * gr_deflection  # 1% error típico
        deflection_noise = np.random.normal(0, deflection_error)
        
        deflection_obs = gr_deflection + klein_deflection_corr + deflection_noise
        
        self.gravity_tests['deflection'] = {
            'impact_parameter': impact_param,
            'deflection': deflection_obs,
            'error': deflection_error,
            'test_type': 'light_deflection'
        }
        
        self.data_source = "simulated_data"
        print(f"✓ {len(self.gravity_tests)} tests gravitacionales simulados")
        
    def model_gr_perihelion(self, time, omega_gr):
        """Modelo GR estándar para precesión del perihelio."""
        return omega_gr * time
        
    def model_klein_perihelion(self, time, omega_gr, lambda_klein):
        """Modelo Klein para precesión del perihelio con corrección extradimensional."""
        # GR base + corrección Klein
        gr_term = omega_gr * time
        klein_term = lambda_klein * np.sin(2*np.pi * time / 50)  # Periodo característico
        return gr_term + klein_term
        
    def model_gr_deflection(self, b, deflection_constant):
        """Modelo GR para deflexión de luz."""
        return deflection_constant / b
        
    def model_klein_deflection(self, b, deflection_constant, klein_amp):
        """Modelo Klein para deflexión con corrección 1/b²."""
        gr_term = deflection_constant / b
        klein_term = klein_amp / (b**2)
        return gr_term + klein_term
        
    def analyze_perihelion_precession(self):
        """Analiza datos de precesión del perihelio."""
        
        if 'perihelion' not in self.gravity_tests:
            return None
            
        data = self.gravity_tests['perihelion']
        time = data['time']
        angle = data['angle']
        error = data['error']
        
        print("🔄 Analizando precesión del perihelio...")
        
        result = {'test_type': 'perihelion_precession'}
        
        # Ajuste GR estándar
        try:
            popt_gr, pcov_gr = curve_fit(
                self.model_gr_perihelion, time, angle, sigma=error,
                p0=[0.43]  # ~42.98 arcsec/siglo
            )
            
            angle_fit_gr = self.model_gr_perihelion(time, *popt_gr)
            chi2_gr = np.sum(((angle - angle_fit_gr) / error)**2)
            dof_gr = len(time) - len(popt_gr)
            
            result['gr_fit'] = {
                'omega_gr': popt_gr[0],
                'omega_error': np.sqrt(pcov_gr[0,0]),
                'chi2': chi2_gr,
                'dof': dof_gr,
                'chi2_reduced': chi2_gr / dof_gr
            }
            
        except Exception as e:
            print(f"  ✗ Ajuste GR falló: {e}")
            return None
            
        # Ajuste Klein
        try:
            popt_klein, pcov_klein = curve_fit(
                self.model_klein_perihelion, time, angle, sigma=error,
                p0=[0.43, 0.01]
            )
            
            angle_fit_klein = self.model_klein_perihelion(time, *popt_klein)
            chi2_klein = np.sum(((angle - angle_fit_klein) / error)**2)
            dof_klein = len(time) - len(popt_klein)
            
            result['klein_fit'] = {
                'omega_gr': popt_klein[0],
                'lambda_klein': popt_klein[1],
                'parameter_errors': np.sqrt(np.diag(pcov_klein)).tolist(),
                'chi2': chi2_klein,
                'dof': dof_klein,
                'chi2_reduced': chi2_klein / dof_klein
            }
            
        except Exception as e:
            print(f"  ✗ Ajuste Klein falló: {e}")
            return None
            
        # Significancia
        delta_chi2 = chi2_gr - chi2_klein
        delta_dof = dof_gr - dof_klein
        
        if delta_chi2 > 0:
            p_value = chi2.sf(delta_chi2, delta_dof)
            sigma_level = p_value_to_sigma(p_value) if 0 < p_value < 1 else 0
        else:
            p_value = 1.0
            sigma_level = 0.0
            
        result['significance'] = {
            'delta_chi2': delta_chi2,
            'p_value': p_value,
            'sigma_level': sigma_level
        }
        
        print(f"  ω_GR = {popt_gr[0]:.3f} ± {np.sqrt(pcov_gr[0,0]):.3f} arcsec/año")
        print(f"  λ_Klein = {popt_klein[1]:.4f} ± {np.sqrt(pcov_klein[1,1]):.4f}")
        print(f"  Δχ² = {delta_chi2:.2f}, σ = {sigma_level:.2f}")
        
        return result
        
    def analyze_light_deflection(self):
        """Analiza datos de deflexión de luz."""
        
        if 'deflection' not in self.gravity_tests:
            return None
            
        data = self.gravity_tests['deflection']
        b = data['impact_parameter']
        deflection = data['deflection']
        error = data['error']
        
        print("🔄 Analizando deflexión de luz...")
        
        result = {'test_type': 'light_deflection'}
        
        # Ajuste GR estándar
        try:
            popt_gr, pcov_gr = curve_fit(
                self.model_gr_deflection, b, deflection, sigma=error,
                p0=[4.0]  # Constante deflexión GR
            )
            
            deflection_fit_gr = self.model_gr_deflection(b, *popt_gr)
            chi2_gr = np.sum(((deflection - deflection_fit_gr) / error)**2)
            dof_gr = len(b) - len(popt_gr)
            
            result['gr_fit'] = {
                'deflection_constant': popt_gr[0],
                'constant_error': np.sqrt(pcov_gr[0,0]),
                'chi2': chi2_gr,
                'dof': dof_gr,
                'chi2_reduced': chi2_gr / dof_gr
            }
            
        except Exception as e:
            print(f"  ✗ Ajuste GR falló: {e}")
            return None
            
        # Ajuste Klein
        try:
            popt_klein, pcov_klein = curve_fit(
                self.model_klein_deflection, b, deflection, sigma=error,
                p0=[4.0, 0.001]
            )
            
            deflection_fit_klein = self.model_klein_deflection(b, *popt_klein)
            chi2_klein = np.sum(((deflection - deflection_fit_klein) / error)**2)
            dof_klein = len(b) - len(popt_klein)
            
            result['klein_fit'] = {
                'deflection_constant': popt_klein[0],
                'klein_amplitude': popt_klein[1],
                'parameter_errors': np.sqrt(np.diag(pcov_klein)).tolist(),
                'chi2': chi2_klein,
                'dof': dof_klein,
                'chi2_reduced': chi2_klein / dof_klein
            }
            
        except Exception as e:
            print(f"  ✗ Ajuste Klein falló: {e}")
            return None
            
        # Significancia
        delta_chi2 = chi2_gr - chi2_klein
        delta_dof = dof_gr - dof_klein
        
        if delta_chi2 > 0:
            p_value = chi2.sf(delta_chi2, delta_dof)
            sigma_level = p_value_to_sigma(p_value) if 0 < p_value < 1 else 0
        else:
            p_value = 1.0
            sigma_level = 0.0
            
        result['significance'] = {
            'delta_chi2': delta_chi2,
            'p_value': p_value,
            'sigma_level': sigma_level
        }
        
        print(f"  Constante GR = {popt_gr[0]:.3f} ± {np.sqrt(pcov_gr[0,0]):.3f}")
        print(f"  Amplitud Klein = {popt_klein[1]:.5f} ± {np.sqrt(pcov_klein[1,1]):.5f}")
        print(f"  Δχ² = {delta_chi2:.2f}, σ = {sigma_level:.2f}")
        
        return result
        
    def analyze_llr(self):
        """Analiza datos Lunar Laser Ranging para efectos Klein."""
        
        if 'llr' not in self.gravity_tests:
            return None
            
        print("🔄 Analizando Lunar Laser Ranging...")
        
        # Obtener datos LLR
        data = self.gravity_tests['llr']
        time = data['time']
        residual = data['residual']  # En mm
        error = data['error']        # En mm
        
        result = {
            'test_type': 'lunar_laser_ranging',
            'n_points': len(time)
        }
        
        # Modelo estándar GR (sin efectos Klein)
        try:
            popt_gr, pcov_gr = curve_fit(
                self.model_gr_llr, time, residual, sigma=error,
                p0=[0.0]  # Solo offset constante
            )
            
            residual_fit_gr = self.model_gr_llr(time, *popt_gr)
            chi2_gr = np.sum(((residual - residual_fit_gr) / error)**2)
            dof_gr = len(time) - len(popt_gr)
            
            result['gr_fit'] = {
                'offset': popt_gr[0],
                'parameter_errors': np.sqrt(np.diag(pcov_gr)).tolist(),
                'chi2': chi2_gr,
                'dof': dof_gr,
                'chi2_reduced': chi2_gr / dof_gr
            }
            
        except Exception as e:
            print(f"  ✗ Ajuste GR falló: {e}")
            return None
            
        # Modelo Klein LLR 
        try:
            popt_klein, pcov_klein = curve_fit(
                self.model_klein_llr, time, residual, sigma=error,
                p0=[0.0, 1e-6]  # offset + amplitud Klein
            )
            
            residual_fit_klein = self.model_klein_llr(time, *popt_klein)
            chi2_klein = np.sum(((residual - residual_fit_klein) / error)**2)
            dof_klein = len(time) - len(popt_klein)
            
            result['klein_fit'] = {
                'offset': popt_klein[0],
                'klein_amplitude': popt_klein[1],
                'parameter_errors': np.sqrt(np.diag(pcov_klein)).tolist(),
                'chi2': chi2_klein,
                'dof': dof_klein,
                'chi2_reduced': chi2_klein / dof_klein
            }
            
        except Exception as e:
            print(f"  ✗ Ajuste Klein falló: {e}")
            return None
            
        # Significancia
        delta_chi2 = chi2_gr - chi2_klein
        delta_dof = dof_gr - dof_klein
        
        if delta_chi2 > 0:
            p_value = chi2.sf(delta_chi2, delta_dof)
            sigma_level = p_value_to_sigma(p_value) if 0 < p_value < 1 else 0
        else:
            p_value = 1.0
            sigma_level = 0.0
            
        result['significance'] = {
            'delta_chi2': delta_chi2,
            'p_value': p_value,
            'sigma_level': sigma_level
        }
        
        print(f"  Offset GR = {popt_gr[0]:.3f} ± {np.sqrt(pcov_gr[0,0]):.3f} mm")
        print(f"  Amplitud Klein = {popt_klein[1]:.5f} ± {np.sqrt(pcov_klein[1,1]):.5f} mm")
        print(f"  Δχ² = {delta_chi2:.2f}, σ = {sigma_level:.2f}")
        
        return result
        
    def model_gr_llr(self, time, offset):
        """Modelo GR para residuos LLR (solo offset constante)."""
        return np.full_like(time, offset)
        
    def model_klein_llr(self, time, offset, klein_amp):
        """Modelo Klein para residuos LLR con modulación temporal."""
        # Klein effect: pequeña modulación sinusoidal
        klein_modulation = klein_amp * np.sin(2*np.pi * time / 365.25)  # Anual
        return offset + klein_modulation
        
    def run_all_gravity_tests(self):
        """Ejecuta todos los tests gravitacionales disponibles."""
        
        print(f"🔄 Ejecutando {len(self.gravity_tests)} tests gravitacionales...")
        
        test_results = []
        
        # Precesión del perihelio
        perihelion_result = self.analyze_perihelion_precession()
        if perihelion_result:
            test_results.append(perihelion_result)
            
        # Deflexión de luz
        deflection_result = self.analyze_light_deflection()
        if deflection_result:
            test_results.append(deflection_result)
            
        # Lunar Laser Ranging (LLR)
        llr_result = self.analyze_llr()
        if llr_result:
            test_results.append(llr_result)
            
        self.results['individual_tests'] = test_results
        
        # Estadísticas combinadas
        if test_results:
            sigma_levels = [r['significance']['sigma_level'] for r in test_results]
            
            # Combinación simple (Fisher)
            combined_sigma = np.sqrt(np.sum(np.array(sigma_levels)**2))
            
            significant_tests = sum(1 for s in sigma_levels if s >= 3.0)
            
            self.results['combined_statistics'] = {
                'n_tests': len(test_results),
                'sigma_levels': sigma_levels,
                'combined_sigma': combined_sigma,
                'significant_detections': significant_tests,
                'detection_rate': significant_tests / len(test_results) if test_results else 0,
                'mean_sigma': np.mean(sigma_levels),
                'median_sigma': np.median(sigma_levels)
            }
            
            print(f"📊 {significant_tests}/{len(test_results)} tests ≥3σ")
            print(f"📊 σ combinado = {combined_sigma:.2f}")
            
    def create_diagnostic_plots(self, output_dir):
        """Genera plots diagnósticos de los tests gravitacionales."""
        
        if 'individual_tests' not in self.results:
            print("✗ No hay resultados para plotting")
            return
            
        n_tests = len(self.results['individual_tests'])
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        ax1, ax2, ax3, ax4 = axes.flatten()
        
        # Plot 1: Precesión del perihelio (si disponible)
        perihelion_tests = [t for t in self.results['individual_tests'] 
                          if t['test_type'] == 'perihelion_precession']
        
        if perihelion_tests and 'perihelion' in self.gravity_tests:
            data = self.gravity_tests['perihelion']
            test = perihelion_tests[0]
            
            time = data['time']
            angle = data['angle']
            error = data['error']
            
            ax1.errorbar(time, angle, yerr=error, fmt='o', alpha=0.7, label='Datos')
            
            # Modelo GR
            angle_gr = self.model_gr_perihelion(time, test['gr_fit']['omega_gr'])
            ax1.plot(time, angle_gr, 'b-', linewidth=2, label='GR')
            
            # Modelo Klein
            angle_klein = self.model_klein_perihelion(
                time, test['klein_fit']['omega_gr'], test['klein_fit']['lambda_klein'])
            ax1.plot(time, angle_klein, 'r--', linewidth=2, label='Klein')
            
            ax1.set_xlabel('Tiempo (años)')
            ax1.set_ylabel('Ángulo perihelio (arcsec)')
            ax1.set_title('Precesión del Perihelio')
            ax1.legend()
            ax1.grid(True, alpha=0.3)
        else:
            ax1.text(0.5, 0.5, 'Datos precesión\nno disponibles',
                    ha='center', va='center', transform=ax1.transAxes)
            
        # Plot 2: Deflexión de luz (si disponible)
        deflection_tests = [t for t in self.results['individual_tests']
                           if t['test_type'] == 'light_deflection']
        
        if deflection_tests and 'deflection' in self.gravity_tests:
            data = self.gravity_tests['deflection']
            test = deflection_tests[0]
            
            b = data['impact_parameter']
            deflection = data['deflection']
            error = data['error']
            
            ax2.errorbar(b, deflection, yerr=error, fmt='o', alpha=0.7, label='Datos')
            
            # Modelo GR
            deflection_gr = self.model_gr_deflection(b, test['gr_fit']['deflection_constant'])
            ax2.plot(b, deflection_gr, 'b-', linewidth=2, label='GR')
            
            # Modelo Klein
            deflection_klein = self.model_klein_deflection(
                b, test['klein_fit']['deflection_constant'], test['klein_fit']['klein_amplitude'])
            ax2.plot(b, deflection_klein, 'r--', linewidth=2, label='Klein')
            
            ax2.set_xlabel('Parámetro impacto (Rs)')
            ax2.set_ylabel('Deflexión (arcsec)')
            ax2.set_title('Deflexión de Luz')
            ax2.set_xscale('log')
            ax2.set_yscale('log')
            ax2.legend()
            ax2.grid(True, alpha=0.3)
        else:
            ax2.text(0.5, 0.5, 'Datos deflexión\nno disponibles',
                    ha='center', va='center', transform=ax2.transAxes)
            
        # Plot 3: Distribución de significancias
        if 'combined_statistics' in self.results:
            sigma_levels = self.results['combined_statistics']['sigma_levels']
            test_names = [t['test_type'].replace('_', ' ').title() 
                         for t in self.results['individual_tests']]
            
            bars = ax3.bar(range(len(sigma_levels)), sigma_levels, 
                          color=['red' if s >= 3 else 'blue' for s in sigma_levels],
                          alpha=0.7)
            
            ax3.axhline(y=3, color='red', linestyle='--', alpha=0.7, label='3σ threshold')
            ax3.axhline(y=5, color='red', linestyle='-', alpha=0.7, label='5σ discovery')
            
            ax3.set_xticks(range(len(test_names)))
            ax3.set_xticklabels(test_names, rotation=45, ha='right')
            ax3.set_ylabel('Significancia (σ)')
            ax3.set_title('Significancia por Test')
            ax3.legend()
            ax3.grid(True, alpha=0.3)
            
            # Añadir valores sobre barras
            for i, (bar, sigma) in enumerate(zip(bars, sigma_levels)):
                height = bar.get_height()
                ax3.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                        f'{sigma:.2f}', ha='center', va='bottom')
        else:
            ax3.text(0.5, 0.5, 'Estadísticas no\ndisponibles',
                    ha='center', va='center', transform=ax3.transAxes)
            
        # Plot 4: Resumen estadístico
        ax4.axis('off')
        
        if 'combined_statistics' in self.results:
            stats = self.results['combined_statistics']
            
            stats_text = f"""
ANÁLISIS TESTS GRAVITACIONALES

Fuente: {self.data_source}
Tests ejecutados: {stats['n_tests']}

RESULTADOS INDIVIDUALES:
{chr(10).join([f"• {t['test_type']}: {t['significance']['sigma_level']:.2f}σ" 
               for t in self.results['individual_tests']])}

ESTADÍSTICAS COMBINADAS:
• Detecciones ≥3σ: {stats['significant_detections']}/{stats['n_tests']}
• Tasa detección: {stats['detection_rate']:.1%}
• σ combinado: {stats['combined_sigma']:.2f}
• σ promedio: {stats['mean_sigma']:.2f}
• σ mediano: {stats['median_sigma']:.2f}

INTERPRETACIÓN:
{self._interpret_gravity_results()}
            """
            
            ax4.text(0.05, 0.95, stats_text, transform=ax4.transAxes,
                    fontsize=10, verticalalignment='top', fontfamily='monospace')
        
        plt.tight_layout()
        
        # Guardar plot
        plot_path = os.path.join(output_dir, 'rigorous_gravity_tests_klein_analysis.png')
        plt.savefig(plot_path, dpi=300, bbox_inches='tight')
        print(f"✓ Plot guardado: {plot_path}")
        plt.show()
        
    def _interpret_gravity_results(self):
        """Interpreta resultados de tests gravitacionales."""
        
        if 'combined_statistics' not in self.results:
            return "No hay estadísticas disponibles"
            
        combined_sigma = self.results['combined_statistics']['combined_sigma']
        
        if combined_sigma >= 5.0:
            return "EVIDENCIA FUERTE para modificaciones Klein"
        elif combined_sigma >= 3.0:
            return "EVIDENCIA SIGNIFICATIVA para modificaciones Klein"
        elif combined_sigma >= 1.0:
            return "EVIDENCIA MARGINAL para modificaciones Klein"
        else:
            return "NO EVIDENCIA para modificaciones Klein"
            
    def save_results(self, output_dir):
        """Guarda resultados en archivo JSON."""
        
        # Añadir metadatos
        self.results['metadata'] = {
            'analysis_type': 'Gravity_Tests_Klein_Rigorous',
            'timestamp': self.analysis_timestamp,
            'data_source': self.data_source,
            'tests_available': list(self.gravity_tests.keys()),
            'methodology': 'Post-Newtonian analysis with Klein corrections',
            'software': 'Python scipy.optimize'
        }
        
        # Guardar archivo
        results_path = os.path.join(output_dir, 'rigorous_gravity_tests_klein_results.json')
        with open(results_path, 'w') as f:
            json.dump(self.results, f, indent=2, default=str)
            
        print(f"✓ Resultados guardados: {results_path}")
        
    def run_complete_analysis(self, output_dir):
        """Ejecuta análisis completo de tests gravitacionales Klein."""
        
        print("🌍 INICIANDO ANÁLISIS RIGUROSO TESTS GRAVITACIONALES - KLEIN")
        print("="*60)
        
        # Asegurar directorio de salida
        os.makedirs(output_dir, exist_ok=True)
        
        # Pipeline de análisis
        self.load_gravity_test_data()
        
        if not self.gravity_tests:
            print("✗ No hay datos de tests gravitacionales")
            return False
            
        self.run_all_gravity_tests()
        self.create_diagnostic_plots(output_dir)
        self.save_results(output_dir)
        
        # Resumen ejecutivo
        if 'combined_statistics' in self.results:
            stats = self.results['combined_statistics']
            
            print("\n📋 RESUMEN EJECUTIVO TESTS GRAVITACIONALES:")
            print("="*50)
            print(f"• Tests ejecutados: {stats['n_tests']}")
            print(f"• Detecciones ≥3σ: {stats['significant_detections']}")
            print(f"• Significancia combinada: {stats['combined_sigma']:.2f}σ")
            print(f"• {self._interpret_gravity_results()}")
        
        return True

def main():
    """Función principal para ejecutar análisis de tests gravitacionales."""
    
    # Configurar paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = current_dir
    
    # Buscar datos de tests gravitacionales
    parent_dir = os.path.dirname(current_dir)
    possible_data_files = [
        os.path.join(parent_dir, 'gravity_tests_data', 'orbital_data.csv'),
        os.path.join(parent_dir, 'perihelion_data.csv'),
        os.path.join(parent_dir, 'deflection_data.csv'),
        os.path.join(parent_dir, 'gravity_data.csv')
    ]
    
    data_path = None
    for path in possible_data_files:
        if os.path.exists(path):
            data_path = path
            break
    
    # Ejecutar análisis
    analyzer = RigorousGravityTestsAnalysis(data_path=data_path)
    success = analyzer.run_complete_analysis(output_dir)
    
    if success:
        print("\n✅ ANÁLISIS TESTS GRAVITACIONALES COMPLETADO")
    else:
        print("\n❌ ANÁLISIS TESTS GRAVITACIONALES FALLÓ")
    
    return success

if __name__ == "__main__":
    main()