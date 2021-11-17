"""JWorker is a QRunnable thread to run Julia.
The goal is to execute multiple threads
each with different target image size.
This allows to progressively improve the image
quality at high performance.
"""
import numpy as np
from PySide2.QtGui import QImage
from PySide2.QtCore import QRunnable, QThreadPool, Signal, Slot
from fractal.Julia import Julia


ThreadPool = QThreadPool()

class JWorker(QRunnable):
    finished = Signal(QImage, int)

    def __init__(self):
        super().__init__()

    @Slot()
    def run(self):
        # TODO execute Julia paint
        job_id = 0
        result = None
        self.finished.emit(result, job_id)
