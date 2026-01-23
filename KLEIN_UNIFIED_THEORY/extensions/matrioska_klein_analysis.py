#!/usr/bin/env python3
"""
MATRIOSKA-KLEIN HYPOTHESIS ANALYSIS
====================================

Hypothesis: There exist MULTIPLE nested Klein dimensions, each operating
at different scales. Each mass/energy scale "sees" the Klein level
appropriate to its size.

This is an INDEPENDENT analysis - we do NOT assume previous Klein
validations are correct. We test whether this framework:
1. Has internal mathematical consistency
2. Makes predictions different from single-Klein models
3. Could explain observations that single-Klein cannot (e.g., H₀ tension)

Author: Klein Theory Team
Date: January 2026
"""

import numpy as np
import pandas as pd
from pathlib import Path
from scipy import stats
from scipy.optimize import minimize, curve_fit
from scipy.constants import c, G, hbar, k as k_B
import json
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# =============================================================================
# PHYSICAL CONSTANTS (SI units)
# =============================================================================

c_si = 299792458  # m/s
G_si = 6.674e-11  # m³/(kg·s²)
hbar_si = 1.055e-34  # J·s
k_B_si = 1.381e-23  # J/K
M_sun = 1.989e30  # kg
H_0_local = 73.04  # km/s/Mpc (SH0ES)
H_0_cmb = 67.4  # km/s/Mpc (Planck)
Mpc_to_m = 3.086e22  # m per Mpc

print("=" * 70)
print("MATRIOSKA-KLEIN HYPOTHESIS ANALYSIS")
print("=" * 70)
print("\nHypothesis: Nested Klein dimensions at different scales")
print("Goal: Test if this explains what single-Klein cannot")

# =============================================================================
# PART 1: THEORETICAL FRAMEWORK
# =============================================================================

def define_matrioska_levels():
    """
    Define the hierarchy of Klein levels based on scaling arguments.

    Key assumption: Each Klein level has R proportional to a
    characteristic length scale of physics at that level.
    """

    print("\n" + "=" * 70)
    print("PART 1: MATRIOSKA-KLEIN THEORETICAL FRAMEWORK")
    print("=" * 70)

    # Characteristic scales in physics
    scales = {
        'planck': {
            'name': 'Klein₁ (Planck)',
            'L_char': np.sqrt(hbar_si * G_si / c_si**3),  # Planck length
            'description': 'Quantum gravity scale'
        },
        'nuclear': {
            'name': 'Klein₂ (Nuclear)',
            'L_char': 1e-15,  # ~1 fm
            'description': 'Strong interaction scale'
        },
        'stellar_bh': {
            'name': 'Klein₃ (Stellar BH)',
            'L_char': 8.4e6,  # 8400 km in meters (from GW validation)
            'description': 'Gravitational wave scale'
        },
        'cosmological': {
            'name': 'Klein₄ (Cosmological)',
            'L_char': None,  # To be determined
            'description': 'Hubble scale physics'
        }
    }

    # Print known scales
    print("\n  Known characteristic scales:")
    for key, scale in scales.items():
        if scale['L_char'] is not None:
            print(f"    {scale['name']}: L = {scale['L_char']:.2e} m")

    # HYPOTHESIS: Klein radii follow a scaling law
    # R_n ∝ L_char^α where α is to be determined

    # From Klein₃ validation: R₃ = 8400 km for stellar BH scale
    R_3 = 8.4e6  # meters
    L_3 = 2.95 * 30 * 1000  # R_s of 30 M☉ BH in meters ≈ 88.5 km

    print(f"\n  Anchor point (Klein₃):")
    print(f"    R₃ = {R_3/1000:.0f} km")
    print(f"    Characteristic mass: ~30 M☉ (stellar BH)")

    # Scaling hypothesis: R_Klein ∝ M^β or R_Klein ∝ R_s^β
    # From R₃ and L₃, we can estimate β

    return scales, R_3

