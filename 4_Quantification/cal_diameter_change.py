#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 13:45:35 2019

@author: aik19
"""


from pathlib import Path
import nrrd
from skimage import measure
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import os
from scipy.spatial import distance
#import Image

firstfolder = 74122
folder = "/media/aik19/Seagate Backup Plus Drive/ICIE16_Analysis_V2/Stage1/rm_smallCC/"
outfolder1 = "/media/aik19/Seagate Backup Plus Drive/ICIE16_Analysis_V2/Stage1/centers_macro/"
outfolder2 = "/media/aik19/Seagate Backup Plus Drive/ICIE16_Analysis_V2/Stage1/centers_micro/"
outfolder3 = "/media/aik19/Seagate Backup Plus Drive/ICIE16_Analysis_V2/Stage1/labeled struts/"



#vf_folder_1 = "/media/aik19/Seagate Backup Plus Drive/Sintering_ICIE16_printed_Vf/Cropped_hyperstack/"
#vf_folder_2 = "/media/aik19/Seagate Backup Plus Drive/Sintering_ICIE16_printed_Vf/labeledMA/"
#vf_folder_3 = "/media/aik19/Seagate Backup Plus Drive/Sintering_ICIE16_printed_Vf/CsvMA1"
#vf_folder_4 = "/media/aik19/Seagate Backup Plus Drive/Sintering_ICIE16_printed_Vf/CsvMA2"

wvf_folder_1 = "G:/Sintering_ICIE16_printed_Vf/Strut_segmentation/all/"  
wvf_folder_2 = "G:/Sintering_ICIE16_printed_Vf/Centers_resampled/"
wvf_folder_3 = "G:/Sintering_ICIE16_printed_Vf/Centers/"
wvf_folder_4 = "G:/Sintering_ICIE16_printed_Vf/Labelled_sliced_struts/"

wvf_folder_5 = "E:/ICIE16/DiameterChange/"
wvf_folder_6 = "D:/Sintering analysis/Sinteiring-of-Bioactive-glasses/Mean_diamters/"

input_folder1 = "C:/Sintering Analysis/Segmented Struts/Object11/"
input_folder2 = "C:/Sintering Analysis/Diameter_struts/"



def calDimaterChange(folder_in,folder_out):
    for i in range(11,15):
        dimater_csvs = folder_in+"Diameter_object"+str(i)+"_v2.csv"
        df = pd.read_csv(dimater_csvs)
        df2 = df.groupby('Image').mean()
        print(df2)
        outfile = folder_out + "Diameter_object"+str(i)+".csv"
        df2.to_csv(outfile)

#calDimaterChange(wvf_folder_5,wvf_folder_6)



def concatNcalDiameter(folder_in):
    
    df_list = []
    for i in range(11,15):
       dimater_csvs = folder_in+"Diameter_object"+str(i)+".csv"
       df = pd.read_csv(dimater_csvs)
       df_list.append(df)
    dimater_values = pd.concat(df_list)
    print(dimater_values)
    dimater_final_values =  dimater_values.groupby('Image').mean()
    print(dimater_final_values)
    dimater_final_values.to_csv("D:/Sintering analysis/Sinteiring-of-Bioactive-glasses/dimater_final_values.csv")
#concatNcalDiameter(wvf_folder_6)    

def plotDiamterChange():
    df = pd.read_csv("C:/Users/achin/Documents/phd/sintering_workspace/Sinteiring-of-Bioactive-glasses/diamater_final_values.csv")
    Time = df['Time'].tolist()
    Diameter = df['Diameter micro'].tolist()
    Temperature = df['Temperature'].tolist()
    
    dim = pd.Series(Diameter) 
    rolling = dim.rolling(window=3)
    rolling_mean = rolling.mean()
    print(rolling_mean)
    fig, ax1 = plt.subplots()
    
    color = 'tab:green'
    ax1.set_xlabel('time (Mins)')
    ax1.set_ylabel('Diameter (Micro meters)', color=color)
    ax1.plot(Time, Diameter, color=color)
    ax1.plot(Time, rolling_mean, color='tab:red')
    ax1.tick_params(axis='y', labelcolor=color)
    
    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    
    color = 'tab:blue'
    ax2.set_ylabel('Temperature(C)', color=color)  # we already handled the x-label with ax1
    ax2.plot(Time, Temperature, color=color)
    ax2.tick_params(axis='y', labelcolor=color)
    
    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.show()
    fig.savefig('DiamterChange.png')
#plotDiamterChange()
def center_data_arrangement():

    for i in range(1,2):
        print("processing object",i)
       # object_list =[]
        for folder in range(74122,74125):
            if folder == 74218:
                continue
            csvfilepath="C:/Users/achin/Documents/phd/sintering_workspace/Sinteiring-of-Bioactive-glasses/Centers/"+str(folder)+".nrrd.csv"
            df = pd.read_csv(csvfilepath) 
            object_cordinates = df.T[i-1:i]  
            a = object_cordinates.loc['object1']
            print(a[0])
            #r,c = object_cordinates.shape
            #if r == 0:
            #    continue
            #objectname = 'object'+str(folder)
            #object_cordinates.rename(index={object_cordinates.index[0]:folder}, inplace=True)
            #object_list.append(object_cordinates)
        
            
           # print(csvfilepath)
            
            
        #df1 = pd.read_csv("G:/Sintering_ICIE16_printed_Vf/Centers/74122.nrrd.csv") 
        #df2 = pd.read_csv("G:/Sintering_ICIE16_printed_Vf/Centers/74123.nrrd.csv")
        #df1t = df1.T
        #df2t = df2.T 
        #object1 = [df1t[0:1],df2t[0:1]]
        #df_object_list = pd.concat(object_list)
        #df_object_list.to_csv("G:/Sintering_ICIE16_printed_Vf/center_cordinates_micro/object"+str(i)+".csv")
        #print(df_object_list)


   # print(type(df2.iloc[0]))
   # print(df2.iloc[0])

#center_data_arrangement()


def allignCenters():
    #csvfilepath="C:/Users/achin/Documents/phd/sintering_workspace/Sinteiring-of-Bioactive-glasses/Centers/74122.nrrd.csv"
    #df = pd.read_csv(csvfilepath)
    
    for j in range(1,37):
        csvfilepath="C:/Users/achin/Documents/phd/sintering_workspace/Sinteiring-of-Bioactive-glasses/Centers/74122.nrrd.csv"
        df = pd.read_csv(csvfilepath)
        newobject1 = []
        scan74122 = df.T[j-1:j]
        x_1,y_1,z_1 = scan74122.loc['object'+str(j)]
        p1 = (x_1,y_1,z_1)
        
        scan74122.rename(index={scan74122.index[0]:'74122'}, inplace=True)
        newobject1.append(scan74122)
    
        #print(newobject1)
        
        for folder in range(74123,74235):
            if folder == 74218:
                continue 
            min_d=1000000000
            for i in range(1,37):
                csvfilepath="C:/Users/achin/Documents/phd/sintering_workspace/Sinteiring-of-Bioactive-glasses/Centers/"+str(folder)+".nrrd.csv"
                df = pd.read_csv(csvfilepath) 
                object_cordinates = df.T[i-1:i]
                x_2,y_2,z_2 = object_cordinates.loc['object'+str(i)]
                p2=(x_2,y_2,z_2)
                d = distance.euclidean(p1, p2)
                if(d < min_d):
                    min_d = d
                    next_cordinates= object_cordinates.copy()
                    p_next = (x_2,y_2,z_2)
                    #print(d)
            next_cordinates.rename(index={next_cordinates.index[0]:folder}, inplace=True)
            next_cordinate_copy = next_cordinates.copy()
            newobject1.append(next_cordinate_copy)
                #print(object_cordinates)
            p1 = p_next   
        newobject1 = pd.concat(newobject1)
        newobject1.to_csv("C:/Users/achin/Documents/phd/sintering_workspace/Sinteiring-of-Bioactive-glasses/Alligened_centers/newObject"+str(j)+".csv")
        print(newobject1)        
    
#allignCenters()
def centerFinder(firstfolder,folder,outfolder1,outfolder2,outfolder3):

    cfobjects1 = {}
    cfobjects2 = {} 
    centers_df1 = {}
    centers_df2 = {}
    
    for i in range(5):
        folder_num = firstfolder + i 
        image,header = nrrd.read(Path(folder+str(folder_num)+".nrrd"))

        labelledImage = measure.label(image,background=0)
        
        nrrd.write(outfolder3+str(folder_num)+".nrrd",np.float32(labelledImage) )
        objectmes = measure.regionprops(labelledImage)
        for j in range(len(objectmes)):
            objectlabel = objectmes[j].label
            obejectName = "object"+str(objectlabel)
            lst = objectmes[j].centroid
            lst1 =[round(x) for x in lst]
            lst2 =[round(x*4) for x in lst]
            cfobjects1.update({obejectName:lst1})
            cfobjects2.update({obejectName:lst2})
        df1 = pd.DataFrame(cfobjects1,index=['x','y','z'])
        df2 = pd.DataFrame(cfobjects2,index=['x','y','z'])
        centers_df1[folder_num]=df1
        centers_df2[folder_num]=df2
        df1.to_csv(outfolder1+str(folder_num)+".csv", index=False)
        df2.to_csv(outfolder2+str(folder_num)+".csv", index=False)
        
    for key in centers_df1.keys():
        print("\n" +"="*40)
        print(key)
        print("-"*40)
        print(centers_df1[key])



def centerFinderMA(folder_in,folder_out1,folder_out2,folder_out3):
    cfobjects1 = {}
    cfobjects2 = {} 
    #centers_df1 = {}
    #centers_df2 = {}
    #i=0
    for filename in os.listdir(folder_in):
        print(filename)
        filepath_in = os.path.join(folder_in,filename)
        image,header = nrrd.read(filepath_in)
        labelledImage = measure.label(image,background=0)
        filepath_out1 = os.path.join(folder_out1,filename)
        nrrd.write(filepath_out1,np.float32(labelledImage))
        objectmes = measure.regionprops(labelledImage)
        print(len(objectmes))
        for j in range(len(objectmes)):
            objectlabel = objectmes[j].label
            obejectName = "object"+str(objectlabel)
            lst = objectmes[j].centroid
            lst1 =[round(x) for x in lst]
            lst2 =[round(x*4) for x in lst]
            cfobjects1.update({obejectName:lst1})
            cfobjects2.update({obejectName:lst2})
        
        df1 = pd.DataFrame(cfobjects1,index=['x','y','z'])
        df2 = pd.DataFrame(cfobjects2,index=['x','y','z'])
        filepath_out2 = os.path.join(folder_out2,filename)
        filepath_out3 = os.path.join(folder_out3,filename)
        df1.to_csv(filepath_out2+".csv", index=False)
        df2.to_csv(filepath_out3+".csv", index=False)
        
    

#centerFinderMA(wvf_folder_1,wvf_folder_2,wvf_folder_3,wvf_folder_4)


#centerFinder(firstfolder,folder,outfolder1,outfolder2,outfolder3)
def f(x, y):
    return np.sin(np.sqrt(x ** 2 + y ** 2))

def plot3D():
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    x = np.array([1,1,5,5,1,1,5,5,1,1,5,5])
    y = np.array([1,5,5,1,1,5,5,1,1,5,5,1])
    z = np.array([1,1,1,1,3,3,3,3,5,5,5,5])
    X, Y = np.meshgrid(x, y)
    Y, Z = np.meshgrid(y, z)

    ax.plot_wireframe(X, Y, Z, color='black')
    ax.set_title('wireframe')
    
#plot3D()



def plotCenters():
    
    data = pd.read_csv("/media/aik19/Seagate Backup Plus Drive/ICIE16_Analysis_V2/Stage1/centers_micro/74122.csv") 
    
    Row_list =[]
    
    for index, rows in data.iterrows(): 
        my_list =[rows.object1,
                  #rows.object2,
                  rows.object3,
                  #rows.object4,
                  #rows.object5,
                  #rows.object6,
                  rows.object7, 
                  #rows.object8, 
                  rows.object9, 
                  #rows.object10, 
                  #rows.object11, 
                  #rows.object12,
                  #rows.object13, 
                  #rows.object14, 
                  #rows.object15, 
                  #rows.object16, 
                  #rows.object17, 
                  #rows.object18,
                  #rows.object19, 
                  #rows.object20, 
                  #rows.object21, 
                  rows.object22, 
                  #rows.object23, 
                  rows.object24,
                  rows.object25,
                  #rows.object26,
                  rows.object27
                  ] 
        Row_list.append(my_list) 
         
    x = np.array(Row_list[0])
    y = np.array(Row_list[1])
    z = np.array(Row_list[2])
    
    X,Y = np.meshgrid(x, y)
    Y, Z = np.meshgrid(y, z)
    
    box= []
    
    for index, rows in data.iterrows(): 
        my_list =[rows.object1,
                  rows.object3,
                  rows.object7,  
                  rows.object9,  
                  rows.object22, 
                  rows.object24,
                  rows.object25,
                  rows.object27,
                  rows.object1,
                  rows.object3,
                  ] 
        box.append(my_list) 
    
    
    x_1 = np.array(box[0])
    y_1 = np.array(box[1])
    z_1 = np.array(box[2])
    
    X_1,Y_1 = np.meshgrid(x_1, y_1)
    Y_1, Z_1 = np.meshgrid(y_1, z_1)
    
    
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    #ax.scatter(X, Y, Z, color='black')
    
    ax.plot_wireframe(X_1, Y_1, Z_1, color='black')
    ax.set_xlabel('$X$')
    ax.set_ylabel('$Y$')
    ax.set_zlabel('$Z$')


#plotCenters()

#plot3D()
        
    
    

