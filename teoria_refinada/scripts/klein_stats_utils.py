#!/usr/bin/env python3
"""
KLEIN STATISTICS UTILITIES
===========================

Utilidades estadísticas compatibles con versiones antiguas de scipy.
Implementa funciones que pueden no estar disponibles en todas las versiones.

Author: Klein Theory Validation Team
Date: July 26, 2025
"""

import numpy as np
from scipy.stats import chi2, norm

def safe_erfinv(p):
    """
    Función de error inversa compatible con versiones antiguas de scipy.
    
    Parameters:
    -----------
    p : float or array
        Probabilidad entre 0 y 1
        
    Returns:
    --------
    float or array
        Valor de error inverso
    """
    try:
        # Intentar usar erfinv de scipy.special si está disponible
        from scipy.special import erfinv
        return erfinv(p)
    except ImportError:
        # Fallback usando aproximación con distribución normal
        # erfinv(p) ≈ norm.ppf((1+p)/2) / sqrt(2)
        return norm.ppf((1 + p) / 2) / np.sqrt(2)

def p_value_to_sigma(p_value):
    """
    Convierte p-valor a niveles sigma (significancia estadística).
    
    Parameters:
    -----------
    p_value : float
        P-valor entre 0 y 1
        
    Returns:
    --------
    float
        Significancia en unidades sigma
    """
    # Manejar casos extremos
    if p_value <= 0:
        # Para p-valores exactamente 0 o negativos, usar límite superior
        return 6.0  # Cap en 6 sigma para evitar infinitos
    elif p_value >= 1:
        return 0.0
        
    try:
        # Método principal: usar distribución normal inversa
        # Para distribución normal: p = 2 * (1 - Φ(σ))
        # Por lo tanto: σ = Φ^(-1)(1 - p/2)
        sigma = norm.ppf(1 - p_value / 2)
        return abs(sigma)
    except:
        # Fallback usando aproximación
        if p_value < 1e-10:
            return 6.0  # Cap en 6 sigma
        else:
            return abs(np.sqrt(2) * safe_erfinv(1 - p_value))

def chi2_significance(delta_chi2, delta_dof):
    """
    Calcula significancia desde test de razón de verosimilitudes.
    
    Parameters:
    -----------
    delta_chi2 : float
        Diferencia en chi-cuadrado
    delta_dof : int
        Diferencia en grados de libertad
        
    Returns:
    --------
    dict
        Contiene p_value y sigma_level
    """
    if delta_chi2 <= 0:
        return {'p_value': 1.0, 'sigma_level': 0.0}
        
    try:
        # P-valor usando distribución chi-cuadrado
        p_value = chi2.sf(delta_chi2, delta_dof)
        
        # Para casos extremos con p_value = 0.0, usar aproximación directa
        if p_value == 0.0 and delta_dof == 1:
            # Para 1 grado de libertad: σ ≈ √Δχ²
            sigma_level = np.sqrt(delta_chi2)
            sigma_level = min(sigma_level, 10.0)  # Cap razonable en 10σ
        else:
            # Convertir a sigma usando función estándar
            sigma_level = p_value_to_sigma(p_value)
        
        return {
            'p_value': p_value,
            'sigma_level': sigma_level
        }
    except Exception as e:
        print(f"Warning: Error calculando significancia: {e}")
        return {'p_value': 1.0, 'sigma_level': 0.0}

def combine_significances(sigma_list, method='fisher'):
    """
    Combina múltiples significancias estadísticas.
    
    Parameters:
    -----------
    sigma_list : list
        Lista de significancias individuales
    method : str
        Método de combinación ('fisher', 'quadrature')
        
    Returns:
    --------
    float
        Significancia combinada
    """
    sigma_array = np.array(sigma_list)
    
    if method == 'fisher':
        # Método Fisher: combinar p-valores
        p_values = [2 * (1 - norm.cdf(abs(s))) for s in sigma_array]
        
        # Fisher's combined test
        fisher_stat = -2 * np.sum(np.log(np.maximum(p_values, 1e-16)))
        combined_p = chi2.sf(fisher_stat, 2 * len(p_values))
        
        return p_value_to_sigma(combined_p)
        
    elif method == 'quadrature':
        # Método cuadratura: suma en cuadratura
        return np.sqrt(np.sum(sigma_array**2))
        
    else:
        raise ValueError(f"Método '{method}' no reconocido")

