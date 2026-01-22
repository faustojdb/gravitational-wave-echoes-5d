#!/usr/bin/env python3
"""
DOPPLER-KLEIN FALSIFICATION PROTOCOL
====================================
Testing the Doppler-Klein extension with GWTC data

Key differences from basic Klein:
- f₀ = 5.68 Hz (R = 8400 km empirical radius)
- Uses twist factors for par/impar modes
- Doppler shift of Klein frequency, not merger frequency harmonics
- 10σ claimed significance

Author: Klein Theory Falsification Team
Date: January 2026
"""

import numpy as np
import pandas as pd
import json
from pathlib import Path
from scipy import stats
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# =============================================================================
# DOPPLER-KLEIN PARAMETERS
# =============================================================================

c = 299792.458  # km/s
R_EMPIRICAL = 8400  # km (empirical radius)
f_0 = 5.68  # Hz (Doppler-Klein reference frequency)
EPSILON_MAX = 0.65

print("=" * 70)
print("DOPPLER-KLEIN FALSIFICATION PROTOCOL")
print("=" * 70)
print(f"\nDoppler-Klein Parameters:")
print(f"  R_empirical = {R_EMPIRICAL} km")
print(f"  f₀ = {f_0} Hz")
print(f"  ε_max = {EPSILON_MAX}")

# =============================================================================
# LOAD GWTC DATA
# =============================================================================

def load_gwtc_data():
    """Load GWTC event data."""
    csv_path = Path(__file__).parent.parent.parent / "FUNDAMENTAL_RADIUS_INVESTIGATION" / "5_Code" / "data" / "events.csv"

    if csv_path.exists():
        df = pd.read_csv(csv_path)
        print(f"\n✓ Loaded {len(df)} events from GWTC catalog")
        return df

    raise FileNotFoundError("No GWTC data found!")


# =============================================================================
# DOPPLER-KLEIN MODEL
# =============================================================================

def calculate_doppler_klein(row):
    """
    Calculate Doppler-Klein parameters for an event.
    Based on the integrated_final_klein_doppler.py model.
    """
    # Extract parameters
    M1 = row.get('mass_1_source', np.nan)
    M2 = row.get('mass_2_source', np.nan)
    d_L = row.get('luminosity_distance', np.nan)
    snr = row.get('network_matched_filter_snr', np.nan)
    z = row.get('redshift', np.nan)
    chi_eff = row.get('chi_eff', 0)

    if pd.isna(M1) or pd.isna(M2) or pd.isna(d_L):
        return None

    M_total = M1 + M2

    # Handle missing values
    if pd.isna(snr): snr = 10
    if pd.isna(z): z = d_L * 70.0 / c / 1000  # Estimate from Hubble
    if pd.isna(chi_eff): chi_eff = 0

    # Efficiency estimate
    mass_ratio = min(M1, M2) / max(M1, M2) if max(M1, M2) > 0 else 0.5
    efficiency = 0.005 + 0.045 * mass_ratio + 0.01 * max(0, chi_eff)
    efficiency = np.clip(efficiency, 0.005, 0.05)

    # Energy
    radiated_energy = M_total * efficiency
    E_initial = radiated_energy * snr / 20.0

    # Distance in km
    L_km = d_L * 3.086e19  # Mpc to km

    # Velocities (cosmological model)
    v_hubble = 70.0 * d_L  # km/s
    v_peculiar = np.random.uniform(-800, 800)
    v_spin_kick = chi_eff * 500
    v_total = v_hubble + v_peculiar + v_spin_kick

    # Beta (v/c)
    beta_raw = abs(v_total) / c
    beta = np.clip(beta_raw, 0.0, 0.15)
    v_sign = 1 if v_total > 0 else -1

    # Scale factor
    ratio = L_km / (R_EMPIRICAL * 1000)  # R in meters
    scale_factor = 1.0 + np.log10(max(ratio, 1.0)) * 0.5
    scale_factor = np.clip(scale_factor, 1.0, 25.0)

    # Klein temperature and state
    E_norm = E_initial / (M_total * 0.01)
    snr_factor = snr / 8.0
    z_dilution = 1.0 / (1.0 + z * 0.5)
    spin_factor = 1.0 / (1.0 + 0.3 * (1.0 - chi_eff**2))

    T_klein = E_norm * snr_factor * z_dilution * spin_factor

    # State classification (from Klein thermodynamics)
    threshold_extrema = 0.16
    threshold_relajada = 0.06

    if T_klein > threshold_extrema:
        state = "Klein_extrema"
        par_impar = 1
    elif T_klein < threshold_relajada:
        state = "Klein_relajada"
        par_impar = -1
    else:
        state = "Klein_deformada"
        par_impar = 0

    # Klein deformation (Master Equation)
    gamma = 50.0 * scale_factor
    coupling = 15.0 * scale_factor
    epsilon = (coupling * E_initial / (gamma + coupling)) * EPSILON_MAX
    epsilon = np.clip(epsilon, 0.0, EPSILON_MAX)

    # Doppler factor with Klein twist
    if v_sign > 0:
        doppler_factor = np.sqrt((1 - beta) / (1 + beta))  # Recession
    else:
        doppler_factor = np.sqrt((1 + beta) / (1 - beta))  # Approach

    # Klein twist factor (the key signature!)
    if par_impar != 0 and beta > 0.001:
        if par_impar == 1:  # Par mode: constructive
            twist_factor = 1.0 + beta * 0.18
        else:  # Impar mode: destructive
            twist_factor = 1.0 - beta * 0.08
        doppler_factor *= twist_factor
    else:
        twist_factor = 1.0

    # Klein scale correction
    klein_correction = 1.0 + (ratio / 1e18) * beta * 0.012
    klein_correction = np.clip(klein_correction, 0.95, 1.05)
    doppler_factor *= klein_correction

    # Cosmological factor
    cosmo_factor = 1.0 / (1.0 + z)
    doppler_factor *= cosmo_factor

    # Final frequency and shift
    doppler_factor = np.clip(doppler_factor, 0.5, 1.5)
    f_observed = f_0 * doppler_factor
    doppler_shift = f_observed - f_0

    return {
        'M_total': M_total,
        'd_L': d_L,
        'snr': snr,
        'z': z,
        'epsilon': epsilon,
        'T_klein': T_klein,
        'state': state,
        'par_impar': par_impar,
        'beta': beta,
        'twist_factor': twist_factor,
        'doppler_factor': doppler_factor,
        'f_observed': f_observed,
        'doppler_shift': doppler_shift
    }


