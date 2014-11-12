/*
* LookupTable.cpp
*
*  Created on: 2014/11/4
*      Author: Chun-Hsien Lin (D03922030)
* Description: Using OpenCV API and a look up table
*              to reconstruct the distortion image acquired
*              from fish eye lens.
*
*/
#include <iostream>
#include <sstream>
#include <time.h>
#include <stdio.h>
#include <fstream>
#define _USE_MATH_DEFINES
#include <math.h>
#include "opencv.hpp"
#include "opencv2/core/core.hpp"
#include "opencv2/imgproc/imgproc.hpp"
#include "opencv2/calib3d/calib3d.hpp"
#include "opencv2/highgui/highgui.hpp"
#include "cvaux.hpp"

#ifndef _CRT_SECURE_NO_WARNINGS
#define _CRT_SECURE_NO_WARNINGS
#endif

using namespace std;
using namespace cv;

int main(int argc, const char * argv[])
{
// Declare the variable for look up table, input view, output view, and so on.
	double lut[] = {
			0,
			4.38797235520332,
			8.78010323704483,
			13.1757480310648,
			17.5742621228035,
			21.9750008978012,
			26.3773197415981,
			30.7805740397345,
			35.1841191777507,
			39.5873105411869,
			43.9895035155833,
			48.3900534864804,
			52.7883158394182,
			57.1836459599371,
			61.5753992335774,
			65.9629310458792,
			70.3455967823828,
			74.7227518286286,
			79.0937515701568,
			83.4579513925076,
			87.8147066812213,
			92.1633728218381,
			96.5033051998984,
			100.833859200942,
			105.154390210510,
			109.464253614142,
			113.762804797379,
			118.049399145760,
			122.323392044826,
			126.584138880118,
			130.830995037175,
			135.063315901537,
			139.280456858746,
			143.481773294341,
			147.666620593863,
			151.834354142851,
			155.984329326847,
			160.115901531389,
			164.228426142020,
			168.321258544278,
			172.393754123705,
			176.445268265839,
			180.475156356223,
			184.482773780395,
			188.467475923896,
			192.428618172267,
			196.365555911048,
			200.277644525778,
			204.164239401999,
			208.024695925250,
			211.858369481072,
			215.664615455005,
			219.442789232589,
			223.192246199364,
			226.912341740872,
			230.602431242651,
			234.261870090243,
			237.890013669187,
			241.486217365024,
			245.049836563294,
			248.580226649537,
			252.076743009294,
			255.538741028105,
			258.965576091510,
			262.356603585049,
			265.711178894263,
			269.028657404692,
			272.308394501876,
			275.549745571356,
			278.752065998671,
			281.914711169362,
			285.037036468969,
			288.118397283033,
			291.158148997094,
			294.155646996691,
			297.110246667366,
			300.021303394658,
			302.888172564108,
			305.710209561256,
			308.486769771642,
			311.217208580807,
			313.900881374291,
			316.537143537633,
			319.125350456375,
			321.664857516057,
			324.155020102219,
			326.595193600400,
			328.984733396142,
			331.322994874985,
			333.609333422468,
			335.843104424133,
			338.023663265519,
			340.150365332167,
			342.222566009617,
			344.239620683409,
			346.200884739083,
			348.105713562180,
			349.953462538240,
			351.743487052804,
			353.475142491411,
			355.147784239601
	};
	IplImage * image;
	IplImage * newImg;
//	IplImage * undistortImg;
	int height, width, step, channels, depth;
	int new_height, new_width, new_step;
//	int undistort_height, undistort_width, undistort_step;
	uchar *data;
	uchar *new_data;
//	uchar *undistort_data;
	int i, j;
	CvScalar new_s;
	double col, row;
	double r1r, r1g, r1b, r2r, r2g, r2b;
	double factor1, factor2, factor3, factor4;
	CvScalar q11, q12, q21, q22;
	int finalR, finalG, finalB;

	image = cvLoadImage(argv[1], 1);

	if (argc != 2 || !image)
	{
		printf("Could not load image file: %s\n", argv[1]);
		exit(0);
	}
	// get the original image data
	height = image->height;
	width = image->width;
	step = image->widthStep;
	depth = image->depth;
	channels = image->nChannels;
	data = (uchar *)image->imageData;

	printf("Processing a %dx%d image with %d channels %d depth\n", height, width, channels, depth);
	// create a new 1000x1000 image buffer. 
	newImg = cvCreateImage(cvSize(1000, 1000), IPL_DEPTH_8U, channels);
	new_data = (uchar *)newImg->imageData;
	new_height = newImg->height;
	new_width = newImg->width;
	new_step = newImg->widthStep / sizeof(uchar);
	printf("Creating a new %dx%d image with %d channels for undistortion.\n", new_height, new_width, channels);
	// Using bilinear interpolation
	for (i = 1; i < new_height - 2; i++)
		for (j = 1; j < new_width - 2; j++)
		{
		// incremental step for original image column and row.
		col = (float)i * height / new_height;
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
	

	// create a window
	cvNamedWindow("mainWin", CV_WINDOW_AUTOSIZE);
	cvMoveWindow("mainWin", 100, 50);
	cvNamedWindow("zoomWin", CV_WINDOW_AUTOSIZE);
	cvMoveWindow("zoomWin", 300, 50);


	// show the image
	cvShowImage("mainWin", image);
	cvShowImage("zoomWin", newImg);

	// save the image
	cvSaveImage("lut_1.jpg", newImg);
	// wait for a key
	cvWaitKey(0);

	// release the image
	cvReleaseImage(&image);
	cvReleaseImage(&newImg);
	return 0;
}
