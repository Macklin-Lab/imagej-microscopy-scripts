
"""
!!Don't use this one yet. Still in progress. will be merged with convert-tif.py


author: Nick George
email: nicholas.m.george@ucdenver.edu

"""

from ij import IJ, WindowManager, ImagePlus
from ij.io import DirectoryChooser, FileSaver
from loci.plugins import BF
from loci.plugins.in import ImporterOptions
from loci.formats import ImageReader
import os


# open directoy
dc = DirectoryChooser("Choose a folder")
#folder = os.path.join("C:", "\Users", "geornich", "Desktop", "test")
folder = dc.getDirectory()

# functions to make stuff easier

def make_dir(workingDir):
	"""
	make new file directory for extracted lifs
	"""
	new_dir = os.path.join(workingDir, "converted_lif")
	if os.path.exists(new_dir):
		return new_dir
	else:
		os.mkdir(new_dir)
		return new_dir


def make_tile_folder(workingDir, imps):
	name_str = imps[0].title.split(" - ")[0]#.replace(" ","").replace(".lif-","_")
	folder_name = name_str.replace(" ","").replace(".lif-","_").replace(".lif", "")
	name_str_fix = name_str.replace(" ","").replace(".lif-","_").replace(".lif", "_")
	print(" ")
	print("NAME STR FIX")
	print(name_str_fix)
	tile_dir = os.path.join(workingDir,folder_name)
	if os.path.exists(tile_dir):
		return tile_dir, name_str_fix
	else:
		os.mkdir(tile_dir)
		return tile_dir, name_str_fix

def set_options(image, series = None):
	"""
	creates ImporterOptions object adn sets options
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
	expects naming setup as:
	2017-01-29_SLICEID-sliceNumber.lif - 2017-01-29_SLICEID-sliceNumber_notes_imgNumber
	ouputs as:
	2017-01-29_SLICEID-sliceNumber_notes_imgNumber
	"""
	name_str = imps[0].title.split(" - ")#.replace(" ","").replace(".lif-","_")
	name_str_fix = name_str[-1]
	if "TileScan" in name_str_fix:
		name_str_tile = name_str_fix.replace(" ","|")
		if not "Merging" in name_str_tile:
			return "Tile"
		else:
			print("Merge found " + name_str_tile)
			new_merged_name = imps[0].title.replace(".lif - ", "_")
			return new_merged_name
	return name_str_fix



def save_tif(imps, name, new_dir):
	"""
	takes imps object and name string, saves as tif
	"""
	new_name = os.path.join(new_dir, name+".tif")
	if os.path.exists(new_name):
		print("File "+ new_name + " exists, continuing")
		return
	else:
		fs = FileSaver(imps[0])
		fs.saveAsTiff(new_name)

# Main script

if folder is None:
	print("User Canceled")
else:
	new_dir = make_dir(folder)
	# filter for your images
	listoffiles = [ str(f) for f in os.listdir(folder) if f.endswith(".lif") or f.endswith(".oib") if not f.startswith(".")]
	for i in listoffiles:
		image = os.path.join(folder,i)
		assert os.path.exists(image)
		reader = ImageReader()
		# set image id
		reader.setId(image)
		# get series list
		series = reader.getSeriesCount()
		# iterate through series
		for s in range(series):
			imps = set_options(image, s)
			fixed_name = fix_name(imps)
			if fixed_name == "Tile":
				tile_folder, tile_name = make_tile_folder(folder, imps)
				print(tile_folder)
				save_tif(imps, tile_name+str(s), tile_folder)
				continue
			else:
				print('now saving ' + fixed_name)
				save_tif(imps, fixed_name, new_dir)
