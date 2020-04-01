import cv2
import numpy as np
import matplotlib.pylab  as plt
import seaborn as sns
import pandas as pd
import math
from PIL import Image as image
import pytesseract


#全局自适应
def adaptive(img):
    blur = cv2.GaussianBlur(img, (3, 3), 0)
    th = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
    return th

#大津
def otsu(img):
    blur = cv2.GaussianBlur(img, (3, 3), 0)
    ret, th = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return th

#二值化
def thresholding(img):
  ad = adaptive(img)
  ot = otsu(img)
  tot = (1-ot/255)
  tad = (1-ad/255)
  add = 255-cv2.multiply(tot,tad).astype('uint8')*255
  return add

#逐行识别
def rowSegment(img):
  (row,col)=img.shape[0:2]
  print(row,col)
  thre = 245
  rowAvg = np.floor(np.mean(add,axis=1))

  start = 0
  end = -1
  enable = 0
  empcount = 0
  rowList = []
  for i in range(row):
      if rowAvg[i]<thre:
          enable = 1
      elif empcount >= 5 and end == -1:
          end = i
          # print(start," ",end)
          img = image.fromarray(cv2.cvtColor(add[start:end,:], cv2.COLOR_BGR2RGB))
          str = pytesseract.image_to_string((img), lang='chi_sim+eng')
          # img.show()
          rowList.append(str)
          empcount = 0
          start = i
          enable = 0
          end = -1
      elif rowAvg[i]>thre and abs(rowAvg[i]-rowAvg[i-1])<1 and enable == 1:
          empcount = empcount+1
  # print(rowList)
  return rowList


# img = cv2.imread('图片路径',0)
def rowOCR(img):
  add = thresholding(img)
  return rowSegment(add)


if __name__ == '__main__':
    img = cv2.imread('/home/python/Desktop/gitodk/odk/odk/utils/ocr/mark6.jpg',0)
    ret = rowOCR(img)
    print(ret)



