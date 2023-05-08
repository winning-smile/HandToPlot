from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal, QTime
from PyQt5.QtGui import QImage, QPixmap
import PyQt5.QtGui
import numpy as np
import mediapipe as mp
import cv2
import math
import qimage2ndarray

class handDetector(QThread):
   changePixmap = pyqtSignal(QImage)
   changePixmap2 = pyqtSignal(QImage)
   graph = pyqtSignal(str)

   def __init__(self, mode=False, maxHands=1, detectionCon=1, trackCon=0.5):
      super().__init__()
      self.cap1 = None
      self.mode = mode
      self.maxHands = maxHands
      self.detectionCon = detectionCon
      self.trackCon = trackCon
      self.mpHands = mp.solutions.hands
      self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.detectionCon, self.trackCon)
      self.mpDraw = mp.solutions.drawing_utils
      self.signal = "clear"
      self.back = cv2.imread('test3.png')

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

         flag = all(elem > 450 for elem in tmparr)
         tmparr = []

         if flag:
            # парабола done
            if (math.hypot(lmlist[4][1] - lmlist[14][1], lmlist[4][2] - lmlist[14][2]) < 10) and (lmlist[8][2] < lmlist[16][2]) and (lmlist[8][2] < lmlist[20][2]) and (lmlist[12][2] < lmlist[16][2]) and (lmlist[12][2] < lmlist[20][2]):
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

   # Транслятор движений руки с канала видеокамеры на верхний слой
   def translator(self, lmlist):
      # Делаем копию оригинального фона
      self.cache = self.back.copy()

      if lmlist:
         for elem in lmlist:
            # Рисуем круг на каждой опорной точке
            cv2.circle(self.cache, (elem[1], elem[2]), 10, (255, 0, 255), cv2.FILLED)

      # Преобразуем массив значений в формат QImage
      self.cache = cv2.cvtColor(self.cache, cv2.COLOR_BGR2RGB)
      height, width, channel = self.cache.shape
      bytesPerLine = 3 * width
      qImg = QImage(self.cache.data, width, height, bytesPerLine, QImage.Format_RGB888)
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
            #self.on_build(lmList)
            self.translator(lmList)
            height1, width1, channel1 = im1.shape
            step1 = channel1 * width1
            qImg1 = QImage(im1.data, width1, height1, step1, QImage.Format_RGB888)
            self.changePixmap.emit(qImg1)