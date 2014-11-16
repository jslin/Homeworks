#!/usr/bin/env python2
# coding:utf-8
#
# Copyright (c) 2014 Chun-Hsien Lin (D03922030). All right reserved.
"""
電腦視覺作業HW5 #1
2014.11.14 v.0.1
讀入 lena.bmp 圖檔後，將該圖檔做 mathematical morphology (gray scale Erosion)。
本模組處理灰階圖的 erosion 運算。
使用 Pillow 程式庫來處理圖檔的讀寫。
(http://pillow.readthedocs.org/en/latest/index.html)
"""
from __future__ import print_function
from PIL import Image

def grayErosion(imageBuffer, kernel):
    try:
        imageBuffer.load() # load image data into memory.
        width = imageBuffer.size[0]
        height = imageBuffer.size[1]
        inputIm = imageBuffer.copy()

    # Create a blank image, fill up with color = 0 (white).
        eroIm = Image.new("L",(width, height), 0)
    # Using Erosion definition to implement.
    #
        for i in range(width):
            for j in range(height):
                minValue = 255
                for k in range(len(kernel)):
                    p = kernel[k][0]
                    q = kernel[k][1]
                    value = kernel[k][2]
                    temp = inputIm.getpixel((i,j))
                    x = i + p
                    y = j + q
                    if (x >= 0) and (x < width) and (y >= 0) and (y < height):
                        temp = inputIm.getpixel((x,y)) - value
                    if temp < minValue:
                        minValue = temp
                    eroIm.putpixel((i,j), minValue)
        inputIm.close()
    except IOError:
        print("cannot open lena")
    finally:
        inputIm.close()
    return eroIm