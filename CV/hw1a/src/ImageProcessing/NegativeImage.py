#!/usr/bin/env python3
# coding:utf-8
#
# Copyright (c) 2014 Chun-Hsien Lin (D03922030). All right reserved.
"""
電腦視覺作業 #1
2014.09.19 v.0.1
讀入 lena.bmp 圖檔後，將該圖檔做成負片效果後輸出。
使用 Pillow 程式庫來處理圖檔的讀寫。
(http://pillow.readthedocs.org/en/latest/index.html)
"""
from __future__ import print_function
from PIL import Image

try:
    im = Image.open("lena.bmp", "r")
    im.load() # load image data into memory.
    imList = list(im.getdata()) # Get the image data, then convert each pixel to an ordinary sequence.
#
# This loop dealing with image negative pixel by pixel.
    for i in range(len(imList)):
        imList[i] = 255 - imList[i]
# Restore the negative image data 
    im.putdata(imList)
#    print(im.format, im.size, im.mode)
#    print(imList)
    im.show()
    im.save("NegLena.bmp")
    im.close()
except IOError:
    print("cannot open lena")