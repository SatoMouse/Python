# -*- coding: utf-8 -*-
import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import requests
import base64
import json
import pyperclip

height = 0
width = 0
minX = 0
minY = 0
maxX = 0
maxY = 0

GOOGLE_CLOUD_VISION_API_URL = 'https://vision.googleapis.com/v1/images:annotate?key='
API_KEY = 'API_KEY' # TODO 取得したAPIキーを入力してください。

# APIを呼び、認識結果をjson型で返す
def request_cloud_vison_api(image_base64):
  api_url = GOOGLE_CLOUD_VISION_API_URL + API_KEY
  req_body = json.dumps({
    'requests': [{
      'image': {
        'content': image_base64.decode('utf-8') # jsonに変換するためにstring型に変換する
      },
      'features': [{
        'type': 'TEXT_DETECTION', # ここを変更することで分析内容を変更できる
        'maxResults': 10,
      }]
    }]
  })
  res = requests.post(api_url, data=req_body)
  return res.json()

# 画像読み込み
def img_to_base64(filepath):
  with open(filepath, 'rb') as img:
    img_byte = img.read()
  return base64.b64encode(img_byte)

class Snapshot():
  def __init__(self):
    screen = QApplication.primaryScreen()
    self.img = screen.grabWindow(QApplication.desktop().winId())
  def trim(self):
    global minX
    global minY
    global maxX
    global maxY
    img2 =self.img.copy(QRect(minX, minY, (maxX - minX), (maxY - minY)))
    img2.save('temp.png')
    img_base64 = img_to_base64('temp.png')
    result = request_cloud_vison_api(img_base64)
    
    #認識した文字のみを出力
    rawDatas = result["responses"][0]["fullTextAnnotation"]["text"]
    rawDatas = rawDatas.replace(',', '')
    rawDatas = rawDatas.replace(' ', '')
    #rawDatas = rawDatas.replace('　', '')
    rawDatas = rawDatas.rstrip("\n")
    pyperclip.copy(str(rawDatas)) #クリップボードにコピー
    print(rawDatas)

class Window(QWidget):
  def __init__(self):
    QWidget.__init__(self)
    self.setWindowFlags(Qt.FramelessWindowHint)
    self.setAttribute(Qt.WA_TranslucentBackground)
    self.rubberband = QRubberBand(QRubberBand.Rectangle, self)
    self.setMouseTracking(True)
    self.showFullScreen()
    self.show()
  def paintEvent(self, event):
    painter = QPainter(self)
    painter.fillRect(0, 0, width, height, QColor(255, 255, 255, 1));
  def mouseMoveEvent(self,event):
    if self.rubberband.isVisible():
      self.rubberband.setGeometry(QRect(self.origin, event.pos()).normalized())
    QWidget.mouseMoveEvent(self, event)
  def mouseReleaseEvent(self, event):
    if self.rubberband.isVisible() == False:
      return
    global minX
    global minY
    global maxX
    global maxY
    self.rubberband.hide()
    minX = min(self.origin.x(), event.pos().x())
    maxX = max(self.origin.x(), event.pos().x())
    minY = min(self.origin.y(), event.pos().y())
    maxY = max(self.origin.y(), event.pos().y())
    QCoreApplication.instance().quit()
  def mousePressEvent(self, event):
    self.origin = event.pos()
    self.rubberband.setGeometry(QRect(self.origin, QSize()))
    self.rubberband.show()

def main():
  global height
  global width
  app = QApplication(sys.argv)
  height = app.desktop().height()
  width = app.desktop().width()
  snap = Snapshot()
  window = Window()
  
  app.exec_()
  snap.trim()
  sys.exit()

if __name__ == '__main__':
  main()
