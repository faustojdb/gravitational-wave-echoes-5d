#!/usr/bin/env python3
"""
VERIFY AND ANALYZE DOWNLOADED LIGO FILES
========================================

Analiza la estructura de los archivos LIGO descargados manualmente
para verificar qué tipo de datos contienen y su estructura.

Date: 26 August, 2025
"""

import h5py
import numpy as np
from pathlib import Path
import json
from typing import Dict, List

class LIGOFileAnalyzer:
    """
    Analiza archivos LIGO descargados para verificar estructura
    """
    
    def __init__(self, data_dir: str = None):
        if data_dir is None:
            data_dir = "/mnt/d/Multidimensional_Theory_Simulations/multidimensional-theory/gravitational-wave-echoes-5d/FUNDAMENTAL_RADIUS_INVESTIGATION/ligo_events"
        
        self.data_dir = Path(data_dir)
        
        print("🔍 LIGO File Structure Analyzer")
        print("=" * 60)
        print(f"📁 Directory: {self.data_dir}")
        print()
    
    def analyze_hdf5_structure(self, filepath: Path) -> Dict:
        """Analiza la estructura de un archivo HDF5"""
        try:
            with h5py.File(filepath, 'r') as f:
                structure = {}
                
                def visit_func(name, obj):
                    if isinstance(obj, h5py.Dataset):
                        structure[name] = {
                            'type': 'dataset',
                            'shape': obj.shape,
                            'dtype': str(obj.dtype),
                            'size': obj.size
                        }
                        
                        # Atributos del dataset
                        attrs = {}
                        for attr_name, attr_val in obj.attrs.items():
                            try:
                                attrs[attr_name] = attr_val.decode() if isinstance(attr_val, bytes) else attr_val
                            except:
                                attrs[attr_name] = str(attr_val)
                        structure[name]['attributes'] = attrs
                        
                    elif isinstance(obj, h5py.Group):
                        structure[name] = {
                            'type': 'group',
                            'keys': list(obj.keys())
                        }
                
                f.visititems(visit_func)
                
                # Atributos del archivo raíz
                root_attrs = {}
                for attr_name, attr_val in f.attrs.items():
                    try:
                        root_attrs[attr_name] = attr_val.decode() if isinstance(attr_val, bytes) else attr_val
                    except:
                        root_attrs[attr_name] = str(attr_val)
                
                return {
                    'filename': filepath.name,
                    'size_bytes': filepath.stat().st_size,
                    'root_keys': list(f.keys()),
                    'root_attributes': root_attrs,
                    'structure': structure
                }
                
        except Exception as e:
            return {
                'filename': filepath.name,
                'error': str(e),
                'size_bytes': filepath.stat().st_size
            }
    
    def check_for_strain_data(self, structure: Dict) -> Dict:
        """Verifica si hay datos strain en la estructura"""
        strain_info = {
            'has_strain': False,
            'strain_datasets': [],
            'potential_event_data': [],
            'catalog_type': 'unknown'
        }
        
        # Buscar datasets que contengan 'strain'
        for path, info in structure.get('structure', {}).items():
            if info['type'] == 'dataset':
                path_lower = path.lower()
                if 'strain' in path_lower:
                    strain_info['strain_datasets'].append({
                        'path': path,
                        'shape': info['shape'],
                        'dtype': info['dtype']
                    })
                    strain_info['has_strain'] = True
                
                # Buscar datos que podrían ser eventos
                if any(keyword in path_lower for keyword in ['event', 'gw', 'mass', 'snr', 'time']):
                    strain_info['potential_event_data'].append({
                        'path': path,
                        'shape': info['shape'],
                        'dtype': info['dtype']
                    })
        
        # Determinar tipo de catálogo
        filename = structure['filename'].lower()
        if 'gwtc' in filename:
            strain_info['catalog_type'] = 'GWTC_catalog'
        elif 'bbhpop' in filename:
            strain_info['catalog_type'] = 'BBH_population'
        elif 'bnspop' in filename:
            strain_info['catalog_type'] = 'BNS_population'
        elif 'imbhpop' in filename:
            strain_info['catalog_type'] = 'IMBH_population'
        elif 'nsbhpop' in filename:
            strain_info['catalog_type'] = 'NSBH_population'
        elif 'mixture' in filename:
            strain_info['catalog_type'] = 'Population_mixture'
        
        return strain_info
    
    def analyze_all_files(self):
        """Analiza todos los archivos HDF5 en el directorio"""
        hdf5_files = list(self.data_dir.glob("*.hdf5"))
        
        if not hdf5_files:
            print("❌ No HDF5 files found")
            return None
        
        print(f"📊 Found {len(hdf5_files)} HDF5 files")
        print("=" * 60)
        
        results = {}
        strain_files = []
        catalog_files = []
        
        for i, filepath in enumerate(hdf5_files):
            print(f"[{i+1}/{len(hdf5_files)}] Analyzing: {filepath.name}")
            
            structure = self.analyze_hdf5_structure(filepath)
            
            if 'error' in structure:
                print(f"   ❌ Error: {structure['error']}")
                continue
            
            strain_info = self.check_for_strain_data(structure)
            
            print(f"   📁 Size: {structure['size_bytes'] / (1024*1024):.1f} MB")
            print(f"   🗂️  Type: {strain_info['catalog_type']}")
            print(f"   📊 Root keys: {structure['root_keys'][:5]}...")
            
            if strain_info['has_strain']:
                print(f"   🌊 Strain datasets: {len(strain_info['strain_datasets'])}")
                strain_files.append(filepath)
            else:
                print(f"   📋 Event data paths: {len(strain_info['potential_event_data'])}")
                catalog_files.append(filepath)
            
            results[filepath.name] = {
                'structure': structure,
                'strain_info': strain_info
            }
            print()
        
        # Resumen final
        print("=" * 60)
        print("📊 ANALYSIS SUMMARY")
        print("=" * 60)
        print(f"✅ Total files analyzed: {len(results)}")
        print(f"🌊 Files with strain data: {len(strain_files)}")
        print(f"📋 Catalog/parameter files: {len(catalog_files)}")
        
        if strain_files:
            print(f"\n🌊 STRAIN DATA FILES:")
            for f in strain_files:
                print(f"   - {f.name}")
        
        if catalog_files:
            print(f"\n📋 CATALOG FILES:")
            for f in catalog_files[:10]:  # Limit display
                catalog_type = results[f.name]['strain_info']['catalog_type']
                print(f"   - {f.name} ({catalog_type})")
            if len(catalog_files) > 10:
                print(f"   ... and {len(catalog_files)-10} more")
        
        # Guardar análisis completo
        analysis_file = self.data_dir / "file_analysis_report.json"
        
        # Convertir Path objects a strings para JSON
        json_results = {}
        for filename, data in results.items():
            json_results[filename] = data
            # Convert any Path objects to strings if needed
        
        with open(analysis_file, 'w') as f:
            json.dump(json_results, f, indent=2, default=str)
        
        print(f"\n💾 Full analysis saved: {analysis_file}")
        
        return {
            'strain_files': strain_files,
            'catalog_files': catalog_files,
            'analysis': results
        }


def main():
    """
    Main execution: analyze downloaded LIGO files
    """
    print("=" * 70)
    print("🔍 ANALYZING DOWNLOADED LIGO FILES")
    print("=" * 70)
    print("Checking structure and content of manually downloaded files...")
    print()
    
    analyzer = LIGOFileAnalyzer()
    results = analyzer.analyze_all_files()
    
    if results:
        if results['strain_files']:
            print(f"\n🎉 Found {len(results['strain_files'])} files with strain data!")
            print("🎯 Next: Rename and organize for Klein analysis")
        else:
            print(f"\n⚠️  No strain data found - these appear to be catalog files")
            print("🔍 Consider downloading actual strain data files")


if __name__ == "__main__":
    main()