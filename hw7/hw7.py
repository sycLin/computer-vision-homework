
import os, sys
from PIL import Image

#####################
# utility functions #
#####################

def print_usage():
	print >> sys.stderr, "Usage:\n$python hw7.py <img path>"

"""
	This function sets pixels to 0 if they're less than $threshold$ in $src$.
	@param src should be an image
	@param threshold should be an integer (default 128 if not given)
	@return a binarized image instance
"""
def binarize(src, threshold=128):
	srcPixels = src.load() # for speed-up, getpixel((i, j)) is too slow
	newImage = Image.new(src.mode, src.size)
	newImagePixels = newImage.load()
	for i in range(src.size[0]):
		for j in range(src.size[1]):
			old = srcPixels[i, j]
			if old < 128:
				newImagePixels[i, j] = 0
			else:
				newImagePixels[i, j] = 255
	return newImage

"""
	This function returns a list pixels,
	which are neighbors of ($x$, $y$) at $pixels$
	@param pixels a pixel access object usually returned by load()
	@param x the x coordinate of the pixel where we want to get neighbors
	@param y the y coordinate of the pixel where we want to get neighbors
	@return a list of length 9 = self + 8 neighbors
"""
def get8Neighbors(pixels, x, y):
	n = []
	try:
		tmp = pixels[x, y] # x0
		n.append(tmp)
	except:
		n.append(0)
	try:
		tmp = pixels[x+1, y] # x1
		n.append(tmp)
	except:
		n.append(0)
	try:
		tmp = pixels[x, y-1] # x2
		n.append(tmp)
	except:
		n.append(0)
	try:
		tmp = pixels[x-1, y] # x3
		n.append(tmp)
	except:
		n.append(0)
	try:
		tmp = pixels[x, y+1] # x4
		n.append(tmp)
	except:
		n.append(0)
	try:
		tmp = pixels[x+1, y+1] # x5
		n.append(tmp)
	except:
		n.append(0)
	try:
		tmp = pixels[x+1, y-1] # x6
		n.append(tmp)
	except:
		n.append(0)
	try:
		tmp = pixels[x-1, y-1] # x7
		n.append(tmp)
	except:
		n.append(0)
	try:
		tmp = pixels[x-1, y+1] # x8
		n.append(tmp)
	except:
		n.append(0)
	return n

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
		print >> sys.stderr, "fatal: cannot open image at:" + sys.argv[1]
		sys.exit(1)

	# binarize the image
	binarized = binarize(orig, 128)
	binarizedPixels = binarized.load()
	binarized.save('binarized.bmp')

	# main while loop for thinning
	thinned = binarized.copy()
	thinnedPixels = thinned.load()
	while True:
		nothingChanged = True # a boolean to record if there's any change made
		# part A - check if need deleting
		tmp_list = []
		for i in range(thinned.size[0]):
			for j in range(thinned.size[1]):
				if thinnedPixels[i, j] == 0: # we are not interested in this pixel
					continue
				N8 = get8Neighbors(thinnedPixels, i, j)
				# 1) sum of N8[1] to N8[8] is between 2 to 6
				s = sum(N8[1:len(N8)])
				# 2) clockwise go-through from top, if 1->0 counter++, counter == 1?
				counter = 0
				clockwiseList = [N8[2], N8[6], N8[1], N8[5], N8[4], N8[8], N8[3], N8[7], N8[2]]
				for k in range(len(clockwiseList)-1):
					if clockwiseList[k] == 255 and clockwiseList[k+1] == 0:
						counter += 1
				# 3) N8[2] * N8[1] * N8[4] == 0?
				checkPoint3 = True if N8[2] * N8[1] * N8[4] == 0 else False
				# 4) N8[1] * N8[4] * N8[3] == 0?
				checkPoint4 = True if N8[1] * N8[4] * N8[3] == 0 else False
				# check all the conditions above
				if s >= 2*255 and s <= 6 * 255 and counter == 1 and checkPoint3 and checkPoint4:
					tmp_list.append((i, j))
					nothingChanged = False
		# part A - delete them
		# print >> sys.stderr, "delete these:"
		# print >> sys.stderr, tmp_list
		for p in tmp_list:
			thinnedPixels[p[0], p[1]] = 0 # set to black
		# part B - check if need deleting
		tmp_list = []
		for i in range(thinned.size[0]):
			for j in range(thinned.size[1]):
				if thinnedPixels[i, j] == 0: # we are not interested in this pixel
					continue
				N8 = get8Neighbors(thinnedPixels, i, j)
				# 1) sum of N8[1] to N8[8] is between 2 to 6
				s = sum(N8[1:len(N8)])
				# 2) clockwise go-through from top, if 1->0 counter++, counter == 1?
				counter = 0
				clockwiseList = [N8[2], N8[6], N8[1], N8[5], N8[4], N8[8], N8[3], N8[7], N8[2]]
				for k in range(len(clockwiseList)-1):
					if clockwiseList[k] == 255 and clockwiseList[k+1] == 0:
						counter += 1
				# 3) N8[3] * N8[2] * N8[1] == 0?
				checkPoint3 = True if N8[3] * N8[2] * N8[1] == 0 else False
				# 4) N8[4] * N8[3] * N8[2] == 0?
				checkPoint4 = True if N8[4] * N8[3] * N8[2] == 0 else False
				# check all the conditions above
				if s >= 2*255 and s <= 6*255 and counter == 1 and checkPoint3 and checkPoint4:
					tmp_list.append((i, j))
					nothingChanged = False
		# part B - delete them
		# print >> sys.stderr, "delete these:"
		# print >> sys.stderr, tmp_list
		for p in tmp_list:
			thinnedPixels[p[0], p[1]] = 0 # set to black
		if nothingChanged:
			break

	# save the thinned image
	thinned.show()
	thinned.save('thinned.bmp')



