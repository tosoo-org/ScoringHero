import os
from PySide6.QtWidgets import QFileDialog
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
    if datatype == "tosoo3":
        datatype_to_show = "*.parquet"

    name_of_eegfile, _ = QFileDialog.getOpenFileName(
        None, "Open File", ui.default_data_path, datatype_to_show
    )

    # Check if the user clicked "Cancel"
    if not name_of_eegfile:
        return  # Exit the function if no file is selected

    # Handle different file extensions
    if datatype == "tosoo3":
        # For tosoo3 files, store the full path for loading
        # but use base name without .tosoo3.parquet for config/scoring files
        if name_of_eegfile.endswith('.parquet'):
            ui.full_filename = name_of_eegfile  # Full path for loading the data file
            ui.filename = name_of_eegfile  # Remove '.parquet' for config/scoring
        else:
            ui.full_filename = name_of_eegfile
            ui.filename, _ = os.path.splitext(name_of_eegfile)

    else:
        ui.filename, suffix = os.path.splitext(name_of_eegfile)
        ui.full_filename = ui.filename  # For non-tosoo3, both are the same

    ui.default_data_path = os.path.dirname(name_of_eegfile)
    MainWindow.setWindowTitle(f"Scoring Hero v.{ui.version[0]}.{ui.version[1]}.{ui.version[2]} ({os.path.basename(name_of_eegfile)})")
    load_wrapper(ui, datatype)