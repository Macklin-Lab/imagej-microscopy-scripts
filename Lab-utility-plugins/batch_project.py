# script to max project a directory full of images. 
#@ File (label="Choose the image directory of tif's to Project.", style="directory") directory
#@ String(choices={"Max Projection", "Average Projection", "Min Projection", "SD Projection", "Sum Projection", "Median Projection"}, style="listBox") projection_type
import os
from ij import IJ
from ij.io import FileSaver
from ij.plugin import ZProjector

folder = str(directory)

proj_opts_dir = {"Max Projection":"max", "Average Projection":"avg", "Min Projection":"min", "SD Projection":"sd", "Sum Projection":"sum", "Median Projection":"median"}
opt = proj_opts_dir[projection_type]


def make_dir(workingDir):
	"""
	make new file directory for projected images
	"""
	new_dir = os.path.join(workingDir, "projected")
	if os.path.exists(new_dir):
		return new_dir
	else:
		os.mkdir(new_dir)
		return new_dir


def project(img, method):
	zp = ZProjector.run(img, method)
	return zp 

def make_name(str_name, type_of_proj):
	"""Makes the new name for the file. 
	"""
	new_name = str_name.replace(".tif", "_" + str(type_of_proj) + ".tif")
	just_name = os.path.split(new_name)[-1]
	return just_name

def save_tif(imps, new_name, new_dir):
	"""
	takes imps object and name string, saves as tif
	"""
	new_name = os.path.join(new_dir, new_name)
	if os.path.exists(new_name):
		print("File "+ new_name + " exists, continuing")
		return
	else:
		fs = FileSaver(imps)
		fs.saveAsTiff(new_name)


assert os.path.exists(folder), "Couldnt find the directory. Try using 'Browse' next time"

new_dir = make_dir(folder)

# filter for your images, get the files with the accepted endings
listoffiles = [ str(f) for f in os.listdir(folder) if f.endswith(".tif")]
# ignore automatically generated hidden files that start with .
real_names = [os.path.join(folder,f) for f in listoffiles if not f.startswith(".")]

for i in real_names:
	img = IJ.openImage(i)
	print(type(img))
	new = project(img, opt)
	new_name = make_name(i,opt)
	save_tif(new, new_name, new_dir)

print("Done")
