# blind files

"""
!!
If desired file type is not ".tif" change the "fileending" variable to the appropriate file ending
!!

author: Nick George
email: nicholas.m.george@ucdenver.edu

updated 2018-02-15

choose input folder. Will make the output folder "blinded"
and copy files to new folder.
A key will be saved in the original folder. If a key already exists, then the
script will quit.
"""


import os
import uuid
import shutil
import sys
from ij.io import DirectoryChooser

### CHANGE THIS VARIABLE FOR DIFFERENT FILE TYPES!
fileending = ".tif"
###

dc = DirectoryChooser("Choose a folder")

# store chosen directory in "folder" variable

folder = dc.getDirectory()


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
		print("file " + new + " exists, continuing")
	else:
		print("original file "+ old+ " saving as " + new)
		shutil.copyfile(old, new)


# main script

if folder is None:
	print("User canceled")

else:
	# make new directory
	new_dir = make_dir(folder)

	# create key file name based on input directory.
	key_file = os.path.join(folder, "KEY.csv")
	# make blinded key path

	blinded_key = os.path.join(new_dir, "blinded-key.csv")

	listoffiles = [f for f in os.listdir(folder) if f.endswith(fileending)]

        # ignore hidden files starting with .
	real_names = [os.path.join(folder,f) for f in listoffiles if not f.startswith(".")]

	# make unique blinded names use a set comprehension to avoid duplicates

	uniquenames = {os.path.join(new_dir, str(uuid.uuid4().hex)+ fileending) for old_name in real_names}

	# verify that there are no duplicate names. if this fails, something very rare has happened and you can try again
	assert len(real_names) == len(uniquenames)

	# zip the two lists for processing
	zipped = zip(real_names, list(uniquenames))

	print("writing key")
	# if a key file already exists, quit.
	if os.path.exists(key_file):
		print("key exists, quitting")
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
