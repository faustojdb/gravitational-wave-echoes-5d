#!/usr/bin/env python3
"""
COMPARACIÓN LIGO CON MODELO KLEIN SOFISTICADO
============================================

Integra el modelo Klein sofisticado con datos LIGO reales
para obtener diferenciación real entre diferentes radios Klein.
"""

import numpy as np
import h5py
from pathlib import Path
import json
from sophisticated_klein_model import SophisticatedMultipleRadiusComparator

# Constantes
m_electron = 9.10938356e-31  # kg
c = 299792458  # m/s

def load_ligo_data_for_sophisticated_analysis(event_names=None):
    """
    Cargar datos LIGO para análisis sofisticado.
    
    Args:
        event_names (list): Eventos a cargar
        
    Returns:
        dict: Datos organizados por evento/detector
    """
    
    if event_names is None:
        event_names = ['GW200115', 'GW200128']
    
    data_dir = Path("/mnt/d/Multidimensional_Theory_Simulations/multidimensional-theory/gravitational-wave-echoes-5d/S2_SPHERICAL_SPACETIME_THEORY/5_Code/ligo_real_data/strain_data")
    
    strain_data_dict = {}
    
    for event_name in event_names:
        print(f"\n📡 Cargando datos para {event_name}...")
        
        event_data = {}
        
        # Buscar archivos H1 y L1
        for detector in ['H1', 'L1']:
            pattern = f"{event_name}*{detector}*.hdf5"
            files = list(data_dir.glob(pattern))
            
            if files:
                file_path = files[0]  # Tomar el primero si hay múltiples
                
                try:
                    with h5py.File(file_path, 'r') as f:
                        strain = f['strain'][:]
                        dt = 1.0 / f.attrs['sample_rate']
                        gps_time = f.attrs['gps_time']
                        
                        event_data[detector] = {
                            'strain': strain,
                            'dt': dt,
                            'gps_time': gps_time,
                            'file_name': file_path.name
                        }
                        
                        print(f"   ✅ {detector}: {len(strain)} samples, dt={dt:.2e}s")
                        
                except Exception as e:
                    print(f"   ❌ Error cargando {detector}: {e}")
            else:
                print(f"   ⚠️ No encontrado archivo para {detector}")
        
        if event_data:
            strain_data_dict[event_name] = event_data
        else:
            print(f"   ❌ No se pudieron cargar datos para {event_name}")
    
    return strain_data_dict

