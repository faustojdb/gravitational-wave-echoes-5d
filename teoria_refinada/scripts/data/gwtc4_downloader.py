#!/usr/bin/env python3
"""
GWTC-4.0 CATALOG DOWNLOADER
===========================

Professional downloader for the complete GWTC-4.0 catalog from GWOSC.
Downloads all 128+ events from O4a with official parameters.

Data source: Gravitational Wave Open Science Center (GWOSC)
API: https://gwosc.org/eventapi/

Author: Klein Theory Validation Team
Date: January 2026
"""

import os
import json
import requests
import pandas as pd
import numpy as np
from datetime import datetime
from pathlib import Path
import time

class GWTC4Downloader:
    """
    Professional downloader for GWTC-4.0 catalog data.
    """

    # GWOSC API endpoints
    GWOSC_BASE_URL = "https://gwosc.org/eventapi/json"
    CATALOGS = {
        'GWTC-1-confident': 'O1/O2 confident events',
        'GWTC-2.1-confident': 'O3a confident events',
        'GWTC-3-confident': 'O3b confident events',
        'GWTC-4.0': 'O4a confident events (NEW - 128 events)',
        'O4_Discovery_Papers': 'O4 notable events (GW231123, GW230529, etc.)',
    }

    # Parameters to extract
    PARAMETERS = [
        'GPS', 'mass_1_source', 'mass_1_source_lower', 'mass_1_source_upper',
        'mass_2_source', 'mass_2_source_lower', 'mass_2_source_upper',
        'total_mass_source', 'total_mass_source_lower', 'total_mass_source_upper',
        'final_mass_source', 'final_mass_source_lower', 'final_mass_source_upper',
        'chirp_mass_source', 'chirp_mass_source_lower', 'chirp_mass_source_upper',
        'luminosity_distance', 'luminosity_distance_lower', 'luminosity_distance_upper',
        'redshift', 'redshift_lower', 'redshift_upper',
        'network_matched_filter_snr', 'network_matched_filter_snr_lower', 'network_matched_filter_snr_upper',
        'chi_eff', 'chi_eff_lower', 'chi_eff_upper',
        'far', 'p_astro',
        'final_spin', 'final_spin_lower', 'final_spin_upper',
    ]

    def __init__(self, output_dir=None):
        if output_dir is None:
            script_dir = Path(__file__).parent
            output_dir = script_dir.parent.parent / 'datos' / 'gwtc4'

        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Klein-Theory-GWTC4-Downloader/1.0'
        })

        self.download_log = []
        self.timestamp = datetime.now().isoformat()

        print("=" * 70)
        print("GWTC-4.0 CATALOG DOWNLOADER")
        print("=" * 70)
        print(f"Output directory: {self.output_dir.absolute()}")
        print(f"Timestamp: {self.timestamp}")
        print()

    def _log(self, message, level="INFO"):
        """Log message with timestamp."""
        ts = datetime.now().strftime("%H:%M:%S")
        prefix = {"INFO": "ℹ️", "SUCCESS": "✅", "ERROR": "❌", "WARNING": "⚠️"}.get(level, "")
        print(f"[{ts}] {prefix} {message}")
        self.download_log.append({
            'timestamp': ts,
            'level': level,
            'message': message
        })

    def fetch_catalog_events(self, catalog_name):
        """
        Fetch all events from a specific catalog.

        Parameters
        ----------
        catalog_name : str
            Name of catalog (e.g., 'GWTC-4.0-confident')

        Returns
        -------
        list : List of event dictionaries
        """
        url = f"{self.GWOSC_BASE_URL}/{catalog_name}/"

        self._log(f"Fetching catalog: {catalog_name}")

        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            data = response.json()

            events = data.get('events', {})
            self._log(f"Found {len(events)} events in {catalog_name}", "SUCCESS")

            return events

        except requests.exceptions.RequestException as e:
            self._log(f"Failed to fetch {catalog_name}: {e}", "ERROR")
            return {}

    def fetch_event_parameters(self, event_url):
        """
        Fetch detailed parameters for a single event.

        Parameters
        ----------
        event_url : str
            JSON URL for the event

        Returns
        -------
        dict : Event parameters
        """
        try:
            response = self.session.get(event_url, timeout=30)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            self._log(f"Failed to fetch event details: {e}", "WARNING")
            return {}

    def extract_event_data(self, event_name, event_info, catalog_name):
        """
        Extract relevant parameters from event data.

        Parameters
        ----------
        event_name : str
            Event identifier
        event_info : dict
            Raw event data from API
        catalog_name : str
            Source catalog name

        Returns
        -------
        dict : Extracted parameters
        """
        # Get the latest version
        if isinstance(event_info, dict):
            # Event info might have version keys
            versions = [k for k in event_info.keys() if k.startswith(event_name)]
            if versions:
                latest = sorted(versions)[-1]
                params = event_info[latest]
            else:
                params = event_info
        else:
            params = {}

        # Extract parameters
        extracted = {
            'event_name': event_name.split('-')[0] if '-' in event_name else event_name,
            'catalog': catalog_name,
            'version': params.get('version', 1),
        }

        # Extract all defined parameters
        for param in self.PARAMETERS:
            extracted[param] = params.get(param)

        # Calculate derived parameters
        if extracted.get('total_mass_source') and extracted.get('final_mass_source'):
            total = extracted['total_mass_source']
            final = extracted['final_mass_source']
            if total and final:
                extracted['energy_radiated'] = total - final

        # Determine observing run from event name
        extracted['observing_run'] = self._determine_run(event_name)

        return extracted

    def _determine_run(self, event_name):
        """Determine observing run from event name."""
        if not event_name.startswith('GW'):
            return 'Unknown'

        try:
            # Extract date part (e.g., GW150914 -> 150914)
            date_str = event_name[2:8]
            year = int('20' + date_str[:2])

            if year <= 2016:
                return 'O1'
            elif year <= 2017:
                return 'O2'
            elif year <= 2020 and int(date_str[2:4]) <= 3:
                return 'O3a'
            elif year <= 2020:
                return 'O3b'
            elif year >= 2023:
                return 'O4a'
            else:
                return 'Unknown'
        except:
            return 'Unknown'

    def download_all_catalogs(self, include_historical=True):
        """
        Download all available catalogs.

        Parameters
        ----------
        include_historical : bool
            Whether to include GWTC-1, 2.1, 3 (default: True)

        Returns
        -------
        pd.DataFrame : Combined catalog data
        """
        all_events = []

        catalogs_to_fetch = list(self.CATALOGS.keys()) if include_historical else ['GWTC-4.0-confident']

        for catalog_name in catalogs_to_fetch:
            self._log(f"Processing {catalog_name}: {self.CATALOGS[catalog_name]}")

            events = self.fetch_catalog_events(catalog_name)

            for event_name, event_info in events.items():
                event_data = self.extract_event_data(event_name, event_info, catalog_name)
                all_events.append(event_data)

            # Be nice to the server
            time.sleep(0.5)

        # Create DataFrame
        df = pd.DataFrame(all_events)

        # Sort by GPS time
        if 'GPS' in df.columns:
            df = df.sort_values('GPS').reset_index(drop=True)

        self._log(f"Total events downloaded: {len(df)}", "SUCCESS")

        return df

    def download_gwtc4_only(self):
        """
        Download only GWTC-4.0 events (O4a).

        Returns
        -------
        pd.DataFrame : GWTC-4.0 catalog data
        """
        self._log("Downloading GWTC-4.0 catalog only")

        events_dict = self.fetch_catalog_events('GWTC-4.0-confident')

        all_events = []
        for event_name, event_info in events_dict.items():
            event_data = self.extract_event_data(event_name, event_info, 'GWTC-4.0-confident')
            all_events.append(event_data)

        df = pd.DataFrame(all_events)

        if 'GPS' in df.columns:
            df = df.sort_values('GPS').reset_index(drop=True)

        return df

    def save_catalog(self, df, filename_prefix='gwtc'):
        """
        Save catalog to CSV and JSON formats.

        Parameters
        ----------
        df : pd.DataFrame
            Catalog data
        filename_prefix : str
            Prefix for output files

        Returns
        -------
        dict : Paths to saved files
        """
        timestamp_str = datetime.now().strftime('%Y%m%d')

        # Save CSV
        csv_path = self.output_dir / f"{filename_prefix}_catalog_{timestamp_str}.csv"
        df.to_csv(csv_path, index=False)
        self._log(f"Saved CSV: {csv_path}", "SUCCESS")

        # Save JSON with metadata
        json_path = self.output_dir / f"{filename_prefix}_catalog_{timestamp_str}.json"

        output_data = {
            'metadata': {
                'download_timestamp': self.timestamp,
                'n_events': len(df),
                'catalogs': df['catalog'].unique().tolist() if 'catalog' in df.columns else [],
                'observing_runs': df['observing_run'].unique().tolist() if 'observing_run' in df.columns else [],
                'source': 'GWOSC (gwosc.org)',
                'download_log': self.download_log
            },
            'events': df.to_dict(orient='records')
        }

        with open(json_path, 'w') as f:
            json.dump(output_data, f, indent=2, default=str)
        self._log(f"Saved JSON: {json_path}", "SUCCESS")

        # Create a symlink to latest version
        latest_csv = self.output_dir / f"{filename_prefix}_latest.csv"
        latest_json = self.output_dir / f"{filename_prefix}_latest.json"

        # Remove old symlinks if they exist
        for link in [latest_csv, latest_json]:
            if link.exists() or link.is_symlink():
                link.unlink()

        # Create new symlinks
        try:
            latest_csv.symlink_to(csv_path.name)
            latest_json.symlink_to(json_path.name)
            self._log("Created symlinks to latest versions", "SUCCESS")
        except OSError:
            # Symlinks might not work on all systems
            pass

        return {
            'csv': str(csv_path),
            'json': str(json_path)
        }

    def print_summary(self, df):
        """
        Print summary statistics of the catalog.

        Parameters
        ----------
        df : pd.DataFrame
            Catalog data
        """
        print("\n" + "=" * 70)
        print("CATALOG SUMMARY")
        print("=" * 70)

        print(f"\nTotal events: {len(df)}")

        if 'catalog' in df.columns:
            print("\nEvents by catalog:")
            for cat, count in df['catalog'].value_counts().items():
                print(f"  • {cat}: {count}")

        if 'observing_run' in df.columns:
            print("\nEvents by observing run:")
            for run, count in df['observing_run'].value_counts().items():
                print(f"  • {run}: {count}")

        if 'total_mass_source' in df.columns:
            masses = df['total_mass_source'].dropna()
            if len(masses) > 0:
                print(f"\nMass statistics (M☉):")
                print(f"  • Range: {masses.min():.1f} - {masses.max():.1f}")
                print(f"  • Mean: {masses.mean():.1f}")
                print(f"  • Median: {masses.median():.1f}")

        if 'network_matched_filter_snr' in df.columns:
            snrs = df['network_matched_filter_snr'].dropna()
            if len(snrs) > 0:
                print(f"\nSNR statistics:")
                print(f"  • Range: {snrs.min():.1f} - {snrs.max():.1f}")
                print(f"  • Mean: {snrs.mean():.1f}")
                print(f"  • Max SNR event: {df.loc[snrs.idxmax(), 'event_name']}")

        if 'energy_radiated' in df.columns:
            energies = df['energy_radiated'].dropna()
            if len(energies) > 0:
                print(f"\nEnergy radiated statistics (M☉c²):")
                print(f"  • Range: {energies.min():.2f} - {energies.max():.2f}")
                print(f"  • Mean: {energies.mean():.2f}")

        # Notable events
        print("\n" + "-" * 40)
        print("NOTABLE EVENTS FOR KLEIN ANALYSIS:")
        print("-" * 40)

        # Highest mass
        if 'total_mass_source' in df.columns:
            max_mass_idx = df['total_mass_source'].idxmax()
            if pd.notna(max_mass_idx):
                event = df.loc[max_mass_idx]
                print(f"\n🏋️ Highest mass: {event['event_name']}")
                print(f"   M_total = {event['total_mass_source']:.1f} M☉")

        # Highest SNR
        if 'network_matched_filter_snr' in df.columns:
            max_snr_idx = df['network_matched_filter_snr'].idxmax()
            if pd.notna(max_snr_idx):
                event = df.loc[max_snr_idx]
                print(f"\n📡 Highest SNR: {event['event_name']}")
                print(f"   SNR = {event['network_matched_filter_snr']:.1f}")

        # Mass gap candidates (2-5 M☉ component)
        if 'mass_2_source' in df.columns:
            mass_gap = df[(df['mass_2_source'] >= 2) & (df['mass_2_source'] <= 5)]
            if len(mass_gap) > 0:
                print(f"\n🔍 Mass gap candidates: {len(mass_gap)} events")
                for _, event in mass_gap.head(3).iterrows():
                    print(f"   • {event['event_name']}: m2 = {event['mass_2_source']:.1f} M☉")


def main():
    """Main function to download GWTC-4.0 catalog."""

    print("\n" + "🌌" * 35)
    print("GRAVITATIONAL WAVE CATALOG DOWNLOADER")
    print("🌌" * 35 + "\n")

    # Initialize downloader
    downloader = GWTC4Downloader()

    # Download all catalogs (including historical for comparison)
    print("\n📥 DOWNLOADING ALL GWTC CATALOGS...")
    print("-" * 40)

    df_all = downloader.download_all_catalogs(include_historical=True)

    # Save combined catalog
    if len(df_all) > 0:
        paths = downloader.save_catalog(df_all, filename_prefix='gwtc_combined')

        # Print summary
        downloader.print_summary(df_all)

        print("\n" + "=" * 70)
        print("DOWNLOAD COMPLETE")
        print("=" * 70)
        print(f"\nFiles saved to: {downloader.output_dir}")
        print(f"  • CSV: {paths['csv']}")
        print(f"  • JSON: {paths['json']}")

        return df_all
    else:
        print("\n❌ No events downloaded. Check network connection and API availability.")
        return None


if __name__ == "__main__":
    df = main()
