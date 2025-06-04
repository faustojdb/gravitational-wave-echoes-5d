# Klein Bottle Echo Search - Reproducibility Package

## Overview

This package contains all code, data, and documentation necessary to reproduce the results presented in "Robust Evidence for Gravitational Wave Echoes: A Population-Based Search for Klein Bottle Extra Dimensions" by Di Bacco (2025).

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run complete analysis  
python master_analysis.py

# 3. Generate all figures
python generate_all_figures.py

# 4. Verify results
python verify_reproducibility.py
```

## Analysis Pipeline

### Step 1: Population Optimization
```bash
cd Code_Essential/Population_Analysis/
python script1_population_optimization.py
```

### Step 2: Random Experiments  
```bash
cd Code_Essential/Random_Experiments/
python script2_random_experiments.py
```

### Step 3: Statistical Analysis
```bash
cd Code_Essential/Statistical_Tests/
python final_statistical_analysis.py
```

## Expected Results

- **Average significance**: 2.80σ ± 0.28σ
- **Detection rate**: 4.8% ± 4.1%  
- **Null hypothesis p-value**: p < 0.0001
- **Klein bottle parameters**: R_eff = 8400 km, τ = 2.574M^(-0.826) + 0.273 s

## File Structure

```
Klein_Echoes_Publication/
├── Paper_Manuscript/           # LaTeX and Markdown versions
├── Figures_High_Resolution/    # All publication figures  
├── Code_Essential/            # Core analysis scripts
├── Data_Processed/           # Input data and results
├── Results_Outputs/          # Analysis outputs
└── Reproducibility_Package/  # This documentation
```

## Data Sources

All gravitational wave strain data from LIGO Open Science Center:
- https://www.gw-openscience.org/

## Dependencies

- Python 3.8+
- NumPy, SciPy, Matplotlib
- GWpy for gravitational wave analysis
- scikit-learn for statistical methods

## Citation

If you use this code or reproduce these results, please cite:

Di Bacco, F. J. (2025). "Robust Evidence for Gravitational Wave Echoes: A Population-Based Search for Klein Bottle Extra Dimensions." Submitted to Physical Review D.

## Contact

Fausto José Di Bacco  
faustojdb@gmail.com
