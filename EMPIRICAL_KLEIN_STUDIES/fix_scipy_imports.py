#!/usr/bin/env python3
"""
Script para corregir imports de scipy en todos los análisis Klein.
"""

import os
import re

def fix_scipy_imports(file_path):
    """Corrige imports de scipy en un archivo."""
    
    if not os.path.exists(file_path):
        return False
    
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Corregir import de erfinv
        old_import = "from scipy.stats import chi2, erfinv"
        new_import = """from scipy.stats import chi2
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from klein_stats_utils import p_value_to_sigma, model_comparison_stats"""
        
        if old_import in content:
            content = content.replace(old_import, new_import)
            print(f"  ✓ Fixed imports in {os.path.basename(file_path)}")
            
            # Guardar archivo corregido
            with open(file_path, 'w') as f:
                f.write(content)
            return True
    except Exception as e:
        print(f"  ✗ Error fixing {file_path}: {e}")
        return False
        
    return False

def main():
    print("🔧 Fixing scipy imports in all Klein analysis scripts...")
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Archivos a corregir
    files_to_fix = [
        "2_PTA_Analysis/rigorous_analysis/rigorous_pta_klein_analysis.py",
        "3_BAO_LSS_Analysis/rigorous_analysis/rigorous_bao_lss_klein_analysis.py", 
        "4_Gravity_Tests/rigorous_analysis/rigorous_gravity_tests_klein_analysis.py",
        "5_Supernovae_Analysis/rigorous_analysis/rigorous_supernovae_klein_analysis.py"
    ]
    
    fixed = 0
    for file_rel_path in files_to_fix:
        file_path = os.path.join(base_dir, file_rel_path)
        if fix_scipy_imports(file_path):
            fixed += 1
    
    print(f"📊 {fixed}/{len(files_to_fix)} archivos corregidos")
    
    # Corregir también el error de sintaxis en supernovae
    supernovae_file = os.path.join(base_dir, "5_Supernovae_Analysis/rigorous_analysis/rigorous_supernovae_klein_analysis.py")
    if os.path.exists(supernovae_file):
        try:
            with open(supernovae_file, 'r') as f:
                content = f.read()
            
            # Corregir nombre de clase
            content = content.replace("class RigorousSupernova eAnalysis:", "class RigorousSupernova Analysis:")
            content = content.replace("analyzer = RigorousSupernova eAnalysis(", "analyzer = RigorousSupernova Analysis(")
            
            with open(supernovae_file, 'w') as f:
                f.write(content)
            print("  ✓ Fixed Supernovae class name")
        except Exception as e:
            print(f"  ✗ Error fixing Supernovae: {e}")
    
    print("✅ All fixes completed!")

if __name__ == "__main__":
    main()