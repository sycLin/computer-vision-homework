
import os, sys, random
from PIL import Image
from math import log, sqrt

#####################
# class definitions #
#####################

class Kernel:
	def __init__(self, init_list, origin):
		self.pattern = init_list
		self.origin = origin

	"""
		@return a list of directions, i.e., list of 2-tuples
	"""
	def get_directions(self):
		tmp_list = []
		for i in range(len(self.pattern)):
			for j in range(len(self.pattern[0])):
				if self.pattern[i][j] != "x":
					direction = (j - self.origin[0], i - self.origin[1])
					tmp_list.append(direction)
		return tmp_list

####################
# global variables #
####################

octo_kernel_pattern = [
	["x", 0, 0, 0, "x"],
	[0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0],
	["x", 0, 0, 0, "x"]
]


#####################
# utility functions #
#####################

def print_usage():
	print >> sys.stderr, "Usage:\n$python " + __file__ + " <img path>"

"""
	This function does the dilation operation.
	@param src should be an image
	@param kernel should be an instance of Kernel class
	@param threshold should be an integer (default 128 if not given)
	@return a resulted image
"""
def dilation(src, kernel):
	newImage = Image.new(src.mode, src.size)
	newImagePixels = newImage.load()
	for i in range(src.size[0]):
		for j in range(src.size[1]):
			localMax = 0
			for direction in kernel.get_directions():
				new_i = i + direction[0]
				new_j = j + direction[1]
				if new_i >= 0 and new_i < src.size[0] and new_j >= 0 and new_j < src.size[1]:
					localMax = max(localMax, src.getpixel((new_i, new_j)))
			newImagePixels[i, j] = localMax
	return newImage

"""
	This function does the erosion operation.
	@param src should be an image
	@param kernel should be an instance of Kernel class
	@param threshold should be an integer (default 128 if not given)
	@return a resulted image
"""
def erosion(src, kernel):
	newImage = Image.new(src.mode, src.size)
	newImagePixels = newImage.load()
	for i in range(src.size[0]):
		for j in range(src.size[1]):
			set = True
			localMin = 255
			for direction in kernel.get_directions():
				new_i = i + direction[0]
				new_j = j + direction[1]
				if new_i >= 0 and new_i < src.size[0] and new_j >= 0 and new_j < src.size[1]:
					localMin = min(localMin, src.getpixel((new_i, new_j)))
					continue
				else:
					set = False
					break
			if set:
				newImagePixels[i, j] = localMin
	return newImage

"""
	This function does the opening operation.
	@param src should be an image
	@param kernel should be an instance of Kernel class
	@return a resulted image
"""
def opening(src, kernel):
	# simply take advantage of erosion() and dilation()
	return dilation(erosion(src, kernel), kernel)

"""
	This function does the closing operation.
	@param src should be an image
	@param kernel should be an instance of Kernel class
	@return a resulted image
"""
def closing(src, kernel):
	# simply take advantage of dilation() and erosion()
	return erosion(dilation(src, kernel), kernel)


"""
	TODO: ...
	@param src
	@param amplitude
	@return a new image with gaussian noises
"""
def createGaussianNoise(src, amplitude):
	newImage = Image.new(src.mode, src.size)
	newImagePixels = newImage.load()
	srcPixels = src.load()
	# setup the 2 parameters for random.gauss() function.
	gaussian_mu = 0
	gaussian_sigma = 1
	for i in range(newImage.size[0]):
		for j in range(newImage.size[1]):
			value = int(srcPixels[i, j] + amplitude * random.gauss(gaussian_mu, gaussian_sigma))
			newImagePixels[i, j] = max(0, min(255, value))
	return newImage

