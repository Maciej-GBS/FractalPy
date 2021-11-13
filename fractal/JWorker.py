import numpy as np
from PySide2.QtGui import QImage
from PySide2.QtCore import QRunnable, QThreadPool, Signal, Slot
from fractal.Julia import Julia


ThreadPool = QThreadPool()

class JWorker(QRunnable):
    finished = Signal(QImage)

    def __init__(self):
        super().__init__()

    @Slot()
    def run(self):
        pass
