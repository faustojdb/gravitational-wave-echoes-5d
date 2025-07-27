#!/usr/bin/env python3
"""
RIGOROUS PTA ANALYSIS - KLEIN THEORY VALIDATION
==============================================

Análisis no sesgado de residuos de timing de pulsares (NANOGrav) para detectar
señales Klein a frecuencias nanohertz, especialmente buscando la frecuencia
universal f₀ = 5.68 Hz predicha por Klein Theory.

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
from scipy.signal import periodogram, welch
import glob
import json
import os
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class RigorousPTAAnalysis:
    """
    Análisis riguroso de datos PTA (Pulsar Timing Array) para efectos Klein.
    Enfoque en detección de periodicidades y análisis espectral sin sesgos.
    """
    
    def __init__(self, data_dir=None):
        self.data_dir = data_dir
        self.results = {}
        self.analysis_timestamp = datetime.now().isoformat()
        self.pulsar_data = {}
        
    def load_nanograv_data(self):
        """Carga datos reales de NANOGrav desde archivos CSV."""
        
        if not self.data_dir or not os.path.exists(self.data_dir):
            print("⚠ Directorio de datos no encontrado, simulando datos sintéticos")
            self._simulate_pta_data()
            return
            
        # Buscar archivos de residuos de timing
        residual_files = glob.glob(os.path.join(self.data_dir, "*_residuals.csv"))
        
        if not residual_files:
            print("⚠ No se encontraron archivos de residuos, simulando datos")
            self._simulate_pta_data()
            return
            
        print(f"📡 Cargando datos de {len(residual_files)} pulsares NANOGrav...")
        
        loaded_pulsars = 0
        for file_path in residual_files:
            try:
                pulsar_name = os.path.basename(file_path).replace('_residuals.csv', '')
                
                df = pd.read_csv(file_path)
                
                # Verificar columnas esperadas (mapear desde formato NANOGrav)
                required_cols = ['time_years', 'residual_us', 'residual_error_us']
                if not all(col in df.columns for col in required_cols):
                    continue
                    
                # Filtrar datos válidos
                mask = (~np.isnan(df['residual_us'])) & (~np.isnan(df['residual_error_us'])) & (df['residual_error_us'] > 0)
                df_clean = df[mask].copy()
                
                if len(df_clean) < 10:  # Mínimo 10 puntos
                    continue
                    
                # Ordenar por tiempo
                df_clean = df_clean.sort_values('time_years')
                
                self.pulsar_data[pulsar_name] = {
                    'time': df_clean['time_years'].values,
                    'residual': df_clean['residual_us'].values,  # En microsegundos
                    'error': df_clean['residual_error_us'].values,
                    'n_points': len(df_clean)
                }
                
                loaded_pulsars += 1
                
            except Exception as e:
                print(f"✗ Error cargando {file_path}: {e}")
                continue
                
        if loaded_pulsars == 0:
            print("⚠ No se pudieron cargar datos válidos, simulando")
            self._simulate_pta_data()
        else:
            print(f"✓ {loaded_pulsars} pulsares cargados exitosamente")
            self.data_source = "nanograv_real_data"
            
    def _simulate_pta_data(self):
        """Simula datos PTA sintéticos para testing."""
        print("🔄 Simulando datos PTA sintéticos...")
        
        # Crear varios pulsares sintéticos
        n_pulsars = 10
        
        for i in range(n_pulsars):
            pulsar_name = f"J{1000+i:04d}+{2000+i:04d}"
            
            # Tiempo en MJD típico de NANOGrav
            n_obs = np.random.randint(50, 200)
            time = np.sort(np.random.uniform(55000, 59000, n_obs))  # MJD
            
            # Residuos base: tendencia polinomial + ruido
            poly_coeffs = np.random.normal(0, 1e-7, 3)
            time_norm = (time - time.mean()) / time.std()
            residual_base = np.polyval(poly_coeffs, time_norm)
            
            # Ruido blanco
            error = np.random.uniform(1e-7, 5e-7, n_obs)
            noise = np.random.normal(0, error)
            
            # Posible señal Klein (con probabilidad 50%)
            if np.random.random() < 0.5:
                # Frecuencia Klein en nHz (f₀ = 5.68 Hz convertido)
                f_klein_nHz = 5.68e9  # 5.68 Hz en nanohertz
                period_years = 1.0 / (f_klein_nHz * 1e-9) / (365.25 * 24 * 3600)
                
                amplitude = np.random.uniform(1e-8, 1e-7)
                phase = np.random.uniform(0, 2*np.pi)
                time_years = (time - time.min()) / 365.25
                
                klein_signal = amplitude * np.sin(2*np.pi * time_years / period_years + phase)
            else:
                klein_signal = 0
                
            residual = residual_base + noise + klein_signal
            
            self.pulsar_data[pulsar_name] = {
                'time': time,
                'residual': residual,
                'error': error,
                'n_points': n_obs
            }
            
        self.data_source = "simulated_pta_data"
        print(f"✓ {len(self.pulsar_data)} pulsares sintéticos creados")
        
    def model_standard_timing(self, params, time):
        """
        Modelo estándar de timing: tendencia polinomial + ruido blanco.
        
        Parámetros:
        -----------
        params : array
            [a0, a1, a2, sigma_white] - coeficientes polinomiales y ruido
        time : array
            Tiempos de observación
        """
        a0, a1, a2, sigma_white = params
        time_norm = (time - time.mean()) / time.std()
        
        return a0 + a1 * time_norm + a2 * time_norm**2
        
    def model_klein_timing(self, params, time):
        """
        Modelo Klein: timing estándar + oscilación a frecuencia Klein.
        
        Parámetros:
        -----------
        params : array  
            [a0, a1, a2, sigma_white, amp_klein, f_klein, phase]
        time : array
            Tiempos de observación
        """
        a0, a1, a2, sigma_white, amp_klein, f_klein, phase = params
        
        # Componente estándar
        standard = self.model_standard_timing([a0, a1, a2, sigma_white], time)
        
        # Componente Klein (f_klein en nanohertz)
        time_seconds = time * 24 * 3600  # MJD a segundos
        klein_component = amp_klein * np.sin(2*np.pi * f_klein * 1e-9 * time_seconds + phase)
        
        return standard + klein_component
        
    def analyze_single_pulsar(self, pulsar_name):
        """Analiza un pulsar individual."""
        
        if pulsar_name not in self.pulsar_data:
            return None
            
        data = self.pulsar_data[pulsar_name]
        time = data['time']
        residual = data['residual']
        error = data['error']
        
        print(f"🔄 Analizando {pulsar_name} ({len(time)} observaciones)...")
        
        result = {'pulsar': pulsar_name}
        
        # Ajuste modelo estándar
        def residuals_standard(params):
            model = self.model_standard_timing(params, time)
            return (residual - model) / error
            
        # Parámetros iniciales estándar
        p0_standard = [0, 0, 0, np.std(residual)]
        
        try:
            fit_standard = least_squares(residuals_standard, p0_standard, 
                                       method='lm', max_nfev=5000)
            
            chi2_standard = np.sum(fit_standard.fun**2)
            dof_standard = len(time) - len(p0_standard)
            chi2_red_standard = chi2_standard / dof_standard
            
            result['standard_fit'] = {
                'parameters': fit_standard.x.tolist(),
                'chi2': chi2_standard,
                'dof': dof_standard,
                'chi2_reduced': chi2_red_standard,
                'success': fit_standard.success
            }
            
        except Exception as e:
            print(f"  ✗ Ajuste estándar falló: {e}")
            return None
            
        # Ajuste modelo Klein
        def residuals_klein(params):
            model = self.model_klein_timing(params, time)
            return (residual - model) / error
            
        # Parámetros iniciales Klein (incluye f₀ = 5.68 Hz = 5.68e9 nHz)
        p0_klein = [0, 0, 0, np.std(residual), 1e-8, 5.68e9, 0]
        
        try:
            fit_klein = least_squares(residuals_klein, p0_klein,
                                    method='lm', max_nfev=5000)
            
            chi2_klein = np.sum(fit_klein.fun**2)
            dof_klein = len(time) - len(p0_klein)
            chi2_red_klein = chi2_klein / dof_klein
            
            result['klein_fit'] = {
                'parameters': fit_klein.x.tolist(),
                'chi2': chi2_klein,
                'dof': dof_klein,
                'chi2_reduced': chi2_red_klein,
                'success': fit_klein.success,
                'f_klein_nHz': fit_klein.x[5],
                'amplitude_klein': fit_klein.x[4]
            }
            
        except Exception as e:
            print(f"  ✗ Ajuste Klein falló: {e}")
            return None
            
        # Significancia
        delta_chi2 = chi2_standard - chi2_klein
        delta_dof = dof_standard - dof_klein
        
        if delta_chi2 > 0:
            p_value = chi2.sf(delta_chi2, delta_dof)
            sigma_level = p_value_to_sigma(p_value) if p_value < 1 and p_value > 0 else 0
        else:
            p_value = 1.0
            sigma_level = 0.0
            
        result['significance'] = {
            'delta_chi2': delta_chi2,
            'p_value': p_value,
            'sigma_level': sigma_level
        }
        
        print(f"  χ²_std/dof = {chi2_red_standard:.3f}, χ²_Klein/dof = {chi2_red_klein:.3f}")
        print(f"  Δχ² = {delta_chi2:.2f}, σ = {sigma_level:.2f}")
        
        return result
        
    def analyze_all_pulsars(self):
        """Analiza todos los pulsares cargados."""
        
        print(f"🔄 Analizando {len(self.pulsar_data)} pulsares...")
        
        individual_results = []
        
        for pulsar_name in self.pulsar_data.keys():
            result = self.analyze_single_pulsar(pulsar_name)
            if result:
                individual_results.append(result)
                
        self.results['individual_pulsars'] = individual_results
        
        # Estadísticas combinadas
        if individual_results:
            sigma_levels = [r['significance']['sigma_level'] for r in individual_results]
            delta_chi2_values = [r['significance']['delta_chi2'] for r in individual_results]
            
            # Estadística combinada simple
            combined_sigma = np.sqrt(np.sum(np.array(sigma_levels)**2))
            
            # Detecciones significativas (≥3σ)
            significant_detections = sum(1 for s in sigma_levels if s >= 3.0)
            
            self.results['combined_statistics'] = {
                'n_pulsars_analyzed': len(individual_results),
                'sigma_levels': sigma_levels,
                'combined_sigma': combined_sigma,
                'significant_detections': significant_detections,
                'detection_rate': significant_detections / len(individual_results),
                'mean_sigma': np.mean(sigma_levels),
                'median_sigma': np.median(sigma_levels)
            }
            
            print(f"📊 {significant_detections}/{len(individual_results)} detecciones ≥3σ")
            print(f"📊 σ combinado = {combined_sigma:.2f}")
            
    def perform_spectral_analysis(self):
        """Realiza análisis espectral de todos los pulsares."""
        
        print("🔄 Realizando análisis espectral...")
        
        spectral_results = []
        
        for pulsar_name, data in self.pulsar_data.items():
            time = data['time']
            residual = data['residual']
            
            # Verificar espaciado temporal regular
            dt = np.median(np.diff(time))
            sampling_rate = 1.0 / (dt * 24 * 3600)  # Hz
            
            try:
                # Análisis espectral usando Welch
                frequencies, psd = welch(residual, fs=sampling_rate, 
                                       nperseg=min(len(residual)//4, 256))
                
                # Buscar pico cerca de f₀ = 5.68 Hz
                f_target = 5.68  # Hz
                freq_tolerance = 0.1  # ±0.1 Hz
                
                mask = (frequencies >= f_target - freq_tolerance) & \
                       (frequencies <= f_target + freq_tolerance)
                
                if np.any(mask):
                    power_at_f0 = np.max(psd[mask])
                    freq_at_max = frequencies[mask][np.argmax(psd[mask])]
                    
                    # Significancia respecto al continuo
                    continuum_power = np.median(psd)
                    snr = power_at_f0 / continuum_power
                    
                    spectral_results.append({
                        'pulsar': pulsar_name,
                        'freq_target': freq_at_max,
                        'power_ratio': snr,
                        'power_at_f0': power_at_f0,
                        'continuum_power': continuum_power
                    })
                    
            except Exception as e:
                print(f"  ✗ Error en análisis espectral de {pulsar_name}: {e}")
                continue
                
        self.results['spectral_analysis'] = spectral_results
        
        if spectral_results:
            power_ratios = [r['power_ratio'] for r in spectral_results]
            print(f"📊 Análisis espectral: {len(spectral_results)} pulsares")
            print(f"📊 S/N promedio en f₀: {np.mean(power_ratios):.2f}")
            
    def create_diagnostic_plots(self, output_dir):
        """Genera plots diagnósticos del análisis PTA."""
        
        if 'individual_pulsars' not in self.results:
            print("✗ No hay resultados para plotting")
            return
            
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        
        # Plot 1: Distribución de significancias
        sigma_levels = self.results['combined_statistics']['sigma_levels']
        
        ax1.hist(sigma_levels, bins=20, alpha=0.7, color='blue', edgecolor='black')
        ax1.axvline(x=3, color='red', linestyle='--', label='3σ threshold')
        ax1.axvline(x=5, color='red', linestyle='-', label='5σ discovery')
        ax1.set_xlabel('Nivel de significancia (σ)')
        ax1.set_ylabel('Número de pulsares')
        ax1.set_title('Distribución de Significancias Klein')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Chi-cuadrado reducido comparación
        chi2_standard = [r['standard_fit']['chi2_reduced'] for r in self.results['individual_pulsars']]
        chi2_klein = [r['klein_fit']['chi2_reduced'] for r in self.results['individual_pulsars']]
        
        ax2.scatter(chi2_standard, chi2_klein, alpha=0.7)
        ax2.plot([0, max(max(chi2_standard), max(chi2_klein))], 
                [0, max(max(chi2_standard), max(chi2_klein))], 
                'k--', alpha=0.5, label='1:1 line')
        ax2.set_xlabel('χ²/dof Estándar')
        ax2.set_ylabel('χ²/dof Klein')
        ax2.set_title('Calidad de Ajuste: Estándar vs Klein')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # Plot 3: Ejemplo de residuos de un pulsar
        if self.pulsar_data:
            example_pulsar = list(self.pulsar_data.keys())[0]
            data = self.pulsar_data[example_pulsar]
            
            ax3.errorbar(data['time'], data['residual'], yerr=data['error'],
                        fmt='o', alpha=0.7, markersize=3)
            ax3.set_xlabel('Tiempo (MJD)')
            ax3.set_ylabel('Residual de timing (s)')
            ax3.set_title(f'Ejemplo: {example_pulsar}')
            ax3.grid(True, alpha=0.3)
        
        # Plot 4: Análisis espectral (si disponible)
        if 'spectral_analysis' in self.results and self.results['spectral_analysis']:
            power_ratios = [r['power_ratio'] for r in self.results['spectral_analysis']]
            
            ax4.hist(power_ratios, bins=15, alpha=0.7, color='green', edgecolor='black')
            ax4.axvline(x=1, color='red', linestyle='--', label='Continuum level')
            ax4.set_xlabel('S/N en f₀ = 5.68 Hz')
            ax4.set_ylabel('Número de pulsares')
            ax4.set_title('Análisis Espectral en f₀ Klein')
            ax4.legend()
            ax4.grid(True, alpha=0.3)
        else:
            ax4.text(0.5, 0.5, 'Análisis espectral\nno disponible', 
                    ha='center', va='center', transform=ax4.transAxes,
                    fontsize=12)
            ax4.set_title('Análisis Espectral')
        
        plt.tight_layout()
        
        # Guardar plot
        plot_path = os.path.join(output_dir, 'rigorous_pta_klein_analysis.png')
        plt.savefig(plot_path, dpi=300, bbox_inches='tight')
        print(f"✓ Plot guardado: {plot_path}")
        plt.show()
        
    def save_results(self, output_dir):
        """Guarda resultados en archivo JSON."""
        
        # Añadir metadatos
        self.results['metadata'] = {
            'analysis_type': 'PTA_Klein_Rigorous',
            'timestamp': self.analysis_timestamp,
            'data_source': self.data_source,
            'n_pulsars': len(self.pulsar_data),
            'klein_frequency_target': 5.68,  # Hz
            'methodology': 'Least squares fitting with likelihood ratio test',
            'software': 'Python scipy.optimize + scipy.signal'
        }
        
        # Guardar archivo
        results_path = os.path.join(output_dir, 'rigorous_pta_klein_results.json')
        with open(results_path, 'w') as f:
            json.dump(self.results, f, indent=2, default=str)
            
        print(f"✓ Resultados guardados: {results_path}")
        
    def run_complete_analysis(self, output_dir):
        """Ejecuta análisis completo PTA Klein."""
        
        print("📡 INICIANDO ANÁLISIS RIGUROSO PTA - KLEIN THEORY")
        print("="*60)
        
        # Asegurar directorio de salida
        os.makedirs(output_dir, exist_ok=True)
        
        # Pipeline de análisis
        self.load_nanograv_data()
        
        if not self.pulsar_data:
            print("✗ No hay datos de pulsares para analizar")
            return False
            
        self.analyze_all_pulsars()
        self.perform_spectral_analysis()
        self.create_diagnostic_plots(output_dir)
        self.save_results(output_dir)
        
        # Resumen ejecutivo
        if 'combined_statistics' in self.results:
            stats = self.results['combined_statistics']
            
            print("\n📋 RESUMEN EJECUTIVO PTA:")
            print("="*40)
            print(f"• Pulsares analizados: {stats['n_pulsars_analyzed']}")
            print(f"• Detecciones ≥3σ: {stats['significant_detections']}")
            print(f"• Tasa detección: {stats['detection_rate']:.1%}")
            print(f"• Significancia combinada: {stats['combined_sigma']:.2f}σ")
            
            if stats['combined_sigma'] >= 3.0:
                print("• RESULTADO: EVIDENCIA SIGNIFICATIVA PARA EFECTOS KLEIN")
            elif stats['combined_sigma'] >= 1.0:
                print("• RESULTADO: EVIDENCIA MARGINAL PARA EFECTOS KLEIN")
            else:
                print("• RESULTADO: NO EVIDENCIA SIGNIFICATIVA")
        
        return True

def main():
    """Función principal para ejecutar análisis PTA."""
    
    # Configurar paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = current_dir
    
    # Buscar directorio de datos NANOGrav
    parent_dir = os.path.dirname(current_dir)
    possible_data_dirs = [
        os.path.join(parent_dir, 'nanograv_15yr_data', 'timing_residuals'),
        os.path.join(parent_dir, 'timing_residuals'),
        os.path.join(parent_dir, 'nanograv_data')
    ]
    
    data_dir = None
    for path in possible_data_dirs:
        if os.path.exists(path):
            data_dir = path
            break
    
    # Ejecutar análisis
    analyzer = RigorousPTAAnalysis(data_dir=data_dir)
    success = analyzer.run_complete_analysis(output_dir)
    
    if success:
        print("\n✅ ANÁLISIS PTA COMPLETADO EXITOSAMENTE")
    else:
        print("\n❌ ANÁLISIS PTA FALLÓ")
    
    return success

if __name__ == "__main__":
    main()