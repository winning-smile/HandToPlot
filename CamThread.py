from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap
import numpy as np
import mediapipe as mp
import cv2

class handDetector(QThread):
   changePixmap = pyqtSignal(QImage)

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

   def findHands(self, img, draw=True):
      imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
      self.results = self.hands.process(imgRGB)
      self.lmList = []

      if self.results.multi_hand_landmarks:
         for handLms in self.results.multi_hand_landmarks:
            if draw:
               self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
      return img

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
            height1, width1, channel1 = im1.shape
            step1 = channel1 * width1
            qImg1 = QImage(im1.data, width1, height1, step1, QImage.Format_RGB888)
            self.changePixmap.emit(qImg1)

   def stop(self):
      self.stop_capture(self)
      super().stop()