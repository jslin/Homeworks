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
        octangon = [(-1,2,0),(0,2,0),(1,2,0),(-2,1,0),(-1,1,0),(0,1,0),(1,1,0),(2,1,0),(-2,1,0),(-1,1,0),(0,1,0),(1,1,0),(2,1,0),(-2,0,0),(-1,0,0),(0,0,0),(1,0,0),(2,0,0),(-2,-1,0),(-1,-1,0),(0,-1,0),(1,-1,0),(2,-1,0),(-1,-2,0),(0,-2,0),(1,-2,0)]   
        
        GNIm = GaussNoiseImage(im, 10)
        GNIm.show("Gaussian Noise with amplitude = 10")
        GNIm.save("10GN_Lena.bmp")
        SPIm = SNPNoiseImage(im, 0.05)
        SPIm.show("Salt and Pepper Noise with coef=0.05")
        SPIm.save("05_SP_Lena.bmp")
        BFIm = BoxFilter(GNIm, 3)
        BFIm.show("3x3 Box Filter on Gaussian Noise image")
        BFIm.save("3x3_BF_10GNLena.bmp")
        BFIm = BoxFilter(GNIm, 5)
        BFIm.show("5x5 Box Filter on Gaussian Noise image")
        BFIm.save("5x5_BF_10GNLena.bmp")
        BFIm = BoxFilter(SPIm, 3)
        BFIm.show()
        BFIm.save("3x3_BF_05SNPLena.bmp")
        BFIm = BoxFilter(SPIm, 5)
        BFIm.show()
        BFIm.save("5x5_BF_05SNPLena.bmp")
        MFIm = medianFilter(GNIm, 3)
        MFIm.show()
        MFIm.save("3x3_MF_10GNLena.bmp")
        MFIm = medianFilter(GNIm, 5)
        MFIm.show()
        MFIm.save("5x5_MF_10GNLena.bmp")
        MFIm = medianFilter(SPIm, 3)
        MFIm.show("3x3 median filter on Gaussian Noise image")
        MFIm.save("3x3_MF_05SNPLena.bmp")
        MFIm = medianFilter(SPIm, 5)
        MFIm.show("5x5 median filter on Gaussian Noise image")
        MFIm.save("5x5_MF_05SNPLena.bmp")
        
        eroImage = grayErosion(GNIm, octangon)
        dilImage = grayDilation(GNIm, octangon)
        # Opening Gaussian noise image
        openingImage = grayDilation(eroImage, octangon)
        openingImage.show("Opening")
        # Closing followed by opening
        CFOIm = grayErosion(openingImage, octangon)
        CFOIm.show()
        CFOIm.save("close_open_10GNLena.bmp")
        # Closing
        closingImage = grayErosion(dilImage, octangon)
        closingImage.show("Closing")
        # Opening followed by closing
        OFCIm = grayDilation(closingImage, octangon)
        OFCIm.save("open_close_10GNLena.bmp")
        # Salt and pepper noise image
        eroImage = grayErosion(SPIm, octangon)
        dilImage = grayDilation(SPIm, octangon)
        # Opening
        openingImage = grayDilation(eroImage, octangon)
        openingImage.show("Opening")
        # Closing followed by opening
        CFOIm = grayErosion(openingImage, octangon)
        CFOIm.show()
        CFOIm.save("close_open_05SNPLena.bmp")
        # Closing
        closingImage = grayErosion(dilImage, octangon)
        closingImage.show("Closing")
        # Opening followed by closing
        OFCIm = grayDilation(closingImage, octangon)
        OFCIm.save("open_close_05SNPLena.bmp")
        
        GNIm = GaussNoiseImage(im, 30)
        GNIm.show("Gaussian Noise with amplitude = 30")
        GNIm.save("30GN_Lena.bmp")
        SPIm = SNPNoiseImage(im, 0.1)
        SPIm.show("Salt and Pepper Noise with coef=0.1")
        SPIm.save("1_SP_Lena.bmp")
        BFIm = BoxFilter(GNIm, 3)
        BFIm.show("3x3 Box Filter on Gaussian Noise image")
        BFIm.save("3x3_BF_30GNLena.bmp")
        BFIm = BoxFilter(GNIm, 5)
        BFIm.show("5x5 Box Filter on Gaussian Noise image")
        BFIm.save("5x5_BF_30GNLena.bmp")
        BFIm = BoxFilter(SPIm, 3)
        BFIm.show()
        BFIm.save("3x3_BF_1_SNPLena.bmp")
        BFIm = BoxFilter(SPIm, 5)
        BFIm.show()
        BFIm.save("5x5_BF_1_SNPLena.bmp")
        MFIm = medianFilter(GNIm, 3)
        MFIm.show()
        MFIm.save("3x3_MF_30GNLena.bmp")
        MFIm = medianFilter(GNIm, 5)
        MFIm.show()
        MFIm.save("5x5_MF_30GNLena.bmp")
        MFIm = medianFilter(SPIm, 3)
        MFIm.show("3x3 median filter on Gaussian Noise image")
        MFIm.save("3x3_MF_1_SNPLena.bmp")
        MFIm = medianFilter(SPIm, 5)
        MFIm.show("5x5 median filter on Gaussian Noise image")
        MFIm.save("5x5_MF_1_SNPLena.bmp")
        
        eroImage = grayErosion(GNIm, octangon)
        dilImage = grayDilation(GNIm, octangon)
        # Opening Gaussian noise image
        openingImage = grayDilation(eroImage, octangon)
        openingImage.show("Opening")
        # Closing followed by opening
        CFOIm = grayErosion(openingImage, octangon)
        CFOIm.show()
        CFOIm.save("close_open_30GNLena.bmp")
        # Closing
        closingImage = grayErosion(dilImage, octangon)
        closingImage.show("Closing")
        # Opening followed by closing
        OFCIm = grayDilation(closingImage, octangon)
        OFCIm.save("open_close_30GNLena.bmp")
        # Salt and pepper noise image
        eroImage = grayErosion(SPIm, octangon)
        dilImage = grayDilation(SPIm, octangon)
        # Opening
        openingImage = grayDilation(eroImage, octangon)
        openingImage.show("Opening")
        # Closing followed by opening
        CFOIm = grayErosion(openingImage, octangon)
        CFOIm.show()
        CFOIm.save("close_open_1SNPLena.bmp")
        # Closing
        closingImage = grayErosion(dilImage, octangon)
        closingImage.show("Closing")
        # Opening followed by closing
        OFCIm = grayDilation(closingImage, octangon)
        OFCIm.save("open_close_1SNPLena.bmp")
    except IOError:
        print("cannot open lena")
    finally:
        BFIm.close()
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
    filteredIm = Image.new("L",(width, height), 255)
    for i in range(halfN, H):
        for j in range(halfN, W):
            boxSum = 0
            for x in range(-halfN, halfN+1):
                for y in range(-halfN, halfN+1):
                    boxSum = boxSum + im.getpixel((x+i,y+j)) / normalizeCoefficient
            filteredIm.putpixel((i,j), boxSum)
    return filteredIm

