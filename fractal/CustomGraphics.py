from PySide2.QtWidgets import QGraphicsView

class CustomGraphics(QGraphicsView):
    def __init__(self, scene, parent=None):
        super().__init__(scene, parent=parent)
