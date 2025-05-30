#!/usr/bin/env python3
"""
Klein Bottle Topology Diagram for Paper I v2.0
Creates a sophisticated visualization of the 5D Klein bottle structure
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch
import matplotlib.gridspec as gridspec

# Set up the figure with multiple subplots
fig = plt.figure(figsize=(20, 12))
gs = gridspec.GridSpec(2, 3, figure=fig)

# Color scheme
colors = {
    'klein': '#2E86AB',      # Blue
    'modes': '#A23B72',      # Purple  
    'universe': '#F18F01',   # Orange
    'forbidden': '#C73E1D',  # Red
    'allowed': '#52A270',    # Green
    'background': '#F5F5F5'  # Light gray
}

# Main title
fig.suptitle('Klein Bottle Topology: Fifth Dimension Structure\n' + 
             r'$R = 1751.173$ km, $\omega_0 = 42$ rad/s', 
             fontsize=20, fontweight='bold')

# ============================================================================
# Panel 1: Klein Bottle 3D Visualization
# ============================================================================
ax1 = fig.add_subplot(gs[0, :2], projection='3d')

def klein_bottle_parametric(u, v):
    """
    Parametric equations for Klein bottle in 3D (immersion)
    """
    x = (2 + np.cos(v/2) * np.sin(u) - np.sin(v/2) * np.sin(2*u)) * np.cos(v)
    y = (2 + np.cos(v/2) * np.sin(u) - np.sin(v/2) * np.sin(2*u)) * np.sin(v)
    z = np.sin(v/2) * np.sin(u) + np.cos(v/2) * np.sin(2*u)
    return x, y, z

# Create parameter space
u = np.linspace(0, 2*np.pi, 50)
v = np.linspace(0, 2*np.pi, 50)
U, V = np.meshgrid(u, v)

# Generate Klein bottle surface
X, Y, Z = klein_bottle_parametric(U, V)

# Plot the Klein bottle surface
surface = ax1.plot_surface(X, Y, Z, alpha=0.7, cmap='viridis', 
                          facecolors=plt.cm.coolwarm(V/np.pi))

# Add vibration mode indicators (only odd modes)
odd_modes = [1, 3, 5, 7]
mode_colors = ['red', 'orange', 'yellow', 'green']

for i, (mode, color) in enumerate(zip(odd_modes, mode_colors)):
    # Add mode indicators along the Klein bottle
    theta = np.linspace(0, 2*np.pi, 20)
    mode_x = 3.5 * np.cos(theta)
    mode_y = 3.5 * np.sin(theta) 
    mode_z = 0.5 * np.sin(mode * theta) + 2 + i*0.3
    
    ax1.plot(mode_x, mode_y, mode_z, color=color, linewidth=3,
             label=f'Mode n={mode}')

# Styling
ax1.set_title('5D Klein Bottle Topology\n(Non-Orientable Surface)', 
              fontsize=14, fontweight='bold')
ax1.set_xlabel('X')
ax1.set_ylabel('Y') 
ax1.set_zlabel('Z')
ax1.legend(loc='upper left', bbox_to_anchor=(0, 1))

# ============================================================================
# Panel 2: Mode Spectrum Diagram  
# ============================================================================
ax2 = fig.add_subplot(gs[0, 2])

# Mode data
all_modes = np.arange(1, 9)
frequencies = 42 * all_modes  # ω_n = n × ω_0
amplitudes = np.where(all_modes % 2 == 1, 1/all_modes, 0)  # Only odd modes

# Create bar plot
bars = ax2.bar(all_modes, amplitudes, color=[colors['allowed'] if n%2==1 
               else colors['forbidden'] for n in all_modes])

# Add frequency labels
for i, (mode, freq, amp) in enumerate(zip(all_modes, frequencies, amplitudes)):
    if amp > 0:  # Only for allowed modes
        ax2.text(mode, amp + 0.05, f'{freq} rad/s', 
                ha='center', va='bottom', fontsize=9, rotation=45)
    else:  # For forbidden modes
        ax2.text(mode, 0.1, 'FORBIDDEN', ha='center', va='bottom', 
                color='red', fontsize=8, fontweight='bold')

ax2.set_title('Klein Bottle Mode Spectrum\n(Only Odd Modes Allowed)', 
              fontsize=12, fontweight='bold')
ax2.set_xlabel('Mode Number (n)')
ax2.set_ylabel('Relative Amplitude')
ax2.set_ylim(0, 1.2)
ax2.grid(True, alpha=0.3)

# Add legend
from matplotlib.lines import Line2D
legend_elements = [Line2D([0], [0], color=colors['allowed'], lw=4, label='Allowed (odd)'),
                   Line2D([0], [0], color=colors['forbidden'], lw=4, label='Forbidden (even)')]
ax2.legend(handles=legend_elements, loc='upper right')

# ============================================================================
# Panel 3: Dimensional Evolution
# ============================================================================
ax3 = fig.add_subplot(gs[1, 0])

# Time evolution data
z_values = np.logspace(-3, 1, 100)  # Redshift from z=0.001 to z=10
a_values = 1 / (1 + z_values)      # Scale factor
R_values = 1751.173 * (a_values)**(3/4)  # R(t) ∝ a^(3/4)

# Plot evolution
ax3.loglog(z_values, R_values, color=colors['klein'], linewidth=3)

# Mark important epochs
epochs = {
    'Today': (0, 1751.173),
    'Recombination': (1000, 9.8),
    'Matter-Radiation\nEquality': (3400, 5.2)
}

for label, (z, R) in epochs.items():
    if 0.001 <= z <= 10:  # Only plot if in range
        ax3.plot(z, R, 'o', markersize=10, color=colors['universe'])
        ax3.annotate(f'{label}\nz={z}, R={R:.1f} km', 
                    xy=(z, R), xytext=(10, 10), 
                    textcoords='offset points', fontsize=9,
                    bbox=dict(boxstyle='round,pad=0.3', fc='yellow', alpha=0.7))

ax3.set_title('Dimensional Evolution\n' + r'$R(t) \propto a(t)^{3/4}$', 
              fontsize=12, fontweight='bold')
ax3.set_xlabel('Redshift (z)')
ax3.set_ylabel('5D Radius R (km)')
ax3.grid(True, alpha=0.3)

# ============================================================================
# Panel 4: Cross-Section View
# ============================================================================
ax4 = fig.add_subplot(gs[1, 1])

# Create a cross-sectional view of Klein bottle
theta = np.linspace(0, 2*np.pi, 1000)

# Klein bottle cross-section (figure-8 like shape)
r1 = 1 + 0.3 * np.cos(2*theta)
x1 = r1 * np.cos(theta)
y1 = r1 * np.sin(theta)

# Plot the cross-section
ax4.plot(x1, y1, color=colors['klein'], linewidth=3)

# Add identification lines showing non-orientable property
# Points that get identified
identify_points = [(0, 1.3), (0, -1.3)]
for point in identify_points:
    circle = plt.Circle(point, 0.1, color='red', fill=True)
    ax4.add_patch(circle)

# Arrow showing identification
ax4.annotate('', xy=(0, -1.3), xytext=(0, 1.3),
            arrowprops=dict(arrowstyle='<->', color='red', lw=2))
ax4.text(0.2, 0, 'Non-orientable\nIdentification\n(φ, χ) ~ (φ+π, -χ)', 
         fontsize=10, bbox=dict(boxstyle='round', facecolor='lightblue'))

# Add current universe indicator
universe_circle = plt.Circle((0, 0), 0.05, color=colors['universe'], fill=True)
ax4.add_patch(universe_circle)
ax4.text(0.1, 0, 'Our 4D\nUniverse', fontsize=9, 
         bbox=dict(boxstyle='round', facecolor='yellow'))

ax4.set_title('Klein Bottle Cross-Section\n(Non-Orientable Topology)', 
              fontsize=12, fontweight='bold')
ax4.set_aspect('equal')
ax4.grid(True, alpha=0.3)
ax4.set_xlim(-2, 2)
ax4.set_ylim(-2, 2)

# ============================================================================
# Panel 5: Physical Parameters Summary
# ============================================================================
ax5 = fig.add_subplot(gs[1, 2])
ax5.axis('off')

# Create text summary of key parameters
summary_text = f"""
KLEIN BOTTLE PARAMETERS

