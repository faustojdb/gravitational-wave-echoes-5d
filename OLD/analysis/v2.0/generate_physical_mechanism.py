#!/usr/bin/env python3
"""
Physical Mechanism Diagram for Paper I v2.0
Shows how gravitational wave echoes are generated in 5D Klein bottle
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle, Arrow
import os

# Set up the figure
fig = plt.figure(figsize=(16, 12))
gs = gridspec.GridSpec(2, 2, figure=fig, hspace=0.3, wspace=0.3)

# Color scheme
colors = {
    'merger': '#E74C3C',        # Red
    'gw_4d': '#3498DB',         # Blue  
    'gw_5d': '#9B59B6',         # Purple
    'echo': '#F39C12',          # Orange
    'medium': '#2ECC71',        # Green
    'klein': '#34495E',         # Dark gray
    'detector': '#E67E22'       # Dark orange
}

# Main title
fig.suptitle('Physical Mechanism: 5D Gravitational Wave Echo Generation\n' + 
             r'From Black Hole Merger to Klein Bottle Resonance', 
             fontsize=18, fontweight='bold')

# ============================================================================
# Panel A: 5D Wave Propagation Process
# ============================================================================
ax1 = fig.add_subplot(gs[0, 0])
ax1.set_aspect('equal')

# Draw the process timeline
timeline_y = 0.5
process_steps = [
    (0.1, 'BH Merger\nt = 0'),
    (0.3, '4D GW\nPropagation'),
    (0.5, '5D Coupling\n~1% energy'),
    (0.7, '5D Propagation\nc_eff = c/6.4'),
    (0.9, 'Echo Return\nt = τ')
]

# Draw timeline
ax1.arrow(0.05, timeline_y, 0.9, 0, head_width=0.03, head_length=0.02, 
         fc='black', ec='black', linewidth=2)

# Add process steps
for i, (x, label) in enumerate(process_steps):
    # Draw step marker
    circle = Circle((x, timeline_y), 0.04, color=colors['merger'] if i == 0 
                   else colors['echo'] if i == 4 else colors['gw_5d'], 
                   zorder=3)
    ax1.add_patch(circle)
    
    # Add label
    ax1.text(x, timeline_y + 0.15, label, ha='center', va='bottom', 
            fontsize=10, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))

# Add Klein bottle representation
klein_center = (0.5, 0.2)
klein_width, klein_height = 0.3, 0.15

# Klein bottle as figure-8
theta = np.linspace(0, 2*np.pi, 100)
klein_x = klein_center[0] + 0.1 * np.cos(theta) + 0.05 * np.cos(2*theta)
klein_y = klein_center[1] + 0.08 * np.sin(theta)
ax1.plot(klein_x, klein_y, color=colors['klein'], linewidth=3)

# Add 5D propagation path
path_x = np.linspace(0.45, 0.55, 20)
path_y = klein_center[1] + 0.02 * np.sin(10 * np.pi * (path_x - 0.45) / 0.1)
ax1.plot(path_x, path_y, color=colors['gw_5d'], linewidth=2, linestyle='--')

# Add annotations
ax1.text(0.5, 0.05, 'Klein Bottle\n5th Dimension', ha='center', 
         fontsize=12, fontweight='bold',
         bbox=dict(boxstyle='round,pad=0.5', facecolor=colors['klein'], 
                  alpha=0.3, edgecolor=colors['klein']))

ax1.set_title('Panel A: Echo Generation Process\nStep-by-Step Mechanism', 
              fontweight='bold')
ax1.set_xlim(0, 1)
ax1.set_ylim(0, 0.8)
ax1.axis('off')

# ============================================================================
# Panel B: Compressible Medium Properties
# ============================================================================
ax2 = fig.add_subplot(gs[0, 1])

# Medium parameters
rho_5d = 4.45e19  # kg/m³
K = 1e35         # Pa
c = 3e8          # m/s
c_eff = c / 6.403

# Create visualization of medium properties
x = np.linspace(0, 1, 100)

# Density variation (conceptual)
density_profile = rho_5d * (1 + 0.1 * np.sin(10 * np.pi * x))

# Plot density
ax2_twin = ax2.twinx()
line1 = ax2.plot(x, density_profile/1e19, color=colors['medium'], linewidth=3,
                label=f'Density: ρ = {rho_5d:.1e} kg/m³')

# Effective velocity
velocity_profile = c_eff * np.ones_like(x)
line2 = ax2_twin.plot(x, velocity_profile/1e7, color=colors['gw_5d'], linewidth=3,
                     label=f'c_eff = c/6.403 = {c_eff:.1e} m/s')

# Add bulk modulus annotation
ax2.text(0.5, rho_5d/1e19 * 1.1, f'Bulk Modulus\nK = {K:.0e} Pa\n(Ultra-dense matter)', 
         ha='center', va='bottom', fontsize=11,
         bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.8))

# Add wave propagation illustration
wave_x = np.linspace(0.1, 0.9, 50)
wave_y = rho_5d/1e19 * 0.95 + 0.1 * np.sin(20 * np.pi * wave_x)
ax2.plot(wave_x, wave_y, color=colors['gw_5d'], linewidth=2, alpha=0.7)

# Add arrows showing wave direction
for i in range(0, len(wave_x), 10):
    ax2.arrow(wave_x[i], wave_y[i], 0.05, 0, head_width=0.02, head_length=0.02,
             fc=colors['gw_5d'], ec=colors['gw_5d'], alpha=0.5)

ax2.set_title('Panel B: 5D Medium Properties\nCompressible Klein Bottle Interior', 
              fontweight='bold')
ax2.set_xlabel('Position in 5D')
ax2.set_ylabel('Density (×10¹⁹ kg/m³)', color=colors['medium'])
ax2_twin.set_ylabel('Velocity (×10⁷ m/s)', color=colors['gw_5d'])

# Color the y-axis labels
ax2.tick_params(axis='y', labelcolor=colors['medium'])
ax2_twin.tick_params(axis='y', labelcolor=colors['gw_5d'])

# Add combined legend
lines1, labels1 = ax2.get_legend_handles_labels()
lines2, labels2 = ax2_twin.get_legend_handles_labels()
ax2.legend(lines1 + lines2, labels1 + labels2, loc='upper right')

ax2.grid(True, alpha=0.3)

# ============================================================================
# Panel C: Coupling Mechanism 4D ↔ 5D
# ============================================================================
ax3 = fig.add_subplot(gs[1, 0])

# Draw 4D spacetime (left side)
spacetime_4d = patches.Rectangle((0.1, 0.2), 0.3, 0.6, 
                                linewidth=2, edgecolor=colors['gw_4d'], 
                                facecolor=colors['gw_4d'], alpha=0.3)
ax3.add_patch(spacetime_4d)

# Draw 5D Klein bottle (right side)
spacetime_5d = patches.Ellipse((0.7, 0.5), 0.25, 0.4, 
                              linewidth=2, edgecolor=colors['klein'], 
                              facecolor=colors['klein'], alpha=0.3)
ax3.add_patch(spacetime_5d)

# Add merger location
merger_point = Circle((0.25, 0.5), 0.03, color=colors['merger'], zorder=3)
ax3.add_patch(merger_point)

# Add coupling region
coupling_region = patches.Rectangle((0.4, 0.3), 0.2, 0.4, 
                                   linewidth=2, edgecolor='orange', 
                                   facecolor='orange', alpha=0.2)
ax3.add_patch(coupling_region)

# Add energy flow arrows
# 4D → Coupling
ax3.arrow(0.4, 0.5, -0.08, 0, head_width=0.03, head_length=0.02,
         fc=colors['gw_4d'], ec=colors['gw_4d'], linewidth=3)
ax3.text(0.32, 0.55, '99% Energy\n4D Propagation', ha='center', fontsize=9,
         bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))

# Coupling → 5D
ax3.arrow(0.6, 0.5, 0.08, 0, head_width=0.03, head_length=0.02,
         fc=colors['gw_5d'], ec=colors['gw_5d'], linewidth=3)
ax3.text(0.68, 0.55, '1% Energy\n5D Coupling', ha='center', fontsize=9,
         bbox=dict(boxstyle='round', facecolor='lightpurple', alpha=0.8))

# 5D → 4D (echo return)
ax3.arrow(0.6, 0.4, -0.08, 0, head_width=0.03, head_length=0.02,
         fc=colors['echo'], ec=colors['echo'], linewidth=3)
ax3.text(0.52, 0.35, 'Echo Return\n~0.1% Energy', ha='center', fontsize=9,
         bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

# Labels
ax3.text(0.25, 0.1, '4D Spacetime\n(Observable)', ha='center', fontweight='bold',
         fontsize=12, bbox=dict(boxstyle='round', facecolor=colors['gw_4d'], alpha=0.5))
ax3.text(0.7, 0.1, '5D Klein Bottle\n(Hidden)', ha='center', fontweight='bold',
         fontsize=12, bbox=dict(boxstyle='round', facecolor=colors['klein'], alpha=0.5))
ax3.text(0.5, 0.85, 'Coupling Region\nη ~ 1%', ha='center', fontweight='bold',
         fontsize=12, bbox=dict(boxstyle='round', facecolor='orange', alpha=0.5))

ax3.set_title('Panel C: 4D ↔ 5D Coupling Mechanism\nEnergy Transfer Process', 
              fontweight='bold')
ax3.set_xlim(0, 1)
ax3.set_ylim(0, 1)
ax3.axis('off')

# ============================================================================
# Panel D: Echo Detection Timeline
# ============================================================================
ax4 = fig.add_subplot(gs[1, 1])

# Time axis
t_max = 0.5
t = np.linspace(0, t_max, 1000)

# Main GW signal (simplified)
def gw_signal(t, t_merger=0, f_start=35, f_end=250):
    mask = t >= t_merger
    result = np.zeros_like(t)
    t_rel = t[mask] - t_merger
    
    # Chirp frequency evolution
    f_inst = f_start + (f_end - f_start) * (t_rel / 0.1)**3
    f_inst = np.minimum(f_inst, f_end)
    
    # Amplitude decay
    amp = np.exp(-t_rel / 0.05)
    
    # Phase evolution
    phase = 2 * np.pi * np.cumsum(f_inst) * (t[1] - t[0])
    result[mask] = amp * np.sin(phase)
    
    return result

# Echo signal
tau_echo = 0.1496
def echo_signal(t, tau=tau_echo, amp=0.01):
    mask = t >= tau
    result = np.zeros_like(t)
    t_rel = t[mask] - tau
    
    # Echo frequency (42 rad/s = 6.68 Hz)
    f_echo = 6.68
    decay = np.exp(-t_rel / 0.1)
    result[mask] = amp * decay * np.sin(2 * np.pi * f_echo * t_rel)
    
    return result

# Generate signals
h_main = gw_signal(t)
h_echo = echo_signal(t)
h_total = h_main + h_echo

# Add noise
np.random.seed(42)
noise = 0.05 * np.random.normal(0, 1, len(t))
h_observed = h_total + noise

# Plot signals
ax4.plot(t, h_observed, color='gray', alpha=0.5, linewidth=1, label='LIGO Data (with noise)')
ax4.plot(t, h_main, color=colors['gw_4d'], linewidth=2, label='Main GW Signal')
ax4.plot(t, 10*h_echo, color=colors['echo'], linewidth=2, label='Echo (×10 amplified)')

# Mark echo time
ax4.axvline(tau_echo, color=colors['echo'], linestyle='--', linewidth=2, alpha=0.7)
ax4.text(tau_echo + 0.01, 0.8, f'Echo Detection\nτ = {tau_echo} s', 
         fontsize=10, bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.8))

# Mark merger time
ax4.axvline(0, color=colors['merger'], linestyle='--', linewidth=2, alpha=0.7)
ax4.text(0.01, 0.8, 'BH Merger\nt = 0', 
         fontsize=10, bbox=dict(boxstyle='round', facecolor='red', alpha=0.8))

# Add phases
phases = [
    (0, 0.05, 'Inspiral'),
    (0.05, 0.1, 'Merger'),
    (0.1, tau_echo, 'Ringdown'),
    (tau_echo, 0.3, 'Echo')
]

for i, (t_start, t_end, phase) in enumerate(phases):
    y_pos = -0.6 - 0.1 * (i % 2)
    ax4.annotate('', xy=(t_end, y_pos), xytext=(t_start, y_pos),
                arrowprops=dict(arrowstyle='<->', color='black', lw=1.5))
    ax4.text((t_start + t_end)/2, y_pos - 0.1, phase, ha='center', fontsize=9)

ax4.set_title('Panel D: Echo Detection Timeline\nFrom Merger to Echo', fontweight='bold')
ax4.set_xlabel('Time (s)')
ax4.set_ylabel('GW Strain (arbitrary units)')
ax4.legend()
ax4.grid(True, alpha=0.3)
ax4.set_xlim(0, 0.4)
ax4.set_ylim(-1, 1)

# Save the figure
figures_dir = 'figures'
os.makedirs(figures_dir, exist_ok=True)

plt.tight_layout()
plt.savefig(f'{figures_dir}/figure_4_physical_mechanism.png', 
            dpi=300, bbox_inches='tight', facecolor='white')
plt.savefig(f'{figures_dir}/figure_4_physical_mechanism.pdf', 
            bbox_inches='tight', facecolor='white')

print("Physical Mechanism diagram created successfully!")
print("Files saved in figures/ directory:")
print("- figure_4_physical_mechanism.png (300 DPI)")
print("- figure_4_physical_mechanism.pdf (vector format)")

plt.show()