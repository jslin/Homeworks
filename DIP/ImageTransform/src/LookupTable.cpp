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
#define PI 3.14159265

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

	int height, width, step, channels, depth;
	int new_height, new_width, new_step;
	int lutIdx;
	int xr, yr;
	double theta_fov, theta;
	uchar *data;
	uchar *new_data;
	int i, j;
	CvScalar new_s;
	CvScalar fisheyeDot;

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
	for (i = 0; i < new_height; i++)
		for (j = 0; j < new_width; j++)
		{
		// Scanning the new image from up-left corner to bottom-right.
		// 1. Calculate the theta of (x, y)
		// 2. find out the theta of FOV
		// 3. find out the look up table index by theta of FOV  divided by 0.9.
		// 4. query out the displacement from table
		// 5. find out the dot on fish-eye image.
		// 6. Filling in the fish-eye dot into the new image.
		// 7. again step 1 until scan finished.
			theta = atan((i+499)/(j+499)) * 180 / PI;
			theta_fov = 0.15 * sqrt(pow((i-499),2) + pow((j-499), 2));
			lutIdx = round(theta_fov / 0.9);
//			printf("(i,j) = (%d, %d), theta = %f, theta of FOV = %f, lut index = %d\n", i, j, theta, theta_fov, lutIdx);
			xr = 360 + round(lut[lutIdx]*cos(theta));
			yr = 240 + round(lut[lutIdx]*sin(theta));
			if (xr < 0) xr = 0;
			if (xr >= 720) xr = 719;
			if (yr < 0) yr = 0;
			if (yr >= 480) yr = 479;
//			printf("(xr, yr) = (%d, %d)\n", xr, yr);

			fisheyeDot = cvGet2D(image, yr, xr);
			new_s.val[0] = fisheyeDot.val[0]; // Blue
			new_s.val[1] = fisheyeDot.val[1]; // Green
			new_s.val[2] = fisheyeDot.val[2]; // Red
//			printf("Setting new image.\n");
			cvSet2D(newImg, j, i, new_s);

	};
	
	// create a window
	cvNamedWindow("mainWin", CV_WINDOW_AUTOSIZE);
	cvMoveWindow("mainWin", 100, 50);
	cvNamedWindow("undistortedWin", CV_WINDOW_AUTOSIZE);
	cvMoveWindow("undistortedWin", 300, 50);


	// show the image
	cvShowImage("mainWin", image);
	cvShowImage("undistortedWin", newImg);

	// save the image
//	cvSaveImage("lut_1.jpg", newImg);
	// wait for a key
	cvWaitKey(0);

	// release the image
	cvReleaseImage(&image);
	cvReleaseImage(&newImg);
	return 0;
}
