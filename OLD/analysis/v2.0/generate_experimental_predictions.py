#!/usr/bin/env python3
"""
Experimental Predictions Diagram for Paper I v2.0
Shows testable predictions across multiple experiments
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as patches
from matplotlib.patches import Rectangle, Circle
import os

# Set up the figure
fig = plt.figure(figsize=(18, 12))
gs = gridspec.GridSpec(2, 2, figure=fig, hspace=0.3, wspace=0.3)

# Color scheme
colors = {
    'ligo': '#3498DB',          # Blue
    'resonator': '#E74C3C',     # Red
    'atomic': '#2ECC71',        # Green
    'cosmology': '#9B59B6',     # Purple
    'prediction': '#F39C12',    # Orange
    'confirmed': '#27AE60',     # Dark green
    'future': '#95A5A6'         # Gray
}

# Main title
fig.suptitle('Experimental Predictions and Tests\n' + 
             r'Multiple Independent Verifications of Klein Bottle Theory', 
             fontsize=18, fontweight='bold')

# ============================================================================
# Panel A: LIGO/Virgo Future Predictions (O4-O5)
# ============================================================================
ax1 = fig.add_subplot(gs[0, 0])

# Mode spectrum data
modes = np.array([1, 2, 3, 4, 5, 6, 7, 8])
frequencies = 42 * modes  # ω_n = n × ω_0 (rad/s)
tau_values = 2 * np.pi / frequencies  # τ_n = 2π/ω_n
amplitudes = np.where(modes % 2 == 1, 1.0/modes, 0)  # Only odd modes

# Expected detection sensitivity for O4-O5
sensitivity_improvement = 2.0  # 2x better than O3
current_snr_threshold = 4.5
expected_detections = amplitudes > (current_snr_threshold / (sensitivity_improvement * 10))

# Create bar chart
bars = ax1.bar(modes, amplitudes, 
              color=[colors['confirmed'] if modes[i] == 1 
                    else colors['prediction'] if modes[i] % 2 == 1 
                    else colors['future'] for i in range(len(modes))])

# Add detection predictions
for i, (mode, amp, detect) in enumerate(zip(modes, amplitudes, expected_detections)):
    if mode % 2 == 1:  # Only odd modes
        if mode == 1:
            status = "DETECTED"
            color = 'green'
        elif detect:
            status = "DETECTABLE"
            color = 'orange'
        else:
            status = "CHALLENGING"
            color = 'red'
        
        ax1.text(mode, amp + 0.05, f'{frequencies[i]} rad/s\n{status}', 
                ha='center', va='bottom', fontsize=8, color=color, fontweight='bold')
    else:
        ax1.text(mode, 0.05, 'FORBIDDEN', ha='center', va='bottom', 
                color='red', fontsize=9, fontweight='bold')

# Add annotations
ax1.text(0.5, 0.8, 'Klein Bottle Signature:\nOnly odd modes allowed', 
         transform=ax1.transAxes, fontsize=12, fontweight='bold',
         bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.8))

ax1.set_title('Panel A: LIGO/Virgo O4-O5 Predictions\n(2023-2025)', fontweight='bold')
ax1.set_xlabel('Mode Number n')
ax1.set_ylabel('Relative Amplitude')
ax1.set_ylim(0, 1.2)
ax1.grid(True, alpha=0.3)

# Add legend
from matplotlib.lines import Line2D
legend_elements = [
    Line2D([0], [0], color=colors['confirmed'], lw=4, label='Detected (n=1)'),
    Line2D([0], [0], color=colors['prediction'], lw=4, label='Predicted (odd)'),
    Line2D([0], [0], color=colors['future'], lw=4, label='Forbidden (even)')
]
ax1.legend(handles=legend_elements, loc='upper right')

# ============================================================================
# Panel B: Klein Mechanical Resonator
# ============================================================================
ax2 = fig.add_subplot(gs[0, 1])

# Resonator design schematic
theta = np.linspace(0, 2*np.pi, 100)

# Toroidal resonator (approximates Klein bottle)
R_major = 0.4
R_minor = 0.15
resonator_x = R_major * np.cos(theta)
resonator_y = R_major * np.sin(theta)

# Draw resonator
ax2.plot(resonator_x, resonator_y, color=colors['resonator'], linewidth=4)

# Add inner structure
inner_theta = np.linspace(0, 2*np.pi, 50)
for i in range(8):
    angle = i * np.pi / 4
    center_x = 0.25 * np.cos(angle)
    center_y = 0.25 * np.sin(angle)
    inner_x = center_x + 0.08 * np.cos(inner_theta)
    inner_y = center_y + 0.08 * np.sin(inner_theta)
    ax2.plot(inner_x, inner_y, color=colors['resonator'], linewidth=1, alpha=0.5)

# Add vibration pattern (fundamental mode)
vibration_amplitude = 0.05
vibration_pattern = vibration_amplitude * np.sin(theta)  # n=1 mode
vib_x = (R_major + vibration_pattern) * np.cos(theta)
vib_y = (R_major + vibration_pattern) * np.sin(theta)
ax2.plot(vib_x, vib_y, color=colors['prediction'], linewidth=2, linestyle='--')

# Add specifications
specs_text = """SPECIFICATIONS:
• Frequency: f₀ = 6.68 Hz
• Quality Factor: Q > 10⁸
• Mass: ~1000 kg
• Temperature: <10 mK
• Material: Ultra-low loss

