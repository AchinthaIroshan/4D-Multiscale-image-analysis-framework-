"""@author: Achintha I. Kondarage@Project: Sintering of Bioactive glassesSet of functions to segment VOIs in imagesopen with fiji"""from ij.plugin import FolderOpener
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




def segVOI_image_series(folder_in,folder_out,filepath_labels,x_len,y_len):    """    Segment VOIs of a 3D image where whole 3D image series and slices which contain VOIs are given    """
	
	file_names,rows = getLabels(filepath_labels)
	for i in range(len(file_names)):
		imp = IJ.openImage(os.path.join(folder_in, file_names[i]))
		print(os.path.join(folder_in, file_names[i]))
		stack = imp.getImageStack()
		stack2 = ImageStack(imp.width,imp.height)
		blankim = IJ.createImage("blank", "8-bit black", imp.width, imp.height, 1)
		ipb= blankim.getProcessor()	
		for j in range(imp.getNSlices()):
			if rows[j][i]== '0':
				ip = stack.getProcessor(j+1)
				#NormalizeLocalContrast.run(ip, 341, 326, 4, True, True)
				imagep = ImagePlus("imp",ip)
				IJ.run(imagep, "Non-local Means Denoising", "sigma=10 smoothing_factor=1 slice")
				imagep.setRoi(1,1,x_len,y_len);
				IJ.run(imagep, "Level Sets", "method=[Active Contours] use_level_sets grey_value_threshold=50 distance_threshold=0.50 advection=2.20 propagation=1 curvature=1 grayscale=30 convergence=0.03 region=inside")
				fimp = IJ.getImage()
				#fip  = fimp.getProcessor()
				fimp = removeSmallCCs(fimp)
				fip  = fimp.getProcessor()
				stack2.addSlice(fip)
				print("process")
		
			else:
				#ip = stack.getProcessor(j+1)
				stack2.addSlice(ipb)
		
		final_imp = ImagePlus("image",stack2)
		output = "nrrd=["+folder_out+file_names[i]+"]"
		IJ.run(final_imp, "Nrrd ... ", output)
		IJ.run(imp, "Close All", "");



def preprocess_slices_giv_im(image_num,file_inpath,file_outpath):
    """    Segment VOIs of a 3D image  slices which contain VOIs are given    """
	imp = IJ.openImage(file_inpath)
	file_names,rows = getLabels()
	
	stack = imp.getImageStack()
	stack2 = ImageStack(imp.width,imp.height)
	 
	for j in range(imp.getNSlices()):
		if rows[j][image_num]== '0':
			ip = stack.getProcessor(j+1)
			NormalizeLocalContrast.run(ip, 341, 326, 4, True, True)
			imagep = ImagePlus("imp",ip)
			IJ.run(imagep, "Non-local Means Denoising", "sigma=15 smoothing_factor=1 slice")
			imagep.setRoi(2,2,302,282);
			IJ.run(imagep, "Level Sets", "method=[Active Contours] use_level_sets grey_value_threshold=50 distance_threshold=0.50 advection=2.20 propagation=1 curvature=1 grayscale=30 convergence=0.0025 region=inside")
			fimp = IJ.getImage()
			#fip  = fimp.getProcessor()
			fimp = removeSmallCCs(fimp)
			fip  = fimp.getProcessor()
			stack2.addSlice(fip)
			print("process")
		
		else:
			ip = stack.getProcessor(j+1)
			stack2.addSlice(ip)


	final_imp = ImagePlus("image",stack2)
	output = "nrrd=["+file_outpath+"]"
	IJ.run(final_imp, "Nrrd ... ", output)



