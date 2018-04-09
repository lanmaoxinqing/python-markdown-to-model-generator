# -*- coding: UTF-8 -*-

import re
import os
import sys

def enum(**enums):
    return type('Enum', (), enums)


PropertyTypes = enum(
    Bool = 1,
    Int = 2,
    Long = 3,
    Point = 4,
    String = 5,

    List = 900,
    Custom = 999,
)


typeDict = {
    #要转换的名称         #转换后的名称 #替换所需表达式
    ('bool', 'boolean') : PropertyTypes.Bool,
    ('int', 'integer') : PropertyTypes.Int,
    ('long', 'long long') : PropertyTypes.Long,
    ('float', 'cgfloat', 'double') : PropertyTypes.Point,
    ('string') : PropertyTypes.String,
    ('list', 'array') : PropertyTypes.List,
}


def getFiles(path) :
    if os.path.isfile(path) :
        return [path]
    paths = []
    for (dirPath, dirNames, fileNames) in os.walk(path) :
        for fileName in fileNames :
            absolutePath = os.path.join(dirPath, fileName)
            if os.path.splitext(absolutePath)[1] == '.md' :
                paths.append(absolutePath)
    return paths


def readFile(filePath) :
    file = open(filePath)
    lines = file.readlines()
    return lines


def isTableLine(line) :
    global tableState
    pattern = re.compile('^((.+)\|)+((.+))$')
    if not pattern.match(line) :
        tableState = 0
        return False
    # print line
    #第一次匹配，表格头
    if tableState == 0 :
        tableState = 1
        return False
    #第二次匹配，表格排版
    if tableState == 1 :
        tableState = 2
        return False
    if tableState == 2 :
        return True


def titleParser(line) :
    title = re.search('^# (.+)$', line)
    if not title:
        return None
    titleStr = title.group(1).strip()
    if titleStr == 'Title' :
        return None
    return titleStr


def descParser(line) :
    pass


def lineParser(line) :
    params = line.split('|')
    if params[0].strip() == "" :
        params.pop(0)
    if params[-1].strip() == "" :
        params.pop(-1)
    # print len(params)
    #不是4行，不是属性表格
    if len(params) != 4 :
        return
    name = params[0].strip()
    #名字没字母
    if not re.search('\w+', name) :
        return
    type = params[2].strip()
    comment = params[3].strip()
    return (name, type, comment)



'''
    属性类型，属性名，列表层级
'''
def typeParser(originType, listLevel = 0) :
    typeStr = originType.strip().lower()
    #无类型，默认String
    if not typeStr :
        return (PropertyTypes.String, None, listLevel)
    #匹配列表[xxx]
    match = re.search('\[(.+)\]', typeStr)
    if match:
        subOriginType = match.group(1)
        subTypeResult = typeParser(subOriginType, listLevel + 1)
        subType = subTypeResult[1]
        currentListLevel = subTypeResult[2]
        return (PropertyTypes.List, subType, currentListLevel)

    #匹配列表list<xxx>
    match = re.search('list\<(.+)\>', typeStr)
    if match:
        subOriginType = match.group(1)
        subTypeResult = typeParser(subOriginType, listLevel + 1)
        subType = subTypeResult[1]
        currentListLevel = subTypeResult[2]
        return (PropertyTypes.List, subType, currentListLevel)
    #匹配列表array<xxx>
    match = re.search('array\<(.+)\>', typeStr)
    if match:
        subOriginType = match.group(1)
        subTypeResult = typeParser(subOriginType, listLevel + 1)
        subType = subTypeResult[1]
        currentListLevel = subTypeResult[2]
        return (PropertyTypes.List, subType, currentListLevel)

    #匹配预设字典
    for eles in typeDict.keys() :
        if typeStr in eles :
            return (typeDict[eles], None, listLevel)
    #自定义对象
    resultType = originType.strip()#默认不修改类型大小写
    if not re.search('[A-Z]+', resultType) :
        resultType = typeStr.title()#如果全是小写，标题化
    return (PropertyTypes.Custom, resultType, listLevel)
