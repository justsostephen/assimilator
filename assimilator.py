#! /usr/bin/env python

"""
Assimilator | Gourmet ground images.

Utilise the Python Imaging Library (PIL) to process a batch of images given a
number of user defined parameters.

Assimilator is available from stephenmather.com, Copyright (C) 2013 Stephen
Mather.  The Python Imaging Library (PIL) is available from
pythonware.com/products/pil, Copyright (C) 1997-2009 Secret Labs AB, Copyright
(C) 1995-2009 Fredrik Lundh.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

__version__ = '1.0.0'
__author__ = 'Stephen Mather <stephen@stephenmather.com>'

import os
import sys

# PIL modules.
import Image
import ImageFile


def get_directory():
    """Working directory -- prompt for and set working directory."""
    # Loop until entered string is a valid directory, then set it as the
    # working directory.
    while True:
        directory = raw_input('Source directory: ')
        # If value entered is 'q', quit.
        if directory == 'q': sys.exit()
        # Remove invalid characters from path.
        directory = directory.strip()
        directory = directory.strip("'")
        directory = directory.strip('"')
        directory = directory.replace('\ ', ' ')
        if os.path.isdir(directory):
            os.chdir(directory)
            break
        print 'Invalid entry.'


def get_dimensions():
    
    """
    Output dimensions -- prompt for desired dimensions.
    
    Return:
    out_width -- specified image output width as a float
    out_height -- specified image output height as a float
    out_size -- tuple containing out_width and out_height
    
    """
    
    # Output width -- loop until value entered is an integer greater than 0,
    # then turn it into a float (necessary for later calculations).
    while True:
        out_width = raw_input('Width: ')
        # If value entered is 'q', quit.
        if out_width == 'q': sys.exit()
        try:
            out_width = int(out_width)
        except Exception:
            print 'Invalid entry.'
        else:
            if out_width > 0:
                out_width = float(out_width)
                break
            print 'Invalid entry.'
    
    # Output height -- loop until value entered is an integer greater than 0,
    # then turn it into a float (necessary for later calculations).
    while True:
        out_height = raw_input('Height: ')
        # If value entered is 'q', quit.
        if out_height == 'q': sys.exit()
        try:
            out_height = int(out_height)
        except Exception:
            print 'Invalid entry.'
        else:
            if out_height > 0:
                out_height = float(out_height)
                break
            print 'Invalid entry.'
    
    out_size = (out_width, out_height)
    
    return out_width, out_height, out_size


def get_dpi():
    """Output DPI -- prompt for value and return it as an integer."""
    # Loop until value entered is an integer greater than 0.
    while True:
        out_dpi = raw_input('DPI: ')
        # If value entered is 'q', quit.
        if out_dpi == 'q': sys.exit()
        try:
            out_dpi = int(out_dpi)
        except Exception:
            print 'Invalid entry.'
        else:
            if out_dpi > 0:
                break
            print 'Invalid entry.'
    return out_dpi


def get_quality():
    """Output quality -- prompt for value and return it as an integer."""
    # Loop until value entered is an integer between 1 and 100.
    while True:
        out_quality = raw_input('Quality (1 = lowest, 100 = highest): ')
        # If value entered is 'q', quit.
        if out_quality == 'q': sys.exit()
        try:
            out_quality = int(out_quality)
        except Exception:
            print 'Invalid entry.'
        else:
            if 1 <= out_quality <= 100:
                break
            print 'Invalid entry.'
    return out_quality


def get_type():
    
    """
    Output file type -- prompt for desired file type and set variables.
    
    Return:
    out_type -- output filename extension as a string
    out_dpi -- specified image output DPI as an integer (JPEG and PNG only)
    out_quality -- specified image output quality as an integer (JPEG only)
    
    """
    
    # Loop until a valid string is entered.
    t = ('b', 'j', 'p')
    while True:
        out_type = raw_input('Bitmap, JPEG or PNG (b/j/p): ')
        # If value entered is 'q', quit.
        if out_type == 'q': sys.exit()
        if out_type in t: break
        print 'Invalid entry.'
    
    # Set bitmap variables.
    if out_type == 'b':
        out_type = '.bmp'
        out_dpi = None
        out_quality = None
    
    # Set JPEG variables.
    if out_type == 'j':
        out_type = '.jpg'
        out_dpi = get_dpi()
        out_quality = get_quality()
    
    # Set PNG variables.
    if out_type == 'p':
        out_type = '.png'
        out_dpi = get_dpi()
        out_quality = None
    
    return out_type, out_dpi, out_quality


def get_bgd_colour():
    """Background colour -- prompt for RGB values and return as a tuple."""
    # Loop until three comma separated integer values between 0 and 255 are
    # entered.
    while True:
        bgd_colour = raw_input('Background colour (Comma separated RGB values, e.g. 255, 255, 255): ')
        # If value entered is 'q', quit.
        if bgd_colour == 'q': sys.exit()
        # Split entered string on commas.
        values = bgd_colour.split(',')
        # Check for 3 values.
        if len(values) == 3:
            # Check that the values are integers.
            try:
                i = 0
                for value in values:
                    values[i] = int(value)
                    i += 1
            except Exception:
                print 'Invalid entry.'
            else:
                # Check that the values are between 0 and 255.
                valid = 0
                for value in values:
                    if 0 <= value <= 255:
                        valid += 1
                if valid == 3:
                    break
                print 'Invalid entry.'
        else:
            print 'Invalid entry.'
    return tuple(values)


def get_conflict():
    
    """
    Orientation conflict resolution.
    
    If an image's orientation conflicts with the specified output dimensions,
    ask whether to rotate it, scale it or transpose its dimensions.  Return:
    conflict -- string indicating whether to rotate, scale or transpose images
    with orientations that conflict with specified output dimensions
    clockwise -- boolean indicating direction of rotation
    background -- boolean indicating if a background is required
    bgd_colour -- tuple containing background RGB values
    
    """
    
    # Prompt for type of conflict resolution.
    t = ('r', 's', 't')
    print 'If an image\'s orientation conflicts with the entered dimensions,'
    print 'you can rotate it, scale it or transpose its dimensions.'
    # Loop until a valid string is entered.
    while True:
        conflict = raw_input('Rotate, scale or transpose (r/s/t): ')
        # If value entered is 'q', quit.
        if conflict == 'q': sys.exit()
        if conflict in t: break
        print 'Invalid entry.'
    
    # If conflicts are to be rotated, ask which direction they should be
    # rotated in.
    if conflict == 'r':
        t = ('c', 'a')
        # Loop until a valid string is entered.
        while True:
            clockwise = raw_input('Clockwise or anticlockwise (c/a): ')
            # If value entered is 'q', quit.
            if clockwise == 'q': sys.exit()
            if clockwise in t: break
            print 'Invalid entry.'
        # Set rotation direction.
        if clockwise == 'c':
            clockwise = True
        else:
            clockwise = False
        # Assign unused variable(s).
        background = None
        bgd_colour = None
    
    # If conflicts are to be scaled, ask if a background is required.
    if conflict == 's':
        t = ('y', 'n')
        # Loop until a valid string is entered.
        while True:
            background = raw_input('Background (y/n): ')
            # If value entered is 'q', quit.
            if background == 'q': sys.exit()
            if background in t: break
            print 'Invalid entry.'
        if background == 'y':
            background = True
            bgd_colour = get_bgd_colour()
        else:
            background = False
            bgd_colour = None
        # Assign unused variable(s).
        clockwise = None
    
    # If conflicts are to have their dimensions transposed, assign unused
    # variable(s).
    if conflict == 't':
        clockwise = None
        background = None
        bgd_colour = None
    
    return conflict, clockwise, background, bgd_colour


def get_prefix():
    """Filename prefix -- prompt for prefix and return it as a string."""
    prefix = raw_input('Filename prefix: ')
    # If value entered is 'q', quit.
    if prefix == 'q': sys.exit()
    return prefix


def confliction(
        out_width, out_height, in_width, in_height, conflict, clockwise, img):
    """
    Determine if input image orientation conflicts with desired output.
    
    Parameters:
    out_width -- image output width as a float
    out_height -- image output height as a float
    in_width -- image input width as an integer
    in_height -- image input height as an integer
    conflict -- type of conflict resolution as a string
    clockwise -- boolean indicating rotation direction
    img -- the input image object, an instance of the PIL Image class
    Return:
    in_width
    in_height
    img
    conflicted -- boolean indicating if dimensions conflict
    
    """
    if (out_width > out_height and in_width < in_height or
        out_width < out_height and in_width > in_height):
        conflicted = True
        # If 'rotate' or 'transpose' has been selected, rotate.
        if conflict == 'r' and not clockwise or conflict == 't':
            img = img.rotate(90)
            in_width, in_height = img.size
        if conflict == 'r' and clockwise:
            img = img.rotate(270)
            in_width, in_height = img.size
    # If square output image is desired and 'scale' has been selected, force
    # scale.
    elif out_width == out_height and conflict == 's':
        conflicted = True
    else:
        conflicted = False
    return in_width, in_height, img, conflicted


def scaling_req(
        out_width, out_height, in_width, in_height, out_size, conflict,
        conflicted, img):
    
    """
    Determine if scaling is required and if so, in which direction.
    
    Parameters:
    out_width -- image output width as a float
    out_height -- image output height as a float
    in_width -- image input width as an integer
    in_height -- image input height as an integer
    out_size -- tuple containing out_width and out_height
    conflict -- type of conflict resolution as a string
    conflicted -- boolean indicating if dimensions conflict
    img -- the input image object, an instance of the PIL Image class
    Return:
    scale -- boolean indicating whether scaling is required or not
    scl_up -- boolean indicating which direction to scale in
    
    """
    
    # If none of the conditions below are met, scaling is not required.
    scale = False
    scl_up = None
    # Not required if image is already correct dimensions.
    if img.size != out_size:
        # Not required if 'scale' has been selected, orientation
        # conflicts, one dimension is correct and the other is smaller.
        if conflict == 's' and conflicted:
            if not (in_width == out_width and in_height < out_height):
                if not (in_width < out_width and in_height == out_height):
                    scale = True
        else:
            # Not required if one dimension is correct and the other is
            # larger.
            if not (in_width == out_width and in_height > out_height):
                if not (in_width > out_width and in_height == out_height):
                    scale = True
    
    # If scaling is required, determine whether to scale up or down.
    if scale:
        # If 'scale' has been selected, orientation conflicts and one
        # dimension is larger scale down, else scale up.
        if conflict == 's' and conflicted:
            if in_width > out_width or in_height > out_height:
                scl_up = False
            else:
                scl_up = True
        else:
            # If both dimensions are larger scale down, else scale up.
            if in_width > out_width and in_height > out_height:
                scl_up = False
            else:
                scl_up = True
    
    return scale, scl_up


def scaling(
        out_width, out_height, in_width, in_height, conflict, conflicted,
        scl_up, img):
    """
    Scale input image.
    
    Parameters:
    out_width -- image output width as a float
    out_height -- image output height as a float
    in_width -- image input width as an integer
    in_height -- image input height as an integer
    conflict -- type of conflict resolution as a string
    conflicted -- boolean indicating if dimensions conflict
    scl_up -- boolean indicating which direction to scale in
    img -- the input image object, an instance of the PIL Image class
    Return:
    in_width
    in_height
    img
    
    """
    # Calculate scaling parameters.
    if not scl_up:
        # Scale down.
        # Calculate width and height percentage differences between desired
        # output and input image.
        pct_width = 100 - ((out_width / in_width) * 100)
        pct_height = 100 - ((out_height / in_height) * 100)
        # If 'scale' has been selected and orientation conflicts choose
        # highest difference, else choose lowest.
        if conflict == 's' and conflicted:
            pct_decrease = max(pct_width, pct_height)
        else:
            pct_decrease = min(pct_width, pct_height)
        # Calculate number of pixels to decrease axes by.
        dec_width = int(round(in_width * (pct_decrease / 100)))
        dec_height = int(round(in_height * (pct_decrease / 100)))
        # Calculate scaled image dimensions.  Make sure result is never 0.
        fin_width = max(1, in_width - dec_width)
        fin_height = max(1, in_height - dec_height)
    else:
        # Scale up.
        # Calculate width and height percentage differences between desired
        # output and input image.
        pct_width = ((out_width / in_width) * 100) - 100
        pct_height = ((out_height / in_height) * 100) - 100
        # If 'scale' has been selected and orientation conflicts choose lowest
        # difference, else choose highest.
        if conflict == 's' and conflicted:
            pct_increase = min(pct_width, pct_height)
        else:
            pct_increase = max(pct_width, pct_height)
        # Calculate number of pixels to increase axes by.
        inc_width = int(round(in_width * (pct_increase / 100)))
        inc_height = int(round(in_height * (pct_increase / 100)))
        # Calculate scaled image dimensions.
        fin_width = in_width + inc_width
        fin_height = in_height + inc_height
    # Perform scaling.
    img = img.resize((fin_width, fin_height), Image.ANTIALIAS)
    # Reassign width and height.
    in_width, in_height = img.size
    return in_width, in_height, img


def cropping(out_width, out_height, in_width, in_height, img):
    """
    Crop input image.
    
    Parameters:
    out_width -- image output width as a float
    out_height -- image output height as a float
    in_width -- image input width as an integer
    in_height -- image input height as an integer
    img -- the input image object, an instance of the PIL Image class
    Return:
    in_width
    in_height
    img
    
    """
    # Calculate cropping boundaries.
    left = int((in_width - out_width) / 2)
    upper = int((in_height - out_height) / 2)
    right = int(left + out_width)
    lower = int(upper + out_height)
    # Perform cropping.
    img = img.crop((left, upper, right, lower))
    # Reassign width and height.
    in_width, in_height = img.size
    return in_width, in_height, img


def backgrounding(
        out_width, out_height, in_width, in_height, bgd_colour, img):
    """
    Add a background to the input image.
    
    Parameters:
    out_width -- image output width as a float
    out_height -- image output height as a float
    in_width -- image input width as an integer
    in_height -- image input height as an integer
    bgd_colour -- tuple containing background RGB values
    img -- the input image object, an instance of the PIL Image class
    Return:
    in_width
    in_height
    img
    
    """
    # Create a new image object with desired dimensions and background colour.
    bgd = Image.new('RGB', (int(out_width), int(out_height)), bgd_colour)
    # Calculate input image paste location.
    left = int((out_width - in_width) / 2)
    upper = int((out_height - in_height) / 2)
    # Paste input image onto background.
    bgd.paste(img, (left, upper))
    # Assign new image object to 'img' variable.
    img = bgd
    # Reassign width and height.
    in_width, in_height = img.size
    return in_width, in_height, img


def save_img(
        in_file, prefix, out_type, out_dpi, out_quality, assimilated, img):
    """
    Save the processed image.
    
    Parameters:
    in_file -- input image filename as a string
    prefix -- desired output filename prefix as a string
    out_type -- output filename extension as a string
    out_dpi -- specified image output DPI as an integer (JPEG and PNG only)
    out_quality -- specified image output quality as an integer (JPEG only)
    assimilated -- the number of images processed as an integer
    img -- the input image object, an instance of the PIL Image class
    Return:
    assimilated
    
    """
    # If the output directory does not exist, create it.
    if not os.path.isdir('assimilated'):
        os.mkdir('assimilated')
    # Get the input image filename and extension.
    filename, extension = os.path.splitext(in_file)
    # Convert the input image mode to RGB.
    img = img.convert('RGB')
    # Try and save the image.
    try:
        img.save('assimilated/' + prefix + filename + out_type, optimize=True,
                 dpi=(out_dpi, out_dpi), quality=out_quality)
    except IOError:
        print "Assimilation of '" + in_file + "' failed..."
    else:
        print "'" + in_file + "' assimilated..."
        assimilated += 1
    return assimilated


def main():
    
    print
    print 'Assimilator | Gourmet ground images.'
    print
    print 'Version', __version__
    print 'stephenmather.com'
    print 'Copyright (C) 2013 Stephen Mather'
    print 'Available under the GNU Lesser General Public License.'
    print
    print 'Please see README.txt for usage details.'
    print 'Enter \'q\' at any prompt to quit.'
    print
    get_directory()
    out_width, out_height, out_size = get_dimensions()
    out_type, out_dpi, out_quality = get_type()
    conflict, clockwise, background, bgd_colour = get_conflict()
    prefix = get_prefix()
    
    # Begin assimilation prompt -- loop until a valid string is entered.
    while True:
        begin = raw_input('Begin assimilation? (y/n): ')
        # If value entered is 'q' or 'n', quit.
        if begin == 'q' or begin == 'n': sys.exit()
        if begin == 'y':
            print
            break
        print 'Invalid entry.'
    
    # Blacklisted files.
    blk_files = ('assimilator', 'Assimilator', 'assimilator.py',
                 'Assimilator.app', 'Assimilator.exe')
    # Create a list of files from the working directory that are not
    # blacklisted.
    files = []
    for in_file in os.listdir('.'):
        if in_file not in blk_files and os.path.isfile(in_file):
            files.append(in_file)
    
    # Override the 'ImageFile' module's 'MAXBLOCK' constant if necessary to
    # make saving large images possible.
    ImageFile.MAXBLOCK = max(ImageFile.MAXBLOCK, int(out_width * out_height))
    
    # Count the number of images processed.
    assimilated = 0
    # Try and open each file in the 'files' list and process it.
    for in_file in files:
        try:
            img = Image.open(in_file)
        except IOError:
            print "'" + in_file + "' is not an image file, skipping..."
        else:
            # Assign variables for input image width and height.
            in_width, in_height = img.size
            
            # Determine if orientations conflict.
            in_width, in_height, img, conflicted = confliction(
                out_width, out_height, in_width, in_height, conflict,
                clockwise, img)
            
            # Determine if scaling is required and if so, in which direction.
            scale, scl_up = scaling_req(
                out_width, out_height, in_width, in_height, out_size,
                conflict, conflicted, img)
            
            # If the input image needs to be scaled, scale it.
            if scale:
                in_width, in_height, img = scaling(
                    out_width, out_height, in_width, in_height, conflict,
                    conflicted, scl_up, img)
            
            # If the input image is not yet the correct size and it is not a
            # scaled conflict, crop it.
            if img.size != out_size:
                if not (conflict == 's' and conflicted):
                    in_width, in_height, img = cropping(
                        out_width, out_height, in_width, in_height, img)
            
            # If 'transpose' was selected and the input image had a
            # conflicting orientation and was hence rotated, rotate back.
            if conflict == 't' and conflicted:
                img = img.rotate(270)
            
            # Apply background, if required.
            if conflict == 's' and conflicted and background:
                in_width, in_height, img = backgrounding(
                    out_width, out_height, in_width, in_height, bgd_colour,
                    img)
            
            # Save image.
            assimilated = save_img(
                in_file, prefix, out_type, out_dpi, out_quality, assimilated,
                img)
    
    print
    print assimilated, 'file(s) assimilated.'
    raw_input('Press Enter key to exit.')


if __name__ == '__main__':
    main()
