''' 
Author: Emma Dyer
Date: 18 July 2023

This script is used to convert the .txt ROI files produced by Cellpose into
.zip files that can be opened natively in ImageJ.

This script performs two processing steps:
1. Scales the .txt ROI files produced on the 512x512 .png 
    images in Cellpose to match the scale of the original .TIF image files
2. Saves .txt ROIs as .zip files that can be opened natively in ImageJ

When running this script, the user will need to input the path to the folder
that contains the .txt ROIs produced by Cellpose. 

New .zip file ROIs will be saved in the same folder. 
'''

import os
from roifile import ImagejRoi, roiwrite
import numpy as np
import pandas as pd
from tqdm import tqdm

folder_path = input("Enter path to folder containing .txt ROI files: ")
all_files = os.listdir(folder_path)
#folder_path = '/Volumes/ECD/microscopy_v2/images/high_T_1_DIC_png_512'

def multiply_list(l:str):
    '''
    Helper function that takes a string of numbers separated by a 
    comma and converts this into a numpy array that is then
    multiplied by 2.635. 
    
    Args:
        l (str): string of that contains numbers separated by commas.
        Example: "31,32,44,71"
    
    Returns:
        string_again (str): string of the input numbers that have
        been multiplied by 2.635.
    '''
    arr=np.array(list(map(int,l.split(','))))
    arr_multiplied = arr.astype(float) * 2.635
    arr_multiplied = [int(round(x)) for x in arr_multiplied]
    string_again = ','.join(map(str, arr_multiplied))
    return string_again

for file in tqdm(all_files, desc='Converting ROI files'):
    if '.txt' in file and '._' not in file:   
        file_path = folder_path + '/' + file
        rois = pd.read_csv(file_path, delimiter='\t', header=None)
        scaled_roi = rois.iloc[:, 0].map(multiply_list)
        scaled_file_path = folder_path + '/' + 'scaled_' + file
        scaled_roi.to_csv(scaled_file_path, sep='\t', index=False, header=False)
        with open(scaled_file_path, "r", encoding='latin-1') as textfile:
            all_rois=[]
            for line in textfile:
                xy = list(map(float, line.rstrip().split(",")))  # Use float instead of int for decimal numbers
                X = xy[::2]
                Y = xy[1::2]
                
                # Save the ROI points as a list of lists
                roi_points = [[x, y] for x, y in zip(X, Y)]
                roi_points = np.array(roi_points)
                all_rois.append(roi_points)

# Save the ROI points as an ROI archive file
            rois = [ImagejRoi.frompoints(rois) for rois in all_rois]
            roi_folder = folder_path + '/imagej_rois/'
            if not os.path.exists(roi_folder):
                os.makedirs(roi_folder)
            file = folder_path + '/imagej_rois/' + file[:-4] + '_rois.zip'
            if 'scaled' in file:
                roiwrite(file, rois)