#
# FILENAME.
#       SampleImages.py - Sample Images Python Application.
#
# FUNCTIONAL DESCRIPTION.
#       The app samples or partitions images from a directory by a given rate.
#
# NOTICE.
#       Author: visualge@gmail.com (CountChu)
#       Created on 2019/8/5
#

#
# Include standard packages.
#

import argparse
import logging
import pdb
import os
import json
import sys

#
# Include specific packages.
#

import Util

#
# Build argument parser and return it.
#

def buildArgParser():

    desc = '''
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

'''

    parser = argparse.ArgumentParser(
                formatter_class=argparse.RawTextHelpFormatter,
                description=desc)

    #
    # Standard arguments
    #

    parser.add_argument(
            "-v",
            dest="verbose",
            action='store_true',
            help="Verbose log")

    parser.add_argument(
            '--log',
            dest='logFn',
            help='A name of a log file.')

    #
    # Anonymous arguments.
    #

    parser.add_argument(
            'dir',
            help='A directory that contains files')

    #
    # Specific arguments
    #

    parser.add_argument(
            '-o',
            dest='outputDir',
            help='A directory that contains output results')

    parser.add_argument(
            "-r",
            type=int,
            required=True,
            dest="rate",
            help="Input rate (1-99)")

    parser.add_argument(
            "-p",
            dest="partition",
            action='store_true',
            help="Partition the samples.")

    parser.add_argument(
            "-c",
            dest="check",
            action='store_true',
            help="Check means no output.")

    return parser

def readConfig(jsonFn):
    if not os.path.exists(jsonFn):
        return None

    f = open(jsonFn, 'r')
    lines = f.readlines()
    jsonStr = ''.join(lines)
    jsonObj = json.loads(jsonStr)
    f.close()

    return jsonObj

#
# It reads file content into lines.
#

def readFileContent(fn):

    if not os.path.exists(fn):
        print('Error! The file is not found.')
        print(fn)
        sys.exit(0)

    f = open(fn, 'r')
    lines = f.readlines()
    f.close()

    return lines

#
# It reads base names in the dir directory.
#

def readBaseNames(dir):
    baseNameList = []
    if not os.path.exists(dir):
            print('Error! The directory is not found.')
            print(dir)
            sys.exit(0)

    for fn in os.listdir(dir):
        path = os.path.join(dir, fn)
        if not os.path.isdir(path):
            baseNameList.append(fn)

    return baseNameList

def main():

    #
    # Parse arguments
    #

    args = buildArgParser().parse_args()

    #
    # Enable log if -v
    #

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG, format='%(message)s')
    logging.info(args)

    #
    # Check arguments.
    #

    #
    # Open a log file if --log
    #

    if args.logFn != None:
        logF = open(args.logFn, 'w')

    '''
    #
    # Read config.
    #

    jsonFn = 'CommandApp.json'
    jsonObj = readConfig(jsonFn)

    #
    # Override args
    #

    if jsonObj != None:
        if 'default' in jsonObj:
            if 'dir' in jsonObj['default']:
                if args.dir is None:
                    args.dir = jsonObj['default']['dir']
                    print('Override dir = %s' % args.dir)
            if 'outputDir' in jsonObj['default']:
                if args.outputDir is None:
                    args.outputDir = jsonObj['default']['outputDir']
                    print('Override outputDir = %s' % args.outputDir)
    '''

    #
    # Specify outputDir
    #

    if args.outputDir is None:
        args.outputDir = '%s#s-r%d' % (args.dir, args.rate)
        print('Specify outputDir = %s' % args.outputDir)

    #
    # Read file base names if -d.
    #

    baseNameList = []
    if 'dir' in args and args.dir != None:
        baseNameList = readBaseNames(args.dir)

    #
    # Here is core function.
    #

    baseNameDict = Util.getBaseNameDict(baseNameList)
    idList = list(baseNameDict.keys())
    idList.sort()
    total = len(idList)
    (idxList, interval) = Util.getIdxList(total, args.rate)
    partList = Util.getPartitionList(idxList, interval, total)

    if args.partition:
        count = len(partList)
    else:
        count = 1

    all = []
    for i in range(count):
        print('partition_%d[:10] = %s' % (i, partList[i][:10]))
        idPartList = Util.samplingKeys(idList, partList[i])
        for id in idPartList:
            if id in all:
                print('Error. Duplicated IDs.')
                sys.exit(0)
        all.extend(idPartList)
        logging.info('len(all) = %d' % len(all))
        if count == 1:
            outputDir = '%s' % (args.outputDir)
        else:
            outputDir = '%s-p%02d' % (args.outputDir, i)
        Util.copyFiles(idPartList, baseNameDict, args.dir, outputDir, args.check)
    #pdb.set_trace()

    #sampling(args.dir, baseNameDict, args.outputDir, args.rate)
    #Util.handle(args.file, args.dir, baseNameList, args.outputDir)

    #
    # Close the log file if --log
    #

    if args.logFn != None:
        logF.close()

if __name__ == '__main__':

    main()
