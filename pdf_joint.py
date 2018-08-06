# -*- coding:utf-8 -*-

import os
from PyPDF2 import PdfFileMerger

path = os.path.dirname(os.path.abspath(__file__))
os.chdir(path)

if os.path.exists('output') == False:
  os.mkdir('output')

filelist = []
files = os.listdir(path)

for file_name in files:
  body, ext = os.path.splitext(file_name)
  if ext == '.pdf':
    filelist.append(file_name)

filelist.sort()

merger = PdfFileMerger()

for file in filelist:
  merger.append(file)

merger.write(u'output\一式.pdf')
merger.close()