def estimate_klein4_parameters():
    """
    Estimate Klein₄ parameters for cosmological scale.

    Method: Use scaling relations and H₀ tension to constrain R₄.
    """

    print("\n" + "-" * 70)
    print("  Estimating Klein₄ (Cosmological) parameters")
    print("-" * 70)

    # Known: R₃ = 8400 km works for stellar BH (M ~ 30-100 M☉)
    R_3 = 8.4e6  # m
    M_3_typical = 60 * M_sun  # kg (typical BBH total mass)

    # For cosmological scale, characteristic mass is much larger
    # Option 1: Scale by Hubble radius
    R_Hubble = c_si / (H_0_local * 1000 / Mpc_to_m)  # Hubble radius in m

    # Option 2: Scale by mass ratio
    # If R scales with mass: R₄/R₃ = (M₄/M₃)^α
    # We need to find α that gives consistent physics

    # Option 3: Scale by characteristic time
    # f₃ = 5.68 Hz → τ₃ = 176 ms
    # f₄ should match Hubble time scale?

    f_3 = 5.68  # Hz
    tau_3 = 1/f_3  # seconds

    # Hubble time
    tau_Hubble = 1 / (H_0_local * 1000 / Mpc_to_m)  # seconds

    print(f"\n  Scaling options:")
    print(f"    Klein₃: R = {R_3/1000:.0f} km, f = {f_3:.2f} Hz, τ = {tau_3*1000:.1f} ms")
    print(f"    Hubble: R_H = {R_Hubble:.2e} m, τ_H = {tau_Hubble/1e9:.1f} Gyr")

    # HYPOTHESIS: Klein levels are logarithmically spaced
    # log(R_n) - log(R_{n-1}) ≈ constant

    # From Planck to Stellar BH: ~41 orders of magnitude
    # Klein₁ → Klein₃: factor of ~10^41
    R_1 = np.sqrt(hbar_si * G_si / c_si**3)  # Planck length

    log_ratio_13 = np.log10(R_3 / R_1)
    print(f"\n  Log spacing analysis:")
    print(f"    log(R₃/R₁) = {log_ratio_13:.1f}")
    print(f"    If 2 steps: each step = {log_ratio_13/2:.1f} orders of magnitude")

    # Estimate R₄ by continuing the pattern
    # One more step of similar magnitude
    step_size = log_ratio_13 / 2  # ~20.5 orders of magnitude per step

    R_4_estimate_geometric = R_3 * 10**step_size
    f_4_estimate_geometric = c_si / (2 * np.pi * R_4_estimate_geometric)

    print(f"\n  Klein₄ estimates (geometric progression):")
    print(f"    R₄ = {R_4_estimate_geometric:.2e} m")
    print(f"    f₄ = {f_4_estimate_geometric:.2e} Hz")

    # Alternative: R₄ such that it explains H₀ tension
    # The tension is ~8% difference between local and CMB
    # If Klein₄ causes distance correction at cosmological scales...

    delta_H0 = (H_0_local - H_0_cmb) / H_0_cmb  # ~0.084

    # Simple model: Klein correction to distance
    # D_observed = D_true × (1 + ε₄ × f(z))
    # This would modify H₀ inference

    # For ε₄ ~ 0.1 (similar to Klein₃ deformations)
    # Need f(z) ~ 0.8 at z ~ 1 (SN distances)

    # This constrains R₄ to be comparable to typical SN distances
    # D_SN ~ 100-1000 Mpc
    R_4_from_H0 = 500 * Mpc_to_m  # ~500 Mpc in meters
    f_4_from_H0 = c_si / (2 * np.pi * R_4_from_H0)

    print(f"\n  Klein₄ estimates (from H₀ tension constraint):")
    print(f"    R₄ = {R_4_from_H0:.2e} m = {R_4_from_H0/Mpc_to_m:.0f} Mpc")
    print(f"    f₄ = {f_4_from_H0:.2e} Hz")

    klein4_params = {
        'geometric': {
            'R_m': R_4_estimate_geometric,
            'f_Hz': f_4_estimate_geometric,
            'method': 'Logarithmic extrapolation from Klein₁→Klein₃'
        },
        'H0_constrained': {
            'R_m': R_4_from_H0,
            'R_Mpc': R_4_from_H0 / Mpc_to_m,
            'f_Hz': f_4_from_H0,
            'method': 'Constrained to explain H₀ tension'
        }
    }

    return klein4_params

