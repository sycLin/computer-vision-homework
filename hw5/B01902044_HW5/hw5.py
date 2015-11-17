
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
	print >> sys.stderr, "Usage:\n$python hw5.py <image path>"



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


	# dilation
	octoKernel = Kernel(octo_kernel_pattern, (2, 2))
	dilationImage = dilation(orig, octoKernel)
	dilationImage.show()
	dilationImage.save("Dilation.bmp")

	# erosion
	erosionImage = erosion(orig, octoKernel)
	erosionImage.show()
	erosionImage.save("Erosion.bmp")

	# opening
	openingImage = opening(orig, octoKernel)
	openingImage.show()
	openingImage.save("Opening.bmp")

	# closing
	closingImage = closing(orig, octoKernel)
	closingImage.show()
	closingImage.save("Closing.bmp")

