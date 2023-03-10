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

```
$ python mass_tracker.py -i 1kg_freedrop_test1_skip2_50seconds_C001H001S0001/ -o location_data.txt
[INFO] working on frame 0/1256
[INFO] working on frame 20/1256
[INFO] working on frame 40/1256
...
[INFO] working on frame 1220/1256
[INFO] working on frame 1240/1256
[INFO] data successfully written to: location_data.txt
```
The `location_data.txt` file looks like:
```
0.000000 116.502752
0.040000 116.508991
0.080000 116.493535
0.120000 116.415520
0.160000 116.327529
...
```
where the first column are the time stamps in seconds and the second column is the vertical location.  The top of the image is referenced to be 0 mm and any movement downward will be some positive distance in millimeters.  

## Potential issues

If the software fails to detect the AprilTag, you will be notified.  If you are missing a frame but the adjacent frames are detected, the system will use a linear interpolation to fill in the missing data.  However, if you are misisng multiple frames in a row the interpolation will fail.  In this scenario you should consider redoing the experiment and gather more data.

