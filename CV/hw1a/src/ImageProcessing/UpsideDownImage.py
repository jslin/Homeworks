#!/usr/bin/env python3
# coding:big5
#
# Copyright (c) 2014 Chun-Hsien Lin (D03922030). All right reserved.
"""
�q����ı�@�~ #2
2014.09.19 v.0.1
Ū�J lena.bmp ���ɫ�A�N�ӹ��ɤW�U�A�˫��X�C
�ϥ� Pillow �{���w�ӳB�z���ɪ�Ū�g�C
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
    udList = []
#
# This nest loop dealing with image up-side-down pixel by pixel.
    for i in range(height):
        for j in range(width):
            udList.insert(height*i+j, imList[width*height - (width*i+j) - 1])

    rlList = []
#
# This nest loop dealing with image right-side-left pixel by pixel.
    for i in range(height):
        for j in range(width):
            rlList.insert(height*i+j, udList[width*i - j])
# Restore the up-side-down image data to image buffer.
    im.putdata(rlList)
    im.show()
#    im.save("UDLena.bmp")
    im.close()
except IOError:
    print("cannot open lena")