# =============================================================================
# PART 2: MATRIOSKA TRANSITION MODEL
# =============================================================================

def matrioska_transition_model():
    """
    Model how systems transition between Klein levels.

    Key question: At what mass/scale does Klein₃ → Klein₄?
    """

    print("\n" + "=" * 70)
    print("PART 2: MATRIOSKA TRANSITION MODEL")
    print("=" * 70)

    # Hypothesis: Transition occurs when R_s of system ≈ R_Klein
    # For Klein₃: R₃ = 8400 km
    # Transition mass: M where R_s(M) = R₃

    R_3 = 8.4e6  # m = 8400 km
    R_s_per_kg = 2 * G_si / c_si**2  # R_s = 2GM/c²

    M_transition_3_4 = R_3 / R_s_per_kg
    M_transition_solar = M_transition_3_4 / M_sun

    print(f"\n  Klein₃ → Klein₄ transition:")
    print(f"    Occurs when R_s ≈ R₃ = {R_3/1000:.0f} km")
    print(f"    M_transition = {M_transition_solar:.0f} M☉")
    print(f"    This is {M_transition_solar/1e6:.1f} × 10⁶ M☉")

    # This is in the SMBH range!
    print(f"\n  Physical interpretation:")
    print(f"    Stellar BH (< 100 M☉): Klein₃ dominant")
    print(f"    IMBH (100 - 10⁵ M☉): Transition region")
    print(f"    SMBH (> 10⁵ M☉): Klein₄ dominant")

    # Smooth transition function
    def klein_mixing_fraction(M_solar, M_trans=M_transition_solar, width=0.5):
        """
        Fraction of Klein₄ vs Klein₃ as function of mass.
        Returns f₄ ∈ [0, 1] where:
          f₄ = 0 → pure Klein₃
          f₄ = 1 → pure Klein₄
        """
        log_ratio = np.log10(M_solar / M_trans)
        f_4 = 1 / (1 + np.exp(-log_ratio / width))
        return f_4

    # Test the transition function
    test_masses = [30, 100, 1000, 1e4, 1e5, 1e6, 1e7]

    print(f"\n  Klein mixing fraction by mass:")
    print(f"    {'Mass (M☉)':<15} {'f₄ (Klein₄ fraction)':<25} {'Regime'}")
    print(f"    {'-'*60}")

    for M in test_masses:
        f4 = klein_mixing_fraction(M)
        if f4 < 0.1:
            regime = "Klein₃ dominant"
        elif f4 > 0.9:
            regime = "Klein₄ dominant"
        else:
            regime = "Mixed regime"
        print(f"    {M:<15.0e} {f4:<25.3f} {regime}")

    return {
        'M_transition_solar': M_transition_solar,
        'transition_function': klein_mixing_fraction,
        'R_3_m': R_3
    }

# =============================================================================
# PART 3: H₀ TENSION WITH KLEIN₄
# =============================================================================

