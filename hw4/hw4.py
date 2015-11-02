
import os
import sys
from PIL import Image

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
				if self.pattern[i][j] == 1:
					direction = (j - self.origin[0], i - self.origin[1])
					tmp_list.append(direction)
		return tmp_list

####################
# global variables #
####################

octo_kernel_pattern = [
	[0, 1, 1, 1, 0],
	[1, 1, 1, 1, 1],
	[1, 1, 1, 1, 1],
	[1, 1, 1, 1, 1],
	[0, 1, 1, 1, 0]
]

L_shape_kernel_pattern = [
	[1, 1],
	[0, 1]
]

#####################
# utility functions #
#####################

def print_usage():
	print >> sys.stderr, "Usage:\n$python hw4.py <image path>"

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
	This function sets pixels to 255 if they're less than $threshold$ in $src$.
	@param src should be an image
	@param threshold should be an integer (default 128 if not given)
	@return an image instance
"""
def complement(src, threshold=128):
	newImage = Image.new(src.mode, src.size)
	newImagePixels = newImage.load()
	for i in range(src.size[0]):
		for j in range(src.size[1]):
			old = src.getpixel((i, j))
			if old < threshold:
				newImagePixels[i, j] = 255
			else:
				newImagePixels[i, j] = 0
	return newImage


"""
	This function finds the intersection of two images.
	@param src1 should be an image
	@param src2 should be an image
	@param threshold should be an integer (default 128 if not given)
	@return a resulted image
"""
def intersection(src1, src2, threshold=128):
	newImage = Image.new(src1.mode, src1.size)
	newImagePixels = newImage.load()
	for i in range(src1.size[0]):
		for j in range(src1.size[1]):
			old1 = src1.getpixel((i, j))
			old2 = src2.getpixel((i, j))
			if old1 > threshold and old2 > threshold:
				newImagePixels[i, j] = 255
			else:
				newImagePixels[i, j] = 0
	return newImage

"""
	This function finds the union of two images.
	@param src1 should be an image
	@param src2 should be an image
	@param threshold should be an integer (default 128 if not given)
	@return a resulted image
"""
def union(src1, src2, threshold=128):
	newImage = Image.new(src1.mode, src1.size)
	newImagePixels = newImage.load()
	for i in range(src1.size[0]):
		for j in range(src1.size[1]):
			old1 = src1.getpixel((i, j))
			old2 = src2.getpixel((i, j))
			if old1 > threshold or old2 > threshold:
				newImagePixels[i, j] = 255
			else:
				newImagePixels[i, j] = 0
	return newImage

"""
	This function does the dilation operation.
	@param src should be an image
	@param kernel should be an instance of Kernel class
	@param threshold should be an integer (default 128 if not given)
	@return a resulted image
"""
def dilation(src, kernel, threshold=128):
	newImage = Image.new(src.mode, src.size)
	newImagePixels = newImage.load()
	for i in range(src.size[0]):
		for j in range(src.size[1]):
			old = src.getpixel((i, j))
			if old < threshold: # we're not interested in this pixel
				continue
			for direction in kernel.get_directions():
				new_i = i + direction[0]
				new_j = j + direction[1]
				if new_i >= 0 and new_i < src.size[0] and new_j >= 0 and new_j < src.size[1]:
					# in range! set it to 255!
					newImagePixels[new_i, new_j] = 255
	return newImage

"""
	This function does the erosion operation.
	@param src should be an image
	@param kernel should be an instance of Kernel class
	@param threshold should be an integer (default 128 if not given)
	@return a resulted image
"""
def erosion(src, kernel, threshold=128):
	newImage = Image.new(src.mode, src.size)
	newImagePixels = newImage.load()
	for i in range(src.size[0]):
		for j in range(src.size[1]):
			old = src.getpixel((i, j))
			set = True
			for direction in kernel.get_directions():
				new_i = i + direction[0]
				new_j = j + direction[1]
				if new_i >= 0 and new_i < src.size[0] and new_j >= 0 and new_j < src.size[1] and src.getpixel((new_i, new_j)) > threshold:
					continue
				else:
					set = False
					break
			if set:
				newImagePixels[i, j] = 255
			else:
				newImagePixels[i, j] = 0
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
	This function does the hit-and-miss operation.
	@param src should be an image
	@param kernelJ should be an instance of Kernel class
	@param kernelK should be an instance of Kernel class
	@return a resulted image
"""
def hit_and_miss(src, kernelJ, kernelK):
	return intersection(erosion(src, kernelJ), erosion(complement(src), kernelK))


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
		print >> sys.stderr, "fatal: wrong image path given..."
		sys.exit(1)

	# binarize the image
	binarized = binarize(orig, 128)

	# dilation
	octoKernel = Kernel(octo_kernel_pattern, (2, 2))
	dilationImage = dilation(binarized, octoKernel)
	dilationImage.show()
	dilationImage.save("Dilation.bmp")

	# erosion
	erosionImage = erosion(binarized, octoKernel)
	erosionImage.show()
	erosionImage.save("Erosion.bmp")

	# opening
	openingImage = opening(binarized, octoKernel)
	openingImage.show()
	openingImage.save("Opening.bmp")

	# closing
	closingImage = closing(binarized, octoKernel)
	closingImage.show()
	closingImage.save("Closing.bmp")

	# hit-and-miss
	kernelJ = Kernel(L_shape_kernel_pattern, (1, 0))
	kernelK = Kernel(L_shape_kernel_pattern, (0, 1))
	hitAndMissImage = hit_and_miss(binarized, kernelJ, kernelK)
	hitAndMissImage.show()
	hitAndMissImage.save("Hit-and-Miss.bmp")












