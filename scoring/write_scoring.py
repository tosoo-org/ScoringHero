import json
from PySide6.QtWidgets import QMessageBox


def write_scoring(ui):
    try:
        annotations = []
        for numerator, container in enumerate(ui.AnnotationContainer):
            for counter, (border, epochs) in enumerate(zip(container.borders, container.epochs)):
                annotations.append(
                    {
                        "key": container.key,
                        "event": container.label,
                        "digit": numerator,
                        "counter": counter,
                        "epoch": epochs,
                        "start": border[0],
                        "end": border[1],
                    }
                )

        scoring_filename = f"{ui.filename}{ui.scoring_suffix}"
        with open(scoring_filename, "w") as file:
            json.dump([ui.stages, annotations], file, indent=1)

    except Exception as e:
        scoring_filename = f"{ui.filename}{ui.scoring_suffix}"
        error_message = f"An error occurred while writing the scoring file in \n{scoring_filename}: \n\n{str(e)} \n\nThis means that the latest change in the scoring file was not saved! Please 1) screenshot this errorbox and 2) go to the black command window that opened with this program and copy the last error messages. Please report this bug so that it can be fixed fast!"
        QMessageBox.critical(ui, "Error", error_message)
