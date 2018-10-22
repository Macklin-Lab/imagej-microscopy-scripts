#tif-convert.py
# Author: Nick George
# Contact: nicholas.m.george@ucdenver.edu
# updated last: 2018-10-22
# using imagej script parameters(https://imagej.net/Script_Parameters) for the gui on this one.
# script params below
#@ File (label="Choose the image directory to convert to tif.", style="directory") directory

from ij import IJ, WindowManager, ImagePlus
from ij.io import FileSaver
from loci.plugins import BF
from loci.plugins.in import ImporterOptions
from loci.formats import ImageReader
import os

## this is a list of files I have tested it with and it seems to work with.
## let me know if you want others included,
accepted_files = (".czi", ".lsm", ".lif", ".oib", ".nd2")
IJ.log("\n\n >> Welcome to tif-convert! <<" )
IJ.log("\n >> Please report issues here: \nhttps://github.com/Macklin-Lab/imagej-microscopy-scripts/issues\n\n")

# open directoy
folder = str(directory)

# functions to make stuff easier

def make_dir(workingDir):
	"""
	make new file directory for extracted tifs
	"""
	new_dir = os.path.join(workingDir, "converted_tif")
	message = "\n>> Files will be saved: \n --> "+str(new_dir)
	IJ.log(message)
	if os.path.exists(new_dir):
		return new_dir
	else:
		os.mkdir(new_dir)
		return new_dir


def set_options(image, series = None):
	"""
	creates ImporterOptions object and sets options
	returns the imps object
	"""
	if series is not None:
		options = ImporterOptions()
		options.setId(image)
		options.setSeriesOn(s,True)
		imps = BF.openImagePlus(options)
		return imps
	else:
		print("no series found")
		options = ImporterOptions()
		options.setId(image)
		imps = BF.openImagePlus(options)
		return imps


def fix_name(imps):
	"""
	takes imps object, returns fixed name string
        expects format as:
        2018-01-29_SLICEID-sliceNumber.lif - Image001_notes-here
        outputs as:
        2018-01-29_SLICEID-sliceNumber_img001_notes-here
        Will not skip tiled repeats, please see nick for help with that.
	"""
	name_str = imps[0].title.replace(" ","").replace(".lif-","_").replace(".oib","").replace(".czi","").replace(".lsm","").replace(".nd2", "")
	name_str_fix = name_str.replace("Image", "img")
	return name_str_fix

def save_tif(imps, name, new_dir):
	"""
	takes imps object and name string, saves as tif
	"""
	new_name = os.path.join(new_dir, name+".tif")
	if os.path.exists(new_name):
		message = ">> *File:* \n -->"+ new_name + "\n exists, continuing"
		IJ.log(message)
		print("File "+ new_name + " exists, continuing")
		return
	else:
		fs = FileSaver(imps[0])
		fs.saveAsTiff(new_name)

# Main script

new_dir = make_dir(folder)
# filter for your images, get the files with the accepted endings
listoffiles = [ str(f) for f in os.listdir(folder) if f.endswith(accepted_files)]
# ignore automatically generated hidden files that start with .
real_names = [f for f in listoffiles if not f.startswith(".")]
message = "\n\n >> Now converting the following files: \n"+ "\n --> ".join(real_names) 
IJ.log(message)

for i in real_names:
	image = os.path.join(folder, i)
	print(image)
	message = "\n >> Now processing: \n --> " +str(image)
	IJ.log(message)
	reader = ImageReader()
	# set image id
	reader.setId(image)
	# get series list
	series = reader.getSeriesCount()
	# iterate through series
	for s in range(series):
	       	imps = set_options(image, s)
	       	fixed_name = fix_name(imps)
	       	save_tif(imps, fixed_name, new_dir)

print("DONE!")
IJ.log("\n\n >> DONE!")
