#!/usr/bin/env python3
"""
Visualización del Modelo de Transición Topológica Klein-Toroide
================================================================

Este módulo genera visualizaciones comprehensivas de la evolución
topológica durante eventos gravitacionales de alta energía.

Autor: Fausto José Di Bacco
Fecha: Diciembre 2024
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Rectangle, FancyBboxPatch
from matplotlib.gridspec import GridSpec
from typing import Dict, List, Tuple
import os

# Importar el modelo
from topological_transition_implementation import TopologicalTransitionModel

# Configuración de estilo
plt.style.use('default')
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor'] = 'white'
plt.rcParams['axes.grid'] = True
plt.rcParams['grid.alpha'] = 0.3


def plot_evolution_comparison(results: Dict[str, Dict], save_path: str = None):
    """
    Compara la evolución topológica para diferentes eventos.
    """
    fig, axes = plt.subplots(3, 2, figsize=(14, 10))
    fig.suptitle('Evolución Topológica: Comparación de Eventos Gravitacionales', 
                 fontsize=16, fontweight='bold')
    
    # Colores para cada evento
    colors = {'GW150914': '#e74c3c', 'GW151226': '#3498db', 'GW170608': '#2ecc71'}
    
    for idx, (event_name, evolution) in enumerate(results.items()):
        color = colors[event_name]
        t_ms = evolution['time'] * 1000  # Convertir a ms
        
        # 1. Parámetro de orientabilidad Ω(t)
        ax1 = axes[0, 0]
        ax1.plot(t_ms, evolution['Omega'], label=event_name, 
                color=color, linewidth=2.5)
        ax1.axhline(y=-1, color='gray', linestyle='--', alpha=0.5, label='Klein puro' if idx==0 else '')
        ax1.axhline(y=1, color='gray', linestyle='-.', alpha=0.5, label='Toroide puro' if idx==0 else '')
        ax1.axhline(y=0, color='black', linestyle=':', alpha=0.3)
        ax1.set_ylabel('Parámetro Ω', fontsize=12)
        ax1.set_xlabel('Tiempo (ms)', fontsize=12)
        ax1.set_title('A. Evolución del Parámetro de Orientabilidad')
        ax1.set_xlim(0, 60)
        ax1.set_ylim(-1.2, 1.2)
        if idx == 0:
            ax1.legend(loc='right')
        
        # 2. Energía del evento E(t)
        ax2 = axes[0, 1]
        ax2.semilogy(t_ms, evolution['energy'], label=event_name,
                    color=color, linewidth=2.5)
        ax2.set_ylabel('Energía (M☉c²)', fontsize=12)
        ax2.set_xlabel('Tiempo (ms)', fontsize=12)
        ax2.set_title('B. Perfil de Energía del Evento')
        ax2.set_xlim(0, 60)
        ax2.legend()
        
        # 3. Ratio de supresión modal
        ax3 = axes[1, 0]
        # Evitar log(0) para visualización
        suppression = evolution['suppression_ratio'].copy()
        suppression[suppression < 1] = 1
        ax3.semilogy(t_ms, suppression, label=event_name,
                    color=color, linewidth=2.5)
        ax3.axhline(y=20, color='red', linestyle='--', alpha=0.5, 
                   label='Umbral Klein (20:1)' if idx==0 else '')
        ax3.axhline(y=5, color='orange', linestyle='--', alpha=0.5,
                   label='Umbral mixto (5:1)' if idx==0 else '')
        ax3.set_ylabel('Ratio de Supresión', fontsize=12)
        ax3.set_xlabel('Tiempo (ms)', fontsize=12)
        ax3.set_title('C. Supresión de Modos Pares')
        ax3.set_xlim(0, 60)
        ax3.set_ylim(1, 1000)
        if idx == 0:
            ax3.legend(loc='upper right')
    
    # 4. Diagrama de fases (Ω vs E)
    ax4 = axes[1, 1]
    for event_name, evolution in results.items():
        color = colors[event_name]
        # Tomar cada 10 puntos para claridad
        ax4.scatter(evolution['energy'][::10], evolution['Omega'][::10],
                   c=evolution['time'][::10]*1000, cmap='viridis',
                   s=50, alpha=0.7, edgecolors=color, linewidth=1.5,
                   label=event_name)
    ax4.set_xlabel('Energía (M☉c²)', fontsize=12)
    ax4.set_ylabel('Parámetro Ω', fontsize=12)
    ax4.set_title('D. Diagrama de Fases E-Ω')
    ax4.set_xlim(0, 3.5)
    ax4.set_ylim(-1.2, 1.2)
    
    # 5. Ventanas temporales críticas
    ax5 = axes[2, 0]
    time_windows = [
        (0, 14, 'Klein puro', '#e74c3c'),
        (14, 28, 'Transición', '#f39c12'),
        (28, 50, 'Toroide dominante', '#3498db'),
        (50, 100, 'Estado estático', '#95a5a6')
    ]
    
    for i, (t_start, t_end, label, color) in enumerate(time_windows):
        rect = Rectangle((t_start, 0), t_end-t_start, 1, 
                        facecolor=color, alpha=0.3, edgecolor='black')
        ax5.add_patch(rect)
        ax5.text((t_start+t_end)/2, 0.5, label, 
                ha='center', va='center', fontweight='bold')
    
    ax5.set_xlim(0, 100)
    ax5.set_ylim(0, 1)
    ax5.set_xlabel('Tiempo (ms)', fontsize=12)
    ax5.set_title('E. Ventanas Temporales de Análisis')
    ax5.set_yticks([])
    
    # 6. Predicción de frecuencias detectables
    ax6 = axes[2, 1]
    model = TopologicalTransitionModel()
    
    for event_name, evolution in results.items():
        color = colors[event_name]
        # Tomar tiempo t=7ms (máxima amplitud de eco)
        idx_7ms = np.argmin(np.abs(evolution['time']*1000 - 7))
        
        # Obtener masa del evento
        masses = {'GW150914': 62.0, 'GW151226': 21.0, 'GW170608': 18.0}
        mass = masses[event_name]
        
        spectrum = model.predict_echo_spectrum(
            evolution['time'][idx_7ms],
            evolution['Omega'][idx_7ms],
            mass
        )
        
        markerline, stemlines, baseline = ax6.stem(
            spectrum['frequencies'], spectrum['amplitudes']*1e22,
            label=event_name
        )
        plt.setp(markerline, color=color, markersize=8)
        plt.setp(stemlines, color=color, linewidth=2)
        plt.setp(baseline, visible=False)
    
    ax6.set_xlabel('Frecuencia (Hz)', fontsize=12)
    ax6.set_ylabel('Amplitud de eco (×10⁻²²)', fontsize=12)
    ax6.set_title('F. Espectro de Frecuencias de Echo (t=7ms)')
    ax6.set_xlim(0, 60)
    ax6.legend()
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Gráfico guardado en: {save_path}")
    
    return fig


def plot_topological_landscape(model: TopologicalTransitionModel, 
                              save_path: str = None):
    """
    Visualiza el paisaje topológico en el espacio de parámetros.
    """
    fig = plt.figure(figsize=(15, 10))
    gs = GridSpec(3, 3, figure=fig, hspace=0.3, wspace=0.3)
    
    fig.suptitle('Paisaje Topológico: Transición Klein-Toroide', 
                fontsize=16, fontweight='bold')
    
    # 1. Superficie 3D: Ω(E, t)
    ax1 = fig.add_subplot(gs[0:2, 0:2], projection='3d')
    
    # Crear malla
    E_range = np.linspace(0.1, 5, 50)
    t_range = np.linspace(0, 0.05, 50)
    E_mesh, t_mesh = np.meshgrid(E_range, t_range)
    
    # Calcular Ω para cada punto
    Omega_mesh = np.zeros_like(E_mesh)
    for i in range(len(E_range)):
        for j in range(len(t_range)):
            # Solución aproximada de la ecuación maestra
            E0 = E_range[i]
            t = t_range[j]
            # Simplificación: Ω evoluciona exponencialmente desde -1
            tau_eff = model.tau / (1 + E0)
            Omega_mesh[j, i] = -np.exp(-t/tau_eff) + (1 - np.exp(-t/tau_eff)) * 0.1
    
    # Plot superficie
    surf = ax1.plot_surface(E_mesh, t_mesh*1000, Omega_mesh, 
                           cmap='RdBu_r', alpha=0.8, 
                           vmin=-1, vmax=1)
    
    # Añadir trayectorias de eventos específicos
    for E0, color, label in [(3.0, 'red', 'Alta E'), 
                             (1.0, 'blue', 'Media E'),
                             (0.5, 'green', 'Baja E')]:
        t_traj = np.linspace(0, 0.05, 100)
        E_traj = E0 * np.exp(-t_traj/model.tau)
        Omega_traj = -np.exp(-t_traj/(model.tau/(1+E0))) + \
                     (1 - np.exp(-t_traj/(model.tau/(1+E0)))) * 0.1
        ax1.plot(E_traj, t_traj*1000, Omega_traj, 
                color=color, linewidth=3, label=label)
    
    ax1.set_xlabel('Energía (M☉c²)', fontsize=10)
    ax1.set_ylabel('Tiempo (ms)', fontsize=10)
    ax1.set_zlabel('Parámetro Ω', fontsize=10)
    ax1.set_title('Superficie de Evolución Topológica Ω(E,t)')
    ax1.legend()
    
    # 2. Mapa de calor: Tiempo de transición
    ax2 = fig.add_subplot(gs[0, 2])
    
    E_values = np.linspace(0.5, 5, 30)
    transition_times = []
    
    for E in E_values:
        # Encontrar tiempo cuando Ω cruza 0
        t_test = np.linspace(0, 0.1, 1000)
        evolution = model.evolve_topology(t_test, E, include_modes=False)
        
        # Encontrar cruce por cero
        crossings = np.where(np.diff(np.sign(evolution['Omega'])))[0]
        if len(crossings) > 0:
            t_transition = t_test[crossings[0]] * 1000  # ms
        else:
            t_transition = 100  # No transiciona
        
        transition_times.append(t_transition)
    
    ax2.plot(E_values, transition_times, 'b-', linewidth=2)
    ax2.fill_between(E_values, 0, transition_times, alpha=0.3)
    ax2.axhline(y=14, color='red', linestyle='--', label='t = 14 ms')
    ax2.axhline(y=28, color='orange', linestyle='--', label='t = 28 ms')
    ax2.set_xlabel('Energía inicial (M☉c²)')
    ax2.set_ylabel('Tiempo de transición (ms)')
    ax2.set_title('Tiempo hasta Ω = 0')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # 3. Diagrama de bifurcación
    ax3 = fig.add_subplot(gs[1, 2])
    
    # Parámetro de control: energía
    E_control = np.linspace(0.1, 10, 100)
    Omega_equilibrium = []
    
    for E in E_control:
        # Estado de equilibrio (dΩ/dt = 0)
        # Simplificación: equilibrio cuando términos se balancean
        Omega_eq = -E / (E + 1)  # Aproximación
        Omega_equilibrium.append(Omega_eq)
    
    ax3.plot(E_control, Omega_equilibrium, 'k-', linewidth=2)
    ax3.axhline(y=-1, color='red', linestyle='--', alpha=0.5, label='Klein')
    ax3.axhline(y=0, color='gray', linestyle=':', alpha=0.5)
    ax3.axhline(y=1, color='blue', linestyle='--', alpha=0.5, label='Toroide')
    ax3.fill_between(E_control, -1, Omega_equilibrium, 
                    where=(np.array(Omega_equilibrium)<0), alpha=0.3, color='red')
    ax3.set_xlabel('Energía de control (M☉c²)')
    ax3.set_ylabel('Ω de equilibrio')
    ax3.set_title('Diagrama de Bifurcación')
    ax3.set_xlim(0, 10)
    ax3.set_ylim(-1.2, 1.2)
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # 4. Espacio de fases 2D
    ax4 = fig.add_subplot(gs[2, 0])
    
    # Crear campo vectorial
    Omega_vals = np.linspace(-1.2, 1.2, 20)
    E_vals = np.linspace(0.1, 5, 20)
    Omega_grid, E_grid = np.meshgrid(Omega_vals, E_vals)
    
    # Calcular derivadas
    dOmega_dt = -model.alpha * E_grid * Omega_grid + 0.1  # Simplificado
    dE_dt = -E_grid / model.tau
    
    # Normalizar para visualización
    magnitude = np.sqrt(dOmega_dt**2 + dE_dt**2)
    dOmega_dt_norm = dOmega_dt / magnitude
    dE_dt_norm = dE_dt / magnitude
    
    ax4.quiver(Omega_grid, E_grid, dOmega_dt_norm, dE_dt_norm,
              magnitude, cmap='viridis', alpha=0.6)
    
    # Añadir trayectorias
    for E0, color in [(3.0, 'red'), (1.0, 'blue'), (0.5, 'green')]:
        evolution = model.evolve_topology(np.linspace(0, 0.1, 200), E0, 
                                        include_modes=False)
        ax4.plot(evolution['Omega'], evolution['energy'], 
                color=color, linewidth=2, label=f'E₀={E0}')
    
    ax4.set_xlabel('Parámetro Ω')
    ax4.set_ylabel('Energía (M☉c²)')
    ax4.set_title('Espacio de Fases con Campo Vectorial')
    ax4.set_xlim(-1.2, 1.2)
    ax4.set_ylim(0, 5)
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    
    # 5. Potencial efectivo
    ax5 = fig.add_subplot(gs[2, 1])
    
    Omega_range = np.linspace(-1.5, 1.5, 200)
    
    for E in [0.5, 1.0, 2.0, 5.0]:
        # Potencial efectivo (forma esquemática)
        V_eff = E * (Omega_range**2 - 1)**2 + 0.1 * Omega_range**4
        ax5.plot(Omega_range, V_eff, label=f'E={E} M☉c²', linewidth=2)
    
    ax5.axvline(x=-1, color='red', linestyle='--', alpha=0.5)
    ax5.axvline(x=1, color='blue', linestyle='--', alpha=0.5)
    ax5.axvline(x=0, color='gray', linestyle=':', alpha=0.5)
    ax5.set_xlabel('Parámetro Ω')
    ax5.set_ylabel('Potencial efectivo V(Ω)')
    ax5.set_title('Paisaje de Potencial Topológico')
    ax5.legend()
    ax5.grid(True, alpha=0.3)
    ax5.set_ylim(0, 10)
    
    # 6. Resumen de escalas
    ax6 = fig.add_subplot(gs[2, 2])
    ax6.axis('off')
    
    summary_text = f"""
    ESCALAS CARACTERÍSTICAS
    
    Dimensión extra:
    R = {model.R/1e3:.0f} km
    
    Tiempo de relajación:
    τ = {model.tau*1e3:.1f} ms
    
    Frecuencia fundamental:
    f₀ = {model.f0:.2f} Hz
    
    Energía crítica (90%):
    E_c = {model.critical_energy():.1f} M☉c²
    
    Ventanas temporales:
    • Klein puro: 0-14 ms
    • Transición: 14-28 ms  
    • Toroide: 28-50 ms
    • Estático: >50 ms
    """
    
    ax6.text(0.1, 0.9, summary_text, transform=ax6.transAxes,
            fontsize=11, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Paisaje topológico guardado en: {save_path}")
    
    return fig


def create_animation(model: TopologicalTransitionModel, 
                    event_energy: float = 3.0,
                    save_path: str = None):
    """
    Crea una animación de la transición topológica.
    """
    # Configuración
    duration = 0.1  # 100 ms
    fps = 30
    frames = int(duration * fps * 10)  # 10x slow motion
    
    # Evolucionar sistema
    t_array = np.linspace(0, duration, frames)
    evolution = model.evolve_topology(t_array, event_energy, include_modes=True)
    
    # Crear figura
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 12))
    fig.suptitle(f'Evolución Topológica Animada (E₀ = {event_energy} M☉c²)', 
                fontsize=14, fontweight='bold')
    
    # Configurar ejes
    ax1.set_xlim(-1.5, 1.5)
    ax1.set_ylim(-1.5, 1.5)
    ax1.set_aspect('equal')
    ax1.set_xlabel('Dimensión compacta φ')
    ax1.set_ylabel('Dimensión compacta χ')
    ax1.set_title('Geometría de la Dimensión Extra')
    
    ax2.set_xlim(0, 100)
    ax2.set_ylim(-1.2, 1.2)
    ax2.set_xlabel('Tiempo (ms)')
    ax2.set_ylabel('Parámetro Ω')
    ax2.set_title('Evolución del Parámetro de Orientabilidad')
    ax2.axhline(y=-1, color='red', linestyle='--', alpha=0.5)
    ax2.axhline(y=1, color='blue', linestyle='--', alpha=0.5)
    ax2.axhline(y=0, color='gray', linestyle=':', alpha=0.5)
    
    ax3.set_xlim(0, 60)
    ax3.set_ylim(0, 1)
    ax3.set_xlabel('Frecuencia (Hz)')
    ax3.set_ylabel('Amplitud normalizada')
    ax3.set_title('Espectro de Frecuencias de Echo')
    
    # Elementos animados
    topology_plot, = ax1.plot([], [], 'b-', linewidth=2)
    orientation_marker = ax1.scatter([], [], c='red', s=100, marker='o')
    
    omega_line, = ax2.plot([], [], 'g-', linewidth=2)
    current_point = ax2.scatter([], [], c='red', s=100, marker='o')
    
    freq_bars = ax3.bar([], [], width=2, alpha=0.7)
    
    # Texto informativo
    info_text = ax1.text(0.02, 0.98, '', transform=ax1.transAxes,
                        verticalalignment='top',
                        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    def init():
        topology_plot.set_data([], [])
        omega_line.set_data([], [])
        return topology_plot, omega_line
    
    def animate(frame):
        t_current = t_array[frame]
        t_ms = t_current * 1000
        
        # 1. Actualizar geometría topológica
        theta = np.linspace(0, 2*np.pi, 100)
        
        # Parámetro de orientabilidad actual
        Omega = evolution['Omega'][frame]
        
        if Omega < -0.5:  # Klein dominante
            # Forma de 8 (Klein bottle cross-section)
            r = 1 + 0.3 * np.sin(2*theta)
            x = r * np.cos(theta)
            y = r * np.sin(theta) * (1 + 0.5 * Omega)
            label = "Klein Bottle"
            color = 'red'
        elif Omega > 0.5:  # Toroide dominante
            # Círculo simple
            x = np.cos(theta)
            y = np.sin(theta)
            label = "Twisted Torus"
            color = 'blue'
        else:  # Transición
            # Forma intermedia
            blend = (Omega + 1) / 2
            r = 1 + 0.3 * np.sin(2*theta) * (1 - blend)
            x = r * np.cos(theta)
            y = r * np.sin(theta) * (1 + 0.5 * (1 - blend))
            label = "Transition"
            color = 'orange'
        
        topology_plot.set_data(x, y)
        topology_plot.set_color(color)
        
        # 2. Actualizar gráfico de Omega
        omega_line.set_data(t_array[:frame+1]*1000, evolution['Omega'][:frame+1])
        current_point.set_offsets([[t_ms, Omega]])
        
        # 3. Actualizar espectro de frecuencias
        spectrum = model.predict_echo_spectrum(t_current, Omega, 62.0)
        
        # Limpiar barras anteriores
        for bar in freq_bars:
            bar.remove()
        
        # Nuevas barras
        bars = ax3.bar(spectrum['frequencies'], spectrum['amplitudes']/max(spectrum['amplitudes']),
                       width=2, alpha=0.7, color=color)
        
        # 4. Actualizar texto
        info_text.set_text(f'Tiempo: {t_ms:.1f} ms\n'
                          f'Ω = {Omega:.3f}\n'
                          f'Estado: {label}\n'
                          f'Supresión: {evolution["suppression_ratio"][frame]:.1f}:1')
        
        return topology_plot, omega_line, current_point, info_text
    
    # Crear animación
    anim = animation.FuncAnimation(fig, animate, init_func=init,
                                  frames=frames, interval=33, blit=False)
    
    if save_path:
        writer = animation.PillowWriter(fps=fps)
        anim.save(save_path, writer=writer)
        print(f"Animación guardada en: {save_path}")
    
    return anim


def main():
    """
    Genera todas las visualizaciones del modelo.
    """
    print("\n" + "="*60)
    print("GENERANDO VISUALIZACIONES DEL MODELO TOPOLÓGICO")
    print("="*60)
    
    # Crear directorio para resultados
    output_dir = "topological_transition_plots"
    os.makedirs(output_dir, exist_ok=True)
    
    # Inicializar modelo
    model = TopologicalTransitionModel()
    
    # 1. Analizar eventos de referencia
    print("\nAnalizando eventos de referencia...")
    events = {
        'GW150914': {'mass': 62.0, 'energy': 3.0},
        'GW151226': {'mass': 21.0, 'energy': 1.0},
        'GW170608': {'mass': 18.0, 'energy': 0.5}
    }
    
    results = {}
    for event_name, params in events.items():
        t = np.linspace(0, 0.1, 1000)
        evolution = model.evolve_topology(t, params['energy'], 
                                        initial_state='klein',
                                        include_modes=True)
        results[event_name] = evolution
    
    # 2. Generar comparación de evolución
    print("\nGenerando gráfico de comparación de eventos...")
    plot_evolution_comparison(results, 
                            save_path=f"{output_dir}/evolution_comparison.png")
    
    # 3. Generar paisaje topológico
    print("\nGenerando paisaje topológico...")
    plot_topological_landscape(model,
                             save_path=f"{output_dir}/topological_landscape.png")
    
    # 4. Crear animación (solo para GW150914)
    print("\nCreando animación de transición topológica...")
    create_animation(model, event_energy=3.0,
                    save_path=f"{output_dir}/topological_transition.gif")
    
    print(f"\n✅ Todas las visualizaciones generadas en: {output_dir}/")
    print("\nPróximo paso: Desarrollar pipeline de análisis para datos LIGO")


if __name__ == "__main__":
    main()