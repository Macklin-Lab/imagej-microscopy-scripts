import ij
# author: Nick George
# contact: nicholas.m.george@ucdenver.edu
#
#
# keyboard shortcut for quickly changing the display state of the active image.
# It gets the current image, and checks the display state with getCompositeMode().
# if the image is color or greyscale (colors displayed separately), then it makes it composite.
# if it is composite (channels overlaid), it changes it to color. This is useful for quickly
# switching display states when examining images.

# setDisplayMode() == 1 is composite, 2 is color, 3 is greyscale
imp = ij.WindowManager.getCurrentImage()
if imp == None:
    pass
else:
    if imp.getCompositeMode() == 2 or imp.getCompositeMode() == 3:
        imp.setDisplayMode(1)
    elif imp.getCompositeMode() == 1:
        imp.setDisplayMode(2)
