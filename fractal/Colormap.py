import numpy as np


class Colormap:
    def __init__(self):
        self.cmap = {
            0.0: np.array([0, 0, 0]),
            0.5: np.array([0, 255, 0]),
            1.0: np.array([255, 255, 255]),
        }

    def __call__(self, v: float):
        return self.apply(v)

    def apply(self, v: float):
        clr = np.zeros(3)
        values = sorted(list(self.cmap.items()))

        for i in range(0, 3):
            clr[i] = np.interp(v, [x[0] for x in values], [y[1][i] for y in values])

        hexclr = clr * np.array([16**4, 16**2, 1])
        return int(hexclr.sum())


def apply_colormap(func, cmap: Colormap):
    def mapped(*args, **kwargs):
        return cmap.apply(func(*args, **kwargs))

    return mapped