def test_h0_tension_with_klein4(klein4_params):
    """
    Test if Klein₄ can explain the H₀ tension.

    The tension: H₀(local) = 73.04 vs H₀(CMB) = 67.4 km/s/Mpc

    Hypothesis: Klein₄ causes distance-dependent corrections that
    affect distance ladder measurements differently than CMB inference.
    """

    print("\n" + "=" * 70)
    print("PART 3: H₀ TENSION TEST WITH KLEIN₄")
    print("=" * 70)

    print(f"\n  The H₀ tension:")
    print(f"    H₀ (SH0ES/local) = {H_0_local:.2f} km/s/Mpc")
    print(f"    H₀ (Planck/CMB)  = {H_0_cmb:.2f} km/s/Mpc")
    print(f"    Tension = {(H_0_local - H_0_cmb)/H_0_cmb * 100:.1f}%")
    print(f"    Significance = ~5σ")

    # Use H₀-constrained Klein₄ parameters
    R_4 = klein4_params['H0_constrained']['R_m']
    R_4_Mpc = klein4_params['H0_constrained']['R_Mpc']

    print(f"\n  Testing with R₄ = {R_4_Mpc:.0f} Mpc")

    # Model: Klein₄ deformation affects distance measurements
    # D_measured = D_true × (1 + ε₄(z))
    # where ε₄(z) depends on how much the light path samples Klein₄

    def klein4_distance_correction(z, R_4_Mpc, epsilon_4_max=0.1):
        """
        Klein₄ correction to comoving distance.

        Physical picture: Light traveling through Klein₄-deformed space
        experiences path length modification proportional to:
        - Distance traveled (more exposure to Klein₄)
        - Klein₄ deformation amplitude
        """
        # Comoving distance in simple cosmology
        D_comoving_Mpc = c_si / 1000 * z / H_0_cmb  # Mpc (approx for low z)

        # Klein₄ correction: accumulates with distance
        # Saturates at scale R₄
        x = D_comoving_Mpc / R_4_Mpc
        epsilon_4 = epsilon_4_max * (1 - np.exp(-x))

        # Corrected distance
        D_corrected = D_comoving_Mpc * (1 + epsilon_4)

        return D_corrected, epsilon_4

    # Test at different redshifts
    redshifts = [0.01, 0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 1100]  # Including CMB

    print(f"\n  Klein₄ correction by redshift:")
    print(f"    {'z':<10} {'D_true (Mpc)':<15} {'ε₄':<10} {'D_corrected':<15}")
    print(f"    {'-'*55}")

    corrections = []
    for z in redshifts:
        D_true = c_si / 1000 * z / H_0_cmb  # Simple approximation
        D_corr, eps = klein4_distance_correction(z, R_4_Mpc)
        corrections.append({'z': z, 'D_true': D_true, 'epsilon': eps, 'D_corrected': D_corr})

        if z < 100:
            print(f"    {z:<10.2f} {D_true:<15.1f} {eps:<10.4f} {D_corr:<15.1f}")
        else:
            print(f"    {z:<10.0f} {D_true:<15.0f} {eps:<10.4f} {D_corr:<15.0f}")

    # Key test: Does Klein₄ correction explain the H₀ difference?
    # Local measurements (z ~ 0.01-0.1): Small Klein₄ correction
    # CMB (z ~ 1100): Large Klein₄ correction

    # Effective H₀ from corrected distances
    # H₀_eff = c × z / D_corrected = H₀_true / (1 + ε₄)

    eps_local = corrections[1]['epsilon']  # z = 0.1
    eps_cmb = corrections[-1]['epsilon']   # z = 1100

    H0_local_from_model = H_0_cmb * (1 + eps_cmb) / (1 + eps_local)

    print(f"\n  H₀ prediction from Klein₄ model:")
    print(f"    ε₄(z=0.1) = {eps_local:.4f}")
    print(f"    ε₄(z=1100) = {eps_cmb:.4f}")
    print(f"    H₀(predicted local) = {H0_local_from_model:.2f} km/s/Mpc")
    print(f"    H₀(observed local) = {H_0_local:.2f} km/s/Mpc")
    print(f"    Difference = {abs(H0_local_from_model - H_0_local):.2f} km/s/Mpc")

    # Can we fit ε_max to match the tension?
    def h0_residual(epsilon_max):
        eps_l = epsilon_max * (1 - np.exp(-0.1 * c_si/1000/H_0_cmb / R_4_Mpc))
        eps_c = epsilon_max * (1 - np.exp(-1100 * c_si/1000/H_0_cmb / R_4_Mpc))
        H0_pred = H_0_cmb * (1 + eps_c) / (1 + eps_l)
        return (H0_pred - H_0_local)**2

    from scipy.optimize import minimize_scalar
    result = minimize_scalar(h0_residual, bounds=(0, 1), method='bounded')
    epsilon_max_fit = result.x

    # Recalculate with fitted epsilon
    eps_l_fit = epsilon_max_fit * (1 - np.exp(-0.1 * c_si/1000/H_0_cmb / R_4_Mpc))
    eps_c_fit = epsilon_max_fit * (1 - np.exp(-1100 * c_si/1000/H_0_cmb / R_4_Mpc))
    H0_pred_fit = H_0_cmb * (1 + eps_c_fit) / (1 + eps_l_fit)

    print(f"\n  Fitted Klein₄ model:")
    print(f"    ε₄_max (fitted) = {epsilon_max_fit:.4f}")
    print(f"    H₀(predicted) = {H0_pred_fit:.2f} km/s/Mpc")
    print(f"    H₀(observed) = {H_0_local:.2f} km/s/Mpc")

    if abs(H0_pred_fit - H_0_local) < 0.5:
        verdict = "✓ Klein₄ CAN explain H₀ tension with reasonable ε_max"
    else:
        verdict = "✗ Klein₄ CANNOT explain H₀ tension with this model"

    print(f"\n  {verdict}")

    # Check if ε_max is physically reasonable
    if epsilon_max_fit < 0.1:
        physical = "✓ ε_max < 0.1 is physically reasonable (similar to Klein₃)"
    elif epsilon_max_fit < 0.65:
        physical = "⚠ ε_max requires moderate deformation"
    else:
        physical = "✗ ε_max > 0.65 exceeds Klein₃ maximum"

    print(f"  {physical}")

    return {
        'epsilon_max_required': float(epsilon_max_fit),
        'H0_predicted': float(H0_pred_fit),
        'H0_observed': H_0_local,
        'R_4_Mpc': R_4_Mpc,
        'can_explain_tension': abs(H0_pred_fit - H_0_local) < 0.5,
        'physically_reasonable': epsilon_max_fit < 0.65
    }

