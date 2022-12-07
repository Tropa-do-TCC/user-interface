import PyQt5.QtWidgets as QtWidgets
from widgets.common.FileSelector import FileSelector


class LandmarksSettingsWidgets:
    def __init__(self, detect_landmarks_callback, import_landmarks_callback, parent_grid: QtWidgets.QGridLayout):
        self.group_box = QtWidgets.QGroupBox(
            "Pontos Fiduciais Cefalométricos")
        self.group_layout = QtWidgets.QGridLayout()
        self.parent_grid = parent_grid

        self.add_detect_landmarks_button(detect_landmarks_callback)
        self.add_import_landmarks_button(import_landmarks_callback)

        self.group_box.setLayout(self.group_layout)
        self.parent_grid.addWidget(self.group_box, 2, 0, 1, 2)

    def add_detect_landmarks_button(self, detect_landmarks_callback):
        self.detect_landmarks_button_label = QtWidgets.QLabel("Automático")
        self.detect_landmarks_button = QtWidgets.QPushButton(
            "Detectar pontos fiduciais")
        self.detect_landmarks_button.clicked.connect(
            detect_landmarks_callback)

        self.group_layout.addWidget(
            self.detect_landmarks_button_label, 1, 0)
        self.group_layout.addWidget(self.detect_landmarks_button, 1, 1)

        # Turn visible after skull import
        self.detect_landmarks_button.setHidden(True)
        self.detect_landmarks_button_label.setHidden(True)

    def add_import_landmarks_button(self, import_landmarks_callback):
        landmarks_file_selector = FileSelector(
            label="Importar pontos fiduciais",
            window_title='Selecionar JSON com pontos fiduciais',
            name_filter='Arquivos JSON (*.json)',
            load_callback=import_landmarks_callback
        )

        self.group_layout.addWidget(QtWidgets.QLabel("Manual"), 2, 0)
        self.group_layout.addWidget(landmarks_file_selector, 2, 1)

    def reset_values(self):
        self.detect_landmarks_button.setHidden(True)
        self.detect_landmarks_button_label.setHidden(True)
