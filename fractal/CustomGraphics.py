from PySide2.QtCore import Qt
from PySide2.QtWidgets import QGraphicsView


class CustomGraphics(QGraphicsView):
    def __init__(self, scene, parent=None):
        super().__init__(scene, parent)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.setCursor(Qt.ClosedHandCursor)
        self.mousePos = (event.x(), event.y())

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        self.setCursor(Qt.OpenHandCursor)
        dPos = [x - x0 for x0,x in zip(self.mousePos, [event.x(), event.y()])]
        # TODO reposition graphic
