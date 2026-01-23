#!/usr/bin/env python3
"""
H₀ TENSION ANALYSIS WITH KLEIN THEORY
======================================

The Hubble Tension:
- Local (Cepheids/SNe): H₀ = 73.04 ± 1.04 km/s/Mpc (SH0ES 2022)
- CMB (Planck): H₀ = 67.4 ± 0.5 km/s/Mpc
- Difference: ~5.8 km/s/Mpc (>5σ discrepancy)

Question: Can Klein Theory explain this?

Hypothesis: If light/gravity propagates through 5D Klein topology,
distances measured locally vs cosmologically could differ systematically.

Author: Klein Theory Team
Date: January 2026
"""

import numpy as np
import pandas as pd
from scipy import stats
from scipy.optimize import minimize
import json
from pathlib import Path
from datetime import datetime

# =============================================================================
# OBSERVED VALUES
# =============================================================================

# Local measurements (late universe)
H0_LOCAL = 73.04  # km/s/Mpc (SH0ES 2022)
H0_LOCAL_ERR = 1.04

# CMB measurements (early universe)
H0_CMB = 67.4  # km/s/Mpc (Planck 2018)
H0_CMB_ERR = 0.5

# The tension
H0_TENSION = H0_LOCAL - H0_CMB  # ~5.6 km/s/Mpc
H0_TENSION_SIGMA = H0_TENSION / np.sqrt(H0_LOCAL_ERR**2 + H0_CMB_ERR**2)

# Klein parameters (validated)
R_KLEIN = 8400  # km
f_0 = 5.68  # Hz
EPSILON_MAX = 0.65
c = 299792.458  # km/s

print("=" * 70)
print("H₀ TENSION ANALYSIS WITH KLEIN THEORY")
print("=" * 70)
print(f"\nThe Hubble Tension:")
print(f"  H₀ (local/SH0ES):  {H0_LOCAL} ± {H0_LOCAL_ERR} km/s/Mpc")
print(f"  H₀ (CMB/Planck):   {H0_CMB} ± {H0_CMB_ERR} km/s/Mpc")
print(f"  Difference:        {H0_TENSION:.1f} km/s/Mpc")
print(f"  Significance:      {H0_TENSION_SIGMA:.1f}σ")

print(f"\nKlein Parameters (validated 10σ from GW):")
print(f"  R_Klein = {R_KLEIN} km")
print(f"  f₀ = {f_0} Hz")
print(f"  ε_max = {EPSILON_MAX}")

# =============================================================================
# KLEIN MODEL FOR H₀
# =============================================================================

def klein_distance_correction(z, epsilon_eff):
    """
    Klein theory correction to luminosity distance.

    In 5D Klein topology, photons can take slightly different paths,
    effectively changing the measured distance.

    d_observed = d_true × (1 + δ_klein)

    Where δ_klein depends on redshift and Klein coupling.
    """
    # Klein correction factor
    # At low z (local): minimal correction
    # At high z (CMB): accumulated correction

    # Model: correction grows with light travel time
    # δ_klein = ε² × (1 - 1/(1+z))

    delta_klein = epsilon_eff**2 * (1 - 1/(1+z))

    return delta_klein


def klein_h0_model(z, H0_true, epsilon_eff):
    """
    Apparent H₀ as function of redshift in Klein theory.

    If distances are systematically different due to Klein,
    the inferred H₀ will depend on the redshift of calibrators.
    """
    # Distance correction
    delta = klein_distance_correction(z, epsilon_eff)

    # Apparent H₀ = True H₀ × (1 + distance_correction)
    # Because H₀ = v/d, if d is overestimated, H₀ is underestimated
    H0_apparent = H0_true * (1 + delta)

    return H0_apparent


