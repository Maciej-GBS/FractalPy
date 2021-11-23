import numpy as np
from PySide2.QtGui import QImage
from PySide2.QtCore import QObject, Signal
from fractal.Colormap import Colormap


class ArrayImage(QObject):
    updated = Signal(QImage)

    def __init__(self):
        super().__init__()
        self.colormap = Colormap()
        self.data = np.array([])

    def change(self):
        self.updated.emit(self.toImage())

    def setData(self, d: np.array):
        self.data = d
        self.change()

    def setColormap(self, cmap: Colormap):
        self.colormap = cmap
        self.change()

    def toImage(self) -> QImage:
        w, h = self.data.shape
        image = QImage(w, h, QImage.Format_RGB32)
        # TODO improve - remove loops
        # see qtforpython-5 reading and writing image files
        for x in range(0, w):
            for y in range(0, h):
                color = self.colormap(self.data[x][y])
                image.setPixel(x, y, color)
        return image
