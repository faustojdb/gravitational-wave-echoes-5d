# O3 Search Sensitivity Estimates (LIGO-T2100113)

This data release contains sets of simulated signals (injections) that can be used to estimate search sensitivity throughout the LIGO-Virgo-Kagra (LVK) Collaborations' third observing run (O3).
Four (4) injection sets were considered, each spanning a different region of mass, spin, and redshift parameter space: Binary Neutron Star (BNS), Neutron Star-Black Hole (BBH), Binary Black Hole (BBH), and Intermediate-Mass Black Holes (IMBH).
We describe the injected distributions for each injection set below.
Additionally, we provide a combined set of injections (mixture model) that spans the full parameter space covered by the union of the individual subsets.
Users should use the mixture models by default.

These injection summaries only contain detectable signals, defined by estimated network signal-to-noise ratios larger than a low threshold (either 4 or 6).
This ``hopeless cut'' is applied only for computational reasons and corresponds to a much lower threshold than is actually used to detect real signals in real searches.
A selection of hypothetically detected injections can be obtained by placing a threshold on the search statistics provided.

Injection summaries also contain the draw probability (`sampling_pdf`) evaulated at each injection, along with the parameters of that injection and associated search statistics.
These can be used, in conjunction with a criterion to select detected injections, to estimate search sensitivity through Monte Carlo summation.

---

[[_TOC_]]

---

# Injected Populations

All injected populations are uniformly distributed through time, isotropically distributed throughout the sky, and have isotropically distributed inclinations and polarizations.

## Source-Frame Component Mass Distributions

### BNS, NSBH, and BBH Mass Distribution Parametrization

We parametrize the source-frame mass distribution as separate power laws
```
    p(mass1, mass2) = p(mass1) * p(mass2|mass1)
```
with the convention that `mass1 >= mass2` and
```
    p(mass1) ~ (mass1 - ref_mass1)**pow_mass1 * Theta(min_mass1 <= mass1 <= max_mass1)
    p(mass2|mass1) ~ mass2**pow_mass2 * Theta(min_mass2 <= mass2 <= mass1)
```
`Theta(.)` denotes an indicator function, which is 1 wherever its argument is `True` and 0 whenever its argument is `False`.

### IMBH Mass Distribution Parametrization

The IMBH injections were drawn from a joint distribution over both component masses
```
    p(mass1, mass2) ~ mass1**pow_mass1 * mass2**pow_mass2 \
        * Theta(min_mass1 <= mass1 <= max_mass1) \
        * Theta(min_mass2 <= mass2 <= max_mass2) \
        * Theta(mass2 <= mass1)
```

## Spin Distribution Parametrization

We define the injected spin distribution over Cartesian spin components for each component mass.
The distribution is assumed to be isotropic in direction and uniform in magnitude between zero and a maximum spin (`max_spin`).
```
    p(spinx, spiny, spinz) = 1/(4*pi*(spinx**2 + spiny**2 + spinz**2) * max_spin) \
        * Theta(spinx**2 + spiny**2 + spinz**2 <= max_spin**2)
```
The spin distributions are specified separately for each component mass.

## Redshift Distribution Parametrization

