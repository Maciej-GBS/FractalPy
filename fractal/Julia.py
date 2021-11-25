import numpy as np
from PySide2.QtCore import QObject, Signal
from fractal.JTransform import JTransform
from fractal.Polynomial import Polynomial

from typing import Callable
import time


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

    def setTransform(self, t: JTransform):
        self.scale = float(t.scale)
        self.offset = np.copy(t.offset)

    def _getColor(self, progress: float):
        return 0.0 if progress >= 1 else np.exp(-progress)

    def _calc(self, start: complex, c: complex):
        lim = np.sqrt(self.xyrange @ self.xyrange)
        min_delta = 0.1 * lim / self.max_iterations
        Rp = 0.0
        dR = 2 * min_delta
        n = start
        for i in range(0, self.max_iterations):
            n = self.numerator(n) / self.denominator(n) + c
            R = np.array((n.real, n.imag))
            R = R @ R
            dR = 0.5 * dR + 0.5 * abs(R - Rp)
            if dR < min_delta:
                break
            Rp = R
            if R >= lim:
                return self._getColor(i / self.max_iterations)
        return self._getColor(1.0)

    def paint(self, w: int, h: int, progress_callback: Callable = None):
        """Calculate the iterations to escape over max iterations
        and build an array of results:

        J(width, height) = np.array((width, height))
        """
        _timer_start = time.time()
        data = np.zeros((w, h))
        scaled_range = self.xyrange / self.scale
        size_array = np.array([w, h])
        self.progress.emit(0.0)
        progress_callback.emit(0.0)
        for y in range(0, h):
            for x in range(0, w):
                offset_pos = np.array([x, y]) + self.offset
                z = ((offset_pos / size_array) - 0.5) * scaled_range
                data[x][y] = self._calc(complex(*z), self.C)
            self.progress.emit(y / h)
            progress_callback.emit(y / h)
        self.progress.emit(1.0)
        progress_callback.emit(1.0)
        _timer_end = time.time()
        _delta_t = _timer_end - _timer_start
        print(f"{size_array} => {_delta_t}")
        return data
