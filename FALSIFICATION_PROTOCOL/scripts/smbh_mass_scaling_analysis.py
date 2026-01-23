#!/usr/bin/env python3
"""
SMBH MASS SCALING ANALYSIS FOR KLEIN THEORY
============================================

Key Question: Does Klein theory break down when R_Schwarzschild >> R_Klein?

Physics:
- R_Klein = 8400 km (validated at 10σ)
- R_Schwarzschild = 3 × M_solar (km)
- M_critical ≈ 2800 M☉ where R_s ≈ R_Klein

If Klein works via extra-dimensional resonance at R_Klein,
what happens when the black hole is LARGER than the Klein dimension?

Author: Klein Theory Team
Date: January 2026
"""

import numpy as np
import pandas as pd
from pathlib import Path
from scipy import stats
from scipy.optimize import curve_fit
import json
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# =============================================================================
# PHYSICAL CONSTANTS AND KLEIN PARAMETERS
# =============================================================================

c = 299792.458  # km/s
G = 6.674e-11   # m³/kg/s²
M_sun = 1.989e30  # kg

# Klein parameters (validated 10σ)
R_KLEIN = 8400  # km
f_0 = 5.68  # Hz
EPSILON_MAX = 0.65

# Critical mass where R_s = R_Klein
# R_s = 2GM/c² ≈ 3 × M_solar (km)
R_S_PER_SOLAR_MASS = 2.95  # km per solar mass
M_CRITICAL = R_KLEIN / R_S_PER_SOLAR_MASS  # ≈ 2847 M☉

print("=" * 70)
print("SMBH MASS SCALING ANALYSIS")
print("=" * 70)
print(f"\nPhysical Parameters:")
print(f"  R_Klein = {R_KLEIN} km")
print(f"  R_s per M☉ = {R_S_PER_SOLAR_MASS} km")
print(f"  M_critical = {M_CRITICAL:.0f} M☉ (where R_s = R_Klein)")
print(f"\nBelow M_critical: R_s < R_Klein → Klein should work")
print(f"Above M_critical: R_s > R_Klein → Klein might break down")

# =============================================================================
# LOAD DATA
# =============================================================================

def load_gwtc_data():
    """Load GWTC catalog."""
    csv_path = Path(__file__).parent.parent.parent / "FUNDAMENTAL_RADIUS_INVESTIGATION" / "5_Code" / "data" / "events.csv"

    if csv_path.exists():
        df = pd.read_csv(csv_path)
        print(f"\n✓ Loaded {len(df)} events from GWTC")
        return df

    raise FileNotFoundError("GWTC data not found")

# =============================================================================
# CALCULATE KLEIN FEATURES BY MASS BIN
# =============================================================================

def calculate_klein_features(df):
    """Calculate Klein-specific features for each event."""

    features = pd.DataFrame()

    # Basic masses
    features['M1'] = df['mass_1_source'].fillna(30)
    features['M2'] = df['mass_2_source'].fillna(20)
    features['M_total'] = df['total_mass_source'].fillna(features['M1'] + features['M2'])
    features['M_chirp'] = df['chirp_mass_source'].fillna(
        (features['M1'] * features['M2'])**(3/5) / (features['M1'] + features['M2'])**(1/5)
    )

    # Schwarzschild radius of merged BH
    features['R_s'] = R_S_PER_SOLAR_MASS * features['M_total']  # km

    # Ratio: how many Klein radii fit in the Schwarzschild radius?
    features['R_s_over_R_Klein'] = features['R_s'] / R_KLEIN

    # Is this event above or below critical mass?
    features['above_critical'] = features['M_total'] > M_CRITICAL

    # Other observables
    features['d_L'] = df['luminosity_distance'].fillna(1000)
    features['z'] = df['redshift'].fillna(features['d_L'] * 70 / c / 1000)
    features['SNR'] = df['network_matched_filter_snr'].fillna(10)
    features['chi_eff'] = df['chi_eff'].fillna(0)

    # Merger frequency
    features['f_merger'] = 4400 * (30 / features['M_total'])

    # Klein features
    features['f_ratio'] = features['f_merger'] / f_0
    features['n_harmonic'] = np.round(features['f_ratio'])
    features['harmonic_deviation'] = np.abs(features['f_ratio'] - features['n_harmonic'])

    # Klein deformation estimate
    M_ref, d_ref = 60, 500
    features['epsilon_est'] = 0.35 * (features['M_total']/M_ref)**0.2 * (d_ref/features['d_L'])**0.3
    features['epsilon_est'] = features['epsilon_est'].clip(0, EPSILON_MAX)

    # Resonance score
    features['resonance_score'] = np.exp(-features['harmonic_deviation']**2 / 0.1)

    # Doppler-Klein twist factor
    v_hubble = 70 * features['d_L']
    features['beta'] = (v_hubble / c).clip(0, 0.15)
    features['twist_factor'] = 1 + features['beta'] * 0.18 * np.sign(features['chi_eff'])

    # Expected SNR (standard GR model)
    features['SNR_expected'] = (features['M_chirp']**(5/6) / features['d_L']) * 1000
    features['SNR_expected'] = features['SNR_expected'] / features['SNR_expected'].median() * features['SNR'].median()

    # SNR residual (observed - expected)
    features['SNR_residual'] = features['SNR'] - features['SNR_expected']
    features['SNR_residual_norm'] = features['SNR_residual'] / features['SNR_expected']

    # Event name if available
    if 'name' in df.columns:
        features['name'] = df['name']
    elif 'commonName' in df.columns:
        features['name'] = df['commonName']
    else:
        features['name'] = [f'Event_{i}' for i in range(len(df))]

    return features.fillna(features.median(numeric_only=True))

