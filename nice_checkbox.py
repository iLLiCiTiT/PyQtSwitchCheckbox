from math import floor
from Qt import QtWidgets, QtCore, QtGui


class NiceCheckbox(QtWidgets.QFrame):
    def __init__(self, checked=True, parent=None):
        super(NiceCheckbox, self).__init__(parent)
        self._checked = checked

        self._current_step = None
        self._steps = 10
        self.set_steps(self._steps)

        self._pressed = False
        self._under_mouse = False

        self._animation_timer = QtCore.QTimer(self)
        self._animation_timer.timeout.connect(self._on_animation_timeout)

        self.checked_color = QtGui.QColor(67, 181, 129)
        self.unchecked_color = QtGui.QColor(114, 118, 125)

        self.setFixedHeight(20)

    def setFixedHeight(self, height):
        super(NiceCheckbox, self).setFixedHeight(height)
        super(NiceCheckbox, self).setFixedWidth(2 * height)

    def setFixedWidth(self, width):
        width = width - (width % 2)
        super(NiceCheckbox, self).setFixedWidth(width)
        super(NiceCheckbox, self).setFixedHeight(width / 2)

    def steps(self):
        return self._steps

    def set_steps(self, steps):
        if steps < 1:
            # QUESTION log message?
            steps = 1

        # Make sure animation is stopped
        if self._animation_timer.isActive():
            self._animation_timer.stop()

        # Set steps and set current step by current checkstate
        self._steps = steps
        if self._checked:
            self._current_step = self._steps
        else:
            self._current_step = 0

    def isChecked(self):
        return self._checked

    def setChecked(self, checked):
        if checked == self._checked:
            return
        self._checked = checked
        if self._animation_timer.isActive():
            self._animation_timer.stop()

        if self.isEnabled():
            # Start animation
            self._animation_timer.start(7)
        else:
            # Do not animate change if is disabled
            if self._checked:
                self._current_step = self._steps
            else:
                self._current_step = 0
            self.repaint()

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
        if self.width() < 1 or self.height() < 1:
            return

        painter = QtGui.QPainter(self)

        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        checkbox_rect = QtCore.QRect(event.rect())

        # Draw inner background
        if self._current_step == self._steps:
            bg_color = self.checked_color

        elif self._current_step == 0:
            bg_color = self.unchecked_color

        else:
            # Animation bg
            red_dif = (
                self.checked_color.red() - self.unchecked_color.red()
            )
            green_dif = (
                self.checked_color.green() - self.unchecked_color.green()
            )
            blue_dif = (
                self.checked_color.blue() - self.unchecked_color.blue()
            )
            offset_ratio = self._current_step / self._steps
            red = int(self.unchecked_color.red() + (
                red_dif * offset_ratio
            ))
            green = int(self.unchecked_color.green() + (
                green_dif * offset_ratio
            ))
            blue = int(self.unchecked_color.blue() + (
                blue_dif * offset_ratio
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
        self._draw_checker(painter, checkbox_rect)

        # Draw shadow overlay
        if not self.isEnabled():
            level = 33
            alpha = 127
            painter.setBrush(QtGui.QColor(level, level, level, alpha))
            painter.drawRoundedRect(checkbox_rect, radius, radius)

        painter.end()

    def _draw_checker(self, painter, checkbox_rect):
        margins_ratio = 20
        size = int(
            checkbox_rect.height() / margins_ratio * (margins_ratio - 2)
        )
        margin_size = int((checkbox_rect.height() - size) / 2)

        area_width = checkbox_rect.width() - (margin_size * 2) - size
        if self._current_step == 0:
            x_offset = 0
        else:
            x_offset = (area_width / self._steps) * self._current_step

        pos_x = checkbox_rect.x() + x_offset + margin_size
        pos_y = checkbox_rect.y() + margin_size

        checker_rect = QtCore.QRect(pos_x, pos_y, size, size)

        path = QtGui.QPainterPath()
        path.addEllipse(checker_rect)

        gradient_center = QtCore.QPointF(
            checker_rect.x() + (checker_rect.width() / 2),
            checker_rect.y() + (checker_rect.height() / 2)
        )
        gradient = QtGui.QRadialGradient(
            gradient_center, size / 2
        )
        gradient.setColorAt(0, QtCore.Qt.white)
        if self._under_mouse:
            if self._pressed:
                gradient.setColorAt(0.85, QtCore.Qt.white)
                gradient.setColorAt(0.9, QtGui.QColor(0, 0, 0, 77))
                gradient.setColorAt(1, QtCore.Qt.transparent)
            else:
                gradient.setColorAt(0.9, QtCore.Qt.white)
                gradient.setColorAt(0.95, QtCore.Qt.transparent)
        else:
            gradient.setColorAt(0.85, QtCore.Qt.white)
            gradient.setColorAt(0.9, QtCore.Qt.transparent)

        painter.fillPath(path, gradient)
