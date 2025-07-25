#!/usr/bin/env python3
"""
Explore DES Y3 File Structure
============================
Discovers what files are actually available in each directory
of the DES Y3 public data release.
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from pathlib import Path
import re

class DESExplorer:
    """Explores the DES Y3 data structure."""
    
    def __init__(self):
        self.base_url = "https://desdr-server.ncsa.illinois.edu/despublic/y3a2_files/"
        
        # Directories of interest for weak lensing
        self.directories = [
            'y3kp_cats',
            'massmaps', 
            'datavectors',
            'y3a2_beyond_lcdm',
            'y3a2_cmblens',
            'y3a2_joint-des-kids'
        ]
    
    def get_directory_listing(self, directory):
        """Get list of files in a directory."""
        
        url = urljoin(self.base_url, f"{directory}/")
        
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            # Parse HTML to extract file links
            soup = BeautifulSoup(response.text, 'html.parser')
            links = soup.find_all('a', href=True)
            
            files = []
            for link in links:
                href = link['href']
                # Skip parent directory and other navigation links
                if href.startswith('../') or href.startswith('/') or href == './':
                    continue
                
                # Get file info
                text = link.get_text().strip()
                if text and not text.endswith('/'):  # Not a subdirectory
                    # Try to extract file size from the listing
                    parent_text = str(link.parent)
                    size_match = re.search(r'(\d+\.?\d*[KMGT]?B?)', parent_text)
                    size = size_match.group(1) if size_match else "Unknown"
                    
                    files.append({
                        'name': href,
                        'size': size,
                        'url': urljoin(url, href)
                    })
            
            return files
            
        except Exception as e:
            print(f"❌ Error exploring {directory}: {str(e)}")
            return []
    
    def explore_all_directories(self):
        """Explore all directories and print structure."""
        
        print("🔍 EXPLORING DES Y3 DATA STRUCTURE")
        print("=" * 50)
        print(f"Base URL: {self.base_url}")
        print()
        
        all_files = {}
        
        for directory in self.directories:
            print(f"📂 Exploring {directory}/...")
            files = self.get_directory_listing(directory)
            
            if files:
                all_files[directory] = files
                print(f"✅ Found {len(files)} files in {directory}/")
                
                # Show first few files as preview
                for i, file_info in enumerate(files[:5]):
                    print(f"  📄 {file_info['name']} ({file_info['size']})")
                
                if len(files) > 5:
                    print(f"  ... and {len(files) - 5} more files")
            else:
                print(f"❌ No files found or error accessing {directory}/")
            
            print()
        
        return all_files
    
    def find_weak_lensing_files(self, all_files):
        """Identify the most relevant files for weak lensing analysis."""
        
        print("🎯 IDENTIFYING WEAK LENSING FILES")
        print("=" * 40)
        
        # Keywords to look for
        wl_keywords = [
            'shear', 'xi', 'correlation', 'mass', 'kappa', 'gamma',
            'metacal', 'im3shape', 'gold', 'photoz', 'catalog'
        ]
        
        priority_files = {}
        
        for directory, files in all_files.items():
            relevant_files = []
            
            for file_info in files:
                filename = file_info['name'].lower()
                
                # Check if filename contains weak lensing keywords
                for keyword in wl_keywords:
                    if keyword in filename:
                        relevant_files.append(file_info)
                        break
            
            if relevant_files:
                priority_files[directory] = relevant_files
                print(f"\n📂 {directory}/ - {len(relevant_files)} relevant files:")
                
                for file_info in relevant_files:
                    print(f"  🌟 {file_info['name']} ({file_info['size']})")
        
        return priority_files
    
    def generate_download_script(self, priority_files):
        """Generate a download script with the actual file names."""
        
        script_content = '''#!/usr/bin/env python3
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
'''
        
        # Add the discovered files
        for directory, files in priority_files.items():
            script_content += f'        "{directory}": [\n'
            for file_info in files:
                script_content += f'            "{file_info["name"]}",  # {file_info["size"]}\n'
            script_content += f'        ],\n'
        
        script_content += '''    }
    
    print("🌌 Downloading Real DES Y3 Weak Lensing Data")
    print("=" * 45)
    
    total_downloaded = 0
    for directory, filenames in files_to_download.items():
        print(f"\\n📂 Downloading {directory} files...")
        
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
    
    print(f"\\n🎉 Downloaded {total_downloaded} files to {data_dir}")

if __name__ == "__main__":
    main()
'''
        
        # Save the script
        script_path = Path("download_real_des_y3_files.py")
        with open(script_path, 'w') as f:
            f.write(script_content)
        
        print(f"\n✅ Generated download script: {script_path}")
        print("🚀 Run it with: python3 download_real_des_y3_files.py")

def main():
    explorer = DESExplorer()
    
    # Explore the directory structure
    all_files = explorer.explore_all_directories()
    
    if all_files:
        # Find weak lensing relevant files
        priority_files = explorer.find_weak_lensing_files(all_files)
        
        if priority_files:
            # Generate download script
            explorer.generate_download_script(priority_files)
        else:
            print("❌ No weak lensing files identified")
    else:
        print("❌ No files found in any directory")

if __name__ == "__main__":
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        print("❌ BeautifulSoup4 not available.")
        print("This script needs to parse HTML to discover file names.")
        print("Install with: pip install beautifulsoup4")
        print("\nAlternatively, check the directories manually at:")
        print("https://desdr-server.ncsa.illinois.edu/despublic/y3a2_files/")
        exit(1)
    
    main()