import PyQt5.QtWidgets as QtWidgets
from reconstruction.reconstruction import VtkHandler

from widgets.common.DirectorySelector import DirectorySelector
from widgets.common.FileSelector import FileSelector
from widgets.common.Slider import Slider


class SkullSettingsWidget:
    def __init__(self, import_skull_callback, vtk_handler: VtkHandler, parent_grid: QtWidgets.QGridLayout):
        self.group_box = QtWidgets.QGroupBox("Crânio")
        self.group_layout = QtWidgets.QGridLayout()
        self.parent_grid = parent_grid

        self.add_dicom_dir_selector(import_skull_callback)
        self.add_nifti_file_selector(import_skull_callback)
        self.add_skull_opacity_slider(vtk_handler)
        self.group_box.setLayout(self.group_layout)
        self.parent_grid.addWidget(self.group_box, 0, 0, 1, 2)

    def add_dicom_dir_selector(self, import_skull_callback):
        self.dicom_dir_selector = DirectorySelector(
            label="Selecionar DICOMDIR",
            window_title='Selecionar diretório de tomografias',
            load_callback=import_skull_callback
        )
        self.group_layout.addWidget(self.dicom_dir_selector, 1, 0, 1, 3)

    def add_nifti_file_selector(self, import_skull_callback):
        self.nifti_file_selector = FileSelector(
            label="Selecionar arquivo NIFTI",
            window_title='Selecionar arquivo NIFTI',
            name_filter='Arquivos nii.gz (*.nii.gz)',
            load_callback=import_skull_callback
        )
        self.group_layout.addWidget(self.nifti_file_selector, 2, 0, 1, 3)

    def add_skull_opacity_slider(self, vtk_handler: VtkHandler):
        self.skull_opacity_slider = Slider(
            values=range(0, 101),
            default_value=1,
            default_label="Opacidade",
            show_value=False,
            callback=vtk_handler.set_skull_opacity
        )

        self.group_layout.addWidget(
            self.skull_opacity_slider.label_instance, 3, 0)
        self.group_layout.addWidget(self.skull_opacity_slider, 3, 1, 1, 2)

        # Turn visible after skull import
        self.skull_opacity_slider.label_instance.setHidden(True)
        self.skull_opacity_slider.setHidden(True)

    def reset_values(self):
        self.skull_opacity_slider.reset_slider()
        self.skull_opacity_slider.label_instance.setHidden(True)
        self.skull_opacity_slider.setHidden(True)
