#!/usr/bin/env python3
"""
Paradigm Comparison Diagram for Paper I v2.0
Compares emergent vs eternal Klein bottle paradigms and implications
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Ellipse, Arrow
import os

# Set up the figure
fig = plt.figure(figsize=(16, 14))
gs = gridspec.GridSpec(3, 2, figure=fig, hspace=0.4, wspace=0.3, height_ratios=[1, 1, 0.8])

# Color scheme
colors = {
    'emergent': '#E74C3C',      # Red
    'eternal': '#3498DB',       # Blue
    'cyclic': '#2ECC71',        # Green
    'heat_death': '#95A5A6',    # Gray
    'habitable': '#F39C12',     # Orange
    'civilization': '#9B59B6',  # Purple
    'constants': '#E67E22'      # Dark orange
}

# Main title
fig.suptitle('Cosmological Paradigm Comparison\n' + 
             r'Emergent vs Eternal Klein Bottle: Implications for Universe and Life', 
             fontsize=18, fontweight='bold')

# ============================================================================
# Panel A: Emergent Klein Paradigm
# ============================================================================
ax1 = fig.add_subplot(gs[0, 0])

# Timeline for emergent paradigm
t_cosmic = np.logspace(-6, 2, 1000)  # From 10^-6 to 10^2 Gyr
t_bigbang = 0
t_now = 13.8

# R evolution in emergent paradigm (starts from 0)
R_emergent = 1751 * (t_cosmic / t_now)**(3/4)
R_emergent[t_cosmic < 1e-3] = 0  # R = 0 before Klein formation

ax1.loglog(t_cosmic, R_emergent, color=colors['emergent'], linewidth=3,
          label='Emergent: R grows from 0')

# Mark formation epoch
t_formation = 1e-3  # Formation at ~1 million years
ax1.axvline(t_formation, color=colors['emergent'], linestyle='--', alpha=0.7)
ax1.text(t_formation * 1.5, 10, 'Klein Bottle\nFormation', fontsize=10,
         bbox=dict(boxstyle='round', facecolor='red', alpha=0.3))

# Problems with emergent paradigm
problems_text = """PROBLEMS:
• Constants should vary with z
• Fine-tuning of formation time
• Unstable topology
• Information paradox"""

ax1.text(0.02, 0.98, problems_text, transform=ax1.transAxes, fontsize=10,
         bbox=dict(boxstyle='round,pad=0.5', facecolor='lightyellow', alpha=0.9),
         verticalalignment='top')

ax1.set_title('Panel A: Emergent Klein Paradigm\n"Klein Bottle Forms with Universe"', 
              fontweight='bold', color=colors['emergent'])
ax1.set_xlabel('Time (Gyr)')
ax1.set_ylabel('5D Radius R (km)')
ax1.grid(True, alpha=0.3)
ax1.set_ylim(0.1, 10000)

# ============================================================================
# Panel B: Eternal Klein Paradigm
# ============================================================================
ax2 = fig.add_subplot(gs[0, 1])

# R evolution in eternal paradigm (oscillates around eternal geometry)
R_eternal_base = 1751 * np.ones_like(t_cosmic)  # Base eternal value
R_eternal_oscillation = 1751 * (1 + 0.5 * np.sin(2 * np.pi * np.log10(t_cosmic)))
R_eternal = np.where(t_cosmic > 1e-6, R_eternal_oscillation, R_eternal_base)

ax2.semilogx(t_cosmic, R_eternal, color=colors['eternal'], linewidth=3,
            label='Eternal: R oscillates around fixed geometry')

# Mark Big Bang as local event
t_bigbang_local = 1e-2  # Big Bang as local reconnection
ax2.axvline(t_bigbang_local, color='orange', linewidth=2, alpha=0.7)
ax2.text(t_bigbang_local * 1.5, 2500, 'Big Bang:\nLocal Reconnection', fontsize=10,
         bbox=dict(boxstyle='round', facecolor='orange', alpha=0.3))

# Advantages of eternal paradigm
advantages_text = """ADVANTAGES:
✓ Constants remain invariant
✓ Natural topology
✓ Resolves fine-tuning
✓ Information preserved"""

ax2.text(0.02, 0.98, advantages_text, transform=ax2.transAxes, fontsize=10,
         bbox=dict(boxstyle='round,pad=0.5', facecolor='lightcyan', alpha=0.9),
         verticalalignment='top')

ax2.set_title('Panel B: Eternal Klein Paradigm (Favored)\n"Klein Bottle is Eternal Structure"', 
              fontweight='bold', color=colors['eternal'])
ax2.set_xlabel('Time (Gyr)')
ax2.set_ylabel('5D Radius R (km)')
ax2.grid(True, alpha=0.3)
ax2.set_ylim(500, 3000)

# ============================================================================
# Panel C: Cyclic vs Heat Death Cosmology
# ============================================================================
ax3 = fig.add_subplot(gs[1, 0])

# Very long time scale for cosmic cycles
t_cycle = np.logspace(1, 100, 1000)  # 10 Gyr to 10^100 years
cycle_period = 1e50  # years

# Cyclic universe energy
energy_cyclic = 1 + 0.5 * np.sin(2 * np.pi * t_cycle / cycle_period)

# Heat death universe energy (exponential decay)
energy_heat_death = np.exp(-t_cycle / 1e15)  # Decay over 10^15 years

ax3.loglog(t_cycle, energy_cyclic, color=colors['cyclic'], linewidth=3,
          label='Cyclic Universe (Klein Model)')
ax3.loglog(t_cycle, energy_heat_death, color=colors['heat_death'], linewidth=3,
          label='Heat Death (Standard Model)')

# Mark current epoch
t_current = 1.38e1
ax3.axvline(t_current, color='red', linewidth=2, alpha=0.7, label='Current Epoch')

# Mark cycle phases
cycle_phases = [
    (1e20, 'Expansion Phase'),
    (1e40, 'Maximum R'),
    (1e60, 'Contraction'),
    (1e80, 'Reconnection')
]

for t_phase, phase_name in cycle_phases:
    if 1e1 <= t_phase <= 1e100:
        ax3.axvline(t_phase, color=colors['cyclic'], alpha=0.3, linestyle=':')
        ax3.text(t_phase, 2, phase_name, rotation=90, ha='center', va='bottom', fontsize=8)

ax3.set_title('Panel C: Cosmological Destiny\nCyclic vs Heat Death', fontweight='bold')
ax3.set_xlabel('Time (years)')
ax3.set_ylabel('Cosmic Energy (relative)')
ax3.legend()
ax3.grid(True, alpha=0.3)

# ============================================================================
# Panel D: Fundamental Constants Evolution
# ============================================================================
ax4 = fig.add_subplot(gs[1, 1])

# Redshift range
z = np.logspace(-2, 3, 100)  # z = 0.01 to 1000

# In emergent paradigm: constants should vary
alpha_emergent = 1/137 * (1 + 0.1 * z / (1 + z))  # Fine structure "constant" varies
G_emergent = 6.67e-11 * (1 + 0.05 * z / (1 + z))  # Gravitational "constant" varies

# In eternal paradigm: constants remain constant
alpha_eternal = 1/137 * np.ones_like(z)
G_eternal = 6.67e-11 * np.ones_like(z)

# Plot fine structure constant
ax4.semilogx(z, alpha_emergent * 137, color=colors['emergent'], linewidth=3,
            label='Emergent: α varies')
ax4.semilogx(z, alpha_eternal * 137, color=colors['eternal'], linewidth=3,
            label='Eternal: α constant')

# Add observational constraints
ax4.axhline(1/137 * 137, color='black', linestyle='--', alpha=0.7, 
           label='Observed value')
ax4.fill_between([1e-2, 1e3], [136.8, 136.8], [137.2, 137.2], 
                alpha=0.3, color='gray', label='Observational limits')

# Mark key epochs
epochs_z = [0, 1100, 3400]
epoch_names = ['Today', 'Recombination', 'Matter-Rad Eq.']
for z_epoch, name in zip(epochs_z, epoch_names):
    if z_epoch > 0:
        ax4.axvline(z_epoch, color='orange', alpha=0.5, linestyle=':')
        ax4.text(z_epoch, 137.1, name, rotation=90, ha='center', va='bottom', fontsize=8)

ax4.set_title('Panel D: Fundamental Constants\nTest of Paradigms', fontweight='bold')
ax4.set_xlabel('Redshift z')
ax4.set_ylabel('Fine Structure Constant α⁻¹')
ax4.legend()
ax4.grid(True, alpha=0.3)
ax4.set_ylim(136.5, 137.5)

# ============================================================================
# Panel E: Implications for Life and Civilization (spanning bottom)
# ============================================================================
ax5 = fig.add_subplot(gs[2, :])

# Cosmic history timeline
t_life = np.linspace(0, 30, 1000)  # 0 to 30 Gyr
R_life = 1751 * ((t_life + 0.1) / 13.8)**(3/4)  # Avoid t=0 singularity

# Habitable zone
R_hab_min, R_hab_max = 1000, 2000
habitable_mask = (R_life >= R_hab_min) & (R_life <= R_hab_max)

# Plot R evolution
ax5.plot(t_life, R_life, color=colors['eternal'], linewidth=3, label='5D Radius R(t)')

# Highlight habitable zone
if np.any(habitable_mask):
    ax5.fill_between(t_life, R_hab_min, R_hab_max, alpha=0.3, 
                    color=colors['habitable'], label='Habitable Zone')

# Mark key events
life_events = [
    (0.5, 'First Stars', 'star'),
    (4.6, 'Solar System', 'solar'),
    (9, 'Complex Life', 'life'),
    (13.8, 'Today', 'today'),
    (20, 'Far Future', 'future')
]

for t_event, event_name, event_type in life_events:
    if 0 <= t_event <= 30:
        R_event = 1751 * ((t_event + 0.1) / 13.8)**(3/4)
        
        # Color based on habitability
        if R_hab_min <= R_event <= R_hab_max:
            marker_color = colors['habitable']
            viable = '✓'
        else:
            marker_color = colors['heat_death']
            viable = '✗'
        
        ax5.plot(t_event, R_event, 'o', markersize=10, color=marker_color)
        ax5.annotate(f'{event_name}\n{viable} R={R_event:.0f}km', 
                    xy=(t_event, R_event), xytext=(0, 20), 
                    textcoords='offset points', ha='center',
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))

# Add civilizational windows
civ_windows = [
    (10, 15, 'Type I Civilization Window'),
    (15, 25, 'Type II Civilization Window')
]

for t_start, t_end, window_name in civ_windows:
    ax5.axvspan(t_start, t_end, alpha=0.2, color=colors['civilization'])
    ax5.text((t_start + t_end)/2, 2500, window_name, ha='center', va='center',
            bbox=dict(boxstyle='round', facecolor=colors['civilization'], alpha=0.3))

# Add Great Filter annotation
ax5.text(0.7, 0.95, 'Cosmic Great Filter:\nCivilizations must arise during\nR ∈ [1000, 2000] km window\n\nDuration: ~20 Gyr\nWe are at the midpoint!', 
         transform=ax5.transAxes, fontsize=12, fontweight='bold',
         bbox=dict(boxstyle='round,pad=0.5', facecolor='lightyellow', alpha=0.9),
         verticalalignment='top')

ax5.set_title('Panel E: Cosmic Habitability and the Great Filter\nWhen Can Complex Life and Civilizations Exist?', 
              fontweight='bold', fontsize=14)
ax5.set_xlabel('Time (Gyr)')
ax5.set_ylabel('5D Radius R (km)')
ax5.legend(loc='upper left')
ax5.grid(True, alpha=0.3)
ax5.set_xlim(0, 30)
ax5.set_ylim(500, 3000)

# Add horizontal lines for habitable limits
ax5.axhline(R_hab_min, color=colors['habitable'], linestyle='--', alpha=0.7)
ax5.axhline(R_hab_max, color=colors['habitable'], linestyle='--', alpha=0.7)

# Save the figure
figures_dir = 'figures'
os.makedirs(figures_dir, exist_ok=True)

plt.tight_layout()
plt.savefig(f'{figures_dir}/figure_6_paradigm_comparison.png', 
            dpi=300, bbox_inches='tight', facecolor='white')
plt.savefig(f'{figures_dir}/figure_6_paradigm_comparison.pdf', 
            bbox_inches='tight', facecolor='white')

print("Paradigm Comparison diagram created successfully!")
print("Files saved in figures/ directory:")
print("- figure_6_paradigm_comparison.png (300 DPI)")
print("- figure_6_paradigm_comparison.pdf (vector format)")

plt.show()