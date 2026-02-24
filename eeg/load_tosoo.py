import numpy as np
import pyarrow.parquet as pq
import json
import re


def extract_tosoo_version(filename: str) -> int:
    if filename.endswith('.preprocessedEEGAxora.parquet'):
        return 5
    if filename.endswith('.preprocessedEEG.parquet'):
        return 3
    match = re.search(r'\.tosoo(\d+)[a-z]?\.parquet$', filename)
    if not match:
        raise ValueError(f"Could not extract tosoo version from filename: {filename}")
    return int(match.group(1))


def load_tosoo(filename: str):
    version = extract_tosoo_version(filename)

    table = pq.read_table(filename)

    if version == 3:
        metadata = json.loads(table.schema.metadata[b"metadata"])
        srate = metadata['eeg_sampling_frequency_hz']
    elif version == 5:
        stream_header = json.loads(table.schema.metadata[b"stream_header"])
        srate = stream_header['eeg_metadata']['sampling_frequency_hz']
    elif version == 6:
        stream_header = json.loads(table.schema.metadata[b"stream_header"])
        srate = stream_header['eeg_metadata']['sampling_frequency_hz']
    else:
        raise ValueError(f"Unknown tosoo version: {version}")

    df = table.to_pandas()
    if 'is_eeg_sample' in df:
        df = df[df['is_eeg_sample']]

    eeg_columns = [col for col in df.columns if col.startswith('eeg_')]
    df = df[eeg_columns]
    eeg_data = df.values.transpose()

    channel_names = [np.str_(col.replace('eeg_', '')) for col in eeg_columns]

    return eeg_data, int(srate), channel_names