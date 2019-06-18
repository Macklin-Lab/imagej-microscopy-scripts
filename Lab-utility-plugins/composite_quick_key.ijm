// quick macro to change the display mode of the current image. 
// Author: Nick George
// Contact: nicohlas.m.george@ucdenver.edu
// recommend setting this as a keyboard shortcut.
Stack.getDisplayMode(mode);
if (mode == "color" || mode == "greyscale"){
	Stack.setDisplayMode("composite");
} else {
	Stack.setDisplayMode("color");
}
