import sys
from CamThread import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QImage, QPixmap
from PyQt5 import QtCore
import sys
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import random

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        # Window properties
        self.setWindowTitle("UI_Plot")
        self.resize(1920, 1080)
        layout = QHBoxLayout()

        # Окно куда выводить изображение с видеокамеры
        self.label = QLabel()
        #self.setCentralWidget(self.label)

        # Создаём процесс для видеокамеры
        self.camera = handDetector()
        self.camera.changePixmap.connect(self.setImage)
        self.camera.start()

        # Create the maptlotlib FigureCanvas object,
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)

        layout.addWidget(self.label)
        layout.addWidget(self.canvas)

        # Слой для вёрстки
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        #self.setLayout(layout)




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