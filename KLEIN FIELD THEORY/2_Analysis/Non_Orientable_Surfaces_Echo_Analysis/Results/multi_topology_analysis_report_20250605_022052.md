
# Multi-Topology LIGO Analysis Report

**Analysis Date:** 2025-06-05T02:20:52.615299
**Best Performing Topology:** String_Orientifold

## Executive Summary

We tested 5 non-orientable topologies against LIGO gravitational wave data:

## Topology Performance Ranking

| Rank | Topology | Combined σ | Detection Rate | f₀ (Hz) |
|------|----------|------------|----------------|----------|
| 1 | String_Orientifold | 2.42σ | 25.0% | 6.8 |
| 2 | Mobius_Band | 1.82σ | 50.0% | 8.2 |
| 3 | Klein_Bottle | 0.00σ | 0.0% | 6.7 |
| 4 | Real_Projective_Plane | 0.00σ | 0.0% | 4.2 |
| 5 | Twisted_Torus | 0.00σ | 0.0% | 7.1 |

## Detailed Analysis

### Klein_Bottle

- **Fundamental frequency:** 6.7 Hz
- **Detection rate:** 0.0%
- **Mean significance:** 0.00σ
- **Combined significance:** 0.00σ

**Event Results:**
- GW150914: Not detected (σ = 0.00)
- GW151226: Not detected (σ = 0.00)
- GW170104: Not detected (σ = 0.16)
- GW170814: Not detected (σ = 0.00)

### Real_Projective_Plane

- **Fundamental frequency:** 4.2 Hz
- **Detection rate:** 0.0%
- **Mean significance:** 0.00σ
- **Combined significance:** 0.00σ

**Event Results:**
- GW150914: Not detected (σ = 0.00)
- GW151226: Not detected (σ = 0.23)
- GW170104: Not detected (σ = 0.46)
- GW170814: Not detected (σ = 0.08)

### Mobius_Band

- **Fundamental frequency:** 8.2 Hz
- **Detection rate:** 50.0%
- **Mean significance:** 1.27σ
- **Combined significance:** 1.82σ

**Event Results:**
- GW150914: Not detected (σ = 0.24)
- GW151226: **DETECTED** (σ = 1.46)
- GW170104: Not detected (σ = 0.93)
- GW170814: **DETECTED** (σ = 1.08)

### Twisted_Torus

- **Fundamental frequency:** 7.1 Hz
- **Detection rate:** 0.0%
- **Mean significance:** 0.00σ
- **Combined significance:** 0.00σ

**Event Results:**
- GW150914: Not detected (σ = 0.86)
- GW151226: Not detected (σ = 0.78)
- GW170104: Not detected (σ = 0.00)
- GW170814: Not detected (σ = 0.66)

### String_Orientifold

- **Fundamental frequency:** 6.8 Hz
- **Detection rate:** 25.0%
- **Mean significance:** 2.42σ
- **Combined significance:** 2.42σ

**Event Results:**
- GW150914: Not detected (σ = 0.34)
- GW151226: Not detected (σ = 0.61)
- GW170104: Not detected (σ = 0.88)
- GW170814: **DETECTED** (σ = 2.42)

## Key Findings

**String_Orientifold shows the strongest evidence** with 2.42σ combined significance.

## Next Steps

1. Apply to full GWTC catalog (65+ events)
2. Implement advanced template matching
3. Search for topology-specific signatures
4. Bayesian model selection
