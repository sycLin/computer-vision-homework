
import os, sys, math
from PIL import Image


#####################
# utility functions #
#####################

def print_usage():
	print >> sys.stderr, "Usage:\n$python " + __file__ + " <img path>"


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

"""
	This function returns a list pixels,
	which are neighbors of ($x$, $y$) at $pixels$
	@param pixels a pixel access object usually returned by load()
	@param x the x coordinate of the pixel where we want to get neighbors
	@param y the y coordinate of the pixel where we want to get neighbors
	@return a list of length 5 = self + 4 neighbors
"""
def get4Neighbors(pixels, x, y):
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
	return n

"""
	@param src should be an image
	@param connectedType either 4 or 8.
	@return a new image with border pixels in white, interior pixels in grey(128), and background pixels in black.
"""
def getBorderPixels(src, connectedType):
	
	# check connectedType
	if connectedType != 4 and connectedType != 8:
		print >> sys.stderr, "[ERROR] getBorderPixels(): wrong connectedType given:", connectedType
		sys.exit(1)
	
	# the h function of mark interior/border operator
	def h(c, d):
		return c if c == d else 'b'
	
	# the f function of mark interior/border operator
	def f(c):
		return 'b' if c == 'b' else 'i'
	
	pixels = src.load()
	border_pixels = []
	for i in xrange(src.size[0]):
		for j in xrange(src.size[1]):
			if pixels[i, j] == 0: # ignoring black pixels
				continue
			if connectedType == 4:
				n = get4Neighbors(pixels, i, j)
			elif connectedType == 8:
				n = get8Neighbors(pixels, i, j)
			for k in range(len(n)):
				if n[k] == 0:
					border_pixels.append((i, j))
					break
	newImage = Image.new(src.mode, src.size)
	newImagePixels = newImage.load()
	for i in xrange(src.size[0]):
		for j in xrange(src.size[1]):
			if pixels[i, j] == 255:
				newImagePixels[i, j] = 128 # mark foreground as 128 (grey)
			else:
				newImagePixels[i, j] = 0 # background reminas 0 (black)
	for bp in border_pixels:
		newImagePixels[bp[0], bp[1]] = 255 # set border pixel to 255 (white)
	print "There are", len(border_pixels), "pixels being marked."
	return newImage


"""
	@param src should be an image
	@param connectedType either 4 or 8.
	@param borderImage a image returned by getBorderPixels() function.
	@return a new image with marked pixels in white, foregroundpixels in grey(128), and background pixels in black.
"""
def doPairRelationship(src, connectedType, borderImage):

	# check connectedType
	if connectedType != 4 and connectedType != 8:
		print >> sys.stderr, "[ERROR] doPairRelationship(): wrong connectedType given:", connectedType
		sys.exit(1)

	
	srcPixels = src.load()
	borderImagePixels = borderImage.load()

	newImage = Image.new(src.mode, src.size)
	newImagePixels = newImage.load()
	how_many_marked = 0
	for i in xrange(src.size[0]):
		for j in xrange(src.size[1]):
			if borderImagePixels[i, j] != 255:
				# it is not border pixel
				newImagePixels[i, j] = borderImagePixels[i, j]
			else:
				# it is border pixel
				if connectedType == 4:
					n = get4Neighbors(borderImagePixels, i, j)
				else:
					n = get8Neighbors(borderImagePixels, i, j)
				s = 0
				for k in range(1, len(n)):
					if n[k] == 128:
						s += 1
				if s >= 1:
					newImagePixels[i, j] = 255
					how_many_marked += 1
				else:
					newImagePixels[i, j] = 128
	print "There are", how_many_marked, "pixels being marked."
	return newImage


"""
	@param src should be an image
	@param connectedType either 4 or 8.
	@param oList list of pixels marked by << pair relationship operator >>
"""
def doConnectedShrink(src, connectedType, oList):

	# check connectedType
	if connectedType != 4 and connectedType != 8:
		print >> sys.stderr, "[ERROR] doConnectedShrink(): wrong connectedType given:", connectedType
		sys.exit(1)

	# the h function for 4-connected connected shrink
	def h4(b, c, d, e):
		if b == c and (d == b or e == b):
			return 1
		return 0

	# the h function for 8-connected connected shrink
	def h8(b, c, d, e):
		if b != c and (d == b or e == b):
			return 1
		return 0

	def f(a1, a2, a3, a4, x):
		s = a1 + a2 + a3 + a4
		return 'g' if s == 1 else x
	
	pixels = src.load()
	return_list = []
	for i in range(src.size[0]):
		for j in range(src.size[1]):
			if connectedType == 4:
				h = h4
			elif connectedType == 8:
				h = h8
			n = get8Neighbors(pixels, i, j)
			a1 = h(n[0], n[1], n[6], n[2])
			a2 = h(n[0], n[2], n[7], n[3])
			a3 = h(n[0], n[3], n[8], n[4])
			a4 = h(n[0], n[4], n[5], n[1])
			tmp = f(a1, a2, a3, a4, pixels[i, j])
			if tmp == 'g' and (i, j) in oList:
				return_list.append((i, j))
	return return_list
	


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
	binarized = downSample(binarize(orig, 128), (8, 8))
	binarizedPixels = binarized.load()

	# do the thinning
	thinned = binarized.copy()
	thinnedPixels = thinned.load()
	""" testing: start """
	# tmp = getBorderPixels(thinned, 4)
	# tmp.show()
	# tmp = doPairRelationship(thinned, 4, tmp)
	# tmp.show()
	# sys.exit(1)
	""" testing: over """
	while True:
		nothingChanged = True
		#
		# mark interior border pixel
		#
		print "Marking interior border pixels".center(80, '-')
		borderImage = getBorderPixels(thinned, 4)
		#
		# pair relationship operator
		#
		print "Pair Relationship Operator".center(80, '-')
		pairImage = doPairRelationship(thinned, 4, borderImage)
		pairImagePixels = pairImage.load()
		#
		# connected shrink operator
		#
		print "Connected Shrink Operator".center(80, '-')
		connectedType = 4
		# the h function for 4-connected connected shrink
		def h4(b, c, d, e):
			if b == c and (d != b or e != b):
				return 1
			return 0

		# the h function for 8-connected connected shrink
		def h8(b, c, d, e):
			if b != c and (d == b or e == b):
				return 1
			return 0

		def f(a1, a2, a3, a4, x):
			s = a1 + a2 + a3 + a4
			return 'g' if s == 1 else x

		how_many_changed = 0
		for i in range(thinned.size[0]):
			for j in range(thinned.size[1]):
				if connectedType == 4:
					h = h4
				elif connectedType == 8:
					h = h8
				n = get8Neighbors(thinnedPixels, i, j)
				a1 = h(n[0], n[1], n[6], n[2])
				a2 = h(n[0], n[2], n[7], n[3])
				a3 = h(n[0], n[3], n[8], n[4])
				a4 = h(n[0], n[4], n[5], n[1])
				tmp = f(a1, a2, a3, a4, thinnedPixels[i, j])
				if tmp == 'g' and pairImagePixels[i, j] == 255:
					thinnedPixels[i, j] = 0
					how_many_changed += 1
					nothingChanged = False
		print "There are", how_many_changed, "pixels changed in this round."
		if nothingChanged:
			break

	thinned.show()
	thinned.save('thinned_ver2.bmp')












