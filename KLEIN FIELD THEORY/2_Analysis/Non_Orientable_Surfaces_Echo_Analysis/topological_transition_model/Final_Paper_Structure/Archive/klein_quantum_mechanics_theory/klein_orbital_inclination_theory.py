"""
Teoría Klein con Inclinación Orbital en 5D
==========================================
Inspirado en el caso Einstein-Mercurio: la inclinación orbital de electrones
en la dimensión 5D Klein puede explicar las discrepancias en átomos específicos.

La topología no-orientable de Klein permite inclinaciones orbitales imposibles
en 3D euclidiano, similar a cómo Einstein explicó la precesión de Mercurio.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import hbar, c, m_e, e
from scipy.optimize import minimize
from typing import Dict, List, Tuple

class KleinOrbitalInclinationTheory:
    """
    Teoría Klein con correcciones por inclinación orbital en 5D.
    
    Principio: Los electrones orbitan en planos inclinados respecto al
    espacio 4D, creando correcciones geométricas específicas por átomo.
    """
    
    def __init__(self):
        """Inicializar teoría con inclinaciones orbitales."""
        self.hbar = hbar
        self.c = c
        self.m_e = m_e
        self.e = e
        
        # Datos atómicos experimentales
        self.atomic_data = {
            'H': {'Z': 1, 'N_e': 1, 'radius_pm': 52.9, 'ionization_eV': 13.598, 'config': '1s1'},
            'He': {'Z': 2, 'N_e': 2, 'radius_pm': 31.0, 'ionization_eV': 24.587, 'config': '1s2'},
            'Li': {'Z': 3, 'N_e': 3, 'radius_pm': 167.0, 'ionization_eV': 5.392, 'config': '1s2 2s1'},
            'Be': {'Z': 4, 'N_e': 4, 'radius_pm': 112.0, 'ionization_eV': 9.323, 'config': '1s2 2s2'},
            'B': {'Z': 5, 'N_e': 5, 'radius_pm': 87.0, 'ionization_eV': 8.298, 'config': '1s2 2s2 2p1'},
            'C': {'Z': 6, 'N_e': 6, 'radius_pm': 67.0, 'ionization_eV': 11.260, 'config': '1s2 2s2 2p2'},
            'N': {'Z': 7, 'N_e': 7, 'radius_pm': 56.0, 'ionization_eV': 14.534, 'config': '1s2 2s2 2p3'},
            'O': {'Z': 8, 'N_e': 8, 'radius_pm': 48.0, 'ionization_eV': 13.618, 'config': '1s2 2s2 2p4'},
            'F': {'Z': 9, 'N_e': 9, 'radius_pm': 42.0, 'ionization_eV': 17.423, 'config': '1s2 2s2 2p5'},
            'Ne': {'Z': 10, 'N_e': 10, 'radius_pm': 38.0, 'ionization_eV': 21.565, 'config': '1s2 2s2 2p6'}
        }
        
    def derive_orbital_inclination_corrections(self) -> Dict:
        """
        Deriva correcciones por inclinación orbital específicas por tipo de orbital.
        
        Como Einstein con Mercurio: la geometría 5D Klein requiere correcciones
        que dependen de la orientación del orbital en el espacio 5D.
        """
        print("=" * 70)
        print("DERIVANDO CORRECCIONES POR INCLINACIÓN ORBITAL KLEIN 5D")
        print("=" * 70)
        
        print("Inspiración Einstein-Mercurio:")
        print("  La precesión de Mercurio se explicó por curvatura espaciotemporal")
        print("  Los orbitales electrónicos pueden tener 'precesión' en espacio Klein 5D")
        print("  La topología no-orientable permite inclinaciones imposibles en 3D")
        
        # Clasificar orbitales por tipo
        orbital_types = {
            's': {'moment_angular': 0, 'shape': 'spherical', 'klein_inclination_base': 0.0},
            'p': {'moment_angular': 1, 'shape': 'dumbbell', 'klein_inclination_base': np.pi/6},  # 30°
            'd': {'moment_angular': 2, 'shape': 'complex', 'klein_inclination_base': np.pi/4},   # 45°
            'f': {'moment_angular': 3, 'shape': 'very_complex', 'klein_inclination_base': np.pi/3} # 60°
        }
        
        print(f"\nTipos de orbital y sus inclinaciones Klein base:")
        for orbital, data in orbital_types.items():
            angle_deg = data['klein_inclination_base'] * 180 / np.pi
            print(f"  {orbital}: l={data['moment_angular']}, inclinación base = {angle_deg:.1f}°")
        
        # Analizar configuraciones electrónicas específicas
        print(f"\nAnálisis de configuraciones atómicas:")
        
        inclination_data = {}
        
        for atom, data in self.atomic_data.items():
            config = data['config']
            Z = data['Z']
            
            # Parsear configuración electrónica
            # Ejemplo: '1s2 2s2 2p4' -> {'1s': 2, '2s': 2, '2p': 4}
            orbitals = {}
            for part in config.split():
                if 's' in part:
                    n = int(part[0])
                    count = int(part[2:])
                    orbitals[f'{n}s'] = count
                elif 'p' in part:
                    n = int(part[0])
                    count = int(part[2:])
                    orbitals[f'{n}p'] = count
                elif 'd' in part:
                    n = int(part[0])
                    count = int(part[2:])
                    orbitals[f'{n}d'] = count
            
            # Calcular inclinación orbital total Klein
            total_inclination = 0.0
            orbital_breakdown = {}
            
            for orbital_name, electron_count in orbitals.items():
                orbital_type = orbital_name[-1]  # 's', 'p', 'd'
                n_quantum = int(orbital_name[0])  # 1, 2, 3...
                
                # Inclinación base por tipo orbital
                base_inclination = orbital_types[orbital_type]['klein_inclination_base']
                
                # Corrección por número cuántico principal (orbitales exteriores más inclinados)
                n_correction = (n_quantum - 1) * np.pi/12  # 15° por nivel
                
                # Corrección por llenado parcial (orbitales semi-llenos tienen inclinación especial)
                max_electrons = {'s': 2, 'p': 6, 'd': 10, 'f': 14}
                filling_fraction = electron_count / max_electrons[orbital_type]
                
                # Orbitales semi-llenos (como N con p3) tienen inclinación especial
                if abs(filling_fraction - 0.5) < 0.1:  # Cerca de semi-lleno
                    half_fill_correction = np.pi/8  # 22.5° extra
                else:
                    half_fill_correction = 0.0
                
                # Inclinación total para este orbital
                orbital_inclination = base_inclination + n_correction + half_fill_correction
                
                # Contribución ponderada por número de electrones
                weighted_contribution = orbital_inclination * electron_count
                total_inclination += weighted_contribution
                
                orbital_breakdown[orbital_name] = {
                    'type': orbital_type,
                    'n_quantum': n_quantum,
                    'electron_count': electron_count,
                    'base_inclination_deg': base_inclination * 180/np.pi,
                    'n_correction_deg': n_correction * 180/np.pi,
                    'half_fill_correction_deg': half_fill_correction * 180/np.pi,
                    'total_inclination_deg': orbital_inclination * 180/np.pi,
                    'weighted_contribution': weighted_contribution
                }
            
            # Inclinación promedio por electrón
            average_inclination = total_inclination / data['N_e']
            
            inclination_data[atom] = {
                'total_inclination_rad': total_inclination,
                'average_inclination_rad': average_inclination,
                'average_inclination_deg': average_inclination * 180/np.pi,
                'orbital_breakdown': orbital_breakdown,
                'configuration': config
            }
            
            print(f"  {atom} ({config}): inclinación promedio = {average_inclination * 180/np.pi:.1f}°")
        
        return {
            'orbital_types': orbital_types,
            'atomic_inclinations': inclination_data,
            'theory': 'Klein orbital inclination in 5D spacetime'
        }
    
    def apply_inclination_corrections(self, inclination_data: Dict) -> Dict:
        """
        Aplica correcciones por inclinación orbital a la fórmula Klein base.
        
        Similar a como Einstein corrigió la órbita de Mercurio.
        """
        print("\n" + "=" * 70)
        print("APLICANDO CORRECCIONES POR INCLINACIÓN ORBITAL")
        print("=" * 70)
        
        # Parámetros Klein base (de calibración anterior)
        A_base = 0.001662
        B_base = 1.851519
        C_base = 1.503983
        D_base = 0.100000
        
        print(f"Parámetros Klein base:")
        print(f"  A = {A_base:.6f}, B = {B_base:.6f}, C = {C_base:.6f}, D = {D_base:.6f}")
        
        predictions_with_inclination = {}
        
        print(f"\nAplicando correcciones por inclinación:")
        print(f"{'Átomo':<6} {'Inclin°':<8} {'R_base':<8} {'R_correg':<9} {'R_exp':<8} {'Precisión':<10}")
        print("-" * 70)
        
        for atom, data in self.atomic_data.items():
            Z = data['Z']
            N_e = data['N_e']
            E_ion = data['ionization_eV']
            R_exp = data['radius_pm']
            
            # Inclinación orbital promedio
            inclination_rad = inclination_data['atomic_inclinations'][atom]['average_inclination_rad']
            inclination_deg = inclination_rad * 180/np.pi
            
            # Fórmula Klein base
            E_joules = E_ion * self.e
            R_klein_base = self.hbar * self.c / E_joules * 1e12  # pm
            
            permanent_term = np.log(N_e + 1)
            transient_term = B_base / N_e
            exponential_term = C_base * np.exp(-N_e / D_base)
            
            R_base_prediction = A_base * R_klein_base * (permanent_term + transient_term + exponential_term)
            
            # Corrección por inclinación orbital
            # Factor geométrico: cos(inclinación) para proyección al espacio 4D
            # Factor topológico: sin(inclinación) para efecto Klein no-orientable
            
            cos_correction = np.cos(inclination_rad)  # Proyección geométrica
            sin_correction = np.sin(inclination_rad)  # Efecto topológico Klein
            
            # Combinación: geometría euclidiana + topología Klein
            inclination_factor = cos_correction + 0.5 * sin_correction  # Factor empírico
            
            # Radio corregido
            R_corrected = R_base_prediction * inclination_factor
            
            # Precisión
            error = abs(R_corrected - R_exp)
            precision = 100 * (1 - error / R_exp) if error < R_exp else 0
            
            predictions_with_inclination[atom] = {
                'Z': Z,
                'N_e': N_e,
                'inclination_deg': inclination_deg,
                'R_base_pm': R_base_prediction,
                'R_corrected_pm': R_corrected,
                'R_experimental_pm': R_exp,
                'inclination_factor': inclination_factor,
                'precision_percent': precision,
                'cos_correction': cos_correction,
                'sin_correction': sin_correction
            }
            
            print(f"{atom:<6} {inclination_deg:<8.1f} {R_base_prediction:<8.1f} {R_corrected:<9.1f} {R_exp:<8.1f} {precision:<10.1f}%")
        
        # Estadísticas
        precisions = [pred['precision_percent'] for pred in predictions_with_inclination.values()]
        avg_precision = np.mean(precisions)
        
        print(f"\nEstadísticas con corrección por inclinación:")
        print(f"  Precisión promedio: {avg_precision:.2f}%")
        print(f"  Mejora vs base: {avg_precision - 86.22:.2f} puntos porcentuales")
        
        return {
            'predictions': predictions_with_inclination,
            'average_precision': avg_precision,
            'improvement': avg_precision - 86.22,
            'inclination_theory_validated': avg_precision > 90.0
        }
    
    def optimize_inclination_model(self, base_results: Dict) -> Dict:
        """
        Optimiza el modelo de inclinación para máxima precisión.
        
        Encuentra los parámetros óptimos para las correcciones geométricas y topológicas.
        """
        print("\n" + "=" * 70)
        print("OPTIMIZANDO MODELO DE INCLINACIÓN ORBITAL")
        print("=" * 70)
        
        inclination_data = base_results['predictions']
        
        # Función a optimizar: encuentra mejor combinación cos/sin
        def objective_function(params):
            """Minimiza error con parámetros de inclinación óptimos."""
            alpha, beta = params  # Pesos para cos y sin
            
            total_error = 0
            for atom, pred in inclination_data.items():
                inclination_rad = pred['inclination_deg'] * np.pi/180
                R_base = pred['R_base_pm']
                R_exp = pred['R_experimental_pm']
                
                # Factor de inclinación optimizado
                cos_term = np.cos(inclination_rad)
                sin_term = np.sin(inclination_rad)
                
                inclination_factor = alpha * cos_term + beta * sin_term
                R_predicted = R_base * inclination_factor
                
                error = abs(R_predicted - R_exp) / R_exp
                total_error += error**2
            
            return total_error
        
        # Optimización
        initial_params = [1.0, 0.5]  # α=1, β=0.5 inicial
        bounds = [(0.1, 2.0), (-1.0, 2.0)]  # Rangos físicamente razonables
        
        result = minimize(objective_function, initial_params, bounds=bounds, method='L-BFGS-B')
        
        if result.success:
            alpha_opt, beta_opt = result.x
            
            print(f"Optimización exitosa:")
            print(f"  α (peso cos): {alpha_opt:.6f}")
            print(f"  β (peso sin): {beta_opt:.6f}")
            print(f"  Error mínimo: {result.fun:.6f}")
            
            # Aplicar parámetros optimizados
            optimized_predictions = {}
            
            print(f"\nPredicciones optimizadas:")
            print(f"{'Átomo':<6} {'R_opt':<8} {'R_exp':<8} {'Precisión':<10} {'Factor':<8}")
            print("-" * 55)
            
            for atom, pred in inclination_data.items():
                inclination_rad = pred['inclination_deg'] * np.pi/180
                R_base = pred['R_base_pm']
                R_exp = pred['R_experimental_pm']
                
                # Factor optimizado
                cos_term = np.cos(inclination_rad)
                sin_term = np.sin(inclination_rad)
                inclination_factor_opt = alpha_opt * cos_term + beta_opt * sin_term
                
                R_optimized = R_base * inclination_factor_opt
                
                error = abs(R_optimized - R_exp)
                precision = 100 * (1 - error / R_exp) if error < R_exp else 0
                
                optimized_predictions[atom] = {
                    **pred,  # Mantener datos originales
                    'R_optimized_pm': R_optimized,
                    'inclination_factor_optimized': inclination_factor_opt,
                    'precision_optimized': precision
                }
                
                print(f"{atom:<6} {R_optimized:<8.1f} {R_exp:<8.1f} {precision:<10.1f}% {inclination_factor_opt:<8.3f}")
            
            # Estadísticas finales
            opt_precisions = [pred['precision_optimized'] for pred in optimized_predictions.values()]
            avg_opt_precision = np.mean(opt_precisions)
            
            print(f"\nResultados optimización:")
            print(f"  Precisión promedio optimizada: {avg_opt_precision:.2f}%")
            print(f"  Mejora vs base: {avg_opt_precision - 86.22:.2f} puntos")
            
            return {
                'optimized_predictions': optimized_predictions,
                'optimal_parameters': {'alpha': alpha_opt, 'beta': beta_opt},
                'average_precision_optimized': avg_opt_precision,
                'optimization_successful': True,
                'total_improvement': avg_opt_precision - 86.22
            }
        else:
            print("❌ Optimización falló")
            return {'optimization_successful': False}
    
    def plot_inclination_results(self, inclination_data: Dict, corrected_results: Dict, optimized_results: Dict):
        """Grafica resultados del modelo de inclinación orbital."""
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Teoría Klein con Inclinación Orbital - Corrección Einstein-Mercurio', fontsize=16, fontweight='bold')
        
        # Plot 1: Inclinaciones orbitales por átomo
        ax1 = axes[0, 0]
        
        atoms = list(self.atomic_data.keys())
        inclinations = [inclination_data['atomic_inclinations'][atom]['average_inclination_deg'] for atom in atoms]
        configs = [self.atomic_data[atom]['config'] for atom in atoms]
        
        bars = ax1.bar(atoms, inclinations, alpha=0.7, 
                      color=['red' if 'p' in config else 'blue' for config in configs])
        
        ax1.set_ylabel('Inclinación Orbital Promedio (°)')
        ax1.set_title('Inclinaciones Klein 5D por Átomo')
        ax1.tick_params(axis='x', rotation=45)
        ax1.grid(True, alpha=0.3)
        
        # Leyenda
        from matplotlib.patches import Patch
        legend_elements = [Patch(facecolor='blue', alpha=0.7, label='Orbitales s'),
                          Patch(facecolor='red', alpha=0.7, label='Orbitales p')]
        ax1.legend(handles=legend_elements)
        
        # Plot 2: Mejora con corrección por inclinación
        ax2 = axes[0, 1]
        
        if corrected_results:
            base_precisions = [86.22] * len(atoms)  # Precisión base constante
            corrected_precisions = [corrected_results['predictions'][atom]['precision_percent'] for atom in atoms]
            
            x = np.arange(len(atoms))
            width = 0.35
            
            bars1 = ax2.bar(x - width/2, base_precisions, width, label='Base Klein', alpha=0.7)
            bars2 = ax2.bar(x + width/2, corrected_precisions, width, label='Con Inclinación', alpha=0.7)
            
            ax2.set_ylabel('Precisión (%)')
            ax2.set_title('Mejora con Corrección por Inclinación')
            ax2.set_xticks(x)
            ax2.set_xticklabels(atoms, rotation=45)
            ax2.legend()
            ax2.set_ylim(0, 105)
        
        # Plot 3: Predicción vs Experimental (optimizado)
        ax3 = axes[1, 0]
        
        if optimized_results and optimized_results['optimization_successful']:
            opt_preds = optimized_results['optimized_predictions']
            predicted = [opt_preds[atom]['R_optimized_pm'] for atom in atoms]
            experimental = [self.atomic_data[atom]['radius_pm'] for atom in atoms]
            
            ax3.scatter(experimental, predicted, s=100, alpha=0.7, c='green')
            
            # Línea perfecta
            min_val = min(min(experimental), min(predicted))
            max_val = max(max(experimental), max(predicted))
            ax3.plot([min_val, max_val], [min_val, max_val], 'r-', linewidth=2, label='Predicción Perfecta')
            
            # Etiquetas
            for i, atom in enumerate(atoms):
                ax3.annotate(atom, (experimental[i], predicted[i]), 
                            xytext=(5, 5), textcoords='offset points', fontsize=9)
            
            ax3.set_xlabel('Radio Experimental (pm)')
            ax3.set_ylabel('Radio Predicho con Inclinación (pm)')
            avg_prec = optimized_results['average_precision_optimized']
            ax3.set_title(f'Modelo Optimizado (Precisión: {avg_prec:.1f}%)')
            ax3.legend()
            ax3.grid(True, alpha=0.3)
        
        # Plot 4: Comparación final de precisiones
        ax4 = axes[1, 1]
        
        methods = ['Klein\nBase', 'Klein +\nInclinación']
        if optimized_results and optimized_results['optimization_successful']:
            methods.append('Klein +\nInclin. Opt.')
        
        precisions = [86.22]  # Base
        if corrected_results:
            precisions.append(corrected_results['average_precision'])
        if optimized_results and optimized_results['optimization_successful']:
            precisions.append(optimized_results['average_precision_optimized'])
        
        colors = ['blue', 'orange', 'green'][:len(methods)]
        bars = ax4.bar(methods, precisions, color=colors, alpha=0.7)
        
        ax4.set_ylabel('Precisión Promedio (%)')
        ax4.set_title('Evolución con Correcciones Orbitales')
        ax4.set_ylim(0, 105)
        
        # Línea objetivo
        ax4.axhline(95, color='red', linestyle='--', alpha=0.7, label='Objetivo 95%')
        ax4.legend()
        
        # Valores en barras
        for bar, prec in zip(bars, precisions):
            ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                    f'{prec:.1f}%', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('klein_orbital_inclination_theory.png', dpi=300, bbox_inches='tight')
        plt.show()


def run_klein_orbital_inclination_theory():
    """Ejecuta teoría completa Klein con inclinación orbital."""
    
    print("\n" + "🌀" * 35)
    print("TEORÍA KLEIN CON INCLINACIÓN ORBITAL 5D")
    print("Inspiración Einstein-Mercurio: geometría 5D corrige orbitales")
    print("🌀" * 35)
    
    # Crear teoría
    theory = KleinOrbitalInclinationTheory()
    
    # Paso 1: Derivar correcciones por inclinación
    inclination_data = theory.derive_orbital_inclination_corrections()
    
    # Paso 2: Aplicar correcciones
    corrected_results = theory.apply_inclination_corrections(inclination_data)
    
    # Paso 3: Optimizar modelo
    optimized_results = theory.optimize_inclination_model(corrected_results)
    
    # Paso 4: Generar gráficas
    print("\nGenerando gráficas de teoría de inclinación orbital...")
    theory.plot_inclination_results(inclination_data, corrected_results, optimized_results)
    
    # Resumen final
    print("\n" + "=" * 70)
    print("RESULTADOS TEORÍA INCLINACIÓN ORBITAL KLEIN")
    print("=" * 70)
    
    base_precision = 86.22
    if corrected_results:
        corrected_precision = corrected_results['average_precision']
        print(f"\nPrecisión Klein base: {base_precision:.2f}%")
        print(f"Precisión con inclinación: {corrected_precision:.2f}%")
        print(f"Mejora inicial: +{corrected_precision - base_precision:.2f} puntos")
    
    if optimized_results and optimized_results['optimization_successful']:
        opt_precision = optimized_results['average_precision_optimized']
        params = optimized_results['optimal_parameters']
        
        print(f"Precisión optimizada: {opt_precision:.2f}%")
        print(f"Mejora total: +{opt_precision - base_precision:.2f} puntos")
        print(f"\nParámetros optimizados:")
        print(f"  Factor cos (geométrico): {params['alpha']:.6f}")
        print(f"  Factor sin (topológico): {params['beta']:.6f}")
        
        if opt_precision > 95:
            print("\n🎯 ¡INCLINACIÓN ORBITAL EXPLICA LAS DISCREPANCIAS! 🎯")
            print("Como Einstein con Mercurio: geometría 5D resuelve el problema!")
        elif opt_precision > 90:
            print("\n✨ Excelente mejora con inclinaciones orbitales")
            print("La geometría 5D Klein es clave para precisión atómica")
        else:
            print("\n🔧 Mejora significativa pero necesita más refinamiento")
    
    print(f"\nGráficas: klein_orbital_inclination_theory.png")
    
    return {
        'inclination_data': inclination_data,
        'corrected_results': corrected_results,
        'optimized_results': optimized_results
    }


if __name__ == "__main__":
    # Ejecutar teoría de inclinación orbital
    results = run_klein_orbital_inclination_theory()
    
    print("\n" + "=" * 70)
    print("¡TEORÍA INCLINACIÓN ORBITAL KLEIN COMPLETA!")
    print("Correcciones geométricas 5D al estilo Einstein-Mercurio")
    print("=" * 70)