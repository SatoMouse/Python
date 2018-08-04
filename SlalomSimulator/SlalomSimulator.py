#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.backends.backend_qt5agg
import SlalomSimulator_GUI as gui

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.Qt import *

half = 1

class Maze(QWidget):
  def __init__(self):
    QWidget.__init__(self)
    self.main_widget = QWidget(self)

    self.fig = matplotlib.figure.Figure()

    self.axes = self.fig.add_subplot(111)
    self.fig.set_facecolor("black")

    self.axes.patch.set_facecolor('black')
    self.axes.tick_params(labelbottom='off', labelleft='off')
    self.axes.tick_params(top='off', bottom='off', left='off', right='off')
    
    self.axes.set_xlim(-10 / half, 370 / half)
    self.axes.set_ylim(-10 / half, 370 / half)

    aspect = (self.axes.get_xlim()[1] - self.axes.get_xlim()[0]) / (self.axes.get_ylim()[1] - self.axes.get_ylim()[0])
    self.axes.set_aspect(aspect)

    figCanvas = matplotlib.backends.backend_qt5agg.FigureCanvasQTAgg(self.fig)

    layout = QVBoxLayout(self.main_widget)
    layout.addWidget(figCanvas)

    self.fig.tight_layout()
    self.setLayout(layout)

  def plot(self):
    global half
    self.axes.set_xlim(-10 / half, 370 / half)
    self.axes.set_ylim(-10 / half, 370 / half)
    c1 = "gray"
    lw1 = 0.5
    self.sectionWidth = 180 / half
    w0 = self.sectionWidth*0
    w1 = self.sectionWidth/2
    w2 = self.sectionWidth
    w3 = self.sectionWidth*3/2
    w4 = self.sectionWidth*2
    self.lines = []
    self.lines.append(self.axes.hlines(y=w1, xmin=w0, xmax=w4, color=c1, lw=lw1))
    self.lines.append(self.axes.hlines(y=w2, xmin=w0, xmax=w4, color=c1, lw=lw1))
    self.lines.append(self.axes.hlines(y=w3, xmin=w0, xmax=w4, color=c1, lw=lw1))
    self.lines.append(self.axes.vlines(x=w1, ymin=w0, ymax=w4, color=c1, lw=lw1))
    self.lines.append(self.axes.vlines(x=w2, ymin=w0, ymax=w4, color=c1, lw=lw1))
    self.lines.append(self.axes.vlines(x=w3, ymin=w0, ymax=w4, color=c1, lw=lw1))
    self.lines.append(self.axes.plot([w0,w1], [w1,w0], color=c1, lw=lw1)[0])
    self.lines.append(self.axes.plot([w0,w1], [w3,w4], color=c1, lw=lw1)[0])
    self.lines.append(self.axes.plot([w3,w4], [w0,w1], color=c1, lw=lw1)[0])
    self.lines.append(self.axes.plot([w3,w4], [w4,w3], color=c1, lw=lw1)[0])
    self.lines.append(self.axes.plot([w0,w3], [w1,w4], color=c1, lw=lw1)[0])
    self.lines.append(self.axes.plot([w0,w3], [w3,w0], color=c1, lw=lw1)[0])
    self.lines.append(self.axes.plot([w1,w4], [w0,w3], color=c1, lw=lw1)[0])
    self.lines.append(self.axes.plot([w1,w4], [w4,w1], color=c1, lw=lw1)[0])

    self.rects = []
    self.rects.append(plt.Rectangle((w2-6/half,-6/half),12/half,w2+12/half,fc="r",ec='none'))
    self.rects.append(plt.Rectangle((-6/half,-6/half),12/half,w4+12/half,fc="r",ec='none'))
    self.rects.append(plt.Rectangle((-6/half,-6/half),w4+12/half,12/half,fc="r",ec='none'))
    self.rects.append(plt.Rectangle((w4-6/half,-6/half),12/half,w4+12/half,fc="r",ec='none'))
    self.rects.append(plt.Rectangle((-6/half,w4-6/half),w4+12/half,12/half,fc="r",ec='none'))
    
    for rect in self.rects:
      rect.set_zorder(9)
      self.axes.add_patch(rect)

  def clear(self):
    for rect in self.rects:
      rect.remove()
    for line in self.lines:
      line.remove()

