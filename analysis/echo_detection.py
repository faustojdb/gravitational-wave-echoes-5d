#!/usr/bin/env python3
"""
Análisis y visualización de resultados de ecos LIGO
"""

import json
import numpy as np
import matplotlib.pyplot as plt
import os
from glob import glob

def load_analysis_results(directory='ligo_data'):
    """Carga todos los archivos de análisis JSON"""
    json_files = glob(f"{directory}/*_analysis.json")
    results = {}
    
    for file in json_files:
        with open(file, 'r') as f:
            data = json.load(f)
            event = data['event_name']
            detector = data['detector']
            
            if event not in results:
                results[event] = {}
            results[event][detector] = data
    
    return results

def analyze_echo_patterns(results):
    """Analiza patrones en los ecos detectados"""
    echo_summary = []
    
    for event, detectors in results.items():
        for detector, data in detectors.items():
            event_info = data['event_info']
            echo_analysis = data['echo_analysis']
            
            # Extraer información relevante
            for echo in echo_analysis['echo_candidates']:
                echo_summary.append({
                    'event': event,
                    'detector': detector,
                    'mass_total': event_info['mass_total'],
                    'echo_number': echo['echo_number'],
                    'actual_time': echo['actual_time'],
                    'amplitude_ratio': echo['amplitude_ratio'],
                    'confidence': echo['confidence']
                })
    
    return echo_summary

def plot_echo_statistics(echo_summary):
    """Genera gráficos de estadísticas de ecos"""
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle('Análisis de Ecos Gravitacionales - Teoría Multidimensional', fontsize=16)
    
    # 1. Distribución de tiempos de eco
    ax = axes[0, 0]
    echo_times = [e['actual_time'] for e in echo_summary if abs(e['actual_time']) < 1]
    if echo_times:
        ax.hist(echo_times, bins=30, alpha=0.7, color='blue')
        ax.axvline(0.15, color='red', linestyle='--', label='τ teórico = 0.15s')
        ax.set_xlabel('Tiempo de eco (s)')
        ax.set_ylabel('Frecuencia')
        ax.set_title('Distribución de Tiempos de Echo')
        ax.legend()
    
    # 2. Amplitud vs número de eco
    ax = axes[0, 1]
    for n in range(1, 6):
        amplitudes = [e['amplitude_ratio'] for e in echo_summary if e['echo_number'] == n]
        if amplitudes:
            ax.scatter([n]*len(amplitudes), amplitudes, alpha=0.5, label=f'Echo {n}')
    
    # Curva teórica
    n_theory = np.arange(1, 6)
    alpha_theory = 0.3
    amp_theory = alpha_theory ** n_theory
    ax.plot(n_theory, amp_theory, 'r--', linewidth=2, label='Teoría (α=0.3)')
    ax.set_xlabel('Número de eco')
    ax.set_ylabel('Razón de amplitud')
    ax.set_title('Atenuación de Amplitud')
    ax.set_yscale('log')
    ax.legend()
    
    # 3. Compatibilidad por evento
    ax = axes[1, 0]
    events = []
    compatibilities = []
    
    for event in set(e['event'] for e in echo_summary):
        events.append(event)
        # Promedio de compatibilidad para el evento
        event_data = [r for r in echo_summary if r['event'] == event]
        avg_confidence = np.mean([e['confidence'] for e in event_data])
        compatibilities.append(avg_confidence)
    
    bars = ax.bar(events, compatibilities, color=['green' if c > 0.5 else 'orange' if c > 0.3 else 'red' for c in compatibilities])
    ax.axhline(0.5, color='black', linestyle='--', alpha=0.5)
    ax.set_ylabel('Compatibilidad promedio')
    ax.set_title('Compatibilidad por Evento')
    ax.set_ylim(0, 1)
    
    # Añadir valores en las barras
    for bar, comp in zip(bars, compatibilities):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                f'{comp:.2f}', ha='center', va='bottom')
    
    # 4. Correlación masa-eco
    ax = axes[1, 1]
    masses = [e['mass_total'] for e in echo_summary]
    confidences = [e['confidence'] for e in echo_summary]
    
    # Agrupar por masa
    unique_masses = sorted(set(masses))
    avg_confidence_by_mass = []
    
    for mass in unique_masses:
        mass_data = [e['confidence'] for e in echo_summary if e['mass_total'] == mass]
        avg_confidence_by_mass.append(np.mean(mass_data))
    
    ax.scatter(unique_masses, avg_confidence_by_mass, s=100, color='purple', alpha=0.7)
    ax.set_xlabel('Masa total (M☉)')
    ax.set_ylabel('Confianza promedio')
    ax.set_title('Correlación Masa-Detección de Ecos')
    
    # Línea de tendencia
    if len(unique_masses) > 1:
        z = np.polyfit(unique_masses, avg_confidence_by_mass, 1)
        p = np.poly1d(z)
        ax.plot(unique_masses, p(unique_masses), "r--", alpha=0.8)
    
    plt.tight_layout()
    plt.savefig('ligo_data/echo_analysis_summary.png', dpi=300, bbox_inches='tight')
    plt.show()

