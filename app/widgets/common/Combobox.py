import PyQt5.QtWidgets as QtWidgets


class Combobox(QtWidgets.QComboBox):
    def __init__(self, label, items, default_value, parent=None):
        super().__init__(parent)

        self.current_value = self.default_value = default_value

        self.label_instance = QtWidgets.QLabel(label)

        [self.addItem(item) for item in items]

        self.activated[str].connect(self.change_callback)

    def reset_combobox(self):
        self.setCurrentText(self.default_value)

    def change_callback(self):
        self.current_value = self.currentText()
