#include "opencv2/imgproc/imgproc.hpp"
#include "opencv2/highgui/highgui.hpp"
#include <iostream>
#include <cmath>
#include <vector>

using namespace std;
using namespace cv;

Mat drawHistogram(Mat src, String displayName, String fileName);
void HistoEqualize(Mat src, Mat& dst);

int main(int argc, char** argv) {
	// check arguments
	if(argc != 2) {
		cout << "Usage: ./main <img file path>" << endl;
		return 1;
	}

	Mat original;

	original = imread(argv[1], CV_LOAD_IMAGE_GRAYSCALE);
	// imread:
	// CV_LOAD_IMAGE_GRAYSCALE (=0)
	// CV_LOAD_IMAGE_COLOR (>0, default)
	// CV_LOAD_IMAGE_UNCHANGED (<0)

	namedWindow("Display original image", WINDOW_AUTOSIZE);
	imshow("Display original image", original);


	/* draw the histogram of the original image */
	Mat dummy = drawHistogram(original, "histogram of original image", "orig_histo.bmp"); // don't write to file, just display


	/* worsen the image by "divide by 3" */
	Mat worse = original.clone();
	for(int i=0; i<worse.rows; i++) {
		for(int j=0; j<worse.cols; j++) {
			worse.at<uchar>(i, j) = original.at<uchar>(i, j) / 3;
		}
	}
	namedWindow("Display worsen image", WINDOW_AUTOSIZE);
	imshow("Display worsen image", worse);
	imwrite("worsen.bmp", worse);

	/* draw the histogram of the worsen image */
	dummy = drawHistogram(worse, "histogram of worsen image", "worse_histo.bmp"); // don't write to file, just display


	/* do the Histogram Equalization by calling the function */
	Mat histo_equalized;
	HistoEqualize(worse, histo_equalized);
	namedWindow("histo_equalized", WINDOW_AUTOSIZE);
	imshow("histo_equalized", histo_equalized);
	imwrite("his_eq.bmp", histo_equalized);

	/* draw the histogram of the histo_equalized image */
	dummy = drawHistogram(histo_equalized, "histogram of histogram equalized image", "his_eq_his.bmp");

	/* just for debug use */
	// print the intensity count of the histogram equalized image
	/*
	int count[256] = {0};
	for(int i=0; i<histo_equalized.rows; i++)
		for(int j=0; j<histo_equalized.cols; j++)
			count[histo_equalized.at<uchar>(i, j)] += 1;
	for(int i=0; i<256; i++)
		printf("%d %d\n", i, count[i]);
	*/

	waitKey();
	return 0;
}

/** draw histogram for image "src"
 *  @param src: the source image for drawing histogram image
 *  @param displayName: if not empty string, display the histogram with this name
 *  @param fileName: if not empty string, write to file with this name
 *  @return the Mat variable storing the histogram image.
 */
Mat drawHistogram(Mat src, String displayName, String fileName) {
	// step 1: count the intensity
	int count_intensity[256] = {0};
	for(int i=0; i<src.rows; i++)
		for(int j=0; j<src.cols; j++)
			count_intensity[src.at<uchar>(i, j)] += 1;
	// step 1.1: get the max intensity count
	int maxIntensityCount = count_intensity[0];
	for(int i=0; i<256; i++)
		if(count_intensity[i] > maxIntensityCount)
			maxIntensityCount = count_intensity[i];
	// step 2: create a Mat to draw the histogram
	Mat histo(512, 512, CV_8UC1, Scalar(200)); // 200: gray background
	// step 3: draw it
	double scale = 512.0/maxIntensityCount;
	for(int i=0; i<256; i++) {
		int draw_pixel_count = (int)floor(count_intensity[i]*scale);
		for(int j=0; j<draw_pixel_count; j++) {
			histo.at<uchar>(512-j-1, i*2) = 0;
			histo.at<uchar>(512-j-1, i*2+1) = 0;
		}
	}
	// step 4: display the histogram
	if(displayName.length() != 0) {
		namedWindow(displayName, WINDOW_AUTOSIZE);
		imshow(displayName, histo);
	}
	if(fileName.length() != 0)
		imwrite(fileName, histo);
	return histo;
}

/** Do histogram equalization to given "src" and store the result in "dst".
 *  @param src: source image
 *  @param dst: resulted image after histogram equalization
 */
void HistoEqualize(Mat src, Mat& dst) {
	dst = src.clone();
	// step 1: calculate the CDF
	int CDF[256] = {0};
	for(int i=0; i<src.rows; i++)
		for(int j=0; j<src.cols; j++)
			CDF[src.at<uchar>(i, j)] += 1;
	for(int i=1; i<256; i++)
		CDF[i] = CDF[i] + CDF[i-1];
	int CDF_min = 0;
	for(int i=0; i<256; i++) {
		if(CDF[i] != 0) {
			CDF_min = CDF[i];
			break;
		}
	}
	// step 2: form the formula?
	for(int i=0; i<src.rows; i++) {
		for(int j=0; j<src.cols; j++) {
			double ratio = double(CDF[src.at<uchar>(i, j)] - CDF_min) / double(src.rows * src.cols - CDF_min);
			dst.at<uchar>(i, j) = floor(ratio * 255);
		}
	}
}





