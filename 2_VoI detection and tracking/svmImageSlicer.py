"""
@author: Achintha I. Kondarage
@Project: Sintering of Bioactive glasses

Set of functions to classify image slices which include VOIs

"""

from pathlib import Path
import pandas as pd
import numpy as np
from sklearn import svm, metrics
from sklearn.utils import Bunch
from sklearn.model_selection import GridSearchCV, train_test_split
from skimage.io import imread
from skimage.transform import resize
#import pickle
from joblib import dump,load
#import matplotlib.pyplot as plt
import nrrd
import os


def load_image_files(container_path, dimension=(64, 64)):
    """
    Load image files with categories as subfolder names 
    which performs like scikit-learn sample dataset
    
    """
    image_dir = Path(container_path)
    folders = [directory for directory in image_dir.iterdir() if directory.is_dir()]
    categories = [fo.name for fo in folders]

    descr = "A image classification dataset"
    images = []
    flat_data = []
    target = []
    for i, direc in enumerate(folders):
        for file in direc.iterdir():
            img = imread(file)
            img_resized = resize(img, dimension, anti_aliasing=True, mode='reflect')
            flat_data.append(img_resized.flatten()) 
            images.append(img_resized)
            target.append(i)
    flat_data = np.array(flat_data)
    target = np.array(target)
    images = np.array(images)
    print('done')
    return Bunch(data=flat_data,
                 target=target,
                 target_names=categories,
                 images=images,
                 DESCR=descr)



def trainSVM():

    """
    train a support vector classifier to classify images based on reduced voxel values.
    
    """
    image_dataset = load_image_files("Images/")
    X_train, X_test, y_train, y_test = train_test_split(
    image_dataset.data, image_dataset.target, test_size=0.3,random_state=109)
    param_grid = [
      {'C': [1, 10, 100, 1000], 'kernel': ['linear']},
      {'C': [1, 10, 100, 1000], 'gamma': [0.001, 0.0001], 'kernel': ['rbf']},
     ]
    svc = svm.SVC()
    clf = GridSearchCV(svc, param_grid)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    print("Classification report for - \n{}:\n{}\n".format(
        clf, metrics.classification_report(y_test, y_pred)))
    dump(clf, 'classifier_svm_slice_sc.joblib')
    

def strutslicer(image_read_path,image_write_path):

 
    """
    Classify slices in a 3D image : slices with VOIs and slices without VOIS
    Replace slices without VOI with a black coloured image slice.
  
    """
    
    data,header = nrrd.read(Path(image_read_path))
    image = data.T
    features = []
    clf = load('classifier_svm_slice_sc.joblib') 
    for slices in image:
         img_resized = resize(slices, (64,64), anti_aliasing=True, mode='reflect')   
         features.append(img_resized.flatten())
    labels = clf.predict(features)
    print(image_read_path)
    print(labels)   

    
    z,y,x = image.shape
    
    black = np.zeros((y,x))
    #plt.imshow(black)
    #plt.imshow(image[0])
    
    for i in range(z):
        if labels[i] == 1:
            image[i] = black
    
    saveIm = image.T
    
    nrrd.write(image_write_path,saveIm )


def strutslice_selector(image_read_path):

    """
    Classify slices in a 3D image

    """

    data,header = nrrd.read(Path(image_read_path))
    image = data.T
    features = []
    clf = load('classifier_svm_slice_sc.joblib') 
    for slices in image:
         img_resized = resize(slices, (64,64), anti_aliasing=True, mode='reflect')   
         features.append(img_resized.flatten())
    labels = clf.predict(features)
    print(clf.decision_function(features))
    #print(labels)
    return labels
    
#trainSVM()  
def run_strut_slicer():


    """
    Execution of fuctions to remove image slices without VOIs based on a support vector machine classifier.

    """

    trainSVM()
    #folder_in = "/media/aik19/Seagate Backup Plus Drive/Sintering_ICIE16_printed_Vf/Resampled/Stage3/ph2/"
    folder_in = "C:/PhD/Sintering Analysis/Anlaysing Shrinkage/segmented_nrrd/"
    #folder_out = "/media/aik19/Seagate Backup Plus Drive/Sintering_ICIE16_printed_Vf/strutSlicer/Stage3/ph2/" 
    folder_out = "C:/PhD/Sintering Analysis/Anlaysing Shrinkage/sliced_struts/"
    slicelabels={}
    for filename in os.listdir(folder_in):
        imagepath = os.path.join(folder_in, filename)
        image_write_path = os.path.join(folder_out, filename)
        labels = strutslice_selector(imagepath)
        slicelabels.update({filename : labels})
        strutslicer(imagepath,image_write_path)
    df = pd.DataFrame(data=slicelabels)
    df.to_csv("sliceLabels_ICIE16_Macro.csv", index=False)

run_strut_slicer()
