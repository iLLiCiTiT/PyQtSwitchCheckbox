# PyQtSwitchCheckbox
Nicer checkbox for Python Qt bindings named `NiceCheckbox`.

![gif](./example.gif)

### Icons
There is also possibility of having icons in checker. To allow this pass keyword argument `draw_icons=True` to `NiceCheckbox` constructor or call `set_draw_icons` method on created object `my_checkbox.set_draw_icons(True/False)`.

![gif2](./example_icon.gif)

### Minimum size
By default is widget expanding but I would recommend to set fixed size of checkbox and use at least 12px height otherwise is widget barely visible and at least 20px when icons should be drawn.

Project is using Python module [Qt.py](https://pypi.org/project/Qt.py/) which support bindings for PySide2, PyQt5, PySide and PyQt4. (Tested only with PySide2)
