import numpy as np
from PySide2 import QtCore, QtGui, QtWidgets
from fractal.CustomGraphics import CustomGraphics
from fractal.ArrayImage import ArrayImage
from fractal.Julia import Julia
from fractal.Polynomial import Polynomial
from fractal.ColormapWidget import ColormapWidget



class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.j = Julia()
        self.image = ArrayImage()
        self.layout_object = MainWindowLayout(self)
        self.layout_object.setupUi()
        self.setupSignals()

    def setZoom(self, z: float):
        self.layout_object.zoomSpin.setValue(z)

    def setupSignals(self):
        lo = self.layout_object
        lo.savButton.clicked.connect(self.exportImageAs)
        lo.genButton.clicked.connect(self.updateImage)
        lo.colorButton.clicked.connect(self.editColormap)
        lo.resetButton.clicked.connect(self.reset)
        lo.zoomSpin.valueChanged[float].connect(self.zoomChanged)
        lo.graphicsView.changeZoom.connect(self.changeZoom)
        lo.graphicsView.changeOffset.connect(self.changeOffset)
        self.j.progress.connect(self.updateProgress)
        self.image.updated.connect(self.imageUpdated)

    def updateJulia(self):
        f = self.layout_object.fText.toPlainText()
        g = self.layout_object.gText.toPlainText()
        r = float(self.layout_object.rSpin.value())
        fi = (
            2
            * np.pi
            * self.layout_object.fiSlider.value()
            / self.layout_object.fiSlider.maximum()
        )
        self.j.max_iterations = self.layout_object.iterSpin.value()
        self.j.setNumerator(Polynomial(f))
        self.j.setDenominator(Polynomial(g))
        self.j.setC(complex(r * np.cos(fi), r * np.sin(fi)))

    def status(self, text: str):
        self.layout_object.statusbar.showMessage(text)

    def updateImage(self):
        self.updateJulia()
        dim = self.layout_object.graphicsView.size().toTuple()
        self.image.setData(self.j(*dim))

    def imageUpdated(self, new_img):
        self.layout_object.graphicsView.setImage(new_img)

    def changeOffset(self, x: float, y: float):
        off = self.j.offset - np.array([x, y])
        self.j.setOffset(*off)
        # self.updateImage()

    def changeZoom(self, dz: float):
        self.setZoom(self.layout_object.zoomSpin.value() * dz)

    def updateProgress(self, p: float):
        self.layout_object.progressBar.setValue(int(p * 100))

    def editColormap(self):
        # TODO show ColormapWidget
        dlg = QtWidgets.QDialog(self)
        layout = QtWidgets.QVBoxLayout(dlg)
        layout.addWidget(ColormapWidget(self.image.colormap))
        dlg.setLayout(layout)
        dlg.exec()

    def reset(self):
        self.setZoom(1.0)
        self.j.setOffset(0.0, 0.0)
        self.layout_object.graphicsView.resetPreview()

    def zoomChanged(self, d: float):
        self.j.setScale(d)
        # self.updateImage()

    def exportImageAs(self):
        # TODO open save as dialog and export image
        raise NotImplementedError


