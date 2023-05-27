from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import QtWebEngineWidgets
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPalette, QColor, QImage, QPixmap, QFont
class Help_Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Справка")
        self.setupUi(self)

    def setupUi(self, HelpWindow):
        # Настройки главного окна
        HelpWindow.setObjectName("HelpWindow")
        HelpWindow.resize(1400, 1080)

        # Виджет всего окна
        self.centralwid = QtWidgets.QScrollArea(HelpWindow)
        self.centralwid.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)

        self.centralwidget = QWidget(self.centralwid)

        # Сетка левого меню
        self.grid = QtWidgets.QVBoxLayout(self.centralwidget)
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.setSpacing(0)

        self.main_img = QtWidgets.QLabel()
        pixmap = QPixmap('img/info.jpg')
        self.main_img.setPixmap(pixmap)
        self.grid.addWidget(self.main_img)

        self.first = QtWidgets.QLabel()
        self.first.setText("Поле под номером 1 служит для вывода уравнения построенного графика.")
        self.first.setFont(QFont('Arial', 16))
        self.grid.addWidget(self.first)

        self.second = QtWidgets.QLabel()
        self.second.setText("Поле под номером 2 служит для вывода графика.")
        self.second.setFont(QFont('Arial', 16))
        self.grid.addWidget(self.second)

        self.third = QtWidgets.QLabel()
        self.third.setText("Поле под номером 1 служит для вывода уравнения построенного графика.")
        self.third.setFont(QFont('Arial', 16))
        self.grid.addWidget(self.third)

        self.fourth = QtWidgets.QLabel()
        self.fourth.setText("Поле под номером 1 служит для вывода уравнения построенного графика.")
        self.fourth.setFont(QFont('Arial', 16))
        self.grid.addWidget(self.fourth)

        self.fifth = QtWidgets.QLabel()
        self.fifth.setText("Поле под номером 1 служит для вывода уравнения построенного графика.")
        self.fifth.setFont(QFont('Arial', 16))
        self.grid.addWidget(self.fifth)

        self.sixth = QtWidgets.QLabel()
        self.sixth.setText("Поле под номером 1 служит для вывода уравнения построенного графика.")
        self.sixth.setFont(QFont('Arial', 16))
        self.grid.addWidget(self.sixth)

        self.seventh = QtWidgets.QLabel()
        self.seventh.setText("Поле под номером 1 служит для вывода уравнения построенного графика.")
        self.seventh.setFont(QFont('Arial', 16))
        self.grid.addWidget(self.seventh)

        # Инициализация интерфейса
        HelpWindow.setCentralWidget(self.centralwidget)
        QtCore.QMetaObject.connectSlotsByName(HelpWindow)


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