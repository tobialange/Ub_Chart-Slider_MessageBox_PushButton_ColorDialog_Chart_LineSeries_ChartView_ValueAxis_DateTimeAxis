import sys
from PySide6 import QtWidgets
from MyMainWindow import MyMainWindow


app = QtWidgets.QApplication(sys.argv)
dialog = MyMainWindow()
dialog.show()
sys.exit(app.exec())

#All you need:
# https://www.w3schools.com/python/default.asp
# https://doc.qt.io/qtforpython-6/quickstart.html
