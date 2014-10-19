//  main.cpp
//  Display an image file.
//
//  Created by 林君憲 on 2014/10/17.
//  Copyright (c) 2014年 Chun-Hsien Lin. All rights reserved.
//  學號：D03922030
//
#include <iostream>
#include <fstream>
#include "opencv.hpp"
#include "highgui.h"
#include "cvaux.hpp"

using namespace std;
using namespace cv;

int Display(int argc, const char * argv[])
{

    IplImage * image;
    int height, width, step, channels;
    uchar *data;
    int i, j, k;

    image = cvLoadImage( argv[1], 1);

    if ( argc != 2 || !image)
    {
        printf( "Could not load image file: %s\n" , argv [1]);
        exit(0);
    }
    // get the image data
    height = image->height;
    width = image->width;
    step = image->widthStep;
    channels = image->nChannels;
    data = ( uchar *)image->imageData;
    printf( "Processing a %dx%d image with %d channels\n" , height, width, channels);

    // create a window
    cvNamedWindow( "mainWin", CV_WINDOW_AUTOSIZE );
    cvMoveWindow( "mainWin", 100, 100);


    // invert the image
    for (i = 0; i<height; i++)
        for (j = 0; j<width; j++)
            for (k = 0; k<channels; k++)
                data[i*step + j*channels + k] = 255 - data[i*step + j*channels + k];

    // show the image
    cvShowImage( "mainWin", image);

    // wait for a key
    cvWaitKey(0);

    // release the image
    cvReleaseImage(&image);
    return 0;
}
