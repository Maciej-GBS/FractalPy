import numpy as np


class Colormap:
    def __init__(self):
        self.cmap = {0.0:0xFF0000, 0.5:0x0000FF, 1.0:0xFFFFFF}

    def __call__(self, v: float):
        return self.apply(v)

    def apply(self, v: float):
        d = np.array([[x,y] for (x,y) in self.cmap.items()]).T
        return np.interp(v, d[0], d[1])

def apply_colormap(func, cmap: Colormap):
    def mapped(*args, **kwargs):
        return cmap.apply(func(*args, **kwargs))
    return mapped
