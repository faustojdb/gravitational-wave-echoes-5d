#!/usr/bin/env python3
"""
FAST RADIO BURSTS + KLEIN THEORY
================================

FRBs are millisecond radio pulses from cosmological distances.
Their Dispersion Measure (DM) depends on electron column density.

Question: Does Klein 5D topology add anomalous dispersion?

If photons briefly traverse 5D:
- Additional path length → additional DM
- DM_observed = DM_cosmic + DM_host + DM_MW + DM_Klein

Test: Look for DM excess that correlates with Klein predictions.

Author: Klein Theory Team
Date: January 2026
"""

import numpy as np
import pandas as pd
from scipy import stats
from scipy.optimize import curve_fit
import json
from pathlib import Path
from datetime import datetime

# =============================================================================
# CONSTANTS
# =============================================================================

c = 299792.458  # km/s
R_KLEIN = 8400  # km
f_0 = 5.68  # Hz
EPSILON_MAX = 0.65
H0 = 70  # km/s/Mpc (approximate)

print("=" * 70)
print("FAST RADIO BURSTS + KLEIN THEORY")
print("=" * 70)

# =============================================================================
# SIMULATED FRB CATALOG (based on CHIME statistics)
# =============================================================================

def generate_frb_catalog(n_frbs=500):
    """
    Generate realistic FRB catalog based on CHIME/FRB statistics.

    Real CHIME data: https://www.chime-frb.ca/catalog
    We simulate similar distributions.
    """
    print("\n" + "=" * 70)
    print("GENERATING FRB CATALOG (CHIME-like)")
    print("=" * 70)

    np.random.seed(42)

    # DM distribution (CHIME shows range ~100-2500 pc/cm³)
    # Follows roughly log-normal
    dm_observed = 10**np.random.normal(2.5, 0.4, n_frbs)  # pc/cm³
    dm_observed = np.clip(dm_observed, 100, 3000)

    # Estimate redshift from DM (Macquart relation)
    # DM_cosmic ≈ 900 × z pc/cm³ (approximate)
    # But observed DM includes MW (~30-100) and host (~50-200)
    dm_mw = np.random.uniform(30, 100, n_frbs)
    dm_host = np.random.uniform(30, 200, n_frbs)  # In host frame

    dm_cosmic = dm_observed - dm_mw - dm_host
    dm_cosmic = np.clip(dm_cosmic, 50, 2500)

    # Redshift estimate
    z_est = dm_cosmic / 900
    z_est = np.clip(z_est, 0.01, 3.0)

    # Correct host DM for redshift
    dm_host_corrected = dm_host * (1 + z_est)

    # Fluence (Jy ms) - log-normal distribution
    fluence = 10**np.random.normal(0.5, 0.8, n_frbs)
    fluence = np.clip(fluence, 0.1, 1000)

    # Width (ms)
    width = 10**np.random.normal(0.3, 0.5, n_frbs)
    width = np.clip(width, 0.1, 50)

    # Frequency (MHz) - CHIME band 400-800 MHz
    freq_mhz = np.random.uniform(400, 800, n_frbs)

    # Repeater flag (~3% are known repeaters)
    is_repeater = np.random.random(n_frbs) < 0.03

    # Scattering time (ms) - correlated with DM
    scattering = 0.001 * (dm_observed/100)**2 * np.random.lognormal(0, 1, n_frbs)

    catalog = pd.DataFrame({
        'frb_id': [f'FRB{20190000 + i}' for i in range(n_frbs)],
        'dm_observed': dm_observed,
        'dm_mw': dm_mw,
        'dm_host': dm_host,
        'dm_cosmic': dm_cosmic,
        'z_est': z_est,
        'fluence': fluence,
        'width': width,
        'freq_mhz': freq_mhz,
        'is_repeater': is_repeater,
        'scattering': scattering
    })

    print(f"\n  Generated {n_frbs} FRBs")
    print(f"  DM range: {dm_observed.min():.0f} - {dm_observed.max():.0f} pc/cm³")
    print(f"  z range: {z_est.min():.2f} - {z_est.max():.2f}")
    print(f"  Repeaters: {is_repeater.sum()}")

    return catalog


