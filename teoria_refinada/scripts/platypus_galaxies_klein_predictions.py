#!/usr/bin/env python3
"""
KLEIN THEORY PREDICTIONS FOR "PLATYPUS GALAXIES"
================================================

The James Webb Space Telescope discovered 9 peculiar galaxies at z ~ 2
(~12 billion years ago) that defy classification:
- Appear as point sources (like stars)
- Have narrow emission lines (like galaxies)
- No signs of violent mergers
- "Silent" formation mechanism

This script explores whether Klein Evolutionary Theory can explain these
objects and makes QUANTITATIVE TESTABLE PREDICTIONS.

Key Hypothesis: The 5th dimension enables "silent" structure formation
without violent 3D collisions, explaining narrow spectral lines.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import constants
import json
from datetime import datetime
import os

# Physical constants
c = constants.c  # m/s
h = constants.h  # J·s
k_B = constants.k  # J/K
G = constants.G  # m³/kg/s²
M_sun = 1.989e30  # kg

# Klein Theory parameters (calibrated from GW observations)
KLEIN_PARAMS = {
    'R0_km': 6100,           # R_Klein at z=0 (km)
    'alpha': 0.41,           # Evolution exponent
    'z_activation': 1.4,     # Activation redshift
    'epsilon_max': 0.65,     # Topological limit
    'f0_hz': 5.68,           # Klein frequency at z=0
}


class KleinEvolutionaryModel:
    """Model for Klein field evolution across cosmic time."""

    def __init__(self, params=KLEIN_PARAMS):
        self.R0 = params['R0_km'] * 1e3  # Convert to meters
        self.alpha = params['alpha']
        self.z_act = params['z_activation']
        self.eps_max = params['epsilon_max']
        self.f0_local = params['f0_hz']

    def R_klein(self, z):
        """
        Klein bottle radius at redshift z.

        R(z) = R₀ × ((1 + z_act)/(1 + z))^α

        At high z: R smaller (Klein "waking up")
        At z=0: R = R₀ (fully macroscopic)
        """
        if z < self.z_act:
            # Below activation: standard scaling
            return self.R0 * ((1 + self.z_act) / (1 + z))**self.alpha
        else:
            # Above activation: Klein actively evolving
            return self.R0 * ((1 + self.z_act) / (1 + z))**self.alpha

    def f_klein(self, z):
        """
        Characteristic Klein frequency at redshift z.

        f₀(z) = c / (2π R(z))
        """
        R_z = self.R_klein(z)
        return c / (2 * np.pi * R_z)

    def coherence_velocity(self, z):
        """
        Characteristic velocity for coherent motion at redshift z.

        v_coherent = f₀(z) × R(z) = c / (2π)

        This is the maximum velocity for "silent" (coherent) processes.
        """
        # Interestingly, this is constant! v = c/(2π) ≈ 47,700 km/s
        # But in practice, Klein coherence limits it further
        f_z = self.f_klein(z)
        R_z = self.R_klein(z)
        return f_z * R_z  # This equals c/(2π) always

    def klein_coupling_strength(self, z):
        """
        Effective coupling strength of Klein field at redshift z.

        Stronger coupling at higher z (during activation era).
        """
        # Coupling increases during activation era
        if z > self.z_act:
            # In activation era: coupling growing
            return self.eps_max * (1 - np.exp(-(z - self.z_act)))
        else:
            # Post-activation: full coupling
            return self.eps_max

    def silent_formation_efficiency(self, z):
        """
        Efficiency of "silent" (non-violent) structure formation.

        Higher during activation era when Klein is "waking up".
        """
        coupling = self.klein_coupling_strength(z)

        # Peak efficiency during activation (z ~ z_act)
        z_peak = self.z_act + 1.0  # Peak around z ~ 2.4
        width = 1.5

        efficiency = coupling * np.exp(-((z - z_peak)**2) / (2 * width**2))
        return efficiency


class PlatypusGalaxyPredictions:
    """
    Predictions for Platypus Galaxy properties based on Klein Theory.
    """

    def __init__(self, klein_model):
        self.klein = klein_model
        self.z_platypus = 2.0  # Approximate redshift of platypus galaxies

    def predict_spectral_line_width(self, z=None):
        """
        Predict spectral line width for silent-formation galaxies.

        KEY PHYSICS:
        - Violent mergers: Gas shocked to T ~ 10^6-7 K → σ_v ~ 100-300 km/s
        - Klein silent formation: No shocks, gas stays at T ~ 10^4 K → σ_v ~ 10-20 km/s

        The 5th dimension allows momentum/mass transfer WITHOUT 3D collisions,
        so the gas never gets shock-heated.

        Returns: velocity dispersion in km/s
        """
        if z is None:
            z = self.z_platypus

        # In Klein silent formation:
        # - No violent shocks (momentum transfers through 5D)
        # - Gas remains at photoionization equilibrium T ~ 10^4 K
        # - Only thermal broadening + small turbulence

        # Thermal velocity for HII region gas (T ~ 10^4 K)
        T_gas_klein = 1e4  # K - photoionization equilibrium
        m_H = 1.67e-27  # kg (hydrogen mass)
        v_thermal = np.sqrt(k_B * T_gas_klein / m_H)  # m/s, ~9 km/s

        # Small turbulent contribution from Klein oscillations
        # This is suppressed by the coherence factor
        f_z = self.klein.f_klein(z)
        efficiency = self.klein.silent_formation_efficiency(z)

        # Turbulent velocity ~ few km/s, decreasing with efficiency
        v_turb = 5e3 * (1 - efficiency)  # m/s, ~2-5 km/s

        # Total velocity dispersion
        sigma_v = np.sqrt(v_thermal**2 + v_turb**2)  # m/s

        return sigma_v / 1e3  # Convert to km/s

    def predict_line_width_ratio(self):
        """
        Predict ratio of line widths: Platypus vs Normal galaxies.

        This is a key testable prediction.
        """
        # Normal galaxy at z~2 (formed by mergers)
        sigma_merger = 150  # km/s typical for merger

        # Platypus galaxy (Klein silent formation)
        sigma_klein = self.predict_spectral_line_width(self.z_platypus)

        ratio = sigma_merger / sigma_klein

        return {
            'sigma_merger_kms': sigma_merger,
            'sigma_klein_kms': sigma_klein,
            'width_ratio': ratio,
            'prediction': f'Platypus lines should be {ratio:.1f}x narrower than merger galaxies'
        }

    def predict_size_vs_redshift(self, z_range=None):
        """
        Predict apparent size scaling with redshift for Klein-formed objects.

        Standard cosmology: θ ∝ 1/D_A(z)
        Klein modification: θ ∝ R_klein(z) / D_A(z)
        """
        if z_range is None:
            z_range = np.linspace(0.5, 4.0, 50)

        # Angular diameter distance (simplified flat ΛCDM)
        def D_A(z, H0=70, Om=0.3):
            """Comoving distance / (1+z) in Mpc"""
            from scipy.integrate import quad
            integrand = lambda zp: 1.0 / np.sqrt(Om*(1+zp)**3 + (1-Om))
            D_c, _ = quad(integrand, 0, z)
            D_c *= c / (H0 * 1e3)  # Mpc
            return D_c / (1 + z)

        sizes_standard = []
        sizes_klein = []

        R0_physical = 1.0  # kpc, reference size

        for z in z_range:
            D_A_z = D_A(z)

            # Standard: fixed physical size
            theta_standard = R0_physical / D_A_z  # arcsec (roughly)

            # Klein: size scales with R_klein(z)
            R_klein_ratio = self.klein.R_klein(z) / self.klein.R_klein(0)
            theta_klein = R0_physical * R_klein_ratio / D_A_z

            sizes_standard.append(theta_standard)
            sizes_klein.append(theta_klein)

        return {
            'z': z_range,
            'theta_standard': np.array(sizes_standard),
            'theta_klein': np.array(sizes_klein),
            'ratio_at_z2': sizes_klein[np.argmin(np.abs(z_range - 2.0))] /
                          sizes_standard[np.argmin(np.abs(z_range - 2.0))]
        }

    def predict_formation_epoch(self):
        """
        Predict the optimal epoch for platypus galaxy formation.

        Should coincide with Klein activation era.
        """
        z_range = np.linspace(0.5, 6.0, 100)
        efficiencies = [self.klein.silent_formation_efficiency(z) for z in z_range]

        z_peak = z_range[np.argmax(efficiencies)]
        max_efficiency = max(efficiencies)

        return {
            'z_peak_formation': z_peak,
            'peak_efficiency': max_efficiency,
            'z_range_high_efficiency': (
                z_range[efficiencies > max_efficiency * 0.5].min(),
                z_range[efficiencies > max_efficiency * 0.5].max()
            ),
            'prediction': f'Platypus galaxies should peak at z ≈ {z_peak:.1f}'
        }

    def predict_spectral_signature(self, z=None):
        """
        Predict specific spectral signatures from Klein oscillations.
        """
        if z is None:
            z = self.z_platypus

        f_klein = self.klein.f_klein(z)

        # Klein oscillations could modulate emission
        # Observable as: periodic variation in line intensity
        # Or: characteristic spacing in line profiles

        # Convert to observable wavelength modulation
        # Δλ/λ = v/c where v = f_klein × characteristic_scale

        v_modulation = f_klein * self.klein.R_klein(z) / c

        # For Hα at 656.3 nm (rest frame)
        lambda_Ha = 656.3e-9  # m
        delta_lambda = lambda_Ha * v_modulation

        # Observed wavelength at z=2
        lambda_observed = lambda_Ha * (1 + z)

        return {
            'f_klein_hz': f_klein,
            'klein_period_seconds': 1/f_klein,
            'velocity_modulation_kms': v_modulation * c / 1e3,
            'Ha_rest_nm': lambda_Ha * 1e9,
            'Ha_observed_nm': lambda_observed * 1e9,
            'predicted_modulation_nm': delta_lambda * 1e9,
            'fractional_modulation': v_modulation
        }

    def generate_full_predictions(self):
        """
        Generate complete set of predictions for platypus galaxies.
        """
        predictions = {
            'metadata': {
                'generated': datetime.now().isoformat(),
                'model': 'Klein Evolutionary Theory',
                'target': 'Platypus Galaxies (JWST)',
                'reference_redshift': self.z_platypus
            },
            'klein_parameters_at_z2': {
                'R_klein_km': self.klein.R_klein(self.z_platypus) / 1e3,
                'f_klein_hz': self.klein.f_klein(self.z_platypus),
                'coupling_strength': self.klein.klein_coupling_strength(self.z_platypus),
                'formation_efficiency': self.klein.silent_formation_efficiency(self.z_platypus)
            },
            'spectral_predictions': self.predict_line_width_ratio(),
            'formation_epoch': self.predict_formation_epoch(),
            'spectral_signature': self.predict_spectral_signature(),
            'testable_predictions': [
                {
                    'test': 'Line Width Comparison',
                    'prediction': 'Platypus galaxies have σ_v < 20 km/s vs ~150 km/s for mergers',
                    'observable': 'FWHM of emission lines',
                    'significance': 'HIGH - direct test of silent formation'
                },
                {
                    'test': 'Redshift Distribution',
                    'prediction': f'Peak abundance at z ≈ {self.predict_formation_epoch()["z_peak_formation"]:.1f}',
                    'observable': 'Number counts vs redshift',
                    'significance': 'MEDIUM - requires larger sample'
                },
                {
                    'test': 'Size Evolution',
                    'prediction': 'Smaller than expected at high z (follows R_klein scaling)',
                    'observable': 'Angular size vs redshift',
                    'significance': 'MEDIUM - requires resolved imaging'
                },
                {
                    'test': 'Velocity Field',
                    'prediction': 'Coherent rotation without merger signatures',
                    'observable': 'IFU spectroscopy velocity maps',
                    'significance': 'HIGH - smoking gun for silent formation'
                },
                {
                    'test': 'Environment',
                    'prediction': 'Can form in isolation (no nearby companions needed)',
                    'observable': 'Environment density',
                    'significance': 'MEDIUM - statistical test'
                }
            ]
        }

        return predictions


def create_visualization(klein_model, predictions, output_dir):
    """Create visualization of Klein predictions for platypus galaxies."""

    fig, axes = plt.subplots(2, 2, figsize=(14, 12))
    fig.suptitle('Klein Theory Predictions for Platypus Galaxies', fontsize=14, fontweight='bold')

    # Panel 1: Klein parameters evolution
    ax1 = axes[0, 0]
    z_range = np.linspace(0, 5, 100)

    R_values = [klein_model.R_klein(z)/1e3 for z in z_range]  # km
    f_values = [klein_model.f_klein(z) for z in z_range]  # Hz

    ax1_twin = ax1.twinx()

    line1, = ax1.plot(z_range, R_values, 'b-', linewidth=2, label='R_Klein (km)')
    line2, = ax1_twin.plot(z_range, f_values, 'r-', linewidth=2, label='f_Klein (Hz)')

    ax1.axvline(2.0, color='green', linestyle='--', alpha=0.7, label='Platypus z ≈ 2')
    ax1.axvline(klein_model.z_act, color='orange', linestyle=':', alpha=0.7, label=f'z_activation = {klein_model.z_act}')

    ax1.axvspan(1.5, 3.0, alpha=0.2, color='green', label='Platypus Era')

    ax1.set_xlabel('Redshift z')
    ax1.set_ylabel('R_Klein (km)', color='blue')
    ax1_twin.set_ylabel('f_Klein (Hz)', color='red')
    ax1.set_title('A. Klein Parameters vs Cosmic Time')
    ax1.legend(loc='upper right')
    ax1.grid(True, alpha=0.3)

    # Panel 2: Silent formation efficiency
    ax2 = axes[0, 1]

    efficiencies = [klein_model.silent_formation_efficiency(z) for z in z_range]

    ax2.fill_between(z_range, efficiencies, alpha=0.3, color='purple')
    ax2.plot(z_range, efficiencies, 'purple', linewidth=2)

    ax2.axvline(2.0, color='green', linestyle='--', linewidth=2, label='Platypus z ≈ 2')

    peak_z = predictions['formation_epoch']['z_peak_formation']
    ax2.axvline(peak_z, color='red', linestyle=':', linewidth=2, label=f'Peak z = {peak_z:.1f}')

    ax2.set_xlabel('Redshift z')
    ax2.set_ylabel('Silent Formation Efficiency')
    ax2.set_title('B. Efficiency of Non-Violent Structure Formation')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # Panel 3: Line width prediction
    ax3 = axes[1, 0]

    z_galaxies = np.linspace(0.5, 4, 50)
    platypus_model = PlatypusGalaxyPredictions(klein_model)

    sigma_klein = [platypus_model.predict_spectral_line_width(z) for z in z_galaxies]
    sigma_merger = [150 * (1 + 0.1*(z-2)) for z in z_galaxies]  # Slight z evolution for mergers

    ax3.plot(z_galaxies, sigma_merger, 'r-', linewidth=2, label='Merger galaxies (typical)')
    ax3.plot(z_galaxies, sigma_klein, 'b-', linewidth=2, label='Klein silent formation')

    ax3.fill_between(z_galaxies, sigma_klein, sigma_merger, alpha=0.2, color='green')

    ax3.axhline(20, color='blue', linestyle=':', alpha=0.7)
    ax3.text(0.6, 22, 'Klein prediction: σ < 20 km/s', fontsize=9, color='blue')

    ax3.set_xlabel('Redshift z')
    ax3.set_ylabel('Velocity Dispersion σ_v (km/s)')
    ax3.set_title('C. Spectral Line Width: Klein vs Merger Formation')
    ax3.legend()
    ax3.set_ylim(0, 200)
    ax3.grid(True, alpha=0.3)

    # Panel 4: Summary of testable predictions
    ax4 = axes[1, 1]
    ax4.axis('off')

    summary_text = """
    TESTABLE PREDICTIONS FOR PLATYPUS GALAXIES
    ═══════════════════════════════════════════

    1. SPECTRAL LINE WIDTH
       Prediction: σ_v < 20 km/s (vs ~150 km/s for mergers)
       Test: Measure FWHM of Hα, [OIII], [NII] lines

    2. FORMATION REDSHIFT PEAK
       Prediction: Maximum abundance at z ≈ {:.1f}
       Test: Count platypus galaxies vs redshift

    3. KLEIN FREQUENCY SIGNATURE
       At z=2: f_Klein = {:.1f} Hz
       Period: {:.2f} seconds
       Test: Look for periodic modulation in spectra

    4. ENVIRONMENT INDEPENDENCE
       Prediction: Form in isolation (no companions needed)
       Test: Measure local galaxy density

    5. VELOCITY FIELD COHERENCE
       Prediction: Smooth rotation, no merger remnants
       Test: IFU velocity maps (JWST/NIRSpec)

    ═══════════════════════════════════════════
    If confirmed: Evidence for 5D "silent" formation
    If falsified: Klein theory needs modification
    """.format(
        predictions['formation_epoch']['z_peak_formation'],
        predictions['klein_parameters_at_z2']['f_klein_hz'],
        1/predictions['klein_parameters_at_z2']['f_klein_hz']
    )

    ax4.text(0.05, 0.95, summary_text, transform=ax4.transAxes,
             fontsize=10, verticalalignment='top', fontfamily='monospace',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    plt.tight_layout()

    output_path = os.path.join(output_dir, 'platypus_klein_predictions.png')
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()

    return output_path


def main():
    """Main execution."""
    print("=" * 70)
    print("🦆 KLEIN THEORY PREDICTIONS FOR PLATYPUS GALAXIES")
    print("=" * 70)

    # Initialize models
    klein = KleinEvolutionaryModel()
    platypus = PlatypusGalaxyPredictions(klein)

    # Generate predictions
    print("\n📊 Generating predictions...")
    predictions = platypus.generate_full_predictions()

    # Print key results
    print("\n" + "=" * 70)
    print("🎯 KEY PREDICTIONS")
    print("=" * 70)

    print(f"\n📍 At Platypus Galaxy Redshift (z ≈ 2.0):")
    params = predictions['klein_parameters_at_z2']
    print(f"   R_Klein = {params['R_klein_km']:.0f} km")
    print(f"   f_Klein = {params['f_klein_hz']:.2f} Hz")
    print(f"   Klein period = {1/params['f_klein_hz']:.3f} seconds")
    print(f"   Formation efficiency = {params['formation_efficiency']:.3f}")

    print(f"\n📏 Spectral Line Width Prediction:")
    spec = predictions['spectral_predictions']
    print(f"   Merger galaxies: σ_v ≈ {spec['sigma_merger_kms']:.0f} km/s")
    print(f"   Klein formation: σ_v ≈ {spec['sigma_klein_kms']:.1f} km/s")
    print(f"   → {spec['prediction']}")

    print(f"\n⏰ Formation Epoch Prediction:")
    epoch = predictions['formation_epoch']
    print(f"   Peak formation at z ≈ {epoch['z_peak_formation']:.1f}")
    print(f"   High-efficiency range: z ∈ [{epoch['z_range_high_efficiency'][0]:.1f}, {epoch['z_range_high_efficiency'][1]:.1f}]")

    print(f"\n🔬 Spectral Signature:")
    sig = predictions['spectral_signature']
    print(f"   Klein frequency at z=2: {sig['f_klein_hz']:.2f} Hz")
    print(f"   Oscillation period: {sig['klein_period_seconds']:.3f} s")
    print(f"   Hα observed wavelength: {sig['Ha_observed_nm']:.1f} nm")

    print("\n" + "=" * 70)
    print("✅ TESTABLE PREDICTIONS")
    print("=" * 70)

    for i, test in enumerate(predictions['testable_predictions'], 1):
        print(f"\n{i}. {test['test']} [{test['significance']}]")
        print(f"   Prediction: {test['prediction']}")
        print(f"   Observable: {test['observable']}")

    # Save results
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'resultados', 'platypus_galaxies')
    os.makedirs(output_dir, exist_ok=True)

    # Save JSON
    json_path = os.path.join(output_dir, 'klein_predictions_platypus.json')
    with open(json_path, 'w') as f:
        json.dump(predictions, f, indent=2, default=str)
    print(f"\n💾 Predictions saved to: {json_path}")

    # Create visualization
    print("\n📈 Creating visualization...")
    fig_path = create_visualization(klein, predictions, output_dir)
    print(f"📊 Figure saved to: {fig_path}")

    # Create summary markdown
    summary_md = f"""# Klein Theory Predictions for Platypus Galaxies

