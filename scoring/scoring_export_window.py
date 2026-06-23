import os
from PySide6.QtWidgets import QFileDialog
from .write_scoring import write_scoring


def scoring_export_window(ui):
    suffix = ui.scoring_suffix
    name_of_scoringfile, _ = QFileDialog.getSaveFileName(
        None, "Write scoring file", f'{ui.filename}{suffix}', "*json"
    )
    if not name_of_scoringfile:
        return
    if name_of_scoringfile.endswith(suffix):
        ui.filename = name_of_scoringfile[:-len(suffix)]
    else:
        ui.filename, _ = os.path.splitext(name_of_scoringfile)
    ui.default_data_path = os.path.dirname(name_of_scoringfile)
    write_scoring(ui)
