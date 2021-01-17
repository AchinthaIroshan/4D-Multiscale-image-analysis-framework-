"""
@author: Achintha I. Kondarage
@Project: Sintering of Bioactive glasses

Functions that can be useful in analysing 3D images

"""


def invertImage(imp):
	"""Invert a binary image"""
	stack = imp.getImageStack()
	stack2 = ImageStack(imp.width,imp.height)
	#image.show()
	for i in xrange(imp.getNSlices()):
	
		ip = stack.getProcessor(i+1).convertToFloat()
		pixels = ip.getPixels()
		for j in xrange(len(pixels)):
			if pixels[j]== 255:
				pixels[j]=0
			else:
				pixels[j]=255
		stack2.addSlice(ip)
	impstk = ImagePlus("rods_inv", stack2)
	IJ.run(impstk, "8-bit", "") 
	return impstk

def stackToSlices(folder_in,folder_out,folder_num):
	"""Convert a 3D nrrd image to a tiff series"""
	for x in range(14): 
		fnum = folder_num+x
		print(fnum)
		filename = str(fnum)+".nrrd"
		imp = IJ.openImage(os.path.join(folder_in, filename))
		print(os.path.join(folder_in, filename))
		stack = imp.getImageStack()
		output=folder_out+str(fnum)
		os.makedirs(output)
		for i in xrange(1, imp.getNSlices()+1):
			ip = stack.getProcessor(i)
			imp = ImagePlus("imp", ip)
			IJ.run(imp, "8-bit", "") 
			fs= FileSaver(imp)
			filepath = os.path.join(output,str(i)+".tif")
			fs.saveAsTiff(filepath)		
