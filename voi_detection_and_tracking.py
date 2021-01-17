from ij.plugin import FolderOpener
from ij import IJ,ImagePlus,ImageStack
import os
from script.imglib import ImgLib
from script.imglib.algorithm import Resample
from ij.io import FileSaver 

"""Preprocessing of VOI detection"""





def rescale(folder_in,folder_out):
	"""Function to rescale 3D NRRD image series"""
	for filename in os.listdir(folder_in):
		imp =IJ.openImage(os.path.join(folder_in,filename))
		img = ImgLib.wrap(imp)
		img2 = Resample(img,0.25)
		imp=ImgLib.wrap(img2)
		output = "nrrd=["+folder_out+filename+"]"
		IJ.run(imp, "Nrrd ... ", output)
		imp=None
		img=None
		img2=None
		gc.collect()
		time.sleep(15)
		gc.collect()
		IJ.run("Collect Garbage", "")
		IJ.run("Collect Garbage", "")



def rescaleimp(file_inpath,file_outpath):
	"""Function to rescale a  single 3D NRRD image """

	imp = IJ.openImage(file_inpath)
	img = ImgLib.wrap(imp)
	img2 = Resample(img,0.25)
	imp = ImgLib.wrap(img2)
	output = "nrrd=["+file_outpath+"]"
	IJ.run(imp, "Nrrd ... ", output)


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