"""
	TODO: comments here!
"""
def createSaltAndPepperNoise(src, probability):
	newImage = Image.new(src.mode, src.size)
	newImagePixels = newImage.load()
	srcPixels = src.load()
	for i in range(newImage.size[0]):
		for j in range(newImage.size[1]):
			ran = random.uniform(0, 1)
			if ran < probability:
				newImagePixels[i, j] = 0
			elif ran > 1 - probability:
				newImagePixels[i, j] = 255
			else:
				newImagePixels[i, j] = srcPixels[i, j]
	return newImage

"""
	TODO: comments here!
	@param src
	@param boxSize a 2-tuple indicating the size of the box
"""
def boxFiltering(src, boxSize):
	newImage = Image.new(src.mode, src.size)
	newImagePixels = newImage.load()
	srcPixels = src.load()
	# start the main loop
	for i in range(newImage.size[0]):
		for j in range(newImage.size[1]):
			# get the box origin, ex: boxSize[5, 5] will result in boxO[i-2, j-2]
			boxO = [i - (boxSize[0]-1)/2, j - (boxSize[1]-1)/2]
			# get box contents
			boxContents = []
			for m in range(boxSize[0]):
				for n in range(boxSize[1]):
					p = [boxO[0] + m, boxO[1] + n]
					# check if in range
					if p[0] >= 0 and p[0] < newImage.size[0] and p[1] >= 0 and p[1] < newImage.size[1]:
						boxContents.append(srcPixels[p[0], p[1]])
			newImagePixels[i, j] = int(sum(boxContents) / len(boxContents))
	return newImage


"""
	TODO: comments here!
"""
def medianFiltering(src, boxSize):
	newImage = Image.new(src.mode, src.size)
	newImagePixels = newImage.load()
	srcPixels = src.load()
	for i in range(newImage.size[0]):
		for j in range(newImage.size[1]):
			# get the box origin
			boxO = [i - (boxSize[0]-1)/2, j - (boxSize[1]-1)/2]
			# get box content
			boxContents = []
			for m in range(boxSize[0]):
				for n in range(boxSize[1]):
					p = [boxO[0] + m, boxO[1] + n]
					# check if in range
					if p[0] >= 0 and p[0] < newImage.size[0] and p[1] >= 0 and p[1] < newImage.size[1]:
						boxContents.append(srcPixels[p[0], p[1]])
			boxContents.sort()
			if len(boxContents) % 2 == 1: # odd length
				newImagePixels[i, j] = boxContents[len(boxContents)/2]
			else: # even length
				newImagePixels[i, j] = (boxContents[len(boxContents)/2-1] + boxContents[len(boxContents)/2])/2
	return newImage


