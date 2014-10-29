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

try:
    im = Image.open("lena.bmp", "r")
    im.load() # load image data into memory.
    width = im.size[0]
    height = im.size[1]
    binIm = im.copy()

# Binarize
# newIm be stored the binary image.
#
    threshold = 128
    for i in range(width):
        for j in range(height):
            pix_val = im.getpixel((i,j))
            if pix_val >= threshold :
                binIm.putpixel((i,j), 255)
            else:
                binIm.putpixel((i,j), 0)
    binIm.show()
# Erosion
# Definition: 
#      A erosion by B = 
#      {x belong to Euclidean 2 space | x + b belong to A, for every b belong to B.}
# Description:
#      Because of we dealing with binary image, using a list to store kernel. 
#      Each list element is (x, y) coordinate tuple.
# 
# Define a type of kernel. It is a octangon with origin.
# 
    octangon = [(-1,2),(0,2),(1,2),(-2,1),(-1,1),(0,1),(1,1),(2,1),(-2,1),(-1,1),(0,1),(1,1),(2,1),(-2,0),(-1,0),(0,0),(1,0),(2,0),(-2,-1),(-1,-1),(0,-1),(1,-1),(2,-1),(-1,-2),(0,-2),(1,-2)]
# Create a blank image for dilation , fill up with color = 0 (white).
    eroIm = Image.new("L",(width, height), 0)
# Using Erosion definition above to implement.
#
    for i in range(width):
        for j in range(height):
#            if binIm.getpixel((i, j)) == 255 :
            for k in range(len(octangon)):
                contain = 1
                p = octangon[k][0]
                q = octangon[k][1]
                x = i + p
                y = j + q
                while (contain == 1) and (x in range(width)) and (y in range(height)):
                    if binIm.getpixel((x,y)) == 0:
                        contain = 0
                        break
                    else:
                        eroIm.putpixel((x,y), 255)
                        contain = 1
# Show result and save image
#    binIm.show()
    eroIm.show()
    eroIm.save("Erosion_lena.bmp")
except IOError:
    print("cannot open lena")
finally:
    im.close()
    binIm.close()
    eroIm.close()