def medianFilter(image, n):
    im =image.copy()
    halfN = n / 2
    kernelLen = n * n
    width = im.size[0]
    height = im.size[1]
    W = width - halfN
    H = height - halfN
    filteredIm = Image.new("L",(width, height), 255)
    for i in range(halfN, H):
        for j in range(halfN, W):
            boxList = []
            for x in range(-halfN, halfN+1):
                for y in range(-halfN, halfN+1):
                    boxList.append(im.getpixel((x+i,y+j)))
            boxList.sort()
            filteredIm.putpixel((i,j), boxList[kernelLen/2])
    return filteredIm

def grayDilation(imageBuffer, kernel):
    try:
        imageBuffer.load() # load image data into memory.
        width = imageBuffer.size[0]
        height = imageBuffer.size[1]
        inputIm = imageBuffer.copy()

    # Create a blank image, fill up with color = 0 (white).
        dilIm = Image.new("L",(width, height), 0)
    # Using Dilation definition to implement.
    #
        for i in range(width):
            for j in range(height):
                maxValue = 0
                for k in range(len(kernel)):
                    p = kernel[k][0]
                    q = kernel[k][1]
                    value = kernel[k][2]
                    temp = inputIm.getpixel((i,j))
                    x = i - p
                    y = j - q
                    if (x >= 0) and (x < width) and (y >= 0) and (y < height):
                        temp = inputIm.getpixel((x,y)) + value
                    if temp > maxValue:
                        maxValue = temp
                    dilIm.putpixel((i,j), maxValue)
        inputIm.close()
    except IOError:
        print("cannot open lena")
    finally:
        inputIm.close()
    return dilIm

def grayErosion(imageBuffer, kernel):
    try:
        imageBuffer.load() # load image data into memory.
        width = imageBuffer.size[0]
        height = imageBuffer.size[1]
        inputIm = imageBuffer.copy()

    # Create a blank image, fill up with color = 0 (white).
        eroIm = Image.new("L",(width, height), 0)
    # Using Erosion definition to implement.
    #
        for i in range(width):
            for j in range(height):
                minValue = 255
                for k in range(len(kernel)):
                    p = kernel[k][0]
                    q = kernel[k][1]
                    value = kernel[k][2]
                    temp = inputIm.getpixel((i,j))
                    x = i + p
                    y = j + q
                    if (x >= 0) and (x < width) and (y >= 0) and (y < height):
                        temp = inputIm.getpixel((x,y)) - value
                    if temp < minValue:
                        minValue = temp
                    eroIm.putpixel((i,j), minValue)
        inputIm.close()
    except IOError:
        print("cannot open lena")
    finally:
        inputIm.close()
    return eroIm

main()