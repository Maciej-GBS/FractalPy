import numpy as np
from PySide2.QtGui import QColor


class Colormap:
    def __init__(self):
        self.cmap = {
            0.0: 0x000000,
            0.5: 0x00ff00,
            1.0: 0xffffff,
        }

    def __call__(self, v: float) -> QColor:
        return self.apply(v)

    def apply(self, v: float) -> QColor:
        values = sorted(list(self.cmap.items()))

        clr = np.interp(v, [x[0] for x in values], [y[1] for y in values])

        return QColor.fromRgb(int(clr))


def apply_colormap(func, cmap: Colormap):
    def mapped(*args, **kwargs):
        return cmap.apply(func(*args, **kwargs))

    return mapped
