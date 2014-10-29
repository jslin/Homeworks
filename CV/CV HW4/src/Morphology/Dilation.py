#!/usr/bin/env python2
# coding:utf-8
#
# Copyright (c) 2014 Chun-Hsien Lin (D03922030). All right reserved.
"""
電腦視覺作業HW4 #1
2014.10.22 v.0.1
讀入 lena.bmp 圖檔後，將該圖檔二元化(Threshold = 128)，
接著再做 mathematical morphology (Dilation)。
使用 Pillow 程式庫來處理圖檔的讀寫。
(http://pillow.readthedocs.org/en/latest/index.html)
"""
from __future__ import print_function
from PIL import Image

def dilation(imageBuffer, kernel):
    try:
        imageBuffer.load() # load image data into memory.
        width = imageBuffer.size[0]
        height = imageBuffer.size[1]
        binIm = imageBuffer.copy()
    # Dilation
    # Definition: 
    #      A dilation by B = 
    #      {x belong to Euclidean 2 space | x = a + b, for some a belong to A , and b belong to B.}
    # Description:
    #      Because of we dealing with binary image, using a list to store kernel. 
    #      Each list element is (x, y) coordinate tuple.
    # 
    # Create a blank image for dilation , fill up with color = 0 (white).
        dilIm = Image.new("L",(width, height), 0)
    # Using Dilation definition above to implement.
    #
        for i in range(width):
            for j in range(height):
                if binIm.getpixel((i, j)) == 255 :
                    for k in range(len(kernel)):
                        p = kernel[k][0]
                        q = kernel[k][1]
                        x = i + p
                        y = j + q
                        if x in range(width):
                            if y in range(height):
                                dilIm.putpixel((x,y), 255)
    except IOError:
        print("cannot open lena")
    finally:
        binIm.close()
    return dilIm