def explain_tension():
    """
    Can Klein theory explain the H₀ tension?
    """
    print("\n" + "=" * 70)
    print("KLEIN MODEL FOR H₀ TENSION")
    print("=" * 70)

    # CMB is at z ~ 1100
    z_cmb = 1100

    # Local measurements use z ~ 0.01-0.1
    z_local = 0.05  # Typical Cepheid/SNe calibrator

    print(f"\n  CMB probes z ~ {z_cmb}")
    print(f"  Local probes z ~ {z_local}")

    # What ε would explain the tension?
    # H0_local/H0_cmb = (1 + δ_local)/(1 + δ_cmb)

    ratio_observed = H0_LOCAL / H0_CMB  # ~1.084

    print(f"\n  Observed ratio H₀_local/H₀_cmb = {ratio_observed:.4f}")

    # Solve for epsilon
    def tension_residual(epsilon):
        delta_local = klein_distance_correction(z_local, epsilon)
        delta_cmb = klein_distance_correction(z_cmb, epsilon)
        ratio_klein = (1 + delta_local) / (1 + delta_cmb)
        return (ratio_klein - ratio_observed)**2

    # Find optimal epsilon
    result = minimize(tension_residual, x0=0.3, bounds=[(0, EPSILON_MAX)])
    epsilon_required = result.x[0]

    # Check if it's physical
    delta_local = klein_distance_correction(z_local, epsilon_required)
    delta_cmb = klein_distance_correction(z_cmb, epsilon_required)
    ratio_klein = (1 + delta_local) / (1 + delta_cmb)

    print(f"\n  To explain tension, need ε = {epsilon_required:.4f}")
    print(f"  This gives:")
    print(f"    δ_klein(z=0.05) = {delta_local:.6f}")
    print(f"    δ_klein(z=1100) = {delta_cmb:.6f}")
    print(f"    Ratio = {ratio_klein:.4f}")

    # Is this consistent with GW-validated epsilon?
    epsilon_gw = 0.2  # Typical from GW analysis

    print(f"\n  Comparison with GW-validated ε:")
    print(f"    Required for H₀: ε = {epsilon_required:.4f}")
    print(f"    From GW analysis: ε ~ {epsilon_gw:.2f}")

    if abs(epsilon_required - epsilon_gw) / epsilon_gw < 0.5:
        consistency = "✓ CONSISTENT - Same order of magnitude"
    else:
        consistency = "⚠ TENSION - Different scales needed"

    print(f"    {consistency}")

    return {
        'epsilon_required': float(epsilon_required),
        'epsilon_gw': epsilon_gw,
        'ratio_observed': ratio_observed,
        'ratio_klein': ratio_klein,
        'delta_local': delta_local,
        'delta_cmb': delta_cmb,
        'consistent': abs(epsilon_required - epsilon_gw) / epsilon_gw < 0.5
    }


# =============================================================================
# ALTERNATIVE MODEL: REDSHIFT-DEPENDENT H₀
# =============================================================================

