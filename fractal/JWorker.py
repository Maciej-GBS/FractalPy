import numpy as np
from PySide2.QtGui import QImage
from PySide2.QtCore import QObject, Signal, Slot
from fractal.Julia import Julia


class JWorker(QObject):
    finished = Signal(QImage)

    def __init__(self):
        super().__init__()
