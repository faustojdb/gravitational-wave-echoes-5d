#!/usr/bin/env python3
"""
Klein Quantum Simulator
Quantum Klein Field Theory Implementation

Simulates atoms in Klein tension - existing simultaneously in two 4D locations
connected by Klein bottle topology with dynamic electron redistribution.

Author: Klein Field Theory Research Group
Date: July 23, 2025
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import eigh, expm
from scipy.integrate import solve_ivp
import json
from dataclasses import dataclass
from typing import Tuple, List, Dict, Optional

@dataclass
class KleinParameters:
    """Klein Field Theory parameters for quantum simulation."""
    alpha_klein: float = 1.0e-3  # Klein tension energy scale (eV)
    beta_klein: float = 0.5e-3   # Klein field coupling (eV)
    r_klein: float = 8.4e6       # Klein radius (m)
    f0_klein: float = 5.68       # Klein universal frequency (Hz)
    epsilon_max: float = 0.65    # Klein field maximum amplitude
    
class KleinQuantumSimulator:
    """
    Simulator for quantum systems in Klein tension.
    
    Models atoms existing simultaneously in two 4D positions connected
    by Klein bottle topology, with dynamic electron redistribution.
    """
    
    def __init__(self, params: KleinParameters = None):
        """Initialize Klein quantum simulator."""
        self.params = params or KleinParameters()
        self.hbar = 1.054571817e-34  # Reduced Planck constant
        self.e_charge = 1.602176634e-19  # Elementary charge
        self.m_electron = 9.1093837015e-31  # Electron mass
        
    def klein_hilbert_space_basis(self, n_levels: int = 10) -> Dict:
        """
        Generate Klein Hilbert space basis states.
        
        Args:
            n_levels: Number of energy levels to include
            
        Returns:
            Dictionary of basis states and Klein operators
        """
        # Standard hydrogen-like basis at each Klein position
        basis_1 = {}  # Basis states at position 1
        basis_2 = {}  # Basis states at position 2
        klein_connection = {}  # Klein bottle connection states
        
        # Generate quantum numbers (n, l, m) for each position
        for n in range(1, n_levels + 1):
            for l in range(n):
                for m in range(-l, l + 1):
                    state_key = f"n{n}l{l}m{m}"
                    basis_1[state_key] = (n, l, m)
                    basis_2[state_key] = (n, l, m)
        
        # Klein connection states with topological constraint
        # (φ, χ) ∼ (φ + π, -χ) identification
        n_phi = 32  # Number of φ grid points
        n_chi = 32  # Number of χ grid points
        
        phi_vals = np.linspace(0, 2*np.pi, n_phi, endpoint=False)
        chi_vals = np.linspace(-np.pi, np.pi, n_chi, endpoint=False)
        
        for i, phi in enumerate(phi_vals):
            for j, chi in enumerate(chi_vals):
                # Apply Klein bottle identification
                phi_id = (phi + np.pi) % (2*np.pi)
                chi_id = -chi
                klein_connection[(i, j)] = {
                    'phi': phi, 'chi': chi,
                    'phi_identified': phi_id, 'chi_identified': chi_id
                }
        
        return {
            'basis_1': basis_1,
            'basis_2': basis_2, 
            'klein_connection': klein_connection,
            'n_states_per_position': len(basis_1),
            'n_connection_states': len(klein_connection)
        }
    
    def klein_tension_hamiltonian(self, basis: Dict) -> np.ndarray:
        """
        Construct Klein tension Hamiltonian matrix.
        
        H_Klein = H_1 ⊗ I_2 ⊗ I_conn + I_1 ⊗ H_2 ⊗ I_conn + V_Klein_tension
        
        Args:
            basis: Klein Hilbert space basis
            
        Returns:
            Klein Hamiltonian matrix
        """
        n1 = basis['n_states_per_position']
        n2 = basis['n_states_per_position'] 
        n_conn = basis['n_connection_states']
        
        total_dim = n1 * n2 * n_conn
        H_klein = np.zeros((total_dim, total_dim), dtype=complex)
        
        # Standard hydrogen Hamiltonian at each position
        H_hydrogen = self._hydrogen_hamiltonian(basis['basis_1'])
        
        # H_1 ⊗ I_2 ⊗ I_conn term
        for i in range(n1):
            for j in range(n1):
                for k in range(n2):
                    for l in range(n_conn):
                        idx1 = i * n2 * n_conn + k * n_conn + l
                        idx2 = j * n2 * n_conn + k * n_conn + l
                        H_klein[idx1, idx2] += H_hydrogen[i, j]
        
        # I_1 ⊗ H_2 ⊗ I_conn term  
        for i in range(n1):
            for j in range(n2):
                for k in range(n2):
                    for l in range(n_conn):
                        idx1 = i * n2 * n_conn + j * n_conn + l
                        idx2 = i * n2 * n_conn + k * n_conn + l
                        H_klein[idx1, idx2] += H_hydrogen[j, k]
        
        # Klein tension potential V_Klein_tension
        V_tension = self._klein_tension_potential(basis)
        H_klein += V_tension
        
        return H_klein
    
    def _hydrogen_hamiltonian(self, basis_states: Dict) -> np.ndarray:
        """Generate hydrogen-like Hamiltonian matrix."""
        n_states = len(basis_states)
        H = np.zeros((n_states, n_states), dtype=complex)
        
        # Diagonal elements: hydrogen energy levels
        for i, (state_key, (n, l, m)) in enumerate(basis_states.items()):
            # Hydrogen energy: E_n = -13.6 eV / n²
            H[i, i] = -13.6 / (n * n)
        
        return H
    
    def _klein_tension_potential(self, basis: Dict) -> np.ndarray:
        """
        Calculate Klein tension potential matrix.
        
        V_Klein = α_Klein(N̂₁ - N̂₂)² + β_Klein φ̂₅²
        """
        n1 = basis['n_states_per_position']
        n2 = basis['n_states_per_position']
        n_conn = basis['n_connection_states']
        total_dim = n1 * n2 * n_conn
        
        V_tension = np.zeros((total_dim, total_dim), dtype=complex)
        
        # Electron number difference term: α_Klein(N̂₁ - N̂₂)²
        for i in range(total_dim):
            for j in range(total_dim):
                # Extract quantum numbers
                i1, i2, i_conn = self._decompose_index(i, n1, n2, n_conn)
                j1, j2, j_conn = self._decompose_index(j, n1, n2, n_conn)
                
                if i_conn == j_conn:  # Klein connection state unchanged
                    # Calculate electron number difference contribution
                    delta_N = self._electron_number_difference(i1, i2, j1, j2, basis)
                    V_tension[i, j] += self.params.alpha_klein * delta_N
        
        # Klein field energy term: β_Klein φ̂₅²
        klein_field_energy = self._klein_field_energy_matrix(basis)
        V_tension += self.params.beta_klein * klein_field_energy
        
        return V_tension
    
    def _decompose_index(self, idx: int, n1: int, n2: int, n_conn: int) -> Tuple[int, int, int]:
        """Decompose flat index into (i1, i2, i_conn) components."""
        i_conn = idx % n_conn
        remaining = idx // n_conn
        i2 = remaining % n2
        i1 = remaining // n2
        return i1, i2, i_conn
    
    def _electron_number_difference(self, i1: int, i2: int, j1: int, j2: int, basis: Dict) -> float:
        """Calculate matrix element of (N̂₁ - N̂₂)² operator."""
        if i1 == j1 and i2 == j2:
            # Diagonal element: assume single electron in each state
            N1 = 1 if i1 == j1 else 0
            N2 = 1 if i2 == j2 else 0
            return (N1 - N2) ** 2
        else:
            # Off-diagonal electron transfer terms
            return 0.1 * np.exp(-abs(i1-j1) - abs(i2-j2))  # Approximate coupling
    
    def _klein_field_energy_matrix(self, basis: Dict) -> np.ndarray:
        """Calculate Klein field energy matrix φ̂₅²."""
        n1 = basis['n_states_per_position']
        n2 = basis['n_states_per_position']
        n_conn = basis['n_connection_states']
        total_dim = n1 * n2 * n_conn
        
        phi_energy = np.zeros((total_dim, total_dim), dtype=complex)
        
        # Klein field oscillates at universal frequency f₀
        omega_klein = 2 * np.pi * self.params.f0_klein
        
        for i in range(total_dim):
            for j in range(total_dim):
                i1, i2, i_conn = self._decompose_index(i, n1, n2, n_conn)
                j1, j2, j_conn = self._decompose_index(j, n1, n2, n_conn)
                
                if i1 == j1 and i2 == j2:  # Same atomic states
                    # Klein field energy depends on connection state
                    phi_i = list(basis['klein_connection'].values())[i_conn]['phi']
                    phi_j = list(basis['klein_connection'].values())[j_conn]['phi']
                    
                    # φ̂₅² matrix element
                    if i_conn == j_conn:
                        phi_energy[i, j] = phi_i ** 2
                    else:
                        # Off-diagonal Klein field coupling
                        phi_energy[i, j] = 0.1 * np.cos(phi_i - phi_j)
        
        return phi_energy
    
    def simulate_klein_spectroscopy(self, n_levels: int = 5) -> Dict:
        """
        Simulate atomic spectroscopy with Klein tension effects.
        
        Args:
            n_levels: Number of atomic energy levels to include
            
        Returns:
            Dictionary with energy levels and transition predictions
        """
        print("🔬 Simulating Klein atomic spectroscopy...")
        
        # Generate Klein Hilbert space
        basis = self.klein_hilbert_space_basis(n_levels)
        print(f"   Klein Hilbert space dimension: {basis['n_states_per_position']**2 * basis['n_connection_states']}")
        
        # Construct Klein Hamiltonian (use reduced dimensionality for demo)
        n_demo = min(3, n_levels)  # Limit size for computational feasibility
        basis_demo = self.klein_hilbert_space_basis(n_demo)
        
        print("   Building Klein tension Hamiltonian...")
        H_klein = self.klein_tension_hamiltonian(basis_demo)
        
        # Diagonalize to find Klein energy levels
        print("   Diagonalizing Klein Hamiltonian...")
        eigenvalues, eigenvectors = eigh(H_klein)
        
        # Analyze Klein splitting patterns
        results = self._analyze_klein_splitting(eigenvalues, eigenvectors, basis_demo)
        
        return results
    
    def _analyze_klein_splitting(self, eigenvalues: np.ndarray, 
                                eigenvectors: np.ndarray, basis: Dict) -> Dict:
        """Analyze Klein splitting patterns in energy spectrum."""
        
        # Sort eigenvalues and group by approximate hydrogen levels
        sorted_idx = np.argsort(eigenvalues)
        sorted_energies = eigenvalues[sorted_idx]
        
        # Expected hydrogen levels (without Klein effects)
        hydrogen_levels = [-13.6 / (n*n) for n in range(1, 4)]  # 1s, 2s, 2p
        
        klein_analysis = {
            'klein_parameters': {
                'alpha_klein_eV': self.params.alpha_klein,
                'beta_klein_eV': self.params.beta_klein,
                'f0_klein_Hz': self.params.f0_klein
            },
            'energy_levels': {
                'hydrogen_reference': hydrogen_levels,
                'klein_modified': sorted_energies.tolist(),
                'klein_splitting': []
            },
            'spectroscopic_predictions': {},
            'transition_matrix': {}
        }
        
        # Identify Klein doublets
        for i, h_energy in enumerate(hydrogen_levels):
            # Find Klein states near this hydrogen level
            klein_states = []
            for j, e_energy in enumerate(sorted_energies):
                if abs(e_energy - h_energy) < 0.1:  # Within 0.1 eV
                    klein_states.append({
                        'energy': e_energy,
                        'index': j,
                        'splitting_from_hydrogen': e_energy - h_energy
                    })
            
            if len(klein_states) > 1:
                # Calculate Klein splitting
                energies = [state['energy'] for state in klein_states]
                klein_splitting = max(energies) - min(energies)
                
                klein_analysis['energy_levels']['klein_splitting'].append({
                    'hydrogen_level': f"n={i+1}",
                    'hydrogen_energy': h_energy,
                    'klein_states': klein_states,
                    'klein_splitting_eV': klein_splitting,
                    'klein_splitting_meV': klein_splitting * 1000,
                    'klein_splitting_GHz': klein_splitting / (4.136e-15)  # eV to GHz
                })
        
        # Predict spectroscopic transitions
        klein_analysis['spectroscopic_predictions'] = self._predict_transitions(
            sorted_energies, hydrogen_levels
        )
        
        return klein_analysis
    
    def _predict_transitions(self, klein_energies: np.ndarray, 
                           hydrogen_levels: List[float]) -> Dict:
        """Predict spectroscopic transitions with Klein effects."""
        
        transitions = {}
        
        # Find Klein states corresponding to n=1 (ground state)
        ground_states = []
        for i, energy in enumerate(klein_energies):
            if abs(energy - hydrogen_levels[0]) < 0.05:  # Within 50 meV of 1s
                ground_states.append({'energy': energy, 'index': i})
        
        # Find Klein states corresponding to n=2 (first excited)
        excited_states = []
        for i, energy in enumerate(klein_energies):
            if len(hydrogen_levels) > 1 and abs(energy - hydrogen_levels[1]) < 0.05:
                excited_states.append({'energy': energy, 'index': i})
        
        # Calculate Lyman-α analog transitions (n=2 → n=1)
        if ground_states and excited_states:
            lyman_transitions = []
            for excited in excited_states:
                for ground in ground_states:
                    transition_energy = excited['energy'] - ground['energy']
                    wavelength = self.hbar * 3e8 / (transition_energy * self.e_charge) * 1e9  # nm
                    
                    lyman_transitions.append({
                        'initial_state': excited['index'],
                        'final_state': ground['index'],
                        'transition_energy_eV': transition_energy,
                        'wavelength_nm': wavelength,
                        'frequency_Hz': abs(transition_energy) * self.e_charge / self.hbar
                    })
            
            transitions['lyman_alpha_klein'] = {
                'classical_lyman_alpha': {
                    'energy_eV': hydrogen_levels[1] - hydrogen_levels[0],
                    'wavelength_nm': 121.6
                },
                'klein_transitions': lyman_transitions,
                'number_of_lines': len(lyman_transitions),
                'predicted_pattern': 'Klein doublet to doublet → quartet pattern'
            }
        
        return transitions
    
    def simulate_klein_dynamics(self, duration: float = 1e-12, dt: float = 1e-15) -> Dict:
        """
        Simulate time evolution of Klein quantum system.
        
        Args:
            duration: Simulation time (seconds)
            dt: Time step (seconds)
            
        Returns:
            Time evolution results
        """
        print("⏱️  Simulating Klein quantum dynamics...")
        
        # Simple 2-level Klein system for demonstration
        # Ground state Klein doublet
        H_klein_simple = np.array([
            [-13.6, self.params.alpha_klein],
            [self.params.alpha_klein, -13.6 + 2*self.params.alpha_klein]
        ], dtype=complex)
        
        # Initial state: Klein superposition
        psi_0 = np.array([1/np.sqrt(2), 1/np.sqrt(2)], dtype=complex)
        
        # Time evolution
        times = np.arange(0, duration, dt)
        n_steps = len(times)
        
        # Evolve state
        psi_evolution = np.zeros((n_steps, 2), dtype=complex)
        psi_evolution[0] = psi_0
        
        for i in range(1, n_steps):
            # Time evolution operator: U = exp(-iHt/ℏ)
            U = expm(-1j * H_klein_simple * dt / self.hbar)
            psi_evolution[i] = U @ psi_evolution[i-1]
        
        # Calculate observables
        electron_position_1 = np.abs(psi_evolution[:, 0])**2
        electron_position_2 = np.abs(psi_evolution[:, 1])**2
        klein_coherence = np.real(psi_evolution[:, 0] * np.conj(psi_evolution[:, 1]))
        
        # Klein breathing frequency
        klein_frequency = self.params.alpha_klein / self.hbar  # rad/s
        
        dynamics_results = {
            'simulation_parameters': {
                'duration_s': duration,
                'time_step_s': dt,
                'klein_frequency_Hz': klein_frequency / (2*np.pi)
            },
            'time_evolution': {
                'times': times.tolist(),
                'electron_position_1': electron_position_1.tolist(),
                'electron_position_2': electron_position_2.tolist(),
                'klein_coherence': klein_coherence.tolist()
            },
            'observables': {
                'klein_oscillation_period': 2*np.pi / klein_frequency,
                'electron_redistribution_amplitude': np.max(electron_position_1) - np.min(electron_position_1),
                'coherence_lifetime': self._estimate_coherence_time(klein_coherence)
            }
        }
        
        return dynamics_results
    
    def _estimate_coherence_time(self, coherence: np.ndarray) -> float:
        """Estimate Klein coherence time from coherence function."""
        # Find 1/e decay time
        max_coherence = np.max(np.abs(coherence))
        threshold = max_coherence / np.e
        
        decay_idx = np.where(np.abs(coherence) < threshold)[0]
        if len(decay_idx) > 0:
            return decay_idx[0] * 1e-15  # Convert to seconds
        else:
            return np.inf  # No decay observed
    
    def visualize_results(self, spectroscopy_results: Dict, dynamics_results: Dict = None):
        """Create visualizations of Klein quantum simulation results."""
        
        fig = plt.figure(figsize=(15, 10))
        
        # Plot 1: Klein energy level splitting
        ax1 = plt.subplot(2, 3, 1)
        if 'klein_splitting' in spectroscopy_results['energy_levels']:
            for splitting_data in spectroscopy_results['energy_levels']['klein_splitting']:
                h_energy = splitting_data['hydrogen_energy']
                klein_states = splitting_data['klein_states']
                
                # Plot hydrogen reference level
                ax1.axhline(h_energy, color='red', linestyle='--', alpha=0.5, 
                           label=f"H {splitting_data['hydrogen_level']}")
                
                # Plot Klein split levels
                for state in klein_states:
                    ax1.axhline(state['energy'], color='blue', linewidth=2)
                    
        ax1.set_ylabel('Energy (eV)')
        ax1.set_title('Klein Energy Level Splitting')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Klein splitting magnitude
        ax2 = plt.subplot(2, 3, 2)
        if 'klein_splitting' in spectroscopy_results['energy_levels']:
            levels = []
            splittings_meV = []
            
            for splitting_data in spectroscopy_results['energy_levels']['klein_splitting']:
                levels.append(splitting_data['hydrogen_level'])
                splittings_meV.append(splitting_data['klein_splitting_meV'])
            
            bars = ax2.bar(levels, splittings_meV, color='purple', alpha=0.7)
            ax2.set_ylabel('Klein Splitting (meV)')
            ax2.set_title('Klein Splitting vs Atomic Level')
            ax2.grid(True, alpha=0.3)
            
            # Add value labels on bars
            for bar, value in zip(bars, splittings_meV):
                ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                        f'{value:.3f}', ha='center', va='bottom')
        
        # Plot 3: Predicted spectrum (Lyman-α region)
        ax3 = plt.subplot(2, 3, 3)
        if 'lyman_alpha_klein' in spectroscopy_results['spectroscopic_predictions']:
            lyman_data = spectroscopy_results['spectroscopic_predictions']['lyman_alpha_klein']
            
            # Classical Lyman-α
            classical_wl = lyman_data['classical_lyman_alpha']['wavelength_nm']
            ax3.axvline(classical_wl, color='red', linestyle='--', linewidth=2,
                       label='Classical Lyman-α')
            
            # Klein transitions
            for i, transition in enumerate(lyman_data['klein_transitions']):
                wl = transition['wavelength_nm']
                ax3.axvline(wl, color='blue', linewidth=1, alpha=0.8)
            
            ax3.set_xlabel('Wavelength (nm)')
            ax3.set_ylabel('Intensity (arbitrary)')
            ax3.set_title('Klein Lyman-α Spectrum Prediction')
            ax3.legend()
            ax3.grid(True, alpha=0.3)
            ax3.set_xlim(121.0, 122.0)
        
        # Dynamic plots if dynamics simulation was run
        if dynamics_results:
            # Plot 4: Electron redistribution
            ax4 = plt.subplot(2, 3, 4)
            times_fs = np.array(dynamics_results['time_evolution']['times']) * 1e15  # Convert to fs
            pos1 = dynamics_results['time_evolution']['electron_position_1']
            pos2 = dynamics_results['time_evolution']['electron_position_2']
            
            ax4.plot(times_fs, pos1, 'b-', label='Position 1', linewidth=2)
            ax4.plot(times_fs, pos2, 'r-', label='Position 2', linewidth=2)
            ax4.set_xlabel('Time (fs)')
            ax4.set_ylabel('Electron Probability')
            ax4.set_title('Klein Electron Redistribution')
            ax4.legend()
            ax4.grid(True, alpha=0.3)
            
            # Plot 5: Klein coherence
            ax5 = plt.subplot(2, 3, 5)
            coherence = dynamics_results['time_evolution']['klein_coherence']
            ax5.plot(times_fs, coherence, 'g-', linewidth=2)
            ax5.set_xlabel('Time (fs)')
            ax5.set_ylabel('Klein Coherence')
            ax5.set_title('Klein Quantum Coherence')
            ax5.grid(True, alpha=0.3)
            
            # Plot 6: Klein breathing mode
            ax6 = plt.subplot(2, 3, 6)
            klein_freq_THz = dynamics_results['simulation_parameters']['klein_frequency_Hz'] * 1e-12
            theoretical_period = 1 / (klein_freq_THz * 1e12) * 1e15  # fs
            
            ax6.text(0.1, 0.8, f"Klein Frequency: {klein_freq_THz:.3f} THz", 
                    transform=ax6.transAxes, fontsize=12)
            ax6.text(0.1, 0.7, f"Klein Period: {theoretical_period:.3f} fs", 
                    transform=ax6.transAxes, fontsize=12)
            ax6.text(0.1, 0.6, f"Klein Energy: {self.params.alpha_klein*1000:.3f} meV", 
                    transform=ax6.transAxes, fontsize=12)
            
            # Show theoretical Klein oscillation
            t_theory = np.linspace(0, max(times_fs), 1000)
            klein_oscillation = np.cos(2*np.pi * klein_freq_THz * 1e12 * t_theory * 1e-15)
            ax6.plot(t_theory, klein_oscillation, 'purple', linewidth=2, 
                    label='Klein Breathing Mode')
            ax6.set_xlabel('Time (fs)')  
            ax6.set_ylabel('Klein Field Amplitude')
            ax6.set_title('Klein Breathing Mode')
            ax6.legend()
            ax6.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('klein_quantum_simulation.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        return fig
    
    def export_results(self, spectroscopy_results: Dict, dynamics_results: Dict = None, 
                      filename: str = 'klein_quantum_results.json'):
        """Export simulation results to JSON file."""
        
        export_data = {
            'simulation_metadata': {
                'simulator': 'Klein Quantum Simulator',
                'version': '1.0.0',
                'date': '2025-07-23',
                'klein_parameters': {
                    'alpha_klein_eV': self.params.alpha_klein,
                    'beta_klein_eV': self.params.beta_klein,
                    'r_klein_m': self.params.r_klein,
                    'f0_klein_Hz': self.params.f0_klein,
                    'epsilon_max': self.params.epsilon_max
                }
            },
            'spectroscopy_results': spectroscopy_results
        }
        
        if dynamics_results:
            export_data['dynamics_results'] = dynamics_results
        
        with open(filename, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        print(f"✅ Results exported to {filename}")
        return filename

def main():
    """Main simulation and demonstration."""
    print("🌌 Klein Quantum Field Theory Simulator")
    print("=" * 50)
    
    # Initialize simulator with default Klein parameters
    simulator = KleinQuantumSimulator()
    
    # Run spectroscopy simulation
    print("\n1. Running Klein Spectroscopy Simulation...")
    spectroscopy_results = simulator.simulate_klein_spectroscopy(n_levels=3)
    
    # Display key results
    print("\n📊 Key Spectroscopy Results:")
    if 'klein_splitting' in spectroscopy_results['energy_levels']:
        for splitting in spectroscopy_results['energy_levels']['klein_splitting']:
            print(f"   {splitting['hydrogen_level']}: {splitting['klein_splitting_meV']:.3f} meV splitting")
    
    # Run dynamics simulation  
    print("\n2. Running Klein Dynamics Simulation...")
    dynamics_results = simulator.simulate_klein_dynamics(duration=1e-12, dt=1e-15)
    
    print(f"\n⏱️  Dynamics Results:")
    print(f"   Klein oscillation frequency: {dynamics_results['simulation_parameters']['klein_frequency_Hz']:.3e} Hz")
    print(f"   Electron redistribution: {dynamics_results['observables']['electron_redistribution_amplitude']:.3f}")
    
    # Create visualizations
    print("\n3. Creating Visualizations...")
    fig = simulator.visualize_results(spectroscopy_results, dynamics_results)
    
    # Export results
    print("\n4. Exporting Results...")
    simulator.export_results(spectroscopy_results, dynamics_results)
    
    print("\n✅ Klein Quantum Simulation Complete!")
    print("\nThis simulation demonstrates:")
    print("  • Klein tension energy level splitting")
    print("  • Quantum Klein spectroscopic predictions") 
    print("  • Klein electron redistribution dynamics")
    print("  • Klein quantum coherence evolution")
    
    return spectroscopy_results, dynamics_results

if __name__ == "__main__":
    results = main()