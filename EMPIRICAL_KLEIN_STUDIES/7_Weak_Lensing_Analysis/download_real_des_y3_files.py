#!/usr/bin/env python3
"""
Download Actual DES Y3 Weak Lensing Files
=========================================
Auto-generated script with real file names from DES Y3 server.
"""

import requests
import os
from pathlib import Path

def download_file(url, filepath):
    """Download a file."""
    try:
        print(f"Downloading {filepath.name}...")
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        
        print(f"✅ Downloaded: {filepath}")
        return True
    except Exception as e:
        print(f"❌ Failed: {str(e)}")
        return False

def main():
    base_url = "https://desdr-server.ncsa.illinois.edu/despublic/y3a2_files/"
    data_dir = Path("des_y3_real_data")
    data_dir.mkdir(exist_ok=True)
    
    # Files to download (discovered from server)
    files_to_download = {
        "y3kp_cats": [
            "DESY3_GOLD_2_2.1.h5",  # 3
            "DESY3_GOLD_2_2.1_DNF.h5",  # 3
            "DESY3_metacal_v03-004.h5",  # 3
        ],
    }
    
    print("🌌 Downloading Real DES Y3 Weak Lensing Data")
    print("=" * 45)
    
    total_downloaded = 0
    for directory, filenames in files_to_download.items():
        print(f"\n📂 Downloading {directory} files...")
        
        dir_path = data_dir / directory
        dir_path.mkdir(exist_ok=True)
        
        for filename in filenames:
            url = f"{base_url}{directory}/{filename}"
            filepath = dir_path / filename
            
            if filepath.exists():
                print(f"⏭️  Skipping {filename} (exists)")
                continue
            
            if download_file(url, filepath):
                total_downloaded += 1
    
    print(f"\n🎉 Downloaded {total_downloaded} files to {data_dir}")

if __name__ == "__main__":
    main()
