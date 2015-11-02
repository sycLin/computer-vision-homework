#include "opencv2/imgproc/imgproc.hpp"
#include "opencv2/highgui/highgui.hpp"
#include <iostream>

using namespace std;
using namespace cv;

int main(int argc, char** argv) {
	// check arguments
	if(argc != 2) {
		cout << "Usage: ./main <img file path>" << endl;
		return 1;
	}

	Mat original;
	Mat upside_down;
	Mat rightside_left;
	Mat diagonally_mirrored;

	original = imread(argv[1], CV_LOAD_IMAGE_GRAYSCALE);
	// imread:
	// CV_LOAD_IMAGE_GRAYSCALE (=0)
	// CV_LOAD_IMAGE_COLOR (>0, default)
	// CV_LOAD_IMAGE_UNCHANGED (<0)

	namedWindow("Display the image", WINDOW_AUTOSIZE);
	imshow("Display the image", original);

	/* let's do the upside-down */
	upside_down = original.clone();
	for(int i=0; i<upside_down.rows; i++) {
		for(int j=0; j<upside_down.cols; j++) {
			upside_down.at<uchar>(i, j) = original.at<uchar>(original.rows - i, j);
		}
	}
	namedWindow("Display Upside-Down", WINDOW_AUTOSIZE);
	imshow("Display Upside-Down", upside_down);
	imwrite("./upside_down.bmp", upside_down);

	/* let's do the rightside-left */
	rightside_left = original.clone();
	for(int i=0; i<rightside_left.rows; i++) {
		for(int j=0; j<rightside_left.cols; j++) {
			rightside_left.at<uchar>(i, j) = original.at<uchar>(i, original.cols - j);
		}
	}
	namedWindow("Display Rightside-Left", WINDOW_AUTOSIZE);
	imshow("Display Rightside-Left", rightside_left);
	imwrite("./rightside_left.bmp", rightside_left);

	/* let's do the diagonally-mirrored */
	diagonally_mirrored = original.clone();
	for(int i=0; i<diagonally_mirrored.rows; i++) {
		for(int j=0; j<diagonally_mirrored.cols; j++) {
			if(i > j) {
				diagonally_mirrored.at<uchar>(i, j) = original.at<uchar>(j, i);
			} else {
				diagonally_mirrored.at<uchar>(i, j) = original.at<uchar>(i, j);
			}
		}
	}
	namedWindow("Display Diagonally-Mirrored", WINDOW_AUTOSIZE);
	imshow("Display Diagonally-Mirrored", diagonally_mirrored);
	imwrite("./diagonally_mirrored.bmp", diagonally_mirrored);


	waitKey();
	return 0;
}
