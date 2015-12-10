
import os, sys
from math import sqrt
from PIL import Image

#####################
# utility functions #
#####################

def print_usage():
	print >> sys.stderr, "Usage:\n$python " + __file__ + " <img path>"

def doRobertDetection(src, threshold):
	srcPixels = src.load()
	# initialize Gx and Gy with zero's
	Gx = []
	Gy = []
	for i in range(src.size[0]):
		Gx.append(([0] * src.size[1]))
		Gy.append(([0] * src.size[1]))
	# computing Gx
	for i in range(src.size[0] - 1):
		for j in range(src.size[1] - 1):
			Gx[i][j] = (-1) * srcPixels[i, j] + 0 * srcPixels[i + 1, j] + 0 * srcPixels[i, j + 1] + 1 * srcPixels[i + 1, j + 1]
	# computing Gy
	for i in range(src.size[0] - 1):
		for j in range(src.size[1] - 1):
			Gy[i][j] = 0 * srcPixels[i, j] + (-1) * srcPixels[i + 1, j] + 1 * srcPixels[i, j + 1] + 0 * srcPixels[i + 1, j + 1]
	# create new image, set the value, and return it
	newImage = Image.new(src.mode, src.size)
	newImagePixels = newImage.load()
	for i in range(src.size[0]):
		for j in range(src.size[1]):
			# if > threshold: black; otherwise, white.
			newImagePixels[i, j] = 0 if sqrt(Gx[i][j] ** 2 + Gy[i][j] ** 2) > threshold else 255
	return newImage

def doPrewittDetection(src, threshold):
	srcPixels = src.load()
	# initialize Gx and Gy with zero's
	Gx = []
	Gy = []
	for i in range(src.size[0]):
		Gx.append(([0] * src.size[1]))
		Gy.append(([0] * src.size[1]))
	# computing Gx
	for i in range(1, src.size[0] - 1):
		for j in range(1, src.size[1] - 1):
			# -1, -1, -1, 0, 0, 0, 1, 1, 1
			Gx[i][j] = (
				(-1) * srcPixels[i-1, j-1]
				+ (-1) * srcPixels[i, j-1]
				+ (-1) * srcPixels[i+1, j-1]
				+ 0 * srcPixels[i-1, j]
				+ 0 * srcPixels[i, j]
				+ 0 * srcPixels[i+1, j]
				+ 1 * srcPixels[i-1, j+1]
				+ 1 * srcPixels[i, j+1]
				+ 1 * srcPixels[i+1, j+1]
			)
	# computing Gy
	for i in range(1, src.size[0] - 1):
		for j in range(1, src.size[1] - 1):
			# -1, 0, 1, -1, 0, 1, -1, 0, 1
			Gy[i][j] = (
				(-1) * srcPixels[i-1, j-1]
				+ 0 * srcPixels[i, j-1]
				+ 1 * srcPixels[i+1, j-1]
				+ (-1) * srcPixels[i-1, j]
				+ 0 * srcPixels[i, j]
				+ 1 * srcPixels[i+1, j]
				+ (-1) * srcPixels[i-1, j+1]
				+ 0 * srcPixels[i, j+1]
				+ 1 * srcPixels[i+1, j+1]
			)
	# create new image, set the value, and return it
	newImage = Image.new(src.mode, src.size)
	newImagePixels = newImage.load()
	for i in range(src.size[0]):
		for j in range(src.size[1]):
			# if > threshold: black; otherwise, white.
			newImagePixels[i, j] = 0 if sqrt(Gx[i][j] ** 2 + Gy[i][j] ** 2) > threshold else 255
	return newImage

