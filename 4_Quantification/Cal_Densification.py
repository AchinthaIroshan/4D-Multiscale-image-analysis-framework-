from ij import IJ,ImagePlus,ImageStack
from ij.io import FileSaver
import os
from trainableSegmentation import WekaSegmentation
from ij.measure import ResultsTable 
from ij.plugin import FolderOpener



folder_in_object11 = "C:/Sintering Analysis/ICIE16 micro/Densification/Child_Volumes_for_density/object11/" 
folder_out1_object11 = "C:/Sintering Analysis/ICIE16 micro/Densification/preprocessed_child_volumes/"
folder_out2_object11 = "C:/Sintering Analysis/ICIE16 micro/Densification/child_volumes_5/"
folder_out3_object11 = "C:/Sintering Analysis/ICIE16 micro/Densification/Child_Volumes_denoised_Stage3/"
folder_out_binary_object11 = "C:/Sintering Analysis/ICIE16 micro/Densification/Segmented_binary/"
folder_out_object11 = "C:/Sintering Analysis/ICIE16 micro/Densification/Object11_analysis/Segmented_8bit/"
folder_out_object11_st3 = "C:/Sintering Analysis/ICIE16 micro/Densification/Child_volumes_segmented_stage3/"

stage3_ph1_ca = "C:/Sintering Analysis/ICIE16 micro/Densification/Object11_analysis/object11_ca/stage/ph1/"
stage3_ph1_raw = "C:/Sintering Analysis/ICIE16 micro/Densification/Object11_analysis/Object11_original/Stage3/ph1/"

diameter_volumes = "C:/Sintering Analysis/ICIE16 micro/Densification/Diameter_volumes/object11/Stage3/ph2/"
segmented_otsu = "C:/Sintering Analysis/ICIE16 micro/Densification/Object11_analysis/Segmented_otsu/stage3/ph2/"


def threshold(folder_in,folder_out):
	for i in range(74164,74214):
		print(i)
		imp = IJ.openImage(folder_in+str(i)+".nrrd")	
		IJ.run(imp, "Non-local Means Denoising", "sigma=10 smoothing_factor=1 stack")
		IJ.run(imp, "Auto Threshold", "method=Otsu white stack use_stack_histogram")
		imp.setRoi(90,85,150,140);
		IJ.run(imp, "Crop", "");
		fs = FileSaver(imp) 
		filepath = folder_out+str(i)+".tif"
		print(filepath)
		fs.saveAsTiff(filepath)


#threshold(diameter_volumes,segmented_otsu)

def ca(folder_in,folder_out):
	
	imp = FolderOpener.open(folder_in)
	IJ.run(imp, "Stack Contrast Adjustment", "is")
	imp2 = IJ.getImage()
	stack = imp2.getImageStack()
	
	for i in range(imp.getNSlices()):
		for im in range(74154,74164):
			new_stack = ImageStack(imp.width,imp.height)
			for j in xrange(1,71):
				ip = stack.getProcessor(i+1)
				new_stack.addSlice(ip)
			imp3 = ImagePlus("image",new_stack)	
			#fs = FileSaver(imp3) 
			#filepath = folder_out+str(im)+".tif"
			#print(filepath)
			#fs.saveAsTiff(filepath)		
			print(imp3.getNSlices())

			

	#imp = ImagePlus("stack",stack)
	#imp.show()

#ca(stage3_ph1_raw,stage3_ph1_ca)




def preprocessing(folder_in,folder_out):
	for filename in os.listdir(folder_in):
		print(os.path.join(folder_in,filename))
		imp =IJ.openImage(os.path.join(folder_in,filename))
		IJ.run(imp, "Non-local Means Denoising", "sigma=10 smoothing_factor=1 stack")
		IJ.run(imp, "Enhance Contrast", "saturated=0.35")
		IJ.run(imp, "Apply LUT", "stack")
		output = "nrrd=["+folder_out+filename+"]"
		IJ.run(imp, "Nrrd ... ", output)


