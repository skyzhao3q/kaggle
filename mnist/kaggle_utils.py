import os
import glob
import random
import shutil

def createDir (dirPath):
    if not os.path.exists(dirPath):
        os.mkdir(dirPath)

def getSubDirListOf(dirPath):
    dirList = []
    for x in os.listdir(dirPath):
        xPath = dirPath + "/" + x
        """
        if not os.path.isabs(xPath):
            xPath = os.path.dirname(os.path.abspath(__file__)) + "/" + xPath
        """
        if os.path.isdir(xPath):
            dirList.append(x)
        else:
            print(x + " is not dir")
    return dirList

def getFileListOf(dirPath, ext):
    fileList = []
    for x in os.listdir(dirPath):
        if x.endswith('.' + ext) and not x.startswith('.'):
            fileList.append(x)
    return fileList

def createValDir(trainDirPath, valRatio, valDirPath):
    # get subdirs
    dirList = getSubDirListOf(trainDirPath)
    print(len(dirList))
    # create dirs
    for i in range(len(dirList)):
        if not dirList[i].startswith('.'):
            dirPath = trainDirPath + "/" + dirList[i]
            # get files
            fileList = getFileListOf(dirPath, 'jpg')
            # create valfile list
            valFilseSum = (int)(valRatio * len(fileList))
            random.shuffle(fileList)
            valFileList = fileList[:valFilseSum]
            # create category dir
            catDirPath = valDirPath + "/" + dirList[i]
            createDir(catDirPath)
            # move files
            for j in range(len(valFileList)):
                srcPath = trainDirPath + "/" + dirList[i] + "/" + valFileList[j]
                dstPath = valDirPath + "/" + dirList[i] + "/" + valFileList[j]
                #shutil.move(srcPath, dstPath)
            print(str(dirList[i]) + ": " + str(len(valFileList)))

def countFilesOf(dirPath):
    # get subdirs
    dirList = getSubDirListOf(trainDirPath)
    print(len(dirList))
    # create dirs
    count = 0
    for i in range(len(dirList)):
        if not dirList[i].startswith('.'):
            dirPath = trainDirPath + "/" + dirList[i]
            # get files
            fileList = getFileListOf(dirPath, 'jpg')
            print(str(dirList[i]) + ": " + str(len(fileList)))
            count += len(fileList)
    return count

if __name__=="__main__":
    trainDirPath = "data/train"
    valRatio = 0.2
    valDirPath = "data/val"
    createValDir(trainDirPath, valRatio, valDirPath)
    print(countFilesOf(trainDirPath))
    print(countFilesOf(valDirPath))