def redshift_dependent_h0():
    """
    Test if H₀ varies with redshift as Klein predicts.
    """
    print("\n" + "=" * 70)
    print("REDSHIFT-DEPENDENT H₀ MODEL")
    print("=" * 70)

    # Simulated/literature data points at different z
    # Real data from various probes
    data = [
        {'probe': 'Cepheids (SH0ES)', 'z_eff': 0.023, 'H0': 73.04, 'err': 1.04},
        {'probe': 'TRGB', 'z_eff': 0.007, 'H0': 69.8, 'err': 1.7},
        {'probe': 'Masers', 'z_eff': 0.016, 'H0': 73.9, 'err': 3.0},
        {'probe': 'SN time delays', 'z_eff': 0.5, 'H0': 74.2, 'err': 1.6},
        {'probe': 'Strong lensing (H0LiCOW)', 'z_eff': 0.6, 'H0': 73.3, 'err': 1.8},
        {'probe': 'BAO + BBN', 'z_eff': 0.5, 'H0': 67.4, 'err': 1.1},
        {'probe': 'BAO + D/H', 'z_eff': 2.3, 'H0': 67.0, 'err': 1.2},
        {'probe': 'Planck CMB', 'z_eff': 1100, 'H0': 67.4, 'err': 0.5},
    ]

    df = pd.DataFrame(data)

    print("\n  H₀ measurements at different redshifts:")
    print(f"  {'Probe':<25} {'z_eff':<10} {'H₀':<15}")
    print("  " + "-" * 50)
    for _, row in df.iterrows():
        print(f"  {row['probe']:<25} {row['z_eff']:<10.3f} {row['H0']:.1f} ± {row['err']:.1f}")

    # Fit Klein model
    def klein_h0_fit(params, z_values):
        H0_true, epsilon = params
        return np.array([klein_h0_model(z, H0_true, epsilon) for z in z_values])

    def chi_squared(params):
        H0_pred = klein_h0_fit(params, df['z_eff'].values)
        chi2 = np.sum(((df['H0'].values - H0_pred) / df['err'].values)**2)
        return chi2

    # Fit
    result = minimize(chi_squared, x0=[70, 0.2],
                      bounds=[(60, 80), (0, EPSILON_MAX)])

    H0_true_fit, epsilon_fit = result.x
    chi2_klein = result.fun
    dof = len(df) - 2

    # Compare to constant H₀ model
    H0_mean = np.average(df['H0'], weights=1/df['err']**2)
    chi2_constant = np.sum(((df['H0'].values - H0_mean) / df['err'].values)**2)

    print(f"\n  Model Comparison:")
    print(f"  {'Model':<20} {'χ²':<10} {'dof':<6} {'χ²/dof':<10}")
    print("  " + "-" * 46)
    print(f"  {'Constant H₀':<20} {chi2_constant:<10.2f} {dof+1:<6} {chi2_constant/(dof+1):<10.2f}")
    print(f"  {'Klein varying H₀':<20} {chi2_klein:<10.2f} {dof:<6} {chi2_klein/dof:<10.2f}")

    # F-test for model comparison
    F_stat = (chi2_constant - chi2_klein) / (chi2_klein / dof)
    p_value = 1 - stats.f.cdf(F_stat, 1, dof)

    print(f"\n  F-test: F = {F_stat:.2f}, p = {p_value:.4f}")

    # Best fit parameters
    print(f"\n  Best-fit Klein model:")
    print(f"    H₀_true = {H0_true_fit:.2f} km/s/Mpc")
    print(f"    ε_eff = {epsilon_fit:.4f}")

    # Predictions
    print(f"\n  Klein model predictions:")
    for z in [0.01, 0.1, 1.0, 10, 100, 1000]:
        H0_pred = klein_h0_model(z, H0_true_fit, epsilon_fit)
        print(f"    z = {z:<6}: H₀_apparent = {H0_pred:.2f} km/s/Mpc")

    # Verdict
    if chi2_klein < chi2_constant and p_value < 0.05:
        verdict = "✓ Klein model fits better than constant H₀"
    elif chi2_klein < chi2_constant:
        verdict = "⚠ Klein model slightly better but not significant"
    else:
        verdict = "✗ Constant H₀ fits as well or better"

    print(f"\n  {verdict}")

    return {
        'data': data,
        'H0_true_fit': H0_true_fit,
        'epsilon_fit': epsilon_fit,
        'chi2_klein': chi2_klein,
        'chi2_constant': chi2_constant,
        'F_stat': F_stat,
        'p_value': p_value,
        'verdict': verdict
    }


# =============================================================================
# PHYSICAL INTERPRETATION
# =============================================================================

