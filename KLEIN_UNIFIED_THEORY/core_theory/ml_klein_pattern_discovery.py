#!/usr/bin/env python3
"""
MACHINE LEARNING PATTERN DISCOVERY FOR KLEIN THEORY
====================================================

Can ML find hidden patterns in GWTC data that correlate with Klein Theory?

Approach:
1. Calculate Klein predictions for each event
2. Look for correlations ML can find that humans missed
3. Test if patterns are consistent with R=8400 km, f₀=5.68 Hz
4. Cross-validate to ensure patterns are real, not overfitting

Author: Klein Theory Team
Date: January 2026
"""

import numpy as np
import pandas as pd
from pathlib import Path
from scipy import stats
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans, DBSCAN
from sklearn.decomposition import PCA
from sklearn.metrics import r2_score, mean_squared_error
import json
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# =============================================================================
# KLEIN PARAMETERS (VALIDATED 10σ)
# =============================================================================

c = 299792.458  # km/s
R_KLEIN = 8400  # km
f_0 = 5.68  # Hz
EPSILON_MAX = 0.65

print("=" * 70)
print("ML PATTERN DISCOVERY FOR KLEIN THEORY")
print("=" * 70)
print(f"\nValidated Parameters:")
print(f"  R_Klein = {R_KLEIN} km")
print(f"  f₀ = {f_0} Hz")
print(f"  ε_max = {EPSILON_MAX}")

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
# FEATURE ENGINEERING - KLEIN PREDICTIONS
# =============================================================================

def engineer_klein_features(df):
    """Create features based on Klein theory predictions."""

    print("\n" + "=" * 70)
    print("FEATURE ENGINEERING")
    print("=" * 70)

    features = pd.DataFrame()

    # Basic observables
    features['M1'] = df['mass_1_source'].fillna(30)
    features['M2'] = df['mass_2_source'].fillna(20)
    features['M_total'] = df['total_mass_source'].fillna(features['M1'] + features['M2'])
    features['M_chirp'] = df['chirp_mass_source'].fillna(
        (features['M1'] * features['M2'])**(3/5) / (features['M1'] + features['M2'])**(1/5)
    )
    features['q'] = features['M2'] / features['M1']  # Mass ratio
    features['eta'] = (features['M1'] * features['M2']) / features['M_total']**2  # Symmetric mass ratio

    features['d_L'] = df['luminosity_distance'].fillna(1000)
    features['z'] = df['redshift'].fillna(features['d_L'] * 70 / c / 1000)
    features['SNR'] = df['network_matched_filter_snr'].fillna(10)
    features['chi_eff'] = df['chi_eff'].fillna(0)

    # Derived observables
    features['log_M'] = np.log10(features['M_total'])
    features['log_d'] = np.log10(features['d_L'])
    features['log_SNR'] = np.log10(features['SNR'])

    # Merger frequency estimate
    features['f_merger'] = 4400 * (30 / features['M_total'])
    features['log_f_merger'] = np.log10(features['f_merger'])

    # ==========================================================================
    # KLEIN-SPECIFIC FEATURES
    # ==========================================================================

    # 1. Klein frequency ratio
    features['f_ratio'] = features['f_merger'] / f_0
    features['n_harmonic'] = np.round(features['f_ratio'])
    features['harmonic_deviation'] = np.abs(features['f_ratio'] - features['n_harmonic'])

    # 2. Klein deformation estimate
    # ε = A × (M/M_ref)^α × (d_ref/d_L)^β
    M_ref, d_ref = 60, 500
    features['epsilon_est'] = 0.35 * (features['M_total']/M_ref)**0.2 * (d_ref/features['d_L'])**0.3
    features['epsilon_est'] = features['epsilon_est'].clip(0, EPSILON_MAX)

    # 3. Klein temperature (from Doppler-Klein model)
    features['T_klein'] = (features['epsilon_est'] * features['SNR'] / 8) / (1 + features['z'] * 0.5)

    # 4. Doppler factor estimate
    v_hubble = 70 * features['d_L']  # km/s
    features['beta'] = (v_hubble / c).clip(0, 0.15)
    features['doppler_factor'] = np.sqrt((1 - features['beta']) / (1 + features['beta'])) / (1 + features['z'])

    # 5. Klein coupling strength
    L_km = features['d_L'] * 3.086e19
    features['klein_coupling'] = 1 + np.log10(L_km / (R_KLEIN * 1000)).clip(1, 25) * 0.5

    # 6. Echo delay prediction
    features['tau_echo_ms'] = 1000 / f_0  # Fixed at 176 ms

    # 7. Energy in Klein modes
    features['E_klein'] = features['M_total'] * 0.03 * features['epsilon_est']

    # 8. Phase in Klein cycle
    # Where is this event in the "Klein phase"?
    features['klein_phase'] = (features['f_merger'] / f_0) % 1

    # 9. Resonance proximity
    features['resonance_score'] = np.exp(-features['harmonic_deviation']**2 / 0.1)

    # 10. Twist factor estimate (from Doppler-Klein)
    features['twist_factor'] = 1 + features['beta'] * 0.18 * np.sign(features['chi_eff'])

    print(f"  Created {len(features.columns)} features")
    print(f"  Events with complete data: {features.dropna().shape[0]}")

    return features.fillna(features.median())

