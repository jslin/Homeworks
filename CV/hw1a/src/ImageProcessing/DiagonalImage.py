#!/usr/bin/env python3
# coding:utf-8
#
# Copyright (c) 2014 Chun-Hsien Lin (D03922030). All right reserved.
"""
電腦視覺作業 #4
2014.09.19 v.0.1
讀入 lena.bmp 圖檔後，將該圖檔對角鏡射後輸出。
使用 Pillow 程式庫來處理圖檔的讀寫。
(http://pillow.readthedocs.org/en/latest/index.html)
"""
from __future__ import print_function
from PIL import Image

try:
    im = Image.open("lena.bmp", "r")
    im.load() # load image data into memory.
    width = im.size[0]
    height = im.size[1]
    imList = list(im.getdata()) # Get the image data, then convert each pixel to an ordinary sequence.
    dList = []
#
# This loop dealing with image data into 2 dimension list pixel by pixel.
    for i in range(height):
        dList.insert(i, imList[i*width:(i+1)*width])
   
#   Diagonally mirrored the image.
    for i in range(1, len(dList)):
        for j in range(i):
#            print("Before swap, i=", i,"j=",j, dList[i][j], dList[j][i])
            dList[i][j], dList[j][i] = dList[j][i], dList[i][j]
#            print("After swap, i=", i,"j=",j, dList[i][j], dList[j][i])
# Restore the up-side-down image data to image buffer.
    im.putdata(dList)
    im.show()
#    im.save("DLena.bmp")
    im.close()
# For test Python's list elements swap function.
#    a = [[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]]
#    for i in range(1,len(a)):
#        for j in range(i):
#            a[i][j], a[j][i] = a[j][i], a[i][j]
#    print(len(a), a)
except IOError:
    print("cannot open lena")
except IndexError:
    print("Index error", i,j)
except TypeError:
    print("Type error: dList[", i,"][",j,"]", dList[i][j])
    print(dList[i][j])