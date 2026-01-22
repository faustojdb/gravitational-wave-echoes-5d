#!/usr/bin/env python3
"""
DUAL RADIUS COMPARISON: 419 km (Fundamental) vs 8400 km (Empirical)
===================================================================

This script compares both Klein radius models against LIGO data and
recalculates predictions for Platypus Galaxies.

Key Question: Which radius has more predictive power?
- R = 419.3 km → f = 113.79 Hz (LIGO optimal)
- R = 8400 km → f = 5.68 Hz (sub-LIGO range)
"""

import numpy as np
import pandas as pd
from scipy import stats, constants
import json
from datetime import datetime
import os

# Physical constants
c = constants.c  # m/s
h = constants.h  # J·s
k_B = constants.k  # J/K
G = constants.G  # m³/kg/s²
M_sun = 1.989e30  # kg
m_e = constants.m_e  # electron mass

# ============================================================
# TWO COMPETING MODELS
# ============================================================

KLEIN_EMPIRICAL = {
    'name': 'Empirical (Original)',
    'R_km': 8400,
    'f_hz': c / (2 * np.pi * 8400e3),  # 5.68 Hz
    'origin': 'Fitted to GW150914 observations',
    'derivation': 'Empirical fitting',
}

KLEIN_FUNDAMENTAL = {
    'name': 'Fundamental (New)',
    'R_km': 419.3,
    'f_hz': c / (2 * np.pi * 419.3e3),  # 113.79 Hz
    'origin': 'Derived from first principles',
    'derivation': 'R = m_e*c² × exp(α⁻¹ × γ_holonomy)',
}


def calculate_klein_frequency(R_km):
    """Calculate Klein frequency from radius."""
    return c / (2 * np.pi * R_km * 1e3)


def resonance_factor(f_gw, f_klein, gamma=0.1):
    """Calculate resonance enhancement factor."""
    delta_f = abs(f_gw - f_klein) / f_klein
    return 1 / (1 + (delta_f / gamma)**2)


def gw_frequency_from_mass(M_total_solar):
    """Estimate GW frequency at merger from total mass."""
    M_total = M_total_solar * M_sun
    # f_gw ≈ c³ / (6^(3/2) × π × G × M)
    f_gw = c**3 / (6**(3/2) * np.pi * G * M_total)
    return f_gw


def load_gwtc_data():
    """Load GWTC catalog data."""
    catalog_path = os.path.join(
        os.path.dirname(__file__),
        '..', 'datos', 'gwtc4', 'gwtc_combined_latest.csv'
    )

    if os.path.exists(catalog_path):
        df = pd.read_csv(catalog_path)
        return df
    else:
        print(f"Warning: Catalog not found at {catalog_path}")
        return None


