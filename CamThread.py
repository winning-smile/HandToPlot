from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal, QTime
from PyQt5.QtGui import QImage, QPixmap
import PyQt5.QtGui
import numpy as np
import time
import mediapipe as mp
import cv2
import math

class handDetector(QThread):
   # Сигналы передающиеся в главное окно
   change_camera = pyqtSignal(QImage)
   change_translator = pyqtSignal(QImage)
   change_graph = pyqtSignal(str)
   change_mode = pyqtSignal(bool)
   change_xy = pyqtSignal(int, int)

   def __init__(self, mode=False, maxHands=1, detectionCon=1, trackCon=0.5):
      super().__init__()
      # Камера
      self.cap1 = None
      self.mode = mode
      self.camera_index = 0
      # Шаги по x,y
      self.x_step = 1
      self.y_step = 1
      # Количество рук, которые можно одновременно отслеживать
      self.maxHands = maxHands
      # Нижний порог подтверждения руки
      self.detectionCon = detectionCon
      self.trackCon = trackCon
      # Модель для поиска руки
      self.mpHands = mp.solutions.hands
      self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.detectionCon, self.trackCon)
      self.mpDraw = mp.solutions.drawing_utils
      # Сигнал для передачи данных, о том какой график строить
      self.signal = "clear"
      # Картинка, на которую транслируется движения скелета руки
      self.back = cv2.imread('img/back.png', cv2.IMREAD_UNCHANGED)
      # Буффер для смены режима
      self.t = []
      # Буфферы для смены графиков
      self.line = []
      self.cubic = []
      self.quadro = []
      self.clear_flag = []
      self.xy_flag = []
      # Флаг для смены режима - по умолчанию построение
      self.flag = True

   # Модель находит на каждом кадре скелет руки и возвращает изображение с нарисованным скелетом
   def find_hands(self, img, draw=True):
      imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
      self.results = self.hands.process(imgRGB)

      if self.results.multi_hand_landmarks:
         for handLms in self.results.multi_hand_landmarks:
            if draw:
               self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
      return img

   # Возвращает массив координат всех опорных точек
   def find_position(self, img, handNo=0, draw=True):
      self.lmList = []
      if self.results.multi_hand_landmarks:
         myHand = self.results.multi_hand_landmarks[handNo]
         for id, lm in enumerate(myHand.landmark):
            h, w, c = img.shape
            cx, cy = int(lm.x * w), int(lm.y * h)
            self.lmList.append([id, cx, cy])

      return self.lmList

   # Смена флага изменения/построения
   def change_flag(self):
      if self.flag:
         self.flag = False
         self.change_mode.emit(self.flag)
      else:
         self.flag = True
         self.change_mode.emit(self.flag)

   # Обнуление счётчиков для жестов построения графиков
   def refresh_flags(self):
      self.line.clear()
      self.cubic.clear()
      self.quadro.clear()
      self.t.clear()
      self.clear_flag.clear()
      self.xy_flag.clear()

   # Функция детекции жестов для построения графиков
   def on_build(self, lmlist):
      tmparr = []

      if lmlist:
         for i in range(len(lmlist)):
            tmparr.append(lmlist[i][1])

         # Переход в режим изменения/построения
         if (math.hypot(lmlist[4][1] - lmlist[8][1], lmlist[4][2] - lmlist[8][2]) < 20) and (lmlist[12][2] < lmlist[4][2]) and (lmlist[12][2] < lmlist[8][2]) and (lmlist[4][1] > lmlist[12][1]) and (lmlist[8][1] > lmlist[12][1]):
            self.t.append(0)
            if len(self.t) >= 30:
               self.refresh_flags()
               self.change_flag()

         if self.flag:
            # Очистка холста
            if (lmlist[4][2] < lmlist[8][2]) and (lmlist[4][2] < lmlist[12][2]) and (lmlist[4][2] < lmlist[16][2]) and (lmlist[4][2] < lmlist[20][2]):
               self.clear_flag.append(0)
               if len(self.clear_flag) >= 30:
                  self.refresh_flags()
                  self.change_graph.emit("clear")

            # линия done
            elif (math.hypot(lmlist[4][1] - lmlist[10][1], lmlist[4][2] - lmlist[10][2]) < 15) and (lmlist[8][2] < lmlist[12][2]) and (lmlist[8][2] < lmlist[16][2]) and (lmlist[8][2] < lmlist[20][2]) and (lmlist[8][2] < lmlist[4][2]):
               self.line.append(0)
               if len(self.line) >= 30:
                  self.refresh_flags()
                  self.change_graph.emit("line")

            # парабола done
            elif (math.hypot(lmlist[4][1] - lmlist[14][1], lmlist[4][2] - lmlist[14][2]) < 15) and (lmlist[8][2] < lmlist[16][2]) and (lmlist[8][2] < lmlist[20][2]) and (lmlist[12][2] < lmlist[16][2]) and (lmlist[12][2] < lmlist[20][2]):
               self.cubic.append(0)
               if len(self.cubic) >= 30:
                  self.refresh_flags()
                  self.change_graph.emit("cubic")

            # гипербола done
            elif (math.hypot(lmlist[4][1] - lmlist[18][1], lmlist[4][2] - lmlist[18][2]) < 15) and (lmlist[8][2] < lmlist[20][2]) and (lmlist[12][2] < lmlist[20][2]) and (lmlist[16][2] < lmlist[20][2]):
               self.quadro.append(0)
               if len(self.quadro) >= 30:
                  self.refresh_flags()
                  self.change_graph.emit("quadro")

         else:
            if (math.hypot(lmlist[4][1] - lmlist[8][1], lmlist[4][2] - lmlist[8][2]) < 15) and (lmlist[4][2] < lmlist[12][2]) and (lmlist[4][2] < lmlist[16][2]) and (lmlist[4][2] < lmlist[20][2]) and(lmlist[8][2] < lmlist[12][2]) and (lmlist[8][2] < lmlist[16][2]) and (lmlist[8][2] < lmlist[20][2]):
               self.xy_flag.append(0)
               if len(self.xy_flag) >= 10:
                  self.refresh_flags()
                  distance_x = lmlist[4][1] - 360
                  distance_y = lmlist[4][2] - 250
                  tdistance_x, tdistance_y = 0, 0

                  if -220 > distance_x >= -330:
                     tdistance_x = -self.x_step * 2
                  elif -110 > distance_x >= -220:
                     tdistance_x = -self.x_step
                  elif 220 >= distance_x > 110:
                     tdistance_x = self.x_step
                  elif 330 >= distance_x > 220:
                     tdistance_x = self.x_step * 2

                  if -150 > distance_y >= -220:
                     tdistance_y = self.y_step * 2
                  elif -70 > distance_y >= -150:
                     tdistance_y = self.y_step
                  elif 150 >= distance_y > 70:
                     tdistance_y = -self.y_step
                  elif 220 >= distance_y > 150:
                     tdistance_y = -self.y_step * 2

                  self.change_xy.emit(tdistance_x, tdistance_y)

   # Транслятор движений руки с канала видеокамеры на верхний слой
   def translator(self, lmlist):
      # Делаем копию оригинального фона
      self.cache = self.back.copy()

      if lmlist:
         for elem in lmlist:
            # Рисуем круг на каждой опорной точке
            cv2.circle(self.cache, (elem[1]+280, elem[2]+260), 5, (50, 0, 255, 255), cv2.FILLED)
            if not self.flag:
               # Опорная точка
               cv2.circle(self.cache, (641, 508), 5, (255, 255, 0, 255), cv2.FILLED) # ЦЕНТР

      # Преобразуем массив значений в формат QImage
      self.cache = cv2.cvtColor(self.cache, cv2.COLOR_BGR2RGBA)
      height, width, channel = self.cache.shape
      bytesPerLine = channel * width
      qImg = QImage(self.cache.data, width, height, bytesPerLine, QImage.Format_RGBA8888)
      # Отправляем скомпонованное изображение в UI
      self.change_translator.emit(qImg)

   # Начало работы видеокамеры
   def start_capture(self):
      self.cap1 = cv2.VideoCapture(self.camera_index, cv2.CAP_DSHOW)

   # Конец работы видеокамеры
   def stop_capture(self):
      if self.cap1:
         self.cap1.release()
         self.cap1 = None

   def run(self):
      self.start_capture()
      while True:
         ret1, image1 = self.cap1.read()
         if ret1:
            im1 = cv2.cvtColor(self.find_hands(image1), cv2.COLOR_BGR2RGB)
            lmList = self.find_position(image1)
            self.translator(lmList)
            self.on_build(lmList)
            height1, width1, channel1 = im1.shape
            step1 = channel1 * width1
            qImg1 = QImage(im1.data, width1, height1, step1, QImage.Format_RGB888)
            self.change_camera.emit(qImg1)