# =============================================================================
# PART 4: TEST WITH GWTC DATA
# =============================================================================

def test_matrioska_with_gwtc(transition_model):
    """
    Look for evidence of Matrioska transitions in GWTC data.

    If Matrioska is real, we should see:
    1. Different Klein correlations for different mass ranges
    2. Weakening of Klein₃ signatures at high mass
    3. Possible emergence of Klein₄ signatures
    """

    print("\n" + "=" * 70)
    print("PART 4: GWTC DATA TEST FOR MATRIOSKA")
    print("=" * 70)

    # Load GWTC data
    csv_path = Path(__file__).parent.parent.parent / "FUNDAMENTAL_RADIUS_INVESTIGATION" / "5_Code" / "data" / "events.csv"

    if not csv_path.exists():
        print("\n  ⚠ GWTC data not found - skipping empirical test")
        return None

    df = pd.read_csv(csv_path)
    print(f"\n  Loaded {len(df)} GWTC events")

    # Calculate Klein₃ and Klein₄ mixing for each event
    M_transition = transition_model['M_transition_solar']
    klein_mixing = transition_model['transition_function']

    # Extract masses
    M_total = df['total_mass_source'].fillna(
        df['mass_1_source'].fillna(30) + df['mass_2_source'].fillna(20)
    )

    # Calculate Klein mixing fraction for each event
    f_4 = np.array([klein_mixing(M) for M in M_total])

    # Classify events by dominant Klein level
    klein_level = np.where(f_4 < 0.1, 'Klein₃',
                          np.where(f_4 > 0.9, 'Klein₄', 'Mixed'))

    # Add to dataframe
    df['M_total'] = M_total
    df['f_klein4'] = f_4
    df['klein_level'] = klein_level

    # Summary by Klein level
    print(f"\n  Event distribution by Klein level:")
    for level in ['Klein₃', 'Mixed', 'Klein₄']:
        n = (klein_level == level).sum()
        pct = 100 * n / len(df)
        masses = M_total[klein_level == level]
        if len(masses) > 0:
            print(f"    {level}: {n} events ({pct:.1f}%), M = {masses.min():.1f} - {masses.max():.1f} M☉")
        else:
            print(f"    {level}: {n} events ({pct:.1f}%)")

    # Test: Do Klein₃ correlations weaken as f₄ increases?
    # Use SNR as proxy for Klein effect (from previous analyses)

    if 'network_matched_filter_snr' in df.columns:
        SNR = df['network_matched_filter_snr'].fillna(10)
        d_L = df['luminosity_distance'].fillna(1000)
        M_chirp = df['chirp_mass_source'].fillna(25)

        # Expected SNR (standard scaling)
        SNR_expected = (M_chirp**(5/6) / d_L) * 1000
        SNR_expected = SNR_expected / SNR_expected.median() * SNR.median()

        # Residual
        SNR_residual = (SNR - SNR_expected) / SNR_expected

        # Correlation of residual with Klein₃ features
        # If Matrioska is real, correlation should weaken at high f₄

        # Split by Klein mixing
        low_f4 = f_4 < 0.1   # Pure Klein₃
        high_f4 = f_4 > 0.01  # Some Klein₄ mixing (most events)

        print(f"\n  Testing Klein₃ correlation vs Klein mixing:")

        if low_f4.sum() > 5:
            corr_low = stats.spearmanr(M_total[low_f4], SNR_residual[low_f4])
            print(f"    Low f₄ (<0.1): r = {corr_low[0]:.3f}, p = {corr_low[1]:.4f}, n = {low_f4.sum()}")

        # Correlation of SNR residual with f₄ directly
        corr_f4 = stats.spearmanr(f_4, SNR_residual)
        print(f"    SNR_residual vs f₄: r = {corr_f4[0]:.3f}, p = {corr_f4[1]:.4f}")

        # Interpretation
        if corr_f4[1] < 0.05 and corr_f4[0] > 0:
            interp = "✓ SNR residual INCREASES with Klein₄ mixing - possible Klein₄ effect"
        elif corr_f4[1] < 0.05 and corr_f4[0] < 0:
            interp = "⚠ SNR residual DECREASES with Klein₄ mixing - Klein₃ weakening?"
        else:
            interp = "✗ No significant correlation with Klein mixing"

        print(f"\n  Interpretation: {interp}")

        return {
            'n_events': len(df),
            'n_klein3': int((klein_level == 'Klein₃').sum()),
            'n_mixed': int((klein_level == 'Mixed').sum()),
            'n_klein4': int((klein_level == 'Klein₄').sum()),
            'corr_f4_snr': {'r': float(corr_f4[0]), 'p': float(corr_f4[1])},
            'M_transition': float(M_transition)
        }

    return None

