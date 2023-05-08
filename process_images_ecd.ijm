/* 
 *  Macro to segement nuclei and measure the intensity. 
 *  Need to input the max/min threshold values for each batch.
 */
 
#@File(label = "Input directory", style = "directory") input
#@File(label = "Output directory", style = "directory") output
#@String(label = "File suffix", value = ".tif") suffix
#@int(label = "Minimum size") minSize
#@String (label = "Image channel", style="list", choices={"cfp", "cy5", "gfp"}) channel
#@String (label = "High or Low?", style="list", choices={"high", "low"}) h_or_l

processFolder(input);
	
// function to scan folders/subfolders/files to find files with correct suffix
function processFolder(input) {
	list = getFileList(input);
	for (i = 0; i < list.length; i++) {
		if(File.isDirectory(input + File.separator + list[i]))
			processFolder("" + input + File.separator + list[i]);
		if(endsWith(list[i], suffix))
			processFile(input, output, list[i]);
	}	 
}


function processFile(input, output, file) {
	setBatchMode(true); // prevents image windows from opening while the script is running
	// open image using Bio-Formats
	run("Bio-Formats", "open=[" + input + "/" + file +"] autoscale color_mode=Default rois_import=[ROI manager] view=Hyperstack stack_order=XYCZT");
	id = getImageID(); // get original image id
	full_name = getTitle();
	no_ext_name = replace(full_name, ".TIF", "");
	run("Duplicate...", " "); // duplicate original image and work on the copy

	// create binary image
	run("Gaussian Blur...", "sigma=2");
	run("Enhance Contrast...", "saturated=0.10");
	
	// Save baseline intensities from the whole image
	// selectImage(id); // activate original image
	run("Select All");
	roiManager("Add");
	roiManager("Measure"); // measure on original image
	roiManager("Deselect");
	saveAs("Results", output + "/" + channel + "_results/" + no_ext_name + "_total_intensity.csv");
	run("Clear Results");
	roiManager("delete");
	
	// run("Threshold...");
	
	if (h_or_l=='high'){
		if(channel =='cfp') {
			setAutoThreshold("Shanbhag dark no-reset");}
		if(channel=='cy5') {
			setAutoThreshold("Default dark no-reset");
			}
		if(channel=='gfp'){
			setAutoThreshold("RenyiEntropy dark no-reset");
			}}
	
	if (h_or_l=='low'){
			setAutoThreshold("MaxEntropy dark no-reset");}
	
	run("Create Mask");
	// save current binary image
	save(output + "/" + channel + "_results/Binary_OUTPUT_" + file);
	
	run("Analyze Particles...", "size=" + minSize + "-Infinity exclude add");
  	selectImage(id); // activate original image
  	roiManager("Show All with labels"); // overlay ROIs
	roiManager("Deselect");
	roiManager("Measure"); // measure on original image
	saveAs("Results", output + "/" + channel + "_results/" + no_ext_name + "_roi_intensity.csv");
	run("Clear Results");
	
	// save ROIs for current image
	roiManager("Deselect");
	roiManager("Save", output + "/" + channel + "_results/" + no_ext_name + "_ROI.zip"); // saves Rois zip file
	roiManager("Deselect");
	roiManager("Delete"); // clear ROI Manager for next image
}