class MainWindowLayout(object):
    def __init__(self, owner: MainWindow):
        super().__init__()
        self.owner = owner

    def setupUi(self):
        self.owner.setWindowTitle("Fractal Generator")
        self.owner.setObjectName("MainWindow")
        self.owner.resize(944, 697)
        self.centralwidget = QtWidgets.QWidget(self.owner)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.setStyleSheet("border-bottom: 1px solid black")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setColumnStretch(1, 6)
        self.populateWidgets()
        self.setTabOrder()
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.owner.setCentralWidget(self.centralwidget)
        self.addStatusBar()

    def addStatusBar(self):
        self.statusbar = QtWidgets.QStatusBar(self.owner)
        self.statusbar.setObjectName("statusbar")
        self.statusbar.showMessage("Click generate to start...")
        self.owner.setStatusBar(self.statusbar)

    def addMenuBar(self):
        # NOTE this is unused code but left for potential improvement
        self.menubar = QtWidgets.QMenuBar(self.owner)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 944, 25))
        self.menubar.setObjectName("menubar")
        self.owner.setMenuBar(self.menubar)

    def populateWidgets(self):
        self.savButton = QtWidgets.QPushButton(self.centralwidget)
        self.savButton.setObjectName("savButton")
        self.savButton.setText("Export as")
        self.gridLayout.addWidget(self.savButton, 0, 0, 1, 1)

        self.genButton = QtWidgets.QPushButton(self.centralwidget)
        self.genButton.setObjectName("genButton")
        self.genButton.setText("Generate")
        self.gridLayout.addWidget(self.genButton, 1, 0, 1, 1)

        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.label_2.setText("Grading:")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)

        self.iterSpin = QtWidgets.QSpinBox(self.centralwidget)
        self.iterSpin.setMinimum(10)
        self.iterSpin.setMaximum(100000000)
        self.iterSpin.setSingleStep(10)
        self.iterSpin.setValue(100)
        self.iterSpin.setObjectName("iterSpin")
        self.gridLayout.addWidget(self.iterSpin, 3, 0, 1, 1)

        self.colorButton = QtWidgets.QPushButton(self.centralwidget)
        self.colorButton.setObjectName("colorButton")
        self.colorButton.setText("Colormap...")
        self.gridLayout.addWidget(self.colorButton, 4, 0, 1, 1)

        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.label_3.setText("Zoom:")
        self.gridLayout.addWidget(self.label_3, 5, 0, 1, 1)

        self.zoomSpin = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.zoomSpin.setDecimals(4)
        self.zoomSpin.setMinimum(0.0001)
        self.zoomSpin.setMaximum(10000000000.0)
        self.zoomSpin.setSingleStep(0.1)
        self.zoomSpin.setValue(1.0)
        self.zoomSpin.setObjectName("zoomSpin")
        self.gridLayout.addWidget(self.zoomSpin, 6, 0, 1, 1)

        self.resetButton = QtWidgets.QPushButton(self.centralwidget)
        self.resetButton.setObjectName("resetButton")
        self.resetButton.setText("Reset")
        self.gridLayout.addWidget(self.resetButton, 7, 0, 1, 1)

        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setObjectName("label_4")
        self.label_4.setText("Constant FI:")
        self.gridLayout.addWidget(self.label_4, 8, 0, 1, 1)

        self.fiSlider = QtWidgets.QSlider(self.centralwidget)
        self.fiSlider.setMinimum(0)
        self.fiSlider.setMaximum(1000)
        self.fiSlider.setOrientation(QtCore.Qt.Horizontal)
        self.fiSlider.setObjectName("fiSlider")
        self.gridLayout.addWidget(self.fiSlider, 9, 0, 1, 1)

        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setObjectName("label_5")
        self.label_5.setText("Constant R:")
        self.gridLayout.addWidget(self.label_5, 10, 0, 1, 1)

        self.rSpin = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.rSpin.setDecimals(4)
        self.rSpin.setMaximum(10000.0)
        self.rSpin.setSingleStep(0.1)
        self.rSpin.setValue(1.0)
        self.rSpin.setObjectName("rSpin")
        self.gridLayout.addWidget(self.rSpin, 11, 0, 1, 1)

        self.fText = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.fText.setMinimumSize(QtCore.QSize(0, 0))
        self.fText.setObjectName("fText")
        self.fText.setPlainText("1x^2")
        self.gridLayout.addWidget(self.fText, 12, 0, 1, 1)

        self.gText = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.gText.setObjectName("gText")
        self.gText.setPlainText("1")
        self.gridLayout.addWidget(self.gText, 13, 0, 1, 1)

        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setValue(100)
        self.progressBar.setObjectName("progressBar")
        self.gridLayout.addWidget(self.progressBar, 14, 0, 1, 1)

        self.graphicsView = CustomGraphics(self.centralwidget)
        self.graphicsView.setCursor(QtCore.Qt.OpenHandCursor)
        self.graphicsView.setObjectName("graphicsView")
        self.gridLayout.addWidget(self.graphicsView, 0, 1, 15, 1)

    def setTabOrder(self):
        self.owner.setTabOrder(self.savButton, self.genButton)
        self.owner.setTabOrder(self.genButton, self.iterSpin)
        self.owner.setTabOrder(self.iterSpin, self.colorButton)
        self.owner.setTabOrder(self.colorButton, self.zoomSpin)
        self.owner.setTabOrder(self.zoomSpin, self.resetButton)
        self.owner.setTabOrder(self.resetButton, self.fiSlider)
        self.owner.setTabOrder(self.fiSlider, self.rSpin)
        self.owner.setTabOrder(self.rSpin, self.fText)
        self.owner.setTabOrder(self.fText, self.gText)
        self.owner.setTabOrder(self.gText, self.graphicsView)
