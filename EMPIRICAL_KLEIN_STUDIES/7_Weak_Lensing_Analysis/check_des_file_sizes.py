#!/usr/bin/env python3
"""
Check DES Y3 File Sizes
=======================
Verifica los tamaños de los archivos antes de descargarlos.
"""

import requests
from pathlib import Path

def check_file_size(url):
    """Check file size without downloading."""
    try:
        response = requests.head(url, allow_redirects=True)
        if 'Content-Length' in response.headers:
            size_bytes = int(response.headers['Content-Length'])
            size_mb = size_bytes / (1024 * 1024)
            size_gb = size_bytes / (1024 * 1024 * 1024)
            
            if size_gb > 1:
                return f"{size_gb:.1f} GB"
            else:
                return f"{size_mb:.1f} MB"
        else:
            return "Unknown size"
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    base_url = "https://desdr-server.ncsa.illinois.edu/despublic/y3a2_files/"
    
    print("🔍 Checking DES Y3 File Sizes")
    print("=" * 40)
    
    # Check current downloaded files
    data_dir = Path("des_y3_real_data/y3kp_cats")
    
    if data_dir.exists():
        print("\n📁 Current local files:")
        for f in data_dir.glob("*.h5"):
            size_mb = f.stat().st_size / (1024 * 1024)
            print(f"  {f.name}: {size_mb:.1f} MB")
    
    # Files we tried to download
    files_to_check = {
        "y3kp_cats": [
            "DESY3_GOLD_2_2.1.h5",
            "DESY3_GOLD_2_2.1_DNF.h5", 
            "DESY3_metacal_v03-004.h5",
        ],
    }
    
    print("\n🌐 Checking remote file sizes:")
    for directory, filenames in files_to_check.items():
        print(f"\n{directory}/")
        for filename in filenames:
            url = f"{base_url}{directory}/{filename}"
            size = check_file_size(url)
            print(f"  {filename}: {size}")
    
    # Suggest alternative files
    print("\n💡 Alternative smaller files that might be available:")
    alternative_files = [
        "y3kp_cats/y3_gold_2_2_small_10k.fits",
        "y3kp_cats/y3_gold_2_2_1_basic_des_y3a2_v02_4.h5", 
        "shear_catalog/mcal-y3a2-v10k.fits",
        "chains/chain_1x2pt_hyperrank_2000_inv.npy",
        "redshift/2pt_NG_final_2ptunblind_02_16_21_wnz.pkl",
    ]
    
    print("\nChecking alternatives...")
    for filepath in alternative_files:
        url = f"{base_url}{filepath}"
        size = check_file_size(url)
        if "Error" not in size:
            print(f"  ✓ {filepath}: {size}")

if __name__ == "__main__":
    main()