The redshift distribution follows the proposal in 

  * [Maya Fishbach, Daniel E. Holz, and Will M. Farr, *Does the Black Hole Merger Rate Evolve with Redshift?*, ApJL **863** L41 (2018)](https://iopscience.iop.org/article/10.3847/2041-8213/aad800)

Specifically,
```
    p(z) = (dVc/dz) * (1+z)**(pow_z - 1) * Theta(z <= max_z)
```
where `Vc` is the contained comoving volume corresponding to a redshift `z` defined by a flat Lambda-Cold Dark Matter cosmology with parameters ([from Planck 2015](https://doi.org/10.1051/0004-6361/201525830))
```
    H0 = 67.9 km/s/Mpc
    Omega_matter = 0.3065
    Omega_lambda = 0.6935
```

### Binary Neutron Star (BNS)

The parameters for the BNS injected distribution are
```
    min_mass1=1.0 [Msun]
    max_mass1=2.5 [Msun]
    pow_mass1=1.0
    ref_mass1=1.0 [Msun]

    min_mass2=1.0 [Msun]
    max_mass2=2.5 [Msun]
    pow_mass2=0.0

    max_spin1=0.4
    max_spin2=0.4

    max_z=0.15
    pow_z=0.0
```

### Neutron Star-Black Hole (NSBH)

The parameters for the NSBH injected distribution are
```
    min_mass1=2.5 [Msun]
    max_mass1=60.0 [Msun]
    pow_mass1=-2.35
    ref_mass1=0.0 [Msun]

    min_mass2=1.0 [Msun]
    max_mass2=2.5 [Msun]
    pow_mass2=0.0

    max_spin1=0.998
    max_spin2=0.4

    max_z=0.25
    pow_z=0.0
```

### Binary Black Hole (BBH)

The parameters for the BBH injected distribution are
```
    min_mass1=2.0 [Msun]
    max_mass1=100.0 [Msun]
    pow_mass1=-2.35
    ref_mass1=0.0 [Msun]

    min_mass2=2.0 [Msun]
    max_mass2=100.0 [Msun]
    pow_mass2=1.0

    max_spin1=0.998
    max_spin2=0.998

    max_z=1.9
    pow_z=1.0
```
We note that only the BBH distribution defines `pow_z != 0.0`.

## Intermediate Mass Black Hole (IMBH)

The parameters for the IMBH injected distribution are
```
    min_mass1=90.0 [Msun]
    max_mass1=600.0 [Msun]
    pow_mass1=-1.0

    min_mass2=10.0 [Msun]
    max_mass2=600.0 [Msun]
    pow_mass2=-1.0

    max_spin1=0.998
    max_spin2=0.998

    max_z=2.50
    pow_z=0.0
```
We note again that the IMBH mass distribution's parametrization is different from the BNS, NSBH, and BBH mass distributions.

---

# Search Statistics

In addition to injection parameters, we record several statistics for each of several searches included within [GWTC-3]().
Specifically, we include the main search results via the False Alarm Rate (`far`) and the inverse False Alarm Rate (`ifar = 1/far`).
Some searches provide additional statistics, such as their `detection_statistic` or an estimate of the probability the event is of astrophysical origin (`pastro`).
When these results are not available, they are either

  * set to zero when the FAR/iFAR is also unavailable (injection was not found)
  * set to -1 when the FAR/iFAR is available the additional statistics are not
    - currently this only occurs for `pastro_pycbc_bbh` with the IMBH injection set

Injections were performed uniformly in time, regardless of whether the detectors were in science mode.
This means that the set of found injections accounts for both detector duty cycle, and the sensitivity to the intrinsic parameters of each system (e.g., we can see larger masses out to higher redshifts).

The available search statistics are as follows

## Coherent WaveBurst (`cwb`)

  * `far_cwb` [1/year]
  * `ifar_cwb` [years]
  * `detection_statistic_cwb`
  * `pastro_cwb`

## GstLAL (`gstlal`)

  * `far_gstlal` [1/year]
  * `ifar_gstlal` [years]
  * `pastro_gstlal`

## Multi-Band Template Analysis (`mbta`)

  * `far_mbta` [1/year]
  * `ifar_mbta` [years]
  * `detection_statistic_mbta`
  * `pastro_mbta`

## PyCBC BBH-focussed Search (`pycbc_bbh`)

  * `far_pycbc_bbh` [1/year]
  * `ifar_pycbc_bbh` [years]
  * `detection_statistic_pycbc_bbh`
  * `pastro_pycbc_bbh`

For the BNS, NSBH, and BBH injection sets, all these statistics were available.  However for the IMBH injections, only `far_pycbc_bbh` and `ifar_pycbc_bbh` were provided and `pastro_pycbc_bbh` was not available: therefore `pastro_pycbc_bbh` was set to the sentinel value `-1.0` for the IMBH injections.

## PyCBC Broad Search (`pycbc_hyperbank`)

  * `far_pycbc_hyperbank` [1/year]
  * `ifar_pycbc_hyperbank` [years]
  * `detection_statistic_pycbc_hyperbank`
  * `pastro_pycbc_hyperbank`

---

# File Format

Injection summaries are provided as HDF files with a single group (`injections`) containing separate datasets for each injection parameter, search statistic, and draw probability.
Attributes are provided both in the top level of the file and within `injections`.

The file format matches the [GWTC-2 (O3a) injection data release](https://dcc.ligo.org/LIGO-P2000217/public) as closely as possible.

## Datasets

The HDF injection summaries define the following datasets

### Injection Parameters

Component Masses:
  * `injections/mass1` [Msun]
    - detector-frame primary mass
  * `injections/mass2` [Msun]
    - detector-frame secondary mass
  * `injections/mass1_source` [Msun]
    - source-frame primary mass
    - `mass1_source = mass1 / (1 + redshift)`
  * `injections/mass2_source` [Msun]
    - source-frame secondary mass
    - `mass2_source = mass2 / (1 + redshift)`

Cartesian Spin Components
  * `injections/spin1x`
  * `injections/spin1x`
  * `injections/spin1y`
  * `injections/spin2x`
  * `injections/spin2y`
  * `injections/spin2z`

Redshift and Distance
  * `injections/redshift`
  * `injections/distance` [Mpc]
    - luminosity distance

Orientation
  * `injections/declination` [radians]
  * `injections/right_ascension` [radians]
  * `injections/inclination` [radians]
  * `injections/polarization` [radians]

Time
  * `injections/gps_time` [sec]
    - coalescence time of the injection at geocenter; should be within +/- 1 sec of the time in each detector due to time-of-flight delays
  * `injections/gps_time_int` [sec]
    - number of integer seconds in `gps_time`, retained for backward compatibility with O3a injection summaries

### Detection Statistics

Signal to Noise Ratio (`snr`) Estimates

  * `injections/optimal_snr_h`
    - an estimate of the optimal SNR using a reference Power Spectral Density for the LIGO Hanford detector (LHO)
  * `injections/optimal_snr_l`
    - an estimate of the optimal SNR using a reference Power Spectral Desnity for the LIGO Livingston detector (LLO)
  * `injections/optimal_snr_v`
    - an estimate of the optimal SNR using a reference Power Spectral Density for Virgo
    - only present for IMBH subpopulation
  * `injections/optimal_snr_net`
    - network SNR based on single-IFO estimates summed in quadrature
    - BNS, NSBH, and BBH injections only included LLO and LHO when computing `optimal_snr_net`. IMBH injections also included Virgo.

Search Statistics
  * all combinations of `statistic_search` for
    - `statistic` : `far`, `ifar`, `pastro` (and sometimes `detection_statistic`)
    - `search` : `cwb`, `gstlal`, `mbta`, `pycbc_bbh`, and `pycbc_hyperbank` (called "PyCBC-broad" in GWTC-3)

### Draw Probabilities

Draw probabilities (also called sampling PDFs) are the probabilities associated with an injection's parameters under the distribution from which that injection was drawn.
These are needed when reweighing injections to approximate other population models through importance sampling.
*Please note*, sampling PDFs are computed in terms of the variates recorded in the summary files.
That is, datasets named `XXX_sampling_pdf` store the probability density in terms of `XXX`.
The exception is `sampling_pdf`, which defines the joint draw probability over the source-frame component masses, redshift, and cartesian spin components of both objects (see below).
When this joint distribution factors, we also provide `sampling_pdf` datasets over each subset of variates.

However, mixture models only contain the `sampling_pdf` because the joint distribution is not the product of the marginals.
The marginal distributions are therefore unhelpful when importance sampling, and we remove these datasets to prevent possible mistakes from erroneously assuming the mixture model's joint distribution factors nicely.

All files contain

  * `injections/sampling_pdf`
    - `p(mass1_source, mass2_source) * p(spin1x, spin1y, spin1z) * p(spin2x, spin2y, spin2z) * p(z)`
  * `injections/declination_sampling_pdf`
  * `injections/right_ascension_sampling_pdf`
  * `injections/inclination_sampling_pdf`

Subpopulations may additionally contain

  * `injections/mass1_source_sampling_pdf`
    - `p(mass1_source)`
  * `injections/mass1_source_mass2_source_sampling_pdf`
    - `p(mass1_source) * p(mass2_source | mass1_source)`
  * `injections/spin1x_spin1y_spin1z_sampling_pdf`
    - `p(spin1x, spin1y, spin1z)`
  * `injections/spin2x_spin2y_spin2z_sampling_pdf`
    - `p(spin2x, spin2y, spin2z)`
  * `injections/redshift_sampling_pdf`
    - `p(z)`

Other sampling PDFs may be available in certain cases and follow the same naming convention.

### Auxiliary Variables

  * `injections/mixture_weight`
    - the weight to be included in Monte Carlo sums as described in [Essick (2021)](https://iopscience.iop.org/article/10.3847/2515-5172/ac2ba7)

Mixture model summaries will additionally contain nontrivial `mixture_weight`, which is described in more detail in [Essick (2021)](https://iopscience.iop.org/article/10.3847/2515-5172/ac2ba7), in which it is called `w_i`.
Although this dataset is provided, care was taken when constructing mixture models to make the mixture weight as close to unity as possible for all injections.
The systematic error introduced by assuming the mixture weight is always exactly 1 will be much smaller than the statistical uncertainty from the finite number of injections available.

## Attributes

The individual injection summaries also contain the following global summary attributes (`attrs` of the `injections` group within the HDF file, also provided as attrs of the root group in the HDF file for backward compatibility).
Each file will contain at least the following attributes.
Additional attributes may be available, but these can be ignored (are for internal use only).

  * `n_rejected`
    - number of injections rejected as being hopeless to detect
    - for computational reasons, a first cut based on a very small SNR threshold was done to avoid processing "hopelessly quiet" injections
  * `n_accepted`
    - number of injections included in the datasets (not hopeless) and processed by searches.
  * `total_generated`
    - `total_generated = n_accepted + n_rejected`
  * `analysis_time_s` [sec]
    - total time over which injections were generated
    - Note that this spans times when the detectors were not in science mode. Detector duty cycle is accounted for in which injections were detected by searches.

---

# References

More information about how to estimate search sensitivity from injection sets can be found in

  * [Vaibhav Tiwari, *Estimation of the Sensitive Volume for Gravitational Wave Source Populations using Weighted Monte Carlo Integration*, CQG **35**, 14 (2018)](https://iopscience.iop.org/article/10.1088/1361-6382/aac89d)
  * [Will M. Farr, *Accuracy Requirements for Empirically Measured Selection Functions*, Res. Notes AAS, **3** 66 (2019).](https://iopscience.iop.org/article/10.3847/2515-5172/ab1d5f)
  * [Reed Essick, *Constructing Mixture Models for Sensitivity Estimates from Subsets of Separate Injections*, Res. Notes AAS, **5** 220 (2021)](https://iopscience.iop.org/article/10.3847/2515-5172/ac2ba7).


## LVK-internal references

These files were generated with

  * https://git.ligo.org/RatesAndPopulations/lvc-rates-and-pop

at commit 28446706ad69ff815a2ddc0b1dc3cf813215899c.

The IMBH injection sets were generated with

  * https://git.ligo.org/reed.essick/o3-high-mass-bbh-injections

at commit 4fe7f10f90c52d986940b2e1dde47a585b30f680.
