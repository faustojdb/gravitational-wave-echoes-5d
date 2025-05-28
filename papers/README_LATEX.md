# LaTeX Compilation Guide

## Files Created

### Main LaTeX Document
- `main_paper_latex.tex` - Complete paper in professional LaTeX format
- Uses `revtex4-2` class (standard for Physical Review Letters)
- All equations properly formatted
- Professional bibliography

### Compilation Script
- `../compile_latex.py` - Automated compilation with error checking

## Manual Compilation (if script fails)

```bash
cd papers/
pdflatex main_paper_latex.tex
pdflatex main_paper_latex.tex  # Second pass for references
```

## Required LaTeX Packages

The document uses these packages (usually included in full LaTeX distributions):
- `revtex4-2` (REVTeX class for physics journals)
- `amsmath`, `amsfonts`, `amssymb` (mathematical symbols)
- `graphicx` (figure inclusion)
- `hyperref` (clickable links)
- `physics` (physics notation)
- `siunitx` (unit formatting)
- `booktabs` (professional tables)

## Installation Commands

### Ubuntu/Debian
```bash
sudo apt update
sudo apt install texlive-full
```

### macOS
```bash
brew install --cask mactex
```

### Windows
Download and install MiKTeX from: https://miktex.org/

## Troubleshooting

### Missing Packages Error
If you get "File 'xxx.sty' not found":
```bash
# Install specific packages (Ubuntu/Debian)
sudo apt install texlive-publishers  # For revtex4-2
sudo apt install texlive-science     # For physics package
```

### Compilation Errors
1. Check for syntax errors in the .tex file
2. Make sure all figures are in the correct path
3. Run pdflatex twice (first pass processes text, second pass handles references)

## Expected Output

- `main_paper_latex.pdf` - Professional quality PDF
- File size: ~500-800 KB
- Pages: ~8-12 (two-column format)
- All equations and figures properly rendered

## arXiv Submission

After successful compilation:
1. Upload the .tex source file to arXiv
2. Include figure files if referenced
3. arXiv will automatically compile to PDF

## Journal Submission

For Physical Review Letters:
1. Use the generated PDF
2. Submit figures separately if required
3. Include source .tex file for production