# =============================================================================
# ANALYSIS 1: KLEIN CORRELATIONS BY MASS BIN
# =============================================================================

def analyze_by_mass_bins(features):
    """Calculate Klein correlations for different mass ranges."""

    print("\n" + "=" * 70)
    print("ANALYSIS 1: KLEIN CORRELATIONS BY MASS BIN")
    print("=" * 70)

    # Define mass bins
    mass_bins = [
        (0, 30, "Light stellar (< 30 M☉)"),
        (30, 60, "Medium stellar (30-60 M☉)"),
        (60, 100, "Heavy stellar (60-100 M☉)"),
        (100, 200, "Very heavy (100-200 M☉)"),
        (200, 500, "Light IMBH (200-500 M☉)"),
        (500, float('inf'), "IMBH+ (> 500 M☉)")
    ]

    results = []

    for m_min, m_max, label in mass_bins:
        mask = (features['M_total'] >= m_min) & (features['M_total'] < m_max)
        n_events = mask.sum()

        if n_events < 5:
            print(f"\n  {label}: {n_events} events (insufficient)")
            results.append({
                'bin': label,
                'm_min': m_min,
                'm_max': m_max if m_max != float('inf') else 9999,
                'n_events': int(n_events),
                'sufficient_data': False
            })
            continue

        subset = features[mask]

        # Mean R_s / R_Klein ratio for this bin
        mean_ratio = subset['R_s_over_R_Klein'].mean()

        # Klein correlations
        corr_resonance = stats.spearmanr(subset['SNR_residual_norm'], subset['resonance_score'])
        corr_epsilon = stats.spearmanr(subset['SNR_residual_norm'], subset['epsilon_est'])
        corr_harmonic = stats.spearmanr(subset['SNR_residual_norm'], subset['harmonic_deviation'])

        # Average Klein metrics
        mean_resonance = subset['resonance_score'].mean()
        mean_epsilon = subset['epsilon_est'].mean()

        result = {
            'bin': label,
            'm_min': m_min,
            'm_max': m_max if m_max != float('inf') else 9999,
            'n_events': int(n_events),
            'sufficient_data': True,
            'mean_M_total': float(subset['M_total'].mean()),
            'mean_R_s': float(subset['R_s'].mean()),
            'mean_R_s_over_R_Klein': float(mean_ratio),
            'mean_resonance_score': float(mean_resonance),
            'mean_epsilon': float(mean_epsilon),
            'correlations': {
                'SNR_vs_resonance': {'r': float(corr_resonance[0]), 'p': float(corr_resonance[1])},
                'SNR_vs_epsilon': {'r': float(corr_epsilon[0]), 'p': float(corr_epsilon[1])},
                'SNR_vs_harmonic_dev': {'r': float(corr_harmonic[0]), 'p': float(corr_harmonic[1])}
            }
        }

        results.append(result)

        # Print results
        print(f"\n  {label}: {n_events} events")
        print(f"    Mean M_total = {subset['M_total'].mean():.1f} M☉")
        print(f"    Mean R_s = {subset['R_s'].mean():.1f} km")
        print(f"    R_s/R_Klein = {mean_ratio:.3f}")
        print(f"    Correlations:")
        print(f"      SNR vs resonance: r={corr_resonance[0]:+.3f}, p={corr_resonance[1]:.4f}")
        print(f"      SNR vs epsilon:   r={corr_epsilon[0]:+.3f}, p={corr_epsilon[1]:.4f}")

    return results

