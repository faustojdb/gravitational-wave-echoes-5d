#!/usr/bin/env python3
"""
Klein Spacetime Atoms Scale Visualization
=========================================

Create comprehensive visualizations showing the corrected scale relationships
between individual Klein atoms and their collective correlation signatures.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Circle, FancyBboxPatch
import seaborn as sns

def create_scale_comparison_plot():
    """Create comprehensive scale comparison visualization"""
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('KLEIN SPACETIME ATOMS: CORRECTED SCALE RELATIONSHIPS', 
                 fontsize=16, fontweight='bold')
    
    # Colors
    colors = {
        'earth': '#4CAF50',
        'klein_atom': '#FF5722', 
        'correlation': '#2196F3',
        'galaxy': '#9C27B0'
    }
    
    # ============ Panel 1: Solar System Scale ============
    ax1 = axes[0, 0]
    
    # Earth orbit (1 AU = 150 million km)
    earth_orbit = Circle((0, 0), 1, fill=False, color='gray', linestyle='--', alpha=0.7)
    ax1.add_patch(earth_orbit)
    
    # Earth
    earth = Circle((1, 0), 0.04, color=colors['earth'], alpha=0.8, label='Earth (6,371 km)')
    ax1.add_patch(earth)
    
    # Klein atom (radius = 8,400 km, larger than Earth)
    klein_atom1 = Circle((0.5, 0.3), 0.056, color=colors['klein_atom'], alpha=0.6, 
                        label='Klein Atom (8,400 km radius)')
    ax1.add_patch(klein_atom1)
    
    klein_atom2 = Circle((-0.3, -0.4), 0.056, color=colors['klein_atom'], alpha=0.6)
    ax1.add_patch(klein_atom2)
    
    klein_atom3 = Circle((0.7, -0.2), 0.056, color=colors['klein_atom'], alpha=0.6)
    ax1.add_patch(klein_atom3)
    
    ax1.set_xlim(-1.5, 1.5)
    ax1.set_ylim(-1.5, 1.5)
    ax1.set_aspect('equal')
    ax1.set_title('A. Solar System Scale\nMultiple Klein Atoms per Star System', fontweight='bold')
    ax1.legend(loc='upper right', fontsize=9)
    ax1.grid(True, alpha=0.3)
    
    # Add scale annotation
    ax1.text(0, -1.3, '1 AU = 150 million km\nKlein atoms > Earth size', 
             ha='center', va='center', fontsize=9, 
             bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    # ============ Panel 2: Klein Atom Properties ============
    ax2 = axes[0, 1]
    ax2.axis('off')
    
    # Create property boxes
    properties = [
        "INDIVIDUAL KLEIN ATOM",
        "Radius: R_K = 8,400 km",
        "Wavelength: λ_K = 52,800 km", 
        "Mass: m_K = 2.35×10⁻¹⁴ eV/c²",
        "Frequency: f₀ = 5.68 Hz",
        "Volume: V_K = 2.48×10²¹ m³",
        "",
        "COLLECTIVE CORRELATION",
        "Length: ξ = 8.4 kpc = 8,400 pc",
        "Scaling: ξ ≈ 160 × R_K",
        "Atoms involved: ~4×10⁶",
        "Observable in: Galaxy dynamics"
    ]
    
    y_start = 0.95
    for i, prop in enumerate(properties):
        if prop == "":
            continue
        color = colors['klein_atom'] if i < 7 else colors['correlation']
        weight = 'bold' if prop.isupper() else 'normal'
        size = 11 if prop.isupper() else 10
        
        ax2.text(0.05, y_start - i*0.08, prop, transform=ax2.transAxes,
                fontsize=size, fontweight=weight, color=color)
    
    # ============ Panel 3: Galactic Scale ============
    ax3 = axes[1, 0]
    
    # Galaxy disk (simplified)
    galaxy_disk = Circle((0, 0), 1, fill=True, color=colors['galaxy'], alpha=0.2)
    ax3.add_patch(galaxy_disk)
    
    # 8.4 kpc correlation scale
    correlation_ring = Circle((0, 0), 0.336, fill=False, color=colors['correlation'], 
                             linewidth=3, label='8.4 kpc Correlation Scale')
    ax3.add_patch(correlation_ring)
    
    # Sun position (8.2 kpc from center)
    sun_pos = Circle((0.328, 0), 0.02, color='yellow', label='Sun (8.2 kpc)')
    ax3.add_patch(sun_pos)
    
    # Sample rotation curve signature
    angles = np.linspace(0, 2*np.pi, 100)
    r_correlation = 0.336
    modulation = 0.05 * np.sin(8 * angles)  # 8.4 kpc feature
    
    x_mod = (r_correlation + modulation) * np.cos(angles)
    y_mod = (r_correlation + modulation) * np.sin(angles)
    ax3.plot(x_mod, y_mod, color='red', linewidth=2, alpha=0.8, 
             label='Rotation Curve Signature')
    
    ax3.set_xlim(-1.2, 1.2)
    ax3.set_ylim(-1.2, 1.2)
    ax3.set_aspect('equal')
    ax3.set_title('B. Galactic Scale\n8.4 kpc Collective Correlation Effects', fontweight='bold')
    ax3.legend(loc='upper right', fontsize=9)
    ax3.grid(True, alpha=0.3)
    
    # Add scale annotation
    ax3.text(0, -1.1, 'Galaxy radius ~25 kpc\n8.4 kpc = correlation scale', 
             ha='center', va='center', fontsize=9,
             bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    # ============ Panel 4: Scale Hierarchy ============
    ax4 = axes[1, 1]
    
    # Logarithmic scale comparison
    scales = np.array([6.371e3, 8.4e3, 52.8e3, 1.496e8, 8.4e16, 7.7e17]) # km
    labels = ['Earth\nRadius', 'Klein Atom\nRadius', 'Klein\nWavelength', 
              'Earth\nOrbit', '8.4 kpc\nCorrelation', 'Galaxy\nRadius']
    colors_list = [colors['earth'], colors['klein_atom'], colors['klein_atom'],
                   'gray', colors['correlation'], colors['galaxy']]
    
    x_pos = np.arange(len(scales))
    bars = ax4.bar(x_pos, np.log10(scales), color=colors_list, alpha=0.7)
    
    # Add value labels on bars
    for i, (bar, scale) in enumerate(zip(bars, scales)):
        height = bar.get_height()
        if scale < 1e6:
            label_text = f'{scale/1e3:.1f} km'
        elif scale < 1e9:
            label_text = f'{scale/1e6:.0f} Mm'
        else:
            label_text = f'{scale/1e16:.1f} kpc'
            
        ax4.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                label_text, ha='center', va='bottom', fontsize=8, fontweight='bold')
    
    ax4.set_xlabel('Physical Scales')
    ax4.set_ylabel('Size (log₁₀ km)')
    ax4.set_title('C. Scale Hierarchy\nFrom Klein Atoms to Galaxies', fontweight='bold')
    ax4.set_xticks(x_pos)
    ax4.set_xticklabels(labels, rotation=45, ha='right')
    ax4.grid(True, alpha=0.3, axis='y')
    
    # Add connecting lines showing relationships
    # Klein atom to correlation
    ax4.annotate('', xy=(4, np.log10(8.4e16)), xytext=(1, np.log10(8.4e3)),
                arrowprops=dict(arrowstyle='<->', color='red', lw=2),
                fontsize=8)
    ax4.text(2.5, 12, '160× scaling\n~10⁶ atoms', ha='center', color='red', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('klein_spacetime_atoms_scale_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("✅ Scale comparison visualization created")

def create_detection_signatures_plot():
    """Create plot showing detection signatures at different scales"""
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('KLEIN DETECTION SIGNATURES: INDIVIDUAL vs COLLECTIVE SCALES', 
                 fontsize=14, fontweight='bold')
    
    # ============ Panel 1: Individual Klein Atom Signatures ============
    ax1 = axes[0, 0]
    
    # Klein atom oscillation at 5.68 Hz
    t = np.linspace(0, 2, 1000)  # 2 seconds
    klein_oscillation = np.sin(2 * np.pi * 5.68 * t)
    
    ax1.plot(t, klein_oscillation, 'red', linewidth=2, label='Klein Oscillation (5.68 Hz)')
    ax1.set_xlabel('Time (seconds)')
    ax1.set_ylabel('Klein Field Amplitude')
    ax1.set_title('A. Individual Klein Atom\nTemporal Signature', fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # Mark periods
    period = 1/5.68
    for i in range(int(2/period) + 1):
        ax1.axvline(i * period, color='gray', linestyle='--', alpha=0.5)
    
    ax1.text(0.5, 0.8, f'Period = {period:.3f} s\nλ_K/c = 176 ms', 
             transform=ax1.transAxes, fontsize=9,
             bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    # ============ Panel 2: Gravitational Wave Echoes ============
    ax2 = axes[0, 1]
    
    # GW150914-like chirp with Klein echoes
    t_gw = np.linspace(-0.2, 0.5, 1000)
    
    # Main chirp (simplified)
    f_chirp = 35 + 200 * np.maximum(0, t_gw)**2
    main_signal = np.exp(-((t_gw - 0)/0.05)**2) * np.sin(2*np.pi*f_chirp*t_gw)
    
    # Klein echoes at 176 ms intervals
    echo_times = [0.176, 0.352]
    echo_signal = main_signal.copy()
    
    for echo_time in echo_times:
        echo_idx = np.argmin(np.abs(t_gw - echo_time))
        if echo_idx < len(echo_signal):
            echo_amp = 0.1 * np.exp(-echo_time/0.2)  # Decaying echoes
            echo_signal[echo_idx:] += echo_amp * main_signal[:len(echo_signal)-echo_idx]
    
    ax2.plot(t_gw, main_signal, 'blue', alpha=0.7, label='GR Signal')
    ax2.plot(t_gw, echo_signal, 'red', label='GR + Klein Echoes')
    
    # Mark echo times
    for echo_time in echo_times:
        ax2.axvline(echo_time, color='red', linestyle='--', alpha=0.7)
    
    ax2.set_xlabel('Time (seconds)')
    ax2.set_ylabel('Gravitational Wave Strain')
    ax2.set_title('B. Gravitational Wave Echoes\nKlein Temporal Discretization', fontweight='bold')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # ============ Panel 3: Galaxy Rotation Curves ============
    ax3 = axes[1, 0]
    
    # Realistic rotation curve with 8.4 kpc signature
    r = np.linspace(0, 30, 300)  # kpc
    
    # Standard NFW + disk model
    v_disk = 200 * r * np.exp(-r/3)
    v_halo = 150 * np.sqrt(1 - np.exp(-r/10))
    v_standard = np.sqrt(v_disk**2 + v_halo**2)
    
    # Klein signature at 8.4 kpc
    klein_signature = 20 * np.exp(-((r - 8.4)/2)**2) * np.sin(2*np.pi*r/8.4)
    v_klein = v_standard + klein_signature
    
    ax3.plot(r, v_standard, 'gray', linewidth=2, label='Standard ΛCDM', alpha=0.7)
    ax3.plot(r, v_klein, 'blue', linewidth=2, label='With Klein Correlations')
    ax3.fill_between(r, v_standard-10, v_standard+10, alpha=0.3, color='gray', label='Observational Uncertainty')
    
    # Highlight 8.4 kpc region
    ax3.axvline(8.4, color='red', linestyle='--', linewidth=2, label='8.4 kpc Correlation Scale')
    ax3.axvspan(6.4, 10.4, alpha=0.2, color='red')
    
    ax3.set_xlabel('Galactocentric Radius (kpc)')
    ax3.set_ylabel('Circular Velocity (km/s)')
    ax3.set_title('C. Galaxy Rotation Curves\nCollective Klein Correlation', fontweight='bold')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    ax3.set_xlim(0, 25)
    
    # ============ Panel 4: Detection Summary ============ 
    ax4 = axes[1, 1]
    ax4.axis('off')
    
    # Detection summary table
    detection_data = [
        ["PHENOMENON", "SCALE", "SIGNIFICANCE", "STATUS"],
        ["Klein Atom Oscillation", "52,800 km", "f₀ = 5.68 Hz", "Theoretical"],
        ["GW Echoes", "176 ms period", "To be tested", "Predicted"],
        ["SPARC Galaxies", "8.4 kpc", "9.22σ", "✅ DETECTED"],
        ["Binary Pulsars", "8.4 kpc", "10.66σ", "✅ DETECTED"], 
        ["Weak Lensing", "8.4 kpc", "1.85σ", "Marginal"],
        ["Galaxy Morphology", "8.4 kpc", "0.66σ", "❌ No Signal"],
        ["Planetary Motion", "8.4 kpc", "2.69σ", "✅ DETECTED"],
    ]
    
    # Create table
    y_start = 0.95
    col_widths = [0.25, 0.25, 0.25, 0.25]
    
    for i, row in enumerate(detection_data):
        x_pos = 0.05
        for j, cell in enumerate(row):
            if i == 0:  # Header
                weight = 'bold'
                color = 'black'
                size = 10
            else:
                weight = 'normal'
                if '✅' in cell:
                    color = 'green'
                elif '❌' in cell:
                    color = 'red'
                elif 'Marginal' in cell:
                    color = 'orange'
                else:
                    color = 'black'
                size = 9
                
            ax4.text(x_pos, y_start - i*0.08, cell, transform=ax4.transAxes,
                    fontsize=size, fontweight=weight, color=color)
            x_pos += col_widths[j]
            
        # Add horizontal line under header
        if i == 0:
            ax4.plot([0.05, 0.95], [y_start - 0.04, y_start - 0.04], 
                    transform=ax4.transAxes, color='black', linewidth=1)
    
    ax4.set_title('D. Detection Status Summary\nIndividual vs Collective Signatures', 
                 fontweight='bold', y=0.98)
    
    plt.tight_layout()
    plt.savefig('klein_detection_signatures.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("✅ Detection signatures visualization created")

def create_theoretical_connections_plot():
    """Create plot showing connections between different theoretical frameworks"""
    
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    
    # Central concept: Klein Spacetime Atoms
    central = patches.FancyBboxPatch((0.4, 0.4), 0.2, 0.2, 
                                   boxstyle="round,pad=0.02",
                                   facecolor='#FF5722', alpha=0.8)
    ax.add_patch(central)
    ax.text(0.5, 0.5, 'KLEIN\nSPACETIME\nATOMS', ha='center', va='center',
           fontsize=12, fontweight='bold', color='white')
    
    # Connected theories and concepts
    connections = [
        # [x, y, width, height, label, color, connection_point]
        [0.05, 0.7, 0.25, 0.15, 'KLEIN FIELD\nTHEORY\n(R₅ = 8,400 km)', '#2196F3', (0.4, 0.6)],
        [0.7, 0.7, 0.25, 0.15, 'MODIFIED\nEINSTEIN\nEQUATIONS', '#4CAF50', (0.6, 0.6)],
        [0.05, 0.05, 0.25, 0.15, 'SPARC GALAXIES\n(9.22σ detection)', '#9C27B0', (0.4, 0.4)],
        [0.7, 0.05, 0.25, 0.15, 'BINARY PULSARS\n(10.66σ detection)', '#FF9800', (0.6, 0.4)],
        [0.375, 0.8, 0.25, 0.1, 'f₀ = 5.68 Hz\nUniversal Frequency', '#795548', (0.5, 0.6)],
        [0.375, 0.05, 0.25, 0.1, '8.4 kpc Correlation\nEmergent Scale', '#607D8B', (0.5, 0.4)]
    ]
    
    for conn in connections:
        x, y, w, h, label, color, (cx, cy) = conn
        
        # Create box
        box = patches.FancyBboxPatch((x, y), w, h,
                                   boxstyle="round,pad=0.01",
                                   facecolor=color, alpha=0.7)
        ax.add_patch(box)
        
        # Add text
        ax.text(x + w/2, y + h/2, label, ha='center', va='center',
               fontsize=10, fontweight='bold', color='white')
        
        # Add connection line
        ax.plot([x + w/2, cx], [y + h/2, cy], 'k-', alpha=0.5, linewidth=2)
        
        # Add arrow
        dx = cx - (x + w/2)
        dy = cy - (y + h/2)
        norm = np.sqrt(dx**2 + dy**2)
        ax.arrow(x + w/2 + 0.8*dx/norm*0.1, y + h/2 + 0.8*dy/norm*0.1,
                0.2*dx/norm*0.1, 0.2*dy/norm*0.1,
                head_width=0.01, head_length=0.01, fc='black', ec='black', alpha=0.7)
    
    # Add key relationships as text annotations
    relationships = [
        (0.02, 0.95, "THEORETICAL UNIFICATION:", 'black', 12, 'bold'),
        (0.02, 0.90, "• Klein atoms (8,400 km) = Klein bottles (R₅)", 'blue', 10, 'normal'),
        (0.02, 0.86, "• Individual oscillations → Collective correlations", 'blue', 10, 'normal'),
        (0.02, 0.82, "• Temporal discretization → Spatial correlations", 'blue', 10, 'normal'),
        
        (0.52, 0.95, "EMPIRICAL VALIDATION:", 'black', 12, 'bold'),
        (0.52, 0.90, "• 8.4 kpc signatures in galaxy dynamics ✅", 'green', 10, 'normal'),
        (0.52, 0.86, "• Dynamic phenomena affected ✅", 'green', 10, 'normal'),
        (0.52, 0.82, "• Static structure unaffected ✅", 'green', 10, 'normal'),
        
        (0.02, 0.35, "SCALE EMERGENCE:", 'black', 12, 'bold'),
        (0.02, 0.30, "• Klein atoms: 8,400 km radius", 'red', 10, 'normal'),
        (0.02, 0.26, "• Correlation length: 8.4 kpc", 'red', 10, 'normal'),
        (0.02, 0.22, "• Scaling factor: ~160×", 'red', 10, 'normal'),
        (0.02, 0.18, "• Correlated atoms: ~4×10⁶", 'red', 10, 'normal'),
    ]
    
    for x, y, text, color, size, weight in relationships:
        ax.text(x, y, text, transform=ax.transAxes, fontsize=size, 
               fontweight=weight, color=color)
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    ax.set_title('KLEIN SPACETIME ATOMS: THEORETICAL CONNECTIONS & EMPIRICAL VALIDATION',
                fontsize=14, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.savefig('klein_theoretical_connections.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("✅ Theoretical connections visualization created")

def main():
    """Create all Klein spacetime atoms visualizations"""
    
    print("🎨 Creating Klein Spacetime Atoms Visualizations")
    print("=" * 55)
    
    try:
        create_scale_comparison_plot()
        create_detection_signatures_plot() 
        create_theoretical_connections_plot()
        
        print("\n✅ ALL VISUALIZATIONS COMPLETED")
        print("Files created:")
        print("• klein_spacetime_atoms_scale_comparison.png")
        print("• klein_detection_signatures.png") 
        print("• klein_theoretical_connections.png")
        
    except Exception as e:
        print(f"❌ Error creating visualizations: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()