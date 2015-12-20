
import os, sys
from math import sqrt
from PIL import Image

####################
# global variables #
####################

DIGITAL_LAPLACIAN_MASK_1 = [
	0, 1, 0, 1, -4, 1, 0, 1, 0
]

DIGITAL_LAPLACIAN_MASK_2 = [
	1, 1, 1, 1, -8, 1, 1, 1, 1
]

DIGITAL_LAPLACIAN_MINIMUM_VARIANCE_MASK = [
	2, -1, 2, -1, -4, -1, 2, -1, 2
]

LAPLACIAN_OF_GAUSSIAN_KERNEL = [
	0, 0, 0, -1, -1, -2, -1, -1, 0, 0, 0,
	0, 0, -2, -4, -8, -9, -8, -4, -2, 0, 0,
	0, -2, -7, -15, -22, -23, -22, -15, -7, -2, 0,
	-1, -4, -15, -24, -14, -1, -14, -24, -15, -4, -1,
	-1, -8, -22, -14, 52, 103, 52, -14, -22, -8, -1,
	-2, -9, -23, -1, 103, 178, 103, -1, -23, -9, -2,
	-1, -8, -22, -14, 52, 103, 52, -14, -22, -8, -1,
	-1, -4, -15, -24, -14, -1, -14, -24, -15, -4, -1,
	0, -2, -7, -15, -22, -23, -22, -15, -7, -2, 0,
	0, 0, -2, -4, -8, -9, -8, -4, -2, 0, 0,
	0, 0, 0, -1, -1, -2, -1, -1, 0, 0, 0
]

DIFFERENCE_OF_GAUSSIAN_MASK = [
	-1, -3, -4, -6, -7, -8, -7, -6, -4, -3, -1,
	-3, -5, -8, -11, -13, -13, -13, -11, -8, -5, -3,
	-4, -8, -12, -16, -17, -17, -17, -16, -12, -8, -4,
	-6, -11, -16, -16, 0, 15, 0, -16, -16, -11, -6,
	-7, -13, -17, 0, 85, 160, 85, 0, -17, -13, -7,
	-8, -13, -17, 15, 160, 283, 160, 15, -17, -13, -8,
	-7, -13, -17, 0, 85, 160, 85, 0, -17, -13, -7,
	-6, -11, -16, -16, 0, 15, 0, -16, -16, -11, -6,
	-4, -8, -12, -16, -17, -17, -17, -16, -12, -8, -4,
	-3, -5, -8, -11, -13, -13, -13, -11, -8, -5, -3,
	-1, -3, -4, -6, -7, -8, -7, -6, -4, -3, -1
]

DOG_MASK = list(DIFFERENCE_OF_GAUSSIAN_MASK) # just a copy

#####################
# utility functions #
#####################

def print_usage():
	print >> sys.stderr, "Usage:\n$python " + __file__ + " <img path>"

def doLaplacian(src, threshold, type):
	# error handling
	if type != 1 and type != 2:
		# error... wrong type given
		print >> sys.stderr, "doLaplacian(): error, wrong type given:", type
		return src
	srcPixels = src.load()
	# initialize the map
	mapp = []
	for i in range(src.size[0]):
		mapp.append(([0] * src.size[1]))
	# time to compute
	for i in range(1, src.size[0] - 1):
		for j in range(1, src.size[1] - 1):
			neighbors = [
				srcPixels[i-1, j-1],
				srcPixels[i, j-1],
				srcPixels[i+1, j-1],
				srcPixels[i-1, j],
				srcPixels[i, j],
				srcPixels[i+1, j],
				srcPixels[i-1, j+1],
				srcPixels[i, j+1],
				srcPixels[i+1, j+1]
			]
			if type == 1: # mask type 1
				coeff = DIGITAL_LAPLACIAN_MASK_1
			else: # mask type 2
				coeff = DIGITAL_LAPLACIAN_MASK_2
			mapp[i][j] = sum([coeff[k] * neighbors[k] for k in range(len(neighbors))])
			if type == 2:
				mapp[i][j] *= (1.0 / 3.0)
			if mapp[i][j] > threshold:
				mapp[i][j] = 1
			elif mapp[i][j] < -threshold:
				mapp[i][j] = -1
			else:
				mapp[i][j] = 0
	# create new image, set the value, and return it
	newImage = Image.new(src.mode, src.size)
	newImagePixels = newImage.load()
	for i in range(src.size[0]):
		for j in range(src.size[1]):
			if mapp[i][j] == 1:
				try:
					neighbors_value = [
						mapp[i-1][j-1],
						mapp[i][j-1],
						mapp[i+1][j-1],
						mapp[i-1][j],
						mapp[i][j],
						mapp[i+1][j],
						mapp[i-1][j+1],
						mapp[i][j+1],
						mapp[i+1][j+1],
					]
					if -1 in neighbors_value:
						newImagePixels[i, j] = 0
					else:
						newImagePixels[i, j] = 255
				except:
					newImagePixels[i, j] = 255
			elif mapp[i][j] == -1:
				try:
					neighbors_value = [
						mapp[i-1][j-1],
						mapp[i][j-1],
						mapp[i+1][j-1],
						mapp[i-1][j],
						mapp[i][j],
						mapp[i+1][j],
						mapp[i-1][j+1],
						mapp[i][j+1],
						mapp[i+1][j+1],
					]
					if 1 in neighbors_value:
						newImagePixels[i, j] = 0
					else:
						newImagePixels[i, j] = 255
				except:
					newImagePixels[i, j] = 255
			else:
				newImagePixels[i, j] = 255 # set to white
	return newImage