def analyze_ligo_with_both_radii():
    """
    Compare both Klein radius models against LIGO data.
    """
    print("=" * 70)
    print("📊 DUAL RADIUS ANALYSIS: 419 km vs 8400 km")
    print("=" * 70)

    df = load_gwtc_data()
    if df is None:
        return None

    # Calculate GW frequencies for all events
    results = []

    for _, row in df.iterrows():
        try:
            m1 = float(row['mass_1_source'])
            m2 = float(row['mass_2_source'])
            M_total = m1 + m2

            # GW frequency at merger
            f_gw = gw_frequency_from_mass(M_total)

            # Resonance with both models
            res_empirical = resonance_factor(f_gw, KLEIN_EMPIRICAL['f_hz'])
            res_fundamental = resonance_factor(f_gw, KLEIN_FUNDAMENTAL['f_hz'])

            results.append({
                'event': row.get('event_name', 'unknown'),
                'M_total': M_total,
                'f_gw': f_gw,
                'resonance_8400km': res_empirical,
                'resonance_419km': res_fundamental,
                'better_model': 'fundamental' if res_fundamental > res_empirical else 'empirical'
            })
        except (ValueError, TypeError):
            continue

    results_df = pd.DataFrame(results)

    # Statistics
    print(f"\n📈 Events analyzed: {len(results_df)}")
    print(f"\n🎯 Model Comparison:")

    # Resonance statistics
    print(f"\n   EMPIRICAL (8400 km, f={KLEIN_EMPIRICAL['f_hz']:.2f} Hz):")
    print(f"      Mean resonance: {results_df['resonance_8400km'].mean():.4f}")
    print(f"      Events in strong resonance (>0.5): {(results_df['resonance_8400km'] > 0.5).sum()}")
    print(f"      Events in perfect resonance (>0.9): {(results_df['resonance_8400km'] > 0.9).sum()}")

    print(f"\n   FUNDAMENTAL (419 km, f={KLEIN_FUNDAMENTAL['f_hz']:.2f} Hz):")
    print(f"      Mean resonance: {results_df['resonance_419km'].mean():.4f}")
    print(f"      Events in strong resonance (>0.5): {(results_df['resonance_419km'] > 0.5).sum()}")
    print(f"      Events in perfect resonance (>0.9): {(results_df['resonance_419km'] > 0.9).sum()}")

    # Which model wins more often?
    fundamental_wins = (results_df['better_model'] == 'fundamental').sum()
    empirical_wins = (results_df['better_model'] == 'empirical').sum()

    print(f"\n   🏆 Better resonance count:")
    print(f"      Fundamental (419 km) wins: {fundamental_wins} events ({100*fundamental_wins/len(results_df):.1f}%)")
    print(f"      Empirical (8400 km) wins: {empirical_wins} events ({100*empirical_wins/len(results_df):.1f}%)")

    # LIGO sensitivity analysis
    print(f"\n📡 LIGO Sensitivity Match:")
    ligo_min, ligo_max = 20, 2000  # Hz

    f_emp = KLEIN_EMPIRICAL['f_hz']
    f_fund = KLEIN_FUNDAMENTAL['f_hz']

    print(f"   LIGO sensitive range: {ligo_min}-{ligo_max} Hz")
    print(f"   Empirical f₀ = {f_emp:.2f} Hz → {'❌ OUTSIDE' if f_emp < ligo_min else '✅ INSIDE'} LIGO range")
    print(f"   Fundamental f₀ = {f_fund:.2f} Hz → {'❌ OUTSIDE' if f_fund < ligo_min else '✅ INSIDE'} LIGO range")

    # GW frequency distribution vs Klein frequencies
    gw_freqs = results_df['f_gw']
    print(f"\n   GW frequency distribution:")
    print(f"      Min: {gw_freqs.min():.1f} Hz")
    print(f"      Max: {gw_freqs.max():.1f} Hz")
    print(f"      Median: {gw_freqs.median():.1f} Hz")
    print(f"      Mean: {gw_freqs.mean():.1f} Hz")

    # Distance to Klein frequencies
    dist_to_emp = abs(gw_freqs - f_emp).mean()
    dist_to_fund = abs(gw_freqs - f_fund).mean()

    print(f"\n   Mean distance to Klein frequency:")
    print(f"      To 5.68 Hz (empirical): {dist_to_emp:.1f} Hz")
    print(f"      To 113.79 Hz (fundamental): {dist_to_fund:.1f} Hz")

    return results_df


