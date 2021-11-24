import numpy as np


class JTransform:
    def __init__(self):
        self.scale = 1.0
        self.offset = np.array([0.0, 0.0])

    def resized(self, s: float):
        if s == 1.0:
            return self
        r = JTransform()
        r.setScale(self.scale)
        r.offset = self.offset * s
        return r

    def changeOffset(self, x: float, y: float):
        self.offset -= np.array([x, y])

    def setOffset(self, x: float, y: float):
        self.offset = np.array([x, y])

    def setScale(self, s: float):
        self.scale = s
