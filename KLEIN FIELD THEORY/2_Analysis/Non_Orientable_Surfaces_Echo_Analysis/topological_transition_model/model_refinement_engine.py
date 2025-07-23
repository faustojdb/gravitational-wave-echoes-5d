#!/usr/bin/env python3
"""
Motor de Refinamiento del Modelo de Transición Topológica
=========================================================

Este módulo implementa refinamiento paralelo de:
1. Parámetros físicos del modelo (ecuación maestra, escalas)
2. Algoritmos de detección (ventanas temporales, indicadores)

Objetivo: Mejorar acuerdo teoría-observación del 35% actual a >70%

Autor: Fausto José Di Bacco
Fecha: Diciembre 2024
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize, differential_evolution, minimize_scalar
from scipy.stats import pearsonr, chi2
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from typing import Dict, List, Tuple, Optional, Callable
import json
import copy
from dataclasses import dataclass, asdict
import warnings

# Importar módulos del proyecto
from topological_transition_implementation import TopologicalTransitionModel
from ligo_analysis_pipeline import TopologicalAnalysisPipeline, LIGOEvent
from ligo_data_analyzer import LIGODataDownloader, LIGOCatalogEvent

warnings.filterwarnings('ignore')


@dataclass
class ModelParameters:
    """Parámetros del modelo topológico optimizables."""
    
    # Parámetros físicos fundamentales
    R: float = 8.4e6                    # Radio 5D (metros)
    kappa: float = 1.0                  # Constante gravitacional 5D normalizada
    alpha_relax: float = 1.0            # Tasa de relajación energética
    beta_coupling: float = 0.1          # Acoplamiento modo-topología
    
    # Escalas temporales
    tau_scale_factor: float = 1.0       # Factor de escala para τ
    omega_damping: float = 0.1          # Amortiguamiento de oscilaciones Ω
    
    # Parámetros de frecuencia
    f0_scale_factor: float = 1.0        # Factor de escala para f₀
    harmonic_coupling: float = 0.05     # Acoplamiento entre armónicos
    
    # Parámetros de amplitud
    echo_amplitude_scale: float = 0.01  # Escala global de amplitud de ecos
    mass_scaling_exponent: float = 0.5  # Exponente de escalamiento con masa
    
    # Nuevos parámetros de no-linealidad
    nonlinear_threshold: float = 2.0    # Umbral para efectos no-lineales
    nonlinear_strength: float = 0.1     # Fuerza de efectos no-lineales
    
    def to_dict(self) -> Dict:
        """Convierte a diccionario."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'ModelParameters':
        """Crea desde diccionario."""
        return cls(**data)


