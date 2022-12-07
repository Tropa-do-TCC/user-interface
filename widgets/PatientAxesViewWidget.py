import PyQt5.QtWidgets as QtWidgets
from reconstruction.reconstruction import VtkHandler


class PatientAxesViewWidget:
    def __init__(self, vtk_handler: VtkHandler, parent_grid: QtWidgets.QGridLayout):
        self.views_box = QtWidgets.QGroupBox("Visualização")
        self.views_box_layout = QtWidgets.QVBoxLayout()
        self.parent_grid = parent_grid

        self.add_axes_buttons(vtk_handler)

        self.views_box.setLayout(self.views_box_layout)
        self.parent_grid.addWidget(self.views_box, 3, 0, 2, 2)

    def add_axes_buttons(self, vtk_handler):
        # axial view button
        axial_view = QtWidgets.QPushButton("Axial")
        axial_view.clicked.connect(vtk_handler.set_axial_view)
        self.views_box_layout.addWidget(axial_view)

        # coronal view button
        coronal_view = QtWidgets.QPushButton("Coronal")
        coronal_view.clicked.connect(vtk_handler.set_coronal_view)
        self.views_box_layout.addWidget(coronal_view)

        # sagittal view button
        sagittal_view = QtWidgets.QPushButton("Sagittal")
        sagittal_view.clicked.connect(vtk_handler.set_sagittal_view)
        self.views_box_layout.addWidget(sagittal_view)
