#!/usr/bin/env python3
"""
ANÁLISIS LIGO REAL CON EXTENSIÓN DOPPLER-KLEIN ESTABLE
======================================================

Aplicación estable de la extensión Doppler Klein a datos reales GWTC-3
usando la versión fija que resuelve problemas numéricos.

Author: Klein Theory Extension Team
Date: July 27, 2025
Status: Análisis production con datos reales
"""

import numpy as np
import pandas as pd
import json
import os
import matplotlib.pyplot as plt
from datetime import datetime

# Usar la versión FIJA estable
from klein_master_equation_doppler_extension_fixed import KleinMasterEquationDopplerExtensionFixed

class LIGORealAnalyzer:
    """
    Analizador para datos reales LIGO con extensión Doppler Klein estable.
    """
    
    def __init__(self):
        self.klein = KleinMasterEquationDopplerExtensionFixed(
            distance_unit='Mpc',
            enable_logging=True,
            performance_mode='robust'
        )
        self.timestamp = datetime.now().isoformat()
        print("🔬 LIGO Real Analyzer initialized with STABLE solver")
    
    def load_gwtc3_data(self):
        """
        Carga datos GWTC-3 reales.
        """
        data_path = "../teoria_refinada/datos/ligo/gwtc3_events.csv"
        
        if not os.path.exists(data_path):
            print(f"❌ No se encontraron datos GWTC-3 en {data_path}")
            return None
        
        df = pd.read_csv(data_path)
        print(f"📊 GWTC-3 cargado: {len(df)} eventos confirmados")
        
        # Filtrar eventos con datos completos
        required_cols = ['luminosity_distance', 'total_mass_source', 'redshift']
        df_clean = df.dropna(subset=required_cols)
        
        print(f"✓ {len(df_clean)} eventos con datos completos")
        
        return df_clean
    
    def estimate_energy_radiated(self, df):
        """
        Estima energía radiada desde masa total y otros parámetros.
        """
        # Aproximación: E_rad ≈ 0.05 * M_total * c²
        # Para mergers BBH típicos, ~5% de masa se convierte en ondas GW
        
        energy_estimates = []
        
        for _, event in df.iterrows():
            M_total = event.get('total_mass_source', 30.0)  # M☉
            
            # Factor de eficiencia basado en masas
            mass_ratio = 1.0  # Simplificado
            if 'mass_1_source' in event and 'mass_2_source' in event:
                m1 = event['mass_1_source']
                m2 = event['mass_2_source']
                if m1 > 0 and m2 > 0:
                    mass_ratio = min(m1, m2) / max(m1, m2)
            
            # Eficiencia radiativa (función de mass ratio)
            efficiency = 0.03 + 0.02 * mass_ratio  # 3-5%
            
            E_rad = efficiency * M_total  # En unidades M☉c²
            energy_estimates.append(E_rad)
        
        df['energy_estimated'] = energy_estimates
        return df
    
    def estimate_peculiar_velocities(self, df):
        """
        Estima velocidades peculiares desde redshift y otras observables.
        """
        velocities = []
        
        for _, event in df.iterrows():
            z = event.get('redshift', 0.1)
            
            # Velocidad peculiar típica: ~0.1 * v_Hubble para z pequeños
            # v_Hubble = c * z para z << 1
            v_hubble = min(z, 0.5)  # Cap redshift
            
            # Velocidad peculiar: fluctuaciones ~ 10% de expansión + scatter
            v_peculiar_base = 0.1 * v_hubble
            
            # Añadir scatter basado en propiedades físicas
            if 'chi_eff' in event and pd.notna(event['chi_eff']):
                # Spins altos pueden indicar formación dinámica → más velocidad
                chi_eff = abs(event['chi_eff'])
                velocity_boost = 1.0 + chi_eff * 0.2  # Hasta 20% más
                v_peculiar = v_peculiar_base * velocity_boost
            else:
                v_peculiar = v_peculiar_base
            
            # Cap final a velocidades realistas
            v_peculiar = min(v_peculiar, 0.3)  # Máximo 0.3c
            
            velocities.append(v_peculiar)
        
        df['v_peculiar_estimated'] = velocities
        return df
    
    def run_klein_analysis(self, df):
        """
        Ejecuta análisis Klein en datos GWTC-3 reales.
        """
        print("\n🚀 Ejecutando análisis Klein en GWTC-3...")
        
        results = []
        
        for idx, event in df.iterrows():
            try:
                # Parámetros del evento
                event_name = event.get('commonName', f'Event_{idx}')
                E_initial = event['energy_estimated']
                L_Mpc = event['luminosity_distance']
                v_peculiar = event['v_peculiar_estimated']
                
                # Resolver evolución Klein
                result = self.klein.solve_evolution_robust(
                    E_initial=E_initial,
                    L=L_Mpc,  # La versión fija maneja Mpc automáticamente
                    v_peculiar=v_peculiar,
                    duration=0.1,
                    n_points=100
                )
                
                # Añadir metadatos del evento
                result.update({
                    'event_name': event_name,
                    'event_idx': idx,
                    'mass_total': event.get('total_mass_source', np.nan),
                    'redshift_obs': event.get('redshift', np.nan),
                    'snr_obs': event.get('network_matched_filter_snr', np.nan),
                    'chi_eff_obs': event.get('chi_eff', np.nan)
                })
                
                results.append(result)
                
                if len(results) % 10 == 0:
                    print(f"  ✓ {len(results)}/{len(df)} eventos procesados")
                
            except Exception as e:
                print(f"⚠ Error procesando {event_name}: {e}")
                continue
        
        print(f"✅ {len(results)} eventos Klein analizados")
        return results
    
    def analyze_correlations(self, results):
        """
        Analiza correlaciones en resultados Klein.
        """
        print("\n📊 Analizando correlaciones...")
        
        # Extraer métricas
        energies = [r['energy_initial'] for r in results]
        max_epsilons = [r['max_epsilon'] for r in results]
        max_elevations = [r['max_elevation'] for r in results]
        doppler_factors = [r['doppler_factor'] for r in results]
        doppler_shifts = [r['doppler_shift_hz'] for r in results]
        velocities = [r['peculiar_velocity'] for r in results]
        masses = [r['mass_total'] for r in results]
        redshifts = [r['redshift_obs'] for r in results]
        snrs = [r['snr_obs'] for r in results]
        
        # Filtrar valores válidos
        valid_mask = [np.isfinite(e) and np.isfinite(eps) and np.isfinite(h) and np.isfinite(d) 
                     for e, eps, h, d in zip(energies, max_epsilons, max_elevations, doppler_factors)]
        
        valid_indices = [i for i, valid in enumerate(valid_mask) if valid]
        print(f"✓ {len(valid_indices)}/{len(results)} eventos con datos válidos")
        
        if len(valid_indices) < 2:
            print("⚠ Insuficientes datos válidos para correlaciones")
            return {}
        
        # Arrays filtrados
        E_valid = np.array([energies[i] for i in valid_indices])
        eps_valid = np.array([max_epsilons[i] for i in valid_indices])
        h_valid = np.array([max_elevations[i] for i in valid_indices])
        df_valid = np.array([doppler_factors[i] for i in valid_indices])
        ds_valid = np.array([doppler_shifts[i] for i in valid_indices])
        v_valid = np.array([velocities[i] for i in valid_indices])
        m_valid = np.array([masses[i] for i in valid_indices])
        z_valid = np.array([redshifts[i] for i in valid_indices])
        snr_valid = np.array([snrs[i] for i in valid_indices])
        
        # Calcular correlaciones
        from scipy.stats import pearsonr
        
        correlations = {}
        
        try:
            correlations['energy_deformation'] = pearsonr(E_valid, eps_valid)
            correlations['energy_elevation'] = pearsonr(E_valid, h_valid)
            correlations['velocity_doppler_factor'] = pearsonr(v_valid, df_valid)
            correlations['velocity_doppler_shift'] = pearsonr(v_valid, ds_valid)
            correlations['mass_deformation'] = pearsonr(m_valid, eps_valid)
            correlations['redshift_doppler'] = pearsonr(z_valid, df_valid)
            correlations['snr_deformation'] = pearsonr(snr_valid, eps_valid)
        except Exception as e:
            print(f"⚠ Error calculando correlaciones: {e}")
        
        # Mostrar resultados
        print("\n📈 CORRELACIONES ENCONTRADAS:")
        print("-" * 50)
        for key, (r, p) in correlations.items():
            significance = "***" if p < 0.001 else "**" if p < 0.01 else "*" if p < 0.05 else ""
            print(f"{key:25}: r={r:6.3f}, p={p:.2e} {significance}")
        
        return correlations
    
    def create_diagnostic_plots(self, results, output_dir="results/"):
        """
        Crea plots diagnósticos para datos LIGO reales.
        """
        os.makedirs(output_dir, exist_ok=True)
        print(f"\n📊 Creando plots diagnósticos...")
        
        # Extraer datos
        energies = [r['energy_initial'] for r in results]
        max_epsilons = [r['max_epsilon'] for r in results]
        max_elevations = [r['max_elevation'] for r in results]
        doppler_factors = [r['doppler_factor'] for r in results]
        velocities = [r['peculiar_velocity'] for r in results]
        masses = [r['mass_total'] for r in results]
        states = [r['final_state'] for r in results]
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        
        # Plot 1: Energía vs Deformación
        ax1.scatter(energies, max_epsilons, alpha=0.7, s=60, c='blue')
        ax1.set_xlabel('Energía Radiada (M☉c²)')
        ax1.set_ylabel('Deformación Máxima ε')
        ax1.set_title('GWTC-3: Energía vs Deformación Klein')
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Velocidad vs Doppler
        ax2.scatter(velocities, doppler_factors, alpha=0.7, s=60, c='red')
        ax2.set_xlabel('Velocidad Peculiar (c)')
        ax2.set_ylabel('Factor Doppler')
        ax2.set_title('GWTC-3: Velocidad vs Factor Doppler')
        ax2.grid(True, alpha=0.3)
        
        # Plot 3: Masa vs Deformación (colored by state)
        state_colors = {'Klein_relajada': 'blue', 'Klein_deformada': 'orange', 'Klein_extrema': 'red'}
        for state in set(states):
            mask = [s == state for s in states]
            state_masses = [m for m, include in zip(masses, mask) if include]
            state_eps = [e for e, include in zip(max_epsilons, mask) if include]
            ax3.scatter(state_masses, state_eps, alpha=0.7, s=60, 
                       label=state, color=state_colors.get(state, 'gray'))
        
        ax3.set_xlabel('Masa Total (M☉)')
        ax3.set_ylabel('Deformación Máxima ε')
        ax3.set_title('GWTC-3: Masa vs Deformación (por Estado)')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # Plot 4: Elevación vs Energía
        ax4.scatter(energies, max_elevations, alpha=0.7, s=60, c='green')
        ax4.set_xlabel('Energía Radiada (M☉c²)')
        ax4.set_ylabel('Elevación Máxima (km)')
        ax4.set_title('GWTC-3: Energía vs Elevación Klein')
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # Guardar
        plot_path = os.path.join(output_dir, 'gwtc3_klein_analysis.png')
        plt.savefig(plot_path, dpi=300, bbox_inches='tight')
        print(f"✅ Plots guardados: {plot_path}")
        plt.show()
        
        return plot_path
    
    def save_results(self, results, correlations, output_dir="results/"):
        """
        Guarda resultados del análisis.
        """
        os.makedirs(output_dir, exist_ok=True)
        
        # Preparar datos para JSON
        results_clean = []
        for result in results:
            result_clean = {}
            for key, value in result.items():
                if isinstance(value, np.ndarray):
                    result_clean[key] = value.tolist()
                elif isinstance(value, (np.integer, np.floating)):
                    result_clean[key] = float(value)
                else:
                    result_clean[key] = value
            results_clean.append(result_clean)
        
        # Resultados principales
        output_data = {
            'analysis_metadata': {
                'timestamp': self.timestamp,
                'n_events_total': len(results),
                'klein_version': 'fixed_stable',
                'dataset': 'GWTC-3_real'
            },
            'correlations': {
                key: {'correlation': float(r), 'p_value': float(p)} 
                for key, (r, p) in correlations.items()
            },
            'detailed_results': results_clean
        }
        
        # Guardar
        results_path = os.path.join(output_dir, 'gwtc3_klein_analysis.json')
        with open(results_path, 'w') as f:
            json.dump(output_data, f, indent=2, default=str)
        
        print(f"✅ Resultados guardados: {results_path}")
        return results_path

