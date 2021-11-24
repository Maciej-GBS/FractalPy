import numpy as np


class JTransform:
    def __init__(self):
        self.scale = 1.0
        self.offset = np.array([0.0, 0.0])

    def changeOffset(self, x: float, y: float):
        self.offset -= np.array([x, y])

    def setOffset(self, x: float, y: float):
        self.offset = np.array([x, y])

    def setScale(self, s: float):
        self.scale = s