def main():
    """Función principal de comparación sofisticada."""
    
    print("="*80)
    print("COMPARACIÓN LIGO CON MODELO KLEIN SOFISTICADO")
    print("¡Ahora con física fundamental que diferencia radios Klein!")
    print("="*80)
    
    # 1. DEFINIR RADIOS KLEIN A COMPARAR
    sophisticated_radii = {
        'Klein_Empírico_Original': 8400e3,        # m
        'Klein_Fundamental_Básico': 8187e3,       # m  
        'Klein_Fundamental_m_e_c2': (m_electron * c**2 * 1e20),  # m
        'Klein_Predicción_Inicial': 38323e3,      # m
        'Klein_Modelo_Corregido': 419.3e3,       # m
        'Klein_Auto_Intersección': 8187e3 / np.pi,  # m
        'Klein_Medio_Geométrico': np.sqrt(8187e3 * 419.3e3),  # m
        'Klein_Test_1000km': 1000e3,             # m
        'Klein_Test_2000km': 2000e3,             # m
        'Klein_Test_5000km': 5000e3              # m
    }
    
    print(f"\n🔬 RADIOS KLEIN PARA ANÁLISIS SOFISTICADO:")
    print(f"{'Nombre':<25} {'Radio (km)':<10} {'Freq Klein (Hz)'}")
    print("-" * 55)
    for name, radius in sophisticated_radii.items():
        f_klein = c / radius / (2 * np.pi)
        print(f"{name:<25} {radius/1000:<10.1f} {f_klein:<10.2e}")
    
    # 2. CREAR COMPARADOR SOFISTICADO
    print(f"\n⚙️ INICIALIZANDO COMPARADOR SOFISTICADO...")
    comparator = SophisticatedMultipleRadiusComparator(sophisticated_radii)
    
    # 3. CARGAR DATOS LIGO
    print(f"\n📊 CARGANDO DATOS LIGO...")
    strain_data = load_ligo_data_for_sophisticated_analysis(['GW200115', 'GW200128'])
    
    if not strain_data:
        print(f"❌ Error: No se pudieron cargar datos LIGO")
        return
    
    print(f"✅ Datos cargados para {len(strain_data)} eventos")
    
    # 4. EJECUTAR COMPARACIÓN SOFISTICADA
    print(f"\n🚀 EJECUTANDO COMPARACIÓN SOFISTICADA...")
    comparison_results = comparator.compare_all_models_on_data(strain_data)
    
    # 5. CALCULAR ESTADÍSTICAS COMPARATIVAS
    print(f"\n📈 CALCULANDO ESTADÍSTICAS...")
    model_statistics = comparator.calculate_comparative_statistics(comparison_results)
    
    # 6. IMPRIMIR RESULTADOS SOFISTICADOS
    print(f"\n" + "="*50)
    print("RESULTADOS COMPARACIÓN SOFISTICADA")
    print("="*50)
    
    comparator.print_sophisticated_results(model_statistics)
    
    # 7. GUARDAR RESULTADOS COMPLETOS
    output_file = "/mnt/d/Multidimensional_Theory_Simulations/multidimensional-theory/gravitational-wave-echoes-5d/FUNDAMENTAL_RADIUS_INVESTIGATION/results/sophisticated_comparison_results.json"
    
    # Preparar datos para JSON
    def convert_for_json(obj):
        if isinstance(obj, dict):
            return {k: convert_for_json(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [convert_for_json(v) for v in obj]
        elif isinstance(obj, (np.integer, np.floating, np.complexfloating)):
            return float(obj.real) if hasattr(obj, 'real') else float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, (np.bool_, bool)):
            return bool(obj)
        else:
            return obj
    
    results_to_save = {
        'metadata': {
            'analysis_type': 'sophisticated_klein_comparison',
            'radii_tested': {k: v/1000 for k, v in sophisticated_radii.items()},  # km
            'events_analyzed': list(strain_data.keys()),
            'model_features': [
                'Resonancia específica por R_Klein',
                'Correcciones topológicas Klein bottle',
                '137 modos electromagnéticos',
                'Amplificación dependiente intensidad GW',
                'Detección sofisticada activación',
                'Análisis espectral avanzado'
            ]
        },
        'detailed_results': comparison_results,
        'statistical_summary': model_statistics
    }
    
    json_safe_results = convert_for_json(results_to_save)
    
    with open(output_file, 'w') as f:
        json.dump(json_safe_results, f, indent=2)
    
    print(f"\n💾 Resultados completos guardados en:")
    print(f"   {output_file}")
    
    # 8. ANÁLISIS DE CONCLUSIONES
    print(f"\n" + "="*60)
    print("ANÁLISIS DE CONCLUSIONES")
    print("="*60)
    
    # Encontrar el mejor modelo
    valid_models = {k: v for k, v in model_statistics.items() if 'error' not in v}
    
    if valid_models:
        best_model_name = max(valid_models.keys(), 
                             key=lambda x: valid_models[x].get('performance_score', 0))
        best_stats = valid_models[best_model_name]
        
        print(f"\n🏆 MODELO KLEIN ÓPTIMO IDENTIFICADO:")
        print(f"   Nombre: {best_model_name}")
        print(f"   R_Klein: {best_stats['R_Klein_km']:.1f} km")
        print(f"   Performance Score: {best_stats['performance_score']:.4f}")
        
        # Evaluación de la diferenciación
        enhancement_values = [v.get('mean_snr_enhancement', 1.0) for v in valid_models.values()]
        enhancement_std = np.std(enhancement_values)
        
        print(f"\n📊 EVALUACIÓN DE DIFERENCIACIÓN:")
        print(f"   Rango SNR Enhancement: {min(enhancement_values):.3f} - {max(enhancement_values):.3f}")
        print(f"   Desviación estándar: {enhancement_std:.4f}")
        
        if enhancement_std > 0.01:
            print(f"   ✅ DIFERENCIACIÓN EXITOSA: Los diferentes radios Klein muestran comportamientos distintos")
        else:
            print(f"   ⚠️ DIFERENCIACIÓN LIMITADA: Los modelos aún son muy similares")
        
        # Recomendaciones
        print(f"\n💡 RECOMENDACIONES:")
        
        if best_stats['mean_snr_enhancement'] > 1.1:
            print(f"   ✅ El modelo Klein sofisticado muestra amplificación significativa")
        else:
            print(f"   📋 Considerar ajustes adicionales en parámetros de resonancia")
        
        if best_stats['mean_resonance_strength'] > 0.3:
            print(f"   ✅ Resonancia electromagnética fuerte detectada")
        else:
            print(f"   📋 Optimizar parámetros de resonancia electromagnética")
    
    else:
        print(f"❌ No se pudieron obtener resultados válidos")
    
    print(f"\n🎯 ¡COMPARACIÓN SOFISTICADA COMPLETADA!")
    print(f"El modelo ahora incorpora física fundamental realista para diferenciación de radios Klein.")

if __name__ == "__main__":
    main()