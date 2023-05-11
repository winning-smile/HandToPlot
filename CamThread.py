from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal, QTime
from PyQt5.QtGui import QImage, QPixmap
import PyQt5.QtGui
import numpy as np
import time
import mediapipe as mp
import cv2
import math

class handDetector(QThread):
   change_camera = pyqtSignal(QImage)
   change_translator = pyqtSignal(QImage)
   change_graph = pyqtSignal(str)
   change_mode = pyqtSignal(bool)

   def __init__(self, mode=False, maxHands=1, detectionCon=1, trackCon=0.5):
      super().__init__()
      # Камера
      self.cap1 = None
      self.mode = mode
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
      self.back = cv2.imread('back.png', cv2.IMREAD_UNCHANGED)
      # Буффер для смены режима
      self.t = []
      # Флаг для смены режима
      self.flag = False

   # Модель находит на каждом кадре скелет руки и возвращает изображение с нарисованным скелетом
   def findHands(self, img, draw=True):
      imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
      self.results = self.hands.process(imgRGB)

      if self.results.multi_hand_landmarks:
         for handLms in self.results.multi_hand_landmarks:
            if draw:
               self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
      return img

   # Возвращает массив координат всех опорных точек
   def findPosition(self, img, handNo=0, draw=True):
      self.lmList = []
      if self.results.multi_hand_landmarks:
         myHand = self.results.multi_hand_landmarks[handNo]
         for id, lm in enumerate(myHand.landmark):
            h, w, c = img.shape
            cx, cy = int(lm.x * w), int(lm.y * h)
            self.lmList.append([id, cx, cy])

      return self.lmList

   # Функция детекции жестов для построения графиков
   def on_build(self, lmlist):
      tmparr = []
      if lmlist:
         for i in range(len(lmlist)):
            tmparr.append(lmlist[i][1])

         build = all(elem > 450 for elem in tmparr)
         change = all(elem < 450 for elem in tmparr)
         tmparr = []

         #if change:
            #if (math.hypot(lmlist[4][1] - lmlist[8][1], lmlist[4][2] - lmlist[8][2]) < 10) and (lmlist[12][2] < lmlist[4][2]) and (lmlist[12][2] < lmlist[4][2]) and (lmlist[4][2] > lmlist[12][1]) and (lmlist[8][1] > lmlist[12][1]):
               ##self.graph.emit("cubic")
               #print("poop")

         if build:
            # парабола done
            if (math.hypot(lmlist[4][1] - lmlist[14][1], lmlist[4][2] - lmlist[14][2]) < 10) and (lmlist[8][2] > lmlist[16][2]) and (lmlist[8][2] > lmlist[20][2]) and (lmlist[12][2] > lmlist[16][2]) and (lmlist[12][2] > lmlist[20][2]):
               self.graph.emit("cubic")
            # гипербола done
            elif (math.hypot(lmlist[4][1] - lmlist[18][1], lmlist[4][2] - lmlist[18][2]) < 10) and (lmlist[8][2] < lmlist[20][2]) and (lmlist[12][2] < lmlist[20][2]) and (lmlist[16][2] < lmlist[20][2]):
               self.graph.emit("quadro")
            # синус done
            elif (math.hypot(lmlist[4][1] - lmlist[5][1], lmlist[4][2] - lmlist[5][2]) < 20) and (lmlist[8][2] < lmlist[12][2]) and (lmlist[8][2] < lmlist[16][2]) and (lmlist[8][2] < lmlist[20][2]):
               self.graph.emit("sin")
            # косинус done
            elif (math.hypot(lmlist[4][1] - lmlist[12][1], lmlist[4][2] - lmlist[12][2]) < 10) and (lmlist[8][2] < lmlist[12][2]):
               self.graph.emit("cos")
            # круг done
            #if (math.hypot(lmlist[4][1] - lmlist[8][1], lmlist[4][2] - lmlist[8][2]) < 10) and (lmlist[12][2] < lmlist[8][2]):
               #self.graph.emit("circle")
            # очистка done
            elif (lmlist[4][2] < lmlist[8][2]) and (lmlist[4][2] < lmlist[12][2]) and (lmlist[4][2] < lmlist[16][2]) and (lmlist[4][2] < lmlist[20][2]):
               self.graph.emit("clear")

   # Смена флага изменения/построения
   def changeFlag(self):
      if self.flag:
         self.flag = False
         self.change_mode.emit(self.flag)
      else:
         self.flag = True
         self.change_mode.emit(self.flag)

   # Функция детекции жестов для построения графиков
   def on_build_new(self, lmlist):
      tmparr = []

      if lmlist:
         for i in range(len(lmlist)):
            tmparr.append(lmlist[i][1])

         # Переход в режим изменения/построения
         if (math.hypot(lmlist[4][1] - lmlist[8][1], lmlist[4][2] - lmlist[8][2]) < 20) and (lmlist[12][2] < lmlist[4][2]) and (lmlist[12][2] < lmlist[8][2]) and (lmlist[4][1] > lmlist[12][1]) and (lmlist[8][1] > lmlist[12][1]):
            self.t.append(0)
            if len(self.t) >= 30:
               self.t.clear()
               self.changeFlag()
               time.sleep(1)

   # Транслятор движений руки с канала видеокамеры на верхний слой
   def translator(self, lmlist):
      # Делаем копию оригинального фона
      self.cache = self.back.copy()

      if lmlist:
         for elem in lmlist:
            # Рисуем круг на каждой опорной точке
            cv2.circle(self.cache, (elem[1]+280, elem[2]+260), 5, (50, 0, 255, 255), cv2.FILLED)

      # Преобразуем массив значений в формат QImage
      self.cache = cv2.cvtColor(self.cache, cv2.COLOR_BGR2RGBA)
      height, width, channel = self.cache.shape
      bytesPerLine = channel * width
      qImg = QImage(self.cache.data, width, height, bytesPerLine, QImage.Format_RGBA8888)
      # Отправляем скомпонованное изображение в UI
      self.changePixmap2.emit(qImg)

   # Начало работы видеокамеры
   def start_capture(self):
      self.cap1 = cv2.VideoCapture(0, cv2.CAP_DSHOW)

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
            im1 = cv2.cvtColor(self.findHands(image1), cv2.COLOR_BGR2RGB)
            lmList = self.findPosition(image1)
            self.translator(lmList)
            self.on_build_new(lmList)
            height1, width1, channel1 = im1.shape
            step1 = channel1 * width1
            qImg1 = QImage(im1.data, width1, height1, step1, QImage.Format_RGB888)
            self.changePixmap.emit(qImg1)