def generate_report(results, echo_summary):
    """Genera un informe detallado"""
    report = []
    report.append("# Informe de Análisis de Ecos LIGO")
    report.append("## Teoría Multidimensional - Validación Experimental\n")
    
    # Resumen general
    total_events = len(results)
    total_detections = len(echo_summary)
    avg_compatibility = np.mean([r['theory_compatibility'] for event in results.values() 
                                for r in event.values()])
    
    report.append("### Resumen General")
    report.append(f"- Eventos analizados: {total_events}")
    report.append(f"- Total de ecos detectados: {total_detections}")
    report.append(f"- Compatibilidad promedio: {avg_compatibility:.2%}")
    report.append(f"- Parámetros teóricos: k=1.2, R=1.5, α=0.3, τ=0.15s\n")
    
    # Resultados por evento
    report.append("### Resultados por Evento")
    
    for event, detectors in sorted(results.items()):
        report.append(f"\n#### {event}")
        event_info = list(detectors.values())[0]['event_info']
        report.append(f"- Fecha: {event_info['date']}")
        report.append(f"- Masa total: {event_info['mass_total']} M☉")
        report.append(f"- Distancia: {event_info['distance']} Gly")
        
        for detector, data in detectors.items():
            n_echoes = data['echo_analysis']['n_echo_candidates']
            compatibility = data['theory_compatibility']
            report.append(f"- {detector}: {n_echoes} ecos, compatibilidad: {compatibility:.2%}")
    
    # Análisis estadístico
    report.append("\n### Análisis Estadístico")
    
    # Distribución de tiempos
    valid_times = [abs(e['actual_time']) for e in echo_summary if abs(e['actual_time']) < 1]
    if valid_times:
        report.append(f"- Tiempo promedio de eco: {np.mean(valid_times):.3f}s")
        report.append(f"- Desviación estándar: {np.std(valid_times):.3f}s")
        report.append(f"- Rango: [{np.min(valid_times):.3f}, {np.max(valid_times):.3f}]s")
    
    # Validación de predicciones
    report.append("\n### Validación de Predicciones Teóricas")
    
    # 1. Intervalos temporales
    tau_theory = 0.15
    if valid_times:
        tau_observed = np.mean(valid_times)
        tau_error = abs(tau_observed - tau_theory) / tau_theory
        status = "✅" if tau_error < 0.3 else "⚠️" if tau_error < 0.5 else "❌"
        report.append(f"1. **Intervalo temporal entre ecos**")
        report.append(f"   - Predicho: τ = {tau_theory}s")
        report.append(f"   - Observado: τ = {tau_observed:.3f}s")
        report.append(f"   - Error: {tau_error:.1%} {status}")
    
    # 2. Atenuación
    alpha_theory = 0.3
    amp_ratios = [e['amplitude_ratio'] for e in echo_summary if e['echo_number'] == 2]
    if amp_ratios:
        alpha_observed = np.mean(amp_ratios)
        alpha_error = abs(alpha_observed - alpha_theory) / alpha_theory
        status = "✅" if alpha_error < 0.3 else "⚠️" if alpha_error < 0.5 else "❌"
        report.append(f"\n2. **Factor de atenuación**")
        report.append(f"   - Predicho: α = {alpha_theory}")
        report.append(f"   - Observado: α ≈ {alpha_observed:.3f}")
        report.append(f"   - Error: {alpha_error:.1%} {status}")
    
    # 3. Número de ecos
    n_echoes_avg = np.mean([len([e for e in echo_summary if e['event'] == event]) 
                           for event in results.keys()]) / 2  # Dividir por 2 detectores
    status = "✅" if n_echoes_avg >= 3 else "⚠️" if n_echoes_avg >= 2 else "❌"
    report.append(f"\n3. **Número de ecos detectables**")
    report.append(f"   - Predicho: 3-5 ecos")
    report.append(f"   - Observado: {n_echoes_avg:.1f} ecos promedio {status}")
    
    # Conclusiones
    report.append("\n### Conclusiones")
    
    if avg_compatibility > 0.5:
        report.append("✅ **Los datos muestran fuerte evidencia de ecos gravitacionales**")
        report.append("- La compatibilidad supera el umbral del 50%")
        report.append("- Se recomienda publicación inmediata de resultados")
    elif avg_compatibility > 0.3:
        report.append("⚠️ **Los datos muestran evidencia parcial de ecos**")
        report.append("- Se detectan estructuras tipo eco pero con desviaciones")
        report.append("- Se recomienda refinar parámetros y ampliar análisis")
    else:
        report.append("❌ **Evidencia débil de ecos en configuración actual**")
        report.append("- Requiere revisión de parámetros teóricos")
        report.append("- Considerar modelos alternativos")
    
    # Guardar informe
    with open('ligo_data/analysis_report.md', 'w', encoding='utf-8') as f:
        f.write('\n'.join(report))
    
    print('\n'.join(report))

def main():
    """Función principal"""
    print("📊 Analizando resultados de ecos LIGO...")
    
    # Cargar resultados
    results = load_analysis_results()
    
    if not results:
        print("❌ No se encontraron archivos de análisis")
        return
    
    # Analizar patrones
    echo_summary = analyze_echo_patterns(results)
    
    # Generar visualizaciones
    print("📈 Generando gráficos...")
    plot_echo_statistics(echo_summary)
    
    # Generar informe
    print("\n📝 Generando informe...")
    generate_report(results, echo_summary)
    
    print("\n✅ Análisis completado!")
    print("📁 Resultados guardados en ligo_data/")

if __name__ == "__main__":
    main()