/*
 * bilinear.cpp
 *
 *  Created on: 2014/11/4
 *      Author: Chun-Hsien Lin (D03922030)
 * Description:
 *
 */
#include <iostream>
#include <fstream>
#define _USE_MATH_DEFINES
#include <math.h>
#include "opencv.hpp"
#include "highgui.h"
#include "cvaux.hpp"

using namespace std;
using namespace cv;

int main(int argc, const char * argv[])
{
	IplImage * image;
    IplImage * newImg;
    IplImage * rotateImg;
    int height, width, step, channels, depth;
    int new_height, new_width, new_step;
    int rotate_height, rotate_width, rotate_step;
    uchar *data;
    uchar *new_data;
    uchar *rotate_data;
    int i, j;
    CvScalar new_s;
	double col, row;
	double r1r, r1g, r1b, r2r, r2g, r2b;
	double factor1, factor2, factor3, factor4;
	CvScalar q11, q12, q21, q22;
	int finalR, finalG, finalB;

    image = cvLoadImage( argv[1], 1);

    if (argc != 2 || !image)
    {
        printf( "Could not load image file: %s\n" , argv[1]);
        exit(0);
    }
    // get the original image data
    height = image->height;
    width = image->width;
    step = image->widthStep;
    depth = image->depth;
    channels = image->nChannels;
    data = ( uchar *)image->imageData;

    printf( "Processing a %dx%d image with %d channels %d depth\n" , height, width, channels, depth);
    // create a new zoom image buffer
    newImg = cvCreateImage(cvSize(width*1.5,height*1.5), IPL_DEPTH_8U, channels);
    new_data = (uchar *)newImg->imageData;
    new_height = newImg->height;
    new_width = newImg->width;
    new_step = newImg->widthStep/sizeof(uchar);
    printf( "Creating a new %dx%d image with %d channels that using bilinear interpolation.\n" , new_height, new_width, channels);
    // Using bilinear interpolation
    for (i = 1; i < new_height - 2; i++)
    	for (j = 1; j < new_width - 2; j++)
    	{
    		// incremental step for original image column and row.
    		col = (float)i * height /new_height;
    		row = (float)j * width / new_width;
			// Get the intensity of the original image's nearest diagonal 4-neighbor pixels.
			// Note that, accessing the pixel of i-row, j-column, the row indexing range is [0, height -1],
			// column indexing range is [0, width - 1].
    		q11 = cvGet2D(image, round(col) - 1, round(row) - 1);
    		q22 = cvGet2D(image, round(col) + 1, round(row) + 1);
    		q21 = cvGet2D(image, round(col) + 1, round(row) - 1);
    		q12 = cvGet2D(image, round(col) - 1, round(row) + 1);
    		// Bilinear interpolation.
    		// round(row) + 1 is point x2. round(row) - 1 is point x1.
    		factor1 = round(row) + 1 - row; // x2 - x
    		factor2 = row - (round(row) - 1); // x - x1
    		r1b = (q11.val[0] * factor1 / 2) + (q21.val[0] * factor2 / 2);
    		r1g = (q11.val[1] * factor1 / 2) + (q21.val[1] * factor2 / 2);
    		r1r = (q11.val[2] * factor1 / 2) + (q21.val[2] * factor2 / 2);
    		r2b = (q12.val[0] * factor1 / 2) + (q22.val[0] * factor2 / 2);
    		r2g = (q12.val[1] * factor1 / 2) + (q22.val[1] * factor2 / 2);
    		r2r = (q12.val[2] * factor1 / 2) + (q22.val[2] * factor2 / 2);

    		factor3 = round(col) + 1 - col; // y2 - y
    		factor4 = col - (round(col) - 1); // y - y1
    		finalB = (r1b * factor3) / 2 + r2b * factor4 / 2; // Blue
    		finalG = (r1g * factor3) / 2 + r2g * factor4 / 2; // Green
    		finalR = (r1r * factor3) / 2 + r2r * factor4 / 2; // Red
    		// Clamp the RBG values to a value between 0 and 255
    		if (finalB >= 255) finalB = 255;
    		if (finalB <= 0) finalB = 0;
    		if (finalG >= 255) finalG = 255;
    		if (finalG <= 0) finalG = 0;
    		if (finalR >= 255) finalR = 255;
    		if (finalR <= 0) finalR = 0;

			new_s.val[0] = finalB;
			new_s.val[1] = finalG;
			new_s.val[2] = finalR;
//    		printf("(i, j)=(%d, %d), B=%f, G=%f, R=%f\n", myround(col) , myround(row), s.val[0],s.val[1],s.val[2]);
    		cvSet2D(newImg, i, j, new_s);
    	}
    // Create a image buffer for rotate 45 degree
    rotateImg = cvCreateImage(cvSize(width,height), IPL_DEPTH_8U, channels);
    rotate_data = (uchar *)rotateImg->imageData;
    rotate_height = rotateImg->height;
    rotate_width = rotateImg->width;
    rotate_step = rotateImg->widthStep/sizeof(uchar);
    printf( "Creating a rotate %dx%d image with %d channels\n" , rotate_height, rotate_width, channels);
    // Using bilinear interpolation to rotate the image
	col = 0.0;
	row = 0.0;
    for (i = 1; i < height - 2; i++)
    	for (j = 1; j < width - 2; j++)
    	{
    		col = (double)i*cos(M_PI/4) - (double)j*sin(M_PI/4) + height/2;
    		row = (double)i*sin(M_PI/4) + (double)j*cos(M_PI/4) - width/4;
    		if (round(row) >= width - 1) {
    			row = (double)width - 2;
    		}
    		if (round(col) >= height - 1) {
    			col = (double)height - 2;
    		}
    		if (row <= 1) {
    			row = 1;
    		}
    		if (col <= 1) {
    			col = 1;
    		}
			// Get the intensity of the original image's nearest diagonal 4-neighbor pixels.
			// Note that, accessing the pixel of i-row, j-column, the row indexing range is [0, height -1],
			// column indexing range is [0, width - 1].
//    		printf("Get intensity of col=%lf, row=%lf\n", col, row);
    		q11 = cvGet2D(image, (int)round(col), (int)round(row) - 1);
    		q22 = cvGet2D(image, (int)round(col), (int)round(row) + 1);
    		q21 = cvGet2D(image, (int)round(col) + 1, (int)round(row));
    		q12 = cvGet2D(image, (int)round(col) - 1, (int)round(row));
    		// Bilinear interpolation.
    		// round(row) + 1 is point x2, round(row) - 1 is point x1.
    		factor1 = round(row) + 1 - row; // x2 - x
    		factor2 = row - (round(row) - 1); // x - x1
    		r1b = (q11.val[0] * factor1 / 2) + (q21.val[0] * factor2 / 2);
    		r1g = (q11.val[1] * factor1 / 2) + (q21.val[1] * factor2 / 2);
    		r1r = (q11.val[2] * factor1 / 2) + (q21.val[2] * factor2 / 2);
    		r2b = (q12.val[0] * factor1 / 2) + (q22.val[0] * factor2 / 2);
    		r2g = (q12.val[1] * factor1 / 2) + (q22.val[1] * factor2 / 2);
    		r2r = (q12.val[2] * factor1 / 2) + (q22.val[2] * factor2 / 2);

    		factor3 = round(col) + 1 - col; // y2 - y
    		factor4 = col - (round(col) - 1); // y - y1
    		finalB = (r1b * factor3) / 2 + r2b * factor4 / 2; // Blue
    		finalG = (r1g * factor3) / 2 + r2g * factor4 / 2; // Green
    		finalR = (r1r * factor3) / 2 + r2r * factor4 / 2; // Red
    		// Clamp the RBG values to a value between 0 and 255
    		if (finalB >= 255) finalB = 255;
    		if (finalB <= 0) finalB = 0;
    		if (finalG >= 255) finalG = 255;
    		if (finalG <= 0) finalG = 0;
    		if (finalR >= 255) finalR = 255;
    		if (finalR <= 0) finalR = 0;

			new_s.val[0] = finalB;
			new_s.val[1] = finalG;
			new_s.val[2] = finalR;

    		if (row >= width - 2) {
        		new_s.val[0] = 111; // Blue
        		new_s.val[1] = 111; // Green
        		new_s.val[2] = 111; // Red
    		}
    		if (col >= height - 2) {
           		new_s.val[0] = 111; // Blue
            	new_s.val[1] = 111; // Green
            	new_s.val[2] = 111; // Red
    		}
    		if (row <= 1) {
           		new_s.val[0] = 111; // Blue
            	new_s.val[1] = 111; // Green
            	new_s.val[2] = 111; // Red
    		}
    		if (col <= 1) {
           		new_s.val[0] = 111; // Blue
            	new_s.val[1] = 111; // Green
            	new_s.val[2] = 111; // Red
    		}
//    		printf("Set intensity of col=%lf, row=%lf\n", col, row);
    		cvSet2D(rotateImg, i, j, new_s);
    	}

    // create a window
    cvNamedWindow( "mainWin", CV_WINDOW_AUTOSIZE );
    cvMoveWindow( "mainWin", 100, 50);
    cvNamedWindow( "zoomWin", CV_WINDOW_AUTOSIZE );
    cvMoveWindow( "zoomWin", 300, 50);
    cvNamedWindow( "rotateWin", CV_WINDOW_AUTOSIZE );
    cvMoveWindow( "rotateWin", 500, 50);

    // show the image
    cvShowImage( "mainWin", image);
    cvShowImage( "zoomWin", newImg);
    cvShowImage( "rotateWin", rotateImg);
    // save the image
    cvSaveImage("B_ZoomIn.jpg",newImg);
    cvSaveImage("B_Rotate.jpg",rotateImg);
    // wait for a key
    cvWaitKey(0);

    // release the image
    cvReleaseImage(&image);
    cvReleaseImage(&newImg);
    cvReleaseImage(&rotateImg);
    return 0;
}

