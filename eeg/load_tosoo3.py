import numpy as np
import pyarrow.parquet as pq
import json


def load_tosoo3(filename: str):
    table = pq.read_table(filename)

    metadata = json.loads(table.schema.metadata[b"metadata"])
    srate = metadata['eeg_sampling_frequency_hz']
    
    df = table.to_pandas()
    if 'is_eeg_sample' in df:
        df = df[df['is_eeg_sample']]

    eeg_columns = [col for col in df.columns if col.startswith('eeg_')]
    df = df[eeg_columns]
    eeg_data = df.values.transpose()

    channel_names = [np.str_(col.replace('eeg_', '')) for col in eeg_columns]

    print(f"Channel names before return: {channel_names}")
    print(f"Channel names first element type: {type(channel_names[0])}")
    print(f"EEG data shape: {eeg_data.shape}")
    print(f"EEG data type: {type(eeg_data)}")
    print(f"Channel names shape: {np.array(channel_names).shape}")
    print(f"Channel names type: {type(channel_names)}")
    return eeg_data, int(srate), channel_names
    # return eeg_data.astype(np.float32), srate, channel_names