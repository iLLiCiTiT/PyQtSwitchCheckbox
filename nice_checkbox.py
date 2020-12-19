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
