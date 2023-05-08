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
        #self.setFixedSize(self, 1)

        widget = QWidget()
        self.setCentralWidget(widget)
        # Обёртка сверху
        #self.background = QLabel()
        #backgroundImg = QPixmap('test2.png')
        #self.background.setPixmap(backgroundImg)
        #self.resize(backgroundImg.width(), backgroundImg.height())

        # Окно куда выводить изображение с видеокамеры
        self.label = QLabel()
        self.label2 = QLabel(widget)
        backgroundImg2 = QPixmap('test3.png')
        self.label2.setPixmap(backgroundImg2)
        self.label2.setFixedSize(backgroundImg2.size())

        #Создаём процесс для видеокамеры
        self.camera = handDetector()
        self.camera.changePixmap.connect(self.setImage)
        #self.camera.graph.connect(self.setGraph)
        self.camera.changePixmap2.connect(self.setImage2)
        #self.camera.changePixmap3.connect(self.setImage2)
        self.camera.start()

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        widget.setLayout(layout)
        layout.addWidget(self.label)

        #self.image2 = QLabel(widget)
        #backgroundImg2 = QPixmap('test3.png')
        #self.image2.setPixmap(backgroundImg2)
        #self.image2.setFixedSize(backgroundImg2.size())

        # Create the maptlotlib FigureCanvas object
        #self.figure = plt.figure()
        #self.canvas = FigureCanvas(self.figure)

       #layout.addWidget(self.background)
        #layout.addWidget(self.label)
        #layout.addWidget(self.canvas)

        # Слой для вёрстки

        #widget.setLayout(layout)
        #self.setCentralWidget(widget)
        #self.setLayout(layout)




    @QtCore.pyqtSlot(QImage)
    def setImage(self, qImg1):
        self.label.setPixmap(QPixmap.fromImage(qImg1))

    @QtCore.pyqtSlot(QImage)
    def setImage2(self, qImg2):
        self.label2.setPixmap(QPixmap.fromImage(qImg2))

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


    # action called by the push button
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

    def clear_canvas(self):
        self.figure.clear()
        self.canvas.draw()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = Window()
    main.show()
    sys.exit(app.exec_())