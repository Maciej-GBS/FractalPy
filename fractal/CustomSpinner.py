from PySide2.QtWidgets import QSpinBox

class CustomSpinner(QSpinBox):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
