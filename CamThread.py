from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap
import numpy as np
import mediapipe as mp
import cv2
import math

class handDetector(QThread):
   changePixmap = pyqtSignal(QImage)
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

   def findHands(self, img, draw=True):
      imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
      self.results = self.hands.process(imgRGB)
      self.lmList = []

      if self.results.multi_hand_landmarks:
         for handLms in self.results.multi_hand_landmarks:
            if draw:
               self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
      return img

   def findPosition(self, img, handNo=0, draw=True):
      self.lmList = []
      if self.results.multi_hand_landmarks:
         myHand = self.results.multi_hand_landmarks[handNo]
         for id, lm in enumerate(myHand.landmark):
            h, w, c = img.shape
            cx, cy = int(lm.x * w), int(lm.y * h)
            self.lmList.append([id, cx, cy])
            #print(id, cx, cy)

      return self.lmList

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


   def start_capture(self):
      self.cap1 = cv2.VideoCapture(0, cv2.CAP_DSHOW)

   def stop_capture(self):
      if self.cap1:
         self.cap1.release()
         self.cap1 = None

   def run(self):
      self.start_capture()
      #self.cap1.set(3, 240)
      #self.cap1.set(4, 240)
      #self.cap1.set(5, 30)
      while True:
         ret1, image1 = self.cap1.read()
         if ret1:
            im1 = cv2.cvtColor(self.findHands(image1), cv2.COLOR_BGR2RGB)
            lmList = self.findPosition(image1)
            self.on_build(lmList)
            height1, width1, channel1 = im1.shape
            step1 = channel1 * width1
            qImg1 = QImage(im1.data, width1, height1, step1, QImage.Format_RGB888)
            self.changePixmap.emit(qImg1)

   def stop(self):
      self.stop_capture(self)
      super().stop()