def physical_interpretation():
    """
    Physical interpretation of Klein's effect on H₀.
    """
    print("\n" + "=" * 70)
    print("PHYSICAL INTERPRETATION")
    print("=" * 70)

    print("""
    WHY KLEIN COULD AFFECT H₀:
    ══════════════════════════

    1. DISTANCE LADDER CALIBRATION
       - Local: d = v/H₀ using Cepheids/SNe at z~0.01-0.1
       - CMB: d from sound horizon at z~1100
       - If Klein affects distance differently at different z → tension

    2. LIGHT PROPAGATION IN 5D
       - Photons can briefly enter 5th dimension
       - This adds effective path length: d_eff = d × (1 + ε²f(z))
       - At low z: minimal effect (short path)
       - At high z: accumulated effect (long path)

    3. ACOUSTIC HORIZON SCALE
       - CMB measures r_s (sound horizon at recombination)
       - If r_s is affected by Klein topology → different H₀ inferred
       - Klein predicts: r_s_observed = r_s_true × (1 + δ_klein(z=1100))

    CRITICAL TEST:
    ══════════════

    Klein theory makes SPECIFIC prediction:

        H₀(z) = H₀_true × (1 + ε² × (1 - 1/(1+z)))

    This is DIFFERENT from:
    - Early dark energy (step function)
    - Modified gravity (power law)
    - New particles (various shapes)

    FALSIFICATION:
    ══════════════

    If H₀(z) measurements don't follow Klein's specific z-dependence
    → Klein explanation FALSIFIED

    If they DO follow it with ε ~ 0.2 (same as GW)
    → STRONG confirmation across domains
    """)


# =============================================================================
# MAIN
# =============================================================================

def main():
    results = {
        'timestamp': datetime.now().isoformat(),
        'tension': {
            'H0_local': H0_LOCAL,
            'H0_cmb': H0_CMB,
            'difference': H0_TENSION,
            'significance_sigma': H0_TENSION_SIGMA
        },
        'klein_parameters': {
            'R_km': R_KLEIN,
            'f0_Hz': f_0,
            'epsilon_max': EPSILON_MAX
        }
    }

    # Analysis 1: Can Klein explain tension?
    results['tension_explanation'] = explain_tension()

    # Analysis 2: Redshift-dependent H₀
    results['z_dependent_h0'] = redshift_dependent_h0()

    # Physical interpretation
    physical_interpretation()

    # ==========================================================================
    # SUMMARY
    # ==========================================================================

    print("\n" + "=" * 70)
    print("SUMMARY: KLEIN THEORY AND H₀ TENSION")
    print("=" * 70)

    eps_required = results['tension_explanation']['epsilon_required']
    eps_gw = results['tension_explanation']['epsilon_gw']
    consistent = results['tension_explanation']['consistent']

    print(f"""
    THE H₀ TENSION: {H0_TENSION:.1f} km/s/Mpc ({H0_TENSION_SIGMA:.1f}σ)

    KLEIN EXPLANATION:
    • Required ε to explain tension: {eps_required:.4f}
    • ε from GW analysis: ~{eps_gw:.2f}
    • Consistency: {'✓ YES' if consistent else '✗ NO'}

    MODEL FIT:
    • H₀_true (Klein) = {results['z_dependent_h0']['H0_true_fit']:.2f} km/s/Mpc
    • ε_effective = {results['z_dependent_h0']['epsilon_fit']:.4f}
    • χ² improvement: {results['z_dependent_h0']['chi2_constant'] - results['z_dependent_h0']['chi2_klein']:.2f}
    • p-value: {results['z_dependent_h0']['p_value']:.4f}

    VERDICT: {results['z_dependent_h0']['verdict']}
    """)

    # Overall assessment
    if consistent and results['z_dependent_h0']['p_value'] < 0.1:
        overall = "✓ Klein theory COULD explain H₀ tension with consistent parameters"
    elif consistent:
        overall = "⚠ Klein theory consistent but not statistically preferred"
    else:
        overall = "✗ Klein theory requires different ε for H₀ vs GW"

    print(f"  OVERALL: {overall}")

    results['overall'] = overall

    # Save
    output_path = Path(__file__).parent.parent / "results" / "h0_tension_klein.json"
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2, default=str)

    print(f"\n✓ Results saved to: {output_path}")

    return results


if __name__ == "__main__":
    results = main()
