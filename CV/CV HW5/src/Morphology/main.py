#!/usr/bin/env python2
# coding:utf-8
#
# Copyright (c) 2014 Chun-Hsien Lin (D03922030). All right reserved.
"""
電腦視覺作業HW5
2014.11.14 v.0.1
讀入 lena.bmp 圖檔後，將該圖檔做灰階的 mathematical morphology 運算，
包括 Dilation, Erosion。
使用 Pillow 程式庫來處理圖檔的讀寫。
(http://pillow.readthedocs.org/en/latest/index.html)
"""
from __future__ import print_function
# from Morphology import *
import grayDilation
import grayErosion
from PIL import Image

def main():
    # Define some kernels.
    #
#    octangon = [(-1,2,10),(0,2,10),(1,2,10),(-2,1,10),(-1,1,10),(0,1,10),(1,1,10),(2,1,10),(-2,1,10),(-1,1,10),(0,1,10),(1,1,10),(2,1,10),(-2,0,10),(-1,0,10),(0,0,10),(1,0,10),(2,0,10),(-2,-1,10),(-1,-1,10),(0,-1,10),(1,-1,10),(2,-1,10),(-1,-2,10),(0,-2,10),(1,-2,10)]
    octangon = [(-1,2,0),(0,2,0),(1,2,0),(-2,1,0),(-1,1,0),(0,1,0),(1,1,0),(2,1,0),(-2,1,0),(-1,1,0),(0,1,0),(1,1,0),(2,1,0),(-2,0,0),(-1,0,0),(0,0,0),(1,0,0),(2,0,0),(-2,-1,0),(-1,-1,0),(0,-1,0),(1,-1,0),(2,-1,0),(-1,-2,0),(0,-2,0),(1,-2,0)]
    im = Image.open("lena.bmp", "r")

    # Erosion
    eroImage = grayErosion.grayErosion(im, octangon)
    eroImage.show()
    eroImage.save("Erosion_lena.bmp")
    # Dilation
    dilImage = grayDilation.grayDilation(im, octangon)
    dilImage.show()
    dilImage.save("Dilation_lena.bmp")
    # Opening
    openingImage = grayDilation.grayDilation(eroImage, octangon)
    openingImage.show()
    openingImage.save("Opening_lena.bmp")
    # Closing
    closingImage = grayErosion.grayErosion(dilImage, octangon)
    closingImage.show()
    closingImage.save("Closing_lena.bmp")
    
    eroImage.close()
    dilImage.close()
    openingImage.close()
    closingImage.close()
# -- end of main()
    
main()