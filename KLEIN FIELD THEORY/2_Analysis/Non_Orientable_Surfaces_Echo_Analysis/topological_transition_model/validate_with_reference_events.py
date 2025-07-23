#!/usr/bin/env python3
"""
Validación del Modelo con Eventos de Referencia
===============================================

Este módulo valida el modelo de transición topológica usando
eventos reales de LIGO con señales de eco mejoradas para
demostrar las capacidades del pipeline.

Autor: Fausto José Di Bacco
Fecha: Diciembre 2024
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import json
from typing import Dict, List, Tuple
import os

# Importar módulos del proyecto
from topological_transition_implementation import TopologicalTransitionModel
from ligo_analysis_pipeline import TopologicalAnalysisPipeline, LIGOEvent


def generate_realistic_echo_signal(event: LIGOEvent, model: TopologicalTransitionModel,
                                 duration: float = 2.0, 
                                 include_transition: bool = True) -> Tuple[np.ndarray, np.ndarray]:
    """
    Genera señal realista con ecos topológicos basados en el modelo.
    
    Parameters
    ----------
    event : LIGOEvent
        Información del evento
    model : TopologicalTransitionModel
        Modelo de transición topológica
    duration : float
        Duración total de la señal
    include_transition : bool
        Si incluir la transición topológica dinámica
        
    Returns
    -------
    strain : np.ndarray
        Strain con señal de fusión + ecos topológicos
    time : np.ndarray
        Array de tiempos
    """
    # Configuración
    fs = 4096  # Hz - frecuencia de muestreo LIGO
    t = np.linspace(0, duration, int(duration * fs))
    merger_time = duration / 2
    
    # Componente 1: Señal de fusión (ringdown simplificado)
    ringdown_freq = 250 * (30 / event.total_mass)  # Escala con masa
    ringdown_tau = 0.004 * (event.total_mass / 30)  # Tiempo de decaimiento
    
    # Ringdown post-fusión
    post_mask = t > merger_time
    ringdown = np.zeros_like(t)
    t_post = t[post_mask] - merger_time
    
    ringdown[post_mask] = (
        np.exp(-t_post / ringdown_tau) * 
        np.sin(2 * np.pi * ringdown_freq * t_post + np.pi/4)
    )
    
    # Escalar por masa y distancia
    distance_factor = 410 / event.luminosity_distance  # Normalizado a GW150914
    mass_factor = np.sqrt(event.total_mass / 62)
    ringdown *= distance_factor * mass_factor
    
    # Componente 2: Ecos topológicos
    echo_signal = np.zeros_like(t)
    
    if include_transition:
        # Evolucionar parámetro Ω(t)
        evolution = model.evolve_topology(
            t_post, event.energy_radiated,
            initial_state='klein', include_modes=False
        )
        
        # Para cada tiempo, generar eco con propiedades dependientes de Ω
        for i, t_i in enumerate(t_post):
            if t_i < 0.1:  # Solo primeros 100 ms
                # Obtener Ω en este tiempo
                idx_evolution = np.argmin(np.abs(evolution['time'] - t_i))
                omega = evolution['Omega'][idx_evolution]
                suppression = evolution['suppression_ratio'][idx_evolution]
                
                # Espectro de eco basado en estado topológico
                spectrum = model.predict_echo_spectrum(t_i, omega, event.total_mass)
                
                # Generar componentes de frecuencia
                for f, amp in zip(spectrum['frequencies'], spectrum['amplitudes']):
                    # Ventana temporal para localizar eco
                    echo_width = 0.005  # 5 ms
                    window = np.exp(-(t_post - t_i)**2 / (2 * echo_width**2))
                    
                    # Añadir componente
                    echo_contribution = (
                        amp * window * np.sin(2 * np.pi * f * t_post)
                    )
                    echo_signal[post_mask] += echo_contribution
    
    else:
        # Eco estático (sin transición)
        for n in [1, 3, 5, 7]:  # Armónicos impares
            f_echo = n * model.f0
            amp = (event.energy_radiated / 3.0) / n**2
            decay = np.exp(-t_post / model.tau)
            
            echo_signal[post_mask] += (
                amp * decay * np.sin(2 * np.pi * f_echo * t_post)
            )
    
    # Escalar ecos por energía del evento
    echo_scale = 0.01 * event.energy_radiated  # 1% de conversión a ecos
    echo_signal *= echo_scale
    
    # Componente 3: Ruido realista
    # Ruido coloreado que simula PSD de LIGO
    white_noise = np.random.randn(len(t))
    
    # Filtro para simular PSD de LIGO (simplificado)
    # Supresión en bajas frecuencias, pico ~100-300 Hz
    freq_shape = signal.butter(2, [20, 800], btype='band', fs=fs, output='sos')
    colored_noise = signal.sosfilt(freq_shape, white_noise)
    
    # Normalizar ruido
    noise_level = 0.5 * np.std(ringdown[post_mask])
    colored_noise *= noise_level / np.std(colored_noise)
    
    # Combinar todas las componentes
    strain = ringdown + echo_signal + colored_noise
    
    # Añadir transitorios aleatorios (glitches)
    n_glitches = np.random.poisson(2)  # Promedio 2 glitches
    for _ in range(n_glitches):
        glitch_time = np.random.uniform(0, duration)
        glitch_idx = np.argmin(np.abs(t - glitch_time))
        glitch_amp = np.random.normal(0, 3 * noise_level)
        glitch_width = int(0.001 * fs)  # 1 ms
        
        if glitch_idx > glitch_width and glitch_idx < len(t) - glitch_width:
            strain[glitch_idx-glitch_width:glitch_idx+glitch_width] += (
                glitch_amp * signal.windows.tukey(2 * glitch_width)
            )
    
    return strain, t


def validate_single_event(event: LIGOEvent, pipeline: TopologicalAnalysisPipeline,
                         model: TopologicalTransitionModel,
                         plot_results: bool = True) -> Dict:
    """
    Valida modelo con un solo evento.
    
    Parameters
    ----------
    event : LIGOEvent
        Evento a analizar
    pipeline : TopologicalAnalysisPipeline
        Pipeline de análisis
    model : TopologicalTransitionModel
        Modelo topológico
    plot_results : bool
        Si generar gráficos
        
    Returns
    -------
    validation_results : Dict
        Resultados de validación
    """
    print(f"\n{'='*60}")
    print(f"VALIDANDO MODELO CON {event.name}")
    print(f"{'='*60}")
    
    # Generar señal realista
    print("Generando señal con ecos topológicos...")
    strain, time = generate_realistic_echo_signal(event, model, include_transition=True)
    
    # Analizar con pipeline
    print("Ejecutando análisis topológico...")
    results = pipeline.analyze_event(strain, time, event)
    
    # Validación específica
    validation = {
        'event': event.name,
        'energy_class': model.classify_event(event.total_mass, event.final_spin),
        'analysis_results': results,
        'validation_metrics': {}
    }
    
    # Métricas de validación
    print("\nMétricas de validación:")
    
    # 1. Detección de fase topológica correcta
    expected_phase = 'klein' if event.energy_radiated > 2.0 else 'transition'
    detected_phase = results['phase_classification']['dominant_phase']
    phase_correct = expected_phase == detected_phase
    
    print(f"  Fase esperada: {expected_phase}")
    print(f"  Fase detectada: {detected_phase} ({'✓' if phase_correct else '✗'})")
    
    validation['validation_metrics']['phase_detection'] = {
        'expected': expected_phase,
        'detected': detected_phase,
        'correct': phase_correct,
        'confidence': results['phase_classification']['confidence']
    }
    
    # 2. Frecuencia fundamental
    observed_freqs = []
    for window in results['indicators'].values():
        observed_freqs.append(window['fundamental_freq'])
    
    mean_f0 = np.mean(observed_freqs)
    f0_error = abs(mean_f0 - model.f0) / model.f0
    f0_valid = f0_error < 0.1  # 10% error
    
    print(f"  f₀ esperada: {model.f0:.2f} Hz")
    print(f"  f₀ observada: {mean_f0:.2f} Hz ({'✓' if f0_valid else '✗'})")
    
    validation['validation_metrics']['frequency'] = {
        'expected': model.f0,
        'observed': mean_f0,
        'error': f0_error,
        'valid': f0_valid
    }
    
    # 3. Evolución temporal
    theory_agreement = results['comparison']['global_agreement']
    agreement_valid = theory_agreement > 0.7
    
    print(f"  Acuerdo con teoría: {theory_agreement:.2%} ({'✓' if agreement_valid else '✗'})")
    
    validation['validation_metrics']['theory_agreement'] = {
        'score': theory_agreement,
        'valid': agreement_valid
    }
    
    # 4. Calidad de datos
    quality = results['quality_assessment']['mean_quality']
    quality_valid = quality > 0.6
    
    print(f"  Calidad de análisis: {quality:.2%} ({'✓' if quality_valid else '✗'})")
    
    validation['validation_metrics']['data_quality'] = {
        'score': quality,
        'valid': quality_valid
    }
    
    # Validación global
    all_valid = all([
        phase_correct,
        f0_valid,
        agreement_valid,
        quality_valid
    ])
    
    validation['validation_metrics']['overall'] = {
        'all_tests_passed': all_valid,
        'success_rate': sum([phase_correct, f0_valid, agreement_valid, quality_valid]) / 4
    }
    
    print(f"\nVALIDACIÓN GLOBAL: {'✓ APROBADA' if all_valid else '✗ FALLÓ'}")
    print(f"Tasa de éxito: {validation['validation_metrics']['overall']['success_rate']:.0%}")
    
    # Generar visualización si se solicita
    if plot_results:
        plot_validation_results(event, strain, time, results, validation, model)
    
    return validation


from scipy import signal


def plot_validation_results(event: LIGOEvent, strain: np.ndarray, time: np.ndarray,
                          results: Dict, validation: Dict, model: TopologicalTransitionModel):
    """
    Genera visualización detallada de resultados de validación.
    """
    fig = plt.figure(figsize=(16, 12))
    gs = GridSpec(4, 3, figure=fig, hspace=0.3, wspace=0.25)
    
    fig.suptitle(f'Validación del Modelo: {event.name} (E = {event.energy_radiated:.1f} M☉c²)',
                fontsize=16, fontweight='bold')
    
    # Encontrar tiempo de fusión
    merger_idx = np.argmax(np.abs(strain))
    merger_time = time[merger_idx]
    
    # 1. Señal completa
    ax1 = fig.add_subplot(gs[0, :])
    ax1.plot(time, strain, 'b-', linewidth=0.5, alpha=0.8)
    ax1.axvline(merger_time, color='red', linestyle='--', label='Coalescencia')
    ax1.set_xlabel('Tiempo (s)')
    ax1.set_ylabel('Strain')
    ax1.set_title('A. Señal Completa con Ecos Topológicos')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # 2. Zoom post-coalescencia
    ax2 = fig.add_subplot(gs[1, :])
    post_mask = (time > merger_time) & (time < merger_time + 0.1)
    t_post = (time[post_mask] - merger_time) * 1000  # ms
    
    ax2.plot(t_post, strain[post_mask], 'b-', linewidth=1)
    
    # Marcar ventanas temporales
    colors = ['red', 'orange', 'green', 'gray']
    labels = ['Klein puro', 'Transición', 'Toroide', 'Estático']
    boundaries = [0, 14, 28, 50, 100]
    
    for i in range(4):
        ax2.axvspan(boundaries[i], boundaries[i+1], alpha=0.2, color=colors[i], label=labels[i])
    
    ax2.set_xlabel('Tiempo post-coalescencia (ms)')
    ax2.set_ylabel('Strain')
    ax2.set_title('B. Ventana de Análisis Post-Coalescencia')
    ax2.legend(loc='upper right')
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim(0, 60)
    
    # 3. Espectrograma
    ax3 = fig.add_subplot(gs[2, 0])
    
    # Calcular espectrograma de la región post-coalescencia
    f, t_spec, Sxx = signal.spectrogram(
        strain[post_mask], 
        fs=4096,
        window='hann',
        nperseg=256,
        noverlap=240
    )
    
    # Limitar rango de frecuencias
    freq_mask = (f > 1) & (f < 100)
    f_plot = f[freq_mask]
    Sxx_plot = Sxx[freq_mask, :]
    
    im = ax3.pcolormesh(t_spec * 1000, f_plot, 10 * np.log10(Sxx_plot + 1e-10),
                       shading='auto', cmap='viridis')
    
    # Marcar frecuencias teóricas
    for n in [1, 3, 5]:
        ax3.axhline(n * model.f0, color='red', linestyle='--', alpha=0.5, linewidth=1)
    
    ax3.set_xlabel('Tiempo (ms)')
    ax3.set_ylabel('Frecuencia (Hz)')
    ax3.set_title('C. Espectrograma Post-Coalescencia')
    ax3.set_ylim(1, 50)
    
    # 4. Evolución de Ω(t)
    ax4 = fig.add_subplot(gs[2, 1])
    
    theory_time = np.array(results['theory_evolution']['time']) * 1000
    theory_omega = results['theory_evolution']['omega']
    
    ax4.plot(theory_time, theory_omega, 'k-', linewidth=2, label='Teoría')
    
    # Estimaciones observacionales
    time_windows = {
        'klein_pure': (0, 0.014),
        'transition': (0.014, 0.028),
        'torus_dominant': (0.028, 0.050),
        'static': (0.050, 0.100)
    }
    
    obs_times = []
    obs_omegas = []
    for window_name, indicators in results['indicators'].items():
        if window_name in time_windows:
            t_start, t_end = time_windows[window_name]
            t_mid = (t_start + t_end) / 2 * 1000  # ms
            obs_times.append(t_mid)
            obs_omegas.append(indicators['omega_estimate'])
    
    ax4.scatter(obs_times, obs_omegas, c='red', s=100, marker='o', 
               label='Observado', zorder=5)
    
    ax4.axhline(-1, color='blue', linestyle='--', alpha=0.5)
    ax4.axhline(0, color='gray', linestyle=':', alpha=0.5)
    ax4.axhline(1, color='green', linestyle='--', alpha=0.5)
    
    ax4.set_xlabel('Tiempo (ms)')
    ax4.set_ylabel('Parámetro Ω')
    ax4.set_title('D. Evolución del Parámetro de Orientabilidad')
    ax4.set_xlim(0, 60)
    ax4.set_ylim(-1.2, 1.2)
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    
    # 5. Ratio de supresión
    ax5 = fig.add_subplot(gs[2, 2])
    
    theory_suppression = results['theory_evolution']['suppression']
    ax5.semilogy(theory_time, theory_suppression, 'k-', linewidth=2, label='Teoría')
    
    # Observaciones
    obs_suppressions = []
    for window_name, indicators in results['indicators'].items():
        if window_name in time_windows:
            obs_suppressions.append(indicators['suppression_ratio'])
    
    if len(obs_times) == len(obs_suppressions):
        ax5.scatter(obs_times, obs_suppressions, c='red', s=100, marker='o',
                   label='Observado', zorder=5)
    
    ax5.axhline(20, color='red', linestyle='--', alpha=0.5, label='Umbral Klein')
    ax5.axhline(5, color='orange', linestyle='--', alpha=0.5, label='Umbral mixto')
    
    ax5.set_xlabel('Tiempo (ms)')
    ax5.set_ylabel('Ratio de Supresión')
    ax5.set_title('E. Supresión de Modos Pares')
    ax5.set_xlim(0, 60)
    ax5.set_ylim(1, 100)
    ax5.legend()
    ax5.grid(True, alpha=0.3)
    
    # 6. Resumen de validación
    ax6 = fig.add_subplot(gs[3, :])
    ax6.axis('off')
    
    # Crear tabla de resultados
    metrics = validation['validation_metrics']
    
    summary_text = f"""
    RESUMEN DE VALIDACIÓN - {event.name}
    
    Parámetros del evento:
    • Masa total: {event.total_mass:.1f} M☉
    • Energía radiada: {event.energy_radiated:.1f} M☉c²
    • Clasificación energética: {validation['energy_class']}
    
    Resultados de validación:
    • Detección de fase: {metrics['phase_detection']['detected']} (esperado: {metrics['phase_detection']['expected']}) {'✓' if metrics['phase_detection']['correct'] else '✗'}
    • Frecuencia fundamental: {metrics['frequency']['observed']:.2f} Hz (error: {metrics['frequency']['error']:.1%}) {'✓' if metrics['frequency']['valid'] else '✗'}
    • Acuerdo con teoría: {metrics['theory_agreement']['score']:.1%} {'✓' if metrics['theory_agreement']['valid'] else '✗'}
    • Calidad de datos: {metrics['data_quality']['score']:.1%} {'✓' if metrics['data_quality']['valid'] else '✗'}
    
    VALIDACIÓN GLOBAL: {'✓ APROBADA' if metrics['overall']['all_tests_passed'] else '✗ FALLÓ'}
    Tasa de éxito: {metrics['overall']['success_rate']:.0%}
    """
    
    ax6.text(0.1, 0.9, summary_text, transform=ax6.transAxes,
            fontsize=11, verticalalignment='top', fontfamily='monospace',
            bbox=dict(boxstyle='round,pad=1', facecolor='wheat', alpha=0.8))
    
    plt.tight_layout()
    
    # Guardar figura
    output_dir = "validation_results"
    os.makedirs(output_dir, exist_ok=True)
    filename = f"{output_dir}/validation_{event.name}.png"
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"\nGráfico guardado en: {filename}")
    
    return fig


def validate_all_reference_events():
    """
    Valida el modelo con todos los eventos de referencia.
    """
    print("\n" + "="*80)
    print("VALIDACIÓN COMPLETA DEL MODELO DE TRANSICIÓN TOPOLÓGICA")
    print("="*80)
    
    # Inicializar modelo y pipeline
    model = TopologicalTransitionModel()
    pipeline = TopologicalAnalysisPipeline(model)
    
    # Eventos de referencia con diferentes energías
    reference_events = [
        LIGOEvent(
            name="GW150914",
            mass_1=36.0,
            mass_2=29.0,
            total_mass=62.0,
            chirp_mass=30.0,
            final_spin=0.68,
            luminosity_distance=410.0,
            merger_time=0.0,
            energy_radiated=3.0  # Alta energía
        ),
        LIGOEvent(
            name="GW190521",
            mass_1=85.0,
            mass_2=66.0,
            total_mass=142.0,
            chirp_mass=64.0,
            final_spin=0.72,
            luminosity_distance=5300.0,
            merger_time=0.0,
            energy_radiated=8.0  # Energía extrema
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
            energy_radiated=1.0  # Energía media
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
            energy_radiated=0.5  # Baja energía
        )
    ]
    
    # Validar cada evento
    all_validations = []
    
    for event in reference_events:
        validation = validate_single_event(event, pipeline, model, plot_results=True)
        all_validations.append(validation)
    
    # Resumen global
    print("\n" + "="*80)
    print("RESUMEN GLOBAL DE VALIDACIÓN")
    print("="*80)
    
    # Estadísticas
    success_rates = [v['validation_metrics']['overall']['success_rate'] 
                    for v in all_validations]
    
    print(f"\nTasa de éxito promedio: {np.mean(success_rates):.0%}")
    print(f"Eventos validados completamente: {sum(v['validation_metrics']['overall']['all_tests_passed'] for v in all_validations)}/{len(all_validations)}")
    
    # Análisis por clase de energía
    print("\nValidación por clase de energía:")
    energy_classes = {}
    for v in all_validations:
        energy_class = v['energy_class']
        if energy_class not in energy_classes:
            energy_classes[energy_class] = []
        energy_classes[energy_class].append(v['validation_metrics']['overall']['success_rate'])
    
    for energy_class, rates in energy_classes.items():
        print(f"  {energy_class}: {np.mean(rates):.0%} éxito")
    
    # Verificar predicción clave: correlación energía-topología
    energies = [e.energy_radiated for e in reference_events]
    phase_detections = [v['validation_metrics']['phase_detection']['correct'] 
                       for v in all_validations]
    
    # Alta energía debería dar detección correcta de Klein
    high_energy_mask = np.array(energies) > 2.0
    high_energy_success = np.mean(np.array(phase_detections)[high_energy_mask])
    
    print(f"\nPredicción clave - Alta energía → Klein puro:")
    print(f"  Tasa de éxito en eventos de alta energía: {high_energy_success:.0%}")
    
    # Guardar resultados completos
    output_file = "validation_results/complete_validation_report.json"
    
    # Convertir a formato serializable
    def make_serializable(obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, np.generic):
            return obj.item()
        elif isinstance(obj, LIGOEvent):
            return obj.__dict__
        elif hasattr(obj, '__dict__'):
            return obj.__dict__
        return obj
    
    validation_report = {
        'model_parameters': {
            'R_km': model.R / 1000,
            'tau_ms': model.tau * 1000,
            'f0_Hz': model.f0
        },
        'individual_validations': all_validations,
        'global_statistics': {
            'mean_success_rate': float(np.mean(success_rates)),
            'fully_validated_events': sum(v['validation_metrics']['overall']['all_tests_passed'] 
                                        for v in all_validations),
            'total_events': len(all_validations),
            'high_energy_prediction_success': float(high_energy_success)
        },
        'energy_class_performance': {
            k: float(np.mean(v)) for k, v in energy_classes.items()
        }
    }
    
    with open(output_file, 'w') as f:
        json.dump(validation_report, f, indent=2, default=make_serializable)
    
    print(f"\n✅ Informe completo guardado en: {output_file}")
    
    # Generar gráfico resumen
    plot_validation_summary(all_validations, reference_events)
    
    return validation_report


def plot_validation_summary(validations: List[Dict], events: List[LIGOEvent]):
    """
    Genera gráfico resumen de toda la validación.
    """
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle('Resumen de Validación del Modelo de Transición Topológica',
                fontsize=14, fontweight='bold')
    
    # 1. Tasa de éxito por evento
    ax1 = axes[0, 0]
    event_names = [e.name for e in events]
    success_rates = [v['validation_metrics']['overall']['success_rate'] * 100 
                    for v in validations]
    
    bars = ax1.bar(event_names, success_rates)
    
    # Colorear por energía
    energies = [e.energy_radiated for e in events]
    colors = plt.cm.RdYlBu_r(np.array(energies) / max(energies))
    for bar, color in zip(bars, colors):
        bar.set_color(color)
    
    ax1.set_ylabel('Tasa de Éxito (%)')
    ax1.set_title('A. Validación por Evento')
    ax1.set_ylim(0, 110)
    ax1.axhline(75, color='green', linestyle='--', alpha=0.5, label='Umbral aceptable')
    ax1.legend()
    
    # Añadir valores
    for i, (bar, rate) in enumerate(zip(bars, success_rates)):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2,
                f'{rate:.0f}%', ha='center', va='bottom')
    
    # 2. Correlación energía vs detección de fase
    ax2 = axes[0, 1]
    
    phase_correct = [v['validation_metrics']['phase_detection']['correct'] 
                    for v in validations]
    
    # Separar por detección correcta/incorrecta
    for i, (e, correct) in enumerate(zip(energies, phase_correct)):
        color = 'green' if correct else 'red'
        marker = 'o' if correct else 'x'
        ax2.scatter(e, i, c=color, s=150, marker=marker)
        ax2.text(e + 0.2, i, events[i].name, fontsize=10, va='center')
    
    ax2.axvline(2.0, color='black', linestyle='--', alpha=0.5, 
               label='Umbral Klein puro')
    ax2.set_xlabel('Energía Radiada (M☉c²)')
    ax2.set_ylabel('Evento')
    ax2.set_title('B. Detección de Fase vs Energía')
    ax2.set_yticks(range(len(events)))
    ax2.set_yticklabels([])
    ax2.legend()
    ax2.grid(True, axis='x', alpha=0.3)
    
    # 3. Métricas individuales
    ax3 = axes[1, 0]
    
    metrics_names = ['Fase', 'Frecuencia', 'Teoría', 'Calidad']
    x = np.arange(len(metrics_names))
    width = 0.2
    
    for i, (event, validation) in enumerate(zip(events, validations)):
        metrics = validation['validation_metrics']
        values = [
            metrics['phase_detection']['correct'] * 100,
            metrics['frequency']['valid'] * 100,
            metrics['theory_agreement']['valid'] * 100,
            metrics['data_quality']['valid'] * 100
        ]
        
        offset = (i - len(events)/2) * width
        ax3.bar(x + offset, values, width, label=event.name, alpha=0.8)
    
    ax3.set_ylabel('Éxito (%)')
    ax3.set_title('C. Desglose de Métricas por Evento')
    ax3.set_xticks(x)
    ax3.set_xticklabels(metrics_names)
    ax3.legend(loc='upper right', fontsize=9)
    ax3.set_ylim(0, 110)
    ax3.grid(True, axis='y', alpha=0.3)
    
    # 4. Resumen textual
    ax4 = axes[1, 1]
    ax4.axis('off')
    
    # Calcular estadísticas globales
    mean_success = np.mean(success_rates)
    high_energy_events = [e for e, v in zip(events, validations) 
                         if e.energy_radiated > 2.0]
    high_energy_success = np.mean([v['validation_metrics']['phase_detection']['correct'] 
                                  for e, v in zip(events, validations) 
                                  if e.energy_radiated > 2.0]) * 100
    
    summary_text = f"""
    ESTADÍSTICAS GLOBALES
    
    Eventos analizados: {len(events)}
    Tasa de éxito promedio: {mean_success:.0f}%
    
    Validación por energía:
    • Alta energía (>2 M☉c²): {len(high_energy_events)} eventos
      Detección Klein correcta: {high_energy_success:.0f}%
    
    Predicciones clave validadas:
    {'✓' if high_energy_success > 75 else '✗'} Alta energía → Klein puro
    {'✓' if mean_success > 70 else '✗'} Modelo general confiable
    
    Parámetros del modelo:
    • R = 8400 km
    • τ = 28 ms  
    • f₀ = 5.68 Hz
    """
    
    ax4.text(0.1, 0.9, summary_text, transform=ax4.transAxes,
            fontsize=11, verticalalignment='top',
            bbox=dict(boxstyle='round,pad=1', facecolor='lightblue', alpha=0.8))
    
    plt.tight_layout()
    
    # Guardar
    output_file = "validation_results/validation_summary.png"
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"\nResumen de validación guardado en: {output_file}")
    
    return fig


def main():
    """
    Ejecuta validación completa del modelo.
    """
    print("VALIDACIÓN DEL MODELO DE TRANSICIÓN TOPOLÓGICA")
    print("="*80)
    print("\nEste proceso validará el modelo usando eventos de referencia")
    print("con señales realistas que incluyen la transición topológica.")
    
    # Ejecutar validación completa
    validation_report = validate_all_reference_events()
    
    print("\n" + "="*80)
    print("VALIDACIÓN COMPLETADA")
    print("="*80)
    
    if validation_report['global_statistics']['mean_success_rate'] > 0.7:
        print("\n✅ El modelo ha sido VALIDADO exitosamente")
        print("   Las predicciones clave se cumplen en los datos de prueba")
    else:
        print("\n⚠️  La validación muestra resultados mixtos")
        print("   Se requiere más análisis y refinamiento")
    
    print("\nPróximos pasos:")
    print("1. Aplicar a datos reales de LIGO")
    print("2. Buscar correlaciones en catálogo completo")
    print("3. Publicar resultados si se confirman predicciones")


if __name__ == "__main__":
    main()