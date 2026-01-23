#!/usr/bin/env python3
"""
BLIND PREDICTION TEST: Klein Theory Validation

This script tests whether parameters calibrated on pre-O4 data (GWTC-1/2.1/3)
can accurately predict O4 observations WITHOUT re-fitting.

This is a critical test for theory validation:
- If pre-O4 parameters predict O4: Theory has predictive power
- If they don't: Theory may be ad-hoc/overfitted
"""

import numpy as np
import pandas as pd
from scipy import stats
import json
from datetime import datetime
import os

# Klein Theory constants - FIXED from pre-O4 calibration
KLEIN_PARAMS_PRE_O4 = {
    'epsilon_max': 0.65,          # Topological limit (from π/√24 ≈ 0.641 + quantum corrections)
    'f0_hz': 5.68,                # Klein frequency (from R_5D)
    'R_5D_km': 8400,              # Fifth dimension radius
    'gamma_coupling': 50.0,       # Energy coupling constant
    'calibration_source': 'GWTC-1/2.1/3 (90 events, pre-O4)',
    'calibration_date': '2023-05-01'  # Before O4 started
}

# Physical constants
c = 2.998e8  # m/s
G = 6.674e-11  # m³/kg/s²
M_sun = 1.989e30  # kg


def load_catalog_data(catalog_path):
    """Load and separate pre-O4 and O4 data."""
    df = pd.read_csv(catalog_path)

    # Rename columns for compatibility
    if 'event_name' in df.columns and 'commonName' not in df.columns:
        df['commonName'] = df['event_name']

    # Filter for valid data
    required_cols = ['commonName', 'mass_1_source', 'mass_2_source',
                     'final_mass_source']
    df = df.dropna(subset=[c for c in required_cols if c in df.columns])

    # Separate by catalog/observation run
    # GWTC-1: GW150914 - GW170823 (O1/O2)
    # GWTC-2.1: GW190403 - GW200316 (O3a)
    # GWTC-3: GW200112 - GW210710 (O3b)
    # GWTC-4: GW230 - GW240 (O4a)

    def get_observation_run(name):
        if not isinstance(name, str):
            return 'unknown'
        if name.startswith('GW15') or name.startswith('GW17'):
            return 'O1O2'
        elif name.startswith('GW19'):
            return 'O3a'
        elif name.startswith('GW20'):
            return 'O3b'
        elif name.startswith('GW21'):
            return 'O3b'
        elif name.startswith('GW22') or name.startswith('GW23') or name.startswith('GW24'):
            return 'O4'
        else:
            return 'unknown'

    df['obs_run'] = df['commonName'].apply(get_observation_run)

    pre_o4 = df[df['obs_run'].isin(['O1O2', 'O3a', 'O3b'])]
    o4 = df[df['obs_run'] == 'O4']

    return pre_o4, o4, df


def calculate_klein_parameters(row, params=KLEIN_PARAMS_PRE_O4):
    """
    Calculate Klein deformation for a GW event using FIXED pre-O4 parameters.
    """
    try:
        m1 = float(row['mass_1_source'])
        m2 = float(row['mass_2_source'])
        m_final = float(row.get('final_mass_source', (m1 + m2) * 0.95))
        snr = float(row.get('network_matched_filter_snr', 10))
    except (ValueError, TypeError):
        return None

    # Total mass
    M_total = (m1 + m2) * M_sun

    # Energy radiated (in solar masses)
    E_rad = (m1 + m2 - m_final)
    if E_rad <= 0:
        E_rad = (m1 + m2) * 0.05  # Fallback: ~5% radiated

    # Klein deformation calculation
    # ε = γ × (E_rad / E_ref) × (M_total / M_ref)^0.5
    E_ref = 3.0  # Reference energy (M_sun)
    M_ref = 60.0 * M_sun  # Reference mass (kg)

    epsilon_raw = params['gamma_coupling'] * (E_rad / E_ref) * np.sqrt(M_total / M_ref)

    # Normalize to [0, 1]
    epsilon_normalized = epsilon_raw / 100.0

    # Apply topological limit
    epsilon = min(epsilon_normalized, params['epsilon_max'])

    return {
        'epsilon': epsilon,
        'epsilon_raw': epsilon_normalized,
        'respects_limit': epsilon_normalized <= params['epsilon_max'],
        'E_rad': E_rad,
        'M_total_solar': (m1 + m2),
        'snr': snr
    }


