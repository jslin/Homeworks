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
    Kirsch(im, 230)
    Robinson(im, 100)
    NevatiaBabu(im, 25000)

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
                
def Kirsch(imageBuffer, threshold):
    k0Kernel = [(-3,-3,5),(-3,0,5),(-3,-3,5)]
    k1Kernel = [(-3,5,5),(-3,0,5),(-3,-3,-3)]
    k2Kernel = [(5,5,5),(-3,0,-3),(-3,-3,-3)]
    k3Kernel = [(5,5,-3),(5,0,-3),(-3,-3,-3)]
    k4Kernel = [(5,-3,-3),(5,0,-3),(5,-3,-3)]
    k5Kernel = [(-3,-3,-3),(5,0,-3),(5,5,-3)]
    k6Kernel = [(-3,-3,-3),(-3,0,-3),(5,5,5)]
    k7Kernel = [(-3,-3,-3),(-3,0,5),(-3,5,5)]
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
                k0 = 0
                k1 = 0
                k2 = 0
                k3 = 0
                k4 = 0
                k5 = 0
                k6 = 0
                k7 = 0
                for x in range(3):
                    for y in range(3):
#                        print("x=",x,"y=",y)
                        k0 = k0 + inputIm.getpixel((j+x,i+y))* k0Kernel[x][y]
                        k1 = k1 + inputIm.getpixel((j+x,i+y))* k1Kernel[x][y]
                        k2 = k2 + inputIm.getpixel((j+x,i+y))* k2Kernel[x][y]
                        k3 = k3 + inputIm.getpixel((j+x,i+y))* k3Kernel[x][y]
                        k4 = k4 + inputIm.getpixel((j+x,i+y))* k4Kernel[x][y]
                        k5 = k5 + inputIm.getpixel((j+x,i+y))* k5Kernel[x][y]
                        k6 = k6 + inputIm.getpixel((j+x,i+y))* k6Kernel[x][y]
                        k7 = k7 + inputIm.getpixel((j+x,i+y))* k7Kernel[x][y]
                gradient = max(k0,k1,k2,k3,k4,k5,k6,k7)
                if (gradient > threshold) :
                    edgeIm.putpixel((j,i), 0)
        edgeIm.show()
        edgeIm.save("Kirsch_lena.bmp")
        return edgeIm
    except IOError:
        print("cannot open lena")
    finally:
        inputIm.close()
        edgeIm.close()

def Robinson(imageBuffer, threshold):
    r0Kernel = [(-1,0,1),(-2,0,2),(-1,0,1)]
    r1Kernel = [(0,1,2),(-1,0,1),(-2,-1,0)]
    r2Kernel = [(1,2,1),(0,0,0),(-1,-2,-1)]
    r3Kernel = [(2,1,0),(1,0,-1),(0,-1,-2)]
    r4Kernel = [(1,0,-1),(2,0,-2),(1,0,-1)]
    r5Kernel = [(0,-1,-2),(1,0,-1),(2,1,0)]
    r6Kernel = [(-1,-2,-1),(0,0,0),(1,2,1)]
    r7Kernel = [(-2,-1,0),(-1,0,1),(0,1,2)]
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
                r0 = 0
                r1 = 0
                r2 = 0
                r3 = 0
                r4 = 0
                r5 = 0
                r6 = 0
                r7 = 0
                for x in range(3):
                    for y in range(3):
#                        print("x=",x,"y=",y)
                        r0 = r0 + inputIm.getpixel((j+x,i+y))* r0Kernel[x][y]
                        r1 = r1 + inputIm.getpixel((j+x,i+y))* r1Kernel[x][y]
                        r2 = r2 + inputIm.getpixel((j+x,i+y))* r2Kernel[x][y]
                        r3 = r3 + inputIm.getpixel((j+x,i+y))* r3Kernel[x][y]
                        r4 = r4 + inputIm.getpixel((j+x,i+y))* r4Kernel[x][y]
                        r5 = r5 + inputIm.getpixel((j+x,i+y))* r5Kernel[x][y]
                        r6 = r6 + inputIm.getpixel((j+x,i+y))* r6Kernel[x][y]
                        r7 = r7 + inputIm.getpixel((j+x,i+y))* r7Kernel[x][y]
                gradient = max(r0,r1,r2,r3,r4,r5,r6,r7)
                if (gradient > threshold) :
                    edgeIm.putpixel((j,i), 0)
        edgeIm.show()
        edgeIm.save("Robinson_lena.bmp")
        return edgeIm
    except IOError:
        print("cannot open lena")
    finally:
        inputIm.close()
        edgeIm.close()

def NevatiaBabu(imageBuffer, threshold):
    r0Kernel = [(100,100,100,100,100),(100,100,100,100,100),(0,0,0,0,0),(-100,-100,-100,-100,-100),(-100,-100,-100,-100,-100)]
    r1Kernel = [(100,100,100,100,100),(100,100,100,78,-32),(100,92,0,-92,-100),(32,-78,-100,-100,-100),(-100,-100,-100,-100,-100)]
    r2Kernel = [(100,100,100,32,-100),(100,100,92,-78,-100),(100,100,0,-100,-100),(100,78,-92,-100,-100),(100,-32,-100,-100,-100)]
    r3Kernel = [(-100,-100,0,100,100),(-100,-100,0,100,100),(-100,-100,0,100,100),(-100,-100,0,100,100),(-100,-100,0,100,100)]
    r4Kernel = [(-100,32,100,100,100),(-100,-78,92,100,100),(-100,-100,0,100,100),(-100,-100,-92,78,100),(-100,-100,-100,-32,100)]
    r5Kernel = [(100,100,100,100,100),(-32,78,100,100,100),(-100,-92,0,92,100),(-100,-100,-100,-78,32),(-100,-100,-100,-100,-100)]
    try:
        imageBuffer.load() # load image data into memory.
        width = imageBuffer.size[0]
        height = imageBuffer.size[1]
        inputIm = imageBuffer.copy()
        # Create a blank image, fill up with color = 255 (white).
        edgeIm = Image.new("L",(width, height), 255)
        for i in range(width-4):
            for j in range(height-4):
                gradient = 0
                r0 = 0
                r1 = 0
                r2 = 0
                r3 = 0
                r4 = 0
                r5 = 0
                for x in range(5):
                    for y in range(5):
#                        print("x=",x,"y=",y)
                        r0 = r0 + inputIm.getpixel((j+x,i+y))* r0Kernel[x][y]
                        r1 = r1 + inputIm.getpixel((j+x,i+y))* r1Kernel[x][y]
                        r2 = r2 + inputIm.getpixel((j+x,i+y))* r2Kernel[x][y]
                        r3 = r3 + inputIm.getpixel((j+x,i+y))* r3Kernel[x][y]
                        r4 = r4 + inputIm.getpixel((j+x,i+y))* r4Kernel[x][y]
                        r5 = r5 + inputIm.getpixel((j+x,i+y))* r5Kernel[x][y]
                gradient = max(r0,r1,r2,r3,r4,r5)
                if (gradient > threshold) :
                    edgeIm.putpixel((j,i), 0)
        edgeIm.show()
        edgeIm.save("NevatiaBabu_lena.bmp")
        return edgeIm
    except IOError:
        print("cannot open lena")
    finally:
        inputIm.close()
        edgeIm.close()

main()