EXPECTED SIGNAL:
• Coherent excitation during GW events
• Amplitude: ~10⁻¹⁸ m
• Detection: SQUID magnetometry"""

ax2.text(0.6, 0.7, specs_text, transform=ax2.transAxes, fontsize=10,
         bbox=dict(boxstyle='round,pad=0.5', facecolor='lightcyan', alpha=0.9),
         verticalalignment='top')

# Add arrows showing excitation
for angle in [0, np.pi/2, np.pi, 3*np.pi/2]:
    x_start = 0.5 * np.cos(angle)
    y_start = 0.5 * np.sin(angle)
    x_end = 0.45 * np.cos(angle)
    y_end = 0.45 * np.sin(angle)
    ax2.arrow(x_start, y_start, x_end - x_start, y_end - y_start,
             head_width=0.03, head_length=0.02, fc=colors['prediction'], 
             ec=colors['prediction'], alpha=0.7)

ax2.set_title('Panel B: Klein Mechanical Resonator\nTerrestrial Detection', fontweight='bold')
ax2.set_aspect('equal')
ax2.set_xlim(-0.7, 0.7)
ax2.set_ylim(-0.7, 0.7)
ax2.axis('off')

# ============================================================================
# Panel C: Atomic Clock Network
# ============================================================================
ax3 = fig.add_subplot(gs[1, 0])

# Simulated atomic clock data showing 42 rad/s oscillation
t_clock = np.linspace(0, 1, 1000)  # 1 second of data
omega_0 = 42  # rad/s

# Expected fractional frequency shift
alpha_5d = 1e-18  # Coupling strength
delta_nu_nu = alpha_5d * np.sin(omega_0 * t_clock)

# Add realistic noise
np.random.seed(123)
noise_level = 5e-19
noise = noise_level * np.random.normal(0, 1, len(t_clock))
observed_signal = delta_nu_nu + noise

# Plot the signal
ax3.plot(t_clock, observed_signal * 1e18, color=colors['atomic'], linewidth=2, alpha=0.7)
ax3.plot(t_clock, delta_nu_nu * 1e18, color=colors['prediction'], linewidth=3,
         label=f'Prediction: α₅ᴅ sin(42t)')

# Add detection threshold
threshold = 3 * noise_level * 1e18
ax3.axhline(threshold, color='red', linestyle='--', alpha=0.7, label='3σ threshold')
ax3.axhline(-threshold, color='red', linestyle='--', alpha=0.7)

# Add correlation analysis window
correlation_window = [0.7, 0.9]
ax3.axvspan(correlation_window[0], correlation_window[1], alpha=0.2, 
           color=colors['prediction'], label='Analysis window')

# Add clock locations (global network)
clock_locations = ['NIST (USA)', 'PTB (Germany)', 'RIKEN (Japan)', 'NPL (UK)']
colors_clocks = ['red', 'blue', 'green', 'orange']

for i, (location, color) in enumerate(zip(clock_locations, colors_clocks)):
    # Simulate slightly different phases for different locations
    phase_shift = i * np.pi / 4
    local_signal = alpha_5d * np.sin(omega_0 * t_clock + phase_shift)
    ax3.plot(t_clock[::50], local_signal[::50] * 1e18, 'o', color=color, 
            markersize=4, alpha=0.7, label=location)

ax3.set_title('Panel C: Atomic Clock Network\nGlobal Frequency Correlations', fontweight='bold')
ax3.set_xlabel('Time (s)')
ax3.set_ylabel('Fractional Frequency Shift (×10⁻¹⁸)')
ax3.legend(loc='upper right', fontsize=9)
ax3.grid(True, alpha=0.3)

# Add inset showing power spectrum
ax3_inset = ax3.inset_axes([0.15, 0.15, 0.3, 0.3])
freqs_fft = np.fft.fftfreq(len(t_clock), t_clock[1] - t_clock[0]) * 2 * np.pi
power_spectrum = np.abs(np.fft.fft(delta_nu_nu))**2
positive_freqs = freqs_fft > 0
ax3_inset.semilogy(freqs_fft[positive_freqs], power_spectrum[positive_freqs], 
                  color=colors['prediction'])
ax3_inset.axvline(42, color='red', linestyle='--', label='42 rad/s')
ax3_inset.set_xlabel('Freq (rad/s)', fontsize=8)
ax3_inset.set_ylabel('Power', fontsize=8)
ax3_inset.set_title('Power Spectrum', fontsize=9)
ax3_inset.grid(True, alpha=0.3)

# ============================================================================
# Panel D: Cosmological Signatures
# ============================================================================
ax4 = fig.add_subplot(gs[1, 1])

# Create timeline of cosmological observations
experiments = [
    ('LiteBIRD', 2028, 'CMB Polarization'),
    ('CMB-S4', 2030, 'Primordial B-modes'),
    ('Roman Space Telescope', 2027, 'BAO Oscillations'),
    ('Euclid', 2024, 'Galaxy Clustering'),
    ('SKA', 2030, 'Dark Age 21cm')
]

years = [exp[1] for exp in experiments]
names = [exp[0] for exp in experiments]
types = [exp[2] for exp in experiments]

# Plot timeline
current_year = 2024
future_years = np.array(years)
y_positions = np.arange(len(experiments))

# Create horizontal timeline
for i, (name, year, obs_type) in enumerate(experiments):
    color = colors['confirmed'] if year <= current_year else colors['future']
    
    # Timeline bar
    ax4.barh(i, year - current_year, left=current_year, height=0.6, 
            color=color, alpha=0.7, edgecolor='black')
    
    # Add experiment name
    ax4.text(current_year - 0.5, i, name, ha='right', va='center', 
            fontweight='bold', fontsize=10)
    
    # Add observation type
    ax4.text(year + 0.5, i, obs_type, ha='left', va='center', 
            fontsize=9, style='italic')

# Add predictions for each experiment
predictions = [
    'Power spectrum oscillations\nwith period 2π/R(z)',
    'Hemispheric correlations\nfrom Klein topology',
    'Modified BAO scale\nR(z) dependence',
    'Non-Gaussian signatures\nin large-scale structure',
    '21cm fluctuations\nfrom early Klein state'
]

for i, prediction in enumerate(predictions):
    ax4.text(2035, i, prediction, ha='left', va='center', fontsize=8,
            bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.6))

# Add current time marker
ax4.axvline(current_year, color='red', linewidth=3, alpha=0.7, label='Now (2024)')

ax4.set_title('Panel D: Cosmological Predictions\nNext Decade Observations', fontweight='bold')
ax4.set_xlabel('Year')
ax4.set_yticks(y_positions)
ax4.set_yticklabels([])
ax4.set_xlim(2022, 2040)
ax4.grid(True, alpha=0.3, axis='x')

# Add legend for timeline
legend_elements = [
    Line2D([0], [0], color=colors['confirmed'], lw=8, label='Operating'),
    Line2D([0], [0], color=colors['future'], lw=8, label='Future'),
    Line2D([0], [0], color='red', lw=3, label='Current Year')
]
ax4.legend(handles=legend_elements, loc='upper left')

# Save the figure
figures_dir = 'figures'
os.makedirs(figures_dir, exist_ok=True)

plt.tight_layout()
plt.savefig(f'{figures_dir}/figure_5_experimental_predictions.png', 
            dpi=300, bbox_inches='tight', facecolor='white')
plt.savefig(f'{figures_dir}/figure_5_experimental_predictions.pdf', 
            bbox_inches='tight', facecolor='white')

print("Experimental Predictions diagram created successfully!")
print("Files saved in figures/ directory:")
print("- figure_5_experimental_predictions.png (300 DPI)")
print("- figure_5_experimental_predictions.pdf (vector format)")

plt.show()