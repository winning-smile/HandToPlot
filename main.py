import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import QtWebEngineWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPalette, QColor, QImage, QPixmap
from CamThread import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=14, height=10, dpi=100):
        figure = Figure(figsize=(width, height), dpi=dpi)
        self.axes = figure.add_subplot(111)
        super(MplCanvas, self).__init__(figure)

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.showMaximized()
        # Цвета для кнопок
        global palette_red, palette_green
        palette_red = QPalette()
        palette_green = QPalette()
        palette_red.setColor(QPalette.Window, (QColor(255, 0, 0, 127)))
        palette_green.setColor(QPalette.Window, (QColor(0, 255, 0, 127)))

    def setupUi(self, MainWindow):
        # Настройки главного окна
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1920, 1080)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMaximumSize(QtCore.QSize(1920, 1080))
        palette_red = QPalette()
        palette_green = QPalette()
        palette_red.setColor(QPalette.Window, (QColor(255, 0, 0, 127)))
        palette_green.setColor(QPalette.Window, (QColor(0, 255, 0, 127)))

        # Виджет всего окна
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Виджет левого меню
        self.widget1 = QtWidgets.QWidget(self.centralwidget)
        self.widget1.setGeometry(QtCore.QRect(10, 10, 1251, 1061))

        # Сетка левого меню
        self.grid = QtWidgets.QGridLayout(self.widget1)
        self.grid.setContentsMargins(0, 0, 0, 0)

        # Холст графиков
        self.canvas = MplCanvas(self.widget1, width=14, height=10, dpi=100)
        self.grid.addWidget(self.canvas, 0, 0)

        # Транслятор движения
        self.translator = QtWidgets.QLabel(self.centralwidget)
        self.grid.addWidget(self.translator, 0, 0)

        # Вывод уравнения графика
        self.webEngineView = QtWebEngineWidgets.QWebEngineView(self.centralwidget)
        #self.webEngineView.setGeometry(QtCore.QRect(270, 50, 811, 41))
        self.webEngineView.setUrl(QtCore.QUrl("about:blank"))
        self.grid.addWidget(self.webEngineView, 0, 0)

        # Виджет правого меню
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(1270, 260, 640, 859))

        # Сетка левого меню
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        # Индикатор режима построения
        self.build_mode = QtWidgets.QLabel(self.layoutWidget)
        self.build_mode.setAutoFillBackground(True)
        self.build_mode.setAlignment(QtCore.Qt.AlignCenter)
        self.build_mode.setPalette(palette_green)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.build_mode.sizePolicy().hasHeightForWidth())
        self.build_mode.setSizePolicy(sizePolicy)
        self.build_mode.setMinimumSize(QtCore.QSize(640, 40))
        self.verticalLayout.addWidget(self.build_mode)

        # Индикатор режима изменения
        self.change_mode = QtWidgets.QLabel(self.layoutWidget)
        self.change_mode.setAutoFillBackground(True)
        self.change_mode.setPalette(palette_red)
        self.change_mode.setAlignment(QtCore.Qt.AlignCenter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.change_mode.sizePolicy().hasHeightForWidth())
        self.change_mode.setSizePolicy(sizePolicy)
        self.change_mode.setMinimumSize(QtCore.QSize(640, 40))
        self.verticalLayout.addWidget(self.change_mode)

        # Кнопка справки
        self.pushButton = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)

        # Вывыод изображения видеокамеры
        self.camera_out = QtWidgets.QLabel(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.camera_out.sizePolicy().hasHeightForWidth())
        self.camera_out.setSizePolicy(sizePolicy)
        self.camera_out.setMinimumSize(QtCore.QSize(640, 480))
        self.camera_out.setObjectName("camera_out")
        self.verticalLayout.addWidget(self.camera_out)

        # Процесс модуля CamThread.py
        self.Camera = handDetector()
        self.Camera.change_camera.connect(self.set_camera_image)
        self.Camera.change_translator.connect(self.set_translator_image)
        #self.Camera.change_graph.connect(self.set_graph_value)
        self.Camera.change_mode.connect(self.set_mode)
        #self.Camera.change_xy.connect(self.set_xy)
        self.Camera.start()

        # Спейсер для правого меню
        spacerItem = QtWidgets.QSpacerItem(20, 250, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem)

        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "HandPlot"))
        self.build_mode.setText(_translate("MainWindow", "Режим построения"))
        self.change_mode.setText(_translate("MainWindow", "Режим изменения"))
        self.pushButton.setText(_translate("MainWindow", "Справка"))

    @QtCore.pyqtSlot(QImage)
    def set_translator_image(self, translator_image):
        self.translator.setPixmap(QPixmap.fromImage(translator_image))

    @QtCore.pyqtSlot(QImage)
    def set_camera_image(self, camera_image):
        self.camera_out.setPixmap(QPixmap.fromImage(camera_image))

    @QtCore.pyqtSlot(bool)
    def set_mode(self, bool_value):
        if not bool_value:
            self.change_mode.setPalette(palette_green)
            self.build_mode.setPalette(palette_red)
        else:
            self.build_mode.setPalette(palette_green)
            self.change_mode.setPalette(palette_red)

    @QtCore.pyqtSlot(str)
    def set_graph_value(self, graph_value):
        if graph_value == "clear":
            self.graph_signal = graph_value
            self.clear_canvas()
        else:
            self.graph_signal = graph_value
            self.plot(graph_value)

    @QtCore.pyqtSlot(int, int)
    def set_xy(self, x_value, y_value):
        self.plot_update(x_value, y_value)

    # TODO: mathtext
    def plot(self, signal):
        if signal == "cubic":
            self.canvas.figure.clear()
            x = np.arange(-10, 10.1, 0.1)
            # create an axis
            ax = self.canvas.figure.add_subplot(111)
            ax.set_xlabel('Ось абсцисс')
            ax.set_ylabel('Ось ординат')
            ax.set_title('y = x*x')
            ax.grid()
            ax.plot(x, x ** 2, label='y=x*x')
            ax.scatter(0,0)
            ax.legend()
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

    def plot_update(self, dist_x, dist_y):
        if self.graph_signal == "cubic":
            self.canvas.figure.clear()
            x = np.arange(-10-dist_x, 11+dist_x, 1)
            # create an axis
            ax = self.canvas.figure.add_subplot(111)
            ax.set_xlabel('Ось абсцисс')
            ax.set_ylabel('Ось ординат')
            ax.set_title('y = x*x')
            ax.grid()
            # plot data
            ax.plot(x, x ** 2, label='y=x*x')

            if dist_x > 0:
                tmp_str = 'y = ' + str(dist_y) + ' + (x + ' + str(dist_x) + ')^2'
            elif dist_x < 0:
                tmp_str = 'y = ' + str(dist_y) + ' + (x ' + str(dist_x) + ')^2'
            elif dist_x == 0 and dist_y == 0:
                tmp_str = 'y = x^2'
            else:
                tmp_str = 'y =' + str(dist_y) + ' + x^2'

            ax.plot(x, ((x-dist_x)**2)+dist_y, label=tmp_str)
            ax.legend()
            # refresh canvas
            self.canvas.draw()

    def clear_canvas(self):
        self.figure.clear()
        self.canvas.draw()

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