import numpy as np
from PySide2.QtGui import QImage
from PySide2.QtCore import QObject, Signal, Slot
from fractal.Polynomial import Polynomial
from fractal.Colormap import Colormap


class Julia(QObject):
    progress = Signal(float)

    def __init__(self):
        super().__init__()
        self.numerator = None
        self.denominator = None
        self.C = None
        self.limits = np.array([4.0, 4.0])
        self.max_iterations = 100
        self.colormap = Colormap()

    def __str__(self):
        return f"({self.numerator}) / ({self.denominator})"

    def setNumerator(self, p: Polynomial):
        self.numerator = p

    def setDenominator(self, p: Polynomial):
        self.denominator = p

    def setC(self, c: complex):
        self.C = c

    def _getColor(self, progress: float):
        if (progress >= 1):
            return self.colormap(0.0)
        else:
            return self.colormap(np.exp(-progress))

    def _calc(self, start: complex, c: complex):
        n = start
        for i in range(0, self.max_iterations):
            n = self.numerator(n) / self.denominator(n) + c
            R = np.array((n.real, n.imag))
            R = R @ R
            lim = np.sqrt(self.limits @ self.limits)
            if (R >= lim):
                return self._getColor(i / self.max_iterations)
        return self._getColor(1.0)

    def paint(self, img: QImage):
        # TODO progressive image generating
        w = img.width()
        h = img.height()
        self.progress.emit(0.0)
        for y in range(0,h):
            for x in range(0,w):
                # TODO translation and zoom
                z = self.limits * np.array([x/w, y/h])
                img.setPixel(x, y, self._calc(complex(*z), self.C))
            self.progress.emit(y / h)
        self.progress.emit(1.0)
        return img
