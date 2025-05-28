#!/usr/bin/env python3
"""
Fix LaTeX file by removing problematic Unicode characters
"""

import re

# Read the file
with open('main_paper_complete.tex', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace problematic characters
replacements = {
    '✅': '* ',
    '⚠️': '* ',
    '—': '--',
    '"': '``',
    '"': "''",
    "'": "'",
    '–': '-',
    '…': '...',
    '×': '$\\times$',
    '→': '$\\rightarrow$',
    '≈': '$\\approx$',
    '∝': '$\\propto$',
    '∈': '$\\in$',
    '√': '$\\sqrt{}$',
    'μ': '$\\mu$',
    'ν': '$\\nu$',
    'φ': '$\\phi$',
    'ω': '$\\omega$',
    'τ': '$\\tau$',
    'σ': '$\\sigma$',
    'ρ': '$\\rho$',
    'π': '$\\pi$',
    'Λ': '$\\Lambda$',
    'γ': '$\\gamma$',
    'α': '$\\alpha$',
    'β': '$\\beta$',
    'δ': '$\\delta$',
    'ε': '$\\epsilon$',
    'θ': '$\\theta$',
    'ψ': '$\\psi$',
    'Γ': '$\\Gamma$',
    'Δ': '$\\Delta$',
    'Ω': '$\\Omega$',
    'ℱ': '$\\mathcal{F}$',
    'ℒ': '$\\mathcal{L}$',
    'ℛ': '$\\mathcal{R}$',
    '□': '$\\square$',
}

# Apply replacements
for old, new in replacements.items():
    content = content.replace(old, new)

# Remove any remaining non-ASCII characters
content = re.sub(r'[^\x00-\x7F]+', '', content)

# Write the fixed file
with open('main_paper_complete_fixed.tex', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed LaTeX file created: main_paper_complete_fixed.tex")
print("Now compile with: pdflatex main_paper_complete_fixed.tex")