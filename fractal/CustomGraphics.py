from PySide2.QtGui import QImage, QPixmap
from PySide2.QtCore import Qt, Signal
from PySide2.QtWidgets import QGraphicsView, QAbstractScrollArea, QGraphicsScene


class CustomGraphics(QGraphicsView):
    changeZoom = Signal(float)
    changeOffset = Signal(float, float)

    def __init__(self, scene, parent=None):
        super().__init__(scene, parent)
        self.setCursor(Qt.CrossCursor)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.mousePos = None
        self.image = None

    def getImage(self):
        """Gets the current image.
        If the image does not match the view size a new blank image is returned.

        Returns:
            QtGui.QImage(view.width, view.height, RGB32)
        """
        w,h = self.size().toTuple()
        iw,ih = (-1,-1) if self.image is None else self.image.size().toTuple()
        if iw == w and ih == h:
            return self.image
        else:
            self.image = QImage(w, h, QImage.Format_RGB32)
            return self.image

    def setImage(self, img: QImage):
        self.image = img
        scene = QGraphicsScene()
        scene.addPixmap(QPixmap.fromImage(img))
        self.setScene(scene)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.setCursor(Qt.ClosedHandCursor)
        self.mousePos = (event.x(), event.y())

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        # TODO translate contents with the mouse

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        self.setCursor(Qt.OpenHandCursor)
        dPos = [x - x0 for x0,x in zip(self.mousePos, [event.x(), event.y()])]
        self.mousePos = None
        self.resetTransform()
        self.changeOffset.emit(dPos[0], dPos[1])

    def wheelEvent(self, event):
        super().wheelEvent(event)
        degrees = event.angleDelta().y() / 8.0
        self.changeZoom.emit(degrees / 180.0)
