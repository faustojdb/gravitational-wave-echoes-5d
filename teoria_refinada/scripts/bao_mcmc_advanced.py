#!/usr/bin/env python3
"""
BAO MCMC ADVANCED ANALYSIS - KLEIN THEORY
========================================

Implementa análisis Bayesiano completo con MCMC para constraints
precisos de parámetros Klein en Large Scale Structure.

Author: Klein Theory Validation Team  
Date: July 27, 2025
Status: Advanced MCMC implementation
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import json
import os

class BAOMCMCAdvanced:
    """
    MCMC Bayesiano avanzado para parámetros Klein en BAO.
    """
    
    def __init__(self):
        self.results = {}
        
        # Datos BAO simulados (como en análisis previo)
        self.redshift = np.array([0.15, 0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85, 0.95, 
                                 1.05, 1.15, 1.25, 1.35, 1.45, 1.55])
        self.distance_ratio = np.array([8.467, 10.135, 11.529, 12.734, 13.808, 14.782, 
                                      15.681, 16.518, 17.304, 18.046, 18.751, 19.422, 
                                      20.064, 20.679, 21.270])
        self.error_ratio = 0.02 * self.distance_ratio  # 2% errors
        
        # Prior ranges (físicamente motivados)
        self.priors = {
            'H0': (60.0, 80.0),       # km/s/Mpc
            'Om': (0.2, 0.4),         # Density parameter  
            'R4_factor': (0.0, 1.0)   # Klein suppression
        }
        
    def bao_model_klein(self, z, H0, Om, R4_factor):
        """
        Modelo BAO Klein para MCMC.
        """
        OL = 1 - Om
        sound_horizon = 147.0  # Mpc
        cosmological_scale = 150e6 * 3.086e16  # km
        R_5D = 8.4e6  # km
        
        ratios = []
        for zi in z:
            # Distancia comóvil integrada
            z_int = np.linspace(0, zi, 50)
            E_z = np.sqrt(Om * (1 + z_int)**3 + OL)
            integral = np.trapz(1/E_z, z_int)
            
            d_c = 3000 * integral / H0
            d_a = d_c / (1 + zi)
            d_v = (d_a**2 * zi * 3000 / (H0 * np.sqrt(Om * (1 + zi)**3 + OL)))**(1/3)
            
            # Ratio estándar
            ratio_std = d_v / sound_horizon
            
            # Corrección Klein con escalado dinámico
            scale_factor = min((cosmological_scale / R_5D)**1.0, 1e6)
            klein_suppression = 1 - R4_factor * np.exp(-zi / 0.5) * scale_factor / 1e6
            klein_suppression = np.clip(klein_suppression, 0.8, 1.2)
            
            ratios.append(ratio_std * klein_suppression)
        
        return np.array(ratios)
    
    def log_likelihood(self, params):
        """
        Log-likelihood para MCMC.
        """
        H0, Om, R4_factor = params
        
        # Verificar priors
        if not (self.priors['H0'][0] <= H0 <= self.priors['H0'][1]):
            return -np.inf
        if not (self.priors['Om'][0] <= Om <= self.priors['Om'][1]):
            return -np.inf  
        if not (self.priors['R4_factor'][0] <= R4_factor <= self.priors['R4_factor'][1]):
            return -np.inf
        
        try:
            # Calcular modelo
            model = self.bao_model_klein(self.redshift, H0, Om, R4_factor)
            
            # Log-likelihood gaussiano
            chi2 = np.sum(((self.distance_ratio - model) / self.error_ratio)**2)
            log_like = -0.5 * chi2
            
            return log_like
            
        except:
            return -np.inf
    
    def log_prior(self, params):
        """
        Log-prior (uniforme en rangos físicos).
        """
        H0, Om, R4_factor = params
        
        # Priors uniformes
        log_p = 0.0
        
        # Prior débilmente informativo para H0 (Gaussiano centrado en Planck)
        log_p += norm.logpdf(H0, loc=67.4, scale=5.0)
        
        return log_p
    
    def log_posterior(self, params):
        """
        Log-posterior = log-likelihood + log-prior.
        """
        return self.log_likelihood(params) + self.log_prior(params)
    
    def metropolis_hastings(self, n_steps=50000, step_size=0.1):
        """
        Implementación Metropolis-Hastings simple pero efectiva.
        """
        print(f"🔄 Ejecutando MCMC con {n_steps:,} pasos...")
        
        # Punto inicial (cerca de mejor ajuste previo)
        current = np.array([62.0, 0.2, 0.183])
        current_log_prob = self.log_posterior(current)
        
        # Almacenar cadena
        chain = np.zeros((n_steps, 3))
        log_probs = np.zeros(n_steps)
        n_accepted = 0
        
        for i in range(n_steps):
            # Proponer nuevo punto
            proposal = current + np.random.normal(0, step_size, 3)
            proposal_log_prob = self.log_posterior(proposal)
            
            # Criterio Metropolis-Hastings
            log_ratio = proposal_log_prob - current_log_prob
            
            if log_ratio > 0 or np.random.random() < np.exp(log_ratio):
                # Aceptar
                current = proposal
                current_log_prob = proposal_log_prob
                n_accepted += 1
            
            # Guardar estado actual
            chain[i] = current
            log_probs[i] = current_log_prob
            
            # Progress
            if (i + 1) % 10000 == 0:
                acceptance_rate = n_accepted / (i + 1)
                print(f"  Paso {i+1:,}: aceptación = {acceptance_rate:.3f}")
        
        acceptance_rate = n_accepted / n_steps
        print(f"✓ MCMC completado: {acceptance_rate:.3f} tasa de aceptación")
        
        return chain, log_probs, acceptance_rate
    
    def analyze_chain(self, chain, burn_in=10000):
        """
        Analiza cadena MCMC para constraints y correlaciones.
        """
        print("📊 Analizando cadena MCMC...")
        
        # Remover burn-in
        chain_clean = chain[burn_in:]
        n_samples = len(chain_clean)
        
        # Estadísticas por parámetro
        param_names = ['H0', 'Om', 'R4_factor']
        constraints = {}
        
        for i, name in enumerate(param_names):
            samples = chain_clean[:, i]
            
            # Percentiles para constraints
            median = np.percentile(samples, 50)
            lower = np.percentile(samples, 16)  # -1σ
            upper = np.percentile(samples, 84)  # +1σ
            lower_2s = np.percentile(samples, 2.5)  # -2σ  
            upper_2s = np.percentile(samples, 97.5)  # +2σ
            
            constraints[name] = {
                'median': median,
                'sigma_1': (lower, upper),
                'sigma_2': (lower_2s, upper_2s),
                'mean': np.mean(samples),
                'std': np.std(samples)
            }
            
            print(f"  {name}: {median:.3f} +{upper-median:.3f}/-{median-lower:.3f}")
        
        # Matriz de correlación
        correlation_matrix = np.corrcoef(chain_clean.T)
        
        self.results['mcmc_analysis'] = {
            'n_samples': n_samples,
            'constraints': constraints,
            'correlation_matrix': correlation_matrix.tolist(),
            'parameter_names': param_names
        }
        
        return constraints, correlation_matrix
    
    def create_corner_plot(self, chain, burn_in=10000, output_dir='.'):
        """
        Genera corner plot para visualizar posterior.
        """
        chain_clean = chain[burn_in:]
        param_names = ['H₀', 'Ωₘ', 'R4_factor']
        
        fig, axes = plt.subplots(3, 3, figsize=(12, 12))
        
        for i in range(3):
            for j in range(3):
                ax = axes[i, j]
                
                if i == j:
                    # Diagonal: histogramas 1D
                    ax.hist(chain_clean[:, i], bins=50, alpha=0.7, density=True)
                    ax.set_xlabel(param_names[i])
                    ax.set_ylabel('Densidad')
                    
                    # Añadir percentiles
                    median = np.percentile(chain_clean[:, i], 50)
                    lower = np.percentile(chain_clean[:, i], 16)
                    upper = np.percentile(chain_clean[:, i], 84)
                    
                    ax.axvline(median, color='red', linestyle='-', alpha=0.7)
                    ax.axvline(lower, color='red', linestyle='--', alpha=0.5)
                    ax.axvline(upper, color='red', linestyle='--', alpha=0.5)
                    
                elif i > j:
                    # Triángulo inferior: scatterplots 2D
                    ax.scatter(chain_clean[:, j], chain_clean[:, i], alpha=0.1, s=1)
                    ax.set_xlabel(param_names[j])
                    ax.set_ylabel(param_names[i])
                    
                    # Contornos de confianza
                    try:
                        from scipy.stats import gaussian_kde
                        xx, yy = np.mgrid[chain_clean[:, j].min():chain_clean[:, j].max():.01j,
                                         chain_clean[:, i].min():chain_clean[:, i].max():.01j]
                        kde = gaussian_kde(np.vstack([chain_clean[:, j], chain_clean[:, i]]))
                        density = kde(np.vstack([xx.ravel(), yy.ravel()])).reshape(xx.shape)
                        ax.contour(xx, yy, density, levels=3, alpha=0.7)
                    except:
                        pass
                        
                else:
                    # Triángulo superior: vacío
                    ax.axis('off')
        
        plt.tight_layout()
        
        # Guardar
        plot_path = os.path.join(output_dir, 'bao_mcmc_corner_plot.png')
        plt.savefig(plot_path, dpi=300, bbox_inches='tight')
        print(f"✓ Corner plot guardado: {plot_path}")
        plt.show()
    
    def run_complete_mcmc(self, output_dir, n_steps=50000):
        """
        Ejecuta análisis MCMC completo.
        """
        print("🌌 INICIANDO ANÁLISIS BAO MCMC AVANZADO")
        print("="*50)
        
        os.makedirs(output_dir, exist_ok=True)
        
        # Ejecutar MCMC
        chain, log_probs, acceptance_rate = self.metropolis_hastings(n_steps)
        
        # Analizar resultados
        constraints, correlation_matrix = self.analyze_chain(chain)
        
        # Plots
        self.create_corner_plot(chain, output_dir=output_dir)
        
        # Guardar cadena y resultados
        results_path = os.path.join(output_dir, 'bao_mcmc_results.json')
        with open(results_path, 'w') as f:
            json.dump(self.results, f, indent=2, default=str)
        
        # Guardar cadena raw
        chain_path = os.path.join(output_dir, 'bao_mcmc_chain.npy')
        np.save(chain_path, chain)
        
        print(f"\n🎯 MCMC BAO COMPLETADO")
        print("="*30)
        print(f"• H₀: {constraints['H0']['median']:.2f} ± {constraints['H0']['std']:.2f}")
        print(f"• Ωₘ: {constraints['Om']['median']:.3f} ± {constraints['Om']['std']:.3f}")
        print(f"• R4_factor: {constraints['R4_factor']['median']:.3f} ± {constraints['R4_factor']['std']:.3f}")
        print(f"• Aceptación: {acceptance_rate:.3f}")
        
        return constraints

def main():
    """
    Función principal.
    """
    output_dir = "/mnt/d/Multidimensional Theory Simulations/multidimensional-theory/gravitational-wave-echoes-5d/teoria_refinada/resultados/bao_mcmc"
    
    analyzer = BAOMCMCAdvanced()
    constraints = analyzer.run_complete_mcmc(output_dir, n_steps=30000)  # Reducido para demo
    
    print("\n✅ ANÁLISIS MCMC BAO EXITOSO")

if __name__ == "__main__":
    main()