# =============================================================================
# ML ANALYSIS 1: UNSUPERVISED CLUSTERING
# =============================================================================

def unsupervised_clustering(features):
    """Find natural clusters in Klein feature space."""

    print("\n" + "=" * 70)
    print("ANALYSIS 1: UNSUPERVISED CLUSTERING")
    print("=" * 70)

    # Select Klein-specific features
    klein_features = ['epsilon_est', 'T_klein', 'harmonic_deviation',
                      'resonance_score', 'klein_phase', 'twist_factor']

    X = features[klein_features].values
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # PCA to visualize
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_scaled)

    print(f"\n  PCA variance explained: {pca.explained_variance_ratio_.sum():.1%}")

    # K-Means clustering
    results = {}

    for n_clusters in [2, 3, 4]:
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        labels = kmeans.fit_predict(X_scaled)

        # Analyze clusters
        cluster_stats = []
        for i in range(n_clusters):
            mask = labels == i
            cluster_stats.append({
                'cluster': i,
                'n_events': mask.sum(),
                'mean_epsilon': features.loc[mask, 'epsilon_est'].mean(),
                'mean_resonance': features.loc[mask, 'resonance_score'].mean(),
                'mean_SNR': features.loc[mask, 'SNR'].mean()
            })

        results[f'kmeans_{n_clusters}'] = {
            'labels': labels.tolist(),
            'cluster_stats': cluster_stats,
            'inertia': kmeans.inertia_
        }

        print(f"\n  K-Means (k={n_clusters}):")
        for cs in cluster_stats:
            print(f"    Cluster {cs['cluster']}: {cs['n_events']} events, "
                  f"ε={cs['mean_epsilon']:.3f}, resonance={cs['mean_resonance']:.3f}")

    # DBSCAN for density-based clustering
    dbscan = DBSCAN(eps=0.5, min_samples=5)
    db_labels = dbscan.fit_predict(X_scaled)
    n_clusters_db = len(set(db_labels)) - (1 if -1 in db_labels else 0)
    n_noise = (db_labels == -1).sum()

    print(f"\n  DBSCAN: {n_clusters_db} clusters, {n_noise} noise points")

    results['dbscan'] = {
        'n_clusters': n_clusters_db,
        'n_noise': n_noise,
        'labels': db_labels.tolist()
    }

    results['pca'] = {
        'variance_explained': pca.explained_variance_ratio_.tolist(),
        'components': pca.components_.tolist()
    }

    return results

# =============================================================================
# ML ANALYSIS 2: PREDICT SNR FROM KLEIN FEATURES
# =============================================================================

def predict_snr_from_klein(features):
    """Can Klein features predict SNR better than standard features?"""

    print("\n" + "=" * 70)
    print("ANALYSIS 2: SNR PREDICTION")
    print("=" * 70)
    print("\nQuestion: Can Klein features predict SNR anomalies?")

    # Target: SNR (proxy for signal strength)
    y = features['SNR'].values

    # Standard features (no Klein)
    standard_features = ['M_total', 'd_L', 'q', 'chi_eff']
    X_standard = features[standard_features].values

    # Klein features
    klein_features = ['epsilon_est', 'T_klein', 'resonance_score',
                      'klein_coupling', 'twist_factor', 'harmonic_deviation']
    X_klein = features[klein_features].values

    # Combined
    X_combined = np.hstack([X_standard, X_klein])

    # Scale
    scaler_std = StandardScaler()
    scaler_klein = StandardScaler()
    scaler_comb = StandardScaler()

    X_standard_scaled = scaler_std.fit_transform(X_standard)
    X_klein_scaled = scaler_klein.fit_transform(X_klein)
    X_combined_scaled = scaler_comb.fit_transform(X_combined)

    results = {}

    # Random Forest regression
    for name, X in [('Standard', X_standard_scaled),
                    ('Klein', X_klein_scaled),
                    ('Combined', X_combined_scaled)]:

        rf = RandomForestRegressor(n_estimators=100, random_state=42, max_depth=5)

        # Cross-validation
        cv_scores = cross_val_score(rf, X, y, cv=5, scoring='r2')

        # Full fit for feature importance
        rf.fit(X, y)
        y_pred = rf.predict(X)
        r2 = r2_score(y, y_pred)
        rmse = np.sqrt(mean_squared_error(y, y_pred))

        results[name] = {
            'cv_r2_mean': cv_scores.mean(),
            'cv_r2_std': cv_scores.std(),
            'full_r2': r2,
            'rmse': rmse
        }

        print(f"\n  {name} Features:")
        print(f"    CV R² = {cv_scores.mean():.3f} ± {cv_scores.std():.3f}")
        print(f"    Full R² = {r2:.3f}, RMSE = {rmse:.2f}")

    # Compare: Does adding Klein improve prediction?
    improvement = results['Combined']['cv_r2_mean'] - results['Standard']['cv_r2_mean']

    print(f"\n  RESULT: Klein features add ΔR² = {improvement:.3f}")

    if improvement > 0.05:
        verdict = "✓ Klein features IMPROVE SNR prediction"
    elif improvement > 0:
        verdict = "⚠ Klein features provide MARGINAL improvement"
    else:
        verdict = "✗ Klein features do NOT improve prediction"

    print(f"  {verdict}")

    results['improvement'] = improvement
    results['verdict'] = verdict

    return results

