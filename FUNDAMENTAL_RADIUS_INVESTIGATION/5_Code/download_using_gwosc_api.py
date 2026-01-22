#!/usr/bin/env python3
"""
DOWNLOAD LIGO EVENTS USING PROPER GWOSC API
============================================

Usa la especificación GWOSC API.yaml para descargar correctamente
los eventos LIGO del CSV usando los endpoints oficiales.

Endpoints clave de la API:
- /api/v2/event-versions/{name}/strain-files: obtener archivos strain
- /api/v2/events/{name}: información del evento
- Formato: hdf5, gwf, txt disponibles

Date: 26 August, 2025
"""

import pandas as pd
import requests
import h5py
import numpy as np
from pathlib import Path
import time
import json
from typing import Dict, List, Optional, Tuple

class GWOSCAPIDownloader:
    """
    Descargador usando la API oficial de GWOSC según especificación YAML
    """
    
    def __init__(self, csv_path: str = None, output_dir: str = None):
        if csv_path is None:
            csv_path = "/mnt/d/Multidimensional_Theory_Simulations/multidimensional-theory/gravitational-wave-echoes-5d/FUNDAMENTAL_RADIUS_INVESTIGATION/events.csv"
        
        if output_dir is None:
            output_dir = "/mnt/d/Multidimensional_Theory_Simulations/multidimensional-theory/gravitational-wave-echoes-5d/S2_SPHERICAL_SPACETIME_THEORY/5_Code/ligo_real_data/gwosc_api_data"
        
        self.csv_path = Path(csv_path)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # GWOSC API base URL según YAML
        self.api_base = "https://gwosc.org/api/v2"
        
        print("🌐 GWOSC API Downloader (usando especificación YAML)")
        print("=" * 60)
        print(f"📄 Events CSV: {self.csv_path}")
        print(f"📁 Output: {self.output_dir}")
        print(f"🔗 API Base: {self.api_base}")
        print()
    
    def load_events_csv(self) -> pd.DataFrame:
        """Carga eventos desde CSV"""
        if not self.csv_path.exists():
            print(f"❌ CSV not found: {self.csv_path}")
            return None
        
        try:
            df = pd.read_csv(self.csv_path)
            print(f"📊 Loaded {len(df)} events from CSV")
            return df
        except Exception as e:
            print(f"❌ Error loading CSV: {e}")
            return None
    
    def test_api_endpoints(self):
        """Test de conectividad con endpoints principales"""
        print("🔧 Testing GWOSC API endpoints...")
        
        endpoints_to_test = [
            "/api/v2/",
            "/api/v2/events",
            "/api/v2/catalogs",
            "/api/v2/runs"
        ]
        
        working_endpoints = []
        
        for endpoint in endpoints_to_test:
            try:
                url = f"https://gwosc.org{endpoint}"
                print(f"   Testing {endpoint}...", end='')
                
                response = requests.get(url, timeout=10)
                
                if response.status_code == 200:
                    print(" ✓")
                    working_endpoints.append(endpoint)
                else:
                    print(f" ✗ (HTTP {response.status_code})")
                    
            except Exception as e:
                print(f" ✗ ({e})")
        
        print(f"\n✅ Working endpoints: {len(working_endpoints)}/{len(endpoints_to_test)}")
        return len(working_endpoints) > 0
    
    def get_event_strain_files(self, event_name: str) -> Dict:
        """
        Usa /api/v2/event-versions/{name}/strain-files para obtener strain files
        """
        try:
            # Endpoint según YAML: /api/v2/event-versions/{name}/strain-files
            url = f"{self.api_base}/event-versions/{event_name}/strain-files"
            
            print(f"      API call: {url}")
            
            response = requests.get(url, timeout=30)
            
            if response.status_code != 200:
                # Intentar con nombre base (sin timestamp)
                base_name = event_name.split('_')[0]  # GW200115_042309 -> GW200115
                alt_url = f"{self.api_base}/event-versions/{base_name}/strain-files"
                
                print(f"      Trying alternative: {alt_url}")
                response = requests.get(alt_url, timeout=30)
                
                if response.status_code != 200:
                    return {}
            
            data = response.json()
            
            # Procesar respuesta según esquema YAML
            strain_files = {}
            
            if 'results' in data:
                for file_info in data['results']:
                    detector = file_info.get('detector', '')
                    download_url = file_info.get('download_url', '')
                    file_format = file_info.get('file_format', '')
                    sample_rate = file_info.get('sample_rate_kHz', 4)
                    
                    # Preferir HDF5 a 4kHz
                    if file_format.lower() == 'hdf5' and sample_rate == 4:
                        strain_files[detector] = {
                            'url': download_url,
                            'format': file_format,
                            'sample_rate': sample_rate,
                            'duration': file_info.get('duration', 32)
                        }
            
            return strain_files
            
        except Exception as e:
            print(f"      API Error: {e}")
            return {}
    
    def download_strain_file(self, url: str, output_path: Path, file_format: str = 'hdf5') -> bool:
        """Descarga archivo strain y verifica integridad"""
        
        try:
            print(f"         Downloading...", end='')
            
            response = requests.get(url, timeout=120, stream=True)
            
            if response.status_code != 200:
                print(f" ✗ (HTTP {response.status_code})")
                return False
            
            # Download with progress indication
            with open(output_path, 'wb') as f:
                total_size = int(response.headers.get('content-length', 0))
                downloaded = 0
                
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
                    downloaded += len(chunk)
            
            # Verificar archivo según formato
            if file_format.lower() == 'hdf5':
                return self.verify_hdf5_file(output_path)
            else:
                # Para otros formatos, verificar que no esté vacío
                return output_path.stat().st_size > 1000
            
        except Exception as e:
            print(f" ✗ ({e})")
            return False
    
    def verify_hdf5_file(self, filepath: Path) -> bool:
        """Verifica que el archivo HDF5 tenga datos strain válidos"""
        try:
            with h5py.File(filepath, 'r') as f:
                if 'strain' in f:
                    strain_data = f['strain']
                    if len(strain_data) > 1000:  # Mínimo razonable
                        sample_rate = f.attrs.get('sample_rate', f.attrs.get('sampling_rate', 4096))
                        duration = len(strain_data) / sample_rate
                        print(f" ✓ ({len(strain_data)} samples, {duration:.1f}s)")
                        return True
                    else:
                        print(f" ✗ (too few samples: {len(strain_data)})")
                        return False
                else:
                    print(" ✗ (no strain data)")
                    return False
        except Exception as e:
            print(f" ✗ (invalid HDF5: {e})")
            return False
    
    def process_event_from_csv(self, row: pd.Series) -> Dict:
        """
        Procesa un evento del CSV usando la API de GWOSC
        """
        event_name = row['name']
        gps_time = row.get('gps', 0)
        snr = row.get('network_matched_filter_snr', 0)
        
        print(f"\n🌊 Event: {event_name}")
        print(f"   GPS: {gps_time}, SNR: {snr}")
        
        # Crear directorio del evento
        event_dir = self.output_dir / event_name
        event_dir.mkdir(exist_ok=True)
        
        # Verificar si ya tenemos datos
        existing_files = list(event_dir.glob("*_strain.hdf5"))
        if len(existing_files) >= 1:
            print(f"   ✓ Already have {len(existing_files)} files")
            return {
                'event_name': event_name,
                'status': 'already_exists',
                'files': len(existing_files)
            }
        
        # Obtener strain files via API
        strain_files = self.get_event_strain_files(event_name)
        
        if not strain_files:
            print(f"   ❌ No strain files found via API")
            return {
                'event_name': event_name,
                'status': 'no_strain_files',
                'files': 0
            }
        
        # Descargar archivos
        downloaded = 0
        download_info = {}
        
        for detector, file_info in strain_files.items():
            print(f"   {detector}: {file_info['format']}, {file_info['sample_rate']}kHz")
            
            output_file = event_dir / f"{event_name}_{detector}_strain.hdf5"
            
            if output_file.exists():
                print(f"         Already exists ✓")
                downloaded += 1
                continue
            
            success = self.download_strain_file(
                file_info['url'], 
                output_file, 
                file_info['format']
            )
            
            if success:
                downloaded += 1
                download_info[detector] = {
                    'file': str(output_file),
                    'url': file_info['url'],
                    'format': file_info['format']
                }
            
            time.sleep(0.5)  # Rate limiting
        
        # Guardar metadata
        metadata = {
            'event_name': event_name,
            'gps_time': gps_time,
            'snr': snr,
            'catalog': row.get('catalog'),
            'downloaded_detectors': list(download_info.keys()),
            'download_info': download_info,
            'api_used': True
        }
        
        metadata_file = event_dir / f"{event_name}_metadata.json"
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        result = {
            'event_name': event_name,
            'status': 'success' if downloaded > 0 else 'failed',
            'files': downloaded,
            'detectors': list(download_info.keys())
        }
        
        if downloaded > 0:
            print(f"   🎉 Downloaded {downloaded} files")
        else:
            print(f"   ❌ No files downloaded")
        
        return result
    
    def download_all_events_via_api(self):
        """
        Descarga todos los eventos del CSV usando la API de GWOSC
        """
        # Test API connectivity
        if not self.test_api_endpoints():
            print("❌ GWOSC API not accessible!")
            return
        
        # Load events
        df = self.load_events_csv()
        if df is None:
            return
        
        print(f"\n🚀 Starting API download for {len(df)} events...")
        print("=" * 60)
        
        successful_events = 0
        total_files = 0
        failed_events = []
        results = []
        
        # Process events in batches
        for i, row in df.iterrows():
            print(f"\n[{i+1}/{len(df)}]", end='')
            
            try:
                result = self.process_event_from_csv(row)
                results.append(result)
                
                if result['status'] in ['success', 'already_exists']:
                    successful_events += 1
                    total_files += result['files']
                else:
                    failed_events.append(result['event_name'])
                
            except Exception as e:
                print(f"   ❌ Processing error: {e}")
                failed_events.append(row['name'])
            
            # Progress reports and rate limiting
            if (i + 1) % 10 == 0:
                print(f"\n   📊 Progress: {successful_events}/{i+1} events, {total_files} files")
                time.sleep(3)  # Longer pause every 10 events for API courtesy
        
        # Final summary
        print("\n" + "=" * 60)
        print("📊 GWOSC API DOWNLOAD SUMMARY")
        print("=" * 60)
        print(f"✅ Events with data: {successful_events}/{len(df)} ({100*successful_events/len(df):.1f}%)")
        print(f"📁 Total files downloaded: {total_files}")
        
        if failed_events:
            print(f"❌ Failed events: {len(failed_events)}")
            for event in failed_events[:10]:
                print(f"   - {event}")
            if len(failed_events) > 10:
                print(f"   ... and {len(failed_events)-10} more")
        
        # Save results
        summary = {
            'total_events_in_csv': len(df),
            'successful_events': successful_events,
            'total_files_downloaded': total_files,
            'success_rate': successful_events / len(df),
            'failed_events': failed_events,
            'all_results': results,
            'download_method': 'GWOSC_API_v2',
            'download_date': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        summary_file = self.output_dir / "gwosc_api_download_summary.json"
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"\n💾 Summary: {summary_file}")
        
        if successful_events > 0:
            print(f"\n🎉 SUCCESS: {successful_events} events ready for Klein analysis!")
            print(f"🎯 Total strain files: {total_files}")
            return self.output_dir
        else:
            print(f"\n⚠️  No events downloaded via API")
            return None


def main():
    """
    Main execution usando GWOSC API v2
    """
    print("=" * 70)
    print("🌟 LIGO DATA DOWNLOAD VIA GWOSC API v2")
    print("=" * 70)
    print("Using official GWOSC API specification...")
    print()
    
    downloader = GWOSCAPIDownloader()
    result_dir = downloader.download_all_events_via_api()
    
    if result_dir:
        print(f"\n✅ Data downloaded via API: {result_dir}")
        print(f"🎯 Next: Run Klein analysis on all downloaded events")
    else:
        print(f"\n🤔 API download incomplete - check network/API status")


if __name__ == "__main__":
    main()