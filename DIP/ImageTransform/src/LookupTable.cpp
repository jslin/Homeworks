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
