# SampleImages
The Python application [SampleImages.py](SampleImages.py) samples or partitions images from a directory by a given rate.

## Usage
```
usage: SampleImages.py [-h] [-v] [--log LOGFN] [-o OUTPUTDIR] -r RATE [-p]
                       [-c]
                       dir

The app samples or partitions images from a directory by a given rate.

Usage 1: python SampleImages.py Test -r 2

    It samples images from the directory Test in the rate 2%.
    It outputs Test#s-r2

Usage 2: python SampleImages.py Test -r 2 -p

    It partitions images from the directory Test in the rate 2%.
    It outputs:
        Test#s-r2-p00
        Test#s-r2-p01
        ... ...

Usage 3: python SampleImages.py Test -r 2 -p -c

    It checks the Usage 2. It doesn't output.

positional arguments:
  dir           A directory that contains files

optional arguments:
  -h, --help    show this help message and exit
  -v            Verbose log
  --log LOGFN   A name of a log file.
  -o OUTPUTDIR  A directory that contains output results
  -r RATE       Input rate (1-99)
  -p            Partition the samples.
  -c            Check means no output.
```
