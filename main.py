import sys
import os
from CamThread import CameraThread
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap
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
        self.camera = CameraThread()
        self.camera.image.connect(self.update_image)
        self.camera.start()


    def update_image(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
        self.label.setPixmap(QPixmap.fromImage(image))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = Window()
    main.show()
    sys.exit(app.exec_())
