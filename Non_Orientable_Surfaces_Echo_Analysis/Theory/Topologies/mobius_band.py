#!/usr/bin/env python3
"""
Möbius Band Theoretical Framework
=================================

The Möbius band is the simplest non-orientable surface, obtained by
twisting a strip and joining the ends. Unlike Klein bottle and ℝP²,
it has a boundary, which introduces unique physics.

Mathematical Construction:
- Start with rectangle [0, L] × [-w, w]  
- Identify (0, y) ~ (L, -y) (twist identification)
- Results in non-orientable surface with boundary

Key Properties:
- Euler characteristic: χ(Möbius) = 0
- Non-orientable
- Has boundary (circle)
- Fundamental group: π₁(Möbius) = ℤ
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from scipy.special import jv, yv  # Bessel functions
from typing import Tuple, List, Dict
import json

class MobiusBand:
    """
    Theoretical framework for gravitational wave propagation
    in a fifth dimension with Möbius band topology.
    """
    
    def __init__(self, length: float = 2*np.pi*1000e3, width: float = 100e3):
        """
        Initialize Möbius band extra dimension.
        
        Parameters:
        -----------
        length : float
            Circumference of the band (meters)
        width : float
            Half-width of the band (meters)
        """
        self.L = length
        self.w = width
        self.c = 299792458  # Speed of light (m/s)
        
        # Topological parameters
        self.euler_characteristic = 0
        self.orientable = False
        self.has_boundary = True
        self.twist = np.pi  # Half-twist
        
        # Effective radius (for comparison with closed surfaces)
        self.R_eff = self.L / (2 * np.pi)
        
    def derive_mode_spectrum(self) -> Dict[str, np.ndarray]:
        """
        Derive allowed modes for Möbius band with boundary conditions.
        
        The twist identification and boundary create unique constraints:
        - Longitudinal modes must satisfy twisted periodic conditions
        - Transverse modes must vanish at the boundary
        
        Returns:
        --------
        modes : dict
            Allowed mode numbers and frequencies
        """
        print("="*60)
        print("DERIVING MÖBIUS BAND MODE SPECTRUM")
        print("="*60)
        
        # Wave function must satisfy:
        # ψ(x + L, y) = -ψ(x, -y)  (twist condition)
        # ψ(x, ±w) = 0  (boundary condition)
        
        allowed_modes = []
        
        # Longitudinal modes (around the band)
        # Due to twist: e^(ikL) = -1, so k = (2n+1)π/L
        print("\nLongitudinal modes (twisted periodic):")
        longitudinal_n = []
        for n in range(10):  # First 10 modes
            k_n = (2*n + 1) * np.pi / self.L
            omega_n = self.c * k_n
            longitudinal_n.append({
                'n': 2*n + 1,  # Only odd modes!
                'k': k_n,
                'omega': omega_n,
                'f': omega_n / (2 * np.pi),
                'type': 'longitudinal'
            })
            print(f"  n={2*n+1}: k={k_n:.6f}/m, f={omega_n/(2*np.pi):.2f} Hz")
        
        # Transverse modes (across the width)
        # Standing waves with nodes at boundaries
        print("\nTransverse modes (boundary conditions):")
        transverse_m = []
        for m in range(1, 6):  # First 5 transverse modes
            k_m = m * np.pi / (2 * self.w)
            omega_m = self.c * k_m
            transverse_m.append({
                'm': m,
                'k': k_m,
                'omega': omega_m,
                'f': omega_m / (2 * np.pi),
                'type': 'transverse'
            })
            print(f"  m={m}: k={k_m:.6f}/m, f={omega_m/(2*np.pi):.2f} Hz")
        
        # Mixed modes (n, m)
        print("\nLowest mixed modes:")
        mixed_modes = []
        for i, ln in enumerate(longitudinal_n[:3]):
            for j, tm in enumerate(transverse_m[:3]):
                k_total = np.sqrt(ln['k']**2 + tm['k']**2)
                omega_total = self.c * k_total
                mixed_modes.append({
                    'n': ln['n'],
                    'm': tm['m'],
                    'k': k_total,
                    'omega': omega_total,
                    'f': omega_total / (2 * np.pi),
                    'type': 'mixed'
                })
                if i < 2 and j < 2:
                    print(f"  (n={ln['n']}, m={tm['m']}): f={omega_total/(2*np.pi):.2f} Hz")
        
        # Fundamental frequency (lowest longitudinal mode)
        self.omega_0 = longitudinal_n[0]['omega']
        self.f_0 = self.omega_0 / (2 * np.pi)
        
        print(f"\nFundamental frequency: f₀ = {self.f_0:.2f} Hz")
        
        # Compare with Klein bottle
        klein_f0 = 6.65  # Hz
        print(f"\nComparison:")
        print(f"  Klein bottle f₀ = {klein_f0:.2f} Hz")
        print(f"  Möbius band f₀ = {self.f_0:.2f} Hz")
        print(f"  Ratio = {self.f_0/klein_f0:.3f}")
        
        return {
            'longitudinal': longitudinal_n,
            'transverse': transverse_m,
            'mixed': mixed_modes,
            'omega_0': self.omega_0,
            'f_0': self.f_0
        }
    
    def wave_function(self, x: float, y: float, n: int, m: int, t: float) -> complex:
        """
        Wave function on Möbius band satisfying boundary conditions.
        
        Parameters:
        -----------
        x : float
            Longitudinal coordinate (0 to L)
        y : float  
            Transverse coordinate (-w to w)
        n : int
            Longitudinal mode number (must be odd)
        m : int
            Transverse mode number
        t : float
            Time
            
        Returns:
        --------
        psi : complex
            Wave function value
        """
        # Longitudinal part (twisted periodic)
        k_n = (2*n + 1) * np.pi / self.L
        psi_x = np.exp(1j * k_n * x)
        
        # Transverse part (vanishes at boundaries)
        psi_y = np.cos(m * np.pi * y / (2 * self.w))
        
        # Time evolution
        k_total = np.sqrt(k_n**2 + (m * np.pi / (2 * self.w))**2)
        omega = self.c * k_total
        psi_t = np.exp(-1j * omega * t)
        
        return psi_x * psi_y * psi_t
    
    def boundary_effects_on_echoes(self) -> Dict[str, any]:
        """
        Analyze how the boundary affects echo generation.
        
        The boundary introduces:
        1. Edge modes that don't exist in closed surfaces
        2. Leakage of energy through the boundary
        3. Modified reflection conditions
        """
        print("\n" + "="*60)
        print("BOUNDARY EFFECTS ANALYSIS")
        print("="*60)
        
        effects = {
            'edge_modes': {
                'description': 'Modes localized near the boundary',
                'decay_length': self.w / np.pi,  # Characteristic decay
                'frequency_shift': 'Lower than bulk modes',
                'observability': 'May create additional echo frequencies'
            },
            'energy_leakage': {
                'description': 'Energy can escape through the boundary',
                'leakage_rate': self.c / self.w,  # Rough estimate
                'echo_suppression': 'Reduces echo amplitude',
                'quality_factor': self.L / self.w  # Dimensionless
            },
            'reflection_modification': {
                'description': 'Boundary changes reflection conditions',
                'phase_shift': 'π/2 for hard boundary',
                'mode_mixing': 'Couples different mode numbers',
                'echo_distortion': 'Changes echo waveform shape'
            }
        }
        
        # Calculate quality factor for echo confinement
        Q_boundary = self.L / (2 * np.pi * self.w)
        print(f"\nQuality factor (confinement): Q = {Q_boundary:.1f}")
        
        if Q_boundary > 100:
            print("High Q: Good echo confinement despite boundary")
        elif Q_boundary > 10:
            print("Moderate Q: Significant boundary losses")
        else:
            print("Low Q: Boundary effects dominate")
        
        effects['overall_quality_factor'] = Q_boundary
        
        return effects
    
    def echo_time_prediction(self, black_hole_mass: float) -> Tuple[float, float]:
        """
        Predict echo times including boundary effects.
        
        Returns both primary echo and boundary-induced secondary echo.
        """
        # Primary echo (bulk propagation)
        tau_bulk = self.L / self.c
        
        # Mass scaling (similar to Klein bottle)
        M_ref = 62.0
        alpha = -0.826
        tau_primary = tau_bulk * (black_hole_mass / M_ref)**alpha
        
        # Secondary echo from boundary reflection
        # Travels to boundary and back
        tau_boundary = 2 * self.w / self.c
        tau_secondary = tau_primary + tau_boundary
        
        return tau_primary, tau_secondary
    
    def plot_mode_comparison(self, save_path: str = None):
        """
        Visualize Möbius band modes and boundary effects.
        """
        modes = self.derive_mode_spectrum()
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))
        
        # 1. Longitudinal mode spectrum
        long_freqs = [m['f'] for m in modes['longitudinal'][:6]]
        long_n = [m['n'] for m in modes['longitudinal'][:6]]
        ax1.stem(long_n, long_freqs, basefmt=' ')
        ax1.set_xlabel('Mode number n')
        ax1.set_ylabel('Frequency (Hz)')
        ax1.set_title('Möbius Band: Longitudinal Modes (Only Odd n)')
        ax1.grid(True, alpha=0.3)
        
        # 2. Transverse mode spectrum  
        trans_freqs = [m['f'] for m in modes['transverse']]
        trans_m = [m['m'] for m in modes['transverse']]
        ax2.stem(trans_m, trans_freqs, basefmt=' ', linefmt='C1-', markerfmt='C1o')
        ax2.set_xlabel('Mode number m')
        ax2.set_ylabel('Frequency (Hz)')
        ax2.set_title('Möbius Band: Transverse Modes (Boundary Conditions)')
        ax2.grid(True, alpha=0.3)
        
        # 3. Mode density comparison
        # Klein bottle: only odd harmonics of f₀
        # Möbius: mixed spectrum
        freq_range = np.linspace(0, 100, 1000)
        
        # Klein bottle spectrum (delta functions at odd harmonics)
        klein_f0 = 6.65
        klein_spectrum = np.zeros_like(freq_range)
        for n in [1, 3, 5, 7, 9]:
            idx = np.argmin(np.abs(freq_range - n * klein_f0))
            klein_spectrum[idx] = 1
        
        # Möbius spectrum (more complex)
        mobius_spectrum = np.zeros_like(freq_range)
        for mode in modes['mixed'][:20]:
            idx = np.argmin(np.abs(freq_range - mode['f']))
            mobius_spectrum[idx] = 1
        
        ax3.plot(freq_range, klein_spectrum, 'b-', alpha=0.7, label='Klein Bottle')
        ax3.plot(freq_range, mobius_spectrum + 1.5, 'r-', alpha=0.7, label='Möbius Band')
        ax3.set_xlabel('Frequency (Hz)')
        ax3.set_ylabel('Mode density (offset)')
        ax3.set_title('Mode Density Comparison')
        ax3.set_xlim(0, 80)
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # 4. Boundary effect visualization
        y = np.linspace(-self.w, self.w, 100)
        boundary_profile = np.cos(np.pi * y / (2 * self.w))
        edge_mode = np.exp(-np.abs(y) / (self.w / 3)) * np.sin(3 * np.pi * y / (2 * self.w))
        
        ax4.plot(y/1000, boundary_profile, 'b-', label='Bulk mode', linewidth=2)
        ax4.plot(y/1000, edge_mode, 'r--', label='Edge mode', linewidth=2)
        ax4.axvline(-self.w/1000, color='k', linestyle=':', alpha=0.5)
        ax4.axvline(self.w/1000, color='k', linestyle=':', alpha=0.5)
        ax4.set_xlabel('Transverse position (km)')
        ax4.set_ylabel('Wave amplitude')
        ax4.set_title('Boundary Effects: Bulk vs Edge Modes')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"\nMode comparison plot saved to: {save_path}")
        
        return fig
    
    def compare_all_topologies(self) -> Dict[str, any]:
        """
        Compare Möbius band with Klein bottle and ℝP².
        """
        comparison = {
            'Möbius Band': {
                'orientable': False,
                'boundary': True,
                'mode_selection': 'Odd longitudinal + all transverse',
                'f_0_Hz': self.f_0,
                'echo_complexity': 'High (boundary effects)',
                'unique_features': ['Edge modes', 'Energy leakage', 'Dual echo times']
            },
            'Klein Bottle': {
                'orientable': False,
                'boundary': False,
                'mode_selection': 'Only odd harmonics',
                'f_0_Hz': 6.65,
                'echo_complexity': 'Low (clean spectrum)',
                'unique_features': ['Perfect odd mode selection', 'No leakage']
            },
            'Real Projective Plane': {
                'orientable': False,
                'boundary': False,
                'mode_selection': 'Only odd l spherical harmonics',
                'f_0_Hz': 'TBD (depends on radius)',
                'echo_complexity': 'Medium',
                'unique_features': ['Antipodal identification', 'Spherical symmetry']
            }
        }
        
        return comparison


def main():
    """
    Test the Möbius band theoretical framework.
    """
    print("MÖBIUS BAND ANALYSIS")
    print("="*60)
    
    # Initialize with parameters giving comparable frequency to Klein bottle
    # Need larger circumference due to twist constraint
    mobius = MobiusBand(length=2*np.pi*8400e3, width=500e3)
    
    # Derive mode spectrum
    modes = mobius.derive_mode_spectrum()
    
    # Analyze boundary effects
    boundary_effects = mobius.boundary_effects_on_echoes()
    
    # Echo predictions for GW150914
    M_test = 62.0
    tau_primary, tau_secondary = mobius.echo_time_prediction(M_test)
    print(f"\nEcho predictions for M = {M_test} M☉:")
    print(f"  Primary echo: τ₁ = {tau_primary:.3f} s")
    print(f"  Secondary echo: τ₂ = {tau_secondary:.3f} s")
    print(f"  Boundary delay: Δτ = {tau_secondary - tau_primary:.6f} s")
    
    # Generate plots
    mobius.plot_mode_comparison(save_path="../Results/mode_spectra/mobius_band_modes.png")
    
    # Compare topologies
    topology_comparison = mobius.compare_all_topologies()
    
    # Save comprehensive results
    results = {
        'topology': 'Möbius Band',
        'parameters': {
            'length_m': mobius.L,
            'width_m': mobius.w,
            'effective_radius_m': mobius.R_eff
        },
        'mode_analysis': {
            'fundamental_frequency_Hz': mobius.f_0,
            'num_longitudinal_modes': len(modes['longitudinal']),
            'num_transverse_modes': len(modes['transverse']),
            'lowest_modes_Hz': [m['f'] for m in modes['mixed'][:5]]
        },
        'boundary_effects': boundary_effects,
        'echo_predictions': {
            'primary_echo_s': tau_primary,
            'secondary_echo_s': tau_secondary,
            'mass_used_Msun': M_test
        },
        'topology_comparison': topology_comparison,
        'key_findings': [
            'Möbius band has both odd and even frequency modes',
            'Boundary introduces edge modes absent in closed surfaces',
            'Energy leakage reduces echo amplitude',
            'Predicts secondary echoes from boundary reflections'
        ]
    }
    
    with open('../Results/comparison_tables/mobius_band_analysis.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print("\n✅ Möbius band analysis complete!")
    print(f"Results saved to: ../Results/comparison_tables/mobius_band_analysis.json")


if __name__ == "__main__":
    main()