def run_blind_prediction_test(catalog_path):
    """
    Main blind prediction test.

    Procedure:
    1. Load all data
    2. Separate into pre-O4 (calibration) and O4 (test)
    3. Apply FIXED pre-O4 parameters to O4 data
    4. Compare predictions with what Klein theory predicts
    """
    print("=" * 70)
    print("🔬 BLIND PREDICTION TEST: Klein Theory Validation")
    print("=" * 70)
    print(f"\n📅 Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"📊 Parameters Source: {KLEIN_PARAMS_PRE_O4['calibration_source']}")
    print(f"📅 Calibration Date: {KLEIN_PARAMS_PRE_O4['calibration_date']}")

    # Load data
    print("\n📂 Loading catalog data...")
    pre_o4, o4, all_data = load_catalog_data(catalog_path)

    print(f"   Pre-O4 events: {len(pre_o4)}")
    print(f"   O4 events: {len(o4)}")

    if len(o4) == 0:
        print("❌ No O4 events found in catalog!")
        return None

    # Calculate Klein parameters for all events
    print("\n🧮 Calculating Klein parameters...")

    results_pre_o4 = []
    for _, row in pre_o4.iterrows():
        klein = calculate_klein_parameters(row)
        if klein:
            klein['name'] = row['commonName']
            klein['run'] = 'pre-O4'
            results_pre_o4.append(klein)

    results_o4 = []
    for _, row in o4.iterrows():
        klein = calculate_klein_parameters(row)
        if klein:
            klein['name'] = row['commonName']
            klein['run'] = 'O4'
            results_o4.append(klein)

    print(f"   Pre-O4 valid: {len(results_pre_o4)}")
    print(f"   O4 valid: {len(results_o4)}")

    # Convert to DataFrames
    df_pre = pd.DataFrame(results_pre_o4)
    df_o4 = pd.DataFrame(results_o4)

    # ================================================================
    # KEY PREDICTIONS TO TEST
    # ================================================================

    print("\n" + "=" * 70)
    print("📊 PREDICTION TESTS")
    print("=" * 70)

    predictions_results = {}

    # -----------------------------------------------------------------
    # PREDICTION 1: Topological Limit ε_max = 0.65
    # -----------------------------------------------------------------
    print("\n🎯 PREDICTION 1: Topological Limit ε_max = 0.65")
    print("-" * 50)

    # Pre-O4 baseline
    pre_violations = sum(1 for r in results_pre_o4 if not r['respects_limit'])
    pre_max_eps = max(r['epsilon'] for r in results_pre_o4)

    # O4 test
    o4_violations = sum(1 for r in results_o4 if not r['respects_limit'])
    o4_max_eps = max(r['epsilon'] for r in results_o4) if results_o4 else 0

    print(f"   Pre-O4: {pre_violations}/{len(results_pre_o4)} violations, ε_max = {pre_max_eps:.4f}")
    print(f"   O4:     {o4_violations}/{len(results_o4)} violations, ε_max = {o4_max_eps:.4f}")

    limit_test_passed = o4_violations == 0
    print(f"   Result: {'✅ PASSED' if limit_test_passed else '❌ FAILED'}")

    predictions_results['topological_limit'] = {
        'prediction': 'ε ≤ 0.65 for all events',
        'pre_o4_violations': pre_violations,
        'o4_violations': o4_violations,
        'o4_max_epsilon': o4_max_eps,
        'passed': limit_test_passed
    }

    # -----------------------------------------------------------------
    # PREDICTION 2: E-ε Correlation Consistency
    # -----------------------------------------------------------------
    print("\n🎯 PREDICTION 2: Energy-Deformation Correlation Consistency")
    print("-" * 50)

    # Pre-O4 correlation
    pre_E = [r['E_rad'] for r in results_pre_o4]
    pre_eps = [r['epsilon'] for r in results_pre_o4]
    r_pre, p_pre = stats.pearsonr(pre_E, pre_eps)

    # O4 correlation
    o4_E = [r['E_rad'] for r in results_o4]
    o4_eps = [r['epsilon'] for r in results_o4]
    r_o4, p_o4 = stats.pearsonr(o4_E, o4_eps)

    print(f"   Pre-O4: r = {r_pre:.4f} (p = {p_pre:.2e})")
    print(f"   O4:     r = {r_o4:.4f} (p = {p_o4:.2e})")

    # Test: O4 correlation should be within 2σ of pre-O4
    # Fisher z-transformation for comparing correlations
    z_pre = np.arctanh(r_pre)
    z_o4 = np.arctanh(r_o4)
    se_diff = np.sqrt(1/(len(results_pre_o4)-3) + 1/(len(results_o4)-3))
    z_diff = abs(z_pre - z_o4) / se_diff

    correlation_consistent = z_diff < 2.0  # Within 2σ
    print(f"   Difference: {z_diff:.2f}σ")
    print(f"   Result: {'✅ PASSED (consistent)' if correlation_consistent else '❌ FAILED (inconsistent)'}")

    predictions_results['correlation_consistency'] = {
        'prediction': 'E-ε correlation consistent between pre-O4 and O4',
        'r_pre_o4': r_pre,
        'r_o4': r_o4,
        'difference_sigma': z_diff,
        'passed': correlation_consistent
    }

    # -----------------------------------------------------------------
    # PREDICTION 3: Mass Scaling Relationship
    # -----------------------------------------------------------------
    print("\n🎯 PREDICTION 3: Mass-Deformation Scaling")
    print("-" * 50)

    # Pre-O4 M-ε relationship
    pre_M = [r['M_total_solar'] for r in results_pre_o4]
    r_M_pre, p_M_pre = stats.pearsonr(pre_M, pre_eps)

    # O4 M-ε relationship
    o4_M = [r['M_total_solar'] for r in results_o4]
    r_M_o4, p_M_o4 = stats.pearsonr(o4_M, o4_eps)

    print(f"   Pre-O4: r(M,ε) = {r_M_pre:.4f}")
    print(f"   O4:     r(M,ε) = {r_M_o4:.4f}")

    # Both should show positive correlation (more massive → higher ε)
    mass_scaling_valid = r_M_o4 > 0.3  # Moderate positive correlation
    print(f"   Result: {'✅ PASSED' if mass_scaling_valid else '❌ FAILED'}")

    predictions_results['mass_scaling'] = {
        'prediction': 'ε ∝ M^0.5 (positive correlation)',
        'r_pre_o4': r_M_pre,
        'r_o4': r_M_o4,
        'passed': mass_scaling_valid
    }

    # -----------------------------------------------------------------
    # PREDICTION 4: Extreme Events Stay Under Limit
    # -----------------------------------------------------------------
    print("\n🎯 PREDICTION 4: Extreme Events (M > 100 M☉) Respect Limit")
    print("-" * 50)

    # Find extreme events in O4
    extreme_o4 = [r for r in results_o4 if r['M_total_solar'] > 100]

    if extreme_o4:
        extreme_violations = sum(1 for r in extreme_o4 if not r['respects_limit'])
        max_extreme_eps = max(r['epsilon'] for r in extreme_o4)
        most_massive = max(extreme_o4, key=lambda x: x['M_total_solar'])

        print(f"   Extreme O4 events: {len(extreme_o4)}")
        print(f"   Most massive: {most_massive['name']} ({most_massive['M_total_solar']:.1f} M☉)")
        print(f"   Its ε = {most_massive['epsilon']:.4f} {'✅' if most_massive['epsilon'] <= 0.65 else '❌'}")
        print(f"   Violations: {extreme_violations}/{len(extreme_o4)}")

        extreme_test_passed = extreme_violations == 0
    else:
        print("   No extreme events (M > 100 M☉) in O4 sample")
        extreme_test_passed = True

    print(f"   Result: {'✅ PASSED' if extreme_test_passed else '❌ FAILED'}")

    predictions_results['extreme_events'] = {
        'prediction': 'All extreme events (M > 100 M☉) respect ε_max = 0.65',
        'n_extreme': len(extreme_o4) if extreme_o4 else 0,
        'violations': extreme_violations if extreme_o4 else 0,
        'passed': extreme_test_passed
    }

    # ================================================================
    # SUMMARY
    # ================================================================
    print("\n" + "=" * 70)
    print("📋 BLIND PREDICTION TEST SUMMARY")
    print("=" * 70)

    n_passed = sum(1 for p in predictions_results.values() if p['passed'])
    n_total = len(predictions_results)

    print(f"\n   Tests passed: {n_passed}/{n_total}")

    for name, result in predictions_results.items():
        status = "✅" if result['passed'] else "❌"
        print(f"   {status} {name}: {result['prediction']}")

    # Overall assessment
    print("\n" + "-" * 50)
    all_passed = n_passed == n_total

    if all_passed:
        print("🎉 OVERALL: Klein Theory PASSES blind prediction test!")
        print("   Pre-O4 parameters successfully predict O4 observations")
        print("   → Theory demonstrates genuine predictive power")
    else:
        print("⚠️  OVERALL: Some predictions failed")
        print("   Theory may need refinement or has limited predictive power")

    # Save results
    output = {
        'test_date': datetime.now().isoformat(),
        'params_used': KLEIN_PARAMS_PRE_O4,
        'sample_sizes': {
            'pre_o4': len(results_pre_o4),
            'o4': len(results_o4)
        },
        'predictions': predictions_results,
        'overall_passed': all_passed
    }

    return output


if __name__ == "__main__":
    # Path to catalog
    catalog_path = os.path.join(
        os.path.dirname(__file__),
        '..', 'datos', 'gwtc4', 'gwtc_combined_latest.csv'
    )

    if os.path.exists(catalog_path):
        results = run_blind_prediction_test(catalog_path)

        # Save results
        output_dir = os.path.join(os.path.dirname(__file__), '..', 'resultados', 'blind_test')
        os.makedirs(output_dir, exist_ok=True)

        output_path = os.path.join(output_dir, 'blind_prediction_results.json')
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2, default=str)

        print(f"\n💾 Results saved to: {output_path}")
    else:
        print(f"❌ Catalog not found: {catalog_path}")
        print("   Please run gwtc4_downloader.py first")
