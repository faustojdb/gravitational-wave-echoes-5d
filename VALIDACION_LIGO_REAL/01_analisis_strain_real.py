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
            return None, None, None

        except Exception as e:
            print(f"   ❌ Error: {e}")
            import traceback
            traceback.print_exc()
            return None, None, None

    def _download_hdf5(self, url, event_name, detector):
        """
        Descarga y lee archivo HDF5 de GWOSC.
        Retorna strain, sample_rate, y gps_start del archivo.
        """
        local_path = self.output_dir / f"{event_name}_{detector}.hdf5"

        try:
            # Descargar si no existe
            if not local_path.exists():
                print(f"   Descargando {local_path.name}...")
                response = requests.get(url, timeout=300, stream=True)
                if response.status_code == 200:
                    with open(local_path, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            f.write(chunk)
                    print(f"   ✓ Descargado: {local_path.stat().st_size / 1e6:.1f} MB")
                else:
                    print(f"   ❌ HTTP {response.status_code}")
                    return None, None, None

            # Leer archivo HDF5
            with h5py.File(local_path, 'r') as f:
                # Estructura típica de GWOSC HDF5
                strain = f['strain']['Strain'][:]
                # Sample rate típico: 4096 o 16384 Hz
                dt = f['strain']['Strain'].attrs.get('Xspacing', 1/4096)
                sample_rate = int(1/dt)
                # GPS start time del archivo
                gps_start = f['strain']['Strain'].attrs.get('Xstart', 0)

            print(f"   ✓ Leído: {len(strain)} samples @ {sample_rate} Hz")
            print(f"   GPS start: {gps_start}")
            return strain, sample_rate, gps_start

        except Exception as e:
            print(f"   ❌ Error leyendo HDF5: {e}")
            return None, None, None

    def extract_event_window(self, strain, sample_rate, gps_start, event_gps,
                              window_before=0.5, window_after=0.1):
        """
        Extrae la ventana temporal alrededor del evento.

        Para BBH mergers:
        - La señal crece en frecuencia y amplitud hacia el merger
        - El merger (coalescencia) es el punto de máxima amplitud
        - Después del merger viene el ringdown (decae rápidamente)

        Parameters
        ----------
        strain : array
            Datos de strain completos
        sample_rate : int
            Tasa de muestreo en Hz
        gps_start : float
            Tiempo GPS del inicio del archivo
        event_gps : float
            Tiempo GPS del evento (coalescencia)
        window_before : float
            Segundos antes del merger a incluir (default 0.5s)
        window_after : float
            Segundos después del merger a incluir (default 0.1s)

        Returns
        -------
        strain_window : array
            Segmento de strain con la señal (None si evento fuera de rango)
        t_window : array
            Vector de tiempo correspondiente
        """
        # Calcular offset temporal
        time_offset = event_gps - gps_start
        file_duration = len(strain) / sample_rate

        print(f"   GPS archivo: {gps_start} a {gps_start + file_duration:.1f}")
        print(f"   GPS evento: {event_gps}")
        print(f"   Offset: {time_offset:.1f} s")

        # Verificar que el evento está dentro del archivo
        if time_offset < 0 or time_offset > file_duration:
            print(f"   ⚠ EVENTO FUERA DE RANGO del archivo descargado")
            return None, None

        # Calcular índices
        center_idx = int(time_offset * sample_rate)

        idx_before = int(window_before * sample_rate)
        idx_after = int(window_after * sample_rate)

        start_idx = max(0, center_idx - idx_before)
        end_idx = min(len(strain), center_idx + idx_after)

        # Verificar que tenemos suficientes datos
        if end_idx <= start_idx:
            print(f"   ⚠ Ventana inválida: start={start_idx}, end={end_idx}")
            return None, None

        strain_window = strain[start_idx:end_idx]
        duration = len(strain_window) / sample_rate

        # Vector de tiempo relativo al merger (t=0 en coalescencia)
        t_window = np.linspace(-window_before, window_after, len(strain_window))

        print(f"   Ventana extraída: {duration:.3f} s alrededor del merger")
        print(f"   Índices: {start_idx} a {end_idx} (de {len(strain)} total)")

        return strain_window, t_window

    def whiten_strain(self, strain, sample_rate, fft_size=4096):
        """
        Whitening de la señal de strain.

        El whitening normaliza el espectro de potencia para que todas
        las frecuencias tengan aproximadamente la misma amplitud.
        Esto es crucial porque el ruido del detector NO es blanco
        (tiene estructura en frecuencia).

        Parameters
        ----------
        strain : array
            Datos de strain
        sample_rate : int
            Tasa de muestreo
        fft_size : int
            Tamaño del segmento para estimar PSD

        Returns
        -------
        whitened : array
            Strain whitened
        """
        # Estimar PSD usando método de Welch
        freqs, psd = signal.welch(strain, sample_rate, nperseg=min(fft_size, len(strain)//4))

        # Interpolar PSD a todas las frecuencias
        psd_interp = np.interp(
            np.fft.rfftfreq(len(strain), 1/sample_rate),
            freqs,
            psd
        )

        # Evitar división por cero
        psd_interp = np.maximum(psd_interp, 1e-40)

        # FFT de la señal
        strain_fft = np.fft.rfft(strain)

        # Dividir por sqrt(PSD) para whitening
        whitened_fft = strain_fft / np.sqrt(psd_interp)

        # Volver al dominio del tiempo
        whitened = np.fft.irfft(whitened_fft, n=len(strain))

        # Normalizar
        whitened = whitened / np.std(whitened) * np.std(strain)

        return whitened

    def generate_synthetic_test_data(self, event_name, sample_rate=4096, duration=0.6):
        """
        Genera datos sintéticos para testing del pipeline.
        SOLO para verificar que el código funciona.
        NO es el análisis real.

        Simula una señal chirp tipo BBH merger SIN supresión de modos
        (expectativa de GR estándar: ratio odd/even ≈ 1)
        """
        print(f"⚠ Generando datos SINTÉTICOS para {event_name} (solo testing)")

        t = np.linspace(0, duration, int(sample_rate * duration))

        # Señal tipo chirp simplificada
        f0 = 50   # Hz, frecuencia inicial
        f1 = 250  # Hz, frecuencia final (merger)

        # Chirp con amplitud creciente hacia el merger
        amplitude_envelope = (t / duration) ** 2

        # Fase del chirp
        phase = 2 * np.pi * (f0 * t + (f1 - f0) * t**2 / (2 * duration))

        # Fundamental + armónicos con decaimiento natural
        # En GR estándar, odd y even deberían tener amplitudes similares
        strain = np.zeros_like(t)

        for n in range(1, 9):
            amp_n = 1.0 / n  # Decaimiento natural 1/n
            strain += amp_n * np.sin(n * phase)

        strain *= amplitude_envelope

        # Añadir ruido gaussiano (SNR ~ 10)
        signal_rms = np.std(strain)
        noise = np.random.normal(0, signal_rms / 10, len(t))
        strain += noise

        return strain, sample_rate

    def analyze_harmonics(self, strain, sample_rate, event_name):
        """
        Análisis de armónicos en la señal de merger.
        Este es el análisis CIEGO - no asume Klein.

        Para ondas gravitacionales de BBH:
        - La señal es un chirp (frecuencia que aumenta hacia el merger)
        - Los "armónicos" son modos multipolares (l=2 cuadrupolo, l=3 octupolo, etc.)
        - En GR, l=2 (m=±2) domina, l=3 es ~10-20% para masas asimétricas
        - Klein predice supresión de ciertos modos

        Método:
        1. Calcular espectrograma (tiempo-frecuencia)
        2. Identificar el track del chirp principal (l=2, m=2)
        3. Buscar potencia en múltiplos de frecuencia
        4. Comparar amplitudes de modos impares vs pares
        """
        print(f"\n🔬 Analizando armónicos de {event_name}...")

        # Parámetros de análisis
        n_samples = len(strain)
        duration = n_samples / sample_rate

        print(f"   Duración ventana: {duration:.3f} s")
        print(f"   Sample rate: {sample_rate} Hz")
        print(f"   Muestras: {n_samples}")

        # Paso 1: Bandpass filter 20-500 Hz (rango típico de GW)
        nyquist = sample_rate / 2
        low = 20 / nyquist
        high = min(500 / nyquist, 0.99)

        try:
            b, a = signal.butter(4, [low, high], btype='band')
            strain_filtered = signal.filtfilt(b, a, strain)
        except Exception as e:
            print(f"   ⚠ Error en filtrado: {e}, usando datos sin filtrar")
            strain_filtered = strain

        # Paso 2: Espectrograma para señal chirp
        # Usar ventana corta para resolución temporal
        nperseg = min(256, n_samples // 4)
        noverlap = nperseg // 2

        f_spec, t_spec, Sxx = signal.spectrogram(
            strain_filtered, sample_rate,
            nperseg=nperseg, noverlap=noverlap
        )

        # Paso 3: Encontrar el track de frecuencia dominante
        # Para cada tiempo, encontrar la frecuencia con máxima potencia
        freq_track = []
        power_track = []
        for i in range(Sxx.shape[1]):
            # Buscar en rango 30-300 Hz
            valid_mask = (f_spec > 30) & (f_spec < 300)
            if np.any(valid_mask):
                slice_power = Sxx[valid_mask, i]
                max_idx = np.argmax(slice_power)
                freq_track.append(f_spec[valid_mask][max_idx])
                power_track.append(slice_power[max_idx])

        if not freq_track:
            print("   ❌ No se encontró señal en rango 30-300 Hz")
            return None

        # Frecuencia característica (mediana del track)
        f0 = np.median(freq_track)
        f0_max = np.max(freq_track)  # Frecuencia en el merger
        print(f"   Frecuencia característica: f₀ = {f0:.1f} Hz")
        print(f"   Frecuencia máxima (merger): {f0_max:.1f} Hz")

        # Paso 4: FFT completa para análisis de armónicos
        fft_result = fft(strain_filtered)
        freqs = fftfreq(n_samples, 1/sample_rate)

        # Solo frecuencias positivas
        positive_mask = freqs > 0
        freqs_pos = freqs[positive_mask]
        amplitudes = np.abs(fft_result[positive_mask])

        # Resolución en frecuencia
        df = freqs_pos[1] - freqs_pos[0]
        print(f"   Resolución FFT: Δf = {df:.2f} Hz")

        # Paso 5: Extraer potencia en bandas armónicas
        # Usar ventana más amplia debido a la naturaleza chirp
        window_hz = max(10, df * 3)  # Ventana de búsqueda

        n_harmonics = min(8, int(500 / f0))  # Hasta 500 Hz
        harmonic_amplitudes = []

        print(f"\n   Armónicos detectados (ventana ±{window_hz:.1f} Hz):")
        for n in range(1, n_harmonics + 1):
            f_harmonic = n * f0

            if f_harmonic > nyquist:
                break

            # Integrar potencia en la banda armónica
            mask = np.abs(freqs_pos - f_harmonic) < window_hz
            if np.any(mask):
                # Usar suma de potencia (mejor para señales chirp)
                power = np.sum(amplitudes[mask]**2)
                amp = np.sqrt(power)
            else:
                amp = 0

            harm_type = 'odd' if n % 2 == 1 else 'even'
            harmonic_amplitudes.append({
                'n': n,
                'frequency': f_harmonic,
                'amplitude': amp,
                'type': harm_type
            })
            print(f"      n={n} ({harm_type}): f={f_harmonic:.1f} Hz, A={amp:.2e}")

        # Paso 6: Separar odd/even y calcular ratio
        odd_amps = [h['amplitude'] for h in harmonic_amplitudes if h['type'] == 'odd']
        even_amps = [h['amplitude'] for h in harmonic_amplitudes if h['type'] == 'even']

        mean_odd = np.mean(odd_amps) if odd_amps else 0
        mean_even = np.mean(even_amps) if even_amps else 1e-20

        ratio = mean_odd / mean_even if mean_even > 1e-20 else np.inf

        print(f"\n   📊 RESULTADOS:")
        print(f"   Amplitud media (odd, n=1,3,5...):  {mean_odd:.2e}")
        print(f"   Amplitud media (even, n=2,4,6...): {mean_even:.2e}")
        print(f"   RATIO odd/even: {ratio:.2f}")

        # Paso 7: Test estadístico
        t_stat, p_value = None, None
        if len(odd_amps) > 1 and len(even_amps) > 1:
            # Usar log para normalizar las distribuciones
            log_odd = np.log10(np.array(odd_amps) + 1e-20)
            log_even = np.log10(np.array(even_amps) + 1e-20)
            t_stat, p_value = ttest_ind(log_odd, log_even)
            print(f"   t-statistic (log): {t_stat:.2f}")
            print(f"   p-value: {p_value:.4f}")

        # Paso 8: Decisión según protocolo pre-registrado
        print(f"\n   📋 DECISIÓN SEGÚN PROTOCOLO:")
        if ratio < 2:
            decision = "H₀ (GR estándar) - Sin supresión"
            klein_status = "❌ REFUTADO"
        elif ratio < 5:
            decision = "AMBIGUO - Posible asimetría natural"
            klein_status = "⚠️ INCONCLUSO"
        elif ratio < 15:
            decision = "SUGESTIVO - Supresión moderada"
            klein_status = "⚠️ SUGESTIVO"
        elif ratio < 30:
            decision = "H₁ (Klein ~7π) - Supresión significativa"
            klein_status = "🔶 CONSISTENTE"
        else:
            decision = "H₂ (Klein ~40:1) - Supresión extrema"
            klein_status = "✅ CONFIRMADO"

        print(f"   Decisión: {decision}")
        print(f"   Estado Klein: {klein_status}")

        return {
            'event': event_name,
            'f0_Hz': float(f0),
            'f0_max_Hz': float(f0_max),
            'duration_s': float(duration),
            'harmonics': harmonic_amplitudes,
            'mean_odd': float(mean_odd),
            'mean_even': float(mean_even),
            'ratio': float(ratio) if not np.isinf(ratio) else 999.0,
            't_statistic': float(t_stat) if t_stat else None,
            'p_value': float(p_value) if p_value else None,
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
            print(f"GPS time: {event_info['gps_time']}")
            print(f"{'─' * 40}")

            is_synthetic = False

            if use_real_data:
                result = self.download_strain_data(event_name, 'H1')
                if result[0] is None:
                    print("   ⚠ Usando datos sintéticos como fallback")
                    strain, sample_rate = self.generate_synthetic_test_data(event_name)
                    is_synthetic = True
                else:
                    strain_full, sample_rate, gps_start = result

                    # PASO CRÍTICO: Extraer ventana alrededor del merger
                    print(f"\n📍 Extrayendo ventana del merger...")
                    strain_window, t_window = self.extract_event_window(
                        strain_full, sample_rate, gps_start,
                        event_info['gps_time'],
                        window_before=0.5,  # 0.5s antes del merger
                        window_after=0.1    # 0.1s después (ringdown)
                    )

                    if strain_window is None or len(strain_window) < 100:
                        print("   ⚠ No se pudo extraer ventana válida")
                        print("   ⚠ Usando datos sintéticos como fallback")
                        strain, sample_rate = self.generate_synthetic_test_data(event_name)
                        is_synthetic = True
                    else:
                        # PASO CRÍTICO: Whitening
                        print(f"📊 Aplicando whitening...")
                        strain = self.whiten_strain(strain_window, sample_rate)
                        print(f"   ✓ Whitening aplicado")

            else:
                strain, sample_rate = self.generate_synthetic_test_data(event_name)
                is_synthetic = True

            if strain is not None:
                result = self.analyze_harmonics(strain, sample_rate, event_name)
                if result:
                    result['is_synthetic'] = is_synthetic
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
            data_type = "SINTÉTICO" if r.get('is_synthetic', False) else "REAL"
            print(f"  {r['event']} [{data_type}]: ratio = {r['ratio']:.2f} → {r['klein_status']}")

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
