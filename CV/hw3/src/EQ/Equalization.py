#!/usr/bin/env python2
# coding:utf-8
#
# Copyright (c) 2014 Chun-Hsien Lin (D03922030). All right reserved.
'''
Created on 2014/10/07

@author: Chun-Hsien Lin (D03922030)
電腦視覺作業HW3 #1
2014.10.07 v.0.1
讀入 lena.im 圖檔後，作灰階等化處理。
使用 Pillow 程式庫來處理 BMP 圖檔的讀寫。
(http://pillow.readthedocs.org/en/latest/index.html)
'''
from __future__ import print_function
from PIL import Image
import struct

newIm = Image.new("L",(512,512), 128)
imList =[]
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
except IOError:
    print("cannot open lena")
finally:
    f.close()
    
width = newIm.size[0]
height = newIm.size[1]
imList = list(newIm.getdata()) # Get the image data, then convert each pixel to an ordinary sequence.
#
# Calculating the Lena image histogram
# Using Python list count function to accumulate the value of each pixel.
histogram =[]
for i in range(256):
    histogram.append(imList.count(i))
# Write out a histogram file.
logFile = open("histogram.txt", "w")
logFile.write(str(histogram))
logFile.close()
newIm.show()

logFile = open("histogram2.txt", "w")
total_number_pixels = width * height
h_sum = 0
s = []
for i in range(len(histogram)):
    h_sum = h_sum + histogram[i]
    s.insert(i, 255 * h_sum / total_number_pixels)
    logFile.write(str(s[i]) + ", ")
logFile.close()
    