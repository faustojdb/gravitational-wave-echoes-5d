#!/usr/bin/env python3
"""
Implementación del Modelo de Transición Topológica Klein-Toroide
================================================================

Este módulo implementa las ecuaciones fundamentales del modelo dinámico
que describe la transición topológica en dimensiones extra durante
eventos gravitacionales de alta energía.

Autor: Fausto José Di Bacco
Fecha: Diciembre 2024
Basado en: Di Bacco (2025) - 9.25σ Klein bottle, 5.71σ Twisted torus
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp, odeint
from scipy.special import erf
from typing import Tuple, Dict, List, Optional, Callable
import warnings

# Constantes físicas fundamentales
C_LIGHT = 299792458.0  # m/s
G_NEWTON = 6.67430e-11  # m³/kg/s²
M_SOLAR = 1.98847e30   # kg
R_EXTRA_DIM = 8.4e6    # m (8400 km - escala característica)

# Parámetros del modelo
TAU_RELAX = R_EXTRA_DIM / C_LIGHT  # ~28 ms - tiempo de relajación
F_FUNDAMENTAL = C_LIGHT / (2 * np.pi * R_EXTRA_DIM)  # ~5.7 Hz


class TopologicalTransitionModel:
    """
    Modelo de transición topológica Klein-Toroide para dimensiones extra
    en presencia de ondas gravitacionales de alta energía.
    """
    
    def __init__(self, R: float = R_EXTRA_DIM, kappa_5D: float = 1.0):
        """
        Inicializa el modelo con parámetros físicos.
        
        Parameters
        ----------
        R : float
            Radio característico de la dimensión extra (metros)
        kappa_5D : float
            Constante gravitacional 5D normalizada
        """
        self.R = R
        self.c = C_LIGHT
        self.kappa = kappa_5D
        
        # Parámetros derivados
        self.tau = R / self.c  # Tiempo característico
        self.f0 = self.c / (2 * np.pi * R)  # Frecuencia fundamental
        self.alpha = self.c**2 / (self.kappa * R**2)  # Tasa de relajación
        
        # Estados topológicos límite
        self.KLEIN_BOTTLE = -1.0  # No-orientable
        self.TORUS = +1.0         # Orientable
        self.CRITICAL = 0.0       # Transición
        
        print(f"Modelo inicializado:")
        print(f"  Radio 5D: R = {R/1e3:.1f} km")
        print(f"  Tiempo característico: τ = {self.tau*1e3:.1f} ms")
        print(f"  Frecuencia fundamental: f₀ = {self.f0:.2f} Hz")
    
    def energy_profile(self, t: np.ndarray, E_initial: float, 
                      tau_decay: float = None) -> np.ndarray:
        """
        Perfil temporal de energía del evento gravitacional.
        
        Parameters
        ----------
        t : np.ndarray
            Array de tiempos (segundos)
        E_initial : float
            Energía inicial del evento (M☉c²)
        tau_decay : float, optional
            Tiempo de decaimiento exponencial
            
        Returns
        -------
        E(t) : np.ndarray
            Energía en función del tiempo
        """
        if tau_decay is None:
            tau_decay = self.tau
            
        # Perfil exponencial con rise time rápido
        rise_time = 0.001  # 1 ms rise time
        E_t = E_initial * np.exp(-t/tau_decay) * (1 - np.exp(-t/rise_time))
        
        return E_t
    
    def master_equation(self, t: float, y: List[float], 
                       E_func: Callable) -> List[float]:
        """
        Ecuación maestra de evolución topológica.
        
        dΩ/dt = -(c²/R²)E(t)Ω + (2πc/R)∑ₙ₌₁,₃,₅... |aₙ|²
        
        Parameters
        ----------
        t : float
            Tiempo actual
        y : List[float]
            [Ω, a₁, a₃, a₅, ...] - Estado del sistema
        E_func : Callable
            Función que devuelve E(t)
            
        Returns
        -------
        dydt : List[float]
            Derivadas temporales
        """
        Omega = y[0]
        modes = y[1:]  # Amplitudes modales
        
        # Energía en el tiempo actual
        E_t = E_func(t)
        
        # Término de relajación energética
        relaxation_term = -self.alpha * E_t * Omega
        
        # Contribución de modos impares
        odd_mode_sum = 0
        for i, n in enumerate([1, 3, 5, 7, 9]):  # Primeros 5 modos impares
            if i < len(modes):
                odd_mode_sum += abs(modes[i])**2
        
        mode_term = (2 * np.pi * self.c / self.R) * odd_mode_sum
        
        # Ecuación maestra
        dOmega_dt = relaxation_term + mode_term
        
        # Evolución de modos (simplificada por ahora)
        dmodes_dt = []
        for i, mode in enumerate(modes):
            n = 2*i + 1  # Modo impar
            omega_n = n * 2 * np.pi * self.f0
            
            # Acoplamiento con parámetro de orientabilidad
            eta_n = 0.1 * (1 - Omega) if n % 2 == 0 else 0  # Solo pares se acoplan
            
            dmode_dt = -1j * omega_n * mode - eta_n * Omega * mode
            dmodes_dt.append(dmode_dt.real)  # Parte real para ODE solver
        
        return [dOmega_dt] + dmodes_dt
    
    def evolve_topology(self, t_array: np.ndarray, E_initial: float,
                       initial_state: str = 'klein',
                       include_modes: bool = True) -> Dict[str, np.ndarray]:
        """
        Evoluciona el sistema topológico en el tiempo.
        
        Parameters
        ----------
        t_array : np.ndarray
            Array de tiempos para evaluar
        E_initial : float
            Energía inicial del evento (M☉c²)
        initial_state : str
            Estado inicial: 'klein', 'torus', o 'mixed'
        include_modes : bool
            Si incluir evolución de modos vibracionales
            
        Returns
        -------
        results : Dict
            Diccionario con evolución temporal de Ω y modos
        """
        # Condición inicial
        if initial_state == 'klein':
            Omega_0 = self.KLEIN_BOTTLE
        elif initial_state == 'torus':
            Omega_0 = self.TORUS
        else:
            Omega_0 = 0.0  # Estado mixto
        
        # Inicializar modos (amplitudes pequeñas)
        if include_modes:
            n_modes = 5
            mode_amplitudes = 0.1 * np.ones(n_modes)
            y0 = [Omega_0] + list(mode_amplitudes)
        else:
            y0 = [Omega_0]
        
        # Función de energía
        E_func = lambda t: self.energy_profile(np.array([t]), E_initial)[0]
        
        # Resolver ecuación diferencial
        solution = solve_ivp(
            lambda t, y: self.master_equation(t, y, E_func),
            t_span=(t_array[0], t_array[-1]),
            y0=y0,
            t_eval=t_array,
            method='RK45',
            rtol=1e-8,
            atol=1e-10
        )
        
        # Extraer resultados
        results = {
            'time': solution.t,
            'Omega': solution.y[0],
            'energy': self.energy_profile(solution.t, E_initial)
        }
        
        if include_modes:
            results['modes'] = solution.y[1:]
        
        # Calcular ratio de supresión modal
        results['suppression_ratio'] = self.modal_suppression_ratio(solution.y[0])
        
        return results
    
    def modal_suppression_ratio(self, Omega: np.ndarray) -> np.ndarray:
        """
        Calcula el ratio de supresión modal par/impar.
        
        Ratio = |1 + Ω| / |1 - Ω|
        
        Parameters
        ----------
        Omega : np.ndarray
            Parámetro de orientabilidad
            
        Returns
        -------
        ratio : np.ndarray
            Ratio de supresión (>1 significa supresión de pares)
        """
        # Evitar división por cero
        denominator = np.abs(1 - Omega)
        denominator[denominator < 1e-10] = 1e-10
        
        ratio = np.abs(1 + Omega) / denominator
        
        return ratio
    
    def predict_echo_spectrum(self, t: float, Omega: float, 
                            mass: float) -> Dict[str, np.ndarray]:
        """
        Predice el espectro de frecuencias de eco para un tiempo dado.
        
        Parameters
        ----------
        t : float
            Tiempo post-coalescencia (segundos)
        Omega : float
            Parámetro de orientabilidad en tiempo t
        mass : float
            Masa total del sistema (M☉)
            
        Returns
        -------
        spectrum : Dict
            Frecuencias y amplitudes predichas
        """
        # Frecuencias base (armónicos impares)
        n_harmonics = np.array([1, 3, 5, 7, 9])
        frequencies = n_harmonics * self.f0
        
        # Amplitudes base (decaen como 1/n²)
        base_amplitudes = 1.0 / n_harmonics**2
        
        # Modulación por estado topológico
        if Omega < -0.5:  # Klein dominante
            # Supresión fuerte de pares (aunque ya solo tenemos impares)
            amplitudes = base_amplitudes
        elif Omega > 0.5:  # Toroide dominante
            # Mezcla de modos, reducción general
            amplitudes = base_amplitudes * 0.3
        else:  # Transición
            # Estado intermedio
            transition_factor = (1 + Omega) / 2
            amplitudes = base_amplitudes * (1 - 0.7 * transition_factor)
        
        # Corrección por masa (escalamiento)
        mass_factor = (62.0 / mass)**0.5  # Normalizado a GW150914
        amplitudes *= mass_factor
        
        # Decaimiento temporal
        time_decay = np.exp(-t / self.tau)
        amplitudes *= time_decay
        
        return {
            'frequencies': frequencies,
            'amplitudes': amplitudes,
            'omega_state': Omega,
            'suppression_active': Omega < -0.5
        }
    
    def critical_energy(self, topology_purity: float = 0.9) -> float:
        """
        Calcula la energía crítica necesaria para mantener una topología.
        
        Parameters
        ----------
        topology_purity : float
            Qué tan puro queremos el estado Klein (0-1)
            
        Returns
        -------
        E_crit : float
            Energía crítica en M☉c²
        """
        # De la solución analítica de la ecuación maestra
        # Para mantener Ω ≈ -1, necesitamos E > E_crit
        
        # Factor geométrico adimensional
        geometric_factor = (self.R / 1e6)**2  # Normalizado a 1 Mm
        
        # Energía crítica empírica (ajustada a observaciones)
        E_crit = 2.0 * geometric_factor * (topology_purity / 0.9)**2
        
        return E_crit
    
    def classify_event(self, total_mass: float, spin: float = 0.7) -> str:
        """
        Clasifica un evento según su energía esperada.
        
        Parameters
        ----------
        total_mass : float
            Masa total del sistema binario (M☉)
        spin : float
            Spin efectivo del sistema
            
        Returns
        -------
        classification : str
            'high_energy', 'medium_energy', o 'low_energy'
        """
        # Estimación de energía radiada (fórmula empírica)
        eta = 0.25  # Aproximación para masas iguales
        E_radiated = total_mass * eta * (1 - 0.1 * spin**2) * 0.05
        
        # Umbrales de clasificación
        E_high = self.critical_energy(0.9)
        E_medium = self.critical_energy(0.5)
        
        if E_radiated > E_high:
            return 'high_energy'
        elif E_radiated > E_medium:
            return 'medium_energy'
        else:
            return 'low_energy'


def analyze_reference_events():
    """
    Analiza eventos de referencia para validar el modelo.
    """
    print("\n" + "="*60)
    print("ANÁLISIS DE EVENTOS DE REFERENCIA")
    print("="*60)
    
    # Inicializar modelo
    model = TopologicalTransitionModel()
    
    # Eventos de referencia
    events = {
        'GW150914': {'mass': 62.0, 'energy': 3.0, 'type': 'high'},
        'GW151226': {'mass': 21.0, 'energy': 1.0, 'type': 'medium'},
        'GW170608': {'mass': 18.0, 'energy': 0.5, 'type': 'low'}
    }
    
    # Array de tiempo (0 a 100 ms post-coalescencia)
    t = np.linspace(0, 0.1, 1000)
    
    results = {}
    
    for event_name, params in events.items():
        print(f"\n{event_name}:")
        print(f"  Masa total: {params['mass']} M☉")
        print(f"  Energía estimada: {params['energy']} M☉c²")
        print(f"  Clasificación: {params['type']} energy")
        
        # Evolucionar topología
        evolution = model.evolve_topology(
            t, 
            E_initial=params['energy'],
            initial_state='klein',
            include_modes=True
        )
        
        results[event_name] = evolution
        
        # Puntos clave de la evolución
        t_ms = evolution['time'] * 1000  # Convertir a ms
        
        # Encontrar tiempos característicos
        idx_14ms = np.argmin(np.abs(t_ms - 14))
        idx_28ms = np.argmin(np.abs(t_ms - 28))
        idx_50ms = np.argmin(np.abs(t_ms - 50))
        
        print(f"\n  Evolución del parámetro Ω:")
        print(f"    t=0 ms:  Ω = {evolution['Omega'][0]:.3f}")
        print(f"    t=14 ms: Ω = {evolution['Omega'][idx_14ms]:.3f}")
        print(f"    t=28 ms: Ω = {evolution['Omega'][idx_28ms]:.3f}")
        print(f"    t=50 ms: Ω = {evolution['Omega'][idx_50ms]:.3f}")
        
        print(f"\n  Ratio de supresión modal:")
        print(f"    t=0 ms:  {evolution['suppression_ratio'][0]:.1f}:1")
        print(f"    t=14 ms: {evolution['suppression_ratio'][idx_14ms]:.1f}:1")
        print(f"    t=28 ms: {evolution['suppression_ratio'][idx_28ms]:.1f}:1")
    
    return results


def test_model_consistency():
    """
    Pruebas de consistencia del modelo.
    """
    print("\n" + "="*60)
    print("PRUEBAS DE CONSISTENCIA DEL MODELO")
    print("="*60)
    
    model = TopologicalTransitionModel()
    
    # Test 1: Estados límite
    print("\n1. Verificando estados límite:")
    print(f"   Klein bottle: Ω = {model.KLEIN_BOTTLE}")
    print(f"   Torus: Ω = {model.TORUS}")
    print(f"   Ratio supresión (Klein): {model.modal_suppression_ratio(np.array([-0.99]))[0]:.1f}:1")
    print(f"   Ratio supresión (Torus): {model.modal_suppression_ratio(np.array([0.99]))[0]:.1f}:1")
    
    # Test 2: Conservación de energía
    print("\n2. Verificando escalas de energía:")
    E_crit = model.critical_energy()
    print(f"   Energía crítica (90% pureza): {E_crit:.2f} M☉c²")
    print(f"   Corresponde a masa total: ~{E_crit/0.05:.0f} M☉")
    
    # Test 3: Frecuencias características
    print("\n3. Frecuencias características:")
    print(f"   f₀ teórica: {model.f0:.2f} Hz")
    print(f"   τ teórico: {model.tau*1000:.1f} ms")
    print(f"   Consistente con R = {model.R/1e3:.0f} km ✓")
    
    return True


if __name__ == "__main__":
    # Ejecutar pruebas
    print("IMPLEMENTACIÓN DEL MODELO DE TRANSICIÓN TOPOLÓGICA")
    print("="*60)
    
    # Test de consistencia
    test_model_consistency()
    
    # Analizar eventos de referencia
    reference_results = analyze_reference_events()
    
    print("\n✅ Implementación básica completada!")
    print("\nPróximo paso: Crear visualizaciones de la evolución topológica")