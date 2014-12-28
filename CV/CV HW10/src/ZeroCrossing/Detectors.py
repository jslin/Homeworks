#!/usr/bin/env python2
# coding:utf-8
#
# Copyright (c) 2014 Chun-Hsien Lin (D03922030). All right reserved.
"""
電腦視覺作業HW10 #1
2014.12.26 v.0.1
讀入 lena.bmp 圖檔後，呼叫各越零點偵測子函式後輸出邊緣圖片。
使用 Pillow 程式庫來處理圖檔的讀寫。
(http://pillow.readthedocs.org/en/latest/index.html)
"""
from __future__ import print_function
from PIL import Image
import math

def main():
    im = Image.open("lena.bmp", "r")
    im.load() # load image data into memory.
    # Define Laplacian type 1 kernel
    lKernel = [(0,1,0),(1,-4,1),(0,1,0)]
    LaplacianIm = Laplacian(im, lKernel, 15)
    LaplacianIm.show()
    LaplacianIm.save("Laplacian_lena.bmp")
    # Define Laplacian type 2 kernel
    l2Kernel = [(1,1,1),(1,-8,1),(1,1,1)]
    Laplacian2Im = Laplacian2(im, l2Kernel, 15)
    Laplacian2Im.show()
    Laplacian2Im.save("Laplacian2_lena.bmp")
    # Define minimum-variance Laplacian kernel
    minKernel = [(2,-1,2),(-1,-4,-1),(2,-1,2)]
    minLaplacianIm = Laplacian2(im, minKernel, 12)
    minLaplacianIm.show()
    minLaplacianIm.save("minimumLaplacian_lena.bmp")
    # Define Laplacian of the Gaussian Kernel
    LOGKernel = [(0, 0, 0, -1, -1, -2, -1, -1, 0, 0, 0),
                (0, 0, -2, -4, -8, -9, -8, -4, -2, 0, 0),
                (0, -2, -7, -15, -22, -23, -22,-15, -7, -2, 0),
                (-1, -4, -15,-24,-14, -1, -14,-24,-15, -4, -1),
                (-1,-8,-22,-14, 52,103, 52,-14,-22, -8, -1),
                (-2,-9,-23, -1,103,178,103, -1,-23, -9, -2),
                (-1,-8,-22,-14, 52,103, 52,-14,-22, -8, -1),
                (-1,-4,-15,-24,-14, -1,-14,-24,-15, -4, -1),
                (0,-2, -7,-15,-22,-23,-22,-15, -7, -2,  0),
                (0, 0, -2, -4, -8, -9, -8, -4, -2,  0,  0),
                (0, 0,  0, -1, -1, -2, -1, -1,  0,  0,  0)]
    LOGIm = Gaussian(im, LOGKernel, 5000)
    LOGIm.show()
    LOGIm.save("LOG_lena.bmp")
    # Call function to generate a Difference of Gaussian Kernel.
    DOGKernel = genDOGKernel(1, 3)
    DOGIm = Gaussian(im, DOGKernel, 5)
    DOGIm.show()
    DOGIm.save("DOG_lena.bmp")
    im.close()
    
def Laplacian(imageBuffer, kernel, threshold):
    try:
        imageBuffer.load() # load image data into memory.
        width = imageBuffer.size[0]
        height = imageBuffer.size[1]
        inputIm = imageBuffer.copy()
        # Create a blank image, fill up with color = 255 (white).
        edgeIm = Image.new("L",(width, height), 255)
        gradientList = []
        for i in range(width-2):
            imList = []
            for j in range(height-2):
                gradient = 0
                for x in range(3):
                    for y in range(3):
#                        print("x=",x,"y=",y)
                        gradient = gradient + inputIm.getpixel((j+x,i+y))* kernel[x][y]
                imList.append(gradient)
#            print(imList)
            gradientList.append(imList)
#        print(gradientList)
        for i in range(width - 3):
            for j in range(height - 3):
                criticalPoint = gradientList[i][j]
                if criticalPoint > threshold:
                    for x in range(-1,2,1):
                        for y in range(-1,2,1):
#                            print("(i,j)=(",i,",", j,"), (x,y)=(",x,", ",y,")")
                            if x <> 0 and y <> 0:
                                if gradientList[i+x][j+y] < (-1 * threshold):
                                    edgeIm.putpixel((j,i), 0)
