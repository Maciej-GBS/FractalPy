from PySide2.QtGui import QImage, QPixmap, QTransform
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
        self.pix = None
        self.originalT = None

    def scrollContentsBy(self, dx, dy):
        # disable scrolling
        pass

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
        self.pix = scene.addPixmap(QPixmap.fromImage(img))
        self.originalT = self.pix.transform()
        self.setScene(scene)

    def resetPreview(self):
        if self.pix:
            self.pix.resetTransform()

    def getMousePos(self, event):
        return event.pos().toTuple()

    def getMouseDPos(self, event):
        return [x - x0 for x0,x in zip(self.mousePos, self.getMousePos(event))]

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.setCursor(Qt.ClosedHandCursor)
        self.mousePos = self.getMousePos(event)
        if self.pix:
            self.originalT = self.pix.transform()

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        if self.mousePos is not None and self.pix is not None:
            dPos = self.getMouseDPos(event)
            t = QTransform()
            t.translate(dPos[0], dPos[1])
            self.pix.setTransform(self.originalT * t)

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        self.setCursor(Qt.OpenHandCursor)
        dPos = self.getMouseDPos(event)
        self.mousePos = None
        self.changeOffset.emit(*dPos)

    def wheelEvent(self, event):
        super().wheelEvent(event)
        degrees = event.angleDelta().y() / 8.0
        dzoom = degrees / 180.0
        self.changeZoom.emit(dzoom)
        if self.pix:
            center = self.pix.boundingRect().center()
            t = self.pix.transform()
            c1 = t.map(center)
            t *= QTransform.fromScale(1.0 + dzoom, 1.0 + dzoom)
            c2 = t.map(center)
            dcenter = (c1 - c2).toTuple()
            t.translate(*dcenter)
            self.pix.setTransform(t)
