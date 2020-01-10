# -*- coding: utf-8 -*-

import cv2
import numpy as np

img = cv2.imread('form.png')

# BGR -> グレースケール
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# エッジ抽出 (Canny)
edges = cv2.Canny(gray, 1, 100, apertureSize=3)
cv2.imwrite('edges.png', edges)
# クロージング処理
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)

h, w = edges.shape[:2]
mask = np.zeros((h + 2, w + 2), dtype=np.uint8)

retval, edges, mask, rect = cv2.floodFill(edges, mask, seedPoint=(0, 0), newVal=(255, 255, 255))
edges = cv2.bitwise_not(edges)

#edges = cv2.erode(edges, kernel, iterations = 0.5)

cv2.imwrite('edges2.png', edges)
# 輪郭抽出
contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# 面積でフィルタリング
rects = []
  
for cnt, hrchy in zip(contours, hierarchy[0]):
  if cv2.contourArea(cnt) < 200:
    continue  # 面積が小さいものは除く
  #if hrchy[3] == -1:
  #  continue  # ルートノードは除く
  # 輪郭を囲む長方形を計算する。
  rect = cv2.minAreaRect(cnt)
  rect_points = cv2.boxPoints(rect).astype(int)
  rects.append(rect_points)

# x-y 順でソート
rects = sorted(rects, key=lambda x: (x[0][1], x[0][0]))

# 描画する。
for i, rect in enumerate(rects):
  color = np.random.randint(0, 255, 3).tolist()
  cv2.drawContours(img, rects, i, color, 2)
  #cv2.putText(img, str(i), tuple(rect[0]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

  print('rect:\n', rect)

cv2.imwrite('img.png', img)
