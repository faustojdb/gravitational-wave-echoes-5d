#!/usr/bin/env python3
"""
Download DES Y3 Weak Lensing Data
=================================
Downloads DES Y3 weak lensing catalogs and mass maps from the public release.
No authentication required!

URL: https://desdr-server.ncsa.illinois.edu/despublic/y3a2_files/
=================================
"""

import os
import requests
import numpy as np
from pathlib import Path
from urllib.parse import urljoin
import time

try:
    from tqdm import tqdm
    HAS_TQDM = True
except ImportError:
    HAS_TQDM = False
    print("Note: tqdm not available. Downloads will work without progress bars.")

class DESWeakLensingDownloader:
    """Downloads DES Y3 weak lensing data from public release."""
    
    def __init__(self):
        self.base_url = "https://desdr-server.ncsa.illinois.edu/despublic/y3a2_files/"
        self.data_dir = Path("des_y3_data")
        self.data_dir.mkdir(exist_ok=True)
        
        # Priority files for Klein analysis
        self.priority_files = {
            # Essential catalogs
            'y3kp_cats': [
                'y3_gold_2_2.h5',  # Main galaxy catalog
                'y3_gold_2_2_shear.h5',  # Shear measurements
                'y3_gold_2_2_photoz.h5',  # Photometric redshifts
                'y3_gold_2_2_mask.h5',  # Survey mask
            ],
            # Mass maps (most direct for Klein detection)
            'massmaps': [
                'y3_kappa_maps.fits',  # Convergence maps
                'y3_mass_maps_metacal.fits',  # Mass maps from metacalibration
                'y3_mass_maps_im3shape.fits',  # Mass maps from IM3SHAPE
            ],
            # Data vectors (pre-computed correlations)
            'datavectors': [
                'xi_pm_metacal.txt',  # ξ± correlation functions
                'xi_pm_im3shape.txt',  # Alternative shear estimator
                'cov_xi_pm.txt',  # Covariance matrix
            ],
            # Beyond ΛCDM analysis (perfect for Klein!)
            'y3a2_beyond_lcdm': [
                'chains_w0wa.txt',  # w0-wa parameter chains
                'chains_modified_gravity.txt',  # Modified gravity chains
                'bestfit_beyond_lcdm.txt',  # Best-fit parameters
            ]
        }
        
        # File size estimates (MB) for download planning
        self.file_sizes = {
            'y3_gold_2_2.h5': 5000,  # ~5GB main catalog
            'y3_gold_2_2_shear.h5': 2000,  # ~2GB shear catalog
            'y3_gold_2_2_photoz.h5': 1000,  # ~1GB photo-z
            'y3_kappa_maps.fits': 1000,  # ~1GB mass maps
            'xi_pm_metacal.txt': 1,  # Small text files
            'xi_pm_im3shape.txt': 1,
            'cov_xi_pm.txt': 10,
        }
    
    def download_file(self, url, filepath, description=None):
        """Download a single file with progress bar."""
        
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            
            desc = description or filepath.name
            
            if HAS_TQDM:
                with tqdm(total=total_size, unit='B', unit_scale=True, desc=desc) as pbar:
                    with open(filepath, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
                                pbar.update(len(chunk))
            else:
                print(f"Downloading {desc}... ({total_size/(1024*1024):.1f} MB)")
                with open(filepath, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
            
            print(f"✓ Downloaded: {filepath}")
            return True
            
        except Exception as e:
            print(f"✗ Failed to download {url}: {str(e)}")
            return False
    
    def check_file_exists(self, url):
        """Check if file exists on server."""
        try:
            response = requests.head(url, timeout=10)
            return response.status_code == 200
        except:
            return False
    
    def download_priority_files(self, categories=None):
        """Download priority files for Klein analysis."""
        
        if categories is None:
            categories = ['y3kp_cats', 'datavectors']  # Start with essentials
        
        print(f"\n🚀 Downloading DES Y3 data from: {self.base_url}")
        print(f"📁 Saving to: {self.data_dir.absolute()}")
        print("=" * 60)
        
        total_downloaded = 0
        total_failed = 0
        
        for category in categories:
            if category not in self.priority_files:
                print(f"❌ Unknown category: {category}")
                continue
                
            print(f"\n📂 Downloading {category} files...")
            category_dir = self.data_dir / category
            category_dir.mkdir(exist_ok=True)
            
            for filename in self.priority_files[category]:
                url = urljoin(self.base_url, f"{category}/{filename}")
                filepath = category_dir / filename
                
                # Skip if already exists
                if filepath.exists():
                    print(f"⏭️  Skipping {filename} (already exists)")
                    continue
                
                # Check if file exists on server
                print(f"🔍 Checking {filename}...")
                if not self.check_file_exists(url):
                    print(f"❌ File not found on server: {filename}")
                    total_failed += 1
                    continue
                
                # Download file
                if self.download_file(url, filepath, f"{category}/{filename}"):
                    total_downloaded += 1
                    time.sleep(1)  # Be nice to server
                else:
                    total_failed += 1
        
        print("\n" + "=" * 60)
        print(f"📊 DOWNLOAD SUMMARY:")
        print(f"✅ Successfully downloaded: {total_downloaded} files")
        print(f"❌ Failed downloads: {total_failed} files")
        print(f"💾 Data saved to: {self.data_dir.absolute()}")
        
        return total_downloaded, total_failed
    
    def download_all_categories(self):
        """Download all priority categories."""
        
        categories = list(self.priority_files.keys())
        return self.download_priority_files(categories)
    
    def list_available_files(self):
        """List what files we're trying to download."""
        
        print("📋 DES Y3 FILES TO DOWNLOAD:")
        print("=" * 50)
        
        total_size_mb = 0
        for category, files in self.priority_files.items():
            print(f"\n📂 {category}:")
            category_size = 0
            
            for filename in files:
                size_mb = self.file_sizes.get(filename, 10)  # Default 10MB
                category_size += size_mb
                print(f"  📄 {filename} (~{size_mb} MB)")
            
            total_size_mb += category_size
            print(f"  📊 Category total: ~{category_size} MB")
        
        print(f"\n💾 ESTIMATED TOTAL SIZE: ~{total_size_mb} MB ({total_size_mb/1024:.1f} GB)")
        print("\n⚠️  Note: Some files may not exist. Script will check before downloading.")

def main():
    """Main function."""
    downloader = DESWeakLensingDownloader()
    
    print("🌌 DES Y3 Weak Lensing Data Downloader")
    print("======================================")
    print("Downloads real DES Y3 weak lensing data for Klein analysis.")
    print("No authentication required!\n")
    
    # List files
    downloader.list_available_files()
    
    # Ask user what to download
    print("\n🤔 What would you like to download?")
    print("1. Essential files only (catalogs + data vectors) [~7 GB]")
    print("2. Essential + mass maps [~8 GB]")
    print("3. Everything including beyond-ΛCDM [~10 GB]")
    print("4. Just list files (no download)")
    
    try:
        choice = input("\nEnter choice (1-4): ").strip()
        
        if choice == '1':
            downloader.download_priority_files(['y3kp_cats', 'datavectors'])
        elif choice == '2':
            downloader.download_priority_files(['y3kp_cats', 'datavectors', 'massmaps'])
        elif choice == '3':
            downloader.download_all_categories()
        elif choice == '4':
            print("\n✅ File listing complete. Run again to download.")
        else:
            print("\n❌ Invalid choice. Run script again.")
            
    except KeyboardInterrupt:
        print("\n\n⚠️  Download interrupted by user.")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
    
    print("\n🚀 Next: Use the downloaded data in weak_lensing_klein_analysis.py")

if __name__ == "__main__":
    main()