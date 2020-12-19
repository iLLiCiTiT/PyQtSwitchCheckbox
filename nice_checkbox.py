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

        # Draw checker
        self._paint_checker(painter, checkbox_rect)
        painter.end()

    def _paint_checker(self, painter, checkbox_rect):
        size = checkbox_rect.height()

        area_width = checkbox_rect.width() - size
        pos_x = checkbox_rect.x()
        if self._checked:
            pos_x += area_width

        pos_y = checkbox_rect.y() + 1

        checker_rect = QtCore.QRect(pos_x, pos_y, size, size)

        radius = floor(size / 2)

        path = QtGui.QPainterPath()
        path.addRoundedRect(checker_rect, radius, radius)

        gradient = QtGui.QRadialGradient(
            checker_rect.center(), checker_rect.width() / 2
        )
        gradient.setColorAt(0, QtCore.Qt.white)
        gradient.setColorAt(0.8, QtCore.Qt.white)
        gradient.setColorAt(0.85, QtCore.Qt.transparent)

        painter.fillPath(path, gradient)
