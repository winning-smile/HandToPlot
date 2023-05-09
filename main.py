import sys
from CamThread import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QImage, QPixmap
from PyQt5 import QtCore
import sys
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import matplotlib
import random

matplotlib.use('Qt5Agg')


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        # Window properties
        self.setWindowTitle("UI_Plot")
        self.setGeometry(100, 100, 600, 400)
        self.showMaximized()
        self.opacity_effect = QGraphicsOpacityEffect()
        self.opacity_effect.setOpacity(0.3)

        widget = QWidget()
        self.setCentralWidget(widget)

        # Сетка
        self.grid = QGridLayout()

        # Слой куда выводить изображение с видеокамеры
        self.CameraOutput = QLabel()

        # Создаём процесс для видеокамеры
        self.Camera = handDetector()
        self.Camera.changePixmap.connect(self.setImage)
        self.Camera.graph.connect(self.setGraph)
        self.Camera.changePixmap2.connect(self.setImage2)
        self.Camera.start()

        # Слой для отображения графиков
        self.figure = Figure(figsize=(14, 10), dpi=100)
        self.canvas = FigureCanvas(self.figure)

        # Слой куда транслировать скелет руки
        self.TranslatorOutput = QLabel()
        backgroundImg = QPixmap('test3.png')
        self.TranslatorOutput.setPixmap(backgroundImg)

        #self.TranslatorOutput.setFixedSize(backgroundImg.size())
        #self.TranslatorOutput.raise_()
        #self.TranslatorOutput.setGraphicsEffect(self.opacity_effect)

        self.but = QPushButton()
        self.but.clicked.connect(self.plot2)

        # Вёрстка
        widget.setLayout(self.grid)
        self.grid.addWidget(self.but, 0, 1)
        self.grid.addWidget(self.CameraOutput, 0, 3)

        self.grid.addWidget(self.canvas, 0, 0, alignment=QtCore.Qt.AlignCenter)
        self.grid.addWidget(self.TranslatorOutput, 0, 0,  alignment=QtCore.Qt.AlignCenter)
        self.setLayout(self.grid)


    @QtCore.pyqtSlot(QImage)
    def setImage(self, qImg1):
        self.CameraOutput.setPixmap(QPixmap.fromImage(qImg1))

    @QtCore.pyqtSlot(QImage)
    def setImage2(self, qImg2):
        self.TranslatorOutput.setPixmap(QPixmap.fromImage(qImg2))

    @QtCore.pyqtSlot(str)
    def setGraph(self, value):
        if value == "clear":
            self.clear_canvas()
        else:
            self.plot(value)

    def closeEvent(self, event):
        reply = QMessageBox.question(QMessageBox, 'Выход',
                                     "Вы уверены, что хотите закрыть программу?",
                                     QMessageBox.Yes,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.camera.stop()
            event.accept()

    def plot(self, signal):
        if signal == "cubic":
            self.figure.clear()
            data = [i**2 for i in range(-10, 11, 1)]
        if signal == "quadro":
            self.figure.clear()
            data = [i**3 for i in range(-10, 11, 1)]
        if signal == "sin":
            self.figure.clear()
            data = [np.sin(i) for i in range(-10, 11, 1)]
        if signal == "cos":
            self.figure.clear()
            data = [np.cos(i) for i in range(-10, 11, 1)]
        # create an axis
        ax = self.figure.add_subplot(111)
        # plot data
        ax.plot(data, '*-')
        # refresh canvas
        self.canvas.draw()

    def plot2(self):
        self.figure.clear()
        data = [np.cos(i) for i in range(-10, 11, 1)]
        # create an axis
        ax = self.figure.add_subplot(111)
        # plot data
        ax.plot(data, '*-')
        # refresh canvas
        self.canvas.draw()

    def clear_canvas(self):
        self.figure.clear()
        self.canvas.draw()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = Window()
    main.show()
    sys.exit(app.exec_())