def main():
    """
    Ejecuta análisis completo GWTC-3 con Klein Doppler Extension.
    """
    print("🌌 ANÁLISIS GWTC-3 CON EXTENSIÓN DOPPLER-KLEIN ESTABLE")
    print("=" * 70)
    
    # Inicializar
    analyzer = LIGORealAnalyzer()
    
    # Cargar datos
    df = analyzer.load_gwtc3_data()
    if df is None or len(df) == 0:
        print("❌ No se pudieron cargar datos GWTC-3")
        return
    
    # Preparar datos
    print("\n🔧 Preparando datos para análisis Klein...")
    df = analyzer.estimate_energy_radiated(df)
    df = analyzer.estimate_peculiar_velocities(df)
    
    print(f"✓ Energías estimadas: {df['energy_estimated'].min():.2f} - {df['energy_estimated'].max():.2f} M☉c²")
    print(f"✓ Velocidades estimadas: {df['v_peculiar_estimated'].min():.3f} - {df['v_peculiar_estimated'].max():.3f} c")
    
    # Análisis Klein
    results = analyzer.run_klein_analysis(df)
    
    if not results:
        print("❌ No se obtuvieron resultados válidos")
        return
    
    # Análisis correlaciones
    correlations = analyzer.analyze_correlations(results)
    
    # Plots y guardado
    plot_path = analyzer.create_diagnostic_plots(results)
    results_path = analyzer.save_results(results, correlations)
    
    # Resumen final
    print("\n🎉 ANÁLISIS COMPLETADO")
    print("=" * 40)
    print(f"✅ {len(results)} eventos GWTC-3 analizados con Klein Theory")
    print(f"📊 Plots: {plot_path}")
    print(f"💾 Datos: {results_path}")
    
    # Destacar correlaciones significativas
    if correlations:
        significant_corr = [(k, r, p) for k, (r, p) in correlations.items() if p < 0.05]
        if significant_corr:
            print(f"\n🔥 CORRELACIONES SIGNIFICATIVAS (p<0.05):")
            for name, r, p in significant_corr:
                print(f"  • {name}: r={r:.3f}, p={p:.2e}")
    
    print("\n🚀 Klein Theory aplicada exitosamente a datos reales LIGO!")

if __name__ == "__main__":
    main()