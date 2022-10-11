
import PyQt5.QtCore as Qt
import PyQt5.QtWidgets as QtWidgets
import vtk
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

from neuralnetwork import train
from neuralnetwork.execute_neural_network import read_dataset
from reconstruction.reconstruction import VtkHandler
from utils.landmarks_utils import get_landmarks_from_network_infer_with_list


class AppWindow(QtWidgets.QMainWindow, QtWidgets.QApplication):
    def __init__(self, app):
        self.app = app
        QtWidgets.QMainWindow.__init__(self, None)

        self.renderer, self.frame, self.vtk_widget, self.interactor, self.render_window = self.setup()
        self.vtk_handler = VtkHandler(self.render_window, self.renderer)
        self.default_vtk_group_box_title = "Visualização do crânio"

        self.skull = [None, None]

        self.add_menu_bar()

        self.grid = QtWidgets.QGridLayout()

        self.add_vtk_widget()
        self.add_skull_settings_widget()
        self.add_landmarks_settings_widget()
        self.add_views_widget()

        self.render_window.Render()
        self.setWindowTitle("Detecção de pontos fiduciais cefalométricos")
        self.frame.setLayout(self.grid)
        self.setCentralWidget(self.frame)
        self.interactor.Initialize()
        self.show()

    @staticmethod
    def setup():
        renderer = vtk.vtkRenderer()
        frame = QtWidgets.QFrame()
        frame.setStyleSheet(open('styles.css').read())
        vtk_widget = QVTKRenderWindowInteractor()
        interactor = vtk_widget.GetRenderWindow().GetInteractor()
        render_window = vtk_widget.GetRenderWindow()

        frame.setAutoFillBackground(True)
        vtk_widget.GetRenderWindow().AddRenderer(renderer)
        render_window.AddRenderer(renderer)
        interactor.SetRenderWindow(render_window)
        interactor.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())

        return renderer, frame, vtk_widget, interactor, render_window

    def add_menu_bar(self):
        menu_bar = self.menuBar()

        # Export menu button
        export_menu = menu_bar.addMenu("&Exportar")

        export_landmarks_action = QtWidgets.QAction(
            "Exportar pontos fiduciais", self)
        export_landmarks_action.triggered.connect(self.set_landmarks_files)
        export_menu.addAction(export_landmarks_action)

        # Neural network menu button
        neural_network_menu = menu_bar.addMenu("&Rede Neural")

        export_landmarks_action = QtWidgets.QAction(
            "Treinar modelo", self)
        export_landmarks_action.triggered.connect(self.train_neural_network)
        neural_network_menu.addAction(export_landmarks_action)

    def add_vtk_widget(self):
        wrapper_group_box = QtWidgets.QGroupBox()
        wrapper_layout = QtWidgets.QVBoxLayout()

        # vtk window view
        vtk_group_box = QtWidgets.QGroupBox(self.default_vtk_group_box_title)
        self.group_box_widget = vtk_group_box
        vtk_layout = QtWidgets.QVBoxLayout()
        vtk_layout.addWidget(self.vtk_widget)
        vtk_group_box.setLayout(vtk_layout)

        # reset view button
        reset_view_button = QtWidgets.QPushButton("Resetar visualização")
        reset_view_button.setFixedSize(150, 30)
        reset_view_button.clicked.connect(self.clean_view)

        wrapper_layout.addWidget(vtk_group_box)
        wrapper_layout.addWidget(reset_view_button)

        wrapper_group_box.setLayout(wrapper_layout)

        self.grid.addWidget(wrapper_group_box, 0, 2, 5, 5)
        self.grid.setColumnMinimumWidth(2, 700)

    def create_directory_selector(self, label, window_title, load_callback):
        directory_import_button = QtWidgets.QPushButton(label)
        directory_import_button.clicked.connect(
            lambda _: self.open_directory(window_title, label, load_callback))

        return directory_import_button

    def open_directory(self, window_title, label, load_callback):
        dialog = QtWidgets.QFileDialog(self)
        dialog.setWindowTitle(window_title)
        dialog.setDirectory(Qt.QDir.currentPath())
        directory_path = QtWidgets.QFileDialog.getExistingDirectory(
            self, label)

        if directory_path:
            load_callback(directory_path)

    def create_file_selector(self, label, window_title, name_filter, load_callback):
        file_import_button = QtWidgets.QPushButton(label)
        file_import_button.clicked.connect(
            lambda _: self.open_file(window_title, name_filter, load_callback))

        return file_import_button

    def open_file(self, window_title, name_filter, load_callback):
        dialog = QtWidgets.QFileDialog(self)
        dialog.setWindowTitle(window_title)
        dialog.setNameFilter(name_filter)
        dialog.setDirectory(Qt.QDir.currentPath())
        dialog.setFileMode(QtWidgets.QFileDialog.ExistingFile)

        if dialog.exec_():
            selected_file = dialog.selectedFiles()[0]
            load_callback(selected_file)

    def set_skull(self, dicom_dir_path):
        self.skull, patient_name = self.vtk_handler.setup_skull(dicom_dir_path)
        self.group_box_widget.setTitle(
            f"Visualização do crânio: {patient_name}")
        self.vtk_handler.set_sagittal_view()

    def set_real_landmarks(self, file_path):
        self.real_landmarks = self.vtk_handler.setup_landmarks_from_file(
            file_path)
        self.vtk_handler.set_sagittal_view()

    def set_detected_landmarks(self):
        if self.skull[1] is None:
            get_landmarks_from_network_infer_with_list()
        else:
            self.real_landmarks, self.detected_landmarks = self.vtk_handler.setup_detected_landmarks(self.skull[1])
            self.vtk_handler.set_sagittal_view()

    def set_landmarks_files(self): read_dataset()

    def train_neural_network(self): train.main()

    def clean_view(self):
        self.group_box_widget.setTitle(self.default_vtk_group_box_title)
        self.renderer.RemoveAllViewProps()
        self.renderer.Render()

    def add_skull_settings_widget(self):
        skull_group_box = QtWidgets.QGroupBox("Crânio")
        skull_group_layout = QtWidgets.QGridLayout()

        skull_file_selector = self.create_directory_selector(
            label="Selecionar DICOMDIR",
            window_title='Selecionar diretório de tomografias',
            load_callback=self.set_skull
        )
        skull_group_layout.addWidget(skull_file_selector, 1, 0, 1, 3)

        # skull opacity slider
        skull_opacity_slider = self.create_slider(
            min_value=0,
            max_value=1,
            initial_value=self.skull[0].property.GetOpacity(
            ) * 100 if self.skull[0] is not None else 100,
            change_callback=self.vtk_handler.set_skull_opacity
        )

        skull_group_layout.addWidget(QtWidgets.QLabel("Opacidade"), 3, 0)
        skull_group_layout.addWidget(skull_opacity_slider, 3, 1, 1, 2)

        # segmentation
        segmentation_combobox = self.create_combobox(
            items=["EHO", "ABC", "FFA"]
        )
        skull_group_layout.addWidget(QtWidgets.QLabel("Segmentação"), 4, 0)
        skull_group_layout.addWidget(segmentation_combobox, 4, 1, 1, 2)

        skull_group_box.setLayout(skull_group_layout)
        self.grid.addWidget(skull_group_box, 0, 0, 1, 2)

    def add_landmarks_settings_widget(self):
        landmarks_group_box = QtWidgets.QGroupBox("Pontos Fiduciais")
        landmarks_group_layout = QtWidgets.QGridLayout()

        # detect landmarks button
        detect_landmarks_button = QtWidgets.QPushButton(
            "Detectar pontos fiduciais")
        detect_landmarks_button.clicked.connect(self.set_detected_landmarks)

        landmarks_group_layout.addWidget(QtWidgets.QLabel("Automático"), 1, 0)
        landmarks_group_layout.addWidget(detect_landmarks_button, 1, 1)

        # import landmarks button
        landmarks_file_selector = self.create_file_selector(
            label="Importar pontos fiduciais",
            window_title='Selecionar JSON com pontos fiduciais',
            name_filter='Arquivos JSON/TXT (*.*)',
            load_callback=self.set_real_landmarks
        )

        landmarks_group_layout.addWidget(QtWidgets.QLabel("Manual"), 2, 0)
        landmarks_group_layout.addWidget(landmarks_file_selector, 2, 1)

        # landmarks visible checkbox
        # landmarks_visible_checkbox = QtWidgets.QCheckBox("Visível")
        # landmarks_group_layout.addWidget(
        #     landmarks_visible_checkbox, 6, 0, 1, 3)

        landmarks_group_box.setLayout(landmarks_group_layout)
        self.grid.addWidget(landmarks_group_box, 1, 0, 2, 2)

    def add_views_widget(self):
        views_box = QtWidgets.QGroupBox("Visualização")
        views_box_layout = QtWidgets.QVBoxLayout()

        # axial view button
        axial_view = QtWidgets.QPushButton("Axial")
        axial_view.clicked.connect(self.vtk_handler.set_axial_view)
        views_box_layout.addWidget(axial_view)

        # coronal view button
        coronal_view = QtWidgets.QPushButton("Coronal")
        coronal_view.clicked.connect(self.vtk_handler.set_coronal_view)
        views_box_layout.addWidget(coronal_view)

        # sagittal view button
        sagittal_view = QtWidgets.QPushButton("Sagittal")
        sagittal_view.clicked.connect(self.vtk_handler.set_sagittal_view)
        views_box_layout.addWidget(sagittal_view)

        views_box.setLayout(views_box_layout)
        self.grid.addWidget(views_box, 3, 0, 2, 2)

    def create_combobox(self, items):
        combobox = QtWidgets.QComboBox(self)
        [combobox.addItem(item) for item in items]

        return combobox

    def create_separator(self):
        separator = QtWidgets.QWidget()
        separator.setFixedHeight(1)
        separator.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        separator.setStyleSheet("background-color: #c8c8c8;")

        return separator

    def create_slider(self, min_value, max_value, initial_value, change_callback):
        slider = QtWidgets.QSlider(Qt.Qt.Horizontal)
        slider.setValue(int(initial_value))

        slider.setMinimum(min_value * 100)
        slider.setMaximum(max_value * 100)

        slider.valueChanged.connect(lambda _: change_callback(slider.value()))

        return slider
