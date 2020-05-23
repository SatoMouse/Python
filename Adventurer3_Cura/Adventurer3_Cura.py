# coding: UTF-8
import os
import codecs
import glob

#スクリプト配置フォルダのファイル一覧取得
files = glob.glob("*.gcode")
for file in files:
  #読み込み
  rFile = codecs.open(file, 'r', 'cp932')
  lines = rFile.readlines()
  rFile.close()
  
  wLines = []
  for line in lines:
    if not line.endswith(' T0\r\n'):
      if line.startswith('M104') or line.startswith('M140'):
        line = line.replace('\r\n','')
        line = line + ' T0\r\n'
    wLines.append(line) #別リストにする
  #書き込み
  wFile = codecs.open(file, 'w', 'cp932')
  wFile.write(''.join(wLines))
  wFile.close()
  name, ext = os.path.splitext(os.path.basename(file))
  os.rename(file, name + '.g')
