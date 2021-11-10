from PySide2 import QtWidgets


class FrontWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.helloLabel = QtWidgets.QLabel("Hello world!")
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.helloLabel)
        self.setLayout(self.layout)
