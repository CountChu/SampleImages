#
# FILENAME.
#       Util.py - Utility Module.
#
# FUNCTIONAL DESCRIPTION.
#       The module provide app with API.
#
# NOTICE.
#       Author: visualge@gmail.com (CountChu)
#       Created on 2019/4/24
#

#
# Include standard packages.
#

import os
import shutil
import pdb
import logging

#
# Include specific packages.
#

#
# It gets dict from baseNameList so that th key is the first part of the base name.
#

def getBaseNameDict(baseNameList):
    baseNameDict = {}
    for bn in baseNameList:
        id = os.path.splitext(bn)[0]
        id = int(id)
        baseNameDict[id] = bn
    return baseNameDict

def getIdxList(total, rate):
    print('total = %d' % total)
    print('rate = %d' % rate)

    sampleCount = int(total * rate / 100)
    interval = int(total / sampleCount)
    print('interval = %d' % interval)
    print('sampleCount = %d' % sampleCount)

    idxList = []
    for i in range(sampleCount + 1):
        idx = int(interval * i)
        if idx >= total:
            break
        idxList.append(idx)
    #pdb.set_trace()
    logging.info('len(idxList) = %d' % len(idxList))
    logging.info('idxList[:10] = %s' % idxList[:10])
    return idxList, interval

def getPartitionList(idxList, interval, total):
    partList = []
    for i in range(interval):
        part = []
        for idx in idxList:
            if (idx + i) >= total:
                break
            part.append(idx + i)
        partList.append(part)
    logging.info('partList[0][:10] = %s' % partList[0][:10])
    logging.info('partList[1][:10] = %s' % partList[1][:10])

    #
    # Check partList.
    #

    count = 0
    for part in partList:
        count += len(part)
    if count != total:
        print('Error. count = %d, total = %d' % (count, total))
        sys.exit(0)
    #pdb.set_trace()

    return partList

def samplingKeys(idList, idxList):

    idPartList = []
    for idx in idxList:
        id = idList[idx]
        idPartList.append(id)

    return idPartList

def copyFiles(keyList, baseNameDict, dir, outputDir, check):

    if not os.path.exists(outputDir):
        if check:
            print('Will create the directory.')
        else:
            print('Create the directory.')
        print(outputDir)

        if not check:
            os.mkdir(outputDir)

    if check:
        #print('')
        print('Will copy files from: %s' % dir)
        print('                  to: %s' % outputDir)

    if not check:
        for key in keyList:
            bn = baseNameDict[key]
            fromFn = os.path.join(dir, bn)
            toFn = os.path.join(outputDir, bn)
            logging.info('Copy %s %s' % (fromFn, toFn))
            shutil.copyfile(fromFn, toFn)
