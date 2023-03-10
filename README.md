# ENGR 2240 Mass Tracker

This program uses AprilTags to track a mass on a spring of a knock Hooke's constant.

## Required software

To run this program you will need Python 3.X will need the AprilTag Python bindings from Pupil Labs.  This package is regularly maintained and can be easily installed through PyPi.

```
pip install pupil-apriltags
```

## Running the code

This code has a fairly straightfoward command-line interface.  You can find a help section using a `-h` flag.

```bash
$ python mass_tracker.py -h
usage: mass_tracker.py [-h] -i INPUT_DIRECTORY [-o OUTPUT_FILE] [-t SAMPLE_PERIOD] [--tag_size TAG_SIZE]

computes the location of the mass on a spring

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_DIRECTORY, --input_directory INPUT_DIRECTORY
                        directory of tiff images
  -o OUTPUT_FILE, --output_file OUTPUT_FILE
                        output text file with time stamps and locations
  -t SAMPLE_PERIOD, --sample_period SAMPLE_PERIOD
                        time between image frames in seconds (default is 0.04 s
  --tag_size TAG_SIZE   size of AprilTag vertically in mm (default is 20 mm)
```
Most of the arguments are optional have a default value if you ommit them.  The exception is the `--input_directory` option.  

Successful usage of the code looks like the following:
