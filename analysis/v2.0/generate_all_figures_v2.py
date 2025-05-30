#!/usr/bin/env python3
"""
Master Script: Create All Diagrams for Paper I v2.0
Generates all 6 figures for the Klein bottle theory paper
"""

import os
import subprocess
import sys

def run_script(script_name):
    """Run a Python script and handle errors"""
    try:
        print(f"\n{'='*60}")
        print(f"Creating {script_name}...")
        print(f"{'='*60}")
        
        result = subprocess.run([sys.executable, script_name], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ SUCCESS: {script_name}")
            if result.stdout:
                print(result.stdout)
        else:
            print(f"❌ ERROR in {script_name}:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ EXCEPTION in {script_name}: {e}")
        return False
    
    return True

def main():
    """Main function to create all diagrams"""
    
    print("🎨 CREATING ALL DIAGRAMS FOR KLEIN BOTTLE PAPER")
    print("=" * 60)
    
    # Ensure we're in the right directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Create figures directory
    os.makedirs('figures', exist_ok=True)
    print(f"📁 Working directory: {script_dir}")
    print(f"📁 Figures directory: {os.path.join(script_dir, 'figures')}")
    
    # List of all diagram scripts in order
    diagram_scripts = [
        'create_klein_topology_diagram.py',
        'create_ligo_analysis_diagram.py', 
        'create_cosmological_evolution_diagram.py',
        'create_physical_mechanism_diagram.py',
        'create_experimental_predictions_diagram.py',
        'create_paradigm_comparison_diagram.py'
    ]
    
    # Figure descriptions
    descriptions = [
        "Figure 1: Klein Bottle Topology and Structure",
        "Figure 2: LIGO Gravitational Wave Echo Analysis", 
        "Figure 3: Cosmological Evolution of Fifth Dimension",
        "Figure 4: Physical Mechanism of Echo Generation",
        "Figure 5: Experimental Predictions and Tests",
        "Figure 6: Paradigm Comparison and Life Implications"
    ]
    
    # Track success/failure
    successful = []
    failed = []
    
    # Execute each script
    for i, (script, description) in enumerate(zip(diagram_scripts, descriptions), 1):
        print(f"\n🔄 [{i}/{len(diagram_scripts)}] {description}")
        
        if os.path.exists(script):
            if run_script(script):
                successful.append((script, description))
            else:
                failed.append((script, description))
        else:
            print(f"❌ MISSING: {script}")
            failed.append((script, description))
    
    # Summary
    print(f"\n{'='*60}")
    print("📊 SUMMARY REPORT")
    print(f"{'='*60}")
    
    print(f"\n✅ SUCCESSFUL ({len(successful)}/{len(diagram_scripts)}):")
    for script, desc in successful:
        print(f"   ✓ {desc}")
    
    if failed:
        print(f"\n❌ FAILED ({len(failed)}/{len(diagram_scripts)}):")
        for script, desc in failed:
            print(f"   ✗ {desc}")
    
    # List generated files
    figures_dir = 'figures'
    if os.path.exists(figures_dir):
        print(f"\n📁 GENERATED FILES in {figures_dir}/:")
        files = sorted([f for f in os.listdir(figures_dir) 
                       if f.endswith(('.png', '.pdf'))])
        
        png_files = [f for f in files if f.endswith('.png')]
        pdf_files = [f for f in files if f.endswith('.pdf')]
        
        print(f"   📄 PNG files ({len(png_files)}):")
        for f in png_files:
            size = os.path.getsize(os.path.join(figures_dir, f)) / 1024
            print(f"      • {f} ({size:.1f} KB)")
            
        print(f"   📄 PDF files ({len(pdf_files)}):")
        for f in pdf_files:
            size = os.path.getsize(os.path.join(figures_dir, f)) / 1024
            print(f"      • {f} ({size:.1f} KB)")
    
    # Final status
    if len(successful) == len(diagram_scripts):
        print(f"\n🎉 ALL DIAGRAMS CREATED SUCCESSFULLY!")
        print(f"   Ready for LaTeX inclusion in paper!")
    else:
        print(f"\n⚠️  {len(failed)} diagram(s) failed to generate")
        print(f"   Please check the error messages above")
    
    return len(failed) == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)