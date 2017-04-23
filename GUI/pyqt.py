__author__ = 'raistlin'
import sys
from PyQt5 import QtWidgets, QtGui


def window():
    app = QtWidgets.QApplication(sys.argv)
    w = QtWidgets.QWidget()
    b = QtWidgets.QPushButton

    w.setWindowTitle("Connected2me")
    w.setGeometry(100,100,500,500)

    q_user_photo = QtWidgets.QLabel(w)
    q_user_photo.setPixmap(QtGui.QPixmap("xxx.jpg"))






    w.show()
    sys.exit(app.exec_())


window()
