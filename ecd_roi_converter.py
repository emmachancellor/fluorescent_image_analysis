''' 
This script is designed to convert the ROI points from a .txt file to a list of lists
that contains the ROI points for each ROI in the image. This conversion facilitates
the creation of an ROI archive file, which can be opened natively in ImageJ. 

'''

import os
from roifile import ImagejRoi, roiwrite

all_files = os.listdir('/Volumes/ECD/microscopy_v2/images/high_T_1_DIC_png_512')
folder_path = '/Volumes/ECD/microscopy_v2/images/high_T_1_DIC_png_512'

for file in all_files:
    if '.txt' in file and '._' not in file:
        file_path = folder_path + '/' + file
        with open(file_path, "r", encoding='latin-1') as textfile:
            print(textfile)
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
            file = folder_path + file[:-4] + '_rois.zip'
            roiwrite(file, rois)