import sys
from PySide6 import QtCore, QtWidgets, QtGui
import fractal.FrontWidget

def main():
    app = QtWidgets.QApplication([])
    widget = FrontWidget()
    widget.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
