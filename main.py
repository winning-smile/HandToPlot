import sys
from CamThread import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QImage, QPixmap, QFont
from PyQt5 import QtCore
import sys
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import matplotlib
from matplotlib import rc
import random

matplotlib.use('Qt5Agg')
plt.style.use("Solarize_Light2")


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        # Window properties
        self.setWindowTitle("UI_Plot")
        self.setGeometry(100, 100, 600, 400)
        self.showMaximized()
        self.graph_signal = None

        widget = QWidget()
        self.setCentralWidget(widget)

        # Сетка
        self.grid = QGridLayout()

        # Слой куда выводить изображение с видеокамеры
        self.camera_out = QLabel()

        # Индикатор режима работы
        self.mode_label = QLabel()
        self.mode_label.setText('Режим: Построение')

        # Создаём процесс для видеокамеры
        self.Camera = handDetector()
        self.Camera.change_camera.connect(self.set_camera_image)
        self.Camera.change_translator.connect(self.set_translator_image)
        self.Camera.change_graph.connect(self.set_graph_value)
        self.Camera.change_mode.connect(self.set_mode)
        self.Camera.change_x.connect(self.set_x)
        self.Camera.start()

        # Слой для отображения графиков
        self.figure = Figure(figsize=(14, 10), dpi=100)
        self.canvas = FigureCanvas(self.figure)

        # Слой куда транслировать скелет руки
        self.translator_out = QLabel()
        background_img = QPixmap('back.png')
        self.translator_out.setPixmap(background_img)

        # Вёрстка
        widget.setLayout(self.grid)
        self.grid.addWidget(self.mode_label, 1, 1)
        self.grid.addWidget(self.camera_out, 0, 1)
        self.grid.addWidget(self.canvas, 0, 0, alignment=QtCore.Qt.AlignCenter)
        self.grid.addWidget(self.translator_out, 0, 0,  alignment=QtCore.Qt.AlignCenter)
        self.setLayout(self.grid)


    @QtCore.pyqtSlot(QImage)
    def set_camera_image(self, camera_image):
        self.camera_out.setPixmap(QPixmap.fromImage(camera_image))

    @QtCore.pyqtSlot(QImage)
    def set_translator_image(self, translator_image):
        self.translator_out.setPixmap(QPixmap.fromImage(translator_image))

    @QtCore.pyqtSlot(bool)
    def set_mode(self, bool_value):
        if not bool_value:
            self.mode_label.setText('Режим: Изменение')
        else:
            self.mode_label.setText('Режим: Построение')

    @QtCore.pyqtSlot(str)
    def set_graph_value(self, graph_value):
        if graph_value == "clear":
            self.graph_signal = graph_value
            self.clear_canvas()
        else:
            self.graph_signal = graph_value
            self.plot(graph_value)

    @QtCore.pyqtSlot(int)
    def set_x(self, x_value):
        self.plot_update(x_value)

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
            x = np.arange(-10, 10.1, 0.1)
            # create an axis
            ax = self.figure.add_subplot(111)
            ax.set_xlabel('Ось абсцисс')
            ax.set_ylabel('Ось ординат')
            ax.set_title('y = x*x')
            ax.grid()
            # plot data
            ax.plot(x, x ** 2)
            # refresh canvas
            self.canvas.draw()

        if signal == "quadro":
            self.figure.clear()
            x = np.arange(-10, 11, 1)
            # create an axis
            ax = self.figure.add_subplot(111)
            ax.set_xlabel('Ось абсцисс')
            ax.set_ylabel('Ось ординат')
            ax.set_title('y = x*x*x')
            ax.grid()
            # plot data
            ax.plot(x, x ** 3, 's-')
            # refresh canvas
            self.canvas.draw()

        if signal == "sin":
            self.figure.clear()
            x = np.arange(-10, 11, 1)
            # create an axis
            ax = self.figure.add_subplot(111)
            ax.set_xlabel('Ось абсцисс')
            ax.set_ylabel('Ось ординат')
            ax.set_title('y = sin(x)')
            ax.grid()
            # plot data
            ax.plot(x, np.sin(x), 's-')
            # refresh canvas
            self.canvas.draw()

        if signal == "cos":
            self.figure.clear()
            x = np.arange(-10, 11, 1)
            # create an axis
            ax = self.figure.add_subplot(111)
            ax.set_xlabel('Ось абсцисс')
            ax.set_ylabel('Ось ординат')
            ax.set_title('y = cos(x)')
            ax.grid()
            # plot data
            ax.plot(x, np.cos(x), 's-')
            # refresh canvas
            self.canvas.draw()

    def plot_update(self, dist_x):
        if self.graph_signal == "cubic":
            self.figure.clear()
            x = np.arange(-10-dist_x, 11+dist_x, 1)
            # create an axis
            ax = self.figure.add_subplot(111)
            ax.set_xlabel('Ось абсцисс')
            ax.set_ylabel('Ось ординат')
            ax.set_title('y = x*x')
            ax.grid()
            # plot data
            ax.plot(x, x ** 2)
            ax.plot(x, (x-dist_x)**2)
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