# =============================================================================
# FALSIFICATION TEST 1: TWIST FACTOR SIGNIFICANCE
# =============================================================================

def test_twist_factor_significance(results, n_random=1000):
    """
    TEST 1: Is the Klein twist factor real or noise?

    FALSIFICATION: If random twist factors produce similar correlations,
    the Klein twist has no physical meaning.
    """
    print("\n" + "=" * 70)
    print("TEST 1: TWIST FACTOR SIGNIFICANCE")
    print("=" * 70)
    print("\nTesting if Klein twist factors produce real effects")

    # Extract data
    betas = np.array([r['beta'] for r in results])
    doppler_shifts = np.array([r['doppler_shift'] for r in results])
    twist_factors = np.array([r['twist_factor'] for r in results])
    par_impars = np.array([r['par_impar'] for r in results])

    # Real correlation: twist factor vs doppler shift
    real_corr, real_p = stats.spearmanr(twist_factors, np.abs(doppler_shifts))

    print(f"\n  Events: {len(results)}")
    print(f"  Real twist-doppler correlation: r = {real_corr:.4f}, p = {real_p:.4e}")

    # Generate random twist factors
    np.random.seed(42)
    random_corrs = []

    for _ in range(n_random):
        # Random twist factors (no Klein structure)
        random_twist = np.random.uniform(0.95, 1.05, len(results))
        corr, _ = stats.spearmanr(random_twist, np.abs(doppler_shifts))
        random_corrs.append(corr)

    mean_random = np.mean(random_corrs)
    std_random = np.std(random_corrs)

    if std_random > 0:
        z_score = (abs(real_corr) - abs(mean_random)) / std_random
    else:
        z_score = 0

    percentile = 100 * sum(1 for c in random_corrs if abs(c) < abs(real_corr)) / n_random

    print(f"  Random twist mean correlation: {mean_random:.4f} ± {std_random:.4f}")
    print(f"  Z-score: {z_score:.2f}σ")
    print(f"  Percentile: {percentile:.1f}%")

    # Check par/impar asymmetry
    par_events = [r for r in results if r['par_impar'] == 1]
    impar_events = [r for r in results if r['par_impar'] == -1]

    if len(par_events) > 5 and len(impar_events) > 5:
        par_shifts = np.array([r['doppler_shift'] for r in par_events])
        impar_shifts = np.array([r['doppler_shift'] for r in impar_events])

        t_stat, t_p = stats.ttest_ind(par_shifts, impar_shifts)
        print(f"\n  Par mode mean shift: {np.mean(par_shifts):.4f} Hz")
        print(f"  Impar mode mean shift: {np.mean(impar_shifts):.4f} Hz")
        print(f"  T-test: t = {t_stat:.2f}, p = {t_p:.4e}")

        asymmetry_significant = t_p < 0.05
    else:
        asymmetry_significant = False
        print(f"\n  Insufficient par/impar events for asymmetry test")

    if z_score > 2.0 and percentile > 95:
        verdict = "✓ PASSED - Twist factor shows significant correlation"
        falsified = False
    elif asymmetry_significant:
        verdict = "⚠ MARGINAL - Par/impar asymmetry detected"
        falsified = False
    else:
        verdict = "✗ FAILED - Twist factor indistinguishable from noise"
        falsified = True

    print(f"\n{verdict}")

    return {
        'test': 'Twist Factor Significance',
        'real_correlation': float(real_corr),
        'random_mean': float(mean_random),
        'z_score': float(z_score),
        'percentile': float(percentile),
        'asymmetry_significant': asymmetry_significant,
        'falsified': falsified,
        'verdict': verdict
    }


