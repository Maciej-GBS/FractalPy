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

    def setData(self, d: np.array):
        self.data = d
        self.updated.emit(self.toImage())

    def setColormap(self, cmap: Colormap):
        self.colormap = cmap
        self.updated.emit(self.toImage())

    def toImage(self) -> QImage:
        vec_colormap = np.vectorize(self.colormap)
        colors = vec_colormap(self.data)
        im_np = np.transpose(colors, (1, 0, 2)).copy()
        qimage = QImage(
            im_np,
            im_np.shape[1],
            im_np.shape[0],
            QImage.Format_RGB888,
        )
        # TODO improve - remove loops
        return qimage