class ApplicationWindow(QMainWindow):
  def __init__(self):
    QMainWindow.__init__(self)
    self.setWindowTitle("Slalom Simulator ver.2")

    self.main_widget = QWidget(self)

    self.mazeFig = Maze()

    self.interface = gui.Interface()
    self.interface.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.MinimumExpanding)

    layout = QHBoxLayout(self.main_widget)

    layout.addWidget(self.mazeFig)
    layout.addWidget(self.interface)

    matplotlib.pyplot.ion()

    self.setCentralWidget(self.main_widget)

class Turn:
  def __init__(self, parent=None):
    self.targetAngle = 90
    self.velocity = 300
    self.CurveR = 10.0
    self.Offset = 0
    self.targetX = 180 / half
    self.targetY = 270 / half
    self.mode = 0
  def setTurn(self, value):
    global half
    self.mode = value
    if self.mode == 0:
      self.targetAngle = 90
      self.targetX = 180 / half - self.Offset
      self.targetY = 270 / half
    elif self.mode == 1:
      self.targetAngle = 90
      self.targetX = 270 / half
      self.targetY = 270 / half
    elif self.mode == 2:
      self.targetAngle = 180
      self.targetX = 270 / half
      self.targetY =  90 / half
    elif self.mode == 3:
      self.targetAngle = 45
      self.targetX = 135 / half
      self.targetY = 225 / half
    elif self.mode == 4:
      self.targetAngle = 135
      self.targetX = 225 / half
      self.targetY = 225 / half
    elif self.mode == 5:
      self.targetAngle = 90
      self.targetX = 270 / half - self.Offset * np.sin(np.pi/4)
      self.targetY = 180 / half + self.Offset * np.cos(np.pi/4)
  def setVelocity(self, value):
    if(value != ""):
      self.velocity = abs(int(value))
  def setTargetAngle(self, value):
    if(value != ""):
      self.targetAngle = abs(float(value))
  def setCurvatureR(self, value):
    if(value != ""):
      self.CurveR = abs(float(value))
  def setOffset(self, value):
    if(value != ""):
      self.Offset = abs(int(value))
#     self.setTurn(self.mode)

class SlalomTrack:
  def __init__(self, parent=None):
    self.turn = Turn()
    self.flag1 = 0
    self.flag2 = 0
    self.flag3 = 0
    self.time = 0
    self.plotFlag = 0
    self.finishFlag = 0
    self.finishCurveRFlag = 0
    self.Divider = 5
    self.HelixAngle = 0.0
    self.MaxAngVel = 0.0
    self.MaxAngAcc = 0.0
    self.Time1 = 0.0
    self.Time2 = 0.0

  def calculate(self, axes):
    global half
    self.time = 0.0
    Angle = 0
    if self.turn.mode == 5:
      Angle = 45 * np.pi / 180
    self.HelixAngle = (self.turn.targetAngle * np.pi / 180) / self.Divider
    self.MaxAngVel = self.turn.velocity / self.turn.CurveR
    self.Time1 = 2 * self.HelixAngle / self.MaxAngVel
    self.Time2 = (self.turn.targetAngle * np.pi / 180) / self.MaxAngVel
    self.MaxAngAcc = self.MaxAngVel / self.Time1

    AngVel2 = 0.0
    Angle2 = 0
    self.SlipAngle = 0
    Milli = 0.001
    K = 100

