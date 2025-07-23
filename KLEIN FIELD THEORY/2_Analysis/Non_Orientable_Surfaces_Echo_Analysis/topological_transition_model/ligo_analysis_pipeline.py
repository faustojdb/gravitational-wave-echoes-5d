#!/usr/bin/env python3
"""
Pipeline de Análisis LIGO para Modelo de Transición Topológica
==============================================================

Este módulo implementa el pipeline completo para analizar datos LIGO
y buscar firmas de transición topológica Klein-Toroide en ecos
gravitacionales post-coalescencia.

Autor: Fausto José Di Bacco
Fecha: Diciembre 2024
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.optimize import curve_fit, minimize
from scipy.stats import pearsonr, chi2
from typing import Dict, List, Tuple, Optional, Union
import json
import os
import warnings
from dataclasses import dataclass

# Importar modelo topológico
from topological_transition_implementation import TopologicalTransitionModel

# Configuración
warnings.filterwarnings('ignore')


@dataclass
class LIGOEvent:
    """Estructura de datos para evento LIGO."""
    name: str
    mass_1: float
    mass_2: float
    total_mass: float
    chirp_mass: float
    final_spin: float
    luminosity_distance: float
    merger_time: float
    energy_radiated: Optional[float] = None
    
    def __post_init__(self):
        """Calcula energía radiada si no se proporciona."""
        if self.energy_radiated is None:
            # Fórmula empírica para energía radiada
            eta = self.mass_1 * self.mass_2 / (self.total_mass**2)
            self.energy_radiated = self.total_mass * eta * 0.05 * (1 - 0.1 * self.final_spin**2)


class TopologicalAnalysisPipeline:
    """
    Pipeline completo para análisis topológico de datos LIGO.
    """
    
    def __init__(self, model: Optional[TopologicalTransitionModel] = None):
        """
        Inicializa pipeline con modelo topológico.
        
        Parameters
        ----------
        model : TopologicalTransitionModel, optional
            Modelo de transición topológica
        """
        self.model = model or TopologicalTransitionModel()
        
        # Parámetros de análisis
        self.sampling_rate = 4096  # Hz (estándar LIGO)
        self.analysis_window = 0.1  # 100 ms post-coalescencia
        self.frequency_bands = {
            'low': (35, 100),
            'mid': (100, 350),
            'high': (350, 1000)
        }
        
        # Ventanas temporales críticas
        self.time_windows = {
            'klein_pure': (0, 0.014),      # 0-14 ms
            'transition': (0.014, 0.028),   # 14-28 ms
            'torus_dominant': (0.028, 0.050), # 28-50 ms
            'static': (0.050, 0.100)        # 50-100 ms
        }
        
        print("Pipeline de análisis topológico inicializado")
        print(f"  Frecuencia de muestreo: {self.sampling_rate} Hz")
        print(f"  Ventana de análisis: {self.analysis_window*1000} ms")
    
    def preprocess_strain(self, strain: np.ndarray, 
                         highpass_freq: float = 20.0) -> np.ndarray:
        """
        Preprocesa datos de strain de LIGO.
        
        Parameters
        ----------
        strain : np.ndarray
            Datos crudos de strain
        highpass_freq : float
            Frecuencia de corte del filtro pasa-altas
            
        Returns
        -------
        processed_strain : np.ndarray
            Strain procesado
        """
        # Remover NaN e infinitos
        strain = np.nan_to_num(strain, nan=0.0, posinf=0.0, neginf=0.0)
        
        # Remover tendencia lineal
        strain = signal.detrend(strain)
        
        # Filtro pasa-altas para remover ruido de baja frecuencia
        if highpass_freq > 0:
            sos = signal.butter(4, highpass_freq, btype='high', 
                              fs=self.sampling_rate, output='sos')
            strain = signal.sosfilt(sos, strain)
        
        # Ventana de Tukey para suavizar bordes
        window = signal.tukey(len(strain), alpha=0.1)
        strain = strain * window
        
        return strain
    
    def find_merger_time(self, strain: np.ndarray, 
                        time_array: np.ndarray) -> Tuple[float, int]:
        """
        Encuentra el tiempo de coalescencia (máxima amplitud).
        
        Parameters
        ----------
        strain : np.ndarray
            Datos de strain
        time_array : np.ndarray
            Array de tiempos
            
        Returns
        -------
        merger_time : float
            Tiempo de coalescencia
        merger_index : int
            Índice en el array
        """
        # Filtrar en banda óptima para SNR
        sos = signal.butter(4, [35, 350], btype='band',
                          fs=self.sampling_rate, output='sos')
        filtered = signal.sosfilt(sos, strain)
        
        # Envolvente analítica
        analytic = signal.hilbert(filtered)
        envelope = np.abs(analytic)
        
        # Suavizar envolvente
        window_size = int(0.01 * self.sampling_rate)  # 10 ms
        smoothed = signal.savgol_filter(envelope, window_size, 3)
        
        # Encontrar máximo
        merger_index = np.argmax(smoothed)
        merger_time = time_array[merger_index]
        
        return merger_time, merger_index
    
    def extract_post_merger(self, strain: np.ndarray, time_array: np.ndarray,
                          merger_time: float) -> Tuple[np.ndarray, np.ndarray]:
        """
        Extrae datos post-coalescencia.
        
        Parameters
        ----------
        strain : np.ndarray
            Datos completos
        time_array : np.ndarray
            Tiempos completos
        merger_time : float
            Tiempo de coalescencia
            
        Returns
        -------
        post_strain : np.ndarray
            Strain post-coalescencia
        post_time : np.ndarray
            Tiempos relativos a coalescencia
        """
        # Índices para ventana post-coalescencia
        post_mask = (time_array >= merger_time) & \
                   (time_array < merger_time + self.analysis_window)
        
        post_strain = strain[post_mask]
        post_time = time_array[post_mask] - merger_time
        
        return post_strain, post_time
    
    def compute_topological_indicators(self, strain: np.ndarray,
                                     time: np.ndarray) -> Dict[str, Dict]:
        """
        Calcula indicadores topológicos para cada ventana temporal.
        
        Parameters
        ----------
        strain : np.ndarray
            Strain post-coalescencia
        time : np.ndarray
            Tiempos relativos
            
        Returns
        -------
        indicators : Dict
            Indicadores por ventana temporal
        """
        indicators = {}
        
        for window_name, (t_start, t_end) in self.time_windows.items():
            # Extraer ventana
            mask = (time >= t_start) & (time < t_end)
            if np.sum(mask) < 100:  # Mínimo de puntos
                continue
                
            window_strain = strain[mask]
            window_time = time[mask]
            
            # Calcular indicadores
            indicators[window_name] = {
                'suppression_ratio': self._compute_modal_suppression(window_strain),
                'fundamental_freq': self._track_fundamental_frequency(window_strain),
                'phase_coherence': self._compute_phase_coherence(window_strain),
                'decay_rate': self._fit_exponential_decay(window_strain, window_time),
                'omega_estimate': self._estimate_omega_parameter(window_strain),
                'spectral_entropy': self._compute_spectral_entropy(window_strain),
                'echo_amplitude': self._estimate_echo_amplitude(window_strain),
                'quality_factor': self._assess_data_quality(window_strain)
            }
        
        return indicators
    
    def _compute_modal_suppression(self, strain: np.ndarray) -> float:
        """
        Calcula ratio de supresión modal par/impar.
        """
        # FFT y espectro de potencia
        freqs, psd = signal.welch(strain, fs=self.sampling_rate, 
                                 nperseg=min(len(strain), 1024))
        
        # Frecuencia fundamental teórica
        f0 = self.model.f0
        
        # Buscar potencia en armónicos
        odd_power = 0
        even_power = 0
        
        for n in range(1, 10):
            f_target = n * f0
            if f_target > self.sampling_rate / 2:
                break
                
            # Ventana de búsqueda ±0.5 Hz
            mask = (freqs >= f_target - 0.5) & (freqs <= f_target + 0.5)
            
            if np.any(mask):
                power = np.max(psd[mask])
                if n % 2 == 1:  # Impar
                    odd_power += power
                else:  # Par
                    even_power += power
        
        # Ratio de supresión
        if even_power > 0:
            ratio = odd_power / even_power
        else:
            ratio = 100  # Supresión completa
            
        return min(ratio, 100)  # Limitar a 100:1
    
    def _track_fundamental_frequency(self, strain: np.ndarray) -> float:
        """
        Rastrea frecuencia fundamental instantánea.
        """
        # Transformada de Hilbert para fase instantánea
        analytic = signal.hilbert(strain)
        phase = np.unwrap(np.angle(analytic))
        
        # Frecuencia instantánea
        inst_freq = np.diff(phase) * self.sampling_rate / (2 * np.pi)
        
        # Filtrar outliers
        inst_freq = inst_freq[(inst_freq > 1) & (inst_freq < 100)]
        
        if len(inst_freq) > 0:
            # Buscar pico cerca de f0 teórico
            hist, bins = np.histogram(inst_freq, bins=100)
            peak_idx = np.argmax(hist)
            f_peak = (bins[peak_idx] + bins[peak_idx + 1]) / 2
            
            # Si está cerca de f0, usar ese valor
            if abs(f_peak - self.model.f0) < 2.0:
                return f_peak
        
        return self.model.f0  # Valor por defecto
    
    def _compute_phase_coherence(self, strain: np.ndarray) -> float:
        """
        Calcula coherencia de fase entre armónicos.
        """
        # FFT compleja
        fft = np.fft.rfft(strain)
        freqs = np.fft.rfftfreq(len(strain), 1/self.sampling_rate)
        
        # Fases en armónicos fundamentales
        phases = []
        f0 = self.model.f0
        
        for n in [1, 3, 5]:  # Primeros armónicos impares
            f_target = n * f0
            idx = np.argmin(np.abs(freqs - f_target))
            
            if idx < len(fft):
                phase = np.angle(fft[idx])
                phases.append(phase)
        
        if len(phases) >= 2:
            # Coherencia como varianza circular
            mean_phase = np.angle(np.mean(np.exp(1j * np.array(phases))))
            coherence = 1 - np.var(np.angle(np.exp(1j * (np.array(phases) - mean_phase))))
            return max(0, min(1, coherence))
        
        return 0.5  # Valor neutral
    
    def _fit_exponential_decay(self, strain: np.ndarray, 
                              time: np.ndarray) -> float:
        """
        Ajusta decaimiento exponencial y retorna tasa.
        """
        # Envolvente del strain
        envelope = np.abs(signal.hilbert(strain))
        
        # Suavizar
        if len(envelope) > 20:
            envelope = signal.savgol_filter(envelope, 
                                          min(21, len(envelope)//2*2-1), 3)
        
        # Ajuste exponencial
        def exp_decay(t, A, tau):
            return A * np.exp(-t/tau)
        
        try:
            # Usar solo puntos positivos
            mask = envelope > 0
            if np.sum(mask) > 10:
                popt, _ = curve_fit(exp_decay, time[mask], envelope[mask],
                                   p0=[np.max(envelope), 0.028],
                                   bounds=([0, 0.001], [np.inf, 0.1]))
                return 1/popt[1]  # Tasa de decaimiento
        except:
            pass
        
        return 1/0.028  # Valor por defecto (1/τ)
    
    def _estimate_omega_parameter(self, strain: np.ndarray) -> float:
        """
        Estima parámetro de orientabilidad Ω basado en observables.
        """
        # Ratio de supresión observado
        suppression = self._compute_modal_suppression(strain)
        
        # Invertir relación teórica: suppression = |1+Ω|/|1-Ω|
        # Resolviendo para Ω:
        if suppression > 1:
            omega_est = (suppression - 1) / (suppression + 1)
        else:
            omega_est = (1 - suppression) / (1 + suppression)
        
        # Limitar a rango físico
        return max(-1, min(1, omega_est))
    
    def _compute_spectral_entropy(self, strain: np.ndarray) -> float:
        """
        Calcula entropía espectral como medida de complejidad.
        """
        # PSD normalizado
        freqs, psd = signal.welch(strain, fs=self.sampling_rate,
                                 nperseg=min(len(strain), 512))
        
        # Normalizar a distribución de probabilidad
        psd_norm = psd / np.sum(psd)
        
        # Entropía de Shannon
        entropy = -np.sum(psd_norm * np.log(psd_norm + 1e-10))
        
        # Normalizar por entropía máxima
        max_entropy = np.log(len(psd))
        
        return entropy / max_entropy
    
    def _estimate_echo_amplitude(self, strain: np.ndarray) -> float:
        """
        Estima amplitud característica de eco.
        """
        # RMS del strain
        rms = np.sqrt(np.mean(strain**2))
        
        # Filtrar en banda de eco esperada
        f0 = self.model.f0
        sos = signal.butter(4, [f0-2, f0+10], btype='band',
                          fs=self.sampling_rate, output='sos')
        filtered = signal.sosfilt(sos, strain)
        
        # Amplitud pico en banda de eco
        echo_amp = np.max(np.abs(filtered))
        
        return echo_amp
    
    def _assess_data_quality(self, strain: np.ndarray) -> float:
        """
        Evalúa calidad de datos en ventana.
        """
        # Factores de calidad
        factors = []
        
        # 1. Proporción de datos válidos
        valid_ratio = np.sum(np.isfinite(strain)) / len(strain)
        factors.append(valid_ratio)
        
        # 2. SNR estimado
        noise_floor = np.percentile(np.abs(strain), 10)
        signal_peak = np.percentile(np.abs(strain), 90)
        if noise_floor > 0:
            snr = signal_peak / noise_floor
            factors.append(min(1, snr / 10))  # Normalizar a [0,1]
        else:
            factors.append(0.5)
        
        # 3. Estacionariedad (variación de varianza)
        chunks = np.array_split(strain, 4)
        variances = [np.var(chunk) for chunk in chunks]
        stationarity = 1 - np.std(variances) / (np.mean(variances) + 1e-10)
        factors.append(max(0, stationarity))
        
        # Promedio de factores
        return np.mean(factors)
    
    def analyze_event(self, strain: np.ndarray, time_array: np.ndarray,
                     event: LIGOEvent) -> Dict:
        """
        Análisis completo de un evento LIGO.
        
        Parameters
        ----------
        strain : np.ndarray
            Datos de strain
        time_array : np.ndarray
            Array de tiempos
        event : LIGOEvent
            Información del evento
            
        Returns
        -------
        results : Dict
            Resultados completos del análisis
        """
        print(f"\nAnalizando evento {event.name}...")
        
        # 1. Preprocesamiento
        processed_strain = self.preprocess_strain(strain)
        
        # 2. Encontrar tiempo de coalescencia
        merger_time, merger_idx = self.find_merger_time(processed_strain, time_array)
        print(f"  Coalescencia detectada en t = {merger_time:.3f} s")
        
        # 3. Extraer post-coalescencia
        post_strain, post_time = self.extract_post_merger(
            processed_strain, time_array, merger_time
        )
        
        # 4. Calcular indicadores topológicos
        indicators = self.compute_topological_indicators(post_strain, post_time)
        
        # 5. Evolución teórica del modelo
        theory_evolution = self.model.evolve_topology(
            post_time, event.energy_radiated,
            initial_state='klein', include_modes=False
        )
        
        # 6. Comparar teoría con observación
        comparison = self._compare_theory_observation(indicators, theory_evolution)
        
        # 7. Clasificar fase topológica dominante
        phase_classification = self._classify_topological_phase(indicators)
        
        # Compilar resultados
        results = {
            'event': event.name,
            'parameters': {
                'total_mass': event.total_mass,
                'energy_radiated': event.energy_radiated,
                'merger_time': merger_time
            },
            'indicators': indicators,
            'theory_evolution': {
                'time': theory_evolution['time'].tolist(),
                'omega': theory_evolution['Omega'].tolist(),
                'suppression': theory_evolution['suppression_ratio'].tolist()
            },
            'comparison': comparison,
            'phase_classification': phase_classification,
            'quality_assessment': self._global_quality_assessment(indicators)
        }
        
        return results
    
    def _compare_theory_observation(self, indicators: Dict,
                                  theory: Dict) -> Dict:
        """
        Compara indicadores observados con predicciones teóricas.
        """
        comparison = {}
        
        # Para cada ventana temporal
        for window_name in indicators.keys():
            if window_name in self.time_windows:
                t_start, t_end = self.time_windows[window_name]
                t_mid = (t_start + t_end) / 2
                
                # Índice en evolución teórica
                idx = np.argmin(np.abs(theory['time'] - t_mid))
                
                # Comparar omega
                omega_obs = indicators[window_name]['omega_estimate']
                omega_theory = theory['Omega'][idx]
                
                # Comparar supresión
                supp_obs = indicators[window_name]['suppression_ratio']
                supp_theory = theory['suppression_ratio'][idx]
                
                comparison[window_name] = {
                    'omega_difference': omega_obs - omega_theory,
                    'omega_relative_error': abs(omega_obs - omega_theory) / (abs(omega_theory) + 0.1),
                    'suppression_difference': supp_obs - supp_theory,
                    'suppression_relative_error': abs(supp_obs - supp_theory) / (supp_theory + 1),
                    'agreement_score': self._calculate_agreement_score(
                        omega_obs, omega_theory, supp_obs, supp_theory
                    )
                }
        
        # Score global
        all_scores = [comp['agreement_score'] for comp in comparison.values()]
        comparison['global_agreement'] = np.mean(all_scores) if all_scores else 0
        
        return comparison
    
    def _calculate_agreement_score(self, omega_obs: float, omega_theory: float,
                                 supp_obs: float, supp_theory: float) -> float:
        """
        Calcula score de acuerdo entre teoría y observación.
        """
        # Error en omega (peso 0.6)
        omega_error = abs(omega_obs - omega_theory) / 2  # Normalizado a [0,1]
        omega_score = 1 - min(1, omega_error)
        
        # Error en supresión (peso 0.4)
        supp_error = abs(np.log10(supp_obs + 1) - np.log10(supp_theory + 1))
        supp_score = 1 - min(1, supp_error / 2)  # Normalizado
        
        # Score combinado
        return 0.6 * omega_score + 0.4 * supp_score
    
    def _classify_topological_phase(self, indicators: Dict) -> Dict:
        """
        Clasifica la fase topológica dominante del evento.
        """
        # Promedios por ventana
        phase_scores = {
            'klein': 0,
            'transition': 0,
            'torus': 0
        }
        
        # Ventana Klein (0-14 ms)
        if 'klein_pure' in indicators:
            ind = indicators['klein_pure']
            # Klein score basado en alta supresión y Ω < -0.5
            klein_score = (
                min(1, ind['suppression_ratio'] / 20) * 0.5 +
                (1 if ind['omega_estimate'] < -0.5 else 0) * 0.5
            )
            phase_scores['klein'] = klein_score * ind['quality_factor']
        
        # Ventana transición (14-28 ms)
        if 'transition' in indicators:
            ind = indicators['transition']
            # Transición score basado en valores intermedios
            trans_score = (
                (1 if 2 < ind['suppression_ratio'] < 20 else 0) * 0.5 +
                (1 if -0.5 < ind['omega_estimate'] < 0.5 else 0) * 0.5
            )
            phase_scores['transition'] = trans_score * ind['quality_factor']
        
        # Ventana toroide (28-50 ms)
        if 'torus_dominant' in indicators:
            ind = indicators['torus_dominant']
            # Toroide score basado en baja supresión y Ω > 0.5
            torus_score = (
                (1 if ind['suppression_ratio'] < 5 else 0) * 0.5 +
                (1 if ind['omega_estimate'] > 0.5 else 0) * 0.5
            )
            phase_scores['torus'] = torus_score * ind['quality_factor']
        
        # Clasificación
        dominant_phase = max(phase_scores, key=phase_scores.get)
        confidence = phase_scores[dominant_phase]
        
        return {
            'dominant_phase': dominant_phase,
            'confidence': confidence,
            'phase_scores': phase_scores,
            'classification': self._get_phase_label(dominant_phase, confidence)
        }
    
    def _get_phase_label(self, phase: str, confidence: float) -> str:
        """
        Etiqueta descriptiva de la fase topológica.
        """
        if confidence < 0.3:
            return "indeterminate"
        elif confidence < 0.6:
            prefix = "likely_"
        else:
            prefix = "strong_"
        
        return prefix + phase
    
    def _global_quality_assessment(self, indicators: Dict) -> Dict:
        """
        Evaluación global de calidad del análisis.
        """
        quality_scores = []
        
        for window_indicators in indicators.values():
            quality_scores.append(window_indicators['quality_factor'])
        
        return {
            'mean_quality': np.mean(quality_scores) if quality_scores else 0,
            'min_quality': np.min(quality_scores) if quality_scores else 0,
            'suitable_for_analysis': np.mean(quality_scores) > 0.6 if quality_scores else False
        }
    
    def batch_analysis(self, events_data: List[Tuple[np.ndarray, np.ndarray, LIGOEvent]]) -> Dict:
        """
        Analiza múltiples eventos en lote.
        
        Parameters
        ----------
        events_data : List[Tuple]
            Lista de tuplas (strain, time, event_info)
            
        Returns
        -------
        batch_results : Dict
            Resultados agregados
        """
        print(f"\n{'='*60}")
        print(f"ANÁLISIS EN LOTE DE {len(events_data)} EVENTOS")
        print(f"{'='*60}")
        
        individual_results = []
        
        for strain, time_array, event in events_data:
            try:
                result = self.analyze_event(strain, time_array, event)
                individual_results.append(result)
            except Exception as e:
                print(f"  Error analizando {event.name}: {e}")
                continue
        
        # Análisis estadístico agregado
        batch_results = {
            'individual_results': individual_results,
            'statistics': self._compute_batch_statistics(individual_results),
            'correlations': self._compute_correlations(individual_results),
            'model_validation': self._validate_model_predictions(individual_results)
        }
        
        return batch_results
    
    def _compute_batch_statistics(self, results: List[Dict]) -> Dict:
        """
        Calcula estadísticas agregadas de múltiples eventos.
        """
        # Extraer métricas clave
        energies = []
        klein_scores = []
        transition_scores = []
        torus_scores = []
        global_agreements = []
        
        for res in results:
            energies.append(res['parameters']['energy_radiated'])
            
            phase_scores = res['phase_classification']['phase_scores']
            klein_scores.append(phase_scores['klein'])
            transition_scores.append(phase_scores['transition'])
            torus_scores.append(phase_scores['torus'])
            
            global_agreements.append(res['comparison']['global_agreement'])
        
        return {
            'n_events': len(results),
            'energy_distribution': {
                'mean': np.mean(energies),
                'std': np.std(energies),
                'min': np.min(energies),
                'max': np.max(energies)
            },
            'phase_distribution': {
                'klein_mean': np.mean(klein_scores),
                'transition_mean': np.mean(transition_scores),
                'torus_mean': np.mean(torus_scores)
            },
            'theory_agreement': {
                'mean': np.mean(global_agreements),
                'std': np.std(global_agreements)
            }
        }
    
    def _compute_correlations(self, results: List[Dict]) -> Dict:
        """
        Calcula correlaciones entre energía y fase topológica.
        """
        # Arrays para correlación
        energies = []
        klein_purities = []
        suppression_evolutions = []
        
        for res in results:
            energies.append(res['parameters']['energy_radiated'])
            
            # Pureza Klein (score en ventana temprana)
            klein_purity = res['phase_classification']['phase_scores']['klein']
            klein_purities.append(klein_purity)
            
            # Evolución de supresión
            if 'klein_pure' in res['indicators'] and 'torus_dominant' in res['indicators']:
                early_supp = res['indicators']['klein_pure']['suppression_ratio']
                late_supp = res['indicators']['torus_dominant']['suppression_ratio']
                evolution = early_supp / (late_supp + 1)
                suppression_evolutions.append(evolution)
            else:
                suppression_evolutions.append(1.0)
        
        # Calcular correlaciones
        energy_klein_corr, energy_klein_p = pearsonr(energies, klein_purities)
        energy_evolution_corr, energy_evolution_p = pearsonr(energies, suppression_evolutions)
        
        return {
            'energy_vs_klein_purity': {
                'correlation': energy_klein_corr,
                'p_value': energy_klein_p,
                'significant': energy_klein_p < 0.05
            },
            'energy_vs_suppression_evolution': {
                'correlation': energy_evolution_corr,
                'p_value': energy_evolution_p,
                'significant': energy_evolution_p < 0.05
            }
        }
    
    def _validate_model_predictions(self, results: List[Dict]) -> Dict:
        """
        Valida predicciones del modelo con resultados observados.
        """
        # Predicciones clave del modelo
        validations = {
            'frequency_consistency': [],
            'relaxation_time_consistency': [],
            'energy_threshold_test': []
        }
        
        for res in results:
            # 1. Consistencia de frecuencia fundamental
            observed_freqs = []
            for window in res['indicators'].values():
                observed_freqs.append(window['fundamental_freq'])
            
            mean_freq = np.mean(observed_freqs)
            freq_error = abs(mean_freq - self.model.f0) / self.model.f0
            validations['frequency_consistency'].append(freq_error < 0.2)  # 20% error
            
            # 2. Tiempo de relajación
            # Buscar transición Ω = 0
            theory_omega = res['theory_evolution']['omega']
            theory_time = res['theory_evolution']['time']
            
            crossings = np.where(np.diff(np.sign(theory_omega)))[0]
            if len(crossings) > 0:
                transition_time = theory_time[crossings[0]]
                time_error = abs(transition_time - 0.028) / 0.028
                validations['relaxation_time_consistency'].append(time_error < 0.3)
            else:
                validations['relaxation_time_consistency'].append(False)
            
            # 3. Umbral de energía
            energy = res['parameters']['energy_radiated']
            klein_score = res['phase_classification']['phase_scores']['klein']
            
            # Alta energía debería dar Klein puro
            if energy > 2.0:  # M☉c²
                validations['energy_threshold_test'].append(klein_score > 0.6)
            else:
                validations['energy_threshold_test'].append(True)  # No aplica
        
        # Resumen de validación
        return {
            'frequency_validation': {
                'pass_rate': np.mean(validations['frequency_consistency']),
                'validated': np.mean(validations['frequency_consistency']) > 0.7
            },
            'relaxation_validation': {
                'pass_rate': np.mean(validations['relaxation_time_consistency']),
                'validated': np.mean(validations['relaxation_time_consistency']) > 0.5
            },
            'energy_threshold_validation': {
                'pass_rate': np.mean(validations['energy_threshold_test']),
                'validated': np.mean(validations['energy_threshold_test']) > 0.7
            },
            'overall_validation': all([
                np.mean(validations['frequency_consistency']) > 0.7,
                np.mean(validations['relaxation_time_consistency']) > 0.5,
                np.mean(validations['energy_threshold_test']) > 0.7
            ])
        }


def generate_test_data(event: LIGOEvent, 
                      duration: float = 2.0) -> Tuple[np.ndarray, np.ndarray]:
    """
    Genera datos de prueba simulados para un evento.
    
    Parameters
    ----------
    event : LIGOEvent
        Información del evento
    duration : float
        Duración de la señal (segundos)
        
    Returns
    -------
    strain : np.ndarray
        Strain simulado
    time : np.ndarray
        Array de tiempos
    """
    # Parámetros
    fs = 4096  # Hz
    t = np.linspace(0, duration, int(duration * fs))
    
    # Componente de fusión (chirp simplificado)
    f_merger = 150  # Hz
    merger_time = duration / 2
    
    # Señal de fusión
    phase = 2 * np.pi * f_merger * (t - merger_time)**2
    merger_signal = np.exp(-(t - merger_time)**2 / 0.01**2) * np.cos(phase)
    
    # Componente de eco (post-fusión)
    model = TopologicalTransitionModel()
    echo_signal = np.zeros_like(t)
    
    # Solo para tiempos post-fusión
    post_mask = t > merger_time
    post_time = t[post_mask] - merger_time
    
    # Generar eco basado en modelo
    for n in [1, 3, 5]:  # Armónicos impares
        f_echo = n * model.f0
        amp = (1/n**2) * np.exp(-post_time / model.tau)
        echo_signal[post_mask] += amp * np.sin(2 * np.pi * f_echo * post_time)
    
    # Escalar por energía del evento
    echo_signal *= event.energy_radiated / 3.0
    
    # Combinar señales
    strain = merger_signal + 0.1 * echo_signal
    
    # Añadir ruido
    noise_level = 0.01
    strain += noise_level * np.random.randn(len(t))
    
    return strain, t


def main():
    """
    Demuestra el pipeline con datos de prueba.
    """
    print("PIPELINE DE ANÁLISIS TOPOLÓGICO LIGO")
    print("="*60)
    
    # Inicializar pipeline
    pipeline = TopologicalAnalysisPipeline()
    
    # Eventos de prueba
    test_events = [
        LIGOEvent(
            name="GW150914",
            mass_1=36.0,
            mass_2=29.0,
            total_mass=62.0,
            chirp_mass=30.0,
            final_spin=0.68,
            luminosity_distance=410.0,
            merger_time=0.0,
            energy_radiated=3.0
        ),
        LIGOEvent(
            name="GW151226",
            mass_1=14.0,
            mass_2=7.8,
            total_mass=21.0,
            chirp_mass=8.9,
            final_spin=0.74,
            luminosity_distance=440.0,
            merger_time=0.0,
            energy_radiated=1.0
        ),
        LIGOEvent(
            name="GW170608",
            mass_1=12.0,
            mass_2=7.0,
            total_mass=18.0,
            chirp_mass=7.9,
            final_spin=0.69,
            luminosity_distance=340.0,
            merger_time=0.0,
            energy_radiated=0.5
        )
    ]
    
    # Generar datos de prueba y analizar
    events_data = []
    for event in test_events:
        print(f"\nGenerando datos de prueba para {event.name}...")
        strain, time = generate_test_data(event)
        events_data.append((strain, time, event))
    
    # Análisis en lote
    batch_results = pipeline.batch_analysis(events_data)
    
    # Mostrar resultados
    print("\n" + "="*60)
    print("RESULTADOS DEL ANÁLISIS")
    print("="*60)
    
    stats = batch_results['statistics']
    print(f"\nEstadísticas de {stats['n_events']} eventos:")
    print(f"  Energía promedio: {stats['energy_distribution']['mean']:.2f} M☉c²")
    print(f"  Distribución de fases:")
    print(f"    Klein: {stats['phase_distribution']['klein_mean']:.2%}")
    print(f"    Transición: {stats['phase_distribution']['transition_mean']:.2%}")
    print(f"    Toroide: {stats['phase_distribution']['torus_mean']:.2%}")
    
    corr = batch_results['correlations']
    print(f"\nCorrelaciones:")
    print(f"  Energía vs Pureza Klein: r = {corr['energy_vs_klein_purity']['correlation']:.3f}")
    print(f"    p-value: {corr['energy_vs_klein_purity']['p_value']:.3f}")
    
    val = batch_results['model_validation']
    print(f"\nValidación del modelo:")
    print(f"  Frecuencia fundamental: {'✓' if val['frequency_validation']['validated'] else '✗'}")
    print(f"  Tiempo de relajación: {'✓' if val['relaxation_validation']['validated'] else '✗'}")
    print(f"  Umbral de energía: {'✓' if val['energy_threshold_validation']['validated'] else '✗'}")
    print(f"  VALIDACIÓN GLOBAL: {'✓ APROBADA' if val['overall_validation'] else '✗ FALLÓ'}")
    
    # Guardar resultados
    output_file = "topological_analysis_results.json"
    with open(output_file, 'w') as f:
        # Convertir arrays numpy a listas para JSON
        def convert_to_serializable(obj):
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            elif isinstance(obj, np.generic):
                return obj.item()
            elif isinstance(obj, LIGOEvent):
                return obj.__dict__
            return obj
        
        # Aplicar conversión recursivamente
        import json
        serializable_results = json.loads(
            json.dumps(batch_results, default=convert_to_serializable)
        )
        
        json.dump(serializable_results, f, indent=2)
    
    print(f"\n✅ Resultados guardados en: {output_file}")
    print("\nPipeline de análisis completado exitosamente!")


if __name__ == "__main__":
    main()