Fundamental Frequency:
ω₀ = 42.00 rad/s
f₀ = 6.68 Hz
τ = 0.1496 s

Dimensional Scale:
R = 1751.173 km
(Not ~1000 km!)

5D Medium Properties:
ρ₅ᴰ = 4.45×10¹⁹ kg/m³
K = 10³⁵ Pa
c_eff = c/6.403

Dark Matter Connection:
ρ_DM = N_eff × ℏc/(2πR⁴c²)
N_eff = 4.02×10⁴¹

Topological Properties:
• Non-orientable surface
• Only odd modes allowed
• π₁(Klein) = ℤ ⋊ ℤ
• χ(Klein) = 0

Evolution:
R(t) ∝ a(t)³/⁴
"""

ax5.text(0.05, 0.95, summary_text, transform=ax5.transAxes, 
         fontsize=11, verticalalignment='top', fontfamily='monospace',
         bbox=dict(boxstyle='round,pad=0.5', facecolor='lightgray', alpha=0.8))

# Add small Klein bottle icon
klein_x = np.linspace(0, 2*np.pi, 50)
klein_r = 0.03 + 0.01*np.cos(2*klein_x)
klein_xx = 0.85 + klein_r*np.cos(klein_x)
klein_yy = 0.15 + klein_r*np.sin(klein_x)
ax5.plot(klein_xx, klein_yy, color=colors['klein'], linewidth=2)

plt.tight_layout()

# Create figures directory if it doesn't exist
import os
figures_dir = 'figures'
os.makedirs(figures_dir, exist_ok=True)

# Save figures in the figures directory
plt.savefig(f'{figures_dir}/figure_1_klein_topology_diagram.png', 
            dpi=300, bbox_inches='tight', facecolor='white')
plt.savefig(f'{figures_dir}/figure_1_klein_topology_diagram.pdf', 
            bbox_inches='tight', facecolor='white')
plt.show()

print("Klein bottle topology diagram created successfully!")
print("Files saved in figures/ directory:")
print("- figure_1_klein_topology_diagram.png (300 DPI)")
print("- figure_1_klein_topology_diagram.pdf (vector format)")