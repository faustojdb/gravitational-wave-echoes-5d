#!/usr/bin/env python3
"""
EXTRACT INDIVIDUAL EVENTS FROM GWTC CATALOGS
=============================================

Extrae información de eventos individuales desde los catálogos GWTC
descargados y los organiza para análisis Klein.

Date: 26 August, 2025
"""

import h5py
import pandas as pd
import numpy as np
from pathlib import Path
import json
from typing import Dict, List, Optional
import re

class GWTCEventExtractor:
    """
    Extrae eventos individuales desde catálogos GWTC
    """
    
    def __init__(self, catalog_dir: str = None, output_dir: str = None):
        if catalog_dir is None:
            catalog_dir = "/mnt/d/Multidimensional_Theory_Simulations/multidimensional-theory/gravitational-wave-echoes-5d/FUNDAMENTAL_RADIUS_INVESTIGATION/ligo_events"
        
        if output_dir is None:
            output_dir = "/mnt/d/Multidimensional_Theory_Simulations/multidimensional-theory/gravitational-wave-echoes-5d/FUNDAMENTAL_RADIUS_INVESTIGATION/extracted_events"
        
        self.catalog_dir = Path(catalog_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        print("📊 GWTC Event Extractor")
        print("=" * 60)
        print(f"📁 Catalogs: {self.catalog_dir}")
        print(f"📁 Output: {self.output_dir}")
        print()
    
    def extract_events_from_gwtc_catalog(self, filepath: Path) -> List[Dict]:
        """Extrae eventos individuales de un catálogo GWTC"""
        
        events = []
        
        try:
            with h5py.File(filepath, 'r') as f:
                print(f"📋 Analyzing catalog: {filepath.name}")
                print(f"   Root keys: {list(f.keys())}")
                
                # Buscar datasets que contengan información de eventos
                event_datasets = []
                
                def find_event_data(name, obj):
                    if isinstance(obj, h5py.Dataset):
                        # Buscar datasets con información de eventos
                        name_lower = name.lower()
                        if any(keyword in name_lower for keyword in [
                            'event', 'gw', 'mass', 'snr', 'time', 'distance', 
                            'chi', 'spin', 'luminosity', 'redshift'
                        ]):
                            event_datasets.append((name, obj))
                
                f.visititems(find_event_data)
                
                print(f"   Found {len(event_datasets)} potential event datasets")
                
                # Analizar cada dataset
                for dataset_name, dataset in event_datasets:
                    print(f"   📊 Dataset: {dataset_name}")
                    print(f"      Shape: {dataset.shape}, Type: {dataset.dtype}")
                    
                    # Si es un dataset estructurado (con nombres de campos)
                    if dataset.dtype.names:
                        print(f"      Fields: {list(dataset.dtype.names)[:10]}...")
                        
                        # Extraer datos
                        data = dataset[:]
                        
                        # Convertir a lista de eventos
                        for i, record in enumerate(data):
                            event = {}
                            for field_name in dataset.dtype.names:
                                value = record[field_name]
                                
                                # Manejar diferentes tipos de datos
                                if isinstance(value, bytes):
                                    try:
                                        event[field_name] = value.decode('utf-8')
                                    except:
                                        event[field_name] = str(value)
                                elif isinstance(value, np.ndarray):
                                    if value.size == 1:
                                        event[field_name] = float(value)
                                    else:
                                        event[field_name] = value.tolist()
                                elif np.isscalar(value):
                                    if np.isnan(value) or np.isinf(value):
                                        event[field_name] = None
                                    else:
                                        event[field_name] = float(value)
                                else:
                                    event[field_name] = str(value)
                            
                            event['source_catalog'] = filepath.name
                            event['source_dataset'] = dataset_name
                            events.append(event)
                    
                    else:
                        # Dataset simple - intentar extraer información
                        print(f"      Simple dataset with {len(dataset)} entries")
        
        except Exception as e:
            print(f"   ❌ Error reading {filepath.name}: {e}")
        
        return events
    
    def merge_and_clean_events(self, all_events: List[Dict]) -> pd.DataFrame:
        """Une y limpia todos los eventos extraídos"""
        
        if not all_events:
            return pd.DataFrame()
        
        print(f"🔄 Processing {len(all_events)} raw event records...")
        
        # Convertir a DataFrame
        df = pd.DataFrame(all_events)
        
        print(f"   Initial columns: {len(df.columns)}")
        print(f"   Sample columns: {list(df.columns)[:10]}...")
        
        # Identificar eventos únicos por nombre
        name_columns = [col for col in df.columns if 'name' in col.lower() or 'event' in col.lower()]
        print(f"   Name columns found: {name_columns}")
        
        if name_columns:
            # Usar la primera columna de nombre encontrada
            primary_name_col = name_columns[0]
            
            # Eliminar duplicados por nombre de evento
            df_unique = df.drop_duplicates(subset=[primary_name_col])
            print(f"   Unique events: {len(df_unique)}")
            
            # Renombrar columna principal
            df_unique = df_unique.rename(columns={primary_name_col: 'event_name'})
        else:
            # Si no hay columna de nombre, usar índice
            df_unique = df.copy()
            df_unique['event_name'] = df_unique.index.astype(str)
        
        # Identificar columnas importantes
        important_columns = []
        column_mapping = {
            'mass': ['mass_1_source', 'mass_2_source', 'mass_1', 'mass_2', 'chirp_mass'],
            'time': ['gps_time', 'gps', 'time', 'tc'],
            'snr': ['snr', 'network_matched_filter_snr', 'optimal_snr'],
            'distance': ['luminosity_distance', 'distance', 'dist'],
            'chi': ['chi_eff', 'chi_p', 'chi_1', 'chi_2'],
            'redshift': ['redshift', 'z']
        }
        
        for category, possible_names in column_mapping.items():
            found_cols = [col for col in df_unique.columns 
                         if any(pname.lower() in col.lower() for pname in possible_names)]
            important_columns.extend(found_cols)
        
        # Mantener columnas importantes + metadatos
        meta_columns = ['event_name', 'source_catalog', 'source_dataset']
        keep_columns = list(set(important_columns + meta_columns))
        keep_columns = [col for col in keep_columns if col in df_unique.columns]
        
        df_clean = df_unique[keep_columns].copy()
        
        print(f"   Final columns: {len(df_clean.columns)}")
        print(f"   Final events: {len(df_clean)}")
        
        return df_clean
    
    def extract_all_catalogs(self):
        """Extrae eventos de todos los catálogos disponibles"""
        
        catalog_files = list(self.catalog_dir.glob("*.hdf5"))
        
        if not catalog_files:
            print("❌ No catalog files found")
            return None
        
        # Filtrar solo catálogos GWTC (no population studies)
        gwtc_files = [f for f in catalog_files if 'gwtc' in f.name.lower()]
        
        if not gwtc_files:
            print("⚠️  No GWTC catalog files found, using all available")
            gwtc_files = catalog_files
        
        print(f"📊 Processing {len(gwtc_files)} catalog files...")
        print("=" * 60)
        
        all_events = []
        
        for i, catalog_file in enumerate(gwtc_files):
            print(f"\n[{i+1}/{len(gwtc_files)}]")
            events = self.extract_events_from_gwtc_catalog(catalog_file)
            print(f"   Extracted: {len(events)} events")
            all_events.extend(events)
        
        if not all_events:
            print("\n❌ No events extracted from any catalog")
            return None
        
        print(f"\n🔄 Merging and cleaning {len(all_events)} total records...")
        
        # Merge y limpiar eventos
        df_events = self.merge_and_clean_events(all_events)
        
        if df_events.empty:
            print("❌ No events after cleaning")
            return None
        
        # Guardar resultados
        events_file = self.output_dir / "extracted_events.csv"
        df_events.to_csv(events_file, index=False)
        
        # Guardar también como JSON para preservar estructura completa
        events_json = self.output_dir / "extracted_events.json"
        df_events.to_json(events_json, orient='records', indent=2)
        
        # Estadísticas finales
        print("\n" + "=" * 60)
        print("📊 EXTRACTION SUMMARY")
        print("=" * 60)
        print(f"✅ Total unique events: {len(df_events)}")
        print(f"📁 Saved to: {events_file}")
        
        # Mostrar sample de eventos
        print(f"\n🌊 Sample Events:")
        for i, row in df_events.head(5).iterrows():
            name = row.get('event_name', f'Event_{i}')
            print(f"   - {name}")
        
        # Mostrar columnas disponibles
        print(f"\n📊 Available data columns:")
        for col in sorted(df_events.columns):
            non_null = df_events[col].notna().sum()
            print(f"   - {col}: {non_null}/{len(df_events)} values")
        
        return df_events


def main():
    """
    Main execution: extract all events from GWTC catalogs
    """
    print("=" * 70)
    print("📊 EXTRACT EVENTS FROM GWTC CATALOGS")
    print("=" * 70)
    print("Processing downloaded LIGO catalog files...")
    print()
    
    extractor = GWTCEventExtractor()
    events_df = extractor.extract_all_catalogs()
    
    if events_df is not None:
        print(f"\n🎉 SUCCESS: Extracted {len(events_df)} unique events!")
        print("🎯 Next: Use these events for comprehensive Klein analysis")
    else:
        print("\n❌ No events could be extracted")


if __name__ == "__main__":
    main()