#        edgeIm.show()
#        edgeIm.save("Laplacian_lena.bmp")
        return edgeIm
    except IOError:
        print("cannot open lena")
    finally:
        inputIm.close()

def Laplacian2(imageBuffer, kernel, threshold):
#    lKernel = [(2,-1,2),(-1,-4,-1),(2,-1,2)]
    try:
        imageBuffer.load() # load image data into memory.
        width = imageBuffer.size[0]
        height = imageBuffer.size[1]
        inputIm = imageBuffer.copy()
        # Create a blank image, fill up with color = 255 (white).
        edgeIm = Image.new("L",(width, height), 255)
        gradientList = []
        for i in range(width-2):
            imList = []
            for j in range(height-2):
                gradient = 0
                for x in range(3):
                    for y in range(3):
#                        print("x=",x,"y=",y)
                        gradient = gradient + inputIm.getpixel((j+x,i+y))* kernel[x][y]
                imList.append(gradient/3)
#            print(imList)
            gradientList.append(imList)
#        print(gradientList)
        for i in range(width - 3):
            for j in range(height - 3):
                criticalPoint = gradientList[i][j]
                if criticalPoint > threshold:
                    for x in range(-1,2,1):
                        for y in range(-1,2,1):
#                            print("(i,j)=(",i,",", j,"), (x,y)=(",x,", ",y,")")
                            if x <> 0 and y <> 0:
                                if gradientList[i+x][j+y] < (-1 * threshold):
                                    edgeIm.putpixel((j,i), 0)
        return edgeIm
    except IOError:
        print("cannot open lena")
    finally:
        inputIm.close()

def Gaussian(imageBuffer, kernel, threshold):
    try:
        imageBuffer.load() # load image data into memory.
        width = imageBuffer.size[0]
        height = imageBuffer.size[1]
        inputIm = imageBuffer.copy()
        # Create a blank image, fill up with color = 255 (white).
        edgeIm = Image.new("L",(width, height), 255)
        gradientList = []
        for i in range(5, width-5):
            imList = []
            for j in range(5, height-5):
                gradient = 0
                for x in range(11):
                    for y in range(11):
#                        print("x=",x,"y=",y)
                        gradient = gradient + inputIm.getpixel((j+x-5,i+y-5))* kernel[x][y]
                imList.append(gradient)
#            print(imList)
            gradientList.append(imList)
#        print(gradientList)
        for i in range(5, width - 5):
            for j in range(5, height - 5):
                criticalPoint = gradientList[i-5][j-5]
                if criticalPoint > threshold:
                    for x in (-5,-4,-3,-2,-1,0,1,2,3,4,5):
                        for y in (-5,-4,-3,-2,-1,0,1,2,3,4,5):
#                            print("(i,j)=(",i,",", j,"), (x,y)=(",x,", ",y,")")
                            if x <> 0 and y <> 0:
                                # Limitation of List upper boundary.
                                if x+i < 502 and y+j < 502:
                                    if gradientList[i+x][j+y] < (-1 * threshold):
                                        edgeIm.putpixel((j,i), 0)
        return edgeIm
    except IOError:
        print("cannot open lena")
    finally:
        inputIm.close()

def genDOGKernel(sigma1, sigma2):
    mean = 0.0
    a = 0.0
    b = 0.0
    temp2 = []
    for i in (-5,-4,-3,-2,-1,0,1,2,3,4,5):
        temp = []
        for j in (-5,-4,-3,-2,-1,0,1,2,3,4,5):
            a = math.exp( -(i*i+j*j)/(2*sigma1*sigma1) ) / (math.sqrt(2*math.pi)*sigma1)
            b = math.exp( -(i*i+j*j)/(2*sigma2*sigma2) ) / (math.sqrt(2*math.pi)*sigma2)
            mean = mean + (a - b)
            temp.append((a-b))
#        print(temp)
        temp2.append(temp)
    mean = mean / 121
    kernel =[]
    for i in range(11):
        row = []
        for j in range(11):
            row.append(temp2[i][j] - mean)
#        print("row(",i,")=", row)
        kernel.append(row)
    return kernel

main()