#    convert = pi / 180
    i = 0
    X2 = []
    Y2 = []
    X3 = []
    Y3 = []
    X4 = []
    Y4 = []
    X5 = []
    Y5 = []
    Indent = 180/half

    def AngAcc():
      if self.time <= self.Time1:
        return self.MaxAngAcc
      if self.time <= self.Time2:
        return 0
      if self.time <= self.Time1 + self.Time2:
        return -self.MaxAngAcc
      return 0

    if self.turn.mode == 0 or self.turn.mode == 5:
      Indent = 180 / half
    else:
      Indent = 90 / half


    if self.plotFlag == 1:
      if self.turn.mode == 3:
        self.line7 = axes.plot([135/half,135/half],   [0, 360/half],  color= "green", linewidth=1)[0]
        self.flag2 = 1
        self.flag3 = 0
      elif self.turn.mode == 4:
        self.line8 = axes.plot([225/half,225/half],   [0, 360/half],  color= "green", linewidth=1)[0]
        self.flag2 = 0
        self.flag3 = 1
      elif self.turn.mode == 5:
        self.line7 = axes.plot([90/half,90/half],   [0, 360/half],  color= "green", linewidth=1)[0]
        self.line8 = axes.plot([270/half,270/half],   [0, 360/half],  color= "green", linewidth=1)[0]
        self.flag2 = 1
        self.flag3 = 1
      else:
        self.flag2 = 0
        self.flag3 = 0

    MouseWidth = 36

    if self.turn.mode == 5:
      X2.append(90/half + self.turn.Offset * np.cos(np.pi/4))
      Y2.append(Indent + self.turn.Offset * np.cos(np.pi/4))
      X3.append(90/half + self.turn.Offset * np.cos(np.pi/4))
      Y3.append(Indent + self.turn.Offset * np.cos(np.pi/4))

      X4.append(90/half + (self.turn.Offset + MouseWidth / 2)* np.sin(np.pi/4))
      X5.append(90/half + (self.turn.Offset - MouseWidth / 2)* np.sin(np.pi/4))
      Y4.append(Indent + (self.turn.Offset - MouseWidth / 2)* np.cos(np.pi/4))
      Y5.append(Indent + (self.turn.Offset + MouseWidth / 2)* np.cos(np.pi/4))
    else:
      X2.append(90/half)
      Y2.append(Indent + self.turn.Offset)
      X3.append(90/half)
      Y3.append(Indent + self.turn.Offset)

      X4.append(90/half + MouseWidth / 2)
      X5.append(90/half - MouseWidth / 2)
      Y4.append(Indent + self.turn.Offset)
      Y5.append(Indent + self.turn.Offset)

    #スラローム軌道
    while self.time <= self.Time1 + self.Time2:
      AngVel2 += AngAcc() * Milli
      Angle += AngVel2 * Milli
      self.SlipAngle = (self.SlipAngle / Milli - AngVel2) / (1 / Milli + K / (self.turn.velocity * Milli))
      Angle2 = Angle + self.SlipAngle
      X2.append(X2[i] + self.turn.velocity * np.sin(Angle) * Milli)
      Y2.append(Y2[i] + self.turn.velocity * np.cos(Angle) * Milli)
      X3.append(X3[i] + self.turn.velocity * np.sin(Angle2) * Milli)
      Y3.append(Y3[i] + self.turn.velocity * np.cos(Angle2) * Milli)

      X4.append(X3[i+1] + MouseWidth / 2 * np.sin(Angle2 + np.pi / 2))
      Y4.append(Y3[i+1] + MouseWidth / 2 * np.cos(Angle2 + np.pi / 2))

      X5.append(X3[i+1] - MouseWidth / 2 * np.sin(Angle2 + np.pi / 2))
      Y5.append(Y3[i+1] - MouseWidth / 2 * np.cos(Angle2 + np.pi / 2))

      self.time += 0.001
      i += 1
    if self.plotFlag == 0 and X3[i] > self.turn.targetX:
      self.finishFlag = 1
    if self.plotFlag == 0 and self.finishCurveRFlag == 1 and (self.turn.mode == 3 or self.turn.mode == 4):
      self.turn.Offset = (int)(self.turn.targetY - Y3[i])
    if self.plotFlag == 1:
      #スラローム軌道のプロット
      self.lines = []
      self.lines.append(axes.plot(X2,  Y2, color="yellow")[0])
      self.lines.append(axes.plot(X3,  Y3, color="cyan"  )[0])
      self.lines.append(axes.plot(X4,  Y4, color="orange")[0])
      self.lines.append(axes.plot(X5,  Y5, color="orange")[0])
      self.flag1 = 1
  def autoCalculate(self,axes):
    global half
    self.clear()
    self.turn.CurveR = 10.0
    self.finishFlag = 0
    self.plotFlag = 0
    if self.turn.mode == 0 and self.turn.Offset > 30.0 / half:
      self.turn.setOffset(30.0 / half)
    if(self.turn.mode == 3 or self.turn.mode == 4):
      self.turn.setOffset(0.0)
    while True:
      self.calculate(axes)
      if self.finishFlag == 1:
        self.turn.CurveR -= 10.0
        self.finishFlag = 0
        break
      self.turn.CurveR += 10.0
    while True:
      self.calculate(axes)
      if self.finishFlag == 1:
        self.turn.CurveR -= 1.0
        self.finishFlag = 0
        break
      self.turn.CurveR += 1.0
    while True:
      self.calculate(axes)
      if self.finishFlag == 1:
        self.turn.CurveR -= 0.1
        self.finishFlag = 0
        break
      self.turn.CurveR += 0.1
    while True:
      self.calculate(axes)
      if self.finishFlag == 1:
        self.turn.CurveR -= 0.01
        self.finishFlag = 0
        break
      self.turn.CurveR += 0.01
    self.finishCurveRFlag = 1
    self.calculate(axes)
    self.finishCurveRFlag = 0
    self.calculate(axes)
  def plot(self, axes):
    self.plotFlag = 1
    self.calculate(axes)
    self.plotFlag = 0
  def remove(self):
    if(self.flag1 == 1):
      for line in self.lines:
        line.remove()
    if(self.flag2 == 1):
      self.line7.remove()
    if(self.flag3 == 1):
      self.line8.remove()
  def clear(self):
    self.plotFlag = 0
    if(self.flag1 == 1):
      for line in self.lines:
        line.remove()
      self.flag1 = 0
    if(self.flag2 == 1):
      self.line7.remove()
      self.flag2 = 0
    if(self.flag3 == 1):
      self.line8.remove()
      self.flag3 = 0