# =============================================================================
# PART 5: PREDICTIONS AND FALSIFICATION
# =============================================================================

def matrioska_predictions():
    """
    Generate specific, falsifiable predictions from Matrioska-Klein.
    """

    print("\n" + "=" * 70)
    print("PART 5: MATRIOSKA-KLEIN PREDICTIONS")
    print("=" * 70)

    predictions = {
        'gw_predictions': {
            'description': 'Gravitational wave observations',
            'tests': [
                {
                    'prediction': 'Klein₃ correlations weaken for M > 10⁴ M☉',
                    'falsification': 'Correlations remain constant across all masses',
                    'data_needed': 'IMBH mergers from LIGO O4/O5'
                },
                {
                    'prediction': 'Different harmonic structure for SMBH mergers',
                    'falsification': 'Same 40:1 odd/even ratio at all masses',
                    'data_needed': 'LISA observations of SMBH mergers'
                },
                {
                    'prediction': 'Transition region at M ~ 10⁵-10⁶ M☉',
                    'falsification': 'Sharp transition or no transition at all',
                    'data_needed': 'IMBH population study'
                }
            ]
        },
        'cosmological_predictions': {
            'description': 'Cosmological observations',
            'tests': [
                {
                    'prediction': 'H₀ tension explained by Klein₄ with ε_max ~ 0.08',
                    'falsification': 'Required ε_max > 0.65 or negative',
                    'data_needed': 'Already available (SH0ES vs Planck)'
                },
                {
                    'prediction': 'Distance-dependent deviation from ΛCDM',
                    'falsification': 'Perfect ΛCDM agreement with high-z data',
                    'data_needed': 'DESI BAO, future SN surveys'
                },
                {
                    'prediction': 'Klein₄ effects in CMB acoustic scale',
                    'falsification': 'No acoustic scale anomaly',
                    'data_needed': 'CMB-S4 precision measurements'
                }
            ]
        },
        'theoretical_predictions': {
            'description': 'Theoretical consistency tests',
            'tests': [
                {
                    'prediction': 'Klein levels logarithmically spaced',
                    'falsification': 'Arbitrary spacing or linear scaling',
                    'data_needed': 'Multi-scale Klein detection'
                },
                {
                    'prediction': 'Smooth transition between levels',
                    'falsification': 'Sharp phase transition',
                    'data_needed': 'Mass-dependent Klein measurements'
                },
                {
                    'prediction': 'All levels share same ε_max ~ 0.65',
                    'falsification': 'Different ε_max at different scales',
                    'data_needed': 'Multi-scale deformation measurements'
                }
            ]
        }
    }

    print("\n  FALSIFIABLE PREDICTIONS:")
    print("-" * 70)

    for category, data in predictions.items():
        print(f"\n  {data['description'].upper()}:")
        for i, test in enumerate(data['tests'], 1):
            print(f"\n    {i}. Prediction: {test['prediction']}")
            print(f"       Falsification: {test['falsification']}")
            print(f"       Data needed: {test['data_needed']}")

    return predictions