# =============================================================================
# KLEIN DM MODEL
# =============================================================================

def klein_dm_contribution(z, epsilon):
    """
    Klein contribution to Dispersion Measure.

    In Klein topology, photons experience additional path through 5D.
    This could manifest as anomalous dispersion.

    DM_Klein = n_e,eff × L_Klein

    Where L_Klein is the effective extra path length.
    """
    # Extra path length from Klein topology
    # L_Klein = ε² × c/f₀ × (1 + z)  [in proper distance units]

    # Convert to DM contribution (pc/cm³)
    # Assuming effective electron density in 5D boundary ~ 10⁻⁷ cm⁻³

    n_e_eff = 1e-7  # cm⁻³ (free parameter)
    L_klein_cm = epsilon**2 * (c * 1e5) / f_0 * (1 + z)  # cm

    # DM = n_e × L in pc/cm³
    # 1 pc = 3.086e18 cm
    dm_klein = n_e_eff * L_klein_cm / 3.086e18

    return dm_klein


def macquart_relation(z, dm_igm_0=900):
    """
    Standard Macquart relation: DM_cosmic ∝ z

    DM_cosmic = DM_IGM × ∫₀ᶻ (1+z')/E(z') dz'

    Simplified: DM_cosmic ≈ DM_IGM_0 × z for z < 1
    """
    # More accurate integral for higher z
    if isinstance(z, np.ndarray):
        dm = np.zeros_like(z)
        for i, zi in enumerate(z):
            if zi < 0.5:
                dm[i] = dm_igm_0 * zi
            else:
                # Include (1+z) growth
                dm[i] = dm_igm_0 * zi * (1 + 0.3 * zi)
        return dm
    else:
        if z < 0.5:
            return dm_igm_0 * z
        else:
            return dm_igm_0 * z * (1 + 0.3 * z)


# =============================================================================
# ANALYSIS 1: DM-z RELATION
# =============================================================================

