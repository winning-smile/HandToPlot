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
        self.resize(1400, 800)
        self.tab_widget =TabWidget(self)
        self.setCentralWidget(self.tab_widget)

class TabWidget(QtWidgets.QWidget):
    def __init__(self, parent):
        super(QtWidgets.QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        # Инициализация закладок
        self.tabs = QTabWidget()
        self.main_tab = QWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tab4 = QWidget()
        self.tab5 = QWidget()
        self.tab6 = QWidget()
        self.tab7 = QWidget()

        # Добавляем закладки
        self.tabs.addTab(self.main_tab, "Главная")
        self.tabs.addTab(self.tab1, "1")
        self.tabs.addTab(self.tab2, "2")
        self.tabs.addTab(self.tab3, "3")
        self.tabs.addTab(self.tab4, "4")
        self.tabs.addTab(self.tab5, "5")
        self.tabs.addTab(self.tab6, "6")
        self.tabs.addTab(self.tab7, "7")

        # Главная закладка
        self.main_tab.layout = QVBoxLayout(self)
        self.main_tab.layout.setContentsMargins(0, 0, 0, 0)
        self.main_tab.layout.setSpacing(0)

        self.main_tab_text = QLabel()
        self.main_tab_text.setText("Для получения справочной информации о полях, представленных на рисунке ниже, перейдите на соответствующую закладку.")
        self.main_tab_text.setFont(QFont('Arial', 16))
        self.main_tab.layout.addWidget(self.main_tab_text)

        self.main_tab_img = QLabel()
        pixmap = QPixmap('img/info.jpg')
        self.main_tab_img.setPixmap(pixmap)
        self.main_tab.layout.addWidget(self.main_tab_img)

        self.main_tab.setLayout(self.main_tab.layout)

        # Первая закладка
        self.tab1.layout = QVBoxLayout(self)
        self.tab1.layout.setContentsMargins(0, 0, 0, 0)
        self.tab1.layout.setSpacing(0)

        self.tab1_text = QLabel()
        self.tab1_text.setText("Данное поле предназначено для вывода зависимости f(x) = x для графиков, которые изображены в поле под номером 2. Ниже представлены примеры, как может выглядеть данное поле.")
        self.tab1_text.setFont(QFont('Arial', 16))
        self.tab1.layout.addWidget(self.tab1_text)

        self.tab1_img = QLabel()
        pixmap = QPixmap('img/tab1img.jpg')
        self.tab1_img.setPixmap(pixmap)
        self.tab1.layout.addWidget(self.tab1_img)

        self.tab1.setLayout(self.tab1.layout)

        # Вторая закладка
        self.tab2.layout = QVBoxLayout(self)
        self.tab2.layout.setContentsMargins(0, 0, 0, 0)
        self.tab2.layout.setSpacing(0)

        self.tab2_text = QLabel()
        self.tab2_text.setText("Данное поле предназначено для вывода графика выбранной пользователем функции Ниже представлен пример, как может выглядеть данное поле.")
        self.tab2_text.setFont(QFont('Arial', 16))
        self.tab2.layout.addWidget(self.tab2_text)

        self.tab2_img = QLabel()
        pixmap = QPixmap('img/tab2img.jpg')
        self.tab2_img.setPixmap(pixmap)
        self.tab2.layout.addWidget(self.tab2_img)

        self.tab2.setLayout(self.tab2.layout)

        # Третья закладка
        self.tab3.layout = QVBoxLayout(self)
        self.tab3.layout.setContentsMargins(0, 0, 0, 0)
        self.tab3.layout.setSpacing(0)

        self.tab3_text = QLabel()
        self.tab3_text.setText("Данное поле предназначено для выбора видеокамеры, с которой пользователь хочет работать.")
        self.tab3_text.setFont(QFont('Arial', 16))
        self.tab3.layout.addWidget(self.tab3_text)

        self.tab3.setLayout(self.tab3.layout)

        # Четвёртая закладка
        self.tab4.layout = QVBoxLayout(self)
        self.tab4.layout.setContentsMargins(0, 0, 0, 0)
        self.tab4.layout.setSpacing(0)

        self.tab4_text = QLabel()
        self.tab4_text.setText("Данное поле предназначено для выбора шага по оси абсции/ординат, на который будет происходить смещение графика при изменении.")
        self.tab4_text.setFont(QFont('Arial', 16))
        self.tab4.layout.addWidget(self.tab4_text)

        self.tab4.setLayout(self.tab4.layout)

        # Пятая закладка
        self.tab5.layout = QVBoxLayout(self)
        self.tab5.layout.setContentsMargins(0, 0, 0, 0)
        self.tab5.layout.setSpacing(0)

        self.tab5_text = QLabel()
        self.tab5_text.setText("Данное поле предназначено для индикации режима работы, в котором находится приложение. Для того чтобы сменить режим, необходимо показать жест представленный ниже.")
        self.tab5_text.setFont(QFont('Arial', 16))
        self.tab5.layout.addWidget(self.tab5_text)

        self.tab5_img = QLabel()
        pixmap = QPixmap('img/tab5img.jpg')
        self.tab5_img.setPixmap(pixmap)
        self.tab5.layout.addWidget(self.tab5_img)

        self.tab5.setLayout(self.tab5.layout)

        # Шестая закладка
        self.tab6.layout = QVBoxLayout(self)
        self.tab6.layout.setContentsMargins(0, 0, 0, 0)
        self.tab6.layout.setSpacing(0)

        self.tab6_text = QLabel()
        self.tab6_text.setText("Данное поле предназначено для получения справочной информации о работе с приложением.")
        self.tab6_text.setFont(QFont('Arial', 16))
        self.tab6.layout.addWidget(self.tab6_text)

        self.tab6.setLayout(self.tab6.layout)

        # Седьмая закладка
        self.tab7.layout = QVBoxLayout(self)
        self.tab7.layout.setContentsMargins(0, 0, 0, 0)
        self.tab7.layout.setSpacing(0)

        self.tab7_text = QLabel()
        self.tab7_text.setText("Данное поле предназначено вывода изображения с выбранной пользователем видеокамеры.")
        self.tab7_text.setFont(QFont('Arial', 16))
        self.tab7.layout.addWidget(self.tab7_text)

        self.tab7_img = QLabel()
        pixmap = QPixmap('img/tab7img.jpg')
        self.tab7_img.setPixmap(pixmap)
        self.tab7.layout.addWidget(self.tab7_img)

        self.tab7.setLayout(self.tab7.layout)


        # Добавляем закладки в виджет
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

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