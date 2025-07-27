#!/usr/bin/env python3
"""
Script para corregir todas las funciones estadísticas en análisis Klein.
"""

import os
import re

def fix_significance_calculations(file_path):
    """Corrige cálculos de significancia en un archivo."""
    
    if not os.path.exists(file_path):
        return False
    
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        original_content = content
        
        # Patrón 1: Reemplazar erfinv usage básico
        pattern1 = r'sigma_level = np\.sqrt\(2\) \* erfinv\(1 - p_value\)'
        replacement1 = 'sigma_level = p_value_to_sigma(p_value)'
        content = re.sub(pattern1, replacement1, content)
        
        # Patrón 2: Reemplazar bloque completo de significancia
        pattern2 = r'if delta_chi2 > 0:\s*p_value = chi2\.sf\(delta_chi2, delta_dof\)\s*sigma_level = np\.sqrt\(2\) \* erfinv\(1 - p_value\) if.*?else:\s*p_value = 1\.0\s*sigma_level = 0\.0'
        replacement2 = '''stats = model_comparison_stats(
            self.results['standard_fit']['chi2'], self.results['standard_fit']['dof'],
            self.results['klein_fit']['chi2'], self.results['klein_fit']['dof']
        )
        
        delta_chi2 = stats['delta_chi2']
        p_value = stats['p_value']
        sigma_level = stats['sigma_level']'''
        
        content = re.sub(pattern2, replacement2, content, flags=re.DOTALL)
        
        # Patrón 3: Versión más simple del bloque significancia
        pattern3 = r'if delta_chi2 > 0:\s+p_value = chi2\.sf\(delta_chi2, delta_dof\)\s+.*?erfinv.*?else:\s+p_value = 1\.0\s+sigma_level = 0\.0'
        
        if re.search(pattern3, content, re.DOTALL):
            content = re.sub(pattern3, replacement2, content, flags=re.DOTALL)
        
        # Corregir también nombres de clase problemáticos
        content = content.replace("class RigorousSupernova eAnalysis:", "class RigorousSupernova Analysis:")
        content = content.replace("RigorousSupernova eAnalysis(", "RigorousSupernova Analysis(")
        
        if content != original_content:
            with open(file_path, 'w') as f:
                f.write(content)
            print(f"  ✓ Updated significance calculations in {os.path.basename(file_path)}")
            return True
        else:
            print(f"  - No changes needed in {os.path.basename(file_path)}")
            return False
            
    except Exception as e:
        print(f"  ✗ Error fixing {file_path}: {e}")
        return False

def main():
    print("🔧 Fixing all statistical calculations in Klein analysis scripts...")
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Todos los archivos de análisis
    files_to_fix = [
        "1_CMB_Analysis/rigorous_analysis/rigorous_cmb_klein_analysis.py",
        "2_PTA_Analysis/rigorous_analysis/rigorous_pta_klein_analysis.py",
        "3_BAO_LSS_Analysis/rigorous_analysis/rigorous_bao_lss_klein_analysis.py", 
        "4_Gravity_Tests/rigorous_analysis/rigorous_gravity_tests_klein_analysis.py",
        "5_Supernovae_Analysis/rigorous_analysis/rigorous_supernovae_klein_analysis.py"
    ]
    
    fixed = 0
    for file_rel_path in files_to_fix:
        file_path = os.path.join(base_dir, file_rel_path)
        if fix_significance_calculations(file_path):
            fixed += 1
    
    print(f"📊 {fixed}/{len(files_to_fix)} archivos actualizados")
    print("✅ All statistical fixes completed!")

if __name__ == "__main__":
    main()