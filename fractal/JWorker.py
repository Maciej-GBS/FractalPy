"""JWorker is a QRunnable thread to run Julia.
The goal is to execute multiple threads
each with different target image size.
This allows to progressively improve the image
quality at high performance.
"""
import numpy as np
from PySide2.QtGui import QImage
from PySide2.QtCore import QRunnable, QThreadPool, Signal, Slot, QObject
from fractal.Julia import Julia

from typing import Callable
import traceback
import sys

ThreadPool = QThreadPool()


class JWorker(QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super(JWorker, self).__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

        # Callback will allow access to current progress from outside of the worker
        self.kwargs['progress_callback'] = self.signals.progress

    @Slot()
    def run(self):
        try:
            result = self.fn(*self.args, **self.kwargs,)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)
        finally:
            self.signals.finished.emit()


# * QSignals can only be defined on objects derived from QObject. QRunnable isn't derived from QObject, so we need to define signals outside of it.
class WorkerSignals(QObject):
    """Defines signals available from a running worker thread.

    Args:
        QObject ([type]): [description]
    """
    finished = Signal()
    error = Signal(tuple)
    result = Signal(object)
    progress = Signal(float)
