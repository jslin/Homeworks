#!/usr/bin/env python2
# coding:utf-8
#
# Copyright (c) 2014 Chun-Hsien Lin (D03922030). All right reserved.
'''
Created on 2014/10/01

@author: Chun-Hsien Lin (D03922030)
電腦視覺作業HW2 #1
2014.10.01 v.0.1
讀入 lena.im 圖檔後，建立一個threshold = 128 的 binarize image。
接著計算該binarize image的connected components。採用 4-connected 及
8-connected。
使用 Pillow 程式庫來處理 BMP 圖檔的讀寫。
(http://pillow.readthedocs.org/en/latest/index.html)
'''
from __future__ import print_function
from PIL import Image
import struct

newIm = Image.new("L",(512,512), 128) # Create a blank image, fill up with color = 128.
imList =[]
# Open Lena.im
try:
    f = open("lena.im", "rb")
    f.seek(172) # The first 172 bytes are header. Skip them.
    byte = f.read(1)
    while byte != "":
        # Unpack byte data into list value.
        imList.append(struct.unpack('B', byte[0])[0])
        # Do stuff with byte.
        byte = f.read(1)
    newIm.putdata(imList)
    newIm.show()
except IOError:
    print("cannot open lena")
finally:
    f.close()

binIm = newIm.copy()
dList = []
rowList =[]
width = newIm.size[0]
height = newIm.size[1]

try:
#
# Binarize
    threshold = 128
    for j in range(height):
        for i in range(width):
            pix_val = binIm.getpixel((i,j))
            if pix_val >= threshold :
                rowList.append(255)
                binIm.putpixel((i,j), 255)
            else:
                rowList.append(0)
                binIm.putpixel((i,j), 0)
        dList.insert(j, rowList) # Let dList be row-major.
    binIm.putdata(dList)
    binIm.load()
    binIm.show()
#
# Labeling
#
# Initialization of each 1-pixel with a unique label.
#
    NEWLABEL = 1
    BLANK = 0
    labList = []
    for j in range(height):
        rowList = []
        for i in range(width):
            if dList[i][j] == 255 :
                rowList.append(NEWLABEL)
                NEWLABEL = NEWLABEL + 1
            else:
                rowList.append(BLANK)
#            print(i, j, dList[i][j], rowList[i])
        labList.insert(j, rowList)
#
# First top-down pass for labeled image.
# Using 4-connected operator.
#
    pre_label = labList[0][0]
    curr_label = labList[1][0]
    min_label = 1
    labChanged = True
    while labChanged:
        labChanged = False
        for j in range(height):
            for i in range(width):
                if labList[i][j] <> 0:
                    min_label = labList[i][j]
                pass
except TypeError:
    print("Type error")
except ValueError:
    print("Parameter Value error") 