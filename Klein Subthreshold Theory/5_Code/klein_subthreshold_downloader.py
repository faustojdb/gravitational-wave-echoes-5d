#!/usr/bin/env python3
"""
Klein Field Theory Subthreshold Candidates Downloader
====================================================

Specifically downloads and prepares LIGO/Virgo subthreshold candidates 
for Klein Field Theory echo analysis. These ~2,242 low-significance events 
may contain Klein field resonances that appear as "noise" in conventional analysis.

Key hypothesis: Low-significance events could be 5D tension effects
that don't register strongly in standard 4D detectors but still carry
Klein field signatures at f₀ = 5.68 Hz.

Author: Klein Field Theory Research Team  
Date: July 2025
"""

import os
import json
import requests
import numpy as np
import pandas as pd
import h5py
import tarfile
from pathlib import Path
from datetime import datetime
import time

class KleinSubthresholdDownloader:
    """
    Downloads LIGO/Virgo subthreshold candidates for Klein field analysis
    """
    
    def __init__(self, data_dir="klein_subthreshold_data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.download_log = []
        
        print("🔍 KLEIN FIELD THEORY SUBTHRESHOLD DOWNLOADER")
        print("=" * 55)
        print(f"📂 Data directory: {self.data_dir.absolute()}")
        print(f"🕒 Timestamp: {datetime.now()}")
        print()
        print("🎯 TARGET: ~2,242 subthreshold candidates")
        print("   • GWTC-2.1: 1,201 candidates (FAR < 2/day)")
        print("   • GWTC-3: 1,041 candidates (FAR < 2/day)")
        print()
        
    def log_download(self, dataset, status, details=""):
        """Log download attempts"""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'dataset': dataset,
            'status': status,
            'details': details
        }
        self.download_log.append(entry)
        
    def download_file(self, url, filename, description=""):
        """Download file with progress tracking"""
        filepath = self.data_dir / filename
        
        if filepath.exists():
            file_size = filepath.stat().st_size
            print(f"✅ {filename} already exists ({file_size:,} bytes)")
            return str(filepath)
            
        try:
            print(f"📥 Downloading {description}")
            print(f"    URL: {url}")
            
            headers = {
                'User-Agent': 'Klein-Field-Theory-Subthreshold-Analysis/1.0'
            }
            
            response = requests.get(url, headers=headers, stream=True, timeout=60)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            
            with open(filepath, 'wb') as f:
                downloaded = 0
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total_size > 0:
                            percent = (downloaded / total_size) * 100
                            print(f"\r    Progress: {percent:.1f}% ({downloaded:,}/{total_size:,} bytes)", end='')
            
            print(f"\n✅ Downloaded {filename} successfully")
            self.log_download(filename, "SUCCESS", f"Size: {downloaded:,} bytes")
            return str(filepath)
            
        except Exception as e:
            print(f"❌ Failed to download {filename}: {e}")
            self.log_download(filename, "FAILED", str(e))
            return None
    
    def download_gwtc21_subthreshold(self):
        """Download GWTC-2.1 subthreshold candidates (1,201 events)"""
        print("\n" + "="*60)
        print("📊 DOWNLOADING GWTC-2.1 SUBTHRESHOLD CANDIDATES")
        print("="*60)
        print("🎯 Target: 1,201 subthreshold candidates from O3a")
        print("📈 Significance: FAR < 2 events/day")
        print()
        
        gwtc21_datasets = {
            'candidates_data': {
                'url': 'https://zenodo.org/records/5117970/files/search_data_GWTC2p1.tar.xml.gz',
                'filename': 'gwtc21_subthreshold_candidates.tar.xml.gz',
                'description': 'GWTC-2.1 subthreshold candidates data (1.6 GB)'
            },
            'analysis_notebook': {
                'url': 'https://zenodo.org/records/5117970/files/search_data.ipynb',
                'filename': 'gwtc21_subthreshold_analysis.ipynb',
                'description': 'GWTC-2.1 subthreshold data usage tutorial'
            }
        }
        
        downloaded_files = {}
        for dataset_name, info in gwtc21_datasets.items():
            result = self.download_file(info['url'], info['filename'], info['description'])
            downloaded_files[dataset_name] = result
            time.sleep(2)
        
        # Extract compressed data
        if downloaded_files['candidates_data']:
            self._extract_gwtc21_data(downloaded_files['candidates_data'])
            
        return downloaded_files
    
    def download_gwtc3_subthreshold(self):
        """Download GWTC-3 subthreshold data (1,041 events)"""
        print("\n" + "="*60)
        print("📊 DOWNLOADING GWTC-3 SUBTHRESHOLD DATA")
        print("="*60)
        print("🎯 Target: 1,041 subthreshold candidates from O3b")
        print("📈 Significance: FAR < 2 events/day")
        print()
        
        gwtc3_datasets = {
            'bbh_population': {
                'url': 'https://zenodo.org/record/5546676/files/endo3_bbhpop-LIGO-T2100113-v12.hdf5',
                'filename': 'gwtc3_subthreshold_bbh_population.hdf5',
                'description': 'GWTC-3 Binary Black Hole subthreshold analysis'
            },
            'bns_population': {
                'url': 'https://zenodo.org/record/5546676/files/endo3_bnspop-LIGO-T2100113-v12.hdf5',
                'filename': 'gwtc3_subthreshold_bns_population.hdf5',
                'description': 'GWTC-3 Binary Neutron Star subthreshold analysis'
            },
            'nsbh_population': {
                'url': 'https://zenodo.org/record/5546676/files/endo3_nsbhpop-LIGO-T2100113-v12.hdf5',
                'filename': 'gwtc3_subthreshold_nsbh_population.hdf5',
                'description': 'GWTC-3 Neutron Star-Black Hole subthreshold analysis'
            },
            'mixture_population': {
                'url': 'https://zenodo.org/record/5546676/files/endo3_mixture-LIGO-T2100113-v12.hdf5',
                'filename': 'gwtc3_subthreshold_mixture_population.hdf5',
                'description': 'GWTC-3 Mixed population subthreshold analysis'
            },
            'documentation': {
                'url': 'https://zenodo.org/record/5546676/files/o3-sensitivity-estimates.md',
                'filename': 'gwtc3_subthreshold_documentation.md',
                'description': 'GWTC-3 subthreshold data format documentation'
            },
            'analysis_notebook': {
                'url': 'https://zenodo.org/record/5546676/files/o3b-vt-dr.ipynb',
                'filename': 'gwtc3_subthreshold_analysis.ipynb',
                'description': 'GWTC-3 O3b subthreshold analysis notebook'
            }
        }
        
        downloaded_files = {}
        for dataset_name, info in gwtc3_datasets.items():
            result = self.download_file(info['url'], info['filename'], info['description'])
            downloaded_files[dataset_name] = result
            time.sleep(2)
            
        return downloaded_files
    
    def _extract_gwtc21_data(self, tar_file_path):
        """Extract GWTC-2.1 compressed data"""
        try:
            print(f"\n📦 Extracting {tar_file_path}...")
            
            extract_dir = self.data_dir / "gwtc21_extracted"
            extract_dir.mkdir(exist_ok=True)
            
            with tarfile.open(tar_file_path, 'r:gz') as tar:
                tar.extractall(extract_dir)
                
            print(f"✅ Extracted to {extract_dir}")
            
            # List extracted contents
            extracted_files = list(extract_dir.rglob('*'))
            print(f"📁 Extracted files: {len(extracted_files)}")
            for file in extracted_files[:10]:  # Show first 10 files
                if file.is_file():
                    print(f"   📄 {file.name} ({file.stat().st_size:,} bytes)")
            if len(extracted_files) > 10:
                print(f"   ... and {len(extracted_files) - 10} more files")
                
        except Exception as e:
            print(f"❌ Error extracting {tar_file_path}: {e}")
    
    def analyze_subthreshold_data(self):
        """Analyze downloaded subthreshold data structure"""
        print("\n" + "="*60)
        print("🔬 ANALYZING SUBTHRESHOLD DATA STRUCTURE")
        print("="*60)
        
        # Analyze GWTC-3 HDF5 files
        hdf5_files = list(self.data_dir.glob('*.hdf5'))
        
        for hdf5_file in hdf5_files:
            try:
                print(f"\n📊 Analyzing {hdf5_file.name}:")
                
                with h5py.File(hdf5_file, 'r') as f:
                    print(f"   📋 Keys: {list(f.keys())}")
                    
                    for key in list(f.keys())[:5]:  # Show first 5 keys
                        dataset = f[key]
                        if hasattr(dataset, 'shape'):
                            print(f"   📈 {key}: shape={dataset.shape}, dtype={dataset.dtype}")
                        else:
                            print(f"   📁 {key}: group with {len(dataset.keys())} items")
                            
            except Exception as e:
                print(f"   ❌ Error analyzing {hdf5_file.name}: {e}")
        
        # Check extracted GWTC-2.1 data
        gwtc21_dir = self.data_dir / "gwtc21_extracted"
        if gwtc21_dir.exists():
            xml_files = list(gwtc21_dir.rglob('*.xml'))
            print(f"\n📊 GWTC-2.1 extracted data:")
            print(f"   📄 XML files found: {len(xml_files)}")
            
            for xml_file in xml_files[:5]:  # Show first 5 files
                size_mb = xml_file.stat().st_size / (1024 * 1024)
                print(f"   📄 {xml_file.name} ({size_mb:.1f} MB)")
    
    def create_klein_analysis_ready_dataset(self):
        """Prepare subthreshold data for Klein field echo analysis"""
        print("\n" + "="*60)
        print("🧪 PREPARING KLEIN FIELD ANALYSIS DATASET")
        print("="*60)
        
        analysis_ready_dir = self.data_dir / "klein_analysis_ready"
        analysis_ready_dir.mkdir(exist_ok=True)
        
        # Create metadata file for Klein analysis
        metadata = {
            'dataset_info': {
                'total_subthreshold_candidates': 2242,
                'gwtc21_candidates': 1201,
                'gwtc3_candidates': 1041,
                'significance_threshold': 'FAR < 2/day',
                'klein_hypothesis': 'Low-significance events may contain 5D Klein field echoes'
            },
            'analysis_parameters': {
                'target_frequency': 5.68,  # Hz, Klein fundamental frequency
                'frequency_tolerance': 0.1,
                'echo_search_window': 0.5,  # seconds after merger
                'min_snr': 4.0,  # Lower than confident detections
                'max_snr': 8.0   # Upper limit for subthreshold
            },
            'file_locations': {
                'gwtc21_data': str(self.data_dir / "gwtc21_extracted"),
                'gwtc3_bbh': str(self.data_dir / "gwtc3_subthreshold_bbh_population.hdf5"),
                'gwtc3_bns': str(self.data_dir / "gwtc3_subthreshold_bns_population.hdf5"),
                'gwtc3_nsbh': str(self.data_dir / "gwtc3_subthreshold_nsbh_population.hdf5"),
                'gwtc3_mixture': str(self.data_dir / "gwtc3_subthreshold_mixture_population.hdf5")
            },
            'download_timestamp': datetime.now().isoformat(),
            'ready_for_klein_analysis': True
        }
        
        metadata_file = analysis_ready_dir / "klein_subthreshold_metadata.json"
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
            
        print(f"✅ Klein analysis metadata saved to: {metadata_file}")
        
        return metadata
    
    def create_summary_report(self):
        """Create comprehensive download summary"""
        print("\n" + "="*80)
        print("📋 SUBTHRESHOLD DOWNLOAD SUMMARY")
        print("="*80)
        
        # Count successful downloads
        successful = len([log for log in self.download_log if log['status'] == 'SUCCESS'])
        total_attempted = len(self.download_log)
        
        print(f"📊 DOWNLOAD STATUS:")
        print(f"   ✅ Successful: {successful}/{total_attempted}")
        print(f"   📂 Data directory: {self.data_dir.absolute()}")
        
        # List downloaded files with sizes
        print(f"\n📁 DOWNLOADED FILES:")
        for file_path in self.data_dir.rglob('*'):
            if file_path.is_file():
                size_mb = file_path.stat().st_size / (1024 * 1024)
                if size_mb > 1:  # Only show files > 1MB
                    print(f"   📄 {file_path.name}: {size_mb:.1f} MB")
        
        # Calculate total data size
        total_size = sum(f.stat().st_size for f in self.data_dir.rglob('*') if f.is_file())
        total_gb = total_size / (1024**3)
        
        print(f"\n💾 TOTAL DATASET SIZE: {total_gb:.2f} GB")
        print(f"🎯 READY FOR KLEIN FIELD ANALYSIS")
        print(f"   • ~2,242 subthreshold candidates")
        print(f"   • Search for Klein echoes at f₀ = 5.68 Hz")
        print(f"   • Test 5D tension hypothesis on low-significance events")
        
        # Save summary
        summary = {
            'download_timestamp': datetime.now().isoformat(),
            'total_files_downloaded': successful,
            'total_size_gb': total_gb,
            'estimated_subthreshold_candidates': 2242,
            'klein_analysis_ready': True,
            'download_log': self.download_log
        }
        
        summary_file = self.data_dir / 'subthreshold_download_summary.json'
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"\n📊 Summary saved to: {summary_file}")
        return summary

