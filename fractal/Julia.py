import numpy as np
from PySide2.QtCore import QObject, Signal
from fractal.Polynomial import Polynomial


class Julia(QObject):
    progress = Signal(float)

    def __init__(self):
        super().__init__()
        self.numerator = None
        self.denominator = None
        self.C = None
        self.scale = 1.0
        self.offset = np.array([0.0, 0.0])
        self.xyrange = np.array([4.0, 4.0])
        self.max_iterations = 100

    def __str__(self):
        return f"({self.numerator}) / ({self.denominator})"

    def __call__(self, w: int, h: int):
        return self.paint(w, h)

    def setNumerator(self, p: Polynomial):
        self.numerator = p

    def setDenominator(self, p: Polynomial):
        self.denominator = p

    def setC(self, c: complex):
        self.C = c

    def setScale(self, s: float):
        self.scale = s

    def setOffset(self, x: float, y: float):
        self.offset = np.array([x, y])

    def _getColor(self, progress: float):
        return 0.0 if progress >= 1 else np.exp(-progress)

    def _calc(self, start: complex, c: complex):
        # TODO dynamic memory
        n = start
        for i in range(0, self.max_iterations):
            n = self.numerator(n) / self.denominator(n) + c
            R = np.array((n.real, n.imag))
            R = R @ R
            lim = np.sqrt(self.xyrange @ self.xyrange)
            if (R >= lim):
                return self._getColor(i / self.max_iterations)
        return self._getColor(1.0)

    def paint(self, w: int, h: int):
        """Calculate the iterations to escape over max iterations
        and build an array of results:

        J(width, height) = np.array((width, height))
        """
        # TODO progressive image generating
        data = np.zeros((w, h))
        self.progress.emit(0.0)
        scaled_range = self.xyrange / self.scale
        size_array = np.array([w, h])
        offset_poses = np.array([[[x + self.offset[0], y + self.offset[1]] for y in range(0, h)] for x in range(0, w)])
        zs = ((offset_poses / size_array) - np.ones_like(offset_poses) * 0.5) * scaled_range
        
        vec_func = np.vectorize(self._calc)

        data = vec_func(zs, self.C)
        self.progress.emit(1.0)
        return data
