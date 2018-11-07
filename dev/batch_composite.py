# script to make composite images for viewing. 
# script params below
#@ File (label="Choose the image directory to make composite", style="directory") directory
import os
from ij import IJ
from ij.io import FileSaver
from ij.plugin import ChannelSplitter

# For testing:
# set display mode is what you are looking for: https://javadoc.scijava.org/ImageJ1/ij/ImagePlus.html#getDisplayMode--

folder = str(directory)

IJ.log("\n\n >> Welcome to batch composite! <<" )
IJ.log("\n\n >> Please report issues here: \nhttps://github.com/Macklin-Lab/imagej-microscopy-scripts/issues")

def make_dir(workingDir):
	"""
	make new file directory for composite images
	"""
	new_dir = os.path.join(workingDir, "composite")
	if os.path.exists(new_dir):
		return new_dir
	else:
		os.mkdir(new_dir)
		return new_dir


def make_name(str_name):
	"""Makes the new name for the file. 
	"""
	new_name = str_name.replace(".tif", "_composite.tif")
	just_name = os.path.split(new_name)[-1]
	return just_name

assert os.path.exists(folder), "Couldnt find the directory. Try using 'Browse' next time"

new_dir = make_dir(folder)

# filter for your images, get the files with the accepted endings
listoffiles = [ str(f) for f in os.listdir(folder) if f.endswith(".tif")]
# ignore automatically generated hidden files that start with .
real_names = [os.path.join(folder,f) for f in listoffiles if not f.startswith(".")]
message = "\n\n >> Now composit-ing the following files: \n--> "+ "\n --> ".join(real_names) 
IJ.log(message)
for i in real_names:
	img = IJ.openImage(i)
	img.setDisplayMode(1)
	#img.show()
	new_name = os.path.join(new_dir, make_name(i))
	message = "\n > saving " + i + " to: \n " + new_name 
	IJ.log(message)
	IJ.saveAs(img, "Tiff", new_name)

print("DONE")
IJ.log("\n\nDONE!\n\n")


	