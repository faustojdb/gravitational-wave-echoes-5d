#!/usr/bin/env python3
"""
Download Planck PSZ2 Galaxy Cluster Catalog
==========================================
Downloads the real Planck SZ cluster catalog for Klein analysis.
"""

import requests
import pandas as pd
import numpy as np
from pathlib import Path
import fits
from astropy.io import fits as pyfits
import json

def download_planck_clusters():
    """Download Planck PSZ2 cluster catalog."""
    
    print("🌌 Downloading Planck PSZ2 Galaxy Cluster Catalog")
    print("=" * 50)
    
    # Create data directory
    data_dir = Path("cluster_data")
    data_dir.mkdir(exist_ok=True)
    
    # Planck PSZ2 catalog URL (from Planck Legacy Archive)
    # Note: You may need to visit https://pla.esac.esa.int/pla/ and search for PSZ2
    # The direct URL might change, but this is the typical structure
    
    catalog_urls = {
        # Main PSZ2 catalog
        "PSZ2_catalog": "https://pla.esac.esa.int/pla-sl/data-action?COSMOLOGY.FILENAME=HFI_PCCS_SZ-union_R2.08.fits",
        
        # Alternative: CDS VizieR service (more reliable)
        "PSZ2_vizier": "https://cdsarc.cds.unistra.fr/ftp/J/A+A/594/A27/psz2.dat"
    }
    
    # Try VizieR first (text format, easier to parse)
    print("\n1. Trying VizieR catalog service...")
    
    try:
        # Download from VizieR
        url = "https://vizier.cds.unistra.fr/viz-bin/votable?-source=J/A+A/594/A27&-out.all&-out.form=TSV"
        
        print(f"Downloading from: {url}")
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # Save raw data
        raw_file = data_dir / "psz2_raw.tsv"
        with open(raw_file, 'w') as f:
            f.write(response.text)
        
        print(f"✅ Downloaded raw catalog to {raw_file}")
        
        # Parse the data
        print("\n2. Parsing PSZ2 catalog...")
        
        # Read TSV file, skipping header lines
        # The VizieR format has metadata at the top
        lines = response.text.split('\n')
        
        # Find start of data
        data_start = 0
        for i, line in enumerate(lines):
            if line.startswith('---'):
                data_start = i + 1
                break
        
        # Extract column names
        col_line = lines[data_start - 2]
        columns = col_line.split('\t')
        
        # Read data
        data_lines = []
        for line in lines[data_start:]:
            if line.strip() and not line.startswith('#'):
                data_lines.append(line.split('\t'))
        
        # Create DataFrame
        df = pd.DataFrame(data_lines, columns=columns)
        
        # Clean up column names
        df.columns = df.columns.str.strip()
        
        print(f"✅ Parsed {len(df)} clusters")
        
        # Extract key columns (adjust based on actual column names)
        # Typical PSZ2 columns:
        # - Name: Cluster name
        # - GLON, GLAT: Galactic coordinates
        # - RA, DE: Equatorial coordinates  
        # - z: Redshift
        # - M500: Mass within R500 (10^14 solar masses)
        # - e_M500: Mass error
        
        # Save cleaned catalog
        cleaned_file = data_dir / "psz2_cleaned.csv"
        df.to_csv(cleaned_file, index=False)
        print(f"✅ Saved cleaned catalog to {cleaned_file}")
        
        # Basic statistics
        print("\n3. Catalog statistics:")
        print(f"   Total clusters: {len(df)}")
        
        if 'z' in df.columns:
            z_col = pd.to_numeric(df['z'], errors='coerce')
            print(f"   Redshift range: {z_col.min():.3f} - {z_col.max():.3f}")
            print(f"   Mean redshift: {z_col.mean():.3f}")
        
        if 'M500' in df.columns:
            m_col = pd.to_numeric(df['M500'], errors='coerce')
            print(f"   Mass range: {m_col.min():.2f} - {m_col.max():.2f} × 10¹⁴ M☉")
        
        return df
        
    except Exception as e:
        print(f"❌ VizieR download failed: {str(e)}")
        print("\nTrying alternative method...")
        
        # Alternative: Download pre-processed catalog
        return download_alternative_catalog(data_dir)