def preprocessing2(folder_in,folder_out):
	for i in range(74143,74150):
		print(i)
		imp = IJ.openImage(folder_in+str(i)+".nrrd")
		IJ.run(imp, "Non-local Means Denoising", "sigma=5 smoothing_factor=1 stack")
		IJ.run(imp, "Enhance Contrast", "saturated=0.35")
		IJ.run(imp, "Apply LUT", "stack")
		fs = FileSaver(imp) 
		filepath = folder_out+str(i)+".tif"
		print(filepath)
		fs.saveAsTiff(filepath)

def preprocessing3(folder_in,folder_out):
	for i in range(74150,74214):
		print(i)
		imp = IJ.openImage(folder_in+str(i)+".nrrd")
		IJ.run(imp, "Non-local Means Denoising", "sigma=10 smoothing_factor=1 stack")
		fs = FileSaver(imp) 
		filepath = folder_out+str(i)+".tif"
		print(filepath)
		fs.saveAsTiff(filepath)
	
#preprocessing3(folder_in_object11,folder_out3_object11)
	


def segmentation(folder_in,folder_out):
	segmentator =  WekaSegmentation()
	segmentator.loadClassifier("C:/Sintering Analysis/Sinteiring-of-Bioactive-glasses/Training_Images/random_forrest_segmentation_new.model")

	for i in range(74143,74144):
		testImage = IJ.openImage("C:/Sintering Analysis/ICIE16 micro/Densification/preprocessed_child_volumes/"+str(i)+".nrrd")
		result = segmentator.applyClassifier( testImage )
		#result.show()
		fs= FileSaver(result)
		filepath = folder_out+str(i)+".tif"
		fs.saveAsTiff(filepath)



#segmentation(folder_out1_object11,folder_out_binary_object11)


def convertToGray8bit(folder_in,folder_out):

	for im in range(74143,74144):
		image = IJ.openImage(folder_in+str(im)+".tif")
		stack = image.getImageStack()
		stack2 = ImageStack(image.width,image.height)
	
		for i in xrange(1, image.getNSlices()+1):
			ip = stack.getProcessor(i).convertToFloat()
			pixels = ip.getPixels()
			for i in xrange(len(pixels)):
				if pixels[i] == 1:
					pixels[i] = 255
			stack2.addSlice(ip)
		final_imp = ImagePlus("image",stack2)
		#final_imp.show()
		IJ.run(final_imp, "8-bit", "") 
		fs = FileSaver(final_imp) 
		filepath = folder_out+str(im)+".tif"
		print(filepath)
		fs.saveAsTiff(filepath)



def theresholdstacks(folder_in,outfolder):
	for im in range(74153,74214):
		imp = IJ.openImage(folder_in+str(im)+".tif")
		stack = imp.getImageStack()
		stack2 = ImageStack(imp.width,imp.height)
		for i in xrange(1, imp.getNSlices()+1):
			ip = stack.getProcessor(i) 
			ip.threshold(152)
			stack2.addSlice(ip)		
		imp2 = ImagePlus("Test", stack2)
		fs= FileSaver(imp2)	
		fs.saveAsTiff(outfolder+ "/" + str(im) + ".tif")

def calcporosity(folder):
	table = ResultsTable()
	for i in range(74153,74164):
		filename = str(i)+".tif"
		print "processing",filename
		imp =IJ.openImage(os.path.join(folder,filename))
		ip = imp.getProcessor().convertToFloat()
		pixels = ip.getPixels()
		pores = 0
		glass = 0 	
	
		for pix in pixels:  
			if pix == 0:  
				pores = pores + 1
			else:
				glass = glass + 1
		porosity = (float(pores)/(pores+glass))*100
		table.incrementCounter()
		table.addValue("Image",i) 
		table.addValue("void",pores)
		table.addValue("glass",glass)
		table.addValue("Porosity",porosity)
	table.show("Porosity")

calcporosity(segmented_otsu)

#theresholdstacks(folder_out3_object11,folder_out_object11_st3)
#convertToGray8bit(folder_out_binary_object11,folder_out_object11)