def analyze_dm_z_relation(catalog):
    """
    Test if DM-z relation shows Klein deviation.
    """
    print("\n" + "=" * 70)
    print("ANALYSIS 1: DM-z RELATION")
    print("=" * 70)

    z = catalog['z_est'].values
    dm_cosmic = catalog['dm_cosmic'].values

    # Standard Macquart fit
    def macquart_fit(z, dm0):
        return macquart_fit_func(z, dm0)

    def macquart_fit_func(z, dm0):
        return dm0 * z * (1 + 0.3 * z)

    # Klein-modified fit
    def klein_fit(z, dm0, epsilon):
        dm_standard = dm0 * z * (1 + 0.3 * z)
        dm_klein = klein_dm_contribution(z, epsilon)
        return dm_standard + dm_klein

    # Fit standard model
    try:
        popt_std, pcov_std = curve_fit(macquart_fit_func, z, dm_cosmic,
                                        p0=[900], bounds=([500], [1500]))
        dm0_std = popt_std[0]
        dm_pred_std = macquart_fit_func(z, dm0_std)
        residuals_std = dm_cosmic - dm_pred_std
        chi2_std = np.sum(residuals_std**2 / (100**2))  # Assume σ=100 pc/cm³
    except:
        dm0_std = 900
        dm_pred_std = macquart_fit_func(z, dm0_std)
        residuals_std = dm_cosmic - dm_pred_std
        chi2_std = np.sum(residuals_std**2 / (100**2))

    # Fit Klein model
    try:
        popt_klein, pcov_klein = curve_fit(klein_fit, z, dm_cosmic,
                                            p0=[900, 0.3],
                                            bounds=([500, 0], [1500, EPSILON_MAX]))
        dm0_klein, eps_klein = popt_klein
        dm_pred_klein = klein_fit(z, dm0_klein, eps_klein)
        residuals_klein = dm_cosmic - dm_pred_klein
        chi2_klein = np.sum(residuals_klein**2 / (100**2))
    except:
        dm0_klein, eps_klein = 900, 0.0
        dm_pred_klein = klein_fit(z, dm0_klein, eps_klein)
        residuals_klein = dm_cosmic - dm_pred_klein
        chi2_klein = np.sum(residuals_klein**2 / (100**2))

    dof_std = len(z) - 1
    dof_klein = len(z) - 2

    print(f"\n  Standard Macquart model:")
    print(f"    DM₀ = {dm0_std:.1f} pc/cm³")
    print(f"    χ²/dof = {chi2_std/dof_std:.3f}")

    print(f"\n  Klein-modified model:")
    print(f"    DM₀ = {dm0_klein:.1f} pc/cm³")
    print(f"    ε = {eps_klein:.4f}")
    print(f"    χ²/dof = {chi2_klein/dof_klein:.3f}")

    # F-test
    F_stat = ((chi2_std - chi2_klein) / 1) / (chi2_klein / dof_klein)
    p_value = 1 - stats.f.cdf(max(0, F_stat), 1, dof_klein)

    print(f"\n  Model comparison:")
    print(f"    Δχ² = {chi2_std - chi2_klein:.2f}")
    print(f"    F-test: F = {F_stat:.2f}, p = {p_value:.4f}")

    if p_value < 0.05 and eps_klein > 0.01:
        verdict = "✓ Klein model significantly better"
    elif chi2_klein < chi2_std:
        verdict = "⚠ Klein model slightly better but not significant"
    else:
        verdict = "✗ Standard model sufficient"

    print(f"\n  {verdict}")

    return {
        'dm0_standard': dm0_std,
        'dm0_klein': dm0_klein,
        'epsilon_klein': eps_klein,
        'chi2_standard': chi2_std,
        'chi2_klein': chi2_klein,
        'F_stat': F_stat,
        'p_value': p_value,
        'verdict': verdict
    }


# =============================================================================
# ANALYSIS 2: DM EXCESS vs REDSHIFT
# =============================================================================

def analyze_dm_excess(catalog):
    """
    Look for systematic DM excess at high z.
    """
    print("\n" + "=" * 70)
    print("ANALYSIS 2: DM EXCESS vs REDSHIFT")
    print("=" * 70)

    z = catalog['z_est'].values
    dm_cosmic = catalog['dm_cosmic'].values

    # Expected DM from standard model
    dm_expected = 900 * z * (1 + 0.3 * z)

    # Excess
    dm_excess = dm_cosmic - dm_expected
    dm_excess_frac = dm_excess / dm_expected

    # Bin by redshift
    z_bins = [0, 0.3, 0.6, 1.0, 1.5, 3.0]
    bin_results = []

    print(f"\n  {'z range':<12} {'N':<6} {'<DM_excess>':<15} {'<frac>':<10}")
    print("  " + "-" * 50)

    for i in range(len(z_bins) - 1):
        mask = (z >= z_bins[i]) & (z < z_bins[i+1])
        if mask.sum() > 5:
            mean_excess = dm_excess[mask].mean()
            std_excess = dm_excess[mask].std() / np.sqrt(mask.sum())
            mean_frac = dm_excess_frac[mask].mean()

            bin_results.append({
                'z_min': z_bins[i],
                'z_max': z_bins[i+1],
                'n': mask.sum(),
                'mean_excess': mean_excess,
                'std_excess': std_excess,
                'mean_frac': mean_frac
            })

            print(f"  {z_bins[i]:.1f}-{z_bins[i+1]:.1f}      {mask.sum():<6} "
                  f"{mean_excess:>8.1f} ± {std_excess:.1f}    {mean_frac:>6.1%}")

    # Test for trend with z
    z_mid = [(b['z_min'] + b['z_max'])/2 for b in bin_results]
    excesses = [b['mean_excess'] for b in bin_results]

    if len(z_mid) > 2:
        slope, intercept, r, p, se = stats.linregress(z_mid, excesses)
        print(f"\n  Trend with z:")
        print(f"    Slope = {slope:.1f} pc/cm³ per unit z")
        print(f"    r = {r:.3f}, p = {p:.4f}")

        if p < 0.05 and slope > 0:
            verdict = "✓ Significant positive DM excess trend with z"
        elif slope > 0:
            verdict = "⚠ Weak positive trend (not significant)"
        else:
            verdict = "✗ No excess trend detected"
    else:
        slope, r, p = 0, 0, 1
        verdict = "Insufficient bins for trend analysis"

    print(f"\n  {verdict}")

    return {
        'bins': bin_results,
        'trend_slope': slope,
        'trend_r': r,
        'trend_p': p,
        'verdict': verdict
    }


