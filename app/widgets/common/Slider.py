import PyQt5.QtCore as Qt
import PyQt5.QtWidgets as QtWidgets


class Slider(QtWidgets.QSlider):
    def __init__(self, values, default_label, default_value, custom_callback=None, show_value=True, parent=None):
        super().__init__(parent)
        self.setOrientation(Qt.Qt.Horizontal)

        self.show_value = show_value
        self.values = values

        self.setRange(0, len(values) - 1)
        self.setTickInterval(1)

        self.current_value = self.default_value = default_value
        self.setValue(int(self.default_value))

        self.default_label = default_label

        label_text = f"{self.default_label} -> {self.default_value}" if show_value else default_label
        self.label_instance = QtWidgets.QLabel(label_text)

        callback = self.change_callback if custom_callback is None else custom_callback

        self.valueChanged.connect(lambda index: callback(values[index]))

    def set_label(self, value):
        self.label_instance.setText(f"{self.default_label} -> {value}")

    def reset_slider(self):
        self.set_label(self.default_value)
        self.current_value = self.default_value

    def change_callback(self, value):
        if self.show_value:
            self.set_label(value)
        self.current_value = value
