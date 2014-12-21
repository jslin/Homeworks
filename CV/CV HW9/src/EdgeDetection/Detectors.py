#!/usr/bin/env python2
# coding:utf-8
#
# Copyright (c) 2014 Chun-Hsien Lin (D03922030). All right reserved.
"""
電腦視覺作業HW9 #1
2014.12.21 v.0.1
讀入 lena.bmp 圖檔後，呼叫各邊緣偵測子函式後輸出邊緣圖片。
使用 Pillow 程式庫來處理圖檔的讀寫。
(http://pillow.readthedocs.org/en/latest/index.html)
"""
from __future__ import print_function
from PIL import Image
import math

def main():
    im = Image.open("lena.bmp", "r")
    im.load() # load image data into memory.
    Roberts(im, 30)
    Prewitt(im, 100)
    Sobel(im, 100)
    Frei(im, 100)

def Roberts(imageBuffer, threshold):
    R1Kernel = [(-1,0),(0,1)]
    R2Kernel = [(0,-1),(1,0)]
    try:
        imageBuffer.load() # load image data into memory.
        width = imageBuffer.size[0]
        height = imageBuffer.size[1]
        inputIm = imageBuffer.copy()
        # Create a blank image, fill up with color = 255 (white).
        edgeIm = Image.new("L",(width, height), 255)
        for i in range(width-1):
            for j in range(height-1):
                gradient = 0
                r1 = 0
                r2 = 0
                for x in range(2):
                    for y in range(2):
#                        print("x=",x,"y=",y)
                        r1 = r1 + inputIm.getpixel((j+x,i+y))* R1Kernel[x][y]
                        r2 = r2 + inputIm.getpixel((j+x,i+y))* R2Kernel[x][y]
                gradient = math.sqrt(r1 * r1 + r2* r2)
                if (gradient > threshold) :
                    edgeIm.putpixel((j,i), 0)
        edgeIm.show()
        edgeIm.save("Roberts_lena.bmp")
        return edgeIm
    except IOError:
        print("cannot open lena")
    finally:
        inputIm.close()
        edgeIm.close()

def Prewitt(imageBuffer, threshold):
    P1Kernel = [(-1,-1,-1),(0,0,0),(1,1,1)]
    P2Kernel = [(-1,0,1),(-1,0,1),(-1,0,1)]
    try:
        imageBuffer.load() # load image data into memory.
        width = imageBuffer.size[0]
        height = imageBuffer.size[1]
        inputIm = imageBuffer.copy()
        # Create a blank image, fill up with color = 255 (white).
        edgeIm = Image.new("L",(width, height), 255)
        for i in range(width-2):
            for j in range(height-2):
                gradient = 0
                p1 = 0
                p2 = 0
                for x in range(3):
                    for y in range(3):
#                        print("x=",x,"y=",y)
                        p1 = p1 + inputIm.getpixel((j+x,i+y))* P1Kernel[x][y]
                        p2 = p2 + inputIm.getpixel((j+x,i+y))* P2Kernel[x][y]
                gradient = math.sqrt(p1 * p1 + p2* p2)
                if (gradient > threshold) :
                    edgeIm.putpixel((j,i), 0)
        edgeIm.show()
        edgeIm.save("Prewitt_lena.bmp")
        return edgeIm
    except IOError:
        print("cannot open lena")
    finally:
        inputIm.close()
        edgeIm.close()
        
def Sobel(imageBuffer, threshold):
    S1Kernel = [(-1,-2,-1),(0,0,0),(1,2,1)]
    S2Kernel = [(-1,0,1),(-2,0,2),(-1,0,1)]
    try:
        imageBuffer.load() # load image data into memory.
        width = imageBuffer.size[0]
        height = imageBuffer.size[1]
        inputIm = imageBuffer.copy()
        # Create a blank image, fill up with color = 255 (white).
        edgeIm = Image.new("L",(width, height), 255)
        for i in range(width-2):
            for j in range(height-2):
                gradient = 0
                s1 = 0
                s2 = 0
                for x in range(3):
                    for y in range(3):
#                        print("x=",x,"y=",y)
                        s1 = s1 + inputIm.getpixel((j+x,i+y))* S1Kernel[x][y]
                        s2 = s2 + inputIm.getpixel((j+x,i+y))* S2Kernel[x][y]
                gradient = math.sqrt(s1 * s1 + s2* s2)
                if (gradient > threshold) :
                    edgeIm.putpixel((j,i), 0)
        edgeIm.show()
        edgeIm.save("Sobel_lena.bmp")
        return edgeIm
    except IOError:
        print("cannot open lena")
    finally:
        inputIm.close()
        edgeIm.close()
                
def Frei(imageBuffer, threshold):
    F1Kernel = [(-1,-math.sqrt(2),-1),(0,0,0),(1,math.sqrt(2),1)]
    F2Kernel = [(-1,0,1),(-math.sqrt(2),0,math.sqrt(2)),(-1,0,1)]
    try:
        imageBuffer.load() # load image data into memory.
        width = imageBuffer.size[0]
        height = imageBuffer.size[1]
        inputIm = imageBuffer.copy()
        # Create a blank image, fill up with color = 255 (white).
        edgeIm = Image.new("L",(width, height), 255)
        for i in range(width-2):
            for j in range(height-2):
                gradient = 0
                f1 = 0
                f2 = 0
                for x in range(3):
                    for y in range(3):
#                        print("x=",x,"y=",y)
                        f1 = f1 + inputIm.getpixel((j+x,i+y))* F1Kernel[x][y]
                        f2 = f2 + inputIm.getpixel((j+x,i+y))* F2Kernel[x][y]
                gradient = math.sqrt(f1 * f1 + f2* f2)
                if (gradient > threshold) :
                    edgeIm.putpixel((j,i), 0)
        edgeIm.show()
        edgeIm.save("Frei_lena.bmp")
        return edgeIm
    except IOError:
        print("cannot open lena")
    finally:
        inputIm.close()
        edgeIm.close()
                
main()