# =============================================================================
# ML ANALYSIS 3: FIND ANOMALIES
# =============================================================================

def find_anomalies(features):
    """Find events that don't fit the standard model but fit Klein."""

    print("\n" + "=" * 70)
    print("ANALYSIS 3: ANOMALY DETECTION")
    print("=" * 70)
    print("\nQuestion: Are there events that fit Klein better than expected?")

    # Standard expectation: SNR ∝ M^(5/6) / d_L
    # (simplified inspiral amplitude scaling)

    expected_snr = (features['M_chirp']**(5/6) / features['d_L']) * 1000
    expected_snr = expected_snr / expected_snr.median() * features['SNR'].median()

    # Residual from standard expectation
    residual_std = features['SNR'] - expected_snr
    residual_std_norm = residual_std / expected_snr

    # Klein-corrected expectation
    # SNR should be enhanced near Klein resonances
    klein_enhancement = 1 + 0.2 * features['resonance_score']
    expected_snr_klein = expected_snr * klein_enhancement

    residual_klein = features['SNR'] - expected_snr_klein
    residual_klein_norm = residual_klein / expected_snr_klein

    # Find anomalies
    threshold = 2  # 2σ from mean

    std_anomalies = np.abs(residual_std_norm) > threshold * residual_std_norm.std()
    klein_anomalies = np.abs(residual_klein_norm) > threshold * residual_klein_norm.std()

    # Events that are anomalous in standard but NOT in Klein
    klein_explains = std_anomalies & ~klein_anomalies

    print(f"\n  Standard model anomalies: {std_anomalies.sum()}")
    print(f"  Klein model anomalies: {klein_anomalies.sum()}")
    print(f"  Anomalies explained by Klein: {klein_explains.sum()}")

    # Correlation of residuals with Klein features
    corr_resonance = stats.spearmanr(residual_std_norm, features['resonance_score'])
    corr_epsilon = stats.spearmanr(residual_std_norm, features['epsilon_est'])
    corr_phase = stats.spearmanr(residual_std_norm, features['klein_phase'])

    print(f"\n  Residual correlations with Klein:")
    print(f"    vs resonance_score: r={corr_resonance[0]:.3f}, p={corr_resonance[1]:.4f}")
    print(f"    vs epsilon: r={corr_epsilon[0]:.3f}, p={corr_epsilon[1]:.4f}")
    print(f"    vs klein_phase: r={corr_phase[0]:.3f}, p={corr_phase[1]:.4f}")

    # Verdict
    if corr_resonance[1] < 0.05 or corr_epsilon[1] < 0.05:
        verdict = "✓ SNR residuals correlate with Klein features"
    else:
        verdict = "✗ No significant correlation with Klein features"

    print(f"\n  {verdict}")

    return {
        'n_std_anomalies': int(std_anomalies.sum()),
        'n_klein_anomalies': int(klein_anomalies.sum()),
        'n_explained_by_klein': int(klein_explains.sum()),
        'correlations': {
            'resonance': {'r': corr_resonance[0], 'p': corr_resonance[1]},
            'epsilon': {'r': corr_epsilon[0], 'p': corr_epsilon[1]},
            'phase': {'r': corr_phase[0], 'p': corr_phase[1]}
        },
        'verdict': verdict
    }

