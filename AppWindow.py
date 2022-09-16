import math
import os

import PyQt5.QtCore as Qt
import PyQt5.QtWidgets as QtWidgets
import vtk
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

from reconstruction import VtkHandler


class AppWindow(QtWidgets.QMainWindow, QtWidgets.QApplication):
    def __init__(self, app):
        self.app = app
        QtWidgets.QMainWindow.__init__(self, None)

        self.nii_file_path = "cts.nii.gz"

        self.renderer, self.frame, self.vtk_widget, self.interactor, self.render_window = self.setup()
        self.vtk_handler = VtkHandler(self.render_window, self.renderer)

        self.skull = self.vtk_handler.setup_skull(self.nii_file_path)

        self.grid = QtWidgets.QGridLayout()

        self.add_vtk_widget()
        self.add_skull_settings_widget()
        self.add_landmarks_settings_widget()
        self.add_views_widget()

        self.render_window.Render()
        self.setWindowTitle("Detecção de pontos fiduciais cefalométricos")
        self.frame.setLayout(self.grid)
        self.setCentralWidget(self.frame)
        self.set_axial_view()
        self.interactor.Initialize()
        self.show()

    @staticmethod
    def setup():
        renderer = vtk.vtkRenderer()
        frame = QtWidgets.QFrame()
        vtk_widget = QVTKRenderWindowInteractor()
        interactor = vtk_widget.GetRenderWindow().GetInteractor()
        render_window = vtk_widget.GetRenderWindow()

        frame.setAutoFillBackground(True)
        vtk_widget.GetRenderWindow().AddRenderer(renderer)
        render_window.AddRenderer(renderer)
        interactor.SetRenderWindow(render_window)
        interactor.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())

        return renderer, frame, vtk_widget, interactor, render_window

    def add_vtk_widget(self):
        base_brain_file = os.path.basename(self.nii_file_path)

        wrapper_group_box = QtWidgets.QGroupBox()
        wrapper_layout = QtWidgets.QVBoxLayout()

        vtk_group_title = f"Crânio: {base_brain_file}"
        vtk_group_box = QtWidgets.QGroupBox(vtk_group_title)
        vtk_layout = QtWidgets.QVBoxLayout()
        vtk_layout.addWidget(self.vtk_widget)
        vtk_group_box.setLayout(vtk_layout)

        reset_button = QtWidgets.QPushButton("Resetar visualização")
        reset_button.setFixedSize(150, 30)
        reset_button.clicked.connect(lambda _: None)

        wrapper_layout.addWidget(vtk_group_box)
        wrapper_layout.addWidget(reset_button)

        wrapper_group_box.setLayout(wrapper_layout)

        self.grid.addWidget(wrapper_group_box, 0, 2, 5, 5)
        self.grid.setColumnMinimumWidth(2, 700)

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

    def add_skull_settings_widget(self):
        skull_group_box = QtWidgets.QGroupBox("Crânio")
        skull_group_layout = QtWidgets.QGridLayout()

        skull_file_selector = self.create_file_selector(
            label="Importar arquivo NIFTI",
            window_title='Selecionar arquivo NIFTI',
            name_filter='Arquivos nii.gz (*.nii.gz)',
            load_callback=lambda file_path: self.vtk_handler.setup_skull(
                self.renderer, file_path)
        )
        skull_group_layout.addWidget(skull_file_selector, 1, 0, 1, 3)

        skull_group_layout.addWidget(self.create_separator(), 2, 0, 1, 3)

        skull_opacity_slider = self.create_slider(
            0, 1, self.skull.property.GetOpacity() * 100, self.vtk_handler.set_skull_opacity)
        skull_group_layout.addWidget(QtWidgets.QLabel("Opacidade"), 3, 0)
        skull_group_layout.addWidget(skull_opacity_slider, 3, 1, 1, 2)

        skull_group_box.setLayout(skull_group_layout)
        self.grid.addWidget(skull_group_box, 0, 0, 1, 2)

    def add_landmarks_settings_widget(self):
        landmarks_group_box = QtWidgets.QGroupBox("Pontos Fiduciais")
        landmarks_group_layout = QtWidgets.QGridLayout()

        detect_landmarks_button = QtWidgets.QPushButton(
            "Detectar pontos fiduciais")
        detect_landmarks_button.clicked.connect(
            self.vtk_handler.setup_detected_landmarks)
        landmarks_group_layout.addWidget(QtWidgets.QLabel("Automático"), 1, 0)
        landmarks_group_layout.addWidget(detect_landmarks_button, 1, 1)

        landmarks_file_selector = self.create_file_selector(
            label="Importar pontos fiduciais",
            window_title='Selecionar JSON com pontos fiduciais',
            name_filter='Arquivos JSON (*.json)',
            load_callback=lambda file_path: self.vtk_handler.setup_landmarks_from_file(
                file_path)
        )
        landmarks_group_layout.addWidget(QtWidgets.QLabel("Manual"), 2, 0)
        landmarks_group_layout.addWidget(landmarks_file_selector, 2, 1)

        landmarks_group_layout.addWidget(self.create_separator(), 3, 0, 1, 3)

        landmarks_visible_checkbox = QtWidgets.QCheckBox("Visível")
        landmarks_group_layout.addWidget(
            landmarks_visible_checkbox, 4, 0, 1, 3)

        landmarks_group_box.setLayout(landmarks_group_layout)
        self.grid.addWidget(landmarks_group_box, 1, 0, 2, 2)

    def add_views_widget(self):
        axial_view = QtWidgets.QPushButton("Axial")
        coronal_view = QtWidgets.QPushButton("Coronal")
        sagittal_view = QtWidgets.QPushButton("Sagittal")

        views_box = QtWidgets.QGroupBox("Visualização")
        views_box_layout = QtWidgets.QVBoxLayout()
        views_box_layout.addWidget(axial_view)
        views_box_layout.addWidget(coronal_view)
        views_box_layout.addWidget(sagittal_view)

        views_box.setLayout(views_box_layout)
        self.grid.addWidget(views_box, 3, 0, 2, 2)

        axial_view.clicked.connect(self.set_axial_view)
        coronal_view.clicked.connect(self.set_coronal_view)
        sagittal_view.clicked.connect(self.set_sagittal_view)

    def set_axial_view(self):
        self.renderer.ResetCamera()
        focal_point = self.renderer.GetActiveCamera().GetFocalPoint()
        position = self.renderer.GetActiveCamera().GetPosition()
        distance = math.sqrt((position[0] - focal_point[0]) ** 2 + (
            position[1] - focal_point[1]) ** 2 + (position[2] - focal_point[2]) ** 2)
        self.renderer.GetActiveCamera().SetPosition(
            focal_point[0], focal_point[1], focal_point[2] + distance)
        self.renderer.GetActiveCamera().SetViewUp(0.0, 1.0, 0.0)
        self.renderer.GetActiveCamera().Zoom(1.8)
        self.render_window.Render()

    def set_coronal_view(self):
        self.renderer.ResetCamera()
        focal_point = self.renderer.GetActiveCamera().GetFocalPoint()
        position = self.renderer.GetActiveCamera().GetPosition()
        distance = math.sqrt((position[0] - focal_point[0]) ** 2 + (
            position[1] - focal_point[1]) ** 2 + (position[2] - focal_point[2]) ** 2)
        self.renderer.GetActiveCamera().SetPosition(
            focal_point[0], focal_point[2] - distance, focal_point[1])
        self.renderer.GetActiveCamera().SetViewUp(0.0, 0.5, 0.5)
        self.renderer.GetActiveCamera().Zoom(1.8)
        self.render_window.Render()

    def set_sagittal_view(self):
        self.renderer.ResetCamera()
        focal_point = self.renderer.GetActiveCamera().GetFocalPoint()
        position = self.renderer.GetActiveCamera().GetPosition()
        distance = math.sqrt((position[0] - focal_point[0]) ** 2 + (
            position[1] - focal_point[1]) ** 2 + (position[2] - focal_point[2]) ** 2)
        self.renderer.GetActiveCamera().SetPosition(
            focal_point[2] + distance, focal_point[0], focal_point[1])
        self.renderer.GetActiveCamera().SetViewUp(0.0, 0.0, 1.0)
        self.renderer.GetActiveCamera().Zoom(1.6)
        self.render_window.Render()

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

        slider.valueChanged.connect(lambda _: change_callback(slider.value()))

        slider.setMinimum(min_value * 100)
        slider.setMaximum(max_value * 100)

        return slider