def platypus_predictions_dual_radius():
    """
    Calculate Platypus Galaxy predictions with BOTH radii.
    """
    print("\n" + "=" * 70)
    print("🦆 PLATYPUS GALAXY PREDICTIONS: Dual Radius Analysis")
    print("=" * 70)

    z_platypus = 2.0  # Redshift of platypus galaxies

    # Evolution models for both radii
    # Using same evolutionary model but different R₀

    def R_klein_evolved(z, R0_km, alpha=0.41, z_act=1.4):
        """Klein radius at redshift z."""
        return R0_km * 1e3 * ((1 + z_act) / (1 + z))**alpha  # meters

    def f_klein_evolved(z, R0_km):
        """Klein frequency at redshift z."""
        R_z = R_klein_evolved(z, R0_km)
        return c / (2 * np.pi * R_z)

    print(f"\n📍 At Platypus Galaxy Redshift z = {z_platypus}:")

    # Empirical model
    R_emp_z2 = R_klein_evolved(z_platypus, 8400) / 1e3  # km
    f_emp_z2 = f_klein_evolved(z_platypus, 8400)

    # Fundamental model
    R_fund_z2 = R_klein_evolved(z_platypus, 419.3) / 1e3  # km
    f_fund_z2 = f_klein_evolved(z_platypus, 419.3)

    print(f"\n   EMPIRICAL MODEL (R₀ = 8400 km):")
    print(f"      R_Klein(z=2) = {R_emp_z2:.0f} km")
    print(f"      f_Klein(z=2) = {f_emp_z2:.2f} Hz")
    print(f"      Period = {1/f_emp_z2:.3f} s")

    print(f"\n   FUNDAMENTAL MODEL (R₀ = 419.3 km):")
    print(f"      R_Klein(z=2) = {R_fund_z2:.1f} km")
    print(f"      f_Klein(z=2) = {f_fund_z2:.2f} Hz")
    print(f"      Period = {1/f_fund_z2:.4f} s")

    # Key prediction: Line width (same physics, different scale)
    # The line width prediction is based on thermal + turbulent velocity
    # which doesn't depend directly on R_Klein, but on formation mechanism

    T_gas = 1e4  # K
    m_H = 1.67e-27  # kg
    v_thermal = np.sqrt(k_B * T_gas / m_H) / 1e3  # km/s

    print(f"\n📏 Spectral Line Width Prediction:")
    print(f"   (Based on silent formation - same for both models)")
    print(f"   σ_v (Klein silent) ≈ {v_thermal:.1f} km/s")
    print(f"   σ_v (Merger typical) ≈ 150 km/s")
    print(f"   Ratio: ~{150/v_thermal:.0f}x narrower for Klein")

    # The KEY difference: observable signatures
    print(f"\n🔬 KEY OBSERVABLE DIFFERENCES:")
    print(f"\n   If EMPIRICAL (8400 km) is correct:")
    print(f"      - Klein effects at f ~ {f_emp_z2:.1f} Hz (VERY low frequency)")
    print(f"      - Hard to detect with current instruments")
    print(f"      - Period ~ {1/f_emp_z2*1000:.0f} ms")

    print(f"\n   If FUNDAMENTAL (419 km) is correct:")
    print(f"      - Klein effects at f ~ {f_fund_z2:.1f} Hz")
    print(f"      - Potentially detectable in radio/IR observations")
    print(f"      - Period ~ {1/f_fund_z2*1000:.1f} ms")

    # Formation epoch prediction
    print(f"\n⏰ Formation Epoch Prediction:")

    z_range = np.linspace(0.5, 5, 50)

    def formation_efficiency(z, z_act=1.4):
        """Peak efficiency around activation era."""
        z_peak = z_act + 1.0
        width = 1.5
        return np.exp(-((z - z_peak)**2) / (2 * width**2))

    efficiencies = [formation_efficiency(z) for z in z_range]
    z_peak = z_range[np.argmax(efficiencies)]

    print(f"   Peak formation efficiency at z ≈ {z_peak:.1f}")
    print(f"   (Same for both models - depends on z_activation, not R₀)")

    return {
        'z': z_platypus,
        'empirical': {
            'R_km': R_emp_z2,
            'f_hz': f_emp_z2,
            'period_s': 1/f_emp_z2
        },
        'fundamental': {
            'R_km': R_fund_z2,
            'f_hz': f_fund_z2,
            'period_s': 1/f_fund_z2
        },
        'line_width_prediction': {
            'klein_kms': v_thermal,
            'merger_kms': 150,
            'ratio': 150/v_thermal
        },
        'peak_formation_z': z_peak
    }