def doSobelDetection(src, threshold):
	srcPixels = src.load()
	# initialize Gx and Gy with zero's
	Gx = []
	Gy = []
	for i in range(src.size[0]):
		Gx.append(([0] * src.size[1]))
		Gy.append(([0] * src.size[1]))
	# computing Gx
	for i in range(1, src.size[0] - 1):
		for j in range(1, src.size[1] - 1):
			# -1, -2, -1, 0, 0, 0, 1, 2, 1
			Gx[i][j] = (
				(-1) * srcPixels[i-1, j-1]
				+ (-2) * srcPixels[i, j-1]
				+ (-1) * srcPixels[i+1, j-1]
				+ 0 * srcPixels[i-1, j]
				+ 0 * srcPixels[i, j]
				+ 0 * srcPixels[i+1, j]
				+ 1 * srcPixels[i-1, j+1]
				+ 2 * srcPixels[i, j+1]
				+ 1 * srcPixels[i+1, j+1]
			)
	# computing Gy
	for i in range(1, src.size[0] - 1):
		for j in range(1, src.size[1] - 1):
			# -1, 0, 1, -2, 0, 2, -1, 0, 1
			Gy[i][j] = (
				(-1) * srcPixels[i-1, j-1]
				+ 0 * srcPixels[i, j-1]
				+ 1 * srcPixels[i+1, j-1]
				+ (-2) * srcPixels[i-1, j]
				+ 0 * srcPixels[i, j]
				+ 2 * srcPixels[i+1, j]
				+ (-1) * srcPixels[i-1, j+1]
				+ 0 * srcPixels[i, j+1]
				+ 1 * srcPixels[i+1, j+1]
			)
	# create new image, set the value, and return it
	newImage = Image.new(src.mode, src.size)
	newImagePixels = newImage.load()
	for i in range(src.size[0]):
		for j in range(src.size[1]):
			# if > threshold: black; otherwise, white.
			newImagePixels[i, j] = 0 if sqrt(Gx[i][j] ** 2 + Gy[i][j] ** 2) > threshold else 255
	return newImage

def doFreiAndChenDetector(src, threshold):
	srcPixels = src.load()
	# initialize Gx and Gy with zero's
	Gx = []
	Gy = []
	for i in range(src.size[0]):
		Gx.append(([0] * src.size[1]))
		Gy.append(([0] * src.size[1]))
	# computing Gx
	SquareRootOfTwo = sqrt(2)
	for i in range(1, src.size[0] - 1):
		for j in range(1, src.size[1] - 1):
			# -1, -sqrt(2), -1, 0, 0, 0, 1, sqrt(2), 1
			Gx[i][j] = (
				(-1) * srcPixels[i-1, j-1]
				+ (-SquareRootOfTwo) * srcPixels[i, j-1]
				+ (-1) * srcPixels[i+1, j-1]
				+ 0 * srcPixels[i-1, j]
				+ 0 * srcPixels[i, j]
				+ 0 * srcPixels[i+1, j]
				+ 1 * srcPixels[i-1, j+1]
				+ SquareRootOfTwo * srcPixels[i, j+1]
				+ 1 * srcPixels[i+1, j+1]
			)
	# computing Gy
	for i in range(1, src.size[0] - 1):
		for j in range(1, src.size[1] - 1):
			# -1, 0, 1, -sqrt(2), 0, sqrt(2), -1, 0, 1
			Gy[i][j] = (
				(-1) * srcPixels[i-1, j-1]
				+ 0 * srcPixels[i, j-1]
				+ 1 * srcPixels[i+1, j-1]
				+ (-SquareRootOfTwo) * srcPixels[i-1, j]
				+ 0 * srcPixels[i, j]
				+ SquareRootOfTwo * srcPixels[i+1, j]
				+ (-1) * srcPixels[i-1, j+1]
				+ 0 * srcPixels[i, j+1]
				+ 1 * srcPixels[i+1, j+1]
			)
	# create new image, set the value, and return it
	newImage = Image.new(src.mode, src.size)
	newImagePixels = newImage.load()
	for i in range(src.size[0]):
		for j in range(src.size[1]):
			# if > threshold: black; otherwise, white.
			newImagePixels[i, j] = 0 if sqrt(Gx[i][j] ** 2 + Gy[i][j] ** 2) > threshold else 255
	return newImage