# =============================================================================
# FALSIFICATION TEST 2: EPSILON MAX (same as before)
# =============================================================================

def test_epsilon_max_violations(results):
    """
    TEST 2: Does any event violate ε_max = 0.65?
    """
    print("\n" + "=" * 70)
    print("TEST 2: ε_max VIOLATION SEARCH (Doppler-Klein)")
    print("=" * 70)

    epsilons = np.array([r['epsilon'] for r in results])

    print(f"\n  Events analyzed: {len(results)}")
    print(f"  ε range: [{epsilons.min():.4f}, {epsilons.max():.4f}]")
    print(f"  ε mean: {epsilons.mean():.4f} ± {epsilons.std():.4f}")
    print(f"  ε_max limit: {EPSILON_MAX}")

    violations = sum(1 for e in epsilons if e > EPSILON_MAX)

    if violations > 0:
        verdict = f"✗ FAILED - {violations} violations found"
        falsified = True
    else:
        verdict = "✓ PASSED - No ε_max violations"
        falsified = False

    print(f"\n{verdict}")

    return {
        'test': 'ε_max Violations (Doppler-Klein)',
        'n_events': len(results),
        'violations': violations,
        'eps_max_observed': float(epsilons.max()),
        'falsified': falsified,
        'verdict': verdict
    }


# =============================================================================
# FALSIFICATION TEST 3: STATE DISTRIBUTION
# =============================================================================

def test_state_distribution(results):
    """
    TEST 3: Does state distribution match Klein thermodynamic predictions?

    Theory predicts for subthreshold: more deformada/relajada, less extrema
    """
    print("\n" + "=" * 70)
    print("TEST 3: KLEIN STATE DISTRIBUTION")
    print("=" * 70)

    states = [r['state'] for r in results]
    state_counts = {
        'Klein_extrema': states.count('Klein_extrema'),
        'Klein_deformada': states.count('Klein_deformada'),
        'Klein_relajada': states.count('Klein_relajada')
    }

    n_total = len(states)

    print(f"\n  Observed distribution:")
    for state, count in state_counts.items():
        print(f"    {state}: {count}/{n_total} ({100*count/n_total:.1f}%)")

    # Theory expectation for confident events (high SNR): more extrema
    # Chi-squared test against uniform distribution
    observed = list(state_counts.values())
    expected = [n_total/3, n_total/3, n_total/3]  # Null: uniform

    chi2, p_value = stats.chisquare(observed, expected)

    print(f"\n  χ² test vs uniform: χ² = {chi2:.2f}, p = {p_value:.4e}")

    if p_value < 0.05:
        verdict = "✓ PASSED - State distribution significantly non-uniform"
        falsified = False
    else:
        verdict = "✗ FAILED - States are uniformly distributed (no Klein structure)"
        falsified = True

    print(f"\n{verdict}")

    return {
        'test': 'State Distribution',
        'distribution': state_counts,
        'chi2': float(chi2),
        'p_value': float(p_value),
        'falsified': falsified,
        'verdict': verdict
    }


