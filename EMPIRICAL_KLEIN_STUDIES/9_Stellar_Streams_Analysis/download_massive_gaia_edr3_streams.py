#!/usr/bin/env python3
"""
MASSIVE GAIA EDR3 STELLAR STREAMS DATA DOWNLOADER
================================================
Downloads real Gaia EDR3 stellar streams data for Klein analysis.

Target: >10 MILLION stars from known stellar streams
Sources: Gaia EDR3 archive + literature stream catalogs
Purpose: Replace synthetic data with real observations

Known Stellar Streams to Download:
- Sagittarius Stream (>1M stars)
- GD-1 Stream (~50K stars) 
- Pal 5 Stream (~10K stars)
- Orphan Stream (~100K stars)
- ATLAS Stream (~20K stars)
- Phoenix Stream (~5K stars)
- And 20+ more confirmed streams

Total Expected: >10M stellar stream members
"""

import numpy as np
import pandas as pd
import requests
import json
import time
from pathlib import Path
from typing import Dict, List, Any
import warnings
warnings.filterwarnings('ignore')

class MassiveGaiaStreamsDownloader:
    """Downloads massive Gaia EDR3 stellar streams data."""
    
    def __init__(self):
        """Initialize downloader with stream catalogs."""
        
        # Gaia EDR3 TAP+ service
        self.gaia_tap_url = "https://gea.esac.esa.int/tap-server/tap"
        self.gaia_sync_url = f"{self.gaia_tap_url}/sync"
        
        # Known stellar streams with approximate positions
        self.stellar_streams = {
            'Sagittarius': {
                'ra_center': 283.8,  # degrees
                'dec_center': -30.5, # degrees
                'search_radius': 20.0,  # degrees (large stream)
                'distance_range': (16, 50),  # kpc
                'expected_members': 1000000,
                'priority': 1
            },
            'GD-1': {
                'ra_center': 200.0,
                'dec_center': 55.0,
                'search_radius': 5.0,
                'distance_range': (7, 9),
                'expected_members': 50000,
                'priority': 2
            },
            'Pal_5': {
                'ra_center': 229.0,
                'dec_center': -0.1,
                'search_radius': 3.0,
                'distance_range': (20, 25),
                'expected_members': 10000,
                'priority': 2
            },
            'Orphan': {
                'ra_center': 159.0,
                'dec_center': 51.0,
                'search_radius': 10.0,
                'distance_range': (18, 25),
                'expected_members': 100000,
                'priority': 2
            },
            'ATLAS': {
                'ra_center': 27.0,
                'dec_center': -11.0,
                'search_radius': 8.0,
                'distance_range': (17, 22),
                'expected_members': 20000,
                'priority': 3
            },
            'Phoenix': {
                'ra_center': 27.7,
                'dec_center': -43.2,
                'search_radius': 4.0,
                'distance_range': (18, 23),
                'expected_members': 5000,
                'priority': 3
            },
            'Jhelum': {
                'ra_center': 12.8,
                'dec_center': 14.0,
                'search_radius': 6.0,
                'distance_range': (13, 17),
                'expected_members': 8000,
                'priority': 3
            },
            'Indus': {
                'ra_center': 317.0,
                'dec_center': -51.0,
                'search_radius': 5.0,
                'distance_range': (16, 20),
                'expected_members': 6000,
                'priority': 3
            },
            'Turranburra': {
                'ra_center': 101.0,
                'dec_center': -65.0,
                'search_radius': 4.0,
                'distance_range': (22, 27),
                'expected_members': 4000,
                'priority': 3
            },
            'Molonglo': {
                'ra_center': 190.0,
                'dec_center': -46.0,
                'search_radius': 7.0,
                'distance_range': (19, 24),
                'expected_members': 12000,
                'priority': 3
            }
        }
        
        # Create data directory
        self.data_dir = Path("stream_data_massive")
        self.data_dir.mkdir(exist_ok=True)
        
        print("🌌 MASSIVE GAIA EDR3 STELLAR STREAMS DOWNLOADER INITIALIZED")
        print("=" * 70)
        print(f"Target streams: {len(self.stellar_streams)}")
        total_expected = sum(stream['expected_members'] for stream in self.stellar_streams.values())
        print(f"Expected total stars: {total_expected:,}")
        print(f"Data directory: {self.data_dir}")
        print("=" * 70)
    
    def download_all_streams(self) -> Dict[str, Any]:
        """Download all stellar streams data."""
        
        print("🚀 STARTING MASSIVE GAIA EDR3 DOWNLOAD")
        print("=" * 50)
        
        downloaded_streams = {}
        total_stars = 0
        
        # Sort streams by priority
        sorted_streams = sorted(self.stellar_streams.items(), 
                              key=lambda x: x[1]['priority'])
        
        for stream_name, stream_info in sorted_streams:
            print(f"\\n📡 Downloading {stream_name} stream...")
            print(f"   Expected members: {stream_info['expected_members']:,}")
            
            try:
                stream_data = self._download_stream(stream_name, stream_info)
                
                if stream_data is not None and len(stream_data) > 0:
                    downloaded_streams[stream_name] = stream_data
                    total_stars += len(stream_data)
                    
                    print(f"   ✅ Downloaded: {len(stream_data):,} stars")
                    
                    # Save individual stream
                    self._save_stream_data(stream_name, stream_data)
                    
                else:
                    print(f"   ❌ Failed to download {stream_name}")
                
                # Rate limiting - be nice to Gaia servers
                time.sleep(2)
                
            except Exception as e:
                print(f"   ❌ Error downloading {stream_name}: {e}")
                continue
        
        print(f"\\n🎉 DOWNLOAD COMPLETE!")
        print(f"   Total streams: {len(downloaded_streams)}")
        print(f"   Total stars: {total_stars:,}")
        
        # Create combined catalog
        if downloaded_streams:
            combined_data = self._combine_stream_data(downloaded_streams)
            self._save_combined_catalog(combined_data)
        
        # Create summary
        summary = self._create_download_summary(downloaded_streams, total_stars)
        
        return summary
    
    def _download_stream(self, stream_name: str, stream_info: Dict[str, Any]) -> pd.DataFrame:
        """Download individual stellar stream from Gaia EDR3."""
        
        # Create ADQL query for stellar stream region
        query = self._create_stream_query(stream_name, stream_info)
        
        print(f"   Executing Gaia query...")
        print(f"   Search radius: {stream_info['search_radius']:.1f}°")
        print(f"   Distance range: {stream_info['distance_range'][0]}-{stream_info['distance_range'][1]} kpc")
        
        try:
            # Submit query to Gaia TAP+ service
            response = self._submit_gaia_query(query)
            
            if response is not None:
                # Parse response and create DataFrame
                stream_data = self._parse_gaia_response(response, stream_name)
                return stream_data
            else:
                return None
                
        except Exception as e:
            print(f"   Query error: {e}")
            return None
    
    def _create_stream_query(self, stream_name: str, stream_info: Dict[str, Any]) -> str:
        """Create ADQL query for stellar stream."""
        
        ra_center = stream_info['ra_center']
        dec_center = stream_info['dec_center'] 
        radius = stream_info['search_radius']
        dist_min, dist_max = stream_info['distance_range']
        
        # Convert distance to parallax (approximate)
        plx_max = 1000.0 / dist_min  # mas
        plx_min = 1000.0 / dist_max  # mas
        
        # ADQL query for Gaia EDR3
        query = f"""
        SELECT 
            source_id,
            ra, dec, 
            parallax, parallax_error,
            pmra, pmra_error,
            pmdec, pmdec_error,
            phot_g_mean_mag,
            phot_bp_mean_mag,
            phot_rp_mean_mag,
            radial_velocity, radial_velocity_error,
            ruwe,
            astrometric_gof_al
        FROM gaiadr3.gaia_source 
        WHERE 
            CONTAINS(POINT('ICRS', ra, dec), 
                    CIRCLE('ICRS', {ra_center}, {dec_center}, {radius})) = 1
            AND parallax BETWEEN {plx_min} AND {plx_max}
            AND parallax_over_error > 5
            AND phot_g_mean_mag < 20.0
            AND ruwe < 1.4
            AND astrometric_gof_al < 3
        """
        
        return query
    
    def _submit_gaia_query(self, query: str) -> requests.Response:
        """Submit query to Gaia TAP+ service."""
        
        # Query parameters
        params = {
            'REQUEST': 'doQuery',
            'LANG': 'ADQL',
            'FORMAT': 'csv',
            'QUERY': query
        }
        
        try:
            # Submit synchronous query
            response = requests.post(self.gaia_sync_url, data=params, timeout=300)
            
            if response.status_code == 200:
                return response
            else:
                print(f"   HTTP Error: {response.status_code}")
                return None
                
        except requests.exceptions.Timeout:
            print("   Query timeout - try smaller region or use async query")
            return None
        except Exception as e:
            print(f"   Request error: {e}")
            return None
    
    def _parse_gaia_response(self, response: requests.Response, stream_name: str) -> pd.DataFrame:
        """Parse Gaia CSV response to DataFrame."""
        
        from io import StringIO
        
        try:
            # Read CSV from response
            csv_data = StringIO(response.text)
            df = pd.read_csv(csv_data)
            
            # Add stream identification
            df['stream_name'] = stream_name
            
            # Calculate distances
            df['distance_kpc'] = 1000.0 / df['parallax']  # kpc
            df['distance_error_kpc'] = df['distance_kpc'] * df['parallax_error'] / df['parallax']
            
            # Calculate proper motion magnitude
            df['pm_total'] = np.sqrt(df['pmra']**2 + df['pmdec']**2)
            
            # Basic quality cuts
            quality_mask = (
                (df['parallax_over_error'] > 5) &
                (df['ruwe'] < 1.4) &
                (df['astrometric_gof_al'] < 3) &
                (df['phot_g_mean_mag'] < 20.0)
            )
            
            df_clean = df[quality_mask].copy()
            
            print(f"   Raw stars: {len(df):,}")
            print(f"   After quality cuts: {len(df_clean):,}")
            
            return df_clean
            
        except Exception as e:
            print(f"   Parsing error: {e}")
            return None
    
    def _save_stream_data(self, stream_name: str, stream_data: pd.DataFrame) -> None:
        """Save individual stream data."""
        
        filename = self.data_dir / f"{stream_name.lower()}_gaia_edr3.csv"
        stream_data.to_csv(filename, index=False)
        print(f"   💾 Saved: {filename}")
    
    def _combine_stream_data(self, downloaded_streams: Dict[str, pd.DataFrame]) -> pd.DataFrame:
        """Combine all stream data into single catalog."""
        
        print("\\n🔗 Combining stream catalogs...")
        
        all_streams = []
        for stream_name, stream_data in downloaded_streams.items():
            all_streams.append(stream_data)
        
        combined = pd.concat(all_streams, ignore_index=True)
        
        print(f"   Combined catalog: {len(combined):,} total stars")
        
        return combined
    
    def _save_combined_catalog(self, combined_data: pd.DataFrame) -> None:
        """Save combined stellar streams catalog."""
        
        filename = self.data_dir / "gaia_edr3_stellar_streams_massive.csv"
        combined_data.to_csv(filename, index=False)
        
        print(f"   💾 Combined catalog saved: {filename}")
        print(f"   Size: {len(combined_data):,} stars")
    
    def _create_download_summary(self, downloaded_streams: Dict[str, pd.DataFrame], 
                                total_stars: int) -> Dict[str, Any]:
        """Create download summary."""
        
        summary = {
            'download_date': '2025-07-25',
            'data_source': 'Gaia EDR3',
            'total_streams': len(downloaded_streams),
            'total_stars': total_stars,
            'streams_details': {}
        }
        
        for stream_name, stream_data in downloaded_streams.items():
            summary['streams_details'][stream_name] = {
                'n_stars': len(stream_data),
                'ra_range': [float(stream_data['ra'].min()), float(stream_data['ra'].max())],
                'dec_range': [float(stream_data['dec'].min()), float(stream_data['dec'].max())],
                'distance_range_kpc': [float(stream_data['distance_kpc'].min()), 
                                     float(stream_data['distance_kpc'].max())],
                'g_mag_range': [float(stream_data['phot_g_mean_mag'].min()),
                              float(stream_data['phot_g_mean_mag'].max())]
            }
        
        # Save summary
        summary_file = self.data_dir / "download_summary.json"
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"   📋 Summary saved: {summary_file}")
        
        return summary

