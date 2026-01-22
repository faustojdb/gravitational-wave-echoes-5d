#!/usr/bin/env python3
"""
DOWNLOAD LIGO EVENTS AS ASCII FROM CSV CATALOG
===============================================

Usa el archivo events.csv para descargar datos LIGO en formato ASCII
desde GWOSC. Los datos ASCII son más fáciles de descargar y procesar.

Estrategia:
1. Leer events.csv con 219 eventos
2. Para cada evento, construir URLs ASCII de GWOSC
3. Descargar strain data en formato TXT/ASCII
4. Convertir a formato que pueda usar nuestro Klein analyzer

Date: 26 August, 2025
"""

import pandas as pd
import requests
import numpy as np
from pathlib import Path
import time
import json
from typing import Dict, List, Optional, Tuple
import re

class LIGOASCIIDownloader:
    """
    Descargador de datos LIGO en formato ASCII usando información del CSV
    """
    
    def __init__(self, csv_path: str = None, output_dir: str = None):
        if csv_path is None:
            csv_path = "/mnt/d/Multidimensional_Theory_Simulations/multidimensional-theory/gravitational-wave-echoes-5d/FUNDAMENTAL_RADIUS_INVESTIGATION/events.csv"
        
        if output_dir is None:
            output_dir = "/mnt/d/Multidimensional_Theory_Simulations/multidimensional-theory/gravitational-wave-echoes-5d/S2_SPHERICAL_SPACETIME_THEORY/5_Code/ligo_real_data/ascii_data"
        
        self.csv_path = Path(csv_path)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # GWOSC ASCII data patterns
        self.gwosc_base = "https://gwosc.org"
        self.ascii_patterns = [
            "/archive/data/S{run}/strain/{detector}/{filename}",
            "/archive/links/S{run}/{detector}/{filename}",
            "/catalog/{catalog}/strain/{detector}/{filename}"
        ]
        
        print("📄 LIGO ASCII Data Downloader")
        print("=" * 60)
        print(f"📊 CSV file: {self.csv_path}")
        print(f"📁 Output: {self.output_dir}")
        print()
    
    def load_events_csv(self) -> pd.DataFrame:
        """Carga el catálogo de eventos"""
        if not self.csv_path.exists():
            print(f"❌ CSV not found: {self.csv_path}")
            return None
        
        try:
            df = pd.read_csv(self.csv_path)
            print(f"✅ Loaded {len(df)} events from CSV")
            
            # Mostrar información del catálogo
            catalogs = df['catalog'].value_counts()
            print(f"📋 Catalog distribution:")
            for cat, count in catalogs.items():
                print(f"   {cat}: {count} events")
            
            return df
            
        except Exception as e:
            print(f"❌ Error loading CSV: {e}")
            return None
    
    def extract_gps_time_window(self, gps_time: float, duration: int = 32) -> Tuple[int, int]:
        """
        Extrae ventana de tiempo GPS para descarga
        LIGO normalmente usa ventanas de 32 segundos centradas en el evento
        """
        center_gps = int(gps_time)
        start_gps = center_gps - duration // 2
        end_gps = center_gps + duration // 2
        
        return start_gps, end_gps
    
    def determine_observing_run(self, gps_time: float) -> str:
        """
        Determina el run de observación basado en GPS time
        """
        # GPS time ranges para diferentes runs (aproximados)
        if gps_time < 1137250000:  # Sept 2015
            return "O1"
        elif gps_time < 1187730000:  # Aug 2017  
            return "O2"
        elif gps_time < 1269360000:  # Apr 2020
            return "O3"
        else:
            return "O4"
    
    def construct_ascii_urls(self, event_name: str, gps_time: float, catalog: str) -> Dict[str, List[str]]:
        """
        Construye URLs posibles para datos ASCII
        """
        urls = {'H1': [], 'L1': [], 'V1': []}
        
        # Determinar run y ventana GPS
        obs_run = self.determine_observing_run(gps_time)
        start_gps, end_gps = self.extract_gps_time_window(gps_time)
        
        # Patrones de nombres de archivo comunes
        filename_patterns = [
            f"{event_name}-{{}}-{start_gps}-32.txt",
            f"{event_name.replace('_', '')}-{{}}-{start_gps}-32.txt", 
            f"H-{{}}_{obs_run}_STRAIN-{start_gps}-32.txt",
            f"{{}}_{obs_run}_STRAIN-{start_gps}-32.txt"
        ]
        
        # URLs base comunes
        base_urls = [
            f"https://gwosc.org/archive/data/{obs_run}/",
            f"https://gwosc.org/archive/links/{obs_run}/",
            "https://gwosc.org/catalog/data/",
            f"https://gwosc.org/eventapi/ascii/{event_name}/"
        ]
        
        # Generar combinaciones
        for detector in ['H1', 'L1', 'V1']:
            for base_url in base_urls:
                for pattern in filename_patterns:
                    filename = pattern.format(detector)
                    
                    # Diferentes estructuras de URL
                    possible_urls = [
                        f"{base_url}{detector}/{filename}",
                        f"{base_url}strain/{detector}/{filename}",
                        f"{base_url}{filename}",
                        f"https://gwosc.org/eventapi/ascii/{event_name}/{detector}/",
                        f"https://gwosc.org/catalog/{catalog}/data/{detector}/{filename}"
                    ]
                    
                    urls[detector].extend(possible_urls)
        
        # Remover duplicados manteniendo orden
        for detector in urls:
            seen = set()
            urls[detector] = [x for x in urls[detector] if not (x in seen or seen.add(x))]
        
        return urls
    
    def download_ascii_data(self, url: str) -> Optional[np.ndarray]:
        """
        Descarga y parsea datos ASCII
        Returns: array de strain data o None si falla
        """
        try:
            response = requests.get(url, timeout=60)
            
            if response.status_code != 200:
                return None
            
            # Parsear datos ASCII
            text_data = response.text.strip()
            
            # Diferentes formatos posibles
            lines = text_data.split('\n')
            
            # Filtrar comentarios y headers
            data_lines = [line.strip() for line in lines 
                         if line.strip() and not line.startswith('#') and not line.startswith('%')]
            
            if not data_lines:
                return None
            
            # Intentar parsear como diferentes formatos
            try:
                # Formato: tiempo strain
                if len(data_lines[0].split()) >= 2:
                    data = []
                    for line in data_lines:
                        parts = line.split()
                        if len(parts) >= 2:
                            try:
                                strain_val = float(parts[1])  # Segunda columna es strain
                                data.append(strain_val)
                            except ValueError:
                                continue
                    
                    if len(data) > 1000:  # Mínimo datos razonables
                        return np.array(data)
                
                # Formato: solo strain (una columna)
                elif len(data_lines[0].split()) == 1:
                    data = []
                    for line in data_lines:
                        try:
                            strain_val = float(line.strip())
                            data.append(strain_val)
                        except ValueError:
                            continue
                    
                    if len(data) > 1000:
                        return np.array(data)
                
            except Exception:
                pass
            
            return None
            
        except Exception:
            return None
    
    def process_single_event(self, row: pd.Series) -> Dict:
        """
        Procesa un evento individual del CSV
        """
        event_name = row['name']
        gps_time = row['gps']
        catalog = row.get('catalog', 'unknown')
        snr = row.get('network_matched_filter_snr', 0)
        
        print(f"\n🌊 Event: {event_name}")
        print(f"   GPS: {gps_time}, SNR: {snr}, Catalog: {catalog}")
        
        # Crear directorio para el evento
        event_dir = self.output_dir / event_name
        event_dir.mkdir(exist_ok=True)
        
        # Verificar si ya tenemos datos
        existing_files = list(event_dir.glob("*_strain.txt"))
        if len(existing_files) >= 1:
            print(f"   ✓ Already have {len(existing_files)} strain files")
            return {
                'event_name': event_name,
                'files_found': len(existing_files),
                'detectors': [f.stem.split('_')[-2] for f in existing_files]
            }
        
        # Construir URLs posibles
        urls = self.construct_ascii_urls(event_name, gps_time, catalog)
        
        downloaded = {}
        
        # Intentar descarga para cada detector
        for detector in ['H1', 'L1', 'V1']:
            if detector not in urls or not urls[detector]:
                continue
            
            print(f"   {detector}: Trying {len(urls[detector])} URLs...")
            
            strain_data = None
            successful_url = None
            
            # Probar cada URL hasta encontrar una que funcione
            for i, url in enumerate(urls[detector][:5]):  # Limitar a 5 intentos
                print(f"      [{i+1}] {url[:80]}...", end='')
                
                strain_data = self.download_ascii_data(url)
                
                if strain_data is not None:
                    successful_url = url
                    print(f" ✓ ({len(strain_data)} samples)")
                    break
                else:
                    print(" ✗")
                
                time.sleep(0.5)  # Rate limiting
            
            if strain_data is not None:
                # Guardar datos
                output_file = event_dir / f"{event_name}_{detector}_strain.txt"
                
                np.savetxt(output_file, strain_data, fmt='%.12e')
                
                # También crear un archivo compatible con HDF5 structure
                compat_file = event_dir / f"{event_name}_{detector}_strain_data.npz"
                np.savez(compat_file, 
                        strain=strain_data, 
                        sample_rate=4096,  # Asumir 4096 Hz típico
                        gps_time=gps_time,
                        detector=detector,
                        source_url=successful_url)
                
                downloaded[detector] = {
                    'samples': len(strain_data),
                    'url': successful_url,
                    'file': str(output_file)
                }
                
                print(f"   ✅ {detector}: {len(strain_data)} samples saved")
            else:
                print(f"   ❌ {detector}: No data found")
        
        # Guardar metadata
        metadata = {
            'event_name': event_name,
            'gps_time': gps_time,
            'snr': snr,
            'catalog': catalog,
            'mass_1': row.get('mass_1_source'),
            'mass_2': row.get('mass_2_source'),
            'distance': row.get('luminosity_distance'),
            'downloaded_detectors': list(downloaded.keys()),
            'download_details': downloaded
        }
        
        metadata_file = event_dir / f"{event_name}_metadata.json"
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        result = {
            'event_name': event_name,
            'files_found': len(downloaded),
            'detectors': list(downloaded.keys()),
            'total_samples': sum(d['samples'] for d in downloaded.values())
        }
        
        if downloaded:
            print(f"   🎉 Success: {len(downloaded)} detectors downloaded")
        
        return result
    
    def download_all_ascii_data(self):
        """
        Descarga datos ASCII para todos los eventos del CSV
        """
        # Cargar eventos
        df = self.load_events_csv()
        
        if df is None:
            return
        
        print(f"\n🚀 Starting ASCII download for {len(df)} events...")
        print("=" * 60)
        
        successful_events = 0
        total_files = 0
        failed_events = []
        results = []
        
        # Procesar eventos en lotes
        for i, row in df.iterrows():
            print(f"\n[{i+1}/{len(df)}]", end='')
            
            try:
                result = self.process_single_event(row)
                results.append(result)
                
                if result['files_found'] > 0:
                    successful_events += 1
                    total_files += result['files_found']
                else:
                    failed_events.append(result['event_name'])
                
            except Exception as e:
                print(f"   ❌ Error: {e}")
                failed_events.append(row['name'])
            
            # Progress report every 20 events
            if (i + 1) % 20 == 0:
                print(f"\n   📊 Progress: {successful_events}/{i+1} events, {total_files} files")
                time.sleep(2)  # Brief pause
        
        # Final summary
        print("\n" + "=" * 60)
        print("📊 ASCII DOWNLOAD SUMMARY")
        print("=" * 60)
        print(f"✅ Events with data: {successful_events}/{len(df)} ({100*successful_events/len(df):.1f}%)")
        print(f"📁 Total strain files: {total_files}")
        
        if failed_events:
            print(f"❌ Failed events: {len(failed_events)}")
            for event in failed_events[:10]:
                print(f"   - {event}")
            if len(failed_events) > 10:
                print(f"   ... and {len(failed_events)-10} more")
        
        # Save summary
        summary = {
            'total_events_in_csv': len(df),
            'events_with_ascii_data': successful_events,
            'total_ascii_files': total_files,
            'success_rate': successful_events / len(df),
            'failed_events': failed_events,
            'all_results': results,
            'download_date': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        summary_file = self.output_dir / "ascii_download_summary.json"
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"\n💾 Summary saved: {summary_file}")
        
        if successful_events > 0:
            print(f"\n🎉 SUCCESS: {successful_events} events with ASCII data ready!")
            print(f"📈 Total samples available for Klein analysis: ~{total_files * 100000:,}")
            return self.output_dir
        else:
            print(f"\n❌ No ASCII data downloaded")
            return None


def main():
    """
    Main execution: download ASCII data for 219 events
    """
    print("=" * 70)
    print("🌟 LIGO ASCII DATA DOWNLOAD FROM 219-EVENT CSV")
    print("=" * 70)
    print("Downloading real gravitational wave data in ASCII format...")
    print()
    
    downloader = LIGOASCIIDownloader()
    result_dir = downloader.download_all_ascii_data()
    
    if result_dir:
        print(f"\n✅ ASCII data ready in: {result_dir}")
        print(f"🎯 Next: Convert to Klein-compatible format and analyze")
    else:
        print(f"\n⚠️  Check alternative data sources")


if __name__ == "__main__":
    main()