def doMinimumVarianceLaplacian(src, threshold):
	srcPixels = src.load()
	# initialize the map
	mapp = []
	for i in range(src.size[0]):
		mapp.append(([0] * src.size[1]))
	# time to compute
	for i in range(1, src.size[0] - 1):
		for j in range(1, src.size[1] - 1):
			neighbors = [
				srcPixels[i-1, j-1],
				srcPixels[i, j-1],
				srcPixels[i+1, j-1],
				srcPixels[i-1, j],
				srcPixels[i, j],
				srcPixels[i+1, j],
				srcPixels[i-1, j+1],
				srcPixels[i, j+1],
				srcPixels[i+1, j+1]
			]
			coeff = DIGITAL_LAPLACIAN_MINIMUM_VARIANCE_MASK
			mapp[i][j] = sum([coeff[k] * neighbors[k] for k in range(len(neighbors))])
			mapp[i][j] *= (1.0 / 3.0)
			if mapp[i][j] > threshold:
				mapp[i][j] = 1
			elif mapp[i][j] < -threshold:
				mapp[i][j] = -1
			else:
				mapp[i][j] = 0
	# create new image, set the value, and return it
	newImage = Image.new(src.mode, src.size)
	newImagePixels = newImage.load()
	for i in range(src.size[0]):
		for j in range(src.size[1]):
			if mapp[i][j] == 1:
				try:
					neighbors_value = [
						mapp[i-1][j-1],
						mapp[i][j-1],
						mapp[i+1][j-1],
						mapp[i-1][j],
						mapp[i][j],
						mapp[i+1][j],
						mapp[i-1][j+1],
						mapp[i][j+1],
						mapp[i+1][j+1],
					]
					if -1 in neighbors_value:
						newImagePixels[i, j] = 0
					else:
						newImagePixels[i, j] = 255
				except:
					newImagePixels[i, j] = 255
			elif mapp[i][j] == -1:
				try:
					neighbors_value = [
						mapp[i-1][j-1],
						mapp[i][j-1],
						mapp[i+1][j-1],
						mapp[i-1][j],
						mapp[i][j],
						mapp[i+1][j],
						mapp[i-1][j+1],
						mapp[i][j+1],
						mapp[i+1][j+1],
					]
					if 1 in neighbors_value:
						newImagePixels[i, j] = 0
					else:
						newImagePixels[i, j] = 255
				except:
					newImagePixels[i, j] = 255
			else:
				newImagePixels[i, j] = 255 # set to white
	return newImage

