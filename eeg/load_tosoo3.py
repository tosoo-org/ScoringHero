import numpy as np
import pandas as pd
import pyarrow.parquet as pq
from typing import Tuple, List, Dict, Any
import json


def load_tosoo3(filename: str) -> Tuple[np.ndarray, float, List[str]]:
    """Load tosoo3 parquet file and extract EEG data.

    Args:
        filename: Path to the .tosoo3.parquet file

    Returns:
        Tuple of:
        - eeg_data: NumPy array of shape (n_channels, n_samples) with EEG data in microvolts
        - srate: Sampling rate in Hz
        - channel_names: List of channel names
    """
    # Read the parquet file
    table = pq.read_table(filename)

    # Extract metadata
    metadata = table.schema.metadata
    if metadata:
        # Decode metadata from bytes
        metadata = {k.decode(): v.decode() for k, v in metadata.items()}

        # Extract sampling rate
        srate = float(metadata.get('eeg_sampling_frequency_hz', 200))

        # Extract configuration to get channel information
        config_str = metadata.get('configuration', '{}')
        try:
            config = json.loads(config_str)
            montage = config.get('Montage', {})
        except (json.JSONDecodeError, KeyError):
            montage = {}
    else:
        # Default values if no metadata
        srate = 200.0
        montage = {}

    # Convert to pandas DataFrame for easier manipulation
    df = table.to_pandas()

    # Filter to only EEG samples (where is_eeg_sample is True)
    eeg_df = df[df['is_eeg_sample'] == True].copy()

    # Identify EEG channels (columns starting with 'eeg_ch')
    # Handle both formats: 'eeg_ch1' and 'eeg_ch1_microvolts'
    eeg_columns = [col for col in eeg_df.columns if col.startswith('eeg_ch')]
    # Filter out any non-data columns (keep only numeric channel columns)
    eeg_columns = [col for col in eeg_columns if col.replace('eeg_ch', '').replace('_microvolts', '').replace('_', '').isdigit()]

    # Sort channel columns to ensure correct order (eeg_ch1, eeg_ch2, etc.)
    def extract_channel_number(col_name):
        # Extract number from names like 'eeg_ch1' or 'eeg_ch1_microvolts'
        import re
        match = re.search(r'eeg_ch(\d+)', col_name)
        return int(match.group(1)) if match else 0

    eeg_columns.sort(key=extract_channel_number)

    # Create channel names based on montage configuration
    channel_names = []
    for col in eeg_columns:
        ch_num = extract_channel_number(col)
        ch_key = f'channel_{ch_num}'

        # Try to get location from montage
        if montage and ch_key in montage:
            location = montage[ch_key]
            # Map location names if they're numeric codes
            location_map = {
                'not_connected': 'NC',
                'unknown': f'CH{ch_num}',
                'fp1': 'Fp1',
                'fp2': 'Fp2',
                'fpz': 'Fpz',
                'left_ear': 'A1',
                'right_ear': 'A2'
            }
            channel_name = location_map.get(location, f'CH{ch_num}')
        else:
            channel_name = f'CH{ch_num}'

        channel_names.append(channel_name)

    # Extract EEG data as numpy array
    # Shape should be (n_channels, n_samples)
    eeg_data = eeg_df[eeg_columns].values.T

    # Handle any NaN values by forward-filling (as the tosoo3 format uses forward-fill)
    # This shouldn't be necessary for EEG samples but included for safety
    eeg_data = pd.DataFrame(eeg_data).ffill(axis=1).fillna(0).values

    # Convert from raw ADC values to microvolts
    # The tosoo3 format stores raw 24-bit ADC values despite metadata saying "microvolts"
    # Standard conversion for ADS1299 (common in EEG devices) with 24x gain:
    # Full scale range is ±8388607 (24-bit) corresponding to ±187.5 µV
    # This gives us approximately 0.0223 µV per ADC count
    ADC_TO_MICROVOLTS = 187.5 / 8388607  # ~0.0223 µV per count
    eeg_data = eeg_data * ADC_TO_MICROVOLTS

    return eeg_data.astype(np.float32), srate, channel_names