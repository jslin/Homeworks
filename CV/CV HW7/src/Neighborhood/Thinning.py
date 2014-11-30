#!/usr/bin/env python2
# coding:utf-8
#
# Copyright (c) 2014 Chun-Hsien Lin (D03922030). All right reserved.
"""
電腦視覺作業HW7 #1
2014.11.28 v.0.1
讀入 lena.bmp 圖檔後，將該圖檔做 binary 後再 resampling 至 64x64，
再做 thinning operation part A 及 part B。
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
        # There is a one pixel border set to white(255) background.
        # So, the re-sampling image is set to center.
        downSampleIm = Image.new("L",(width/8 + 2, height/8 + 2), 255) # zero is black.
        downHeight = downSampleIm.size[0]
        downWidth = downSampleIm.size[1]
        # Down sampling
        for i in range(1, downWidth-1):
            for j in range(1, downHeight-1):
                tempValue = binIm.getpixel(((i-1)*8,(j-1)*8))
                downSampleIm.putpixel((i,j),tempValue)
        downSampleIm.show()
        downSampleIm.save("down_lena.bmp")
        thinIm = downSampleIm.copy()
        preThinIm = thinIm.copy()
        while True: # Do loop until thinning operation is finished.
            # Thinning Operator Part A
            removed = 0
            for i in range(1, downWidth-1):
                for j in range(1, downHeight-1):
                    con1 = False
                    con2 = False
                    con3 = False
                    con4 = False
                    # 0 (255 is white background), 1 (zero is region)
                    P1 = (255 - thinIm.getpixel((i+1, j))) / 255
                    P2 = (255 - thinIm.getpixel((i, j-1))) / 255
                    P3 = (255 - thinIm.getpixel((i-1, j))) / 255
                    P4 = (255 - thinIm.getpixel((i, j+1))) / 255
                    P5 = (255 - thinIm.getpixel((i+1, j+1))) / 255
                    P6 = (255 - thinIm.getpixel((i+1, j-1))) / 255
                    P7 = (255 - thinIm.getpixel((i-1, j-1))) / 255
                    P8 = (255 - thinIm.getpixel((i-1, j+1))) / 255
                    if thinIm.getpixel((i, j)) == 0: # zero is black
                        # If region pixels between 2 and 6, condition one is true.
                        neighborValue = P1 + P2 + P3 + P4 + P5 + P6 + P7 + P8
                        if neighborValue >= 2 and neighborValue <= 6:
                            con1 = True
                        # Go through clockwise from top, once pixel from 0 (255 is background) turn to 1 (zero is region), counter++. Counter = 1, TRUE.
                        counter = 0
                        if P7 < P2:
                            counter = counter + 1
                        if P2 < P6:
                            counter = counter + 1
                        if P6 < P1:
                            counter = counter + 1
                        if P1 < P5:
                            counter = counter + 1
                        if P5 < P4:
                            counter = counter + 1
                        if P4 < P8:
                            counter = counter + 1
                        if P8 < P3:
                            counter = counter + 1
                        if P3 < P7:
                            counter = counter + 1
                        if counter == 1:
                            con2 = True
                        # If on of P2, P1, P4 is background (0), then set condition 3 to TRUE.
                        if P2 * P1 * P4 == 0:
                            con3 = True
                        # If on of P1, P4, P3 is background (0), then set condition 4 to TRUE.   
                        if P1 * P4 * P3 == 0:
                            con4 = True
                        # If the 4 conditions above are all True, remove the pixel that scan.
                        if con1 == con2 == con3 == con4 == True:
                            thinIm.putpixel((i,j), 255) # 255 is white, removed.
                            removed = removed + 1
            print("After thinning operation part A, so that pixels removed = ", removed)
            # Thinning Operator part B
            removed = 0
            for i in range(1, downWidth-1):
                for j in range(1, downHeight-1):
                    con1 = False
                    con2 = False
                    con3 = False
                    con4 = False
                    # 0 (255 is white background), 1 (zero is region). Inverse each neighborhood pixels.
                    P1 = (255 - thinIm.getpixel((i+1, j))) / 255
                    P2 = (255 - thinIm.getpixel((i, j-1))) / 255
                    P3 = (255 - thinIm.getpixel((i-1, j))) / 255
                    P4 = (255 - thinIm.getpixel((i, j+1))) / 255
                    P5 = (255 - thinIm.getpixel((i+1, j+1))) / 255
                    P6 = (255 - thinIm.getpixel((i+1, j-1))) / 255
                    P7 = (255 - thinIm.getpixel((i-1, j-1))) / 255
                    P8 = (255 - thinIm.getpixel((i-1, j+1))) / 255
                    if thinIm.getpixel((i, j)) == 0: # zero is region
                        # If region pixels between 2 and 6, condition one is true.
                        neighborValue = P1 + P2 + P3 + P4 + P5 + P6 + P7 + P8
                        if neighborValue >= 2 and neighborValue <= 6:
                            con1 = True
                        # Go through clockwise from top, once pixel from 0 (gray 255 is background) turn to 1 (gray zero is region), counter++. Counter = 1, TRUE.
                        counter = 0
                        if P7 < P2:
                            counter = counter + 1
                        if P2 < P6:
                            counter = counter + 1
                        if P6 < P1:
                            counter = counter + 1
                        if P1 < P5:
                            counter = counter + 1
                        if P5 < P4:
                            counter = counter + 1
                        if P4 < P8:
                            counter = counter + 1
                        if P8 < P3:
                            counter = counter + 1
                        if P3 < P7:
                            counter = counter + 1
                        if counter == 1:
                            con2 = True
                        # If one of P3, P2, P1 is background, set condition 3 to TRUE
                        if P3 * P2 * P1 == 0:
                            con3 = True
                        # If one of P4, P3, P2 is background, set condition 4 to TRUE
                        if P4 * P3 * P2 == 0:
                            con4 = True
                        # If the 4 conditions above are all True, remove the pixel that scan.
                        if con1 == con2 == con3 == con4 == True:
                            thinIm.putpixel((i,j), 255) # 255 is white background, pixel removed.
                            removed = removed + 1
            print("After thinning operation part B, so that pixels removed = ", removed)
            if preThinIm == thinIm:
                break # thinning operation is finished, exit this while loop.
            else:
                preThinIm = thinIm.copy()
        thinIm.show()
        thinIm.save("thin_lena.bmp")
        with open('thinning.txt', 'w') as thinningFile:
            for i in range(1, downWidth-1):
                for j in range(1, downHeight-1):
                    if thinIm.getpixel((j,i)) == 0:
                        thinningFile.write('*')
                    else:
                        thinningFile.write(' ')
                thinningFile.write('\n')
    except IOError:
        print("cannot open lena")
    finally:
        preThinIm.close()
        downSampleIm.close()
        thinIm.close()
        binIm.close()
        im.close()

main()