def doLaplacianOfGaussian(src, threshold):
	srcPixels = src.load()
	# initialize the map
	mapp = []
	for i in range(src.size[0]):
		mapp.append(([0] * src.size[1]))
	# time to compute
	for i in range(5, src.size[0] - 5):
		for j in range(5, src.size[1] - 5):
			neighbors = [
				srcPixels[i-5, j-5],
				srcPixels[i-4, j-5],
				srcPixels[i-3, j-5],
				srcPixels[i-2, j-5],
				srcPixels[i-1, j-5],
				srcPixels[i, j-5],
				srcPixels[i+1, j-5],
				srcPixels[i+2, j-5],
				srcPixels[i+3, j-5],
				srcPixels[i+4, j-5],
				srcPixels[i+5, j-5],
				srcPixels[i-5, j-4],
				srcPixels[i-4, j-4],
				srcPixels[i-3, j-4],
				srcPixels[i-2, j-4],
				srcPixels[i-1, j-4],
				srcPixels[i, j-4],
				srcPixels[i+1, j-4],
				srcPixels[i+2, j-4],
				srcPixels[i+3, j-4],
				srcPixels[i+4, j-4],
				srcPixels[i+5, j-4],
				srcPixels[i-5, j-3],
				srcPixels[i-4, j-3],
				srcPixels[i-3, j-3],
				srcPixels[i-2, j-3],
				srcPixels[i-1, j-3],
				srcPixels[i, j-3],
				srcPixels[i+1, j-3],
				srcPixels[i+2, j-3],
				srcPixels[i+3, j-3],
				srcPixels[i+4, j-3],
				srcPixels[i+5, j-3],
				srcPixels[i-5, j-2],
				srcPixels[i-4, j-2],
				srcPixels[i-3, j-2],
				srcPixels[i-2, j-2],
				srcPixels[i-1, j-2],
				srcPixels[i, j-2],
				srcPixels[i+1, j-2],
				srcPixels[i+2, j-2],
				srcPixels[i+3, j-2],
				srcPixels[i+4, j-2],
				srcPixels[i+5, j-2],
				srcPixels[i-5, j-1],
				srcPixels[i-4, j-1],
				srcPixels[i-3, j-1],
				srcPixels[i-2, j-1],
				srcPixels[i-1, j-1],
				srcPixels[i, j-1],
				srcPixels[i+1, j-1],
				srcPixels[i+2, j-1],
				srcPixels[i+3, j-1],
				srcPixels[i+4, j-1],
				srcPixels[i+5, j-1],
				srcPixels[i-5, j],
				srcPixels[i-4, j],
				srcPixels[i-3, j],
				srcPixels[i-2, j],
				srcPixels[i-1, j],
				srcPixels[i, j],
				srcPixels[i+1, j],
				srcPixels[i+2, j],
				srcPixels[i+3, j],
				srcPixels[i+4, j],
				srcPixels[i+5, j],
				srcPixels[i-5, j+1],
				srcPixels[i-4, j+1],
				srcPixels[i-3, j+1],
				srcPixels[i-2, j+1],
				srcPixels[i-1, j+1],
				srcPixels[i, j+1],
				srcPixels[i+1, j+1],
				srcPixels[i+2, j+1],
				srcPixels[i+3, j+1],
				srcPixels[i+4, j+1],
				srcPixels[i+5, j+1],
				srcPixels[i-5, j+2],
				srcPixels[i-4, j+2],
				srcPixels[i-3, j+2],
				srcPixels[i-2, j+2],
				srcPixels[i-1, j+2],
				srcPixels[i, j+2],
				srcPixels[i+1, j+2],
				srcPixels[i+2, j+2],
				srcPixels[i+3, j+2],
				srcPixels[i+4, j+2],
				srcPixels[i+5, j+2],
				srcPixels[i-5, j+3],
				srcPixels[i-4, j+3],
				srcPixels[i-3, j+3],
				srcPixels[i-2, j+3],
				srcPixels[i-1, j+3],
				srcPixels[i, j+3],
				srcPixels[i+1, j+3],
				srcPixels[i+2, j+3],
				srcPixels[i+3, j+3],
				srcPixels[i+4, j+3],
				srcPixels[i+5, j+3],
				srcPixels[i-5, j+4],
				srcPixels[i-4, j+4],
				srcPixels[i-3, j+4],
				srcPixels[i-2, j+4],
				srcPixels[i-1, j+4],
				srcPixels[i, j+4],
				srcPixels[i+1, j+4],
				srcPixels[i+2, j+4],
				srcPixels[i+3, j+4],
				srcPixels[i+4, j+4],
				srcPixels[i+5, j+4],
				srcPixels[i-5, j+5],
				srcPixels[i-4, j+5],
				srcPixels[i-3, j+5],
				srcPixels[i-2, j+5],
				srcPixels[i-1, j+5],
				srcPixels[i, j+5],
				srcPixels[i+1, j+5],
				srcPixels[i+2, j+5],
				srcPixels[i+3, j+5],
				srcPixels[i+4, j+5],
				srcPixels[i+5, j+5]
			]
			coeff = LAPLACIAN_OF_GAUSSIAN_KERNEL
			mapp[i][j] = sum([coeff[k] * neighbors[k] for k in range(len(neighbors))])
			if mapp[i][j] > threshold:
				mapp[i][j] = 1
			elif mapp[i][j] < -threshold:
				mapp[i][j] = -1
			else:
				mapp[i][j] = 0
	# create new image, set the value, and return it
	newImage = Image.new(src.mode, src.size)
	newImagePixels = newImage.load()
	for i in range(src.size[0]):
		for j in range(src.size[1]):
			if mapp[i][j] == 1:
				try:
					neighbors_value = [
						mapp[i-1][j-1],
						mapp[i][j-1],
						mapp[i+1][j-1],
						mapp[i-1][j],
						mapp[i][j],
						mapp[i+1][j],
						mapp[i-1][j+1],
						mapp[i][j+1],
						mapp[i+1][j+1],
					]
					if -1 in neighbors_value:
						newImagePixels[i, j] = 0
					else:
						newImagePixels[i, j] = 255
				except:
					newImagePixels[i, j] = 255
			elif mapp[i][j] == -1:
				try:
					neighbors_value = [
						mapp[i-1][j-1],
						mapp[i][j-1],
						mapp[i+1][j-1],
						mapp[i-1][j],
						mapp[i][j],
						mapp[i+1][j],
						mapp[i-1][j+1],
						mapp[i][j+1],
						mapp[i+1][j+1],
					]
					if 1 in neighbors_value:
						newImagePixels[i, j] = 0
					else:
						newImagePixels[i, j] = 255
				except:
					newImagePixels[i, j] = 255
			else:
				newImagePixels[i, j] = 255 # set to white
	return newImage