# =============================================================================
# ANALYSIS 2: SEARCH FOR M_CRITICAL TRANSITION
# =============================================================================

def search_for_transition(features):
    """Look for a transition in Klein correlations near M_critical."""

    print("\n" + "=" * 70)
    print("ANALYSIS 2: SEARCH FOR MASS TRANSITION")
    print("=" * 70)
    print(f"\nSearching for transition near M_critical = {M_CRITICAL:.0f} M☉")

    # Sort by mass
    sorted_features = features.sort_values('M_total').reset_index(drop=True)

    # Calculate rolling correlations
    window_size = 30  # Events per window

    if len(sorted_features) < window_size * 2:
        print(f"\n  ⚠ Not enough events ({len(sorted_features)}) for rolling analysis")
        return {'sufficient_data': False}

    rolling_results = []

    for i in range(0, len(sorted_features) - window_size, 5):
        window = sorted_features.iloc[i:i+window_size]

        m_center = window['M_total'].median()

        # Correlation in this window
        corr = stats.spearmanr(window['SNR_residual_norm'], window['resonance_score'])

        rolling_results.append({
            'M_center': float(m_center),
            'r_correlation': float(corr[0]),
            'p_value': float(corr[1]),
            'n_events': len(window)
        })

    # Convert to array for analysis
    m_centers = np.array([r['M_center'] for r in rolling_results])
    correlations = np.array([r['r_correlation'] for r in rolling_results])

    # Look for sign change or significant drop
    # Hypothesis: correlation should weaken (become less negative or positive)
    # as mass increases past M_critical

    below_critical = m_centers < M_CRITICAL
    above_critical = m_centers >= M_CRITICAL

    if below_critical.sum() > 0 and above_critical.sum() > 0:
        mean_corr_below = correlations[below_critical].mean()
        mean_corr_above = correlations[above_critical].mean()

        print(f"\n  Mean correlation below M_critical: r = {mean_corr_below:+.3f}")
        print(f"  Mean correlation above M_critical: r = {mean_corr_above:+.3f}")
        print(f"  Difference: Δr = {mean_corr_above - mean_corr_below:+.3f}")

        # Statistical test: is the difference significant?
        t_stat, p_value = stats.ttest_ind(
            correlations[below_critical],
            correlations[above_critical]
        )

        print(f"  T-test: t={t_stat:.2f}, p={p_value:.4f}")

        if p_value < 0.05:
            if mean_corr_above > mean_corr_below:
                verdict = "✓ TRANSITION DETECTED: Klein correlation WEAKENS above M_critical"
            else:
                verdict = "⚠ TRANSITION DETECTED: Klein correlation STRENGTHENS above M_critical"
        else:
            verdict = "✗ NO SIGNIFICANT TRANSITION at M_critical"

        print(f"\n  {verdict}")

        return {
            'sufficient_data': True,
            'M_critical': float(M_CRITICAL),
            'mean_corr_below': float(mean_corr_below),
            'mean_corr_above': float(mean_corr_above),
            'correlation_change': float(mean_corr_above - mean_corr_below),
            't_statistic': float(t_stat),
            'p_value': float(p_value),
            'rolling_data': rolling_results,
            'verdict': verdict
        }
    else:
        print("\n  ⚠ All events are on one side of M_critical - cannot test transition")
        return {
            'sufficient_data': False,
            'reason': 'All events on one side of M_critical'
        }

# =============================================================================
# ANALYSIS 3: MASSIVE EVENT ANALYSIS
# =============================================================================

