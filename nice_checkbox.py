from math import floor
from Qt import QtWidgets, QtCore, QtGui


class NiceCheckbox(QtWidgets.QFrame):
    def __init__(self, checked=True, parent=None):
        super(NiceCheckbox, self).__init__(parent)
        self._pressed = False
        self._checked = checked
        self._under_mouse = False

        self._current_step = None
        self._steps = 10
        self.set_steps(self._steps)

        self._animation_timer = QtCore.QTimer(self)
        self._animation_timer.timeout.connect(self._on_animation_timeout)

        self.checked_color = QtGui.QColor(67, 181, 129)
        self.unchecked_color = QtGui.QColor(114, 118, 125)

    def steps(self):
        return self._steps

    def set_steps(self, steps):
        self._steps = steps
        if self._checked:
            self._current_step = self._steps
        else:
            self._current_step = 0

    def setChecked(self, checked):
        if checked == self._checked:
            return
        self._checked = checked
        if self._animation_timer.isActive():
            self._animation_timer.stop()

        self._animation_timer.start(7)

    def sizeHint(self):
        return QtCore.QSize(100, 50)

    def mousePressEvent(self, event):
        if event.buttons() & QtCore.Qt.LeftButton:
            self._pressed = True
            self.repaint()
        super(NiceCheckbox, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if self._pressed and not event.buttons() & QtCore.Qt.LeftButton:
            self._pressed = False
            if self.rect().contains(event.pos()):
                self.setChecked(not self._checked)
        super(NiceCheckbox, self).mouseReleaseEvent(event)

    def enterEvent(self, event):
        self._under_mouse = True
        if self.isEnabled():
            self.repaint()
        super(NiceCheckbox, self).enterEvent(event)

    def leaveEvent(self, event):
        self._under_mouse = False
        if self.isEnabled():
            self.repaint()
        super(NiceCheckbox, self).leaveEvent(event)

    def _on_animation_timeout(self):
        if self._checked:
            self._current_step += 1
            if self._current_step == self._steps:
                self._animation_timer.stop()
        else:
            self._current_step -= 1
            if self._current_step == 0:
                self._animation_timer.stop()

        self.repaint()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)

        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        checkbox_rect = QtCore.QRect(event.rect())

        # Draw inner background
        red_dif = self.checked_color.red() - self.unchecked_color.red()
        green_dif = self.checked_color.green() - self.unchecked_color.green()
        blue_dif = self.checked_color.blue() - self.unchecked_color.blue()

        red = int(self.unchecked_color.red() + (
            red_dif / self._steps * self._current_step
        ))
        green = int(self.unchecked_color.green() + (
            green_dif / self._steps * self._current_step
        ))
        blue = int(self.unchecked_color.blue() + (
            blue_dif / self._steps * self._current_step
        ))

        bg_color = QtGui.QColor(red, green, blue)

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
        x_offset = (area_width / self._steps) * self._current_step
        pos_x = checkbox_rect.x() + x_offset
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
