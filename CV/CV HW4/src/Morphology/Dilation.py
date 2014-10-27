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

try:
    im = Image.open("lena.bmp", "r")
    im.load() # load image data into memory.
    width = im.size[0]
    height = im.size[1]
    imList = list(im.getdata()) # Get the image data, then convert each pixel to an ordinary sequence.
    binIm = im.copy()
    
    width = binIm.size[0]
    height = binIm.size[1]
    imList = list(binIm.getdata()) # Get the image data, then convert each pixel to an ordinary sequence.

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
# Dilation
# Definition: 
#      A dilation by B = 
#      {x belong to Euclidean 2 space | x = a + b, for some a belong to A , and b belong to B.}
# Description:
#      Because of we manipulate binary image, using a list to store kernel. 
#      Each list element is (x, y) coordinate tuple.
# 
# Define a type of kernel. It is a disk.
# 
    kernelList = [(0,0),(-1,0),(0,-1),(1,0),(0,1)]
# Create a blank image for dilation , fill up with color = 128.
    dilIm = Image.new("L",(width, height), 128)
# Show result and save image
    binIm.show()
    dilIm.show()
#    dilIm.save("Dilation_lena.bmp")
except IOError:
    print("cannot open lena")
finally:
    im.close()
    binIm.close()
    dilIm.close()