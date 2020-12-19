from math import floor
from Qt import QtWidgets, QtCore, QtGui


class NiceCheckbox(QtWidgets.QFrame):
    def __init__(self, parent=None):
        super(NiceCheckbox, self).__init__(parent)
        self._checked = True

        self.checked_color = QtGui.QColor(67, 181, 129)
        self.unchecked_color = QtGui.QColor(114, 118, 125)

    def setChecked(self, checked):
        if checked == self._checked:
            return
        self._checked = checked

    def sizeHint(self):
        return QtCore.QSize(100, 50)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)

        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        checkbox_rect = QtCore.QRect(event.rect())

        # Draw inner background
        bg_color = self.unchecked_color

        if checkbox_rect.width() > checkbox_rect.height():
            size = checkbox_rect.height()
        else:
            size = checkbox_rect.width()
        radius = floor(size / 2)

        painter.setPen(QtCore.Qt.transparent)
        painter.setBrush(bg_color)
        painter.drawRoundedRect(checkbox_rect, radius, radius)

        painter.end()
