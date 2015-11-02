#include "opencv2/imgproc/imgproc.hpp"
#include "opencv2/highgui/highgui.hpp"
#include <iostream>
#include <cmath>
#include <vector>

using namespace std;
using namespace cv;

int main(int argc, char** argv) {
	// check arguments
	if(argc != 2) {
		cout << "Usage: ./main <img file path>" << endl;
		return 1;
	}

	Mat original;
	Mat binarized;

	original = imread(argv[1], CV_LOAD_IMAGE_GRAYSCALE);
	// imread:
	// CV_LOAD_IMAGE_GRAYSCALE (=0)
	// CV_LOAD_IMAGE_COLOR (>0, default)
	// CV_LOAD_IMAGE_UNCHANGED (<0)

	namedWindow("Display original image", WINDOW_AUTOSIZE);
	imshow("Display original image", original);


	/* binarization */
	binarized = original.clone();
	for(int i=0; i<binarized.rows; i++)
		for(int j=0; j<binarized.cols; j++)
			if(binarized.at<uchar>(i, j) < 128)
				binarized.at<uchar>(i, j) = 0;
			else
				binarized.at<uchar>(i, j) = 255;
	namedWindow("Display binarized image", WINDOW_AUTOSIZE);
	imshow("Display binarized image", binarized);
	imwrite("./lena_binarized.bmp", binarized);

	/* draw the histogram */
	// step 1: count the intensity
	int count_intensity[256] = {0};
	for(int i=0; i<original.rows; i++)
		for(int j=0; j<original.cols; j++)
			count_intensity[original.at<uchar>(i, j)] += 1;
	int maxIntensityCount = count_intensity[0];
	for(int i=0; i<256; i++)
		if(count_intensity[i] > maxIntensityCount)
			maxIntensityCount = count_intensity[i];
	// step 2: create a Mat to draw histogram
	// Mat my_own(rows, cols, CV_[number of bits][signed or unsigned][type prefix][channel], ScalarToInit)
	Mat histo(512, 512, CV_8UC1, Scalar(200));
	// step 3: draw the histogram
	// TODO:here
	double scale = 512.0/maxIntensityCount;
	for(int i=0; i<256; i++) {
		int draw_pixel_count = (int)floor(count_intensity[i]*scale);
		for(int j=0; j<draw_pixel_count; j++) {
			histo.at<uchar>(512-j-1, i*2) = 0;
			histo.at<uchar>(512-j-1, i*2+1) = 0;
		}
	}
	histo.at<uchar>(100, 100) = 0;
	// ...
	// step 4: display the histogram
	namedWindow("Display histogram image", WINDOW_AUTOSIZE);
	imshow("Display histogram image", histo);
	imwrite("./lena_histogram.bmp", histo);

	/* find connected component */
	int conn[512][512];
	int conn_iterator = 1;
	vector<int> eq_table; // global equivalence table
	eq_table.push_back(0);
	for(int i=0; i<binarized.rows; i++) {
		for(int j=0; j<binarized.cols; j++) {
			if(binarized.at<uchar>(i, j) == 0) { // this pixel is not what we want
				conn[i][j] = 0;
			} else { // this pixel is what we have interests in
				if(i == 0 && j == 0) { // no Left, no Up
					conn[i][j] = conn_iterator++;
					eq_table.push_back(0);
				} else if(i == 0) { // no Up, only Left
					if(conn[i][j-1] != 0) {
						conn[i][j] = conn[i][j-1];
					} else {
						conn[i][j] = conn_iterator++;
						eq_table.push_back(0);
					}
				} else if(j == 0) { // no Left, only Up
					if(conn[i-1][j] != 0) {
						conn[i][j] = conn[i-1][j];
					} else {
						conn[i][j] = conn_iterator++;
						eq_table.push_back(0);
					}
				} else { // both Left and Up
					if(conn[i-1][j] == 0 && conn[i][j-1] == 0) {
						conn[i][j] = conn_iterator++;
						eq_table.push_back(0);
					} else if(conn[i-1][j] == 0) {
						conn[i][j] = conn[i][j-1];
					} else if(conn[i][j-1] == 0) {
						conn[i][j] = conn[i-1][j];
					} else if(conn[i-1][j] == conn[i][j-1]) { // both Left and Up != 0, but they are the same
						conn[i][j] = conn[i-1][j];
					} else { // Equivalence found: both Left and Up are not 0, and they differ!
						// record the equivalence, and assign conn[i][j] to the smaller one (Left / Up)
						if(conn[i-1][j] < conn[i][j-1]) { // Up is smaller than Left
							if(eq_table[conn[i-1][j]] == 0 && eq_table[conn[i][j-1]] == 0) { // Up and Left are both root
								eq_table[conn[i][j-1]] = conn[i-1][j]; // assign Left to Up
							} else if(eq_table[conn[i-1][j]] == 0) { // Up is root but Left is not
								eq_table[eq_table[conn[i][j-1]]] = conn[i-1][j]; // point Left's root to Up
								for(int k=0; k<eq_table.size(); k++) {
									// every Left's siblings (including Left) should be point to Up
									if(eq_table[k] == eq_table[conn[i][j-1]])
										eq_table[k] = conn[i-1][j];
								}
							} else if(eq_table[conn[i][j-1]] == 0){ // Up is not root but Left is
								eq_table[conn[i][j-1]] = eq_table[conn[i-1][j]]; // assign Left to Up's root
							} else { // both Up and Left are not root
								int left_root = eq_table[conn[i][j-1]];
								int right_root = eq_table[conn[i-1][j]];
								if(left_root < right_root) { // left root is smaller than right root
									// point right root -> left root
									eq_table[right_root] = left_root;
									for(int k=0; k<eq_table.size(); k++) {
										if(eq_table[k] == right_root)
											eq_table[k] = left_root;
									}
								} else if(right_root < left_root) { // right root is smaller than left root
									// point left root -> right root
									eq_table[left_root] = right_root;
									for(int k=0; k<eq_table.size(); k++)
										if(eq_table[k] == left_root)
											eq_table[k] = right_root;
								}
							}
							conn[i][j] = conn[i-1][j]; // assign conn[i][j] to the smaller one
						} else { // Left is smaller than Up
							if(eq_table[conn[i-1][j]] == 0 && eq_table[conn[i][j-1]] == 0) { // Up and Left are both root
								eq_table[conn[i-1][j]] = conn[i][j-1]; // assign Up to Left
							} else if(eq_table[conn[i-1][j]] == 0) { // Up is root but Left is not
								// point Up to Left's root
								eq_table[conn[i-1][j]] = eq_table[conn[i][j-1]];
							} else if(eq_table[conn[i][j-1]] == 0){ // Up is not root but Left is
								// point Up's root to Left, and all Up's sibling should be pointing to Left too
								eq_table[eq_table[conn[i-1][j]]] = conn[i][j-1];
								for(int k=0; k<eq_table.size(); k++) {
									if(eq_table[k] == eq_table[conn[i-1][j]])
										eq_table[k] = conn[i][j-1];
								}
							} else { // both Up and Left are not root
								int left_root = eq_table[conn[i][j-1]];
								int right_root = eq_table[conn[i-1][j]];
								if(left_root < right_root) { // left root is smaller than right root
									// point right root -> left root
									eq_table[right_root] = left_root;
									for(int k=0; k<eq_table.size(); k++) {
										if(eq_table[k] == right_root)
											eq_table[k] = left_root;
									}
								} else if(right_root < left_root) { // right root is smaller than left root
									// point left root -> right root
									eq_table[left_root] = right_root;
									for(int k=0; k<eq_table.size(); k++)
										if(eq_table[k] == left_root)
											eq_table[k] = right_root;
								}
							}
							conn[i][j] = conn[i][j-1]; // assign conn[i][j] to the smaller one
						}
					}
				}
			}
		}
	}

	// debug: output "conn" and "eq_table"
	/*
	cout << "Let's take a look at conn: " << endl;
	for(int i=0; i<512; i++) {
		for(int j=0; j<512; j++) {
			cout << conn[i][j] << " ";
		}
		cout << endl;
	}

	cout << "Let's take a look at eq_table: " << endl;
	for(int i=0; i<eq_table.size(); i++) {
		cout << i << " " << eq_table[i] << endl;
	}
	*/

	int MAX_EQ_TABLE_ENTRY = 0;
	/* every pixel reset to their root */
	for(int i=0; i<512; i++) {
		for(int j=0; j<512; j++) {
			if(conn[i][j] == 0) // we don't care about this pixel
				continue;
			if(eq_table[conn[i][j]] != 0)
				conn[i][j] = eq_table[conn[i][j]];
			if(conn[i][j] > MAX_EQ_TABLE_ENTRY)
				MAX_EQ_TABLE_ENTRY = conn[i][j];
		}
	}

	/*
	cout << "Let's take a look at conn AGAIN: " << endl;
	for(int i=0; i<512; i++) {
		for(int j=0; j<100; j++) {
			cout << conn[i][j] << " ";
		}
		cout << endl;
	}

	cout << "MAX_EQ_TABLE_ENTRY = " << MAX_EQ_TABLE_ENTRY << endl;
	*/

	/* do the calculation */
	int conn_component_counter[MAX_EQ_TABLE_ENTRY][5]; // pixel_count, left_margin, right_margin, up_margin, bottom_margin
	memset(conn_component_counter, 0, sizeof(conn_component_counter));
	for(int i=0; i<512; i++) {
		for(int j=0; j<512; j++) {
			if(conn[i][j] == 0) // we don't care about this pixel
				continue;
			if(conn_component_counter[conn[i][j]][0] == 0) {
				// first pixel of this connected component
				conn_component_counter[conn[i][j]][0] += 1; // pixel count (1)
				conn_component_counter[conn[i][j]][1] = j; // left_margin
				conn_component_counter[conn[i][j]][2] = j; // right_margin
				conn_component_counter[conn[i][j]][3] = i; // up_margin
				conn_component_counter[conn[i][j]][4] = i; // bottom_margin
			} else {
				conn_component_counter[conn[i][j]][0] += 1; // update pixel_count
				if(j < conn_component_counter[conn[i][j]][1])
					conn_component_counter[conn[i][j]][1] = j; // update left_margin
				if(j > conn_component_counter[conn[i][j]][2])
					conn_component_counter[conn[i][j]][2] = j; // update right_margin
				if(i < conn_component_counter[conn[i][j]][3])
					conn_component_counter[conn[i][j]][3] = i; // update up_margin
				if(i > conn_component_counter[conn[i][j]][4])
					conn_component_counter[conn[i][j]][4] = i; // update bottom_margin
			}
		}
	}
	
	/* debug: output conn_component_counter[][] */
	/*
	for(int i=0; i<MAX_EQ_TABLE_ENTRY; i++) {
		// let's output those with no less than 500 pixels
		if(conn_component_counter[i][0] >= 500) {
			cout << "Component " << i << ": " << endl;
			cout << conn_component_counter[i][0] << " pixels" << endl;
			cout << "Left margin: " << conn_component_counter[i][1] << endl;
			cout << "Right margin: " << conn_component_counter[i][2] << endl;
			cout << "Up margin: " << conn_component_counter[i][3] << endl;
			cout << "Bottom margin: " << conn_component_counter[i][4] << endl;
			cout << endl;
		}
	}
	*/

	/* show the connected component we found, by drawing bounding boxes */
	Mat connected = binarized.clone();
	// step 1: light off the binarized image
	for(int i=0; i<connected.rows; i++) {
		for(int j=0; j<connected.cols; j++) {
			if(connected.at<uchar>(i, j) == 0)
				connected.at<uchar>(i, j) = 100;
		}
	}
	// step 2: draw the bounding boxes
	for(int i=0; i<MAX_EQ_TABLE_ENTRY; i++) {
		if(conn_component_counter[i][0] >= 500) { // we want only pixel_count >= 500
			// ...
			int left = conn_component_counter[i][1];
			int right = conn_component_counter[i][2];
			int up = conn_component_counter[i][3];
			int bottom = conn_component_counter[i][4];
			for(int j=left; j<=right; j++) {
				connected.at<uchar>(up, j) = 0;
				connected.at<uchar>(bottom, j) = 0;
			}
			for(int j=up; j<=bottom; j++) {
				connected.at<uchar>(j, left) = 0;
				connected.at<uchar>(j, right) = 0;
			}
		}
	}
	namedWindow("Display connected_component image", WINDOW_AUTOSIZE);
	imshow("Display connected_component image", connected);
	imwrite("./lena_connected_component.bmp", connected);



	waitKey();
	return 0;
}

