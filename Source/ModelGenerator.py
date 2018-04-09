# -*- coding: UTF-8 -*-

import re

from util import ObjcParser,AndroidParser,ModelUtil
import sys
import os

folderPath = None
parserType = None

def checkArgs() :
    global folderPath
    global parserType
    if len(sys.argv) > 1 :
        arg = sys.argv[1]
        if (os.path.isdir(arg) or os.path.isfile(arg)) :
            folderPath = arg
        elif arg.isalnum() :
            parserType = arg

    if len(sys.argv) > 2 :
        arg = sys.argv[2]
        if (os.path.isdir(arg) or os.path.isfile(arg)) :
            folderPath = arg
        elif arg.isalnum() :
            parserType = arg

    if not folderPath :
        folderPath = os.getcwd()

    if not parserType :
        parserType = 1


def main(dir) :
    checkArgs()
    parser = None
    # print folderPath, parserType
    if (parserType == 1) :
        parser = ObjcParser
    else :
        parser = AndroidParser
    paths = ModelUtil.getFiles(folderPath)
    for path in paths :
        eles = parser.parse(path)
        name = eles[0]
        results = eles[1]
        for result in results :
            destPath = None
            if os.path.isfile(folderPath) :
                destPath = os.path.split(folderPath)[0]
            else :
                destPath = folderPath
            parser.export(destPath, name, results)
main(folderPath)
