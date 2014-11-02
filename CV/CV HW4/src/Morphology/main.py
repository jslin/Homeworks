#!/usr/bin/env python2
# coding:utf-8
#
# Copyright (c) 2014 Chun-Hsien Lin (D03922030). All right reserved.
"""
電腦視覺作業HW4 #1
2014.10.29 v.0.1
讀入 lena.bmp 圖檔後，將該圖檔二元化(Threshold = 128)，
接著再做 mathematical morphology。
使用 Pillow 程式庫來處理圖檔的讀寫。
(http://pillow.readthedocs.org/en/latest/index.html)
"""
from __future__ import print_function
# from Morphology import *
import Dilation
import Erosion
from PIL import Image

def main():
    # Define some kernels.
    #
    octangon = [(-1,2),(0,2),(1,2),(-2,1),(-1,1),(0,1),(1,1),(2,1),(-2,1),(-1,1),(0,1),(1,1),(2,1),(-2,0),(-1,0),(0,0),(1,0),(2,0),(-2,-1),(-1,-1),(0,-1),(1,-1),(2,-1),(-1,-2),(0,-2),(1,-2)]
    kernelJ = [(0,0),(-1,0),(0,-1)]
    kernelK = [(0,1),(1,1),(1,0)]
    im = Image.open("lena.bmp", "r")
    # Image binarize
    # binIm be stored the binary image.
    # Threshold = 128
    #
    im.load() # load image data into memory.
    width = im.size[0]
    height = im.size[1]
    binIm = im.copy()
    threshold = 128
    for i in range(width):
        for j in range(height):
            pix_val = im.getpixel((i,j))
            if pix_val >= threshold :
                binIm.putpixel((i,j), 255)
            else:
                binIm.putpixel((i,j), 0)

    eroImage = Erosion.erosion(binIm, octangon)
    eroImage.show()
    eroImage.save("Erosion_lena.bmp")
    dilImage = Dilation.dilation(binIm, octangon)
    dilImage.show()
    dilImage.save("Dilation_lena.bmp")
    # opening
    openingIm = Dilation.dilation(eroImage, octangon)
    openingIm.show()
    openingIm.save("Opening_lena.bmp")
    # closing
    closingIm = Erosion.erosion(dilImage, octangon)
    closingIm.show()
    closingIm.save("Closing_lena.bmp")
    # Hit-and-Miss transform
    #
    # complement binary image
    complementIm = Image.new("L",(width, height), 0)
    #
    for i in range(width):
        for j in range(height):
            pix_val = binIm.getpixel((i,j))
            complementIm.putpixel((i,j), 255-pix_val)
#    complementIm.show()
    HAMImage = Image.new("L",(width, height), 0)
    tempIm1 = Erosion.erosion(binIm, kernelJ)
    tempIm2 = Erosion.erosion(complementIm, kernelK)
    for i in range(width):
        for j in range(height):
            if (tempIm1.getpixel((i,j)) == 255) and (tempIm2.getpixel((i,j)) == 255):
                HAMImage.putpixel((i,j), 255)
    HAMImage.show()
    HAMImage.save("HAM_lena.bmp")
    
    eroImage.close()
    dilImage.close()
    openingIm.close()
    closingIm.close()
    complementIm.close()
    HAMImage.close()
    
main()