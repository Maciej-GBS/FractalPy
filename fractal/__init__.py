import sys
from PySide2 import QtCore, QtWidgets, QtGui
from fractal.FrontWidget import FrontWidget

def main():
    app = QtWidgets.QApplication([])
    widget = FrontWidget()
    widget.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