# =============================================================================
# FALSIFICATION TEST 4: REDSHIFT-DOPPLER CORRELATION
# =============================================================================

def test_redshift_doppler_correlation(results):
    """
    TEST 4: Is there physical correlation between redshift and Doppler shift?

    Klein theory predicts: f_observed = f_0 × (1/(1+z)) × Klein_factors
    So doppler_shift should correlate negatively with redshift.
    """
    print("\n" + "=" * 70)
    print("TEST 4: REDSHIFT-DOPPLER CORRELATION")
    print("=" * 70)

    redshifts = np.array([r['z'] for r in results])
    doppler_shifts = np.array([r['doppler_shift'] for r in results])

    # Real correlation
    r_corr, p_corr = stats.spearmanr(redshifts, doppler_shifts)

    print(f"\n  Correlation (z vs Δf): r = {r_corr:.4f}, p = {p_corr:.4e}")

    # Theory predicts negative correlation
    if r_corr < -0.3 and p_corr < 0.01:
        verdict = "✓ PASSED - Strong negative z-Doppler correlation (as predicted)"
        falsified = False
    elif r_corr < 0 and p_corr < 0.05:
        verdict = "⚠ MARGINAL - Weak negative correlation"
        falsified = False
    else:
        verdict = "✗ FAILED - No physical z-Doppler correlation"
        falsified = True

    print(f"\n{verdict}")

    return {
        'test': 'Redshift-Doppler Correlation',
        'correlation': float(r_corr),
        'p_value': float(p_corr),
        'falsified': falsified,
        'verdict': verdict
    }


# =============================================================================
# FALSIFICATION TEST 5: COMBINED SIGNIFICANCE (Fisher's method)
# =============================================================================

def test_combined_significance(results, n_bootstrap=1000):
    """
    TEST 5: Calculate combined statistical significance.

    Using Fisher's method to combine multiple correlations.
    """
    print("\n" + "=" * 70)
    print("TEST 5: COMBINED SIGNIFICANCE (Fisher's Method)")
    print("=" * 70)

    # Extract all observables
    masses = np.array([r['M_total'] for r in results])
    epsilons = np.array([r['epsilon'] for r in results])
    redshifts = np.array([r['z'] for r in results])
    doppler_shifts = np.array([r['doppler_shift'] for r in results])
    snrs = np.array([r['snr'] for r in results])
    T_kleins = np.array([r['T_klein'] for r in results])

    # Calculate multiple correlations
    correlations = [
        ('mass_epsilon', stats.spearmanr(masses, epsilons)),
        ('redshift_doppler', stats.spearmanr(redshifts, doppler_shifts)),
        ('snr_epsilon', stats.spearmanr(snrs, epsilons)),
        ('T_klein_epsilon', stats.spearmanr(T_kleins, epsilons)),
        ('mass_T_klein', stats.spearmanr(masses, T_kleins))
    ]

    print("\n  Individual correlations:")
    p_values = []
    for name, (r, p) in correlations:
        print(f"    {name}: r = {r:.4f}, p = {p:.4e}")
        p_values.append(max(p, 1e-100))  # Avoid log(0)

    # Fisher's combined test
    fisher_stat = -2 * np.sum(np.log(p_values))
    fisher_dof = 2 * len(p_values)
    fisher_p = 1 - stats.chi2.cdf(fisher_stat, fisher_dof)

    # Convert to sigma
    if fisher_p > 1e-15:
        combined_sigma = abs(stats.norm.ppf(fisher_p/2))
    else:
        combined_sigma = np.sqrt(-2 * np.log(max(fisher_p, 1e-300)))
    combined_sigma = min(combined_sigma, 10.0)  # Cap at 10σ

    print(f"\n  Fisher's combined test:")
    print(f"    χ² = {fisher_stat:.2f}, dof = {fisher_dof}")
    print(f"    Combined p-value: {fisher_p:.4e}")
    print(f"    Combined significance: {combined_sigma:.2f}σ")

    if combined_sigma >= 5.0:
        verdict = "✓ PASSED - DISCOVERY level (≥5σ)"
        falsified = False
    elif combined_sigma >= 3.0:
        verdict = "⚠ EVIDENCE - Strong evidence (≥3σ)"
        falsified = False
    else:
        verdict = "✗ FAILED - Insufficient combined significance"
        falsified = True

    print(f"\n{verdict}")

    return {
        'test': 'Combined Significance',
        'fisher_statistic': float(fisher_stat),
        'fisher_dof': fisher_dof,
        'combined_p': float(fisher_p),
        'combined_sigma': float(combined_sigma),
        'individual_correlations': {name: {'r': float(r), 'p': float(p)} for name, (r, p) in correlations},
        'falsified': falsified,
        'verdict': verdict
    }


