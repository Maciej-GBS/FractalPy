import numpy as np
from fractal.Polynomial import Polynomial


class Julia:
    def __init__(self):
        self.numerator = None
        self.denominator = None
        self.limits = np.array([4.0, 4.0])

    def __str__(self):
        return f"({self.numerator}) / ({self.denominator})"

    def setNumerator(self, p: Polynomial):
        self.numerator = p

    def setDenominator(self, p: Polynomial):
        self.denominator = p

    def _getColor(self, progress: float):
        if (progress >= 1):
            return 0.0
        else:
            return np.exp(-progress)

    def _calc(self, iterations: int, start: complex, c: complex):
        n = start
        for i in range(0, iterations):
            n = self.numerator(n) / self.denominator(n) + c
            R = np.array((n.real, n.imag))
            R = R @ R
            lim = np.sqrt(self.limits @ self.limits)
            if (R >= lim):
                return self._getColor()
        return self._getColor(1.0)