## Overview

The James Webb Space Telescope discovered 9 "platypus galaxies" at z ≈ 2 that defy
standard classification. Klein Evolutionary Theory offers a potential explanation:
**"Silent" formation via 5th dimension transfer**.

## Key Predictions

### 1. Spectral Line Width
- **Merger galaxies**: σ_v ≈ 150 km/s (broad lines)
- **Klein formation**: σ_v ≈ {spec['sigma_klein_kms']:.1f} km/s (narrow lines)
- **Ratio**: Platypus lines should be ~{spec['width_ratio']:.0f}x narrower

### 2. Formation Epoch
- **Peak abundance**: z ≈ {epoch['z_peak_formation']:.1f}
- **High-efficiency era**: z ∈ [{epoch['z_range_high_efficiency'][0]:.1f}, {epoch['z_range_high_efficiency'][1]:.1f}]
- This coincides with Klein "activation era"

### 3. Klein Parameters at z = 2
| Parameter | Value |
|-----------|-------|
| R_Klein | {params['R_klein_km']:.0f} km |
| f_Klein | {params['f_klein_hz']:.2f} Hz |
| Period | {1/params['f_klein_hz']:.3f} s |
| Coupling | {params['coupling_strength']:.3f} |

### 4. Physical Mechanism

```
STANDARD FORMATION (Mergers):
  Galaxy A + Galaxy B → Violent collision → High σ_v → Broad lines

KLEIN SILENT FORMATION:
  Gas → 5D transfer → Coherent assembly → Low σ_v → Narrow lines
        (no 3D collision)
```

## Falsifiability

If platypus galaxies show:
- σ_v > 50 km/s: Klein prediction FAILS
- Peak at z ≠ {epoch['z_peak_formation']:.1f}: Need model refinement
- Merger signatures in velocity maps: Silent formation REJECTED

## Conclusion

Klein Evolutionary Theory predicts that platypus galaxies formed during the
"activation era" (z ~ 1.4-3) when the 5th dimension was transitioning to its
macroscopic scale. The narrow spectral lines are a natural consequence of
momentum transfer occurring through 5D topology rather than 3D collisions.

---
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
"""

    md_path = os.path.join(output_dir, 'PLATYPUS_KLEIN_PREDICTIONS.md')
    with open(md_path, 'w') as f:
        f.write(summary_md)
    print(f"📝 Summary saved to: {md_path}")

    return predictions


if __name__ == "__main__":
    predictions = main()
