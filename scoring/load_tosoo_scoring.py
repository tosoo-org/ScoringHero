import os, json
from .default_scoring import default_scoring


def load_tosoo_scoring(scoring_filename, epolen, numepo):

    mapping_str = {'W': 'Wake',
                   'N1': 'N1',
                   'N2': 'N2',
                   'N3': 'N3',
                   'R': 'REM'}
    mapping_num = {'Wake': 1,
                   'N1': -1,
                   'N2': -2,
                   'N3': -3,
                   'REM': 0}

    scoring_data = default_scoring(epolen, numepo)

    if os.path.exists(scoring_filename):
        with open(scoring_filename, "r") as file:
            data = json.load(file)

        hypnogram = data['hypnogram']

        for counter, stage in enumerate(hypnogram[:numepo]):
            stage_str = mapping_str.get(stage, stage)
            scoring_data[counter]["stage"] = stage_str
            scoring_data[counter]["digit"] = int(mapping_num[stage_str])
    else:
        print("Could not find scoring file")

    return scoring_data, []