def model_comparison_stats(chi2_null, dof_null, chi2_alt, dof_alt):
    """
    Estadísticas completas para comparación de modelos.
    
    Parameters:
    -----------
    chi2_null : float
        Chi-cuadrado modelo nulo
    dof_null : int
        Grados libertad modelo nulo
    chi2_alt : float
        Chi-cuadrado modelo alternativo
    dof_alt : int
        Grados libertad modelo alternativo
        
    Returns:
    --------
    dict
        Estadísticas completas de comparación
    """
    # Calcular diferencias
    delta_chi2 = chi2_null - chi2_alt
    delta_dof = dof_null - dof_alt
    
    # Chi-cuadrado reducido
    chi2_red_null = chi2_null / dof_null if dof_null > 0 else np.inf
    chi2_red_alt = chi2_alt / dof_alt if dof_alt > 0 else np.inf
    
    # Significancia
    significance = chi2_significance(delta_chi2, delta_dof)
    
    # Criterios información
    n_params_null = len([]) if dof_null == 0 else 2  # Estimación
    n_params_alt = n_params_null + delta_dof
    
    aic_null = chi2_null + 2 * n_params_null
    aic_alt = chi2_alt + 2 * n_params_alt
    delta_aic = aic_alt - aic_null
    
    # Interpretación
    interpretation = []
    
    sigma = significance['sigma_level']
    if sigma >= 5.0:
        interpretation.append("DETECCIÓN ALTAMENTE SIGNIFICATIVA (≥5σ)")
    elif sigma >= 3.0:
        interpretation.append("EVIDENCIA SIGNIFICATIVA (≥3σ)")
    elif sigma >= 1.0:
        interpretation.append("EVIDENCIA MARGINAL (≥1σ)")
    else:
        interpretation.append("NO EVIDENCIA SIGNIFICATIVA (<1σ)")
        
    if delta_aic < -10:
        interpretation.append("Modelo alternativo fuertemente preferido (ΔAIC < -10)")
    elif delta_aic < -2:
        interpretation.append("Modelo alternativo preferido (ΔAIC < -2)")
    elif delta_aic > 10:
        interpretation.append("Modelo nulo fuertemente preferido (ΔAIC > 10)")
    elif delta_aic > 2:
        interpretation.append("Modelo nulo preferido (ΔAIC > 2)")
    else:
        interpretation.append("Modelos estadísticamente equivalentes")
    
    return {
        'chi2_reduced_null': chi2_red_null,
        'chi2_reduced_alt': chi2_red_alt,
        'delta_chi2': delta_chi2,
        'delta_dof': delta_dof,
        'p_value': significance['p_value'],
        'sigma_level': significance['sigma_level'],
        'delta_aic': delta_aic,
        'interpretation': interpretation
    }

# Test de la funcionalidad
if __name__ == "__main__":
    print("🧪 Testing Klein Statistics Utilities...")
    
    # Test erfinv fallback
    test_p = 0.9
    result = safe_erfinv(test_p)
    print(f"erfinv({test_p}) = {result:.4f}")
    
    # Test p-value to sigma conversion
    test_p_values = [0.1, 0.05, 0.001, 1e-6]
    for p in test_p_values:
        sigma = p_value_to_sigma(p)
        print(f"p = {p:.2e} → σ = {sigma:.2f}")
    
    # Test significance combination
    individual_sigmas = [2.1, 1.8, 2.5, 1.2]
    combined = combine_significances(individual_sigmas, 'quadrature')
    print(f"Individual σ: {individual_sigmas}")
    print(f"Combined σ: {combined:.2f}")
    
    print("✅ Klein Statistics Utilities OK")