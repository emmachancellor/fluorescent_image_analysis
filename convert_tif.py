import pandas as pd
import numpy as np
import PIL
from PIL import Image
import os
'''
This code is designed to convert .TIF files to .png files as well as
reduce the file size of the images to 512x512 pixels.

The user will need to specify the path to the folder containing the .TIF files (files), 
the parent folder of the folder containing the .TIF files (folder_path),
as well as the path to a new folder where the .png files will be saved (new_folder_path).
'''

new_folder_path = '/home/ecdyer/labshare/LL07132018/New_tumor_T_coculture_data/SIY_hi_t_spot2/png_512_bright/'
folder_path = '/home/ecdyer/labshare/LL07132018/New_tumor_T_coculture_data/SIY_hi_t_spot2/high_t_spot2_bright/'
files = os.listdir('/home/ecdyer/labshare/LL07132018/New_tumor_T_coculture_data/SIY_hi_t_spot2/high_t_spot2_bright')
total = len(files)
file_names = []
scale_factors = []

for i, f in enumerate(files):
    if '.TIF' in f:
        print(f'({i}/{total})  Converting image {f} to .png')
        name = folder_path + f
        im = np.array(Image.open(name))
        im = Image.fromarray(im / np.amax(im) * 255)
        im = im.convert("L")

        # Calculate the maximum size that the image can be scaled 
        # to while preserving its aspect ratio
        max_width = 512
        max_height = 512
        width, height = im.size
        scale_factor = min(max_width / width, max_height / height)
        new_size = (int(width * scale_factor), int(height * scale_factor))

        # Resize the image to the calculated size
        im = im.resize(new_size, Image.LANCZOS)

        # Rename file
        file_name = str(f).rstrip(".TIF")
        #im.save(name + '.jpg', 'JPEG')
        new_name = new_folder_path + file_name
        print(new_name)
        im.save(new_name + '.png', 'PNG')



