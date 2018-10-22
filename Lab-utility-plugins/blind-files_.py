# blind files
# Author: Nick George
# Contact: nicholas.m.george@ucdenver.edu
# updated last: 2018-10-22
# using imagej script parameters(https://imagej.net/Script_Parameters) for the gui on this one.
# script params below
#@ File (label="Choose the image directory to blind", style="directory") directory
#@ String (label="What is the file ending of your image files?", choices={".tif",".jpg",".jpeg",".png", ".pdf", ".czi", ".lsm", ".nd2", ".lif", ".oib"}, style="listBox") fileend
import os
import uuid
import shutil
import sys
from ij import IJ

IJ.log("\n\n >> Welcome to blind_files! <<" )
IJ.log("\n\n >> Please report issues here: \nhttps://github.com/Macklin-Lab/imagej-microscopy-scripts/issues")
folder = str(directory)
assert os.path.exists(folder), "Couldnt find the directory. Try using 'Browse' next time"

def make_dir(folder):
	"""
	make new file directory for extracted tifs
	if folder exists, just return the path.
	"""
	new_dir = os.path.join(folder, "blinded")
	if os.path.exists(new_dir):
		return new_dir
	else:
		os.mkdir(new_dir)
		return new_dir


def copy_files(old, new):
	"""
	takes the old file name and the blinded file name
	copies the old to the new.
	"""
	if os.path.exists(new):
		message = str("\n >> *file:* " + new + " exists, continuing")
		IJ.log(message)
		print(message)
	else:
		message = str("\n >> *original file* \n --> "+ old+ "\n >> *saving as* \n --> " + new)
		print(message)
		IJ.log(message)
		shutil.copyfile(old, new)


# main script

# make new directory
new_dir = make_dir(folder)
message = "\n\n >> Making new directory \n"+ str(new_dir) 
IJ.log(message)
# create key file name based on input directory.
key_file = os.path.join(folder, "KEY.csv")
# make blinded key path

blinded_key = os.path.join(new_dir, "blinded-key.csv")

message = "\n\n >> Writing key "+ str(blinded_key) 
IJ.log(message)

listoffiles = [f for f in os.listdir(folder) if f.endswith(fileend)]

# ignore hidden files starting with .
real_names = [os.path.join(folder,f) for f in listoffiles if not f.startswith(".")]
message = "\n\n >> Now blinding the following files: \n"+ "\n --> ".join(real_names) 
IJ.log(message)
# make unique blinded names use a set comprehension to avoid duplicates

uniquenames = {os.path.join(new_dir, str(uuid.uuid4().hex)+ fileend) for old_name in real_names}

# verify that there are no duplicate names. if this fails, something very rare has happened and you can try again
assert len(real_names) == len(uniquenames)

# zip the two lists for processing
zipped = zip(real_names, list(uniquenames))

print("writing key")
# if a key file already exists, quit.
if os.path.exists(key_file):
	print("key exists, quitting")
	IJ.log("\n\n>> !!key exists, quitting!\n\n")
	sys.exit("goodbye!")

# iterate through the zipped list of new and old files, copying them to blinded

for old, new in zipped:
	copy_files(old, new)


# write the key file using the same zipped lists.
with open(key_file, "w") as key:
	key.write("old-name , new-name \n")
	for old, new in zipped:
		key.write(old + "," + new + "\n")

# write our blinded key to the blinded folder
with open(blinded_key, "w") as blindKey:
	# write header
	blindKey.write("blinded name \n")
	for old, new in zipped:
	       	blindKey.write(new + "\n")

print("DONE")
IJ.log("\n\nDONE!\n\n")