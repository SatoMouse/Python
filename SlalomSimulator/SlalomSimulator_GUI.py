#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.Qt import *

#from guidata.dataset.qtitemwidgets import HLayoutMixin

class CheckBox(QWidget):
  def __init__(self):
    QWidget.__init__(self)
    self.check = QCheckBox(self)
    layout = QVBoxLayout()
    layout.addWidget(self.check)
    self.setLayout(layout)
    
class ComboBox(QWidget):
  def __init__(self):
    QWidget.__init__(self)
    self.combo = QComboBox(self)
    layout = QVBoxLayout()
    layout.addWidget(self.combo)
    self.setLayout(layout)

class DoubleLineEdit(QWidget):
  def __init__(self):
    QWidget.__init__(self)
    self.lineEdit = QLineEdit(self)
    validator =  QDoubleValidator(self)
    self.lineEdit.setValidator(validator)
    layout = QVBoxLayout()
    layout.addWidget(self.lineEdit)
    layout.setAlignment(Qt.AlignCenter)
    self.setLayout(layout)

class IntLineEdit(QWidget):
  def __init__(self):
    QWidget.__init__(self)
    self.lineEdit = QLineEdit(self)
    validator =  QIntValidator(self)
    self.lineEdit.setValidator(validator)
    layout = QVBoxLayout()
    layout.addWidget(self.lineEdit)
    self.setLayout(layout)

class Interface(QWidget):
  def __init__(self):
    QWidget.__init__(self)

    self.check = CheckBox()

    self.combo = ComboBox()
    self.combo.combo.addItems([u"小回り90度", u"大回り90度", u"大回り180度", u"斜め45度", u"斜め135度", u"斜め90度"])
    #入力エリア
    self.lineEditVel = IntLineEdit()
    self.lineEditVel.lineEdit.setText("300")

    self.lineEditTargetAngle = DoubleLineEdit()
    self.lineEditTargetAngle.lineEdit.setText("90.00")

    self.lineEditCurvatureR = DoubleLineEdit()
    self.lineEditCurvatureR.lineEdit.setText("10.00")

    self.lineEditOffset = IntLineEdit()
    self.lineEditOffset.lineEdit.setText("0")

    self.lineEditSlipAngle = DoubleLineEdit()
    self.lineEditSlipAngle.lineEdit.setText("0.00")
    self.lineEditSlipAngle.lineEdit.setReadOnly(True)

    self.lineEditMaxAngVel = DoubleLineEdit()
    self.lineEditMaxAngVel.lineEdit.setText("0.00")
    self.lineEditMaxAngVel.lineEdit.setReadOnly(True)

    self.lineEditMaxAngAccel = DoubleLineEdit()
    self.lineEditMaxAngAccel.lineEdit.setText("0.00")
    self.lineEditMaxAngAccel.lineEdit.setReadOnly(True)

    #ボタンウィジェット
    self.excuteButton = QPushButton(u"表示")
    self.autoButton = QPushButton(u"自動")
    self.clearButton  = QPushButton(u"クリア")
    self.exitButton = QPushButton(u"終了")


    #レイアウト配置
    configLayout = QGridLayout()

    checkbox_label = QLabel(u"ハーフサイズ")
    configLayout.addWidget(checkbox_label,0,0)
    configLayout.addWidget(self.check,0,1)

    lineEditVel_label = QLabel(u"速度 [mm/s]")
    configLayout.addWidget(lineEditVel_label,1,0)
    configLayout.addWidget(self.lineEditVel,1,1)

    combo_label = QLabel(u"ターンの種類")
    configLayout.addWidget(combo_label,2,0)
    configLayout.addWidget(self.combo,2,1)

    lineEditTargetAngle_label = QLabel(u"目標角度 [°]")
    configLayout.addWidget(lineEditTargetAngle_label,3,0)
    configLayout.addWidget(self.lineEditTargetAngle,3,1)

    lineEditCurvatureR_label = QLabel(u"最大曲率半径 [mm]")
    configLayout.addWidget(lineEditCurvatureR_label,4,0)
    configLayout.addWidget(self.lineEditCurvatureR,4,1)

    lineEditOffset_label = QLabel(u"オフセット距離 [mm]")
    configLayout.addWidget(lineEditOffset_label,5,0)
    configLayout.addWidget(self.lineEditOffset,5,1)

    space = QLabel("")
    configLayout.addWidget(space,6,0)

    lineEditSlipAngle_label = QLabel(u"最終スリップ角 [°]")
    configLayout.addWidget(lineEditSlipAngle_label,7,0)
    configLayout.addWidget(self.lineEditSlipAngle,7,1)

    lineEditMaxAngVel_label = QLabel(u"最大角速度 [°/s]")
    configLayout.addWidget(lineEditMaxAngVel_label,8,0)
    configLayout.addWidget(self.lineEditMaxAngVel,8,1)

    lineEditMaxAngAccel_label = QLabel(u"最大角速度 [°/s^2]")
    configLayout.addWidget(lineEditMaxAngAccel_label,9,0)
    configLayout.addWidget(self.lineEditMaxAngAccel,9,1)

    buttonLayout = QGridLayout()

    buttonLayout.addWidget(self.excuteButton,0,0)
    buttonLayout.addWidget(self.autoButton,0,1)
    buttonLayout.addWidget(self.clearButton,1,0)
    buttonLayout.addWidget(self.exitButton,1,1)

    config = QWidget()
    config.setLayout(configLayout)

    button = QWidget()
    button.setLayout(buttonLayout)

    layout = QVBoxLayout()

    layout.addWidget(config)

    layout.addStretch()

    layout.addWidget(button)

    self.setLayout(layout)
