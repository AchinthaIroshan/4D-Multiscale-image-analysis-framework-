"""
@author: Achintha I. Kondarage
@Project: Sintering of Bioactive glasses

A set of function to pre-process the 3D images captured in-situ during the sintering of bioactive glass

"""

from ij.plugin import FolderOpener
from ij import IJ,ImagePlus,ImageStack
import os
from script.imglib import ImgLib
from script.imglib.algorithm import Resample
from ij.io import FileSaver 
import csv
from mpicbg.ij.plugin import NormalizeLocalContrast  
from ij.plugin.filter import ParticleAnalyzer as PA
from ij.measure import ResultsTable
import time
import gc
from ij.plugin.frame import RoiManager
from ij.gui import Roi

#All reconstructed of 3D images are saved as a set of 2D tiff files(32 bit)

#Converting the dataset to 8bit to reduce the computation cost


def covertTo8bitsBatch(folder_in,folder_out):
	"""Function to convert 3D images in a set of folders into 8bits"""
	for folder in os.listdir(folder_in):
		infolderpath = folder_in+folder
		outfolderpath = folder_out + folder 
		os.mkdir(outfolderpath)
		for filename in os.listdir(infolderpath):
			imp = IJ.openImage(os.path.join(infolderpath, filename))
			IJ.run(imp, "8-bit", "") 
			fs = FileSaver(imp) 
			filepath = os.path.join(outfolderpath, filename)
			fs.saveAsTiff(filepath)
			
def covertTo8bits(folder_in,folder_out):
	"""Function to convert 3D image stored in tiff series to a 8bit nrrd"""
	for filename in os.listdir(folder_in):  
		imp = IJ.openImage(os.path.join(folder_in, filename))
		IJ.run(imp, "8-bit", "") 
		output = "nrrd=["+folder_out+filename+"]"
		IJ.run(imp, "Nrrd ... ", output)

def rmVoidCropNpreprocess(folder_in,folder_out,firstFolder,r):
	"""Function to remove voids outside the scaffold(a cropping operation), Adding meta data, stack contrast adjust ment 
	Reducing computational cost is one of the main purpose of this fucntion. The function is written in a way that a set of images run at a time
	to manage computation time. Here tiff series of a 3D image is converted to a single NRRD file"""
	
	for x in range(r):
		fnum = firstFolder+x
		print(fnum)
		folder = folder_in+str(fnum)+"/"
		output = "nrrd=["+folder_out+str(fnum)+".nrrd]"
		imp = FolderOpener.open(folder)

		IJ.run(imp, "Properties...", "channels=1 slices=2159 frames=1 unit=[micro meters] pixel_width=0.81 pixel_height=0.81 voxel_depth=0.81")
		stack = imp.getImageStack()
		stackcropped  = stack.crop(404,644,480,1604,1476,1678)
		imp = ImagePlus("1",stackcropped)
		IJ.run(imp, "Stack Contrast Adjustment", "is")
		imp = IJ.getImage()
		IJ.run(imp, "Nrrd ... ", output);
		imp.close()
		imp = None
		stack = None
		stackcropped = None
		gc.collect()
		
		time.sleep(15)
		gc.collect()
		IJ.run("Collect Garbage", "")

def rotationNcropping(folder_in,folder_out):
	""" Function to rotate a set of 3D images such a a way the struts of the scaffold 
	the scaffols are alligned with x and y directions """
	
	for filename in os.listdir(folder_in):
		imp =IJ.openImage(os.path.join(folder_in,filename))		
		IJ.run(imp, "TransformJ Rotate", "z-angle=9 y-angle=-6 x-angle=0.0 interpolation=Linear background=0.0")
		imp = IJ.getImage()
		stack = imp.getImageStack()
		stackcropped  = stack.crop(130,64,77,1356,1296,1540)
		imp = ImagePlus("2",stackcropped)
		output = "nrrd=["+folder_out+filename+"]"
		IJ.run(imp, "Nrrd ... ", output)
		imp.close()
		imp = None
		stack = None
		stackcropped = None
		gc.collect()
		time.sleep(15)
		gc.collect()
		IJ.run("Collect Garbage", "")
		IJ.run("Collect Garbage", "")
		IJ.getImage().close()

def rotationNcroppingSimage(folder_in,folder_out,firstfilenum):	
	""" Function to rotate a 3D image such a a way the struts of the scaffold 
	the scaffols are alligned with x and y directions """
	for i in range(3):
		filenumber = firstfilenum + i
		filename = str(filenumber)+".nrrd"
		imp =IJ.openImage(os.path.join(folder_in,filename))
		IJ.run(imp, "TransformJ Rotate", "z-angle=9 y-angle=-6 x-angle=0.0 interpolation=Linear background=0.0")
		imp = IJ.getImage()
		stack = imp.getImageStack()
		stackcropped  = stack.crop(130,64,77,1356,1296,1540)
		imp = ImagePlus("2",stackcropped)
		output = "nrrd=["+folder_out+filename+"]"
		IJ.run(imp, "Nrrd ... ", output)
		imp.close()
		imp = None
		stack = None
		stackcropped = None
		gc.collect()
		time.sleep(15)
		gc.collect()
		IJ.run("Collect Garbage", "")
		IJ.run("Collect Garbage", "")
		IJ.getImage().close()

def includemeta(folder_in,folder_out):
	""" Function to insert meta data an NRRD image"""
	for filename in os.listdir(folder_in):
		imp =IJ.openImage(os.path.join(folder_in,filename))
		IJ.run(imp, "Properties...", "channels=1 slices=904 frames=1 unit=[micro meters] pixel_width=0.8100000 pixel_height=0.8100000 voxel_depth=0.8100000");
		output = "nrrd=["+folder_out+filename+"]"
		IJ.run(imp, "Nrrd ... ", output)


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








