import os
from PySide6.QtWidgets import QFileDialog
from .write_scoring import write_scoring


def scoring_export_window(ui):
    base, _ = os.path.splitext(ui.filename)
    name_of_scoringfile, _ = QFileDialog.getSaveFileName(
        None, "Write scoring file", os.path.join(ui.default_data_path, f'{base}.scoring.json'), "*json"
    )
    if name_of_scoringfile.endswith('.scoring.json'):
        ui.filename = name_of_scoringfile[:-len('.scoring.json')]
    else:
        ui.filename, _ = os.path.splitext(name_of_scoringfile)
    ui.default_data_path = os.path.dirname(name_of_scoringfile)
    write_scoring(ui)
