from PySide2.QtGui import QImage, QPixmap
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QGraphicsView, QAbstractScrollArea, QGraphicsScene


class CustomGraphics(QGraphicsView):
    def __init__(self, scene, parent=None):
        super().__init__(scene, parent)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def getImage(self):
        w,h = self.size().toTuple()
        return QImage(w, h, QImage.Format_RGB32)

    def setImage(self, img: QImage):
        scene = QGraphicsScene()
        scene.addPixmap(QPixmap.fromImage(img))
        self.setScene(scene)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.setCursor(Qt.ClosedHandCursor)
        self.mousePos = (event.x(), event.y())

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        self.setCursor(Qt.OpenHandCursor)
        dPos = [x - x0 for x0,x in zip(self.mousePos, [event.x(), event.y()])]
        # TODO reposition graphic