def download_alternative_catalog(data_dir):
    """Download alternative cluster catalog."""
    
    print("\n4. Downloading alternative catalog (MCXC)...")
    
    # MCXC (Meta-Catalog of X-ray Clusters)
    # This is a compilation of multiple cluster catalogs
    url = "https://heasarc.gsfc.nasa.gov/cgi-bin/vo/datascope/send.pl?table=mcxclusters&format=csv"
    
    try:
        response = requests.get(url, timeout=60)
        response.raise_for_status()
        
        csv_file = data_dir / "mcxc_clusters.csv"
        with open(csv_file, 'w') as f:
            f.write(response.text)
        
        # Read and process
        df = pd.read_csv(csv_file)
        
        print(f"✅ Downloaded MCXC catalog: {len(df)} clusters")
        
        # MCXC columns typically include:
        # - name: Cluster name
        # - ra, dec: Coordinates
        # - z: Redshift
        # - l500, m500: Mass estimates
        
        return df
        
    except Exception as e:
        print(f"❌ Alternative download failed: {str(e)}")
        return None

def prepare_klein_analysis(df, data_dir):
    """Prepare data for Klein analysis."""
    
    print("\n5. Preparing data for Klein analysis...")
    
    if df is None:
        print("❌ No data available")
        return
    
    # Extract necessary columns for Klein analysis
    analysis_data = {}
    
    # Redshift distribution
    if 'z' in df.columns:
        z = pd.to_numeric(df['z'], errors='coerce').dropna()
        analysis_data['redshifts'] = z.values
        
        # Redshift bins for mass function
        z_bins = np.linspace(0.0, 1.5, 8)
        analysis_data['z_bins'] = z_bins
    
    # Mass data
    mass_col = None
    for col in ['M500', 'm500', 'MASS', 'mass']:
        if col in df.columns:
            mass_col = col
            break
    
    if mass_col:
        masses = pd.to_numeric(df[mass_col], errors='coerce').dropna()
        # Convert to solar masses if needed
        if masses.mean() < 1000:  # Likely in 10^14 units
            masses = masses * 1e14
        analysis_data['masses'] = masses.values
        
        # Mass bins
        log_m_bins = np.linspace(13.5, 15.5, 7)
        analysis_data['log_m_bins'] = log_m_bins
    
    # Save prepared data
    output_file = data_dir / 'planck_clusters_analysis_ready.json'
    
    # Convert numpy arrays to lists for JSON
    save_data = {}
    for key, value in analysis_data.items():
        if isinstance(value, np.ndarray):
            save_data[key] = value.tolist()
        else:
            save_data[key] = value
    
    save_data['n_clusters'] = len(df)
    save_data['catalog_type'] = 'Planck PSZ2' if 'PSZ' in str(df.columns) else 'MCXC'
    
    with open(output_file, 'w') as f:
        json.dump(save_data, f, indent=2)
    
    print(f"✅ Analysis data saved to {output_file}")
    
    # Quick Klein test preview
    if 'redshifts' in analysis_data and 'masses' in analysis_data:
        print("\n6. Quick Klein analysis preview:")
        
        # Count high-mass clusters
        high_mass = analysis_data['masses'] > 5e14
        n_high_mass = np.sum(high_mass)
        fraction_high_mass = n_high_mass / len(analysis_data['masses'])
        
        print(f"   High-mass clusters (M > 5×10¹⁴ M☉): {n_high_mass}")
        print(f"   Fraction: {fraction_high_mass:.3f}")
        
        # Expected in ΛCDM: ~5%
        # Klein predicts: ~5.75% (15% boost)
        klein_expected = 0.05 * 1.15
        
        print(f"   ΛCDM expected: ~5%")
        print(f"   Klein expected: ~{klein_expected:.1%}")
        print(f"   Observed: {fraction_high_mass:.1%}")
        
        if fraction_high_mass > klein_expected * 0.9:
            print("   ✅ Consistent with Klein boost!")
        else:
            print("   ❌ No significant Klein boost detected")

def main():
    """Main function."""
    
    # Download catalog
    df = download_planck_clusters()
    
    if df is not None:
        # Prepare for Klein analysis
        data_dir = Path("cluster_data")
        prepare_klein_analysis(df, data_dir)
        
        print("\n" + "="*50)
        print("✅ Planck cluster data ready for Klein analysis!")
        print(f"📁 Data location: {data_dir}")
        print("\nNext steps:")
        print("1. Run full Klein analysis on real cluster data")
        print("2. Compare with your 1.67σ result")
        print("3. Test if Klein mass boost is real")
    else:
        print("\n❌ Failed to download cluster data")
        print("Please check your internet connection or try:")
        print("1. Visit https://pla.esac.esa.int/pla/")
        print("2. Search for 'PSZ2'")
        print("3. Download the catalog manually")

if __name__ == "__main__":
    main()
