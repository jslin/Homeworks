#!/usr/bin/env python2
# coding:utf-8
#
# Copyright (c) 2014 Chun-Hsien Lin (D03922030). All right reserved.
"""
電腦視覺作業HW8 #1
2014.12.07 v.0.1
讀入 lena.bmp 圖檔後，將該圖檔做加入高斯雜訊、胡椒鹽雜訊，
再做雜訊移除。
使用 Pillow 程式庫來處理圖檔的讀寫。
(http://pillow.readthedocs.org/en/latest/index.html)
"""
from __future__ import print_function
import random
from PIL import Image

def main():
    try:
        im = Image.open("lena.bmp", "r")
        im.load() # load image data into memory.

        GNIm = GaussNoiseImage(im, 10)
        GNIm.show()
        GNIm.save("10GN_Lena.bmp")
        SPIm = SNPNoiseImage(im, 0.05)
        SPIm.show()
        SPIm.save("05_SP_Lena.bmp")
        BFIm = BoxFilter(GNIm, 3)
        BFIm.show()
        BFIm = BoxFilter(GNIm, 5)
        BFIm.show()
        BFIm = BoxFilter(SPIm, 3)
        BFIm.show()
        BFIm = BoxFilter(SPIm, 5)
        BFIm.show()
    except IOError:
        print("cannot open lena")
    finally:
        GNIm.close()
        im.close()

def GaussNoiseImage(image, amplitude):
    im = image.copy()
    width = im.size[0]
    height = im.size[1]
    noiseIm = Image.new("L",(width, height), 0)  
    for i in range(width):
        for j in range(height):
            pix_val = im.getpixel((i,j))
            gn_pix = pix_val + (random.gauss(0,1) * amplitude)
            if gn_pix < 0:
                gn_pix = 0
            if gn_pix > 255:
                gn_pix = 255
            noiseIm.putpixel((i,j), gn_pix)
    return noiseIm

def SNPNoiseImage(image, threshold):
    im = image.copy()
    width = im.size[0]
    height = im.size[1]
    noiseIm = Image.new("L",(width, height), 0)
    for i in range(width):
        for j in range(height):
            rnd = random.uniform(0, 1)
            pix_value = im.getpixel((i,j))                
            if threshold > rnd:
                noiseIm.putpixel((i,j), 0)
            else: 
                if 1 - threshold < rnd:
                    noiseIm.putpixel((i,j), 255)
                else:
                    noiseIm.putpixel((i,j), pix_value)
    return noiseIm

def BoxFilter(image, n):
    im =image.copy()
    halfN = n / 2
    normalizeCoefficient = n * n
    width = im.size[0]
    height = im.size[1]
    W = width - halfN
    H = height - halfN
    noiseIm = Image.new("L",(width, height), 255)
    for i in range(halfN, H):
        for j in range(halfN, W):
            boxSum = 0
            for x in range(-halfN, halfN):
                for y in range(-halfN, halfN):
                    boxSum = boxSum + im.getpixel((x+i,y+j))
            noiseIm.putpixel((i,j), 255 - (boxSum / normalizeCoefficient))
    return noiseIm

main()