#!/usr/bin/env python2
# coding:utf-8
#
# Copyright (c) 2014 Chun-Hsien Lin (D03922030). All right reserved.
"""
電腦視覺作業HW6 #1
2014.11.19 v.0.1
讀入 lena.bmp 圖檔後，將該圖檔做 binary 後再 resampling 至 64x64，
再做Yokoi 4-connectivity number。
使用 Pillow 程式庫來處理圖檔的讀寫。
(http://pillow.readthedocs.org/en/latest/index.html)
"""
from __future__ import print_function
from PIL import Image

def main():
    try:
        im = Image.open("lena.bmp", "r")
        im.load() # load image data into memory.
        width = im.size[0]
        height = im.size[1]
        # Image binarize
        # binIm be stored the binary image.
        # Threshold = 128
        #
        binIm = im.copy()
        threshold = 128
        for i in range(width):
            for j in range(height):
                pix_val = im.getpixel((i,j))
                if pix_val >= threshold :
                    binIm.putpixel((i,j), 255)
                else:
                    binIm.putpixel((i,j), 0)
        # Create a blank image buffer for down sampling image.
        # There is a one pixel border set to gray (50). So, 
        # the re-sampling image is set to center.
        downSampleIm = Image.new("L",(width/8 + 2, height/8 + 2), 50)
        downHeight = downSampleIm.size[0]
        downWidth = downSampleIm.size[1]
        # Down sampling
        for i in range(1, downWidth-1):
            for j in range(1, downHeight-1):
                tempValue = binIm.getpixel(((i-1)*8,(j-1)*8))
                downSampleIm.putpixel((i,j),tempValue)
        downSampleIm.show()       
        yokoi(downSampleIm)
    except IOError:
        print("cannot open lena")
    finally:
        im.close()
        
def h(b, c, d, e):
    if (b == c):
        if (d == b) and (e == b):
            return 'r'
        else:
            return 'q'
    else:
        return 's'

def f(a1, a2, a3, a4):
    if (a1 == a2 == a3 == a4 == 'r'):
        return 5
    n = 0
    if (a1 == 'q'):
        n = n + 1
    if (a2 == 'q'):
        n = n + 1   
    if (a3 == 'q'):
        n = n + 1
    if (a4 == 'q'):
        n = n + 1
    return n

def yokoi(im):
    with open('yokoi.txt', 'w') as yokoifile:
        width = im.size[0]
        height = im.size[1]
        # Because of the input image will be transposed.
        # We transpose the index of image pixel for output.
        #
        for i in range(1, height - 1):
            for j in range(1, width - 1):
                if im.getpixel((j,i)) == 255:
                    a1 = h(im.getpixel((j, i)), im.getpixel((j+1, i)), im.getpixel((j+1, i-1)), im.getpixel((j, i-1)))
                    a2 = h(im.getpixel((j, i)), im.getpixel((j, i-1)), im.getpixel((j-1, i-1)), im.getpixel((j-1, i)))
                    a3 = h(im.getpixel((j, i)), im.getpixel((j-1, i)), im.getpixel((j-1, i+1)), im.getpixel((j, i+1)))
                    a4 = h(im.getpixel((j, i)), im.getpixel((j, i+1)), im.getpixel((j+1, i+1)), im.getpixel((j+1, i)))
                    out = f(a1,a2,a3,a4)
                    yokoifile.write(str(out))
                else:
                    yokoifile.write(' ')
            yokoifile.write('\n')

main()