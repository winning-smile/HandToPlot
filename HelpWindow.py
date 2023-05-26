from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import QtWebEngineWidgets
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPalette, QColor, QImage, QPixmap
class Help_Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Справка")

class Error_Window(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Исключение")
        QBtn = QDialogButtonBox.Ok

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)

        self.layout = QVBoxLayout()
        message = QLabel("Не обнаружено подключенных видеокамер.")
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)