# Toolbox for Live Microscopy Flourescent Image Analysis
#### Toolbox of scripts for processing and analyzing fluorescent microscopy time series images.
Scripts in this repository are for a very specific pipeline in the Pearson Laboratory and are not written with
the expectation that they are ready out-of-the box to be used in other applications, however, this code
may certainly be adapted for other use cases. In short, this code has not been tested with outside datasets 
or written with the intent of it becoming a package—it's not that pretty. <br>
### Analysis Pipeline Overview
1. Acquire Images and Process for Analysis
2. Train a Cellpose Model and Extract ROI Masks
3. Process ROI Masks for ImageJ Compatability
4. Extract Intensity from Each Channel
5. Apply Softmax and Generate ROI-level Channel Assignment Probabilities