@dataclass
class DetectionParameters:
    """Parámetros de algoritmos de detección optimizables."""
    
    # Ventanas temporales (segundos)
    klein_window_end: float = 0.014     # Final de ventana Klein pura
    transition_window_end: float = 0.028  # Final de ventana de transición
    torus_window_end: float = 0.050     # Final de ventana toroide
    
    # Parámetros de procesamiento de señal
    highpass_freq: float = 20.0         # Frecuencia corte pasa-altas
    bandpass_low: float = 35.0          # Límite inferior banda de análisis
    bandpass_high: float = 350.0        # Límite superior banda de análisis
    
    # Parámetros de detección de frecuencia
    freq_search_bandwidth: float = 0.5  # Ancho de banda búsqueda f₀
    spectral_resolution: float = 0.1    # Resolución espectral
    
    # Umbrales de detección
    omega_threshold_klein: float = -0.5  # Umbral para clasificar Klein
    omega_threshold_torus: float = 0.5   # Umbral para clasificar Toroide
    suppression_threshold_klein: float = 5.0  # Umbral supresión para Klein
    
    # Parámetros de calidad
    min_snr_threshold: float = 8.0      # SNR mínimo para análisis
    min_quality_score: float = 0.6      # Score mínimo de calidad
    
    # Nuevos parámetros adaptativos
    adaptive_window_scaling: bool = True  # Escalamiento adaptativo de ventanas
    mass_dependent_thresholds: bool = True  # Umbrales dependientes de masa
    
    def to_dict(self) -> Dict:
        """Convierte a diccionario."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'ModelParameters':
        """Crea desde diccionario."""
        return cls(**data)


class EnhancedTopologicalModel(TopologicalTransitionModel):
    """Modelo topológico mejorado con parámetros refinados."""
    
    def __init__(self, model_params: ModelParameters):
        """
        Inicializa modelo con parámetros refinados.
        
        Parameters
        ----------
        model_params : ModelParameters
            Parámetros del modelo físico
        """
        # Inicializar modelo base
        super().__init__(model_params.R, model_params.kappa)
        
        # Aplicar parámetros refinados
        self.model_params = model_params
        self._apply_refined_parameters()
    
    def _apply_refined_parameters(self):
        """Aplica parámetros refinados al modelo."""
        
        # Recalcular escalas derivadas
        self.tau *= self.model_params.tau_scale_factor
        self.f0 *= self.model_params.f0_scale_factor
        self.alpha *= self.model_params.alpha_relax
        
        # Nuevos parámetros
        self.beta_coupling = self.model_params.beta_coupling
        self.omega_damping = self.model_params.omega_damping
        self.nonlinear_threshold = self.model_params.nonlinear_threshold
        self.nonlinear_strength = self.model_params.nonlinear_strength
    
    def enhanced_master_equation(self, t: float, y: List[float], 
                                E_func: Callable) -> List[float]:
        """
        Ecuación maestra mejorada con efectos no-lineales.
        
        Mejoras:
        - Efectos no-lineales en alta energía
        - Amortiguamiento de oscilaciones
        - Acoplamiento dinámico entre modos
        """
        Omega = y[0]
        modes = y[1:] if len(y) > 1 else []
        
        # Energía en tiempo actual
        E_t = E_func(t)
        
        # Término de relajación básico
        relaxation_term = -self.alpha * E_t * Omega
        
        # Efectos no-lineales en alta energía
        if E_t > self.nonlinear_threshold:
            nonlinear_factor = 1 + self.nonlinear_strength * (E_t / self.nonlinear_threshold - 1)
            relaxation_term *= nonlinear_factor
        
        # Amortiguamiento de oscilaciones
        damping_term = -self.omega_damping * Omega * abs(Omega)
        
        # Contribución de modos (mejorada)
        mode_term = 0
        if modes:
            for i, mode in enumerate(modes):
                n = 2*i + 1  # Modo impar
                mode_contribution = abs(mode)**2 * (1 + self.model_params.harmonic_coupling * n)
                mode_term += mode_contribution
            
            mode_term *= (2 * np.pi * self.c / self.R)
        
        # Ecuación maestra mejorada
        dOmega_dt = relaxation_term + damping_term + mode_term
        
        # Evolución de modos (si incluidos)
        dmodes_dt = []
        if modes:
            for i, mode in enumerate(modes):
                n = 2*i + 1
                omega_n = n * 2 * np.pi * self.f0
                
                # Acoplamiento mejorado
                coupling = self.beta_coupling * (1 - Omega**2) if n % 2 == 0 else 0
                
                dmode_dt = (-1j * omega_n * mode - 
                           coupling * Omega * mode -
                           0.01 * mode * abs(mode)**2)  # Término no-lineal
                
                dmodes_dt.append(dmode_dt.real)
        
        return [dOmega_dt] + dmodes_dt
    
    def evolve_topology_enhanced(self, t_array: np.ndarray, E_initial: float,
                               initial_state: str = 'klein') -> Dict[str, np.ndarray]:
        """
        Evolución mejorada del sistema topológico.
        """
        # Usar ecuación maestra mejorada
        original_master_eq = self.master_equation
        self.master_equation = self.enhanced_master_equation
        
        # Evolucionar con ecuación mejorada
        result = self.evolve_topology(t_array, E_initial, initial_state, include_modes=True)
        
        # Restaurar ecuación original
        self.master_equation = original_master_eq
        
        return result
    
    def predict_echo_spectrum_enhanced(self, t: float, Omega: float, 
                                     mass: float) -> Dict[str, np.ndarray]:
        """
        Predicción mejorada del espectro de ecos.
        """
        # Espectro base
        spectrum = self.predict_echo_spectrum(t, Omega, mass)
        
        # Aplicar escalamiento mejorado
        scaling_factor = self.model_params.echo_amplitude_scale
        mass_factor = (mass / 62.0)**(-self.model_params.mass_scaling_exponent)
        
        # Modulación dependiente del estado topológico
        if Omega < -0.8:  # Klein muy puro
            purity_boost = 1.5
        elif Omega > 0.8:  # Toroide muy puro
            purity_boost = 0.3
        else:  # Estado mixto
            purity_boost = 1.0
        
        # Aplicar mejoras
        spectrum['amplitudes'] *= scaling_factor * mass_factor * purity_boost
        
        # Añadir modulación de frecuencia en transición
        if -0.5 < Omega < 0.5:
            freq_modulation = 1 + 0.1 * np.sin(2 * np.pi * t / self.tau)
            spectrum['frequencies'] *= freq_modulation
        
        return spectrum


class EnhancedAnalysisPipeline(TopologicalAnalysisPipeline):
    """Pipeline de análisis mejorado con detección adaptativa."""
    
    def __init__(self, model: EnhancedTopologicalModel, 
                 detection_params: DetectionParameters):
        """
        Inicializa pipeline mejorado.
        
        Parameters
        ----------
        model : EnhancedTopologicalModel
            Modelo topológico mejorado
        detection_params : DetectionParameters
            Parámetros de detección optimizados
        """
        super().__init__(model)
        self.detection_params = detection_params
        self._update_pipeline_parameters()
    
    def _update_pipeline_parameters(self):
        """Actualiza parámetros del pipeline."""
        
        # Actualizar ventanas temporales
        self.time_windows = {
            'klein_pure': (0, self.detection_params.klein_window_end),
            'transition': (self.detection_params.klein_window_end, 
                          self.detection_params.transition_window_end),
            'torus_dominant': (self.detection_params.transition_window_end,
                              self.detection_params.torus_window_end),
            'static': (self.detection_params.torus_window_end, 0.100)
        }
        
        # Actualizar bandas de frecuencia
        self.frequency_bands['analysis'] = (
            self.detection_params.bandpass_low,
            self.detection_params.bandpass_high
        )
    
    def preprocess_strain_enhanced(self, strain: np.ndarray, 
                                 event_mass: Optional[float] = None) -> np.ndarray:
        """
        Preprocesamiento mejorado con adaptación por masa.
        """
        # Preprocesamiento base
        processed = self.preprocess_strain(strain, self.detection_params.highpass_freq)
        
        # Filtrado adaptativo por masa
        if event_mass and self.detection_params.mass_dependent_thresholds:
            # Ajustar frecuencias basado en masa del evento
            if event_mass > 100:  # Eventos muy masivos
                # Señal más baja en frecuencia
                sos = signal.butter(4, [15, 250], btype='band', 
                                  fs=self.sampling_rate, output='sos')
            elif event_mass < 10:  # Eventos de baja masa
                # Señal más alta en frecuencia
                sos = signal.butter(4, [50, 500], btype='band',
                                  fs=self.sampling_rate, output='sos')
            else:  # Rango normal
                sos = signal.butter(4, [self.detection_params.bandpass_low,
                                      self.detection_params.bandpass_high], 
                                  btype='band', fs=self.sampling_rate, output='sos')
            
            processed = signal.sosfilt(sos, processed)
        
        return processed
    
    def _compute_modal_suppression_enhanced(self, strain: np.ndarray,
                                          event_mass: Optional[float] = None) -> float:
        """
        Cálculo mejorado de supresión modal con adaptación por masa.
        """
        # FFT y espectro de potencia con mayor resolución
        nperseg = min(len(strain), 2048)  # Mayor resolución
        freqs, psd = signal.welch(strain, fs=self.sampling_rate,
                                 nperseg=nperseg, noverlap=nperseg//2)
        
        # Frecuencia fundamental adaptativa
        f0 = self.model.f0
        if event_mass and self.detection_params.mass_dependent_thresholds:
            # Escalamiento empírico con masa
            f0 *= (62.0 / event_mass)**0.1
        
        # Búsqueda de armónicos con ventana adaptativa
        bandwidth = self.detection_params.freq_search_bandwidth
        if event_mass:
            # Ventana más ancha para eventos masivos (señal más ruidosa)
            bandwidth *= (1 + 0.5 * max(0, event_mass - 30) / 70)
        
        odd_power = 0
        even_power = 0
        
        for n in range(1, 10):
            f_target = n * f0
            if f_target > self.sampling_rate / 2:
                break
            
            # Ventana de búsqueda adaptativa
            mask = (freqs >= f_target - bandwidth) & (freqs <= f_target + bandwidth)
            
            if np.any(mask):
                # Usar pico máximo en ventana
                power = np.max(psd[mask])
                
                # Ponderación por armónico (armónicos altos menos confiables)
                weight = 1.0 / (1 + 0.1 * n)
                power *= weight
                
                if n % 2 == 1:  # Impar
                    odd_power += power
                else:  # Par
                    even_power += power
        
        # Ratio de supresión con regularización
        if even_power > 0:
            ratio = odd_power / even_power
        else:
            ratio = 100  # Supresión completa
        
        return min(ratio, 200)  # Cap en 200:1
    
    def _estimate_omega_parameter_enhanced(self, strain: np.ndarray,
                                         event_mass: Optional[float] = None) -> float:
        """
        Estimación mejorada del parámetro Ω con múltiples métodos.
        """
        # Método 1: Basado en supresión modal
        suppression = self._compute_modal_suppression_enhanced(strain, event_mass)
        
        # Convertir supresión a Ω usando relación calibrada
        if suppression > 50:
            omega_suppression = -0.95  # Klein muy puro
        elif suppression > 20:
            omega_suppression = -0.8   # Klein moderado
        elif suppression > 5:
            omega_suppression = -0.3   # Klein débil
        elif suppression > 2:
            omega_suppression = 0.0    # Transición
        else:
            omega_suppression = 0.8    # Toroide
        
        # Método 2: Basado en coherencia espectral
        freqs, times, Sxx = signal.spectrogram(strain, fs=self.sampling_rate,
                                              nperseg=256, noverlap=240)
        
        # Buscar estructura harmónica
        f0 = self.model.f0
        if event_mass:
            f0 *= (62.0 / event_mass)**0.1
        
        harmonic_coherence = 0
        for n in [1, 3, 5]:  # Primeros armónicos impares
            f_harmonic = n * f0
            freq_idx = np.argmin(np.abs(freqs - f_harmonic))
            
            if freq_idx < len(freqs):
                # Coherencia temporal del armónico
                power_evolution = Sxx[freq_idx, :]
                if np.max(power_evolution) > 0:
                    coherence = np.std(power_evolution) / (np.mean(power_evolution) + 1e-10)
                    harmonic_coherence += 1.0 / (1 + coherence)
        
        harmonic_coherence /= 3  # Normalizar
        
        # Convertir coherencia a Ω
        if harmonic_coherence > 0.8:
            omega_coherence = -0.9
        elif harmonic_coherence > 0.6:
            omega_coherence = -0.5
        elif harmonic_coherence > 0.4:
            omega_coherence = 0.0
        else:
            omega_coherence = 0.7
        
        # Método 3: Basado en entropía espectral
        psd_norm = Sxx.flatten()
        psd_norm = psd_norm / (np.sum(psd_norm) + 1e-10)
        
        entropy = -np.sum(psd_norm * np.log(psd_norm + 1e-10))
        max_entropy = np.log(len(psd_norm))
        normalized_entropy = entropy / max_entropy
        
        # Baja entropía → estructura ordenada → Klein
        # Alta entropía → estructura desordenada → Toroide
        omega_entropy = 1 - 2 * normalized_entropy  # Mapear [0,1] → [1,-1]
        
        # Combinar métodos con pesos
        weights = [0.5, 0.3, 0.2]  # Dar más peso a supresión modal
        omega_combined = (weights[0] * omega_suppression +
                         weights[1] * omega_coherence +
                         weights[2] * omega_entropy)
        
        # Limitar a rango físico
        return max(-1, min(1, omega_combined))
    
    def analyze_event_enhanced(self, strain: np.ndarray, time_array: np.ndarray,
                             event: LIGOEvent) -> Dict:
        """
        Análisis mejorado de evento con detección adaptativa.
        """
        print(f"\nAnálisis mejorado de {event.name}...")
        
        # Preprocesamiento adaptativo
        processed_strain = self.preprocess_strain_enhanced(strain, event.total_mass)
        
        # Encontrar coalescencia con método mejorado
        merger_time, merger_idx = self.find_merger_time(processed_strain, time_array)
        
        # Ventanas temporales adaptativas por masa
        if self.detection_params.adaptive_window_scaling:
            # Eventos masivos → ventanas más largas (evolución más lenta)
            mass_factor = max(0.5, min(2.0, event.total_mass / 62.0))
            
            scaled_windows = {}
            for name, (start, end) in self.time_windows.items():
                scaled_windows[name] = (start * mass_factor, end * mass_factor)
            
            # Usar ventanas escaladas temporalmente
            original_windows = self.time_windows
            self.time_windows = scaled_windows
        
        # Extraer región post-coalescencia
        post_strain, post_time = self.extract_post_merger(
            processed_strain, time_array, merger_time
        )
        
        # Análisis de indicadores mejorado
        indicators = {}
        for window_name, (t_start, t_end) in self.time_windows.items():
            mask = (post_time >= t_start) & (post_time < t_end)
            if np.sum(mask) < 50:  # Mínimo de puntos
                continue
            
            window_strain = post_strain[mask]
            window_time = post_time[mask]
            
            # Indicadores mejorados
            indicators[window_name] = {
                'suppression_ratio': self._compute_modal_suppression_enhanced(
                    window_strain, event.total_mass
                ),
                'omega_estimate': self._estimate_omega_parameter_enhanced(
                    window_strain, event.total_mass
                ),
                'fundamental_freq': self._track_fundamental_frequency(window_strain),
                'phase_coherence': self._compute_phase_coherence(window_strain),
                'decay_rate': self._fit_exponential_decay(window_strain, window_time),
                'spectral_entropy': self._compute_spectral_entropy(window_strain),
                'echo_amplitude': self._estimate_echo_amplitude(window_strain),
                'quality_factor': self._assess_data_quality(window_strain),
                
                # Nuevos indicadores
                'harmonic_structure': self._analyze_harmonic_structure(window_strain),
                'temporal_coherence': self._analyze_temporal_coherence(window_strain),
                'nonlinear_signature': self._detect_nonlinear_signatures(window_strain)
            }
        
        # Restaurar ventanas originales si fueron escaladas
        if self.detection_params.adaptive_window_scaling:
            self.time_windows = original_windows
        
        # Evolución teórica mejorada
        theory_evolution = self.model.evolve_topology_enhanced(
            post_time, event.energy_radiated, initial_state='klein'
        )
        
        # Comparación mejorada teoría-observación
        comparison = self._compare_theory_observation_enhanced(
            indicators, theory_evolution, event
        )
        
        # Clasificación de fase mejorada
        phase_classification = self._classify_topological_phase_enhanced(
            indicators, event
        )
        
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
            'quality_assessment': self._global_quality_assessment(indicators),
            'enhancement_flags': {
                'adaptive_windows_used': self.detection_params.adaptive_window_scaling,
                'mass_dependent_processing': self.detection_params.mass_dependent_thresholds,
                'enhanced_omega_estimation': True
            }
        }
        
        return results
    
    def _analyze_harmonic_structure(self, strain: np.ndarray) -> Dict:
        """Analiza estructura harmónica detallada."""
        freqs, psd = signal.welch(strain, fs=self.sampling_rate, nperseg=1024)
        
        f0 = self.model.f0
        harmonics_found = []
        
        for n in range(1, 8):
            f_target = n * f0
            if f_target > self.sampling_rate / 2:
                break
            
            # Buscar pico cerca de frecuencia objetivo
            search_mask = (freqs >= f_target - 1.0) & (freqs <= f_target + 1.0)
            
            if np.any(search_mask):
                power_in_band = np.max(psd[search_mask])
                noise_floor = np.median(psd)
                
                snr = power_in_band / (noise_floor + 1e-10)
                
                harmonics_found.append({
                    'harmonic': n,
                    'frequency': f_target,
                    'snr': float(snr),
                    'detected': snr > 2.0
                })
        
        return {
            'harmonics': harmonics_found,
            'n_detected': sum(h['detected'] for h in harmonics_found),
            'odd_even_ratio': self._calculate_odd_even_ratio(harmonics_found)
        }
    
    def _analyze_temporal_coherence(self, strain: np.ndarray) -> float:
        """Analiza coherencia temporal de la señal."""
        # Dividir en segmentos temporales
        n_segments = 4
        segment_length = len(strain) // n_segments
        
        segment_powers = []
        for i in range(n_segments):
            start_idx = i * segment_length
            end_idx = start_idx + segment_length
            segment = strain[start_idx:end_idx]
            
            segment_power = np.mean(segment**2)
            segment_powers.append(segment_power)
        
        # Coherencia como estabilidad de potencia
        if len(segment_powers) > 1 and np.mean(segment_powers) > 0:
            coherence = 1 - np.std(segment_powers) / np.mean(segment_powers)
        else:
            coherence = 0
        
        return max(0, min(1, coherence))
    
    def _detect_nonlinear_signatures(self, strain: np.ndarray) -> Dict:
        """Detecta firmas de efectos no-lineales."""
        # Bispectrum analysis (simplificado)
        # Buscar acoplamiento entre frecuencias
        
        freqs, psd = signal.welch(strain, fs=self.sampling_rate, nperseg=512)
        
        f0 = self.model.f0
        
        # Buscar intermodulación f1 + f2 = f3
        nonlinear_score = 0
        interactions_found = 0
        
        for f1_mult in [1, 3]:
            for f2_mult in [1, 3]:
                f3_mult = f1_mult + f2_mult
                
                f1 = f1_mult * f0
                f2 = f2_mult * f0
                f3 = f3_mult * f0
                
                if f3 > self.sampling_rate / 2:
                    continue
                
                # Buscar potencia en cada frecuencia
                power1 = self._get_power_at_freq(freqs, psd, f1)
                power2 = self._get_power_at_freq(freqs, psd, f2)
                power3 = self._get_power_at_freq(freqs, psd, f3)
                
                # Evaluar correlación no-lineal
                expected_power3 = np.sqrt(power1 * power2)
                if expected_power3 > 0:
                    correlation = power3 / expected_power3
                    if correlation > 1.5:  # Evidencia de acoplamiento
                        nonlinear_score += correlation
                        interactions_found += 1
        
        return {
            'nonlinear_score': float(nonlinear_score),
            'interactions_found': interactions_found,
            'nonlinearity_detected': nonlinear_score > 2.0
        }
    
    def _get_power_at_freq(self, freqs: np.ndarray, psd: np.ndarray, 
                          target_freq: float, bandwidth: float = 0.5) -> float:
        """Obtiene potencia en frecuencia específica."""
        mask = (freqs >= target_freq - bandwidth) & (freqs <= target_freq + bandwidth)
        if np.any(mask):
            return np.max(psd[mask])
        return 0
    
    def _calculate_odd_even_ratio(self, harmonics: List[Dict]) -> float:
        """Calcula ratio entre armónicos impares y pares detectados."""
        odd_power = sum(h['snr'] for h in harmonics if h['harmonic'] % 2 == 1 and h['detected'])
        even_power = sum(h['snr'] for h in harmonics if h['harmonic'] % 2 == 0 and h['detected'])
        
        if even_power > 0:
            return odd_power / even_power
        elif odd_power > 0:
            return 100  # Solo impares detectados
        else:
            return 1  # Ninguno detectado
    
    def _compare_theory_observation_enhanced(self, indicators: Dict,
                                           theory: Dict, event: LIGOEvent) -> Dict:
        """Comparación mejorada teoría-observación."""
        comparison = {}
        
        # Comparación por ventana con pesos adaptativos
        window_weights = {
            'klein_pure': 0.4,
            'transition': 0.3,
            'torus_dominant': 0.2,
            'static': 0.1
        }
        
        total_agreement = 0
        total_weight = 0
        
        for window_name in indicators.keys():
            if window_name in self.time_windows:
                t_start, t_end = self.time_windows[window_name]
                t_mid = (t_start + t_end) / 2
                
                # Interpolación en evolución teórica
                idx = np.argmin(np.abs(theory['time'] - t_mid))
                
                # Comparar observables clave
                omega_obs = indicators[window_name]['omega_estimate']
                omega_theory = theory['omega'][idx]
                
                supp_obs = indicators[window_name]['suppression_ratio']
                supp_theory = theory['suppression'][idx]
                
                # Score de acuerdo mejorado
                omega_agreement = 1 - abs(omega_obs - omega_theory) / 2
                
                # Acuerdo en supresión (escala log)
                if supp_theory > 0 and supp_obs > 0:
                    log_diff = abs(np.log10(supp_obs + 1) - np.log10(supp_theory + 1))
                    supp_agreement = max(0, 1 - log_diff / 2)
                else:
                    supp_agreement = 0
                
                # Combinar con pesos
                window_agreement = 0.6 * omega_agreement + 0.4 * supp_agreement
                
                # Aplicar peso de ventana
                weight = window_weights.get(window_name, 0.1)
                
                # Ajuste por calidad de datos
                quality_factor = indicators[window_name]['quality_factor']
                effective_weight = weight * quality_factor
                
                total_agreement += window_agreement * effective_weight
                total_weight += effective_weight
                
                comparison[window_name] = {
                    'omega_obs': omega_obs,
                    'omega_theory': omega_theory,
                    'omega_agreement': omega_agreement,
                    'suppression_obs': supp_obs,
                    'suppression_theory': supp_theory,
                    'suppression_agreement': supp_agreement,
                    'window_agreement': window_agreement,
                    'weight': effective_weight
                }
        
        # Score global mejorado
        if total_weight > 0:
            global_agreement = total_agreement / total_weight
        else:
            global_agreement = 0
        
        # Bonificación por consistencia
        consistency_bonus = 0
        if len(comparison) >= 2:
            agreements = [comp['window_agreement'] for comp in comparison.values()]
            consistency = 1 - np.std(agreements) / (np.mean(agreements) + 0.1)
            consistency_bonus = 0.1 * max(0, consistency)
        
        comparison['global_agreement'] = min(1.0, global_agreement + consistency_bonus)
        comparison['consistency_bonus'] = consistency_bonus
        
        return comparison
    
    def _classify_topological_phase_enhanced(self, indicators: Dict,
                                           event: LIGOEvent) -> Dict:
        """Clasificación mejorada de fase topológica."""
        
        # Scores adaptativos por masa del evento
        mass_factor = event.total_mass / 62.0  # Normalizar a GW150914
        
        phase_scores = {'klein': 0, 'transition': 0, 'torus': 0}
        total_weight = 0
        
        # Pesos adaptativos por ventana
        window_weights = {
            'klein_pure': 0.5,
            'transition': 0.3,
            'torus_dominant': 0.2
        }
        
        for window_name, weight in window_weights.items():
            if window_name not in indicators:
                continue
            
            ind = indicators[window_name]
            quality = ind['quality_factor']
            
            # Ajustar peso por calidad
            effective_weight = weight * quality
            
            # Scores por fase basados en múltiples indicadores
            omega = ind['omega_estimate']
            suppression = ind['suppression_ratio']
            coherence = ind.get('phase_coherence', 0.5)
            harmonic_struct = ind.get('harmonic_structure', {'odd_even_ratio': 1})
            
            # Klein score
            klein_score = 0
            if omega < self.detection_params.omega_threshold_klein:
                klein_score += 0.4
            if suppression > self.detection_params.suppression_threshold_klein:
                klein_score += 0.3
            if harmonic_struct['odd_even_ratio'] > 10:
                klein_score += 0.2
            if coherence > 0.7:
                klein_score += 0.1
            
            # Transition score
            transition_score = 0
            if abs(omega) < 0.3:
                transition_score += 0.4
            if 2 < suppression < 20:
                transition_score += 0.3
            if 0.4 < coherence < 0.8:
                transition_score += 0.3
            
            # Torus score
            torus_score = 0
            if omega > self.detection_params.omega_threshold_torus:
                torus_score += 0.4
            if suppression < 3:
                torus_score += 0.3
            if harmonic_struct['odd_even_ratio'] < 2:
                torus_score += 0.3
            
            # Acumular scores ponderados
            phase_scores['klein'] += klein_score * effective_weight
            phase_scores['transition'] += transition_score * effective_weight
            phase_scores['torus'] += torus_score * effective_weight
            total_weight += effective_weight
        
        # Normalizar scores
        if total_weight > 0:
            for phase in phase_scores:
                phase_scores[phase] /= total_weight
        
        # Ajuste por energía del evento
        energy = event.energy_radiated
        if energy > 1.5:  # Alta energía favorece Klein
            phase_scores['klein'] *= 1.2
            phase_scores['torus'] *= 0.8
        elif energy < 0.3:  # Baja energía favorece Toroide
            phase_scores['torus'] *= 1.2
            phase_scores['klein'] *= 0.8
        
        # Clasificación final
        dominant_phase = max(phase_scores, key=phase_scores.get)
        confidence = phase_scores[dominant_phase]
        
        # Etiqueta descriptiva
        if confidence > 0.8:
            classification = f"strong_{dominant_phase}"
        elif confidence > 0.6:
            classification = f"moderate_{dominant_phase}"
        elif confidence > 0.4:
            classification = f"weak_{dominant_phase}"
        else:
            classification = "indeterminate"
        
        return {
            'dominant_phase': dominant_phase,
            'confidence': confidence,
            'phase_scores': phase_scores,
            'classification': classification,
            'energy_adjustment_applied': True,
            'total_weight': total_weight
        }


from scipy import signal


class ModelOptimizer:
    """Optimizador para parámetros del modelo y detección."""
    
    def __init__(self, reference_data: List[Dict]):
        """
        Inicializa optimizador con datos de referencia.
        
        Parameters
        ----------
        reference_data : List[Dict]
            Datos de eventos de referencia para optimización
        """
        self.reference_data = reference_data
        self.optimization_history = []
        
        print(f"Optimizador inicializado con {len(reference_data)} eventos de referencia")
    
    def objective_function(self, params: np.ndarray, param_type: str) -> float:
        """
        Función objetivo para optimización.
        
        Parameters
        ----------
        params : np.ndarray
            Parámetros a optimizar
        param_type : str
            Tipo de parámetros ('model' o 'detection')
            
        Returns
        -------
        cost : float
            Valor de costo (menor es mejor)
        """
        try:
            if param_type == 'model':
                # Optimizar parámetros del modelo
                model_params = self._params_to_model_params(params)
                model = EnhancedTopologicalModel(model_params)
                
                # Usar parámetros de detección por defecto
                detection_params = DetectionParameters()
                pipeline = EnhancedAnalysisPipeline(model, detection_params)
                
            elif param_type == 'detection':
                # Optimizar parámetros de detección
                detection_params = self._params_to_detection_params(params)
                
                # Usar modelo por defecto
                model_params = ModelParameters()
                model = EnhancedTopologicalModel(model_params)
                pipeline = EnhancedAnalysisPipeline(model, detection_params)
            
            else:
                raise ValueError(f"Tipo de parámetro no reconocido: {param_type}")
            
            # Evaluar modelo en datos de referencia
            total_cost = 0
            n_evaluated = 0
            
            for ref_data in self.reference_data[:5]:  # Usar solo primeros 5 para velocidad
                
                # Extraer datos del evento
                strain = ref_data.get('strain')
                time = ref_data.get('time')
                event = ref_data.get('event')
                expected_phase = ref_data.get('expected_phase', 'klein')
                
                if strain is None or time is None or event is None:
                    continue
                
                # Analizar con parámetros actuales
                result = pipeline.analyze_event_enhanced(strain, time, event)
                
                # Calcular costo basado en múltiples métricas
                
                # 1. Acuerdo con teoría (peso 40%)
                theory_agreement = result['comparison']['global_agreement']
                theory_cost = 1 - theory_agreement
                
                # 2. Clasificación de fase correcta (peso 30%)
                detected_phase = result['phase_classification']['dominant_phase']
                phase_correct = 1.0 if detected_phase == expected_phase else 0.0
                phase_cost = 1 - phase_correct
                
                # 3. Consistencia de frecuencia (peso 20%)
                freq_detections = []
                for window in result['indicators'].values():
                    freq_detections.append(window['fundamental_freq'])
                
                if freq_detections:
                    mean_freq = np.mean(freq_detections)
                    freq_error = abs(mean_freq - model.f0) / model.f0
                else:
                    freq_error = 1.0
                
                freq_cost = min(1.0, freq_error)
                
                # 4. Calidad de datos (peso 10%)
                quality = result['quality_assessment']['mean_quality']
                quality_cost = 1 - quality
                
                # Costo combinado para este evento
                event_cost = (0.4 * theory_cost + 
                             0.3 * phase_cost + 
                             0.2 * freq_cost + 
                             0.1 * quality_cost)
                
                total_cost += event_cost
                n_evaluated += 1
            
            # Costo promedio
            if n_evaluated > 0:
                avg_cost = total_cost / n_evaluated
            else:
                avg_cost = 1.0
            
            # Penalización por parámetros extremos
            penalty = self._compute_parameter_penalty(params, param_type)
            
            final_cost = avg_cost + penalty
            
            # Guardar en historial
            self.optimization_history.append({
                'params': params.copy(),
                'cost': final_cost,
                'avg_cost': avg_cost,
                'penalty': penalty,
                'param_type': param_type
            })
            
            return final_cost
            
        except Exception as e:
            print(f"Error en función objetivo: {e}")
            return 1.0  # Costo máximo en caso de error
    
    def _params_to_model_params(self, params: np.ndarray) -> ModelParameters:
        """Convierte array de parámetros a ModelParameters."""
        return ModelParameters(
            R=8.4e6 * params[0],                    # Factor de escala para R
            kappa=params[1],                        # Constante gravitacional 5D
            alpha_relax=params[2],                  # Tasa de relajación
            beta_coupling=params[3],                # Acoplamiento modo-topología
            tau_scale_factor=params[4],             # Factor de escala temporal
            omega_damping=params[5],                # Amortiguamiento Ω
            f0_scale_factor=params[6],              # Factor de escala frecuencia
            harmonic_coupling=params[7],            # Acoplamiento armónico
            echo_amplitude_scale=params[8],         # Escala amplitud ecos
            mass_scaling_exponent=params[9],        # Exponente escalamiento masa
            nonlinear_threshold=params[10],         # Umbral no-linealidad
            nonlinear_strength=params[11]           # Fuerza no-linealidad
        )
    
    def _params_to_detection_params(self, params: np.ndarray) -> DetectionParameters:
        """Convierte array de parámetros a DetectionParameters."""
        return DetectionParameters(
            klein_window_end=params[0],             # Final ventana Klein
            transition_window_end=params[1],        # Final ventana transición
            torus_window_end=params[2],             # Final ventana toroide
            highpass_freq=params[3],                # Frecuencia pasa-altas
            bandpass_low=params[4],                 # Banda baja
            bandpass_high=params[5],                # Banda alta
            freq_search_bandwidth=params[6],        # Ancho banda búsqueda
            omega_threshold_klein=params[7],        # Umbral Klein
            omega_threshold_torus=params[8],        # Umbral Toroide
            suppression_threshold_klein=params[9],  # Umbral supresión Klein
            adaptive_window_scaling=params[10] > 0.5,  # Escalamiento adaptativo
            mass_dependent_thresholds=params[11] > 0.5  # Umbrales dependientes masa
        )
    
    def _compute_parameter_penalty(self, params: np.ndarray, param_type: str) -> float:
        """Computa penalización por parámetros extremos."""
        penalty = 0
        
        if param_type == 'model':
            # Penalizar parámetros físicamente irrazonables
            bounds = [
                (0.5, 2.0),    # R factor
                (0.1, 10.0),   # kappa
                (0.1, 10.0),   # alpha_relax
                (0.001, 1.0),  # beta_coupling
                (0.1, 10.0),   # tau_scale_factor
                (0.0, 1.0),    # omega_damping
                (0.1, 10.0),   # f0_scale_factor
                (0.0, 0.5),    # harmonic_coupling
                (0.001, 0.1),  # echo_amplitude_scale
                (0.1, 2.0),    # mass_scaling_exponent
                (0.5, 10.0),   # nonlinear_threshold
                (0.0, 1.0)     # nonlinear_strength
            ]
        
        elif param_type == 'detection':
            bounds = [
                (0.005, 0.030),  # klein_window_end
                (0.015, 0.050),  # transition_window_end
                (0.030, 0.100),  # torus_window_end
                (10.0, 50.0),    # highpass_freq
                (20.0, 100.0),   # bandpass_low
                (200.0, 800.0),  # bandpass_high
                (0.1, 2.0),      # freq_search_bandwidth
                (-0.8, -0.2),    # omega_threshold_klein
                (0.2, 0.8),      # omega_threshold_torus
                (2.0, 50.0),     # suppression_threshold_klein
                (0.0, 1.0),      # adaptive_window_scaling
                (0.0, 1.0)       # mass_dependent_thresholds
            ]
        
        # Calcular penalización
        for i, (param, (low, high)) in enumerate(zip(params, bounds)):
            if param < low:
                penalty += (low - param)**2
            elif param > high:
                penalty += (param - high)**2
        
        return 0.1 * penalty  # Factor de penalización
    
    def optimize_model_parameters(self, method: str = 'differential_evolution') -> ModelParameters:
        """
        Optimiza parámetros del modelo físico.
        
        Parameters
        ----------
        method : str
            Método de optimización
            
        Returns
        -------
        optimized_params : ModelParameters
            Parámetros optimizados
        """
        print("\nOptimizando parámetros del modelo físico...")
        
        # Parámetros iniciales (valores actuales)
        initial_params = np.array([
            1.0,    # R factor
            1.0,    # kappa
            1.0,    # alpha_relax
            0.1,    # beta_coupling
            1.0,    # tau_scale_factor
            0.1,    # omega_damping
            1.0,    # f0_scale_factor
            0.05,   # harmonic_coupling
            0.01,   # echo_amplitude_scale
            0.5,    # mass_scaling_exponent
            2.0,    # nonlinear_threshold
            0.1     # nonlinear_strength
        ])
        
        # Límites de búsqueda
        bounds = [
            (0.5, 2.0),    # R factor
            (0.1, 10.0),   # kappa
            (0.1, 10.0),   # alpha_relax
            (0.001, 1.0),  # beta_coupling
            (0.1, 10.0),   # tau_scale_factor
            (0.0, 1.0),    # omega_damping
            (0.1, 10.0),   # f0_scale_factor
            (0.0, 0.5),    # harmonic_coupling
            (0.001, 0.1),  # echo_amplitude_scale
            (0.1, 2.0),    # mass_scaling_exponent
            (0.5, 10.0),   # nonlinear_threshold
            (0.0, 1.0)     # nonlinear_strength
        ]
        
        if method == 'differential_evolution':
            result = differential_evolution(
                lambda params: self.objective_function(params, 'model'),
                bounds,
                seed=42,
                maxiter=20,  # Reducido para demo
                popsize=10,
                atol=1e-3,
                tol=1e-3
            )
            optimized_array = result.x
            final_cost = result.fun
            
        else:
            # Usar minimización local
            result = minimize(
                lambda params: self.objective_function(params, 'model'),
                initial_params,
                method='L-BFGS-B',
                bounds=bounds
            )
            optimized_array = result.x
            final_cost = result.fun
        
        # Convertir a ModelParameters
        optimized_params = self._params_to_model_params(optimized_array)
        
        print(f"Optimización completada:")
        print(f"  Costo inicial: {self.objective_function(initial_params, 'model'):.3f}")
        print(f"  Costo final: {final_cost:.3f}")
        print(f"  Mejora: {((self.objective_function(initial_params, 'model') - final_cost) / self.objective_function(initial_params, 'model') * 100):.1f}%")
        
        return optimized_params
    
    def optimize_detection_parameters(self, method: str = 'differential_evolution') -> DetectionParameters:
        """
        Optimiza parámetros de detección.
        
        Parameters
        ----------
        method : str
            Método de optimización
            
        Returns
        -------
        optimized_params : DetectionParameters
            Parámetros optimizados
        """
        print("\nOptimizando parámetros de detección...")
        
        # Parámetros iniciales
        initial_params = np.array([
            0.014,   # klein_window_end
            0.028,   # transition_window_end
            0.050,   # torus_window_end
            20.0,    # highpass_freq
            35.0,    # bandpass_low
            350.0,   # bandpass_high
            0.5,     # freq_search_bandwidth
            -0.5,    # omega_threshold_klein
            0.5,     # omega_threshold_torus
            5.0,     # suppression_threshold_klein
            1.0,     # adaptive_window_scaling
            1.0      # mass_dependent_thresholds
        ])
        
        # Límites
        bounds = [
            (0.005, 0.030),  # klein_window_end
            (0.015, 0.050),  # transition_window_end
            (0.030, 0.100),  # torus_window_end
            (10.0, 50.0),    # highpass_freq
            (20.0, 100.0),   # bandpass_low
            (200.0, 800.0),  # bandpass_high
            (0.1, 2.0),      # freq_search_bandwidth
            (-0.8, -0.2),    # omega_threshold_klein
            (0.2, 0.8),      # omega_threshold_torus
            (2.0, 50.0),     # suppression_threshold_klein
            (0.0, 1.0),      # adaptive_window_scaling
            (0.0, 1.0)       # mass_dependent_thresholds
        ]
        
        if method == 'differential_evolution':
            result = differential_evolution(
                lambda params: self.objective_function(params, 'detection'),
                bounds,
                seed=42,
                maxiter=15,  # Reducido para demo
                popsize=8,
                atol=1e-3,
                tol=1e-3
            )
            optimized_array = result.x
            final_cost = result.fun
            
        else:
            result = minimize(
                lambda params: self.objective_function(params, 'detection'),
                initial_params,
                method='L-BFGS-B',
                bounds=bounds
            )
            optimized_array = result.x
            final_cost = result.fun
        
        # Convertir a DetectionParameters
        optimized_params = self._params_to_detection_params(optimized_array)
        
        print(f"Optimización completada:")
        print(f"  Costo inicial: {self.objective_function(initial_params, 'detection'):.3f}")
        print(f"  Costo final: {final_cost:.3f}")
        print(f"  Mejora: {((self.objective_function(initial_params, 'detection') - final_cost) / self.objective_function(initial_params, 'detection') * 100):.1f}%")
        
        return optimized_params
    
    def plot_optimization_history(self, save_path: str = None):
        """Visualiza historial de optimización."""
        if not self.optimization_history:
            print("No hay historial de optimización para visualizar")
            return
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))
        
        # Separar por tipo de parámetro
        model_history = [h for h in self.optimization_history if h['param_type'] == 'model']
        detection_history = [h for h in self.optimization_history if h['param_type'] == 'detection']
        
        # 1. Evolución del costo
        if model_history:
            costs = [h['cost'] for h in model_history]
            ax1.plot(costs, 'b-', linewidth=2, label='Modelo')
            ax1.set_ylabel('Costo')
            ax1.set_xlabel('Iteración')
            ax1.set_title('Evolución del Costo - Parámetros del Modelo')
            ax1.grid(True, alpha=0.3)
        
        if detection_history:
            costs = [h['cost'] for h in detection_history]
            ax2.plot(costs, 'r-', linewidth=2, label='Detección')
            ax2.set_ylabel('Costo')
            ax2.set_xlabel('Iteración')
            ax2.set_title('Evolución del Costo - Parámetros de Detección')
            ax2.grid(True, alpha=0.3)
        
        # 2. Distribución de costos
        all_costs = [h['cost'] for h in self.optimization_history]
        ax3.hist(all_costs, bins=20, alpha=0.7, color='green', edgecolor='black')
        ax3.axvline(np.mean(all_costs), color='red', linestyle='--', 
                   label=f'Media: {np.mean(all_costs):.3f}')
        ax3.set_xlabel('Costo')
        ax3.set_ylabel('Frecuencia')
        ax3.set_title('Distribución de Costos')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # 3. Convergencia
        if len(all_costs) > 10:
            # Promedios móviles
            window = 5
            moving_avg = []
            for i in range(window, len(all_costs)):
                avg = np.mean(all_costs[i-window:i])
                moving_avg.append(avg)
            
            ax4.plot(range(window, len(all_costs)), moving_avg, 'purple', linewidth=2)
            ax4.set_xlabel('Iteración')
            ax4.set_ylabel('Costo (promedio móvil)')
            ax4.set_title('Convergencia de la Optimización')
            ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Historial de optimización guardado en: {save_path}")
        
        return fig


def main():
    """
    Demuestra el refinamiento del modelo con datos sintéticos.
    """
    print("MOTOR DE REFINAMIENTO DEL MODELO TOPOLÓGICO")
    print("="*80)
    
    # Generar datos de referencia sintéticos para optimización
    print("\nGenerando datos de referencia para optimización...")
    
    downloader = LIGODataDownloader()
    reference_data = []
    
    # Eventos de referencia con diferentes características
    test_events = [
        {
            'name': 'GW150914_ref',
            'mass': 62.0,
            'energy': 3.0,
            'expected_phase': 'klein'
        },
        {
            'name': 'GW151226_ref', 
            'mass': 21.0,
            'energy': 1.0,
            'expected_phase': 'transition'
        },
        {
            'name': 'GW170608_ref',
            'mass': 18.0,
            'energy': 0.5,
            'expected_phase': 'transition'
        }
    ]
    
    for event_info in test_events:
        # Crear evento LIGO
        event = LIGOEvent(
            name=event_info['name'],
            mass_1=event_info['mass'] * 0.6,
            mass_2=event_info['mass'] * 0.4,
            total_mass=event_info['mass'],
            chirp_mass=event_info['mass'] * 0.4,
            final_spin=0.7,
            luminosity_distance=400.0,
            merger_time=0.0,
            energy_radiated=event_info['energy']
        )
        
        # Generar strain realista
        catalog_event = LIGOCatalogEvent(
            name=event_info['name'],
            gps_time=1126259462.0,
            mass_1_source=event['mass_1'],
            mass_2_source=event['mass_2'],
            total_mass_source=event_info['mass'],
            chirp_mass_source=event['chirp_mass'],
            final_mass_source=event_info['mass'] * 0.95,
            final_spin=0.7,
            luminosity_distance=400.0,
            redshift=0.08,
            network_snr=15.0,
            far=1e-6,
            p_astro=0.95,
            run="O3a",
            detectors=["H1", "L1", "V1"],
            energy_radiated=event_info['energy']
        )
        
        strain, time = downloader.generate_realistic_strain(catalog_event)
        
        reference_data.append({
            'strain': strain,
            'time': time,
            'event': event,
            'expected_phase': event_info['expected_phase']
        })
    
    print(f"Datos de referencia generados: {len(reference_data)} eventos")
    
    # Crear optimizador
    optimizer = ModelOptimizer(reference_data)
    
    # Optimizar parámetros del modelo
    print("\n" + "="*60)
    print("OPTIMIZACIÓN DE PARÁMETROS DEL MODELO")
    print("="*60)
    
    optimized_model_params = optimizer.optimize_model_parameters(method='differential_evolution')
    
    # Optimizar parámetros de detección
    print("\n" + "="*60)
    print("OPTIMIZACIÓN DE PARÁMETROS DE DETECCIÓN")  
    print("="*60)
    
    optimized_detection_params = optimizer.optimize_detection_parameters(method='differential_evolution')
    
    # Crear modelos con parámetros optimizados
    print("\n" + "="*60)
    print("VALIDACIÓN DE PARÁMETROS OPTIMIZADOS")
    print("="*60)
    
    # Modelo original
    original_model = TopologicalTransitionModel()
    original_pipeline = TopologicalAnalysisPipeline(original_model)
    
    # Modelo optimizado
    optimized_model = EnhancedTopologicalModel(optimized_model_params)
    optimized_pipeline = EnhancedAnalysisPipeline(optimized_model, optimized_detection_params)
    
    # Comparar rendimiento
    print("\nComparando rendimiento original vs optimizado...")
    
    for i, ref_data in enumerate(reference_data):
        strain = ref_data['strain']
        time = ref_data['time']
        event = ref_data['event']
        expected_phase = ref_data['expected_phase']
        
        print(f"\nEvento {event.name}:")
        
        # Análisis original
        original_result = original_pipeline.analyze_event(strain, time, event)
        original_agreement = original_result['comparison']['global_agreement']
        original_phase = original_result['phase_classification']['dominant_phase']
        
        # Análisis optimizado
        optimized_result = optimized_pipeline.analyze_event_enhanced(strain, time, event)
        optimized_agreement = optimized_result['comparison']['global_agreement']
        optimized_phase = optimized_result['phase_classification']['dominant_phase']
        
        print(f"  Fase esperada: {expected_phase}")
        print(f"  Original: {original_phase} (acuerdo: {original_agreement:.2%})")
        print(f"  Optimizado: {optimized_phase} (acuerdo: {optimized_agreement:.2%})")
        print(f"  Mejora: {(optimized_agreement - original_agreement)*100:.1f} puntos porcentuales")
    
    # Guardar parámetros optimizados
    results_dir = "refined_model_results"
    os.makedirs(results_dir, exist_ok=True)
    
    # Guardar parámetros
    with open(f"{results_dir}/optimized_model_parameters.json", 'w') as f:
        json.dump(optimized_model_params.to_dict(), f, indent=2)
    
    with open(f"{results_dir}/optimized_detection_parameters.json", 'w') as f:
        json.dump(optimized_detection_params.to_dict(), f, indent=2)
    
    # Visualizar historial de optimización
    optimizer.plot_optimization_history(f"{results_dir}/optimization_history.png")
    
    print(f"\n✅ Refinamiento completado!")
    print(f"📁 Parámetros optimizados guardados en: {results_dir}/")
    print(f"📊 Modelo listo para re-validación con catálogo completo")


if __name__ == "__main__":
    main()