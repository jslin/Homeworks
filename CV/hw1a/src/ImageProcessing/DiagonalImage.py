#!/usr/bin/env python3
# coding:big5
#
# Copyright (c) 2014 Chun-Hsien Lin (D03922030). All right reserved.
"""
�q����ı�@�~ #4
2014.09.19 v.0.1
Ū�J lena.bmp ���ɫ�A�N�ӹ��ɹ﨤��g���X�C
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
    tempList = []
#
# This nest loop dealing with image data into 2 dimension list pixel by pixel.
    for i in range(height):
        tempList.insert(i, imList[i:(i+1)*width])
    
    dList = []

    for i in range(width):
        for j in range(i):
            dList.insert(i*j+j + width, tempList[i][j])
            dList.insert(i*j + j,tempList[j][i])
# Restore the up-side-down image data to image buffer.
    im.putdata(dList)
#    print(dList[0])
    im.show()
#    im.save("DLena.bmp")
    im.close()
except IOError:
    print("cannot open lena")
except IndexError:
    print("Index error", i,j)
except TypeError:
    print("Type error: tempList[", i,"][",j,"]", tempList[i][j])
    print(tempList[i][j])