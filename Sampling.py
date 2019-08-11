#
# FILENAME.
#       Sampling.py - Sampling Python Application.
#
# FUNCTIONAL DESCRIPTION.
#       The app samples from dataset by a given rate.
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

    parser = argparse.ArgumentParser(
                description='Build ...')
                
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
            "-c", 
            dest="check", 
            action='store_true',    
            help="Check means don't apply the changes.")                   

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
        args.outputDir = '%s#sample-r%d' % (args.dir, args.rate)
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
    keyList = Util.samplingKeys(list(baseNameDict.keys()), args.rate)
    Util.copyFiles(keyList, baseNameDict, args.dir, args.outputDir, args.check)
    
    #sampling(args.dir, baseNameDict, args.outputDir, args.rate)
    #Util.handle(args.file, args.dir, baseNameList, args.outputDir)
    
    #
    # Close the log file if --log
    #

    if args.logFn != None:
        logF.close()

if __name__ == '__main__':

    main()