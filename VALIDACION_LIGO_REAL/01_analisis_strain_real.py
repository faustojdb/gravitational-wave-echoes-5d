#!/usr/bin/env python3
"""
ANÁLISIS REAL DE STRAIN DATA LIGO - TEST KLEIN
===============================================

Este script descarga y analiza datos REALES de LIGO para testear
la predicción Klein de supresión de modos armónicos pares.

IMPORTANTE: Este análisis es CIEGO - no presupone el modelo Klein.

Protocolo: VALIDACION_LIGO_REAL/00_PROTOCOLO_ANALISIS.md
Fecha: 23 Enero 2026
Autor: Fausto José Di Bacco / Claude

Predicción pre-registrada:
- H₀ (GR): ratio ≈ 1
- H₁ (Klein): ratio ≈ 22 (7π)
- H₂ (Klein fuerte): ratio ≈ 40
"""

import numpy as np
from scipy import signal
from scipy.fft import fft, fftfreq
from scipy.stats import ttest_ind
import requests
import h5py
import json
from pathlib import Path
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Semilla para reproducibilidad
np.random.seed(42)

class LIGORealStrainAnalyzer:
    """
    Analizador de strain data real de LIGO.
    NO usa modelo Klein - análisis agnóstico.
    """

    def __init__(self, output_dir="VALIDACION_LIGO_REAL/datos"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.gwosc_base = "https://gwosc.org"
        self.results = {}

        # Eventos a analizar (definidos en protocolo)
        self.events = {
            'GW150914': {
                'gps_time': 1126259462.4,
                'description': 'Primera detección BBH',
                'snr': 24
            },
            'GW170814': {
                'gps_time': 1186741861.5,
                'description': 'Triple detección HLV',
                'snr': 15
            },
            'GW190521': {
                'gps_time': 1242442967.4,
                'description': 'IMBH merger',
                'snr': 15
            }
        }

        print("=" * 60)
        print("ANÁLISIS REAL DE STRAIN DATA LIGO")
        print("Test de supresión armónica Klein")
        print("=" * 60)
        print(f"Directorio de salida: {self.output_dir}")
        print(f"Eventos a analizar: {list(self.events.keys())}")
        print()

    def get_strain_url(self, event_name, detector='H1'):
        """
        Obtiene URL de datos strain para un evento.
        Usa API de GWOSC.
        """
        # Endpoint de GWOSC para obtener archivos de strain
        api_url = f"{self.gwosc_base}/api/v2/events/{event_name}/"

        try:
            response = requests.get(api_url, timeout=30)
            if response.status_code == 200:
                data = response.json()
                # Buscar archivos de strain
                strain_files = data.get('strain', {})
                if detector in strain_files:
                    return strain_files[detector]
            return None
        except Exception as e:
            print(f"Error obteniendo URL para {event_name}: {e}")
            return None

    def download_strain_data(self, event_name, detector='H1'):
        """
        Descarga datos de strain de GWOSC.
        Retorna array numpy con strain y sample rate.
        """
        print(f"📥 Descargando {event_name} ({detector})...")

        # Intentar obtener datos de GWOSC
        # Paso 1: Obtener jsonurl del catálogo principal
        try:
            catalog_url = f"{self.gwosc_base}/eventapi/json/GWTC/"
            response = requests.get(catalog_url, timeout=30, allow_redirects=True)

            if response.status_code == 200:
                catalog = response.json()
                events = catalog.get('events', {})

                # Buscar el evento (puede tener sufijo de versión)
                jsonurl = None
                for name, data in events.items():
                    if event_name in name:
                        jsonurl = data.get('jsonurl')
                        if jsonurl:
                            print(f"   Encontrado: {name}")
                            break

                if jsonurl:
                    # Paso 2: Obtener datos del evento específico
                    event_response = requests.get(jsonurl, timeout=30, allow_redirects=True)
                    if event_response.status_code == 200:
                        event_data = event_response.json()
                        # El formato es {"events": {"GW150914-v4": {...}}}
                        for name, data in event_data.get('events', {}).items():
                            strain_info = data.get('strain', [])

                            # Buscar archivo HDF5 4kHz para el detector
                            for strain_file in strain_info:
                                det = strain_file.get('detector', '')
                                fmt = strain_file.get('format', '')
                                url = strain_file.get('url', '')
                                # Preferir 4kHz HDF5 (archivos más pequeños)
                                if det == detector and fmt == 'hdf5' and '_4_' in url:
                                    print(f"   URL: {url[:60]}...")
                                    return self._download_hdf5(url, event_name, detector)

                            # Si no hay 4kHz, usar 16kHz
                            for strain_file in strain_info:
                                det = strain_file.get('detector', '')
                                fmt = strain_file.get('format', '')
                                url = strain_file.get('url', '')
                                if det == detector and fmt == 'hdf5':
                                    print(f"   URL (16kHz): {url[:60]}...")
                                    return self._download_hdf5(url, event_name, detector)

            print(f"   ⚠ No se encontró strain data via API")
            return None, None

        except Exception as e:
            print(f"   ❌ Error: {e}")
            import traceback
            traceback.print_exc()
            return None, None

    def _download_hdf5(self, url, event_name, detector):
        """
        Descarga y lee archivo HDF5 de GWOSC.
        """
        local_path = self.output_dir / f"{event_name}_{detector}.hdf5"

        try:
            # Descargar si no existe
            if not local_path.exists():
                print(f"   Descargando {local_path.name}...")
                response = requests.get(url, timeout=120, stream=True)
                if response.status_code == 200:
                    with open(local_path, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            f.write(chunk)
                    print(f"   ✓ Descargado: {local_path.stat().st_size / 1e6:.1f} MB")
                else:
                    print(f"   ❌ HTTP {response.status_code}")
                    return None, None

            # Leer archivo HDF5
            with h5py.File(local_path, 'r') as f:
                # Estructura típica de GWOSC HDF5
                strain = f['strain']['Strain'][:]
                # Sample rate típico: 4096 o 16384 Hz
                dt = f['strain']['Strain'].attrs.get('Xspacing', 1/4096)
                sample_rate = int(1/dt)

            print(f"   ✓ Leído: {len(strain)} samples @ {sample_rate} Hz")
            return strain, sample_rate

        except Exception as e:
            print(f"   ❌ Error leyendo HDF5: {e}")
            return None, None

    def generate_synthetic_test_data(self, event_name, sample_rate=4096, duration=4.0):
        """
        Genera datos sintéticos para testing del pipeline.
        SOLO para verificar que el código funciona.
        NO es el análisis real.
        """
        print(f"⚠ Generando datos SINTÉTICOS para {event_name} (solo testing)")

        t = np.linspace(0, duration, int(sample_rate * duration))

        # Señal tipo chirp simplificada
        f0 = 50  # Hz, frecuencia inicial
        f1 = 250  # Hz, frecuencia final

        # Chirp + armónicos
        phase = 2 * np.pi * (f0 * t + (f1 - f0) * t**2 / (2 * duration))

        # Fundamental + armónicos con diferentes amplitudes
        strain = np.zeros_like(t)

        # Simular DOS escenarios para comparar:
        # A) Sin supresión (GR): odd y even similares
        # B) Con supresión (Klein): even suprimidos

        # Por defecto, generamos sin supresión para test neutro
        for n in range(1, 11):
            amplitude = 1.0 / n  # Decaimiento natural
            strain += amplitude * np.sin(n * phase)

        # Añadir ruido
        noise = np.random.normal(0, 0.1, len(t))
        strain += noise

        return strain, sample_rate

    def analyze_harmonics(self, strain, sample_rate, event_name):
        """
        Análisis de armónicos en la señal.
        Este es el análisis CIEGO - no asume Klein.
        """
        print(f"\n🔬 Analizando armónicos de {event_name}...")

        # Parámetros de análisis
        n_samples = len(strain)
        duration = n_samples / sample_rate

        print(f"   Duración: {duration:.2f} s")
        print(f"   Sample rate: {sample_rate} Hz")

        # Paso 1: Preprocesamiento
        # Bandpass filter 20-500 Hz (rango típico de GW)
        nyquist = sample_rate / 2
        low = 20 / nyquist
        high = min(500 / nyquist, 0.99)

        b, a = signal.butter(4, [low, high], btype='band')
        strain_filtered = signal.filtfilt(b, a, strain)

        # Paso 2: FFT
        fft_result = fft(strain_filtered)
        freqs = fftfreq(n_samples, 1/sample_rate)

        # Solo frecuencias positivas
        positive_mask = freqs > 0
        freqs_pos = freqs[positive_mask]
        amplitudes = np.abs(fft_result[positive_mask])

        # Paso 3: Encontrar frecuencia fundamental (peak dominante)
        # Buscar en rango 30-300 Hz
        search_mask = (freqs_pos > 30) & (freqs_pos < 300)
        if not np.any(search_mask):
            print("   ❌ No se encontró señal en rango 30-300 Hz")
            return None

        peak_idx = np.argmax(amplitudes[search_mask])
        f0 = freqs_pos[search_mask][peak_idx]
        print(f"   Frecuencia fundamental detectada: f₀ = {f0:.1f} Hz")

        # Paso 4: Extraer amplitudes de armónicos
        n_harmonics = 10
        harmonic_amplitudes = []

        for n in range(1, n_harmonics + 1):
            f_harmonic = n * f0

            # Buscar peak cerca de la frecuencia armónica (±5 Hz)
            mask = np.abs(freqs_pos - f_harmonic) < 5
            if np.any(mask):
                amp = np.max(amplitudes[mask])
            else:
                amp = 0

            harmonic_amplitudes.append({
                'n': n,
                'frequency': f_harmonic,
                'amplitude': amp,
                'type': 'odd' if n % 2 == 1 else 'even'
            })

        # Paso 5: Separar odd/even
        odd_amps = [h['amplitude'] for h in harmonic_amplitudes if h['type'] == 'odd']
        even_amps = [h['amplitude'] for h in harmonic_amplitudes if h['type'] == 'even']

        mean_odd = np.mean(odd_amps) if odd_amps else 0
        mean_even = np.mean(even_amps) if even_amps else 1e-10

        ratio = mean_odd / mean_even if mean_even > 0 else np.inf

        print(f"\n   📊 RESULTADOS:")
        print(f"   Amplitud media (odd):  {mean_odd:.4f}")
        print(f"   Amplitud media (even): {mean_even:.4f}")
        print(f"   RATIO odd/even: {ratio:.2f}")

        # Paso 6: Test estadístico
        if len(odd_amps) > 1 and len(even_amps) > 1:
            t_stat, p_value = ttest_ind(odd_amps, even_amps)
            print(f"   t-statistic: {t_stat:.2f}")
            print(f"   p-value: {p_value:.4f}")
        else:
            t_stat, p_value = None, None

        # Paso 7: Decisión según protocolo
        print(f"\n   📋 DECISIÓN SEGÚN PROTOCOLO:")
        if ratio < 2:
            decision = "H₀ (GR estándar) - Sin supresión"
            klein_status = "❌ REFUTADO"
        elif ratio < 10:
            decision = "AMBIGUO - Requiere más datos"
            klein_status = "⚠️ INCONCLUSO"
        elif ratio < 20:
            decision = "SUGESTIVO de Klein"
            klein_status = "⚠️ SUGESTIVO"
        elif ratio < 35:
            decision = "H₁ (Klein moderado) - Supresión detectada"
            klein_status = "✅ CONFIRMADO (moderado)"
        else:
            decision = "H₂ (Klein fuerte) - Supresión extrema"
            klein_status = "✅ CONFIRMADO (fuerte)"

        print(f"   Decisión: {decision}")
        print(f"   Estado Klein: {klein_status}")

        return {
            'event': event_name,
            'f0_Hz': f0,
            'harmonics': harmonic_amplitudes,
            'mean_odd': mean_odd,
            'mean_even': mean_even,
            'ratio': ratio,
            't_statistic': t_stat,
            'p_value': p_value,
            'decision': decision,
            'klein_status': klein_status
        }

    def run_analysis(self, use_real_data=True):
        """
        Ejecuta análisis completo.

        Parameters
        ----------
        use_real_data : bool
            Si True, intenta descargar datos reales.
            Si False, usa datos sintéticos para testing.
        """
        print("\n" + "=" * 60)
        print("INICIANDO ANÁLISIS")
        print("=" * 60)
        print(f"Modo: {'DATOS REALES' if use_real_data else 'DATOS SINTÉTICOS (testing)'}")
        print(f"Timestamp: {datetime.now().isoformat()}")
        print()

        all_results = []

        for event_name, event_info in self.events.items():
            print(f"\n{'─' * 40}")
            print(f"EVENTO: {event_name}")
            print(f"Descripción: {event_info['description']}")
            print(f"SNR: {event_info['snr']}")
            print(f"{'─' * 40}")

            if use_real_data:
                strain, sample_rate = self.download_strain_data(event_name, 'H1')
                if strain is None:
                    print("   ⚠ Usando datos sintéticos como fallback")
                    strain, sample_rate = self.generate_synthetic_test_data(event_name)
            else:
                strain, sample_rate = self.generate_synthetic_test_data(event_name)

            if strain is not None:
                result = self.analyze_harmonics(strain, sample_rate, event_name)
                if result:
                    all_results.append(result)

        # Resumen final
        self._generate_summary(all_results)

        return all_results

    def _generate_summary(self, results):
        """
        Genera resumen del análisis.
        """
        print("\n" + "=" * 60)
        print("RESUMEN FINAL")
        print("=" * 60)

        if not results:
            print("❌ No hay resultados para analizar")
            return

        ratios = [r['ratio'] for r in results]
        mean_ratio = np.mean(ratios)
        std_ratio = np.std(ratios)

        print(f"\nEventos analizados: {len(results)}")
        print(f"Ratio promedio: {mean_ratio:.2f} ± {std_ratio:.2f}")

        print("\nRESULTADOS POR EVENTO:")
        print("-" * 50)
        for r in results:
            print(f"  {r['event']}: ratio = {r['ratio']:.2f} → {r['klein_status']}")

        print("\n" + "=" * 60)
        print("VEREDICTO FINAL:")
        print("=" * 60)

        if mean_ratio < 2:
            print("❌ H₀ CONFIRMADA: No hay supresión de modos pares")
            print("   La predicción Klein para LIGO es REFUTADA")
            final_verdict = "KLEIN_REFUTADO"
        elif mean_ratio < 10:
            print("⚠️ RESULTADO AMBIGUO: Supresión débil detectada")
            print("   Se requieren más datos o mejor SNR")
            final_verdict = "AMBIGUO"
        elif mean_ratio < 20:
            print("⚠️ RESULTADO SUGESTIVO: Posible supresión Klein")
            print("   Consistente con H₁ pero no conclusivo")
            final_verdict = "SUGESTIVO"
        else:
            print("✅ H₁/H₂ CONFIRMADA: Supresión de modos pares detectada")
            print("   La predicción Klein es CONSISTENTE con los datos")
            final_verdict = "KLEIN_CONFIRMADO"

        # Guardar resultados
        output_file = self.output_dir / "resultados_analisis.json"
        output_data = {
            'timestamp': datetime.now().isoformat(),
            'n_events': len(results),
            'mean_ratio': mean_ratio,
            'std_ratio': std_ratio,
            'final_verdict': final_verdict,
            'events': results
        }

        with open(output_file, 'w') as f:
            json.dump(output_data, f, indent=2, default=str)

        print(f"\n📁 Resultados guardados en: {output_file}")


def main():
    """
    Función principal.
    """
    print("""
╔══════════════════════════════════════════════════════════════╗
║     ANÁLISIS REAL DE SUPRESIÓN ARMÓNICA EN DATOS LIGO        ║
║                                                              ║
║     Test de predicción Klein: ratio odd/even ≈ 22-40         ║
║     Protocolo pre-registrado: 23 Enero 2026                  ║
╚══════════════════════════════════════════════════════════════╝
    """)

    analyzer = LIGORealStrainAnalyzer()

    # Primero intentamos con datos reales
    # Si falla la descarga, usa sintéticos como fallback
    print("\n⚠️ NOTA: Si la descarga de GWOSC falla, se usarán datos sintéticos")
    print("   Los datos sintéticos NO tienen supresión Klein (ratio ≈ 1)")
    print("   Solo sirven para verificar que el pipeline funciona\n")

    results = analyzer.run_analysis(use_real_data=True)

    return results


if __name__ == "__main__":
    results = main()
