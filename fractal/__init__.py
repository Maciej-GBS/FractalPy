import sys
from PySide2 import QtWidgets
from fractal.MainWindow import MainWindow


def main():
    app = QtWidgets.QApplication([])
    app.setApplicationName("Fractal Gen")
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
