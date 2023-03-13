import argparse
import glob
import os
import subprocess

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import lines

import imageio
import pupil_apriltags

def rgb_to_bw(im_rgb):
    """convert 3 channel RGB image to grayscale [0,255] with output uint8

    Parameters
    ----------
    im_rgb : ndarray
        input image to convert [ny,nx,3] in RGB format

    Returns
    -------
    output: ndarray
        output image in grayscale [ny, nx] with values [0,255]
    """

    # NTSC standards
    im = (im_rgb[:,:,0]*0.299 +
          im_rgb[:,:,1]*0.587 +
          im_rgb[:,:,2]*0.114)

    im -= np.amin(im)
    im *= 255/np.amax(im)

    return np.rint(im).astype(np.uint8)

if __name__ == "__main__":

    # set up the CLI
    parser = argparse.ArgumentParser(
        prog="mass_tracker.py",
        description="computes the location of the mass on a spring"
    )

    parser.add_argument("-i", "--input_directory",
                        required=True,
                        help="directory of tiff images")
    parser.add_argument("-o", "--output_file",
                        default="locations.txt",
                        help=("output text file with time stamps and locations "
                              "(default is 'locations.txt')"))
    parser.add_argument("-s","--tag_size",
                        required=True,
                        help="size of AprilTag vertically in mm")    
    parser.add_argument("-t", "--sample_period",
                        default=2/50,
                        help="time between image frames in seconds (default is 0.04 s)")
    
    # parse the inputs
    args = parser.parse_args()
    input_directory = args.input_directory
    output_file = args.output_file
    tag_size = float(args.tag_size)
    sample_period = float(args.sample_period) # default is 2/50
                                              # (skip two frames at 50 frames/sec)
                                       
    # finds input images to process
    files = sorted(glob.glob("%s/*.tif" % input_directory))

    # initializes arrays to store the center values
    center_horz = np.zeros(len(files))
    center_vert = np.zeros(len(files))

    # initial list of potentially bad images
    missed_tags = []

    # set up a time array for potentially bad frames
    time_array = np.arange(len(files))*sample_period
    
    for k, filename in enumerate(files):

        # read in and convert image
        image_color = imageio.imread(filename)
        image = rgb_to_bw(image_color)
        
        if k % 20 == 0:
            
            print("[INFO] working on frame %i/%i" %
                  (k, len(files)))

        # set up AprilTag
        at_detector = pupil_apriltags.Detector(
            families="tag36h11",
            nthreads=1,
            quad_decimate=1.0,
            quad_sigma=0.0,
            refine_edges=1,
            decode_sharpening=0.25,
            debug=0
        )

        # process the image
        tag = at_detector.detect(image)

        # grab corner and center data
        try:
            # from the first (and hopefully stationary) frame determine
            # the size of the tag vertically
            if k == 0:
                corners = tag[0].corners
                bottom_left = corners[0]
                bottom_right = corners[1]
                top_right = corners[2]
                top_left = corners[3]

                left_height = bottom_left[1] - top_left[1]
                right_height = bottom_right[1] - top_right[1]

                avg_height_pixels = (left_height + right_height)/2

                pixel_size = tag_size/avg_height_pixels

            center = tag[0].center

            # convert pixel location to actual length in mm and store
            # in an array            
            center_horz[k] = pixel_size*center[0]
            center_vert[k] = pixel_size*center[1]


        except:
            # flag any troublesome frames
            print("[INFO] questionable frame at %s" % filename)
            missed_tags.append(k)

    # interpolate for potential missing frames
    for bad_idx in missed_tags:
        center_vert[bad_idx] = (center_vert[bad_idx - 1] +
                                center_vert[bad_idx + 1])/2
                  
    # write output file
    with open(output_file, "w") as f:
        for time, location in zip(time_array, center_vert):
            f.write("%f %f\n" % (time, location))
            
    print("[INFO] data successfully written to: %s" % output_file)
