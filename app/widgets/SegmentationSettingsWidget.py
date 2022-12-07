import PyQt5.QtWidgets as QtWidgets
from vtkFeatures.VtkHandler import VtkHandler

from app.widgets.common.Combobox import Combobox
from app.widgets.common.Slider import Slider

from default_parameters import DEFAULT_SEGMENTATION_ALG, DEFAULT_SEGMENTATION_DIMENSION, DEFAULT_SEGMENTATION_DIMENSION_LABEL, DEFAULT_SEGMENTATION_ENTROPY, DEFAULT_SEGMENTATION_ENTROPY_LABEL, DEFAULT_SEGMENTATION_GAMA, DEFAULT_SEGMENTATION_GAMA_LABEL


class SegmentationSettingsWidget:
    def __init__(self, vtk_handler: VtkHandler, parent_grid: QtWidgets.QGridLayout):
        self.group_box = QtWidgets.QGroupBox("Segmentação")
        self.group_layout = QtWidgets.QGridLayout()
        self.parent_grid = parent_grid

        self.add_algorithm_combobox()
        self.add_entropy_slider()
        self.add_dimension_slider()
        self.add_gama_slider()
        self.add_segmentation_button(vtk_handler)

        self.group_box.setLayout(self.group_layout)
        self.parent_grid.addWidget(self.group_box, 1, 0, 1, 2)

    def add_algorithm_combobox(self):
        self.algorithm_combobox = Combobox(
            label="Algoritmo",
            items=['FFA', 'KH', 'CS', 'ABC', 'EHO'],
            default_value=DEFAULT_SEGMENTATION_ALG,
        )

        self.group_layout.addWidget(
            self.algorithm_combobox.label_instance, 0, 0)

        self.group_layout.addWidget(
            self.algorithm_combobox, 0, 1, 1, 2)

    def add_entropy_slider(self):
        self.entropy_slider = Slider(
            values=[-2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2],
            default_value=DEFAULT_SEGMENTATION_ENTROPY,
            default_label=DEFAULT_SEGMENTATION_ENTROPY_LABEL,
        )

        self.group_layout.addWidget(
            self.entropy_slider.label_instance, 1, 0)
        self.group_layout.addWidget(
            self.entropy_slider, 1, 1, 1, 2)

    def add_dimension_slider(self):
        self.dimension_slider = Slider(
            values=range(1, 6),
            default_value=DEFAULT_SEGMENTATION_DIMENSION,
            default_label=DEFAULT_SEGMENTATION_DIMENSION_LABEL,
        )

        self.group_layout.addWidget(
            self.dimension_slider.label_instance, 2, 0)
        self.group_layout.addWidget(
            self.dimension_slider, 2, 1, 1, 2)

    def add_gama_slider(self):
        self.gama_slider = Slider(
            values=[1, 1.3, 1.5, 1.7],
            default_value=DEFAULT_SEGMENTATION_GAMA,
            default_label=DEFAULT_SEGMENTATION_GAMA_LABEL,
        )

        self.group_layout.addWidget(
            self.gama_slider.label_instance, 3, 0)
        self.group_layout.addWidget(
            self.gama_slider, 3, 1, 1, 2)

    def add_segmentation_button(self, vtk_handler: VtkHandler):
        self.segmentate_button = QtWidgets.QPushButton("Segmentar")
        self.segmentate_button.clicked.connect(lambda _: vtk_handler.setup_segmented_skull(
            entropy=self.entropy_slider.current_value,
            bioinspired=self.algorithm_combobox.current_value,
            dimension=self.dimension_slider.current_value,
            gama=self.gama_slider.current_value
        ))

        self.group_layout.addWidget(self.segmentate_button, 4, 0, 1, 3)

        # Turn visible after skull import
        self.segmentate_button.setHidden(True)

    def reset_values(self):
        self.algorithm_combobox.reset_combobox()
        self.entropy_slider.reset_slider()
        self.gama_slider.reset_slider()
        self.dimension_slider.reset_slider()
        self.segmentate_button.setHidden(True)