def analyze_massive_events(features):
    """Specifically analyze the most massive events."""

    print("\n" + "=" * 70)
    print("ANALYSIS 3: MOST MASSIVE EVENTS")
    print("=" * 70)

    # Get top 10 most massive events
    top_massive = features.nlargest(10, 'M_total')

    print("\n  Top 10 most massive events:")
    print("-" * 80)

    massive_events = []

    for idx, row in top_massive.iterrows():
        name = row['name'] if isinstance(row['name'], str) else f"Event_{idx}"

        event_info = {
            'name': name,
            'M_total': float(row['M_total']),
            'R_s': float(row['R_s']),
            'R_s_over_R_Klein': float(row['R_s_over_R_Klein']),
            'SNR': float(row['SNR']),
            'SNR_residual_norm': float(row['SNR_residual_norm']),
            'resonance_score': float(row['resonance_score']),
            'epsilon_est': float(row['epsilon_est']),
            'above_critical': bool(row['above_critical'])
        }

        massive_events.append(event_info)

        status = "🔴 ABOVE" if row['above_critical'] else "🟢 BELOW"
        print(f"  {name:20} M={row['M_total']:.1f} M☉  R_s/R_Klein={row['R_s_over_R_Klein']:.3f}  {status}")

    # Specific look at GW190521-like events (if any)
    # GW190521 was ~150 M☉ total mass
    gw190521_candidates = features[features['M_total'] > 140]

    if len(gw190521_candidates) > 0:
        print(f"\n  GW190521-class events (M > 140 M☉): {len(gw190521_candidates)}")

        for idx, row in gw190521_candidates.iterrows():
            name = row['name'] if isinstance(row['name'], str) else f"Event_{idx}"
            print(f"\n    {name}:")
            print(f"      M_total = {row['M_total']:.1f} M☉")
            print(f"      R_s = {row['R_s']:.1f} km ({row['R_s_over_R_Klein']:.2f} × R_Klein)")
            print(f"      SNR residual = {row['SNR_residual_norm']:+.2f} (expected: {row['SNR_expected']:.1f})")
            print(f"      Resonance score = {row['resonance_score']:.3f}")

            if row['SNR_residual_norm'] > 0.2:
                print(f"      → SNR HIGHER than expected (Klein enhancement?)")
            elif row['SNR_residual_norm'] < -0.2:
                print(f"      → SNR LOWER than expected (Klein suppression?)")
            else:
                print(f"      → SNR consistent with expectation")
    else:
        print("\n  No GW190521-class events (M > 140 M☉) in dataset")

    return {
        'top_10_massive': massive_events,
        'n_above_critical': int(features['above_critical'].sum()),
        'n_total': len(features),
        'fraction_above_critical': float(features['above_critical'].mean())
    }

# =============================================================================
# ANALYSIS 4: FIT TRANSITION MODEL
# =============================================================================

def fit_transition_model(features):
    """Fit a model for how Klein effects scale with mass."""

    print("\n" + "=" * 70)
    print("ANALYSIS 4: KLEIN SCALING MODEL")
    print("=" * 70)

    # Hypothesis 1: Klein effect is constant (no mass dependence)
    # Hypothesis 2: Klein effect decreases above M_critical

    # Model: Klein_effect = A / (1 + (M/M_c)^n)
    # This captures suppression above critical mass

    def klein_suppression_model(M, A, M_c, n):
        return A / (1 + (M / M_c)**n)

    # Use resonance_score as proxy for Klein effect
    M = features['M_total'].values
    klein_effect = features['resonance_score'].values

    try:
        # Fit the model
        popt, pcov = curve_fit(
            klein_suppression_model,
            M, klein_effect,
            p0=[0.5, M_CRITICAL, 2],
            bounds=([0, 100, 0.5], [1, 5000, 10]),
            maxfev=5000
        )

        A_fit, M_c_fit, n_fit = popt
        perr = np.sqrt(np.diag(pcov))

        # Predict with model
        klein_predicted = klein_suppression_model(M, *popt)

        # R² score
        ss_res = np.sum((klein_effect - klein_predicted)**2)
        ss_tot = np.sum((klein_effect - klein_effect.mean())**2)
        r2 = 1 - ss_res / ss_tot

        print(f"\n  Klein suppression model: effect = A / (1 + (M/M_c)^n)")
        print(f"  Fitted parameters:")
        print(f"    A (amplitude)  = {A_fit:.3f} ± {perr[0]:.3f}")
        print(f"    M_c (critical) = {M_c_fit:.1f} ± {perr[1]:.1f} M☉")
        print(f"    n (steepness)  = {n_fit:.2f} ± {perr[2]:.2f}")
        print(f"  Model R² = {r2:.3f}")

        # Compare M_c_fit with theoretical M_critical
        print(f"\n  Theoretical M_critical = {M_CRITICAL:.0f} M☉")
        print(f"  Fitted M_c = {M_c_fit:.0f} M☉")

        ratio = M_c_fit / M_CRITICAL
        if 0.5 < ratio < 2:
            verdict_mc = "✓ Fitted M_c consistent with R_s = R_Klein prediction"
        else:
            verdict_mc = f"⚠ Fitted M_c differs from prediction by factor {ratio:.1f}"

        print(f"  {verdict_mc}")

        # Is there suppression?
        if n_fit > 1 and M_c_fit < 10000:
            verdict = "✓ MODEL SUPPORTS Klein suppression at high mass"
        else:
            verdict = "✗ NO EVIDENCE for Klein suppression"

        print(f"\n  {verdict}")

        return {
            'model': 'klein_suppression',
            'parameters': {
                'A': float(A_fit),
                'A_err': float(perr[0]),
                'M_c': float(M_c_fit),
                'M_c_err': float(perr[1]),
                'n': float(n_fit),
                'n_err': float(perr[2])
            },
            'r_squared': float(r2),
            'theoretical_M_critical': float(M_CRITICAL),
            'M_c_vs_theory_ratio': float(ratio),
            'verdict': verdict
        }

    except Exception as e:
        print(f"\n  ⚠ Model fitting failed: {e}")
        return {
            'model': 'klein_suppression',
            'fitting_failed': True,
            'error': str(e)
        }

