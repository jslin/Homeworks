#!/usr/bin/env python2
# coding:utf-8
#
# Copyright (c) 2014 Chun-Hsien Lin (D03922030). All right reserved.
'''
Created on 2014/10/01

@author: Chun-Hsien Lin (D03922030)
電腦視覺作業HW2 #1
2014.10.01 v.0.1
讀入 lena.im 圖檔後，建立一個threshold = 128 的 binarize image。
接著計算該binarize image的connected components。採用 4-connected operator.
使用 Pillow 程式庫來處理 BMP 圖檔的讀寫。
(http://pillow.readthedocs.org/en/latest/index.html)
'''
from __future__ import print_function
from PIL import Image
import struct

newIm = Image.new("L",(512,512), 128) # Create a blank image, fill up with color = 128.
imList =[]
# Open Lena.im
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

binIm = newIm.copy()
dList = []
rowList =[]
width = newIm.size[0]
height = newIm.size[1]

try:
#
# Binarize
    threshold = 128
    for j in range(height):
        for i in range(width):
            pix_val = binIm.getpixel((i,j))
            if pix_val >= threshold :
                rowList.append(255)
                binIm.putpixel((i,j), 255)
            else:
                rowList.append(0)
                binIm.putpixel((i,j), 0)
        dList.insert(j, rowList) # Let dList be row-major.
    binIm.putdata(dList)
    binIm.load()
    binIm.show()
#
# Labeling
#
# Initialization of each 1-pixel with a unique label.
#
    NEWLABEL = 1
    BLANK = 0
    labList = []
    for j in range(height):
        rowList = []
        for i in range(width):
            if dList[i][j] == 255 :
                rowList.append(NEWLABEL)
                NEWLABEL = NEWLABEL + 1
            else:
                rowList.append(BLANK)
#            print(i, j, dList[i][j], rowList[i])
        labList.insert(j, rowList)
# Write out a log file.
    logFile = open("init.txt", "w")
    logFile.write(str(labList))
    logFile.close()
# Scanning image use 4-connected operator. Using iterative algorithm. 
# Using 4-connected operator.
#
#    min_label = 1
    labChanged = True
    logFile = open("log.txt", "w")
    loopCount = 0
    while labChanged:
        labChanged = False
# Top-down pass. Using 4-connected operator.
        for i in range(height):
            for j in range(width):
                curr_label = labList[i][j]
                # If current label is not zero than starting top-down scan with 4-connected operator.
                if labList[i][j] != BLANK:
                    min_label = labList[i][j]
                    if (i - 1) >= 0 and labList[i-1][j] != 0 and labList[i-1][j] < min_label:
                        min_label = labList[i-1][j]
                        labChanged = False
                    elif (j - 1) >= 0 and labList[i][j-1] != 0 and labList[i][j-1] < min_label:
                        min_label = labList[i][j-1]
                        labChanged = False
                    if labList[i][j] > min_label:
                        logStr = "Top-down pass " + str(loopCount) + ", labList[" + str(i) + "][" + str(j) + "] = " + str(labList[i][j]) + " changed with " + str(min_label)
                        logFile.write(logStr + "\n")
                        labList[i][j] = min_label
                        labChanged = True
# Bottom-up pass. Using 4-connected operator.                   
        for i in range(height-1, 0, -1):
            for j in range(width-1, 0, -1):
                curr_label = labList[i][j]
                if labList[i][j] != BLANK:
                    if i+1 < height and labList[i+1][j] != 0 and labList[i+1][j] < min_label:
                        min_label = labList[i+1][j]
                        labChanged = False
                    elif j+1 < width and labList[i][j+1] != 0 and labList[i][j+1] < min_label:
                        min_label = labList[i][j+1]
                        labChanged = False
                    if labList[i][j] > min_label:
                        logStr = "Bottom-up pass " + str(loopCount) + ", labList[" + str(i) + "][" + str(j) + "] = " + str(labList[i][j]) + " changed with " + str(min_label)
                        logFile.write(logStr + "\n")
                        labList[i][j] = min_label
                        labChanged = True
        loopCount = loopCount + 1
#        if loopCount >= 100 :
#            labChanged = False
    logFile.close()
# Write out a log file.
    print("Loop count = ", loopCount)
    logFile = open("scan1.txt", "w")
    for i in range(height):
        logFile.write(str(labList[i]) + "\n")
    logFile.close()
# Drawing bounding box
    region = []
    logFile = open("regions.txt", "w")
    for i in range(NEWLABEL):
        region.insert(i,0)
# Count each region's size.
    for i in range(height):
        for j in range(width):
            region[labList[i][j]] = region[labList[i][j]] + 1
    for r in range(1, NEWLABEL):
        if region[r] >= 500:
            print("Region:" + str(r) + " count = " + str(region[r]))
            logStr = "Region:" + str(r) + " count = " + str(region[r]) + "\n"
            logFile.write(logStr)
            top = height
            bottom = -1
            left = width
            right = -1
            for i in range(height):
                for j in range(width):
                    if labList[i][j] == r:
                        if (i < top):
                            top = i
                        if (i > bottom):
                            bottom = i
                        if (j < left):
                            left = j
                        if (j > right):
                            right = j
            print("Left:", left, " top:", top, " right:", right, " bottom:", bottom)
            logStr = "Left:" +  str(left) + " top:" + str(top) + " right:" + str(right) + " bottom:" + str(bottom) + "\n"
            logFile.write(logStr)
            # Draw vertical lines.
            for i in range(top, bottom):
                binIm.putpixel((left, i), 128)
                binIm.putpixel((right, i), 128)
            # Draw horizontal lines.
            for i in range(left, right):
                binIm.putpixel((i, top), 128)
                binIm.putpixel((i, bottom), 128)
    logFile.close()
    binIm.show()
    binIm.save("result.bmp")
    binIm.close()
except TypeError:
    print("Type error")
except ValueError:
    print("Parameter Value error") 