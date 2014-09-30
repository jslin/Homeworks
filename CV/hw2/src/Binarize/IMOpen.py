#!/usr/bin/env python2
# coding:utf-8
#
# Copyright (c) 2014 Chun-Hsien Lin (D03922030). All right reserved.
'''
Created on 2014/9/30

@author: Chun-Hsien Lin (D03922030)
電腦視覺作業HW2 #1
2014.09.30 v.0.1
讀入 lena.im 圖檔後，顯示該圖檔。
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
    newIm.show()
except IOError:
    print("cannot open lena")
finally:
    f.close()