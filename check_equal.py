import sys, os
from PIL import Image

def print_usage():
	pass

def eq(im1, im2):
	if im1.size[0] != im2.size[0] or im1.size[1] != im2.size[1]:
		return False
	im1Pixels = im1.load()
	im2Pixels = im2.load()
	for i in xrange(im1.size[0]):
		for j in xrange(im1.size[1]):
			if im1Pixels[i, j] != im2Pixels[i, j]:
				return False
	return True

if __name__ == "__main__":
	if len(sys.argv) != 3:
		print_usage()
	try:
		im1 = Image.open(sys.argv[1])
		im2 = Image.open(sys.argv[2])
	except:
		print >> sys.stderr, "fatal: wrong image paths given"
		sys.exit(1)
	print eq(im1, im2)