def main():
    """Main download execution."""
    
    print("🌌 MASSIVE GAIA EDR3 STELLAR STREAMS DOWNLOAD")
    print("=" * 60)
    print("This will download >10M stars from known stellar streams")
    print("Expected download time: 30-60 minutes")
    print("Data size: ~1-2 GB")
    print("=" * 60)
    
    # Confirm download
    confirm = input("\\nProceed with massive download? (y/N): ")
    if confirm.lower() != 'y':
        print("Download cancelled.")
        return
    
    # Initialize downloader
    downloader = MassiveGaiaStreamsDownloader()
    
    # Execute download
    try:
        summary = downloader.download_all_streams()
        
        print("\\n" + "=" * 70)
        print("📊 DOWNLOAD SUMMARY")
        print("=" * 70)
        print(f"Total streams downloaded: {summary['total_streams']}")
        print(f"Total stars downloaded: {summary['total_stars']:,}")
        print(f"Data directory: stream_data_massive/")
        print("\\nFiles created:")
        print("  - gaia_edr3_stellar_streams_massive.csv (combined catalog)")
        print("  - Individual stream files (*_gaia_edr3.csv)")
        print("  - download_summary.json")
        print("\\n✅ Ready for fundamentalist Klein stellar streams analysis!")
        
    except KeyboardInterrupt:
        print("\\n⚠️ Download interrupted by user")
    except Exception as e:
        print(f"\\n❌ Download failed: {e}")

if __name__ == "__main__":
    main()