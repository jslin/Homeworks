#!/usr/bin/env python2
# coding:utf-8
#
# Copyright (c) 2014 Chun-Hsien Lin (D03922030). All right reserved.
"""
電腦視覺作業HW4 #1
2014.10.28 v.0.1
讀入 lena.bmp 圖檔後，將該圖檔二元化(Threshold = 128)，
接著再做 mathematical morphology (Erosion)。
使用 Pillow 程式庫來處理圖檔的讀寫。
(http://pillow.readthedocs.org/en/latest/index.html)
"""
from __future__ import print_function
from PIL import Image

def erosion(imageBuffer, kernel):
    try:
        imageBuffer.load() # load image data into memory.
        width = imageBuffer.size[0]
        height = imageBuffer.size[1]
        binIm = imageBuffer.copy()
    # Erosion
    # Definition: 
    #      A erosion by B = 
    #      {x belong to Euclidean 2 space | x + b belong to A, for every b belong to B.}
    # Description:
    #      Because of we dealing with binary image, using a list to store kernel. 
    #      Each list element is (x, y) coordinate tuple.
    # 
    # Create a blank image for dilation , fill up with color = 0 (white).
        eroIm = Image.new("L",(width, height), 0)
    # Using Erosion definition above to implement.
    #
        for i in range(width):
            for j in range(height):
                contain = 1
                k = 0
                # for kernel b, check x + b are belong to a or not.
                while (k < len(kernel)) and (contain == 1):
                    p = kernel[k][0]
                    q = kernel[k][1]
                    x = i + p
                    y = j + q
                    k = k + 1
                    if (x < 0) or (x >= width) or (y < 0) or (y >= height) or (binIm.getpixel((x,y)) == 0):
                        contain = 0
                if (contain == 1):
                    eroIm.putpixel((i,j), 255)
        binIm.close()
    except IOError:
        print("cannot open lena")
    finally:
        binIm.close()
    return eroIm