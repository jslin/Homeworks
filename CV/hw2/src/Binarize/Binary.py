#!/usr/bin/env python2
# coding:utf-8
#
# Copyright (c) 2014 Chun-Hsien Lin (D03922030). All right reserved.
"""
電腦視覺作業HW2 #1
2014.09.30 v.0.1
讀入 lena.bmp 圖檔後，將該圖檔二元化後輸出。Threshold = 128。
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
    newIm = im.copy()
    
    width = newIm.size[0]
    height = newIm.size[1]
    imList = list(newIm.getdata()) # Get the image data, then convert each pixel to an ordinary sequence.
    dList = []
#
# This loop dealing with image data into 2 dimension list pixel by pixel.
    for i in (range(height)):
        dList.insert(i, imList[i*width:(i+1)*width])

# Binarize
    threshold = 128
    for i in range(width):
        for j in range(height):
            pix_val = im.getpixel((i,j))
            if pix_val >= threshold :
                newIm.putpixel((i,j), 255)
            else:
                newIm.putpixel((i,j), 0)
#
# Calculating the Lena image histogram
# Using Python list count function to accumulate the value of each pixel.
    histogram =[]
    for i in range(256):
        histogram.append(imList.count(i))
# Check the histogram count. It should be the product of height with width.
# Lena image is 256 gray-level, 512 x 512.
#    hsum = 0
#    for i in range(256):
#        hsum = hsum + histogram[i]
    print(histogram)
#    print(hsum)
    newIm.show()
    newIm.save("Bin_lena.bmp")
    im.close()
    newIm.close()
except IOError:
    print("cannot open lena")