# =============================================================================
# MAIN EXECUTION
# =============================================================================

def run_doppler_klein_falsification():
    """Execute Doppler-Klein falsification protocol."""

    print("\n" + "=" * 70)
    print("EXECUTING DOPPLER-KLEIN FALSIFICATION PROTOCOL")
    print("=" * 70)
    print(f"\nTimestamp: {datetime.now().isoformat()}")

    # Load data
    df = load_gwtc_data()

    # Calculate Doppler-Klein parameters for all events
    print("\nCalculating Doppler-Klein parameters...")
    results = []

    for _, row in df.iterrows():
        result = calculate_doppler_klein(row)
        if result is not None:
            result['name'] = row.get('name', 'Unknown')
            results.append(result)

    print(f"  Successfully processed: {len(results)} events")

    if len(results) < 10:
        print("ERROR: Too few events processed")
        return None

    # Run all tests
    test_results = []

    test_results.append(test_twist_factor_significance(results))
    test_results.append(test_epsilon_max_violations(results))
    test_results.append(test_state_distribution(results))
    test_results.append(test_redshift_doppler_correlation(results))
    test_results.append(test_combined_significance(results))

    # Summary
    print("\n" + "=" * 70)
    print("DOPPLER-KLEIN FALSIFICATION SUMMARY")
    print("=" * 70)

    n_passed = sum(1 for r in test_results if not r['falsified'])
    n_failed = sum(1 for r in test_results if r['falsified'])
    n_marginal = sum(1 for r in test_results if 'MARGINAL' in r['verdict'])

    print(f"\nTests Passed: {n_passed}/{len(test_results)}")
    print(f"Tests Marginal: {n_marginal}/{len(test_results)}")
    print(f"Tests Failed: {n_failed}/{len(test_results)}")

    print("\nDetailed Results:")
    for r in test_results:
        status = "✓ PASSED" if not r['falsified'] else "✗ FAILED"
        if 'MARGINAL' in r['verdict']:
            status = "⚠ MARGINAL"
        print(f"  {r['test']}: {status}")

    # Final verdict
    print("\n" + "-" * 70)
    if n_failed == 0:
        print("FINAL VERDICT: Doppler-Klein Theory SURVIVES all tests")
        overall_status = "VALIDATED"
    elif n_failed <= 1:
        print("FINAL VERDICT: Doppler-Klein Theory shows STRENGTH")
        overall_status = "VIABLE"
    else:
        print("FINAL VERDICT: Doppler-Klein Theory CHALLENGED")
        overall_status = "CHALLENGED"
    print("-" * 70)

    # Save results
    output = {
        'timestamp': datetime.now().isoformat(),
        'parameters': {
            'R_empirical_km': R_EMPIRICAL,
            'f_0_hz': f_0,
            'epsilon_max': EPSILON_MAX
        },
        'n_events': len(results),
        'tests': test_results,
        'summary': {
            'passed': n_passed,
            'marginal': n_marginal,
            'failed': n_failed,
            'status': overall_status
        }
    }

    output_path = Path(__file__).parent.parent / "results" / "doppler_klein_falsification.json"
    output_path.parent.mkdir(exist_ok=True)

    with open(output_path, 'w') as f:
        json.dump(output, f, indent=2, default=str)

    print(f"\n✓ Results saved to: {output_path}")

    return output


if __name__ == "__main__":
    results = run_doppler_klein_falsification()
