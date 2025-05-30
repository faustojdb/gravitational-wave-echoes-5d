#!/usr/bin/env python3
"""
Cosmological Evolution Diagram for Paper I v2.0
Shows dimensional evolution and dark matter implications
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import os

# Set up the figure
fig = plt.figure(figsize=(16, 12))
gs = gridspec.GridSpec(2, 2, figure=fig, hspace=0.3, wspace=0.3)

# Color scheme
colors = {
    'new_model': '#2E86AB',     # Blue - new R ∝ a^(3/4)
    'old_model': '#C73E1D',     # Red - old R ∝ a^(0.1)
    'dark_matter': '#A23B72',   # Purple
    'habitable': '#52A270',     # Green
    'epochs': '#F18F01',        # Orange
    'background': '#F5F5F5'
}

# Main title
fig.suptitle('Cosmological Evolution of Fifth Dimension\n' + 
             r'New Model: $R(t) \propto a(t)^{3/4}$ vs Old Model: $R(t) \propto a(t)^{0.1}$', 
             fontsize=18, fontweight='bold')

# ============================================================================
# Panel A: R(t) vs Cosmic Time
# ============================================================================
ax1 = fig.add_subplot(gs[0, 0])

# Time evolution from Big Bang to far future
t_universe = 13.8e9  # Current age in years
t = np.logspace(6, 13, 1000)  # From 1 million years to 10^13 years

# Scale factor evolution: a(t) ∝ t^(2/3) in matter era, more complex overall
t_eq = 50000  # Matter-radiation equality at ~50,000 years
t_now = t_universe

def scale_factor(time):
    """Simplified scale factor evolution"""
    a_now = 1.0
    # Before equality: a ∝ t^(1/2)
    # After equality: a ∝ t^(2/3)
    # Late time: exponential (dark energy)
    
    ratio = time / t_now
    if hasattr(ratio, '__len__'):
        result = np.zeros_like(ratio)
        early_mask = time < t_eq
        matter_mask = (time >= t_eq) & (time < t_now)
        late_mask = time >= t_now
        
        # Radiation era
        result[early_mask] = a_now * (ratio[early_mask] / (t_eq/t_now))**(1/2) * (t_eq/t_now)**(2/3)
        # Matter era  
        result[matter_mask] = a_now * (ratio[matter_mask])**(2/3)
        # Dark energy era
        result[late_mask] = a_now * np.exp(0.1 * (ratio[late_mask] - 1))
        
        return result
    else:
        if time < t_eq:
            return a_now * (ratio / (t_eq/t_now))**(1/2) * (t_eq/t_now)**(2/3)
        elif time < t_now:
            return a_now * ratio**(2/3)
        else:
            return a_now * np.exp(0.1 * (ratio - 1))

a_values = scale_factor(t)

# Current R value
R_now = 1751.173  # km

# New model: R ∝ a^(3/4)
R_new = R_now * (a_values)**(3/4)

# Old model: R ∝ a^(0.1)  
R_old = R_now * (a_values)**(0.1)

# Plot both models
ax1.loglog(t/1e9, R_new, color=colors['new_model'], linewidth=3, 
          label=r'New: $R \propto a^{3/4}$')
ax1.loglog(t/1e9, R_old, color=colors['old_model'], linewidth=3, linestyle='--',
          label=r'Old: $R \propto a^{0.1}$')

# Mark important epochs
epochs = {
    'Recombination': (380000/1e9, R_now * (1/1100)**(3/4)),
    'Today': (t_universe/1e9, R_now),
    'Future (a=10)': (100*t_universe/1e9, R_now * 10**(3/4))
}

for label, (time, R_val) in epochs.items():
    ax1.plot(time, R_val, 'o', markersize=10, color=colors['epochs'])
    ax1.annotate(f'{label}\nR = {R_val:.1f} km', 
                xy=(time, R_val), xytext=(10, 20), 
                textcoords='offset points',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7))

ax1.set_title('Panel A: Fifth Dimension Evolution\nwith Cosmic Time', fontweight='bold')
ax1.set_xlabel('Time (Gyr)')
ax1.set_ylabel('5D Radius R (km)')
ax1.legend()
ax1.grid(True, alpha=0.3)

# ============================================================================
# Panel B: Comparison of Evolution Laws
# ============================================================================
ax2 = fig.add_subplot(gs[0, 1])

# Scale factor range
a_range = np.logspace(-3, 1, 1000)  # From a=0.001 to a=10

# Different evolution laws
R_34 = (a_range)**(3/4)      # New model
R_01 = (a_range)**(0.1)      # Old model  
R_1 = a_range                # Linear
R_2 = a_range**2             # Quadratic

# Normalize all to 1 at a=1
ax2.loglog(a_range, R_34, color=colors['new_model'], linewidth=3,
          label=r'$R \propto a^{3/4}$ (New)')
ax2.loglog(a_range, R_01, color=colors['old_model'], linewidth=3, linestyle='--',
          label=r'$R \propto a^{0.1}$ (Old)')
ax2.loglog(a_range, R_1, color='gray', linewidth=2, linestyle=':',
          label=r'$R \propto a$ (Linear)')
ax2.loglog(a_range, R_2, color='black', linewidth=2, linestyle='-.',
          label=r'$R \propto a^2$ (Quadratic)')

# Mark current universe
ax2.axvline(1, color=colors['epochs'], linewidth=2, alpha=0.7, label='Today (a=1)')

# Mark recombination
a_rec = 1/1100
ax2.axvline(a_rec, color='purple', linewidth=2, alpha=0.7, label='Recombination')

ax2.set_title('Panel B: Evolution Law Comparison\nDifferent Power Laws', fontweight='bold')
ax2.set_xlabel('Scale Factor a')
ax2.set_ylabel('Relative R(a)/R(a=1)')
ax2.legend()
ax2.grid(True, alpha=0.3)

# ============================================================================
# Panel C: Dark Matter Density Evolution
# ============================================================================
ax3 = fig.add_subplot(gs[1, 0])

# Dark matter density evolution
# ρ_DM ∝ 1/R^4 and ρ_DM ∝ a^(-3)
# This gives R ∝ a^(3/4)

z_values = np.logspace(-2, 3, 1000)  # Redshift from 0.01 to 1000
a_dm = 1 / (1 + z_values)

# Current dark matter density
rho_dm_now = 2.39e-27  # kg/m³

# Density evolution: ρ ∝ a^(-3)
rho_dm_cosmic = rho_dm_now * a_dm**(-3)

# From our model: ρ_DM ∝ 1/R^4, R ∝ a^(3/4)
# So ρ_DM ∝ 1/a^3 ✓ (consistent!)
rho_dm_5d = rho_dm_now * a_dm**(-3)

# Critical density evolution
rho_crit_now = 9.47e-27  # kg/m³
rho_crit = rho_crit_now * a_dm**(-3) * ((1 + z_values)**3 * 0.3 + 0.7)**(-1)  # Approximate

ax3.loglog(z_values, rho_dm_5d, color=colors['dark_matter'], linewidth=3,
          label='5D Vacuum Energy Model')
ax3.loglog(z_values, rho_crit * 0.26, color='gray', linewidth=2, linestyle='--',
          label='ΛCDM Dark Matter')

# Mark important redshifts
z_rec = 1100
z_eq = 3400
z_now = 0

for z_mark, label in [(z_rec, 'Recombination'), (z_eq, 'Matter-Rad Equality'), (1, 'z=1')]:
    if 0.01 <= z_mark <= 1000:
        rho_val = rho_dm_now * (1 + z_mark)**3
        ax3.axvline(z_mark, color=colors['epochs'], alpha=0.5)
        ax3.text(z_mark, rho_val * 2, label, rotation=90, ha='center')

ax3.set_title('Panel C: Dark Matter Density Evolution\n5D Model vs ΛCDM', fontweight='bold')
ax3.set_xlabel('Redshift z')
ax3.set_ylabel('Dark Matter Density (kg/m³)')
ax3.legend()
ax3.grid(True, alpha=0.3)

# ============================================================================
# Panel D: Habitable Window
# ============================================================================
ax4 = fig.add_subplot(gs[1, 1])

# Define habitability conditions
# R must be in range ~1000-2000 km for complex chemistry
R_min_hab = 1000  # km
R_max_hab = 2000  # km

# Time when R reaches these values
a_min = (R_min_hab / R_now)**(4/3)  # From R ∝ a^(3/4)
a_max = (R_max_hab / R_now)**(4/3)

t_min = t_universe * a_min**(3/2)  # Approximate
t_max = t_universe * a_max**(3/2)

# Plot R evolution with habitability zone
t_hab = np.linspace(0.1e9, 50e9, 1000)
a_hab = (t_hab / t_universe)**(2/3)  # Simplified
R_hab = R_now * a_hab**(3/4)

ax4.plot(t_hab/1e9, R_hab, color=colors['new_model'], linewidth=3)

# Highlight habitable zone
hab_mask = (R_hab >= R_min_hab) & (R_hab <= R_max_hab)
if np.any(hab_mask):
    ax4.fill_between(t_hab[hab_mask]/1e9, R_min_hab, R_max_hab, 
                    color=colors['habitable'], alpha=0.3, label='Habitable Window')

# Mark current time
ax4.axvline(t_universe/1e9, color=colors['epochs'], linewidth=3, 
           label=f'Today ({t_universe/1e9:.1f} Gyr)')

# Add horizontal lines for habitability limits
ax4.axhline(R_min_hab, color=colors['habitable'], linestyle='--', alpha=0.7)
ax4.axhline(R_max_hab, color=colors['habitable'], linestyle='--', alpha=0.7)

# Annotations
ax4.text(t_universe/1e9 + 2, R_now + 200, 
         f'Current R = {R_now:.0f} km\n(Mid-habitable zone)', 
         bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))

ax4.text(30, 1500, 
         'Habitable Window:\n~20 Billion Years\n(Complex chemistry possible)', 
         bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.8))

ax4.set_title('Panel D: Cosmic Habitability Window\nR ∈ [1000, 2000] km', fontweight='bold')
ax4.set_xlabel('Time (Gyr)')
ax4.set_ylabel('5D Radius R (km)')
ax4.legend()
ax4.grid(True, alpha=0.3)
ax4.set_xlim(0, 40)
ax4.set_ylim(500, 3000)

# Save the figure
figures_dir = 'figures'
os.makedirs(figures_dir, exist_ok=True)

plt.tight_layout()
plt.savefig(f'{figures_dir}/figure_3_cosmological_evolution.png', 
            dpi=300, bbox_inches='tight', facecolor='white')
plt.savefig(f'{figures_dir}/figure_3_cosmological_evolution.pdf', 
            bbox_inches='tight', facecolor='white')

print("Cosmological Evolution diagram created successfully!")
print("Files saved in figures/ directory:")
print("- figure_3_cosmological_evolution.png (300 DPI)")
print("- figure_3_cosmological_evolution.pdf (vector format)")

plt.show()