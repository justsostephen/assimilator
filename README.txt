Assimilator | Gourmet ground images.
====================================

Version 1.0.0
stephenmather.com
Copyright (C) 2013 Stephen Mather
Available under the GNU Lesser General Public License.  Please see LICENSE.txt
for further details.  Download the source from stephenmather.com.

Copying and distribution of this file, with or without modification, are
permitted in any medium without royalty provided the copyright notice and this
notice are preserved.  This file is offered as-is, without any warranty.


Contents
--------

- Introduction
- System Requirements
- Installation
- Usage
- Square Images and Scaling Images Without Cropping
- Version History


Introduction
------------

Assimilator is a batch image processor written in Python.  It utilises the
Python Imaging Library (PIL) to:

- Resize and crop images to specified dimensions
- Intelligently handle conflicting orientations by rotating, scaling or
  transposing dimensions
- Optionally add a background to scaled images and set its colour
- Output bitmap, JPEG or PNG files
- Set JPEG and PNG DPI
- Set JPEG quality level
- Add a prefix to output filenames

Assimilator's primary purpose is to produce images of exact horizontal and
vertical dimensions.  It does this by constraining image proportions, scaling
to fill the desired dimensions and cropping an equal amount from the left and
right / top and bottom of images.  This method is a "best fit" for batch
processing images, based on the fact that the focus of most images is roughly
central.

Assimilator does have additional functionality, however.  Please see the
section titled 'Square Images and Scaling Images Without Cropping' for further
details.


System Requirements
-------------------

Linux
'''''

- 32 or 64 bit (there are separate versions for each) GNU/Linux based operating
  system (tested on Ubuntu and Fedora)


Macintosh
'''''''''

- 64 bit Mac OS X 10.6 or later


Windows
'''''''

- 32 or 64 bit Windows XP or later


Installation
------------

Linux and Macintosh
'''''''''''''''''''

- Move the 'assimilator' binary contained in the same archive as this README to
  a location in your PATH such as '/usr/bin/'.  This can be done by opening a
  terminal emulator (the Terminal application on Macintosh), changing to the
  directory containing the 'assimilator' binary by issuing the command:
  
  cd ~/Downloads/Assimilator-1.0.0-mac/
  
  assuming the 'assimilator' binary is located in the 'Assimilator-1.0.0-mac'
  directory in your 'Downloads' directory, then issuing the command:
  
  sudo mv assimilator /usr/bin/
  
  You may be prompted to enter a password in order to run 'sudo'.  Enter your
  user password.

- Make sure the 'assimilator' binary is executable by issuing the command:
  
  sudo chmod +x /usr/bin/assimilator


Windows
'''''''

- 'Assimilator.exe' contained in the same archive as this README can be run
  from anywhere.


Usage
-----

On Linux and Macintosh, open a terminal emulator and issue the command:

assimilator

On Windows, run 'Assimilator.exe'.

You will be prompted to enter a series of parameters.  These are detailed
below.  Enter 'q' at any prompt to quit without processing any images.


Source directory
''''''''''''''''

Enter the path of the directory containing the images you wish to process.  If
you have run Assimilator from this directory, you can simply enter a dot ('.'
without the quotes).  If you have run Assimilator from another directory, you
can type the path, copy and paste it, or drag and drop a folder on to the
command window.


Width
'''''

Enter the desired output image width in pixels.


Height
''''''

Enter the desired output image height in pixels.


Bitmap, JPEG or PNG
'''''''''''''''''''

Assimilator can output images in one of three file formats: bitmap, JPEG or
PNG.  Select one by entering the letter 'b', 'j' or 'p', respectively.


DPI
'''

If you selected JPEG or PNG file format, you will be prompted to enter the
desired output image DPI (dots per inch).  The PIL does not support setting a
bitmap image's DPI.  As a rule of thumb, enter 72 if you intend to use your
images on screen and 300 if you'd like to print your images.


Quality
'''''''

If you selected JPEG file format, you will be prompted to enter the desired
output image quality.  This affects the level of compression used.  Entering a
value of 1 will compress the output images heavily (small file size, but poor
appearance); entering a value of 100 will not compress them at all (large file
size, but excellent appearance).  A value of 75 is a good default, resulting in
an optimal balance between file size and appearance.


Rotate, scale or transpose
''''''''''''''''''''''''''

When an input image has an orientation that differs from that specified by your
desired output dimensions (e.g. an input image has a portrait orientation and
the dimensions you specify would result in landscape images), you can choose
what to do.  There are three options:

- Rotate the image through 90 degrees
- Scale the image to fit inside the output dimensions
- Transpose the output dimensions so that the width becomes the height and vice
  versa

Select one by entering the letter 'r', 's' or 't', respectively.


Clockwise or anticlockwise
''''''''''''''''''''''''''

If you chose to rotate images with conflicting orientations, you will be
prompted to select a rotation direction.  Enter the letter 'c' for clockwise or
'a' for anticlockwise.


Background
''''''''''

If you chose to scale images with conflicting orientations, you will be asked
if you would like to add a background to the output images.  Enter 'y' for yes
or 'n' for no.


Background colour
'''''''''''''''''

If you chose to add a background to the output images, you will be prompted to
enter the RGB values of the desired background colour.  Separate each value
with a comma.  If you are unsure of the values for a particular colour, most
image editing software will display RGB values in its colour selection window.


Filename prefix
'''''''''''''''

Assimilator puts all of the output images in a directory called 'assimilated'
in the specified source directory so that you will never overwrite your
original images.  The output images will have the same filenames as your
original images, however you can add a prefix to those filenames by entering it
here.  If you don't want to add a prefix, don't enter anything.


Begin assimilation?
'''''''''''''''''''

This final prompt serves to let you know that you have entered all requisite
parameters and also gives you one last opportunity to quit Assimilator without
processing any images.  To begin assimilation enter a 'y' for yes, or enter an
'n' for no to quit.

If you choose to begin assimilation, Assimilator will look at each file in the
specified source directory, check to see if it is a compatible image file and
if so, process it.  All output image files are written to a directory named
'assimilated' in the specified source directory.  Once complete, the number of
assimilated files will be indicated and you will be prompted to press the Enter
key to exit.


Square Images and Scaling Images Without Cropping
-------------------------------------------------

If the entered dimensions will result in square images (i.e. the specified
width and height are the same), there will not be any conflicting orientations
as a square image is neither landscape nor portrait.  However, it may be
desirable to scale images to fit inside square dimensions.  As such, if the
'scale' conflict option is selected it will apply to all input images when
square dimensions have been entered.

This functionality allows Assimilator to scale images based on a single
dimension (the greater of the desired width and height) without any cropping
occurring.  To do this, enter the greater dimension at both the width and
height prompts, select the 'scale' conflict option and don't apply a
background.  The lesser dimension will be resized proportionally.


Version History
---------------

This software uses Semantic Versioning.  Please see semver.org for further
details.


1.0.0
'''''

- Initial release.
