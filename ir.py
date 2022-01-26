import os
import platform
import json
import PyQt5
import sys

from PyQt5.QtGui import QPainterPath, QRegion
from PyQt5.uic.properties import QtGui

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtCore import QPoint
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget, QApplication, QGridLayout, QLineEdit


class Form(QtGui.QWidget):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        # for making the window draggable
        self.oPos = self.pos()
        self.setFixedSize(1000, 650)

        testlw = QVBoxLayout()


        testlo = QGridLayout()
        testlo.addLayout(testlw, 0, 1)

        self.setLayout(testlo)
        self.setWindowTitle('test')
        self.setStyleSheet('background-color: rgb(255,255,0);')
        self.setStyleSheet('border-radius: 30px')

def mousePressEvent(self, event):
    self.oPos = event.globalPos()

def mouseMoveEvent(self, QMouseEvent):
    delta = QPoint(QMouseEvent.globalPos() - self.oPos)
    self.move(self.x() + delta.x(), self.y() + delta.y())
    self.oPos = QMouseEvent.globalPos()


app = QApplication(sys.argv)
screen = Form()
screen.show()
sys.exit(app.exec_())