# =============================================================================
# MAIN
# =============================================================================

def main():
    print("\n" + "=" * 70)
    print("EXECUTING SMBH MASS SCALING ANALYSIS")
    print("=" * 70)

    # Load data
    df = load_gwtc_data()

    # Calculate features
    features = calculate_klein_features(df)

    # Summary statistics
    print("\n" + "=" * 70)
    print("DATA SUMMARY")
    print("=" * 70)
    print(f"\n  Total events: {len(features)}")
    print(f"  Mass range: {features['M_total'].min():.1f} - {features['M_total'].max():.1f} M☉")
    print(f"  Events above M_critical ({M_CRITICAL:.0f} M☉): {features['above_critical'].sum()}")
    print(f"  Events below M_critical: {(~features['above_critical']).sum()}")

    # Run analyses
    results = {
        'timestamp': datetime.now().isoformat(),
        'parameters': {
            'R_Klein_km': R_KLEIN,
            'f0_Hz': f_0,
            'M_critical_solar': float(M_CRITICAL)
        },
        'data_summary': {
            'n_events': len(features),
            'M_min': float(features['M_total'].min()),
            'M_max': float(features['M_total'].max()),
            'n_above_critical': int(features['above_critical'].sum()),
            'n_below_critical': int((~features['above_critical']).sum())
        }
    }

    results['mass_bin_analysis'] = analyze_by_mass_bins(features)
    results['transition_search'] = search_for_transition(features)
    results['massive_events'] = analyze_massive_events(features)
    results['scaling_model'] = fit_transition_model(features)

    # ==========================================================================
    # OVERALL CONCLUSIONS
    # ==========================================================================

    print("\n" + "=" * 70)
    print("OVERALL CONCLUSIONS")
    print("=" * 70)

    conclusions = []

    # From mass bin analysis
    bins_with_data = [b for b in results['mass_bin_analysis'] if b.get('sufficient_data', False)]
    if bins_with_data:
        # Check if correlations weaken with mass
        low_mass_corr = [b['correlations']['SNR_vs_epsilon']['r'] for b in bins_with_data
                         if b['mean_M_total'] < 60]
        high_mass_corr = [b['correlations']['SNR_vs_epsilon']['r'] for b in bins_with_data
                          if b['mean_M_total'] >= 60]

        if low_mass_corr and high_mass_corr:
            mean_low = np.mean(low_mass_corr)
            mean_high = np.mean(high_mass_corr)
            if abs(mean_low) > abs(mean_high):
                conclusions.append("Klein correlations ARE weaker at higher mass")
            else:
                conclusions.append("Klein correlations do NOT weaken at higher mass")

    # From transition search
    if results['transition_search'].get('sufficient_data', False):
        if results['transition_search']['p_value'] < 0.05:
            conclusions.append(f"Transition detected at M ~ {results['transition_search'].get('M_critical', M_CRITICAL):.0f} M☉")

    # From scaling model
    if not results['scaling_model'].get('fitting_failed', False):
        if results['scaling_model']['r_squared'] > 0.1:
            M_c = results['scaling_model']['parameters']['M_c']
            conclusions.append(f"Scaling model suggests transition at M ~ {M_c:.0f} M☉")

    print("\n  KEY CONCLUSIONS:")
    if conclusions:
        for c in conclusions:
            print(f"    • {c}")
    else:
        print("    • No conclusive evidence for mass-dependent Klein effects")

    # Critical assessment
    print("\n  CRITICAL ASSESSMENT:")
    n_above = results['data_summary']['n_above_critical']
    if n_above < 5:
        print(f"    ⚠ Only {n_above} events above M_critical - insufficient for strong conclusions")
        print(f"    → Need LIGO O4/O5 data with more massive events")
        print(f"    → Or need to study IMBH candidates more carefully")
    else:
        print(f"    ✓ {n_above} events above M_critical - analysis is informative")

    results['conclusions'] = conclusions

    # Save
    output_path = Path(__file__).parent.parent / "results" / "smbh_mass_scaling.json"
    output_path.parent.mkdir(exist_ok=True)

    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2, default=str)

    print(f"\n✓ Results saved to: {output_path}")

    return results


if __name__ == "__main__":
    results = main()
