import numpy as np
from PySide2 import QtWidgets
from fractal import ArrayImage


class ColormapWidget(QtWidgets.QWidget):
    def __init__(self, img: ArrayImage, parent=None):
        super().__init__(parent)
        self.img = img
        self.colormap = img.colormap

        # Return first key-val pair
        self.colormap_start = lambda: sorted(list(self.colormap.cmap.items()))[0]
        self.colormap_mid = lambda: sorted(list(self.colormap.cmap.items()))[1]
        self.colormap_stop = lambda: sorted(list(self.colormap.cmap.items()))[2]

        self.helloLabel = QtWidgets.QLabel("Pick colors for the colormap")

        self.startColorButton = QtWidgets.QPushButton()
        self.startColorButton.clicked.connect(
            lambda: self.set_color_stop(
                stop_key=self.colormap_start()[0],
            ),
        )

        self.midColorButton = QtWidgets.QPushButton()
        self.midColorButton.clicked.connect(
            lambda: self.set_color_stop(
                stop_key=self.colormap_mid()[0],
            ),
        )

        self.stopColorButton = QtWidgets.QPushButton()
        self.stopColorButton.clicked.connect(
            lambda: self.set_color_stop(
                stop_key=self.colormap_stop()[0],
            ),
        )

        self._set_button_labels()

        self.layout = QtWidgets.QGridLayout(self)
        self.layout.addWidget(self.helloLabel, 0, 0, 1, 1)
        self.layout.addWidget(self.startColorButton, 1, 0, 1, 1)
        self.layout.addWidget(self.midColorButton, 1, 1, 1, 1)
        self.layout.addWidget(self.stopColorButton, 1, 2, 1, 1)
        self.setLayout(self.layout)

    def set_color_stop(self, stop_key: float):
        color = QtWidgets.QColorDialog.getColor()
        # print(int(color.name()[1:], 16))
        self.colormap.cmap[stop_key] = np.array([color.r, color.g, color.b])
        self._set_button_labels()
        self.img.change()

    def _set_button_labels(self):
        self.startColorButton.setText(f"Color at value: {self.colormap_start()[0]}\n#{f'{self.colormap_start()[1]:06x}':^7}")
        self.midColorButton.setText(f"Color at value: {self.colormap_mid()[0]}\n#{f'{self.colormap_mid()[1]:06x}':^7}")
        self.stopColorButton.setText(f"Color at value: {self.colormap_stop()[0]}\n#{f'{self.colormap_stop()[1]:06x}':^7}")