def doKirschDetector(src, threshold):
	srcPixels = src.load()
	# initialize gradient map with zero's
	gradientMap = [] # store the gradient magnitude of every pixel
	for i in range(src.size[0]):
		gradientMap.append(([0] * src.size[1]))
	# for every pixel, compute the 8 compasses and store the max into _gradientMap_
	for i in range(1, src.size[0] - 1):
		for j in range(1, src.size[1] - 1):
			# initialize a list of 8 zero's for storing 8 compasses
			compasses = [0 for k in range(8)]
			# get all the data we need
			coefficientList = [
				[-3, -3, 5, -3, 0, 5, -3, -3, 5],
				[-3, 5, 5, -3, 0, 5, -3, -3, -3],
				[5, 5, 5, -3, 0, -3, -3, -3, -3],
				[5, 5, -3, 5, 0, -3, -3, -3, -3],
				[5, -3, -3, 5, 0, -3, 5, -3, -3],
				[-3, -3, -3, 5, 0, -3, 5, 5, -3],
				[-3, -3, -3, -3, 0, -3, 5, 5, 5],
				[-3, -3, -3, -3, 0, 5, -3, 5, 5]
			]
			neighborList = [
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
			# compute the 8 compasses
			for k in range(8):
				compasses[k] = sum([coefficientList[k][tmp] * neighborList[tmp] for tmp in range(9)])
			# put the max of 8 compasses into gradientMap
			gradientMap[i][j] = max(compasses)
	# create new image, set the value, and return it
	newImage = Image.new(src.mode, src.size)
	newImagePixels = newImage.load()
	for i in range(src.size[0]):
		for j in range(src.size[1]):
			# if > threshold: black; otherwise, white.
			newImagePixels[i, j] = 0 if gradientMap[i][j] > threshold else 255
	return newImage

def doRobinsonDetector(src, threshold):
	srcPixels = src.load()
	# initialize gradient map with zero's
	gradientMap = [] # store the gradient magnitude of every pixel
	for i in range(src.size[0]):
		gradientMap.append(([0] * src.size[1]))
	# for every pixel, compute the 8 compasses and store the max into _gradientMap_
	for i in range(1, src.size[0] - 1):
		for j in range(1, src.size[1] - 1):
			# initialize a list of 8 zero's for storing 8 compasses
			compasses = [0 for k in range(8)]
			# get all the data we need
			coefficientList = [
				[-1, 0, 1, -2, 0, 2, -1, 0, 1],
				[0, 1, 2, -1, 0, 1, -2, -1, 0],
				[1, 2, 1, 0, 0, 0, -1, -2, -1],
				[2, 1, 0, 1, 0, -1, 0, -2, -2],
				[1, 0, -1, 2, 0, -2, 1, 0, -1],
				[0, -1, -2, 1, 0, -1, 2, 1, 0],
				[-1, -2, -1, 0, 0, 0, 1, 2, 1],
				[-2, -1, 0, -1, 0, 1, 0, 1, 2]
			]
			neighborList = [
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
			# compute the 8 compasses
			for k in range(8):
				compasses[k] = sum([coefficientList[k][tmp] * neighborList[tmp] for tmp in range(9)])
			# put the max of 8 compasses into gradientMap
			gradientMap[i][j] = max(compasses)
	# create new image, set the value, and return it
	newImage = Image.new(src.mode, src.size)
	newImagePixels = newImage.load()
	for i in range(src.size[0]):
		for j in range(src.size[1]):
			# if > threshold: black; otherwise, white.
			newImagePixels[i, j] = 0 if gradientMap[i][j] > threshold else 255
	return newImage

def doNevatiaAndBabuDetector(src, threshold):
	srcPixels = src.load()
	# initialize gradient map with zero's
	gradientMap = [] # store the gradient magnitude of every pixel
	for i in range(src.size[0]):
		gradientMap.append(([0] * src.size[1]))
	# for every pixel, compute the 8 compasses and store the max into _gradientMap_
	for i in range(2, src.size[0] - 2):
		for j in range(2, src.size[1] - 2):
			# initialize a list of 8 zero's for storing 6 compasses
			compasses = [0 for k in range(6)]
			# get all the data we need
			coefficientList = [
				[100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 0, 0, 0, 0, 0, -100, -100, -100, -100, -100, -100, -100, -100, -100, -100],
				[100, 100, 100, 100, 100, 100, 100, 100, 78, -32, 100, 92, 0, -92, -100, 32, -78, -100, -100, -100, -100, -100, -100, -100, -100],
				[100, 100, 100, 32, -100, 100, 100, 92, -78, -100, 100, 100, 0, -100, -100, 100, 78, -92, -100, -100, 100, -32, -100, -100, -100],
				[-100, -100, 0, 100, 100, -100, -100, 0, 100, 100, -100, -100, 0, 100, 100, -100, -100, 0, 100, 100, -100, -100, 0, 100, 100],
				[-100, 32, 100, 100, 100, -100, -78, 92, 100, 100, -100, -100, 0, 100, 100, -100, -100, -92, 78, 100, -100, -100, -100, -32, 100],
				[100, 100, 100, 100, 100, -32, 78, 100, 100, 100, -100, -92, 0, 92, 100, -100, -100, -100, -78, 32, -100, -100, -100, -100, -100]
			] # actually there are 12, but it's "symmetric", and therefore we need to implement only 6.
			neighborList = [
				srcPixels[i-2, j-2],
				srcPixels[i-1, j-2],
				srcPixels[i, j-2],
				srcPixels[i+1, j-2],
				srcPixels[i+2, j-2],
				srcPixels[i-2, j-1],
				srcPixels[i-1, j-1],
				srcPixels[i, j-1],
				srcPixels[i+1, j-1],
				srcPixels[i+2, j-1],
				srcPixels[i-2, j],
				srcPixels[i-1, j],
				srcPixels[i, j],
				srcPixels[i+1, j],
				srcPixels[i+2, j],
				srcPixels[i-2, j+1],
				srcPixels[i-1, j+1],
				srcPixels[i, j+1],
				srcPixels[i+1, j+1],
				srcPixels[i+2, j+1],
				srcPixels[i-2, j+2],
				srcPixels[i-1, j+2],
				srcPixels[i, j+2],
				srcPixels[i+1, j+2],
				srcPixels[i+2, j+2]
			]
			# compute the 6 compasses
			for k in range(6):
				compasses[k] = abs(sum([coefficientList[k][tmp] * neighborList[tmp] for tmp in range(25)]))
			# put the max of 8 compasses into gradientMap
			gradientMap[i][j] = max(compasses)
	# create new image, set the value, and return it
	newImage = Image.new(src.mode, src.size)
	newImagePixels = newImage.load()
	for i in range(src.size[0]):
		for j in range(src.size[1]):
			# if > threshold: black; otherwise, white.
			newImagePixels[i, j] = 0 if gradientMap[i][j] > threshold else 255
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

	# robert's
	doRobertDetection(orig, 30).save("robert_30.bmp")

	# prewitt's
	doPrewittDetection(orig, 24).save("prewitt_24.bmp")

	# sobel's
	doSobelDetection(orig, 38).save("sobel_38.bmp")

	# frei and chen's
	doFreiAndChenDetector(orig, 30).save("frei_and_chen_30.bmp")

	# kirsch's
	doKirschDetector(orig, 135).save("kirsch_135.bmp")

	# robinson's
	doRobinsonDetector(orig, 43).save("robinson_43.bmp")

	# nevatia and babu's
	doNevatiaAndBabuDetector(orig, 12500).save("nevatia_and_babu_12500.bmp")

