#!/usr/bin/env python3
"""
LaTeX Compilation Script for Fifth Dimension Discovery Paper
===========================================================

Compiles the LaTeX paper to professional PDF format suitable for:
- arXiv submission
- Journal publication (Physical Review Letters)
- Distribution to scientific community

Requirements:
- LaTeX distribution (TeX Live, MiKTeX, etc.)
- Python 3.6+
"""

import os
import subprocess
import sys
from pathlib import Path

def check_latex_installation():
    """Check if LaTeX is properly installed"""
    try:
        result = subprocess.run(['pdflatex', '--version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ LaTeX installation found")
            return True
        else:
            print("❌ LaTeX not found")
            return False
    except FileNotFoundError:
        print("❌ LaTeX not installed")
        return False

def compile_latex_paper():
    """Compile the main LaTeX paper to PDF"""
    
    # Change to papers directory
    papers_dir = Path(__file__).parent / "papers"
    os.chdir(papers_dir)
    
    latex_file = "main_paper_latex.tex"
    
    if not Path(latex_file).exists():
        print(f"❌ LaTeX file {latex_file} not found")
        return False
    
    print(f"🔧 Compiling {latex_file}...")
    
    # First compilation
    print("📝 First pass...")
    result1 = subprocess.run(['pdflatex', '-interaction=nonstopmode', latex_file],
                           capture_output=True, text=True)
    
    if result1.returncode != 0:
        print("❌ First compilation failed:")
        print(result1.stdout[-1000:])  # Last 1000 chars of output
        return False
    
    # Second compilation (for references)
    print("📝 Second pass (references)...")
    result2 = subprocess.run(['pdflatex', '-interaction=nonstopmode', latex_file],
                           capture_output=True, text=True)
    
    if result2.returncode != 0:
        print("❌ Second compilation failed:")
        print(result2.stdout[-1000:])
        return False
    
    # Check if PDF was created
    pdf_file = latex_file.replace('.tex', '.pdf')
    if Path(pdf_file).exists():
        print(f"✅ PDF successfully created: {pdf_file}")
        
        # Get PDF size
        pdf_size = Path(pdf_file).stat().st_size
        print(f"📊 PDF size: {pdf_size / 1024:.1f} KB")
        
        return True
    else:
        print("❌ PDF was not created")
        return False

def clean_latex_files():
    """Clean up auxiliary LaTeX files"""
    papers_dir = Path(__file__).parent / "papers"
    
    extensions_to_remove = ['.aux', '.log', '.out', '.bbl', '.blg', '.fls', '.fdb_latexmk']
    
    for ext in extensions_to_remove:
        for file in papers_dir.glob(f"*{ext}"):
            file.unlink()
            print(f"🧹 Removed {file.name}")

def create_arxiv_version():
    """Create arXiv-optimized version"""
    print("📦 Creating arXiv submission package...")
    
    papers_dir = Path(__file__).parent / "papers"
    arxiv_dir = Path(__file__).parent / "arxiv_submission"
    
    # Create arXiv directory
    arxiv_dir.mkdir(exist_ok=True)
    
    # Copy essential files
    import shutil
    
    # Copy LaTeX source
    shutil.copy(papers_dir / "main_paper_latex.tex", 
                arxiv_dir / "main_paper.tex")
    
    # Copy PDF
    shutil.copy(papers_dir / "main_paper_latex.pdf", 
                arxiv_dir / "main_paper.pdf")
    
    # Copy figures
    figures_dir = Path(__file__).parent / "figures"
    arxiv_figures = arxiv_dir / "figures"
    if figures_dir.exists():
        shutil.copytree(figures_dir, arxiv_figures, dirs_exist_ok=True)
    
    print(f"✅ arXiv package ready in: {arxiv_dir}")
    print("📋 Contents:")
    for file in arxiv_dir.rglob("*"):
        if file.is_file():
            print(f"   - {file.relative_to(arxiv_dir)}")

def main():
    """Main compilation workflow"""
    print("🌟 LaTeX Compilation for Fifth Dimension Discovery Paper")
    print("=" * 60)
    
    # Check LaTeX installation
    if not check_latex_installation():
        print("\n💡 To install LaTeX:")
        print("   Ubuntu/Debian: sudo apt install texlive-full")
        print("   macOS: brew install --cask mactex")
        print("   Windows: Download MiKTeX from miktex.org")
        return False
    
    # Compile paper
    if compile_latex_paper():
        print("\n🎉 Compilation successful!")
        
        # Clean up
        clean_latex_files()
        
        # Create arXiv version
        create_arxiv_version()
        
        print("\n📋 Next steps:")
        print("1. Review the generated PDF")
        print("2. Check figures are properly included")
        print("3. Use arxiv_submission/ folder for arXiv upload")
        print("4. Submit to Physical Review Letters")
        
        return True
    else:
        print("\n❌ Compilation failed")
        print("Check LaTeX installation and file permissions")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)