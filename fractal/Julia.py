import numpy as np
from PySide2.QtCore import QObject, Signal
from fractal.Polynomial import Polynomial


class Julia(QObject):
    progress = Signal(float)

    def __init__(self):
        super().__init__()
        self._memory = {}
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

    def _memkey(self, k: complex):
        return str(round(k.real, 12)) + str(round(k.imag, 12))

    def _calc(self, start: complex):
        l1key = self._memkey(self.C)
        l2key = self._memkey(start)
        if self._memory.get(l1key):
            if self._memory[l1key].get(l2key):
                self._ctr_hit += 1
                return self._memory[l1key][l2key]
        else:
            self._memory[l1key] = {}
        self._ctr_miss += 1
        n = start
        for i in range(0, self.max_iterations):
            n = self.numerator(n) / self.denominator(n) + self.C
            R = np.array((n.real, n.imag))
            R = R @ R
            lim = np.sqrt(self.xyrange @ self.xyrange)
            if (R >= lim):
                result = self._getColor(i / self.max_iterations)
                self._memory[l1key][l2key] = result
                return result
        result = self._getColor(1.0)
        self._memory[l1key][l2key] = result
        return result

    def paint(self, w: int, h: int):
        """Calculate the iterations to escape over max iterations
        and build an array of results:

        J(width, height) = np.array((width, height))
        """
        # TODO progressive image generating
        data = np.zeros((w, h))
        self._ctr_hit = 0
        self._ctr_miss = 0
        self.progress.emit(0.0)
        for y in range(0,h):
            for x in range(0,w):
                scaled_range = self.xyrange / self.scale
                offset_pos = np.array([x, y]) + self.offset
                z = ((offset_pos / np.array([w, h])) - 0.5) * scaled_range
                data[x][y] = self._calc(complex(*z))
            self.progress.emit(y / h)
        self.progress.emit(1.0)
        print(f"hits={self._ctr_hit}\tmiss={self._ctr_miss}")
        return data
