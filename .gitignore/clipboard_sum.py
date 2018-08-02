# -*- coding: utf-8 -*-

import pyperclip
import time
import re
import sys

rawDatas = pyperclip.paste().split()
datas = []
nums = []

for rawData in rawDatas:
  nums = re.findall(r'([+-]?[0-9]+\.?[0-9]*)',rawData)
  if len(nums) == 1:
    datas.append(float(nums[0]))
  else:
    print(u"エラー")
    print(u"1行に数値が2箇所あります。")
    time.sleep(3)
    sys.exit()
print(sum(datas))
# pyperclip.copy(str(sum(datas))) #合計値をクリップボードにコピーする。
time.sleep(5)
