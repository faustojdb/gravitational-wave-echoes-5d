#!/usr/bin/env python3
"""
Investigate Real Planck Data Structure
=====================================
Let's properly understand what data we actually downloaded.
"""

import pandas as pd
import numpy as np
from pathlib import Path

def investigate_vizier_format():
    """Investigate the VizieR TSV format."""
    
    print("🔍 Investigating Planck cluster data structure...")
    print("=" * 60)
    
    # Read raw TSV file
    raw_file = Path("cluster_data/psz2_raw.tsv")
    
    with open(raw_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    print(f"Total lines: {len(lines)}")
    
    # Find the actual PSZ2 catalog reference
    print("\n1. Looking for catalog identification...")
    for i, line in enumerate(lines[:50]):
        if 'PSZ' in line or 'Planck' in line or 'A+A' in line:
            print(f"Line {i}: {line.strip()}")
    
    # Find column headers
    print("\n2. Looking for column definitions...")
    header_lines = []
    data_start = 0
    
    for i, line in enumerate(lines):
        if line.startswith('#') or line.startswith(';'):
            if 'Name' in line or 'RA' in line or 'M500' in line or any(key in line for key in ['z', 'Mass', 'SNR']):
                header_lines.append((i, line.strip()))
        elif '---' in line:
            data_start = i + 1
            break
    
    print("\nHeader lines found:")
    for i, line in header_lines[:20]:
        print(f"Line {i}: {line[:100]}")
    
    # Try to parse with correct delimiter
    print(f"\n3. Data starts at line {data_start}")
    
    # Sample first few data lines
    print("\nFirst 5 data lines:")
    for i in range(data_start, min(data_start + 5, len(lines))):
        if i < len(lines):
            print(f"Line {i}: {lines[i].strip()[:150]}...")
    
    # Count fields in data lines
    if data_start < len(lines):
        fields = lines[data_start].strip().split('\t')
        print(f"\nNumber of tab-separated fields: {len(fields)}")
        
        # Try other delimiters
        for delim in ['|', '  ', '   ']:
            fields_alt = lines[data_start].strip().split(delim)
            if len(fields_alt) > len(fields):
                print(f"Number of '{delim}'-separated fields: {len(fields_alt)}")
    
    # Try to identify PSZ2 catalog format
    print("\n4. Attempting to identify catalog format...")
    
    # PSZ2 catalog typically has these columns:
    # Name, GLON, GLAT, RA, DEC, SNR, z, M500, etc.
    
    # Look for tell-tale signs
    psz2_indicators = ['PSZ2', 'SNR', 'M500', 'GLON', 'GLAT']
    found_indicators = []
    
    for indicator in psz2_indicators:
        for line in lines[:100]:
            if indicator in line:
                found_indicators.append(indicator)
                break
    
    print(f"Found PSZ2 indicators: {found_indicators}")
    
    # Try to load with pandas using different strategies
    print("\n5. Attempting to parse with pandas...")
    
    # Strategy 1: Skip to data and use tabs
    try:
        df1 = pd.read_csv(raw_file, sep='\t', skiprows=data_start-1, 
                         nrows=10, header=None)
        print(f"\nTab-delimited parsing: {df1.shape}")
        print("First row sample:")
        print(df1.iloc[0])
    except Exception as e:
        print(f"Tab parsing failed: {e}")
    
    # Strategy 2: Look for VizieR format markers
    for i, line in enumerate(lines):
        if 'Name' in line and ('RA' in line or 'GLON' in line):
            print(f"\nPotential header at line {i}: {line.strip()}")
            
            # Try to extract column names
            if '\t' in line:
                cols = line.strip().split('\t')
            else:
                cols = line.strip().split()
            
            print(f"Extracted {len(cols)} column names")
            print(f"Columns: {cols[:10]}...")
            
            try:
                df2 = pd.read_csv(raw_file, sep='\t', skiprows=i+1,
                                 names=cols, nrows=10)
                print(f"\nParsed with extracted columns: {df2.shape}")
                print("Columns with 'M' or 'z':")
                for col in df2.columns:
                    if 'M' in col or 'z' in col or 'mass' in col.lower():
                        print(f"  {col}: {df2[col].iloc[0]}")
            except:
                pass
    
    return data_start, lines

def analyze_cleaned_csv():
    """Analyze the cleaned CSV we already have."""
    
    print("\n\n6. Analyzing cleaned CSV structure...")
    print("=" * 60)
    
    csv_file = Path("cluster_data/psz2_cleaned.csv")
    df = pd.read_csv(csv_file)
    
    print(f"Shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    
    # Analyze each column
    print("\nColumn analysis:")
    
    for col in df.columns:
        try:
            # Skip if mostly null
            if df[col].notna().sum() < 10:
                continue
                
            # Try to convert to numeric
            numeric_vals = pd.to_numeric(df[col], errors='coerce')
            n_numeric = numeric_vals.notna().sum()
            
            if n_numeric > len(df) * 0.5:  # At least 50% numeric
                min_val = numeric_vals.min()
                max_val = numeric_vals.max()
                mean_val = numeric_vals.mean()
                
                print(f"\n{col}:")
                print(f"  Numeric values: {n_numeric}/{len(df)}")
                print(f"  Range: {min_val:.3g} to {max_val:.3g}")
                print(f"  Mean: {mean_val:.3g}")
                
                # Guess what it might be
                if 0 < min_val < 5 and max_val < 10:
                    print("  → Possibly REDSHIFT")
                elif 1e13 < mean_val < 1e16:
                    print("  → Possibly MASS (solar masses)")
                elif 0.1 < mean_val < 100:
                    print("  → Possibly MASS (10^14 solar masses)")
                elif 0 < mean_val < 360:
                    print("  → Possibly COORDINATES (deg)")
                elif 1 < mean_val < 50:
                    print("  → Possibly SNR")
        except:
            pass
    
    # Check if this is actually PSZ2 or something else
    print("\n7. Checking if this is really PSZ2 catalog...")
    
    # Real PSZ2 has exactly 1653 confirmed clusters
    if 1500 < len(df) < 1700:
        print("✓ Row count consistent with PSZ2 catalog (1653 clusters)")
    elif 5000 < len(df) < 6000:
        print("✓ Row count suggests this might be extended PSZ2 catalog or candidates")
    else:
        print("? Unexpected row count for PSZ2")
    
    # Look for PSZ2 naming convention
    name_cols = [col for col in df.columns if df[col].dtype == 'object']
    for col in name_cols[:5]:
        sample = df[col].dropna().iloc[:5]
        if any('PSZ' in str(val) for val in sample):
            print(f"\n✓ Found PSZ2 names in column '{col}':")
            print(sample)
            break

def manual_parse_psz2():
    """Manually parse PSZ2 catalog based on known format."""
    
    print("\n\n8. Manual parsing based on PSZ2 format...")
    print("=" * 60)
    
    # Known PSZ2 catalog format from Planck documentation:
    # The PSZ2 catalog from VizieR typically has these columns:
    # Name | GLON | GLAT | RA | DEC | SNR | z | M500 | ...
    
    raw_file = Path("cluster_data/psz2_raw.tsv")
    
    # Read and find data section
    with open(raw_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Find where actual data starts (after dashed line)
    data_start = 0
    for i, line in enumerate(lines):
        if '---' in line and len(line.strip()) > 20:
            data_start = i + 1
            break
    
    print(f"Data starts at line {data_start}")
    
    # Parse a few lines manually
    parsed_data = []
    for i in range(data_start, min(data_start + 100, len(lines))):
        if i < len(lines) and lines[i].strip():
            # Try different delimiters
            fields = None
            if '\t' in lines[i]:
                fields = lines[i].strip().split('\t')
            elif '|' in lines[i]:
                fields = [f.strip() for f in lines[i].strip().split('|')]
            else:
                fields = lines[i].strip().split()
            
            if fields and len(fields) > 5:
                parsed_data.append(fields)
    
    if parsed_data:
        print(f"\nParsed {len(parsed_data)} lines")
        print(f"Fields per line: {len(parsed_data[0])}")
        
        # Show sample
        print("\nSample parsed data (first 3 rows, first 8 fields):")
        for row in parsed_data[:3]:
            print([f[:20] for f in row[:8]])
        
        # Try to identify mass and redshift columns
        print("\n9. Searching for mass and redshift columns...")
        
        for col_idx in range(min(len(parsed_data[0]), 20)):
            col_vals = [row[col_idx] for row in parsed_data[:20] if col_idx < len(row)]
            
            # Try to convert to float
            numeric_vals = []
            for val in col_vals:
                try:
                    numeric_vals.append(float(val))
                except:
                    pass
            
            if len(numeric_vals) > 5:
                min_val = min(numeric_vals)
                max_val = max(numeric_vals)
                mean_val = sum(numeric_vals) / len(numeric_vals)
                
                # Check if this could be redshift (0 < z < 3)
                if 0 < min_val < 0.5 and 0.5 < max_val < 3:
                    print(f"\nColumn {col_idx} might be REDSHIFT:")
                    print(f"  Range: {min_val:.3f} to {max_val:.3f}")
                    print(f"  Sample: {numeric_vals[:5]}")
                
                # Check if this could be mass (10^14 solar masses)
                elif 0.1 < min_val < 50 and max_val < 100:
                    print(f"\nColumn {col_idx} might be MASS (10^14 M☉):")
                    print(f"  Range: {min_val:.3f} to {max_val:.3f}")
                    print(f"  Sample: {numeric_vals[:5]}")

def main():
    """Run all investigations."""
    
    # First investigate raw format
    data_start, lines = investigate_vizier_format()
    
    # Then analyze cleaned CSV
    analyze_cleaned_csv()
    
    # Finally try manual parsing
    manual_parse_psz2()
    
    print("\n\n" + "=" * 60)
    print("INVESTIGATION COMPLETE")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Check if we downloaded the right catalog")
    print("2. Look for column documentation on VizieR")
    print("3. Try alternative Planck data sources")
    print("4. Use columns identified as likely mass/redshift")

if __name__ == "__main__":
    main()