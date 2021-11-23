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

from typing import Callable

ThreadPool = QThreadPool()


class JWorker(QRunnable):

    def __init__(self):
        super().__init__()
        self.job_id = 0
        self.finished = Signal(QImage, int)

    @Slot()
    def run(
        self,
        func: Callable,
        *args,
    ):
        self.job_id += 1
        result = func(*args)
        self.finished.emit(result, self.job_id)