def critical_analysis():
    """
    Critical analysis of which model is more likely correct.
    """
    print("\n" + "=" * 70)
    print("⚖️  CRITICAL ANALYSIS: Which Model is Correct?")
    print("=" * 70)

    print("""
    ┌─────────────────────────────────────────────────────────────────┐
    │                    EMPIRICAL (8400 km)                         │
    ├─────────────────────────────────────────────────────────────────┤
    │ ✅ Strengths:                                                   │
    │    - Originally fitted to GW150914 observations                │
    │    - Used in all previous analyses                             │
    │    - Correlations found (r ~ 0.9)                              │
    │                                                                 │
    │ ❌ Weaknesses:                                                  │
    │    - f₀ = 5.68 Hz is BELOW LIGO sensitivity (20-2000 Hz)       │
    │    - No derivation from first principles                       │
    │    - R₅D derivation was circular                               │
    │    - Blind prediction test showed degradation (3.77σ)          │
    └─────────────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────────────┐
    │                  FUNDAMENTAL (419.3 km)                        │
    ├─────────────────────────────────────────────────────────────────┤
    │ ✅ Strengths:                                                   │
    │    - Derived from first principles (m_e, α, γ_holonomy)        │
    │    - f₀ = 113.79 Hz is INSIDE LIGO optimal range               │
    │    - 13.9σ significance claimed (but see weaknesses)           │
    │    - No free parameters - all from physics constants           │
    │                                                                 │
    │ ❌ Weaknesses:                                                  │
    │    - Statistical validation "methodologically invalid"         │
    │    - Factor of 20x different from empirical                    │
    │    - γ_holonomy = 0.336 derivation needs verification          │
    │    - Discards all previous empirical work                      │
    └─────────────────────────────────────────────────────────────────┘
    """)

    print("🎯 KEY DISCRIMINATING TEST:")
    print("""
    The models predict VERY different Klein frequencies:

    - Empirical:    f₀ = 5.68 Hz   (period = 176 ms)
    - Fundamental:  f₀ = 113.79 Hz (period = 8.8 ms)

    If Klein effects are real, they should show up at ONE of these
    frequencies, not both. The question is: which one?

    CRITICAL OBSERVATION:
    - LIGO is sensitive to 20-2000 Hz
    - 5.68 Hz is OUTSIDE this range
    - 113.79 Hz is INSIDE this range

    If LIGO detects Klein signatures, the 419 km model is more
    plausible because LIGO literally cannot see 5.68 Hz.

    However, the previous correlations (r ~ 0.9) were found using
    derived parameters (ε, E_rad), not direct frequency detection.
    The correlations might be real even if f₀ interpretation is wrong.
    """)

    return {
        'empirical_f_hz': 5.68,
        'fundamental_f_hz': 113.79,
        'ligo_range': (20, 2000),
        'empirical_in_ligo': False,
        'fundamental_in_ligo': True
    }


def main():
    """Main execution."""
    print("🔬 KLEIN THEORY: DUAL RADIUS INVESTIGATION")
    print("=" * 70)
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 70)

    # 1. Compare both models with LIGO data
    ligo_results = analyze_ligo_with_both_radii()

    # 2. Platypus galaxy predictions
    platypus_results = platypus_predictions_dual_radius()

    # 3. Critical analysis
    critical_results = critical_analysis()

    # Save results
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'resultados', 'dual_radius_analysis')
    os.makedirs(output_dir, exist_ok=True)

    results = {
        'timestamp': datetime.now().isoformat(),
        'models_compared': {
            'empirical': KLEIN_EMPIRICAL,
            'fundamental': KLEIN_FUNDAMENTAL
        },
        'platypus_predictions': platypus_results,
        'critical_analysis': critical_results,
        'conclusion': {
            'key_difference': 'f₀ = 5.68 Hz vs 113.79 Hz (factor 20x)',
            'ligo_sensitivity': 'Only fundamental (113.79 Hz) is in LIGO range',
            'recommendation': 'Both models need independent validation; platypus galaxies may help discriminate'
        }
    }

    output_path = os.path.join(output_dir, 'dual_radius_comparison.json')
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2, default=str)

    print(f"\n💾 Results saved to: {output_path}")

    return results


if __name__ == "__main__":
    results = main()
