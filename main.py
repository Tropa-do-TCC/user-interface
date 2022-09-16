import sys
import PyQt5.QtWidgets as QtWidgets
from AppWindow import AppWindow

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    window = AppWindow(app)
    sys.exit(app.exec_())
