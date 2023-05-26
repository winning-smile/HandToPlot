import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import QtWebEngineWidgets
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPalette, QColor, QImage, QPixmap
from PyQt5.QtCore import pyqtSignal
from CamThread import *
from labeler import *
from HelpWindow import *
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
        # список рабочих видеокамер
        self.working_ports = []
        # флаг рабочей видеокамеры
        self.camera_aviable = True
        # проверка рабочих видеокамер
        self.list_ports()
        self.text = ""
        self.camera_handler()

        if self.camera_aviable:
            # инициализируем интерфейс
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
        self.mathtext = QWebEngineView(self.centralwidget)
        pageSource = """
                     <html><head>
                     <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/MathJax.js?config=TeX-AMS-MML_HTMLorMML">                     
                     </script></head>
                     <body>
                     <p><mathjax style="font-size:2em">Ожидание ввода</mathjax></p>
                     </body></html>
                     """
        self.mathtext.setHtml(pageSource)
        self.mathtext.page().settings().setAttribute(QtWebEngineWidgets.QWebEngineSettings.ShowScrollBars, False)
        self.mathtext.setGeometry(QtCore.QRect(270, 50, 811, 80))

        # Виджет правого меню
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(1270, 100, 640, 859))

        # Сетка правого меню
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        # Выбор видеокамеры
        self.camera_list = QtWidgets.QComboBox(self.layoutWidget)
        self.camera_list.setMinimumSize(QtCore.QSize(640, 20))
        self.camera_list.addItems(self.working_ports)
        self.camera_list.activated[int].connect(self.camera_index)
        self.verticalLayout.addWidget(self.camera_list)

        # Слайдер шаг по x
        self.x_slider_label = QtWidgets.QLabel(self.layoutWidget)
        self.x_slider_label.setText("Шаг по оси абсцисс: 1")
        self.x_slider_label.setMinimumSize(QtCore.QSize(640, 40))
        self.verticalLayout.addWidget(self.x_slider_label)

        self.x_slider = QtWidgets.QSlider(self.layoutWidget)
        self.x_slider.setOrientation(QtCore.Qt.Horizontal)
        self.x_slider.setMinimumSize(QtCore.QSize(640, 40))
        self.x_slider.setMinimum(1)
        self.x_slider.setMaximum(50)
        self.x_slider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.x_slider.setTickInterval(4)
        self.x_slider.valueChanged.connect(self.x_step)
        self.verticalLayout.addWidget(self.x_slider)

        # Слайдер шаг по y
        self.y_slider_label = QtWidgets.QLabel(self.layoutWidget)
        self.y_slider_label.setText("Шаг по оси ординат: 1")
        self.y_slider_label.setMinimumSize(QtCore.QSize(640, 40))
        self.verticalLayout.addWidget(self.y_slider_label)

        self.y_slider = QtWidgets.QSlider(self.layoutWidget)
        self.y_slider.setOrientation(QtCore.Qt.Horizontal)
        self.y_slider.setMinimumSize(QtCore.QSize(640, 40))
        self.y_slider.setMinimum(1)
        self.y_slider.setMaximum(50)
        self.y_slider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.y_slider.setTickInterval(4)
        self.y_slider.valueChanged.connect(self.y_step)
        self.verticalLayout.addWidget(self.y_slider)

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
        self.help_button = QtWidgets.QPushButton(self.layoutWidget)
        self.verticalLayout.addWidget(self.help_button)
        self.help_button.clicked.connect(self.help_window_show)

        # Вывыод изображения видеокамеры
        self.camera_out = QtWidgets.QLabel(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.camera_out.sizePolicy().hasHeightForWidth())
        self.camera_out.setSizePolicy(sizePolicy)
        self.camera_out.setMinimumSize(QtCore.QSize(640, 480))
        self.verticalLayout.addWidget(self.camera_out)

        # Процесс модуля CamThread.py
        self.Camera = handDetector()
        self.Camera.change_camera.connect(self.set_camera_image)
        self.Camera.change_translator.connect(self.set_translator_image)
        self.Camera.change_graph.connect(self.set_graph_value)
        self.Camera.change_mode.connect(self.set_mode)
        self.Camera.change_xy.connect(self.set_xy)
        self.Camera.start()

        #Спейсер для правого меню
        spacerItem = QtWidgets.QSpacerItem(20, 250, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem)

        # Инициализация интерфейса
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def list_ports(self):
        dev_port = 1
        while dev_port != 5:
            camera = cv2.VideoCapture(dev_port)
            if not camera.isOpened():
                pass
            else:
                is_reading, img = camera.read()
                if is_reading:
                    self.working_ports.append("Видеокамера " + str(dev_port))
            dev_port += 1

    def camera_handler(self):
        if not self.working_ports:
            self.camera_aviable = False
            self.error = Error_Window()
            self.error.show()

    def camera_index(self, camera_number):
        self.Camera.camera_index = camera_number - 1

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "HandPlot"))
        self.build_mode.setText(_translate("MainWindow", "Режим построения"))
        self.change_mode.setText(_translate("MainWindow", "Режим изменения"))
        self.help_button.setText(_translate("MainWindow", "Справка"))

    def help_window_show(self):
        self.help = Help_Window()
        self.help.show()

    def x_step(self, value):
        self.x_slider_label.setText(f"Шаг по оси абсцисс: {value}")
        self.Camera.x_step = value

    def y_step(self, value):
        self.y_slider_label.setText(f"Шаг по оси ординат: {value}")
        self.Camera.y_step = value

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

    def retranslate_mathtext(self, signal, x, y, z):
        self.text = mathtext_update(signal, x, y, z)
        self.mathtext.setHtml(self.text)
        self.mathtext.page().settings().setAttribute(QtWebEngineWidgets.QWebEngineSettings.ShowScrollBars, False)

    def plot(self, signal):
        if signal == "line":
            self.canvas.figure.clear()
            x = np.arange(-10, 10.1, 0.1)
            ax = self.canvas.figure.add_subplot(111)
            ax.set_xlabel('Ось абсцисс')
            ax.set_ylabel('Ось ординат')
            ax.grid()
            ax.axvline(x=0, color='black')
            ax.axhline(y=0, color='black')
            ax.plot(x, x, label='y=x')
            ax.set_xlim(-10, 10)
            ax.set_ylim(-20, 100)
            ax.legend()
            self.retranslate_mathtext(signal, 0, 0, 1)
            self.canvas.draw()

        if signal == "cubic":
            self.canvas.figure.clear()
            x = np.arange(-10, 10.1, 0.1)
            ax = self.canvas.figure.add_subplot(111)
            ax.set_xlabel('Ось абсцисс')
            ax.set_ylabel('Ось ординат')
            ax.grid()
            ax.axvline(x=0, color='black')
            ax.axhline(y=0, color='black')
            ax.plot(x, x ** 2, label='y=x*x')
            ax.set_xlim(-10, 10)
            ax.set_ylim(-20, 100)
            ax.legend()
            # refresh canvas
            self.retranslate_mathtext(signal, 0, 0, 1)
            self.canvas.draw()

        if signal == "quadro":
            self.figure.clear()
            x = np.arange(-10, 11, 1)
            ax = self.figure.add_subplot(111)
            ax.set_xlabel('Ось абсцисс')
            ax.set_ylabel('Ось ординат')
            ax.grid()
            ax.axvline(x=0, color='black')
            ax.axhline(y=0, color='black')
            ax.plot(x, x ** 3, 's-')
            ax.set_xlim(-10, 10)
            ax.set_ylim(-20, 100)
            ax.legend()
            self.retranslate_mathtext(signal, 0, 0, 1)
            self.canvas.draw()

    def plot_update(self, dist_x, dist_y):
        if self.graph_signal == "cubic":
            self.canvas.figure.clear()
            x = np.arange(-10-dist_x, 11+dist_x, 1)
            ax = self.canvas.figure.add_subplot(111)
            ax.set_xlabel('Ось абсцисс')
            ax.set_ylabel('Ось ординат')
            ax.set_title('y = x*x')
            ax.grid()
            ax.axvline(x=0, color='black')
            ax.axhline(y=0, color='black')
            ax.plot(x, x ** 2, label='y=x*x')
            ax.plot(x, ((x-dist_x)**2)+dist_y)
            ax.set_xlim(-10, 10)
            ax.set_ylim(-20, 100)
            ax.legend()
            self.retranslate_mathtext(self.graph_signal, dist_x, dist_y, 1)
            self.canvas.draw()

    def clear_canvas(self):

        self.canvas.figure.clear()
        self.canvas.draw()
        pageSource = """
                     <html><head>
                     <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/MathJax.js?config=TeX-AMS-MML_HTMLorMML">                     
                     </script></head>
                     <body>
                     <p><mathjax style="font-size:2em">Ожидание ввода</mathjax></p>
                     </body></html>
                     """
        self.mathtext.setHtml(pageSource)

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