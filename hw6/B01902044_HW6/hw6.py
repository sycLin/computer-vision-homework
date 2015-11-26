
import os, sys, math
from PIL import Image


#####################
# class definitions #
#####################

class RegionalOperator:
	def __init__(self, func1, func2):
		self.f = func1
		self.h = func2
	def getValue(self, *x):
		a1 = self.h(x[0], x[1], x[6], x[2])
		a2 = self.h(x[0], x[2], x[7], x[3])
		a3 = self.h(x[0], x[3], x[8], x[4])
		a4 = self.h(x[0], x[4], x[5], x[1])
		return self.f(a1, a2, a3, a4)


####################
# global variables #
####################
#
# Yokoi
#
def YokoiF(a1, a2, a3, a4):
	if a1 == a2 and a2 == a3 and a3 == a4 and a4 == 'r':
		return 5
	qCount = 0
	if a1 == 'q':
		qCount += 1
	if a2 == 'q':
		qCount += 1
	if a3 == 'q':
		qCount += 1
	if a4 == 'q':
		qCount += 1
	return qCount

def YokoiH(b, c, d, e):
	if b == c and (d != b or e != b):
		return 'q'
	if b == c and (d == b and e == b):
		return 'r'
	return 's'

Yokoi = RegionalOperator(YokoiF, YokoiH)


#####################
# utility functions #
#####################

def print_usage():
	print >> sys.stderr, "Usage:\n$python hw6.py <image path>"


"""
	This function sets pixels to 0 if they're less than $threshold$ in $src$.
	@param src should be an image
	@param threshold should be an integer (default 128 if not given)
	@return a binarized image instance
"""
def binarize(src, threshold=128):
	newImage = Image.new(src.mode, src.size)
	newImagePixels = newImage.load()
	for i in range(src.size[0]):
		for j in range(src.size[1]):
			old = src.getpixel((i, j))
			if old < 128:
				newImagePixels[i, j] = 0
			else:
				newImagePixels[i, j] = 255
	return newImage

"""
	This function does the downsampling.
	@param src should be an image
	@param block a 2-tuple representing a block, and we'll take upmost-left point of this block
	@return the new image downsampled
"""
def downSample(src, block=(8, 8)):
	# calculate the size of the down-sampled image
	newImageSize = [0, 0]
	newImageSize[0] = int(math.ceil(float(src.size[0]) / block[0]))
	newImageSize[1] = int(math.ceil(float(src.size[1]) / block[1]))
	# create the new image
	newImage = Image.new(src.mode, newImageSize)
	newImagePixels = newImage.load()
	# down-sampling
	srcPixels = src.load()
	for i in range(newImageSize[0]):
		for j in range(newImageSize[1]):
			newImagePixels[i, j] = srcPixels[i*block[0], j*block[1]]
	return newImage



######################
# main program entry #
######################

if __name__ == "__main__":
	# check the arguments
	if len(sys.argv) != 2:
		print_usage()
		sys.exit(1)

	# load the original image
	try:
		orig = Image.open(sys.argv[1])
	except:
		print >> sys.stderr, "fatal: wrong image path given"
		sys.exit(1)
	
	# binarize the image
	binarized = binarize(orig, 128)
	binarized.show()
	
	# down-sample the image
	downSampled = downSample(binarized, (8, 8))
	downSampled.show()

	# do the Yokoi connectivity number
	downSampledPixels = downSampled.load()
	yokoiResult = []
	for row in range(downSampled.size[1]):
		tmpList = []
		for col in range(downSampled.size[0]):
			# we are not interested in black pixels
			if downSampledPixels[col, row] == 0:
				tmpList.append(' ') # a blank space
			else:
				# get neighbors
				x0 = downSampledPixels[col, row]
				x1 = downSampledPixels[col+1, row] if (col+1 < downSampled.size[0]) else 0
				x2 = downSampledPixels[col, row-1] if (row-1 >= 0) else 0
				x3 = downSampledPixels[col-1, row] if (col-1 >= 0) else 0
				x4 = downSampledPixels[col, row+1] if (row+1 < downSampled.size[1]) else 0
				x5 = downSampledPixels[col+1, row+1] if (col+1 < downSampled.size[0] and row+1 < downSampled.size[1]) else 0
				x6 = downSampledPixels[col+1, row-1] if (row-1 >=0 and col+1 < downSampled.size[0]) else 0
				x7 = downSampledPixels[col-1, row-1] if (col-1 >= 0 and row-1 >= 0) else 0
				x8 = downSampledPixels[col-1, row+1] if (row+1 < downSampled.size[1] and col-1 >= 0) else 0
				# get yokoi connectivity number
				res = str(Yokoi.getValue(x0, x1, x2, x3, x4, x5, x6, x7, x8))
				if res == "0":
				    res = " "
				tmpList.append(res)
		yokoiResult.append(tmpList)
	
	# write result to file
	f = open("yokoi_result.txt", "w")
	buf = ""
	for line in yokoiResult:
		buf = buf + ''.join(line) + '\n'
	f.write(buf)
	f.close()

