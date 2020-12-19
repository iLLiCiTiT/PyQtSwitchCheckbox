from math import floor
from Qt import QtWidgets, QtCore, QtGui


class NiceCheckbox(QtWidgets.QFrame):
    def __init__(self, parent=None):
        super(NiceCheckbox, self).__init__(parent)
        self._pressed = False
        self._checked = True
        self._under_mouse = False


        self.checked_color = QtGui.QColor(67, 181, 129)
        self.unchecked_color = QtGui.QColor(114, 118, 125)

    def setChecked(self, checked):
        if checked == self._checked:
            return
        self._checked = checked

    def sizeHint(self):
        return QtCore.QSize(100, 50)

    def mousePressEvent(self, event):
        if event.buttons() & QtCore.Qt.LeftButton:
            self._pressed = True
        super(NiceCheckbox, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if self._pressed and not event.buttons() & QtCore.Qt.LeftButton:
            self._pressed = False
        super(NiceCheckbox, self).mouseReleaseEvent(event)

    def enterEvent(self, event):
        self._under_mouse = True
        super(NiceCheckbox, self).enterEvent(event)

    def leaveEvent(self, event):
        self._under_mouse = False
        super(NiceCheckbox, self).leaveEvent(event)

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

        if not self.isEnabled():
            level = 33
            alpha = 127
            painter.setBrush(QtGui.QColor(level, level, level, alpha))
            painter.drawRoundedRect(checkbox_rect, radius, radius)

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
        if self._under_mouse:
            if self._pressed:
                gradient.setColorAt(0.75, QtCore.Qt.white)
                gradient.setColorAt(0.8, QtGui.QColor(0, 0, 0, 77))
                gradient.setColorAt(0.9, QtCore.Qt.transparent)
            else:
                gradient.setColorAt(0.8, QtCore.Qt.white)
                gradient.setColorAt(0.85, QtCore.Qt.transparent)
        else:
            gradient.setColorAt(0.75, QtCore.Qt.white)
            gradient.setColorAt(0.8, QtCore.Qt.transparent)

        painter.fillPath(path, gradient)