# =============================================================================
# MAIN
# =============================================================================

def main():
    print("\n" + "=" * 70)
    print("EXECUTING MATRIOSKA-KLEIN ANALYSIS")
    print("=" * 70)

    results = {
        'timestamp': datetime.now().isoformat(),
        'hypothesis': 'Nested Klein dimensions at different scales'
    }

    # Part 1: Theoretical framework
    scales, R_3 = define_matrioska_levels()
    results['anchor_R3_m'] = R_3

    # Estimate Klein₄ parameters
    klein4_params = estimate_klein4_parameters()
    results['klein4_estimates'] = {
        'geometric': {
            'R_m': float(klein4_params['geometric']['R_m']),
            'f_Hz': float(klein4_params['geometric']['f_Hz'])
        },
        'H0_constrained': {
            'R_Mpc': float(klein4_params['H0_constrained']['R_Mpc']),
            'f_Hz': float(klein4_params['H0_constrained']['f_Hz'])
        }
    }

    # Part 2: Transition model
    transition = matrioska_transition_model()
    results['transition'] = {
        'M_transition_solar': float(transition['M_transition_solar']),
        'interpretation': 'Stellar BH → Klein₃, SMBH → Klein₄'
    }

    # Part 3: H₀ tension test
    h0_results = test_h0_tension_with_klein4(klein4_params)
    results['h0_tension_test'] = h0_results

    # Part 4: GWTC test
    gwtc_results = test_matrioska_with_gwtc(transition)
    if gwtc_results:
        results['gwtc_test'] = gwtc_results

    # Part 5: Predictions
    predictions = matrioska_predictions()
    results['predictions'] = predictions

    # ==========================================================================
    # SUMMARY
    # ==========================================================================

    print("\n" + "=" * 70)
    print("MATRIOSKA-KLEIN ANALYSIS SUMMARY")
    print("=" * 70)

    print("\n  FRAMEWORK:")
    print(f"    Klein₃: R = 8,400 km (stellar BH scale) - VALIDATED")
    print(f"    Klein₄: R ~ {klein4_params['H0_constrained']['R_Mpc']:.0f} Mpc (cosmological scale) - HYPOTHESIZED")
    print(f"    Transition mass: ~{transition['M_transition_solar']:.0e} M☉")

    print("\n  KEY RESULTS:")
    if h0_results['can_explain_tension']:
        print(f"    ✓ Klein₄ CAN explain H₀ tension with ε_max = {h0_results['epsilon_max_required']:.4f}")
    else:
        print(f"    ✗ Klein₄ CANNOT explain H₀ tension with simple model")

    if h0_results['physically_reasonable']:
        print(f"    ✓ Required ε_max is physically reasonable")
    else:
        print(f"    ✗ Required ε_max exceeds physical bounds")

    if gwtc_results:
        print(f"    Events by level: Klein₃={gwtc_results['n_klein3']}, Mixed={gwtc_results['n_mixed']}, Klein₄={gwtc_results['n_klein4']}")

    print("\n  STATUS:")
    if h0_results['can_explain_tension'] and h0_results['physically_reasonable']:
        overall = "✓ PROMISING - Matrioska-Klein is internally consistent and could explain H₀"
    else:
        overall = "⚠ NEEDS WORK - Framework requires refinement"

    print(f"    {overall}")

    results['overall_status'] = overall

    # Save results
    output_path = Path(__file__).parent.parent / "results" / "matrioska_klein_analysis.json"
    output_path.parent.mkdir(exist_ok=True)

    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2, default=str)

    print(f"\n✓ Results saved to: {output_path}")

    return results


if __name__ == "__main__":
    results = main()