# =============================================================================
# ANALYSIS 3: SCATTERING vs KLEIN
# =============================================================================

def analyze_scattering_klein(catalog):
    """
    Scattering time could also have Klein component.
    """
    print("\n" + "=" * 70)
    print("ANALYSIS 3: SCATTERING ANOMALIES")
    print("=" * 70)

    dm = catalog['dm_observed'].values
    scattering = catalog['scattering'].values
    z = catalog['z_est'].values

    # Standard expectation: τ_scatter ∝ DM^α with α ~ 2
    # Log-log fit
    log_dm = np.log10(dm)
    log_scat = np.log10(scattering + 1e-6)

    # Remove outliers
    mask = (log_scat > -4) & (log_scat < 3)
    log_dm_clean = log_dm[mask]
    log_scat_clean = log_scat[mask]
    z_clean = z[mask]

    # Fit
    slope, intercept, r, p, se = stats.linregress(log_dm_clean, log_scat_clean)

    print(f"\n  Scattering-DM relation:")
    print(f"    τ_scat ∝ DM^{slope:.2f}")
    print(f"    Expected: DM^2.0")
    print(f"    r = {r:.3f}")

    # Residuals from fit
    log_scat_pred = intercept + slope * log_dm_clean
    residuals = log_scat_clean - log_scat_pred

    # Correlate residuals with z (Klein prediction: excess at high z)
    r_z, p_z = stats.spearmanr(z_clean, residuals)

    print(f"\n  Scattering residuals vs z:")
    print(f"    r = {r_z:.3f}, p = {p_z:.4f}")

    if p_z < 0.05 and r_z > 0:
        verdict = "✓ Scattering excess at high z (Klein-consistent)"
    else:
        verdict = "✗ No anomalous scattering pattern"

    print(f"\n  {verdict}")

    return {
        'dm_power_law': slope,
        'expected_power': 2.0,
        'residual_z_correlation': r_z,
        'residual_z_pvalue': p_z,
        'verdict': verdict
    }


# =============================================================================
# ANALYSIS 4: REPEATERS vs ONE-OFFS
# =============================================================================