def main():
    """Download all LIGO/Virgo subthreshold candidates for Klein analysis"""
    print("🌟 KLEIN FIELD THEORY SUBTHRESHOLD DATA ACQUISITION")
    print("=" * 55)
    print("📡 Downloading low-significance gravitational wave candidates")
    print("🔬 Hypothesis: 5D Klein field echoes in 'noise' events")
    print()
    
    downloader = KleinSubthresholdDownloader()
    
    try:
        print("🚀 Starting subthreshold data download...")
        
        # Download GWTC-2.1 subthreshold candidates
        gwtc21_results = downloader.download_gwtc21_subthreshold()
        
        # Download GWTC-3 subthreshold data
        gwtc3_results = downloader.download_gwtc3_subthreshold()
        
        # Analyze data structure
        downloader.analyze_subthreshold_data()
        
        # Prepare for Klein analysis
        analysis_metadata = downloader.create_klein_analysis_ready_dataset()
        
        # Create summary report
        final_summary = downloader.create_summary_report()
        
        print(f"\n🎉 SUBTHRESHOLD DATA DOWNLOAD COMPLETED!")
        print(f"   📊 Ready to search for Klein field echoes in {final_summary['estimated_subthreshold_candidates']} candidates")
        print(f"   🔍 Next step: Run Klein echo analysis on subthreshold data")
        
        return final_summary
        
    except KeyboardInterrupt:
        print(f"\n⚠️ Download interrupted by user")
        return None
    except Exception as e:
        print(f"\n❌ Error during download: {e}")
        return None

if __name__ == "__main__":
    result = main()