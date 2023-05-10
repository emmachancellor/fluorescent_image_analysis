import numpy as np
import matplotlib.pyplot as plt
import os
from cellpose import models, utils, io
from cellpose.io import imread

# Load pre-trained model
model = models.CellposeModel(model_type='SIY_high_t1_bladder_cancer')

# Path to files
folder_path = "/Volumes/ECD/microscopy_v2/images/high_T_2_DIC_png_512"

imgs=[]
files=[]
for f in os.listdir(folder_path):
    if f[:7] == "SIY_Sam":
        files.append(f)
        img = imread(folder_path+'/'+f)
        imgs.append(img)

# Define channels (grayscale in this case)
channels = [[0,0]]

# Run model on images
masks, flows, styles, diams = model.eval(imgs, diameter=18.5, channels=channels)
io.save_to_png(imgs, masks, flows, files)
io.masks_flows_to_seg(imgs, masks, flows, diams, files, channels)


base = os.path.split(full_file_path)[0]
outlines=utils.outlines_list(masks)
io.outlines_to_text(base, outlines)