from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal
import numpy as np
import cv2

class CameraThread(QThread):
   image = pyqtSignal(np.ndarray)

   def __init__(self):
      super().__init__()
      self.capture = None

   def start_capture(self):
      self.capture = cv2.VideoCapture(0)

   def stop_capture(self):
      if self.capture:
         self.capture.release()
         self.capture = None

   def run(self):
      self.start_capture()
      while True:
         ret, frame = self.capture.read()
         if ret:
            self.image.emit(frame)

   def stop(self):
      self.stop_capture()
      super().stop()
