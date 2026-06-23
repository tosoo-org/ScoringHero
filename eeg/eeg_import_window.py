import os
from PySide6.QtWidgets import QFileDialog
from .load_tosoo import strip_tosoo_suffix
from .load_wrapper import load_wrapper


def eeg_import_window(ui, MainWindow, datatype):
    if datatype == "eeglab":
        datatype_to_show = "*.mat"
    if datatype == "r09":
        datatype_to_show = "*.r09"
    if datatype == "edf":
        datatype_to_show = "*.edf"
    if datatype == "edfvolt":
        datatype_to_show = "*.edf"
    if datatype == "tosoo":
        datatype_to_show = "*.parquet"

    name_of_eegfile, _ = QFileDialog.getOpenFileName(
        None, "Open File", ui.default_data_path, datatype_to_show
    )

    # Check if the user clicked "Cancel"
    if not name_of_eegfile:
        return  # Exit the function if no file is selected

    ui.full_filename = name_of_eegfile
    if datatype == "tosoo":
        ui.filename = strip_tosoo_suffix(name_of_eegfile)
        ui.scoring_suffix = ".json"
    else:
        ui.filename, _ = os.path.splitext(name_of_eegfile)
        ui.scoring_suffix = ".scoring.json"

    ui.default_data_path = os.path.dirname(name_of_eegfile)
    MainWindow.setWindowTitle(f"Scoring Hero v.{ui.version[0]}.{ui.version[1]}.{ui.version[2]} ({os.path.basename(name_of_eegfile)})")
    load_wrapper(ui, datatype)