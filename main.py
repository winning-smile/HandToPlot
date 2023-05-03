import sys
import os
from CamThread import *
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap
from PyQt5 import QtCore, QtGui
import cv2
import mediapipe as mp
import numpy as np

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        # Window properties
        self.setWindowTitle("UI_Plot")
        self.resize(1080, 1080)

        # Окно куда выводить изображение с видеокамеры
        self.label = QLabel()
        self.setCentralWidget(self.label)

        # Создаём процесс для видеокамеры
        self.camera = handDetector()
        self.camera.changePixmap.connect(self.setImage)
        self.camera.start()


    @QtCore.pyqtSlot(QImage)
    def setImage(self, qImg1):
        self.label.setPixmap(QPixmap.fromImage(qImg1))

    def closeEvent(self, event):
        reply = QMessageBox.question(QMessageBox, 'Выход',
                                     "Вы уверены, что хотите закрыть программу?",
                                     QMessageBox.Yes,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.camera.stop()
            event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = Window()
    main.show()
    sys.exit(app.exec_())
