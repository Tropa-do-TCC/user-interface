import PyQt5.QtCore as Qt
import PyQt5.QtWidgets as QtWidgets


class DirectorySelector(QtWidgets.QPushButton):
    def __init__(self, label, window_title, load_callback):
        super().__init__(label)

        self.clicked.connect(
            lambda _: self.open_directory(window_title, label, load_callback))

    def open_directory(self, window_title, label, load_callback):
        dialog = QtWidgets.QFileDialog(self)

        dialog.setWindowTitle(window_title)
        dialog.setDirectory(Qt.QDir.currentPath())

        directory_path = QtWidgets.QFileDialog.getExistingDirectory(
            self, label)

        if directory_path:
            load_callback(directory_path)
