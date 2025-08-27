# 5_Code - Implementation Scripts

**Purpose:** All implementation scripts, utilities, and data files

---

## 📁 Structure

### Core Analysis Scripts
**Essential calculations and investigations**

#### `numerical_analysis.py`
- **Purpose:** Core fundamental radius calculation  
- **Key Result:** R_Klein ≈ (m_e × c²) × 10²⁰ correlation discovery

#### `factor_10_20_deep_investigation.py`
- **Purpose:** Deep investigation of 10²⁰ amplification factor
- **Key Result:** 10²⁰ = exp(137 × 0.336) electromagnetic coherence

#### `frequency_scale_diagnosis.py`
- **Purpose:** LIGO frequency optimization analysis
- **Key Result:** Klein_419km → 113.79 Hz (optimal vs 5.68 Hz empirical)

#### `physical_interpretation_investigation.py`
- **Purpose:** Physical meaning and interpretation analysis

---

### Klein Model Implementations

#### `klein_corrected_theory.py`
- **Purpose:** Corrected Klein theory implementation

#### `klein_dynamic_corrected.py`  
- **Purpose:** Dynamic Klein model with R(t) variable radius

#### `klein_quantum_extension.py`
- **Purpose:** Quantum Klein theory extensions

#### `sophisticated_klein_model.py`
- **Purpose:** Advanced Klein framework

#### `sophisticated_ligo_comparison.py`
- **Purpose:** LIGO comparison suite for different Klein radii

---

### Data Processing Scripts

#### `download_using_gwosc_api.py`
- **Purpose:** Download LIGO data using official GWOSC API v2
- **Features:** Proper API endpoint usage, strain file verification

#### `download_ascii_from_csv.py`
- **Purpose:** Download ASCII format LIGO data from event catalog
- **Features:** Alternative download method for ASCII strain data

#### `extract_events_from_catalogs.py`
- **Purpose:** Extract individual events from GWTC catalog files
- **Features:** Parse HDF5 catalogs and extract event metadata

#### `verify_downloaded_files.py`
- **Purpose:** Verify structure and content of downloaded files
- **Features:** HDF5 analysis and data validation

---

### Data Files (`data/` subdirectory)

#### `events.csv`
- **Content:** 219 LIGO events from GWTC catalog
- **Columns:** name, gps, snr, masses, distances, catalog info
- **Source:** Official LIGO-Virgo-KAGRA collaboration data

#### `ligo_events/`
- **Content:** Downloaded LIGO catalog files
- **Format:** HDF5 files with event metadata and population studies
- **Note:** Search summary tables, not strain data

#### `GWOSC API.yaml`
- **Content:** Official GWOSC API v2 specification
- **Purpose:** Reference for proper API usage and endpoints
- **Source:** Gravitational Wave Open Science Center

---

## 🚀 Usage Examples

### Reproduce Core Derivation
```bash
# Fundamental radius calculation
python numerical_analysis.py

# Deep factor investigation
python factor_10_20_deep_investigation.py

# Frequency optimization analysis
python frequency_scale_diagnosis.py
```

### Data Processing
```bash
# Download LIGO data (if needed)
python download_using_gwosc_api.py

# Verify data structure
python verify_downloaded_files.py

# Extract events from catalogs
python extract_events_from_catalogs.py
```

### Klein Model Testing
```bash
# Test different Klein implementations
python klein_corrected_theory.py
python klein_dynamic_corrected.py
python sophisticated_klein_model.py
```

---

## 📊 Key Computational Results

**From `numerical_analysis.py`:**
- R_Klein correlation: 2.5% accuracy with (m_e × c²) × factor
- Discovery of fundamental relationship

**From `factor_10_20_deep_investigation.py`:**
- Factor explanation: 10²⁰ = exp(137 × 0.336)
- Physical interpretation: electromagnetic coherent amplification

**From `frequency_scale_diagnosis.py`:**
- Klein_419km: 113.79 Hz (LIGO optimal)
- Klein_8400km: 5.68 Hz (sub-optimal)
- Performance prediction confirmed by empirical analysis

---

## 🔧 Dependencies

**Required Python packages:**
```
numpy >= 1.24
scipy >= 1.11  
pandas >= 2.1
h5py >= 3.9
requests >= 2.31
matplotlib >= 3.7 (for plotting scripts)
```

**Data requirements:**
- Internet connection for GWOSC API access
- ~500MB storage for downloaded LIGO catalog files
- events.csv must be present in data/ directory

---

**Note:** All scripts are self-contained and include comprehensive error handling and documentation.