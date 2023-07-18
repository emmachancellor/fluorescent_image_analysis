/* 
 *  Macro to segement nuclei and measure the intensity. 
 *  Need to input the max/min threshold values for each batch.
 */
 
#@File(label = "Input image directory", style = "directory") image_dir
#@File(label = "Input roi directory", style = "directory") roi_dir
#@File(label = "Output directory", style = "directory") output
#@String(label = "File suffix", value = ".tif") suffix
#@int(label = "Minimum size") minSize

processImages(image_dir, roi_dir);

// function to scan folders/subfolders/files to find files with correct suffix
function processImages(image_dir, roi_dir) {
	image_list = getFileList(image_dir);
    roi_list = getFileList(roi_dir);
	for (i = 0; i < image_list.length; i++) {
		if(endsWith(image_list[i], suffix))
			processFile(image_dir, roi_dir, output, image_list[i], roi_list[i]);
	}	 
}

function processImages(image_dir, roi_dir, image, roi) {
	setBatchMode(true); // prevents image windows from opening while the script is running
	// open image using Bio-Formats
	run("Bio-Formats", "open=[" + image_dir + "/" + image +"] autoscale color_mode=Default rois_import=[ROI manager] view=Hyperstack stack_order=XYCZT");
    id = getImageID(); // get original image id
	full_name = getTitle();
	no_ext_name = replace(full_name, ".TIF", "");
	run("Duplicate...", " "); // duplicate original image and work on the copy


	// Save baseline intensities from the whole image
	// selectImage(id); // activate original image
	run("Select All");
	roiManager("Add");
	roiManager("Measure"); // measure on original image
	roiManager("Deselect");
	saveAs("Results", output + "/results/" + no_ext_name + "_total_intensity.csv");
	run("Clear Results");
	roiManager("delete");

    // Open Cellpose Masks
    open(roi_dir + "/" + roi);
    selectImage(id); // activate original image
  	roiManager("Show All with labels"); // overlay ROIs
	roiManager("Deselect");
	roiManager("Measure"); // measure on original image
	saveAs("Results", output + "/results/" + no_ext_name + "_roi_intensity.csv");
	run("Clear Results");
	roiManager("Delete"); // clear ROI Manager for next image
}