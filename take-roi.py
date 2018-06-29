# a simple script to apply the same ROI to a directory full of images.
# select the image directoy
# select the roi
# Author: Nick George
# contact: nicholas.m.george@ucdenver.edu
# updated last: 2018-06-29
# using imagej script parameters(https://imagej.net/Script_Parameters) for the gui on this one.
# script params below
#@ File (label="Choose the image directory to crop", style="directory") directory
#@ String (label="What is the file ending of your image files?", choices={".tif",".jpg",".jpeg",".png"}, style="listBox") fileend
#@ File (label="Choose the pre-made ROI file", style="extensions:roi" ) roi
import os
from ij import IJ, ImagePlus
from ij.io import RoiDecoder

def decode_roi(roi_file):
    roi_obj = RoiDecoder(roi_file)
    x = roi_obj.getRoi().getPolygon().getBounds().x
    y = roi_obj.getRoi().getPolygon().getBounds().y
    width = roi_obj.getRoi().getPolygon().getBounds().width
    height = roi_obj.getRoi().getPolygon().getBounds().height
    return x,y,width,height    

def make_dir(folder):
	"""
	make new file directory for extracted tifs
	if folder exists, just return the path.
	"""
	new_dir = os.path.join(folder, "cropped")
	if os.path.exists(new_dir):
		return new_dir
	else:
		os.mkdir(new_dir)
		return new_dir

		
def make_name(str_name, fileend):
	"""Makes the new name for the file. 
	"""
	new_name = str_name.replace(fileend, "") +"_cropped" + fileend
	just_name = os.path.split(new_name)[-1]
	return just_name

##### Begin script #####

# convert from java file obj to string
stDir = str(directory)
roi_f = str(roi)

assert os.path.exists(stDir), "Couldnt find the directory. Try using 'Browse' next time"
assert os.path.exists(roi_f), "Couldnt find the roi file. Try using 'Browse' next time"

# make list of files and filter it for relevant ones. 
selected_files = [f for f in os.listdir(stDir) if f.endswith(fileend)]
full_selected = [os.path.join(stDir, f)  for f in selected_files if not f.startswith(".")]

# this only needs to be done once as we are using the same ROI for each image
X,Y,W,H = decode_roi(roi_f)
# make new folder
new_folder = make_dir(stDir)
print("saving cropped images to: {}".format(new_folder))
for cropme in full_selected:
    print("Processing: {}".format(cropme))
    img = ImagePlus(cropme)
    img.setRoi(X,Y,W,H)
    IJ.run(img, "Crop", "")
    new_name = os.path.join(new_folder,make_name(cropme, fileend))
    IJ.saveAs(img, "Tiff", new_name)

print("Done")