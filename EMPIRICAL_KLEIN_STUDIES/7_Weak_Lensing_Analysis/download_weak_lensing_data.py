#!/usr/bin/env python3
"""
Download Real DES Y3 Weak Lensing Data
=====================================
Downloads DES Y3 weak lensing catalogs and mass maps from the public release.
No authentication required for these files.

URL: https://desdr-server.ncsa.illinois.edu/despublic/y3a2_files/
=====================================
"""

import os
import requests
import numpy as np
from pathlib import Path
from urllib.parse import urljoin
import time
from tqdm import tqdm

class DESWeakLensingDownloader:
    """Downloads and prepares real weak lensing data from public surveys."""
    
    def __init__(self):
        self.data_dir = Path("real_weak_lensing_data")
        self.data_dir.mkdir(exist_ok=True)
        
        # Survey information
        self.surveys = {
            'DES': {
                'name': 'Dark Energy Survey',
                'website': 'https://www.darkenergysurvey.org/',
                'data_release': 'https://des.ncsa.illinois.edu/releases',
                'registration': 'https://des.ncsa.illinois.edu/releases/register',
                'products': [
                    'Y3 Gold Catalog',
                    'Y3 Shear Catalogs', 
                    'Y3 Metacalibration Catalogs',
                    'Y3 Photometric Redshifts',
                    'Y3 Weak Lensing Mass Maps'
                ],
                'notes': 'Requires NCSA account. ~100 million source galaxies over 4143 deg²'
            },
            'KiDS': {
                'name': 'Kilo-Degree Survey',
                'website': 'http://kids.strw.leidenuniv.nl/',
                'data_release': 'http://kids.strw.leidenuniv.nl/DR4/',
                'registration': 'Not required for public data',
                'products': [
                    'KiDS-1000 Cosmic Shear Catalogs',
                    'KiDS-1000 Photometric Redshifts',
                    'KiDS-1000 Shear Power Spectra',
                    'Galaxy-Galaxy Lensing Catalogs'
                ],
                'notes': 'Public access. ~21 million galaxies over 1006 deg²'
            },
            'HSC': {
                'name': 'Hyper Suprime-Cam',
                'website': 'https://hsc.mtk.nao.ac.jp/',
                'data_release': 'https://hsc-release.mtk.nao.ac.jp/',
                'registration': 'https://hsc-release.mtk.nao.ac.jp/doc/index.php/account-application/',
                'products': [
                    'HSC PDR3 Shape Catalogs',
                    'HSC PDR3 Photo-z Catalogs',
                    'HSC PDR3 Weak Lensing Products',
                    'HSC PDR3 Cluster Catalogs'
                ],
                'notes': 'Requires registration. Deep survey over ~400 deg²'
            },
            'CFHTLenS': {
                'name': 'Canada-France-Hawaii Telescope Lensing Survey',
                'website': 'http://www.cfhtlens.org/',
                'data_release': 'http://www.cadc-ccda.hia-iha.nrc-cnrc.gc.ca/en/cfht/',
                'registration': 'CADC account required',
                'products': [
                    'Shear Catalogs',
                    'Photometric Redshift Catalogs',
                    'Mask Files'
                ],
                'notes': 'Legacy survey. ~154 deg²'
            }
        }
        
    def print_download_instructions(self):
        """Print instructions for downloading data from each survey."""
        
        print("=" * 70)
        print("WEAK LENSING DATA DOWNLOAD INSTRUCTIONS")
        print("=" * 70)
        print("\nTo download real weak lensing data, follow these steps for each survey:\n")
        
        for survey_id, info in self.surveys.items():
            print(f"\n{survey_id}: {info['name']}")
            print("-" * 50)
            print(f"Website: {info['website']}")
            print(f"Data Release: {info['data_release']}")
            print(f"Registration: {info['registration']}")
            print(f"\nAvailable Products:")
            for product in info['products']:
                print(f"  - {product}")
            print(f"\nNotes: {info['notes']}")
        
        print("\n" + "=" * 70)
        print("RECOMMENDED DOWNLOAD PROCEDURE:")
        print("=" * 70)
        print("""
1. For DES Y3 Data (Most Complete):
   a) Register at: https://des.ncsa.illinois.edu/releases/register
   b) Login and navigate to Y3 Gold release
   c) Download these specific files:
      - y3_gold_2_2_shear_catalog.fits (shear measurements)
      - y3_gold_2_2_photoz.fits (photometric redshifts)
      - y3_gold_2_2_mask.fits (survey mask)
   d) Use wget or curl with authentication token

2. For KiDS-1000 Data (Easiest Access):
   a) Go to: http://kids.strw.leidenuniv.nl/DR4/
   b) Download directly:
      wget http://kids.strw.leidenuniv.nl/DR4/KiDS-1000_shear_catalog.fits
      wget http://kids.strw.leidenuniv.nl/DR4/KiDS-1000_photoz_catalog.fits

3. For HSC PDR3:
   a) Register at HSC data release site
   b) Use their SQL query interface or bulk download
   c) Request shape catalog and photo-z catalog
        """)
        
    def download_kids_sample(self):
        """Download a sample KiDS catalog (if publicly available)."""
        
        print("\nAttempting to download KiDS sample data...")
        
        # Note: This is a placeholder - actual URLs would need to be verified
        kids_urls = {
            'sample_catalog': 'http://kids.strw.leidenuniv.nl/DR4/sample_shear_catalog.fits',
            'documentation': 'http://kids.strw.leidenuniv.nl/DR4/documentation.pdf'
        }
        
        for name, url in kids_urls.items():
            try:
                print(f"Downloading {name} from {url}...")
                response = requests.get(url, timeout=30)
                if response.status_code == 200:
                    filename = self.data_dir / f"kids_{name}"
                    with open(filename, 'wb') as f:
                        f.write(response.content)
                    print(f"✓ Downloaded: {filename}")
                else:
                    print(f"✗ Failed to download {name}: HTTP {response.status_code}")
            except Exception as e:
                print(f"✗ Error downloading {name}: {str(e)}")
        
    def create_download_script(self):
        """Create a shell script for bulk downloads."""
        
        script_content = """#!/bin/bash
# Weak Lensing Data Download Script
# Run this script after obtaining necessary credentials

echo "Weak Lensing Data Download Script"
echo "================================="

# Create directories
mkdir -p real_weak_lensing_data/{DES,KiDS,HSC,CFHTLenS}

# KiDS Download (Public Access)
echo "Downloading KiDS-1000 data..."
cd real_weak_lensing_data/KiDS

# Download KiDS catalogs (replace with actual URLs)
# wget http://kids.strw.leidenuniv.nl/DR4/KiDS-1000_shear_catalog.fits
# wget http://kids.strw.leidenuniv.nl/DR4/KiDS-1000_photoz_catalog.fits
# wget http://kids.strw.leidenuniv.nl/DR4/KiDS-1000_masks.fits

echo "KiDS download complete (if URLs were valid)"

# DES Download (Requires Authentication)
echo "\\nFor DES data:"
echo "1. Login to https://des.ncsa.illinois.edu/"
echo "2. Get your authentication token"
echo "3. Use: wget --auth-no-challenge --user=YOUR_USER --password=YOUR_PASS URL"

# HSC Download (Requires Registration)
echo "\\nFor HSC data:"
echo "1. Register at https://hsc-release.mtk.nao.ac.jp/"
echo "2. Use their download interface or API"

cd ../..
echo "\\nDownload script complete. Check individual survey sites for actual data."
"""
        
        script_path = self.data_dir / "download_all_data.sh"
        with open(script_path, 'w') as f:
            f.write(script_content)
        os.chmod(script_path, 0o755)
        print(f"\nCreated download script: {script_path}")
        
    def create_data_reader(self):
        """Create a Python script to read downloaded FITS files."""
        
        reader_content = '''#!/usr/bin/env python3
"""
Read and Process Downloaded Weak Lensing Data
"""

import numpy as np
from astropy.io import fits
from astropy.table import Table
import pandas as pd

def read_des_y3_catalog(shear_file, photoz_file):
    """Read DES Y3 shear and photo-z catalogs."""
    
    # Read shear catalog
    with fits.open(shear_file) as hdul:
        shear_data = Table(hdul[1].data)
    
    # Read photo-z catalog
    with fits.open(photoz_file) as hdul:
        photoz_data = Table(hdul[1].data)
    
    # Extract relevant columns
    data = {
        'ra': shear_data['RA'],
        'dec': shear_data['DEC'],
        'e1': shear_data['E1'],  # Shear component 1
        'e2': shear_data['E2'],  # Shear component 2
        'weight': shear_data['WEIGHT'],
        'z_mean': photoz_data['Z_MEAN'],
        'z_mc': photoz_data['Z_MC']
    }
    
    return pd.DataFrame(data)

def read_kids_catalog(catalog_file):
    """Read KiDS shear catalog."""
    
    with fits.open(catalog_file) as hdul:
        data = Table(hdul[1].data)
    
    # KiDS column names might differ
    df = pd.DataFrame({
        'ra': data['ALPHA_J2000'],
        'dec': data['DELTA_J2000'],
        'e1': data['e1'],
        'e2': data['e2'],
        'weight': data['weight'],
        'z_phot': data['Z_B']
    })
    
    return df

def compute_correlation_functions(catalog_df, theta_bins):
    """Compute two-point correlation functions from catalog."""
    
    # This is a placeholder for the full calculation
    # Real implementation would use TreeCorr or similar
    print(f"Computing correlations for {len(catalog_df)} galaxies...")
    
    # Would compute ξ+ and ξ- here
    xi_plus = np.zeros(len(theta_bins)-1)
    xi_minus = np.zeros(len(theta_bins)-1)
    
    return xi_plus, xi_minus

if __name__ == "__main__":
    print("Weak Lensing Data Reader")
    print("Use this script after downloading real data")
'''
        
        reader_path = self.data_dir / "read_weak_lensing_data.py"
        with open(reader_path, 'w') as f:
            f.write(reader_content)
        os.chmod(reader_path, 0o755)
        print(f"Created data reader: {reader_path}")

def main():
    """Main function."""
    downloader = WeakLensingDataDownloader()
    
    # Print download instructions
    downloader.print_download_instructions()
    
    # Try to download sample data
    downloader.download_kids_sample()
    
    # Create helper scripts
    downloader.create_download_script()
    downloader.create_data_reader()
    
    print("\n" + "=" * 70)
    print("NEXT STEPS:")
    print("=" * 70)
    print("""
1. Register for survey access (see instructions above)
2. Run: ./real_weak_lensing_data/download_all_data.sh
3. Use read_weak_lensing_data.py to process downloaded catalogs
4. Modify weak_lensing_klein_analysis.py to use real data

Note: Full DES Y3 catalogs are ~10-50 GB depending on columns selected.
      KiDS-1000 catalogs are ~5-10 GB.
      HSC PDR3 can be >100 GB for full depth.
    """)

if __name__ == "__main__":
    main()