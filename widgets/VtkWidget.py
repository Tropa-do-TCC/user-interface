import vtk
import PyQt5.QtWidgets as QtWidgets
from default_parameters import DEFAULT_VTK_WINDOW_TITLE
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor


class VtkWidget:
    def __init__(self, vtk_window, callback_clean_view, parent_grid: QtWidgets.QGridLayout):
        self.wrapper_group_box = QtWidgets.QGroupBox()
        self.wrapper_layout = QtWidgets.QVBoxLayout()
        self.parent_grid = parent_grid
        self.vtk_window = vtk_window

        self.add_vtk_window()
        self.add_reset_view_button(callback_clean_view)

        self.wrapper_group_box.setLayout(self.wrapper_layout)

        self.parent_grid.addWidget(self.wrapper_group_box, 0, 2, 5, 5)
        self.parent_grid.setColumnMinimumWidth(2, 700)

    @staticmethod
    def setup_vtk_window():
        renderer = vtk.vtkRenderer()

        vtk_window = QVTKRenderWindowInteractor()
        interactor = vtk_window.GetRenderWindow().GetInteractor()
        render_window = vtk_window.GetRenderWindow()

        vtk_window.GetRenderWindow().AddRenderer(renderer)
        render_window.AddRenderer(renderer)
        interactor.SetRenderWindow(render_window)
        interactor.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())

        render_window.Render()
        interactor.Initialize()

        return renderer, render_window, vtk_window

    def add_vtk_window(self):
        self.vtk_group_box = QtWidgets.QGroupBox(DEFAULT_VTK_WINDOW_TITLE)
        self.group_box_widget = self.vtk_group_box
        vtk_layout = QtWidgets.QVBoxLayout()
        vtk_layout.addWidget(self.vtk_window)
        self.vtk_group_box.setLayout(vtk_layout)

        self.wrapper_layout.addWidget(self.vtk_group_box)

    def add_reset_view_button(self, callback_clean_view):
        reset_view_button = QtWidgets.QPushButton("Resetar visualização")
        reset_view_button.setFixedSize(150, 30)
        reset_view_button.clicked.connect(callback_clean_view)

        self.wrapper_layout.addWidget(reset_view_button)

    def set_vtk_window_title(self, title):
        self.vtk_group_box.setTitle(title)

    def reset_values(self):
        self.set_vtk_window_title(DEFAULT_VTK_WINDOW_TITLE)
