# Toolbox for Live Microscopy Flourescent Image Analysis
#### Toolbox of scripts for processing and analyzing fluorescent microscopy time series images.
Scripts in this repository are for a very specific pipeline in the Pearson Laboratory and are not written with
the expectation that they are ready out-of-the box to be used in other applications, however, this code
may certainly be adapted for other use cases. In short, this code has not been tested with outside datasets 
or written with the intent of it becoming a package—it's not that pretty. <br>
### Analysis Pipeline Overview
1. **Acquire Images and Process for Analysis**
     * **[convert_tif.py](https://github.com/emmachancellor/fluorescent_image_analysis/blob/main/convert_tif.py)**: Fluorescence images captured as .TIF images must be converted into .png and scaled to 512x512 pixels for Cellpose to properly segment the cells. This script completes these two steps and saves the new 512x512 .png image.  
3. **Train a Cellpose Model and Extract ROI Masks**
     * For instructions on how to segment images using Cellpose, see [Training and Fine-Tuning a Cellpose Model](#cellpose)
5. **Process ROI Masks for ImageJ Compatability**
     * **[ecd_roi_converter.py](https://github.com/emmachancellor/fluorescent_image_analysis/blob/main/ecd_roi_converter.py)**: This script performs two processing steps. First, the .txt ROIs saved from 512x512 .png images in Cellpose will be scaled to the original .TIF file size so that they can be overlayed on the original images. Second, the newly scaled .txt ROIs will be saved as a .zip file that can be opened natively in ImageJ. 
6. **Extract Intensity from Each Channel**
7. **Apply Softmax and Generate ROI-level Channel Assignment Probabilities**
---
### Training and Fine-Tuning a Cellpose Model <a name="cellpose"></a>
All Cellpose documentation can be found in the original repository: https://github.com/mouseland/cellpose <br>
#### Downloading and Running Cellpose on Your Computer
Start by creating a new condo environment and downloading cellpose <br>
`conda create —n cellpose python=3.8`<br>
`pip install cellpose`<br><br>
To open the GUI, run: `python -m cellpose`<br>
If the GUI dependencies are not present, you will need to download those as well by running `pip install cellpose[gui]`<br><br>
**NOTE**: When using zsh and want to install dependencies with square brackets, you need to escape the brackets by putting the package name in quotations like this:
`pip install 'cellpose[gui]'`
#### Fine Tuning Models in Cellpose
1. Calibrate the cell diameter
2. Try out models from the model zoo to find the one that works the best. For the live cell images, ‘CP’ has tended to work the best.
3. Once you find a decent model, begin fine tuning by hand by drawing annotations. There are instructions for how to draw new ROIs in the ‘Help’ tab on the application bar at the top of the screen.
4. In the top menubar for the application (top of a Mac) go to ‘Models’ and select  ‘Train new model with image+mask in folder’ (you can also press `Cmd+T` to run this)
5. Re-do step 3, annotating the next image in the folder. Then run the same `Cmd+T`. Continue this until the model performs as you would like (usually between 2-5 fine tuned images).
6. To extract masks with your newly fine-tuned model you can either use the command line (shown below) or the API in python. In the command line, make sure you put the complete path of the image folder after `--dir`  and the full name of the fine tuned model after `--pretrained_model` 
7. Other notes `--save_outlines` saves the ROIs in a .txt file and `--verbose` displays the model’s progress while running<br><br>
Here is an example of the command line interface code that will run a pre-trained model over all images in a given directory and save the ROIs as .txt files:
```
python -m cellpose --dir <your/directory/of/images> --pretrained_model <model_name> --diameter <diameter_as_integer> --save_txt --verbose
```
