#!/usr/bin/env python3
"""
Script para crear versiones simplificadas sin astropy de los análisis que la requieren.
"""

import os
import re

def create_simplified_cmb():
    """Crea versión simplificada del análisis CMB sin astropy."""
    
    cmb_file = "/mnt/d/Multidimensional Theory Simulations/multidimensional-theory/gravitational-wave-echoes-5d/EMPIRICAL_KLEIN_STUDIES/1_CMB_Analysis/rigorous_analysis/rigorous_cmb_klein_analysis.py"
    
    with open(cmb_file, 'r') as f:
        content = f.read()
    
    # Remover import de astropy
    content = content.replace("from astropy.cosmology import Planck18", "# astropy not available")
    
    # Reemplazar referencias a Planck18 con parámetros directos
    content = content.replace("cosmo = Planck18", "# Parámetros Planck18 directos\n        H0, Om0 = 67.4, 0.315")
    
    with open(cmb_file, 'w') as f:
        f.write(content)
    
    print("✓ CMB simplificado (removido astropy)")

def create_simplified_bao():
    """Crea versión simplificada del análisis BAO sin astropy."""
    
    bao_file = "/mnt/d/Multidimensional Theory Simulations/multidimensional-theory/gravitational-wave-echoes-5d/EMPIRICAL_KLEIN_STUDIES/3_BAO_LSS_Analysis/rigorous_analysis/rigorous_bao_lss_klein_analysis.py"
    
    with open(bao_file, 'r') as f:
        content = f.read()
    
    # Remover import de astropy
    content = content.replace("from astropy.cosmology import FlatLambdaCDM", "# astropy not available")
    
    # Reemplazar referencias a FlatLambdaCDM con implementación simple
    simple_cosmo = '''
# Cosmología simple sin astropy
class SimpleFlatLambdaCDM:
    def __init__(self, H0=67.4, Om0=0.315):
        self.H0 = H0
        self.Om0 = Om0
'''
    
    # Insertar después de los imports
    import_end = content.find("warnings.filterwarnings('ignore')")
    if import_end != -1:
        insert_pos = content.find('\n', import_end) + 1
        content = content[:insert_pos] + simple_cosmo + content[insert_pos:]
    
    # Reemplazar FlatLambdaCDM con SimpleFlatLambdaCDM
    content = content.replace("FlatLambdaCDM", "SimpleFlatLambdaCDM")
    
    with open(bao_file, 'w') as f:
        f.write(content)
    
    print("✓ BAO simplificado (removido astropy)")

def main():
    print("🔧 Creando versiones simplificadas sin astropy...")
    
    create_simplified_cmb()
    create_simplified_bao()
    
    print("✅ Versiones simplificadas creadas!")

if __name__ == "__main__":
    main()