def doDifferenceOfGaussian(src, threshold):
	srcPixels = src.load()
	# initialize the map
	mapp = []
	for i in range(src.size[0]):
		mapp.append(([0] * src.size[1]))
	# time to compute
	for i in range(5, src.size[0] - 5):
		for j in range(5, src.size[1] - 5):
			neighbors = [
				srcPixels[i-5, j-5],
				srcPixels[i-4, j-5],
				srcPixels[i-3, j-5],
				srcPixels[i-2, j-5],
				srcPixels[i-1, j-5],
				srcPixels[i, j-5],
				srcPixels[i+1, j-5],
				srcPixels[i+2, j-5],
				srcPixels[i+3, j-5],
				srcPixels[i+4, j-5],
				srcPixels[i+5, j-5],
				srcPixels[i-5, j-4],
				srcPixels[i-4, j-4],
				srcPixels[i-3, j-4],
				srcPixels[i-2, j-4],
				srcPixels[i-1, j-4],
				srcPixels[i, j-4],
				srcPixels[i+1, j-4],
				srcPixels[i+2, j-4],
				srcPixels[i+3, j-4],
				srcPixels[i+4, j-4],
				srcPixels[i+5, j-4],
				srcPixels[i-5, j-3],
				srcPixels[i-4, j-3],
				srcPixels[i-3, j-3],
				srcPixels[i-2, j-3],
				srcPixels[i-1, j-3],
				srcPixels[i, j-3],
				srcPixels[i+1, j-3],
				srcPixels[i+2, j-3],
				srcPixels[i+3, j-3],
				srcPixels[i+4, j-3],
				srcPixels[i+5, j-3],
				srcPixels[i-5, j-2],
				srcPixels[i-4, j-2],
				srcPixels[i-3, j-2],
				srcPixels[i-2, j-2],
				srcPixels[i-1, j-2],
				srcPixels[i, j-2],
				srcPixels[i+1, j-2],
				srcPixels[i+2, j-2],
				srcPixels[i+3, j-2],
				srcPixels[i+4, j-2],
				srcPixels[i+5, j-2],
				srcPixels[i-5, j-1],
				srcPixels[i-4, j-1],
				srcPixels[i-3, j-1],
				srcPixels[i-2, j-1],
				srcPixels[i-1, j-1],
				srcPixels[i, j-1],
				srcPixels[i+1, j-1],
				srcPixels[i+2, j-1],
				srcPixels[i+3, j-1],
				srcPixels[i+4, j-1],
				srcPixels[i+5, j-1],
				srcPixels[i-5, j],
				srcPixels[i-4, j],
				srcPixels[i-3, j],
				srcPixels[i-2, j],
				srcPixels[i-1, j],
				srcPixels[i, j],
				srcPixels[i+1, j],
				srcPixels[i+2, j],
				srcPixels[i+3, j],
				srcPixels[i+4, j],
				srcPixels[i+5, j],
				srcPixels[i-5, j+1],
				srcPixels[i-4, j+1],
				srcPixels[i-3, j+1],
				srcPixels[i-2, j+1],
				srcPixels[i-1, j+1],
				srcPixels[i, j+1],
				srcPixels[i+1, j+1],
				srcPixels[i+2, j+1],
				srcPixels[i+3, j+1],
				srcPixels[i+4, j+1],
				srcPixels[i+5, j+1],
				srcPixels[i-5, j+2],
				srcPixels[i-4, j+2],
				srcPixels[i-3, j+2],
				srcPixels[i-2, j+2],
				srcPixels[i-1, j+2],
				srcPixels[i, j+2],
				srcPixels[i+1, j+2],
				srcPixels[i+2, j+2],
				srcPixels[i+3, j+2],
				srcPixels[i+4, j+2],
				srcPixels[i+5, j+2],
				srcPixels[i-5, j+3],
				srcPixels[i-4, j+3],
				srcPixels[i-3, j+3],
				srcPixels[i-2, j+3],
				srcPixels[i-1, j+3],
				srcPixels[i, j+3],
				srcPixels[i+1, j+3],
				srcPixels[i+2, j+3],
				srcPixels[i+3, j+3],
				srcPixels[i+4, j+3],
				srcPixels[i+5, j+3],
				srcPixels[i-5, j+4],
				srcPixels[i-4, j+4],
				srcPixels[i-3, j+4],
				srcPixels[i-2, j+4],
				srcPixels[i-1, j+4],
				srcPixels[i, j+4],
				srcPixels[i+1, j+4],
				srcPixels[i+2, j+4],
				srcPixels[i+3, j+4],
				srcPixels[i+4, j+4],
				srcPixels[i+5, j+4],
				srcPixels[i-5, j+5],
				srcPixels[i-4, j+5],
				srcPixels[i-3, j+5],
				srcPixels[i-2, j+5],
				srcPixels[i-1, j+5],
				srcPixels[i, j+5],
				srcPixels[i+1, j+5],
				srcPixels[i+2, j+5],
				srcPixels[i+3, j+5],
				srcPixels[i+4, j+5],
				srcPixels[i+5, j+5]
			]
			coeff = DIFFERENCE_OF_GAUSSIAN_MASK
			mapp[i][j] = sum([coeff[k] * neighbors[k] for k in range(len(neighbors))])
			if mapp[i][j] > threshold:
				mapp[i][j] = 1
			elif mapp[i][j] < -threshold:
				mapp[i][j] = -1
			else:
				mapp[i][j] = 0
	# create new image, set the value, and return it
	newImage = Image.new(src.mode, src.size)
	newImagePixels = newImage.load()
	for i in range(src.size[0]):
		for j in range(src.size[1]):
			if mapp[i][j] == 1:
				try:
					neighbors_value = [
						mapp[i-1][j-1],
						mapp[i][j-1],
						mapp[i+1][j-1],
						mapp[i-1][j],
						mapp[i][j],
						mapp[i+1][j],
						mapp[i-1][j+1],
						mapp[i][j+1],
						mapp[i+1][j+1],
					]
					if -1 in neighbors_value:
						newImagePixels[i, j] = 0
					else:
						newImagePixels[i, j] = 255
				except:
					newImagePixels[i, j] = 255
			elif mapp[i][j] == -1:
				try:
					neighbors_value = [
						mapp[i-1][j-1],
						mapp[i][j-1],
						mapp[i+1][j-1],
						mapp[i-1][j],
						mapp[i][j],
						mapp[i+1][j],
						mapp[i-1][j+1],
						mapp[i][j+1],
						mapp[i+1][j+1],
					]
					if 1 in neighbors_value:
						newImagePixels[i, j] = 0
					else:
						newImagePixels[i, j] = 255
				except:
					newImagePixels[i, j] = 255
			else:
				newImagePixels[i, j] = 255 # set to white
	return newImage

######################
# main program entry #
######################

if __name__ == "__main__":

	# check the argument
	if len(sys.argv) != 2:
		print_usage()
		sys.exit(1)

	# load the original image
	try:
		orig = Image.open(sys.argv[1])
	except:
		print >> sys.stderr, "fatal: cannot open image at: " + sys.argv[1]
		sys.exit(1)

	# Digital Laplacian: type 1
	doLaplacian(orig, 15, 1).save("laplacian_1.bmp")

	# Digital Laplacian: type 2
	doLaplacian(orig, 15, 2).save("laplacian_2.bmp")

	# Minimum-Variance Laplacian
	doMinimumVarianceLaplacian(orig, 20).save("min_var_laplacian.bmp")

	# Laplacian of Gaussian
	doLaplacianOfGaussian(orig, 3000).save("laplacian_of_gaussian.bmp")
	
	# Difference of Gaussian
	doDifferenceOfGaussian(orig, 1).save("diff_of_gaussian.bmp")