def main():
  app = QApplication(sys.argv)
  track = SlalomTrack()
  mainWindow = ApplicationWindow()
  mainWindow.mazeFig.plot()
  def setDisabled(boolValue=True):
    mainWindow.interface.check.check.setEnabled(not boolValue)
    mainWindow.interface.lineEditVel.lineEdit.setEnabled(not boolValue)
    mainWindow.interface.lineEditCurvatureR.lineEdit.setEnabled(not boolValue)
    mainWindow.interface.lineEditOffset.lineEdit.setEnabled(not boolValue)
    mainWindow.interface.combo.combo.setEnabled(not boolValue)
    mainWindow.interface.excuteButton.setEnabled(not boolValue)
    mainWindow.interface.clearButton.setEnabled(not boolValue)
    mainWindow.interface.autoButton.setEnabled(not boolValue)
    mainWindow.interface.exitButton.setEnabled(not boolValue)
  def displayTrack():
    setDisabled()
    track.remove()
    track.plot(mainWindow.mazeFig.axes)
    mainWindow.mazeFig.fig.canvas.draw()
    mainWindow.interface.lineEditSlipAngle.lineEdit.setText("%.2f" % float(-track.SlipAngle * 180 / np.pi))
    mainWindow.interface.lineEditMaxAngVel.lineEdit.setText("%.2f" % float(track.MaxAngVel * 180 / np.pi))
    mainWindow.interface.lineEditMaxAngAccel.lineEdit.setText("%.2f" % float(track.MaxAngAcc *180 / np.pi))
    setDisabled(False)
  def calculate():
    setDisabled()
    track.autoCalculate(mainWindow.mazeFig.axes)

    mainWindow.interface.lineEditCurvatureR.lineEdit.setText("%.2f" % track.turn.CurveR)
    mainWindow.interface.lineEditOffset.lineEdit.setText("%d" % track.turn.Offset)
    mainWindow.mazeFig.fig.canvas.draw()
    displayTrack()
  def clearTrack():
    track.clear()
    mainWindow.interface.lineEditMaxAngVel.lineEdit.setText("0.00")
    mainWindow.interface.lineEditMaxAngAccel.lineEdit.setText("0.00")
    mainWindow.mazeFig.fig.canvas.draw()
  # save image file of matplotlib graph
  #canvas = matplotlib.backends.backend_agg.FigureCanvasAgg(fig[0][0])
  #canvas.print_figure("qt4mpl.png")

  def changeHalf(state):
    global half
    if state == Qt.Checked:
      half = 2
    else:
      half = 1
    mainWindow.mazeFig.clear()
    mainWindow.mazeFig.plot()
    mainWindow.mazeFig.fig.canvas.draw()
    track.turn.setTurn(track.turn.mode)
    
  def setTurn(value):
    track.turn.setTurn(value)
    mainWindow.interface.lineEditTargetAngle.lineEdit.setText("%.2f" % track.turn.targetAngle)

  mainWindow.interface.check.check.stateChanged.connect(changeHalf)
  mainWindow.interface.combo.combo.activated[int].connect(setTurn)
  mainWindow.interface.lineEditVel.lineEdit.textChanged[str].connect(track.turn.setVelocity)
  mainWindow.interface.lineEditTargetAngle.lineEdit.textChanged[str].connect(track.turn.setTargetAngle)
  mainWindow.interface.lineEditCurvatureR.lineEdit.textChanged[str].connect(track.turn.setCurvatureR)
  mainWindow.interface.lineEditOffset.lineEdit.textChanged[str].connect(track.turn.setOffset)
  mainWindow.interface.excuteButton.clicked.connect(displayTrack)
  mainWindow.interface.clearButton.clicked.connect(clearTrack)
  mainWindow.interface.autoButton.clicked.connect(calculate)
  mainWindow.interface.exitButton.clicked.connect(mainWindow.close)

  mainWindow.show()

  app.exec_()

if __name__ == "__main__":
  main()