"""
	TODO: comments here!
"""
def getSNR(src, noisyImage):
	# check size
	if src.size != noisyImage.size:
		print >> sys.stderr, "ERROR: trying to calculate SNR for 2 images with different size"
		print >> sys.stderr, "src image size = ", src.size
		print >> sys.stderr, "noisyImage size = ", noisyImage.size
		sys.exit(1)
	# calculate the mu for the 2 images
	total_pixel_count = src.size[0] * src.size[1]
	srcPixels = src.load()
	noisyImagePixels = noisyImage.load()
	mu1, mu2 = 0.0, 0.0
	for i in xrange(src.size[0]):
		for j in xrange(src.size[1]):
			mu1 += srcPixels[i, j]
			mu2 += noisyImagePixels[i, j] - srcPixels[i, j]
	mu1 = float(mu1) / total_pixel_count
	mu2 = float(mu2) / total_pixel_count
	# calculate the standard deviation for the 2 images
	sigma1, sigma2 = 0.0, 0.0
	for i in xrange(src.size[0]):
		for j in xrange(src.size[1]):
			sigma1 += (srcPixels[i, j] - mu1) * (srcPixels[i, j] - mu1)
			sigma2 += (noisyImagePixels[i, j] - srcPixels[i, j] - mu2) * (noisyImagePixels[i, j] - srcPixels[i, j] - mu2)
	sigma1 = float(sigma1) / total_pixel_count
	sigma2 = float(sigma2) / total_pixel_count
	return 20 * log(sqrt(sigma1)/sqrt(sigma2), 10)


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
	"""
	create noise:
	1) Gaussian noise: 10
	2) Gaussian noise: 30
	3) salt-and-pepper noise: 0.1
	4) salt-and-pepper noise: 0.05
	And for each of the above, use:
	1) box filter: 3x3
	2) box filter: 5x5
	3) median filter: 3x3
	4) median filter: 5x5
	5) opening-then-closing: 3-5-5-5-3
	6) closing-then-opening: 3-5-5-5-3
	"""

	g10 = createGaussianNoise(orig, 10)
	g30 = createGaussianNoise(orig, 30)

	snp10 = createSaltAndPepperNoise(orig, 0.1)
	snp5 = createSaltAndPepperNoise(orig, 0.05)

	# save the results

	g10.save('g10.bmp')
	g30.save('g30.bmp')
	snp10.save('snp10.bmp')
	snp5.save('snp5.bmp')

	buf = "" # for writing to resulted SNR file
	buf += "Gaussian 10: " + str(getSNR(orig, g10)) + "\n"
	buf += "Gaussian 30: " + str(getSNR(orig, g30)) + "\n"
	buf += "Salt-and-Pepper 0.1: " + str(getSNR(orig, snp10)) + "\n"
	buf += "Salt-and-Pepper 0.05: " + str(getSNR(orig, snp5)) + "\n"

	# box filtering 3x3
	g10_box_3x3 = boxFiltering(g10, (3, 3))
	g30_box_3x3 = boxFiltering(g30, (3, 3))
	snp10_box_3x3 = boxFiltering(snp10, (3, 3))
	snp5_box_3x3 = boxFiltering(snp5, (3, 3))

	g10_box_3x3.save('g10_box_3x3.bmp')
	g30_box_3x3.save('g30_box_3x3.bmp')
	snp10_box_3x3.save('snp10_box_3x3.bmp')
	snp5_box_3x3.save('snp5_box_3x3.bmp')

	buf += "G10 box 3x3: " + str(getSNR(orig, g10_box_3x3)) + "\n"
	buf += "G30 box 3x3: " + str(getSNR(orig, g30_box_3x3)) + "\n"
	buf += "Snp10 box 3x3: " + str(getSNR(orig, snp10_box_3x3)) + "\n"
	buf += "Snp5 box 3x3: " + str(getSNR(orig, snp5_box_3x3)) + "\n"

	# box filtering 5x5
	g10_box_5x5 = boxFiltering(g10, (5, 5))
	g30_box_5x5 = boxFiltering(g30, (5, 5))
	snp10_box_5x5 = boxFiltering(snp10, (5, 5))
	snp5_box_5x5 = boxFiltering(snp5, (5, 5))

	g10_box_5x5.save('g10_box_5x5.bmp')
	g30_box_5x5.save('g30_box_5x5.bmp')
	snp10_box_5x5.save('snp10_box_5x5.bmp')
	snp5_box_5x5.save('snp5_box_5x5.bmp')

	buf += "G10 box 5x5: " + str(getSNR(orig, g10_box_5x5)) + "\n"
	buf += "G30 box 5x5: " + str(getSNR(orig, g30_box_5x5)) + "\n"
	buf += "Snp10 box 5x5: " + str(getSNR(orig, snp10_box_5x5)) + "\n"
	buf += "Snp5 box 5x5: " + str(getSNR(orig, snp5_box_5x5)) + "\n"

	# median filtering 3x3
	g10_median_3x3 = medianFiltering(g10, (3, 3))
	g30_median_3x3 = medianFiltering(g30, (3, 3))
	snp10_median_3x3 = medianFiltering(snp10, (3, 3))
	snp5_median_3x3 = medianFiltering(snp5, (3, 3))

	g10_median_3x3.save('g10_median_3x3.bmp')
	g30_median_3x3.save('g30_median_3x3.bmp')
	snp10_median_3x3.save('snp10_median_3x3.bmp')
	snp5_median_3x3.save('snp5_median_3x3.bmp')

	buf += "G10 median 3x3: " + str(getSNR(orig, g10_median_3x3)) + "\n"
	buf += "G30 median 3x3: " + str(getSNR(orig, g30_median_3x3)) + "\n"
	buf += "Snp10 median 3x3: " + str(getSNR(orig, snp10_median_3x3)) + "\n"
	buf += "Snp5 median 3x3: " + str(getSNR(orig, snp5_median_3x3)) + "\n"

	# median filtering 5x5
	g10_median_5x5 = medianFiltering(g10, (5, 5))
	g30_median_5x5 = medianFiltering(g30, (5, 5))
	snp10_median_5x5 = medianFiltering(snp10, (5, 5))
	snp5_median_5x5 = medianFiltering(snp5, (5, 5))

	g10_median_5x5.save('g10_median_5x5.bmp')
	g30_median_5x5.save('g30_median_5x5.bmp')
	snp10_median_5x5.save('snp10_median_5x5.bmp')
	snp5_median_5x5.save('snp5_median_5x5.bmp')

	buf += "G10 median 5x5: " + str(getSNR(orig, g10_median_5x5)) + "\n"
	buf += "G30 median 5x5: " + str(getSNR(orig, g30_median_5x5)) + "\n"
	buf += "Snp10 median 5x5: " + str(getSNR(orig, snp10_median_5x5)) + "\n"
	buf += "Snp5 median 5x5: " + str(getSNR(orig, snp5_median_5x5)) + "\n"

	# opening-then-closing
	octoKernel = Kernel(octo_kernel_pattern, (2, 2))
	g10_open_then_close = closing(opening(g10, octoKernel), octoKernel)
	g30_open_then_close = closing(opening(g30, octoKernel), octoKernel)
	snp10_open_then_close = closing(opening(snp10, octoKernel), octoKernel)
	snp5_open_then_close = closing(opening(snp5, octoKernel), octoKernel)

	g10_open_then_close.save('g10_open_then_close.bmp')
	g30_open_then_close.save('g30_open_then_close.bmp')
	snp10_open_then_close.save('snp10_open_then_close.bmp')
	snp5_open_then_close.save('snp5_open_then_close.bmp')

	buf += "G10 opening-then-closing: " + str(getSNR(orig, g10_open_then_close)) + "\n"
	buf += "G30 opening-then-closing: " + str(getSNR(orig, g30_open_then_close)) + "\n"
	buf += "Snp10 opening-then-closing: " + str(getSNR(orig, snp10_open_then_close)) + "\n"
	buf += "Snp5 opening-then-closing: " + str(getSNR(orig, snp5_open_then_close)) + "\n"

	# closing-then-opening
	g10_close_then_open = opening(closing(g10, octoKernel), octoKernel)
	g30_close_then_open = opening(closing(g30, octoKernel), octoKernel)
	snp10_close_then_open = opening(closing(snp10, octoKernel), octoKernel)
	snp5_close_then_open = opening(closing(snp5, octoKernel), octoKernel)

	g10_close_then_open.save('g10_close_then_open.bmp')
	g30_close_then_open.save('g30_close_then_open.bmp')
	snp10_close_then_open.save('snp10_close_then_open.bmp')
	snp5_close_then_open.save('snp5_close_then_open.bmp')

	buf += "G10 closing-then-opening: " + str(getSNR(orig, g10_close_then_open)) + "\n"
	buf += "G30 closing-then-opening: " + str(getSNR(orig, g30_close_then_open)) + "\n"
	buf += "Snp10 closing-then-opening: " + str(getSNR(orig, snp10_close_then_open)) + "\n"
	buf += "Snp5 closing-then-opening: " + str(getSNR(orig, snp5_close_then_open)) + "\n"

	f = open("SNR_result.txt", "w")
	f.write(buf)
	f.close()


	pass





