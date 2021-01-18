from ij import IJ,ImagePlus,ImageStack
import os



def ProcessSlices(folder_in,folder_out,filepath_labels,x_len,y_len):
	"""This function segment strut gross sections in each selected image slice"""
	
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
