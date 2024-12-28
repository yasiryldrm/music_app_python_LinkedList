from PyQt5.QtWidgets import QSlider
from PyQt5.QtCore import Qt


class CustomSlider(QSlider):
    def __init__(self, orientation, parent=None):
        super().__init__(orientation, parent)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            # Tıklanan pozisyonu hesapla
            value = self.minimum() + ((self.maximum() - self.minimum()) * event.x()) / self.width()
            self.setValue(round(value))
            # valueChanged sinyalini manuel olarak tetikle
            self.valueChanged.emit(self.value())
        super().mousePressEvent(event)