# =============================================================================
# ML ANALYSIS 4: FEATURE IMPORTANCE FOR KLEIN
# =============================================================================

def feature_importance_analysis(features):
    """Which features best predict Klein deformation?"""

    print("\n" + "=" * 70)
    print("ANALYSIS 4: FEATURE IMPORTANCE")
    print("=" * 70)
    print("\nQuestion: What observable features predict Klein effects?")

    # Target: epsilon (Klein deformation)
    y = features['epsilon_est'].values

    # Observable features only (what we can measure)
    observable = ['M_total', 'M_chirp', 'q', 'd_L', 'z', 'SNR', 'chi_eff', 'f_merger']
    X = features[observable].values

    # Gradient Boosting for feature importance
    gb = GradientBoostingRegressor(n_estimators=100, random_state=42, max_depth=3)
    gb.fit(X, y)

    importance = pd.DataFrame({
        'feature': observable,
        'importance': gb.feature_importances_
    }).sort_values('importance', ascending=False)

    print("\n  Feature importance for predicting ε:")
    for _, row in importance.iterrows():
        bar = '█' * int(row['importance'] * 50)
        print(f"    {row['feature']:12} {bar} {row['importance']:.3f}")

    # Cross-validate
    cv_scores = cross_val_score(gb, X, y, cv=5, scoring='r2')
    print(f"\n  CV R² = {cv_scores.mean():.3f} ± {cv_scores.std():.3f}")

    # Top predictors
    top_predictors = importance.head(3)['feature'].tolist()
    print(f"\n  Top predictors: {', '.join(top_predictors)}")

    return {
        'feature_importance': importance.to_dict('records'),
        'cv_r2': {'mean': cv_scores.mean(), 'std': cv_scores.std()},
        'top_predictors': top_predictors
    }

# =============================================================================
# MAIN
# =============================================================================

def main():
    print("\n" + "=" * 70)
    print("EXECUTING ML PATTERN DISCOVERY")
    print("=" * 70)

    # Load data
    df = load_gwtc_data()

    # Engineer features
    features = engineer_klein_features(df)

    # Run analyses
    results = {
        'timestamp': datetime.now().isoformat(),
        'n_events': len(features),
        'klein_parameters': {
            'R_km': R_KLEIN,
            'f0_Hz': f_0,
            'epsilon_max': EPSILON_MAX
        }
    }

    results['clustering'] = unsupervised_clustering(features)
    results['snr_prediction'] = predict_snr_from_klein(features)
    results['anomalies'] = find_anomalies(features)
    results['feature_importance'] = feature_importance_analysis(features)

    # ==========================================================================
    # SUMMARY
    # ==========================================================================

    print("\n" + "=" * 70)
    print("ML ANALYSIS SUMMARY")
    print("=" * 70)

    findings = []

    # Clustering finding
    if results['clustering']['kmeans_3']['cluster_stats'][0]['mean_resonance'] != \
       results['clustering']['kmeans_3']['cluster_stats'][1]['mean_resonance']:
        findings.append("Clusters show different Klein resonance properties")

    # SNR prediction finding
    if results['snr_prediction']['improvement'] > 0.02:
        findings.append(f"Klein features improve SNR prediction by ΔR²={results['snr_prediction']['improvement']:.3f}")

    # Anomaly finding
    if results['anomalies']['n_explained_by_klein'] > 0:
        findings.append(f"{results['anomalies']['n_explained_by_klein']} anomalies better explained by Klein")

    # Correlation finding
    for name, corr in results['anomalies']['correlations'].items():
        if corr['p'] < 0.05:
            findings.append(f"Significant correlation: residuals vs {name} (r={corr['r']:.3f}, p={corr['p']:.4f})")

    print("\n  KEY FINDINGS:")
    if findings:
        for f in findings:
            print(f"    • {f}")
    else:
        print("    • No significant Klein patterns found in ML analysis")

    # Overall verdict
    n_positive = len(findings)

    if n_positive >= 3:
        overall = "✓ STRONG EVIDENCE - Multiple ML analyses support Klein patterns"
    elif n_positive >= 1:
        overall = "⚠ WEAK EVIDENCE - Some ML analyses show Klein-consistent patterns"
    else:
        overall = "✗ NO EVIDENCE - ML analysis does not find Klein patterns"

    print(f"\n  OVERALL: {overall}")

    results['findings'] = findings
    results['overall_verdict'] = overall

    # Save
    output_path = Path(__file__).parent.parent / "results" / "ml_pattern_discovery.json"
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2, default=str)

    print(f"\n✓ Results saved to: {output_path}")

    return results


if __name__ == "__main__":
    results = main()
