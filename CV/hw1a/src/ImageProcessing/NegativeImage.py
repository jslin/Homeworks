#!/usr/bin/env python3
# coding:big5
#
# Copyright (c) 2014 Chun-Hsien Lin (D03922030). All right reserved.
"""
�q����ı�@�~ #1
2014.09.19 v.0.1
Ū�J lena.bmp ���ɫ�A�N�ӹ��ɰ����t���ĪG���X�C
�ϥ� Pillow �{���w�ӳB�z���ɪ�Ū�g�C
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