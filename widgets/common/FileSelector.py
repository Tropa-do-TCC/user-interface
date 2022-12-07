import PyQt5.QtCore as Qt
import PyQt5.QtWidgets as QtWidgets


class FileSelector(QtWidgets.QPushButton):
    def __init__(self, label, window_title, name_filter, load_callback):
        super().__init__(label)
        self.clicked.connect(
            lambda _: self.open_file(window_title, name_filter, load_callback))

    def open_file(self, window_title, name_filter, load_callback):
        dialog = QtWidgets.QFileDialog(self)

        dialog.setWindowTitle(window_title)

        dialog.setNameFilter(name_filter)
        dialog.setDirectory(Qt.QDir.currentPath())
        dialog.setFileMode(QtWidgets.QFileDialog.ExistingFile)

        if dialog.exec_():
            selected_file = dialog.selectedFiles()[0]
            load_callback(selected_file)