def analyze_repeaters(catalog):
    """
    Do repeating FRBs show different Klein signatures?
    """
    print("\n" + "=" * 70)
    print("ANALYSIS 4: REPEATERS vs ONE-OFF FRBs")
    print("=" * 70)

    repeaters = catalog[catalog['is_repeater']]
    one_offs = catalog[~catalog['is_repeater']]

    print(f"\n  Repeaters: {len(repeaters)}")
    print(f"  One-offs: {len(one_offs)}")

    if len(repeaters) < 5:
        print("  Insufficient repeaters for comparison")
        return {'verdict': 'Insufficient data'}

    # Compare DM distributions
    stat, p_dm = stats.mannwhitneyu(repeaters['dm_observed'], one_offs['dm_observed'])

    # Compare z distributions
    stat, p_z = stats.mannwhitneyu(repeaters['z_est'], one_offs['z_est'])

    print(f"\n  DM comparison (Mann-Whitney):")
    print(f"    Repeaters <DM> = {repeaters['dm_observed'].mean():.0f}")
    print(f"    One-offs <DM> = {one_offs['dm_observed'].mean():.0f}")
    print(f"    p = {p_dm:.4f}")

    print(f"\n  Redshift comparison:")
    print(f"    Repeaters <z> = {repeaters['z_est'].mean():.2f}")
    print(f"    One-offs <z> = {one_offs['z_est'].mean():.2f}")
    print(f"    p = {p_z:.4f}")

    # Klein prediction: repeaters might show consistent DM excess
    # (if Klein coupling is stable for a given source)
    dm_excess_rep = repeaters['dm_cosmic'] - 900 * repeaters['z_est']
    dm_excess_one = one_offs['dm_cosmic'] - 900 * one_offs['z_est']

    stat, p_excess = stats.mannwhitneyu(dm_excess_rep, dm_excess_one)

    print(f"\n  DM excess comparison:")
    print(f"    Repeaters <excess> = {dm_excess_rep.mean():.0f}")
    print(f"    One-offs <excess> = {dm_excess_one.mean():.0f}")
    print(f"    p = {p_excess:.4f}")

    if p_excess < 0.05:
        verdict = "✓ Repeaters show different DM excess pattern"
    else:
        verdict = "✗ No significant difference between repeaters and one-offs"

    print(f"\n  {verdict}")

    return {
        'n_repeaters': len(repeaters),
        'n_one_offs': len(one_offs),
        'p_dm': p_dm,
        'p_z': p_z,
        'p_excess': p_excess,
        'verdict': verdict
    }


# =============================================================================
# MAIN
# =============================================================================

def main():
    results = {
        'timestamp': datetime.now().isoformat(),
        'klein_parameters': {
            'R_km': R_KLEIN,
            'f0_Hz': f_0,
            'epsilon_max': EPSILON_MAX
        }
    }

    # Generate catalog
    catalog = generate_frb_catalog(n_frbs=500)
    results['n_frbs'] = len(catalog)

    # Run analyses
    results['dm_z_relation'] = analyze_dm_z_relation(catalog)
    results['dm_excess'] = analyze_dm_excess(catalog)
    results['scattering'] = analyze_scattering_klein(catalog)
    results['repeaters'] = analyze_repeaters(catalog)

    # ==========================================================================
    # SUMMARY
    # ==========================================================================

    print("\n" + "=" * 70)
    print("SUMMARY: FRB + KLEIN ANALYSIS")
    print("=" * 70)

    findings = []

    if 'better' in results['dm_z_relation']['verdict'].lower():
        findings.append("DM-z relation improved by Klein model")

    if 'positive' in results['dm_excess']['verdict'].lower():
        findings.append("DM excess trend with redshift detected")

    if 'consistent' in results['scattering']['verdict'].lower():
        findings.append("Scattering anomaly at high z")

    if 'different' in results['repeaters']['verdict'].lower():
        findings.append("Repeaters show distinct DM pattern")

    print("\n  KEY FINDINGS:")
    if findings:
        for f in findings:
            print(f"    • {f}")
    else:
        print("    • No significant Klein signatures in FRB data")

    # Overall
    n_positive = len(findings)

    if n_positive >= 2:
        overall = "✓ Multiple Klein-consistent patterns in FRBs"
    elif n_positive == 1:
        overall = "⚠ Weak evidence for Klein effects in FRBs"
    else:
        overall = "✗ No Klein signatures detected (with simulated data)"

    print(f"\n  OVERALL: {overall}")

    print("""
    NOTE: This analysis used SIMULATED FRB data based on CHIME statistics.
    For real confirmation, need actual CHIME/FRB catalog analysis.

    Real data available at: https://www.chime-frb.ca/catalog
    """)

    results['findings'] = findings
    results['overall'] = overall

    # Save
    output_path = Path(__file__).parent.parent / "results" / "frb_klein_analysis.json"
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2, default=str)

    print(f"✓ Results saved to: {output_path}")

    return results


if __name__ == "__main__":
    results = main()
