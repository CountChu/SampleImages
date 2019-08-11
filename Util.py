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
    
def samplingKeys(keyList, rate):
    keyList.sort()
    total = len(keyList)
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
    print('len(idxList) = %d' % len(idxList))
    
    newKeyList = []
    for idx in idxList:
        key = keyList[idx]
        newKeyList.append(key)
    
    return newKeyList
    
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
        print('')
        print('Will copy files from')
        print(dir)
        print('to')
        print(outputDir)
        
    if not check:
        for key in keyList:
            bn = baseNameDict[key]
            fromFn = os.path.join(dir, bn)
            toFn = os.path.join(outputDir, bn)
            print('Copy %s %s' % (fromFn, toFn))
            shutil.copyfile(fromFn, toFn)
    