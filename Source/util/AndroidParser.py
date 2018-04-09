# -*- coding: UTF-8 -*-

import re
import os
import ModelUtil
from ModelUtil import PropertyTypes

pclass = lambda title : 'public class %s {'%(title)
pproperty = lambda type, name, comment : '    public %s %s;//%s'%(type, name, comment)

prefix = ''
suffix = 'Entity'


objcTypeDict = {
    PropertyTypes.Bool : (pproperty, 'boolean'),
    PropertyTypes.Int : (pproperty, 'int'),
    PropertyTypes.Long : (pproperty, 'long'),
    PropertyTypes.Point : (pproperty, 'double'),
    PropertyTypes.String : (pproperty, 'String'),
}

#支持正则
propertyFilters = [
    '~~(.+)~~',
]

def parse(filePath) :
    results = []
    results.append('package com.netease.meixue.data.entity;')

    lines = ModelUtil.readFile(filePath)

    #类名
    fileName = os.path.basename(filePath)
    className = os.path.splitext(fileName)[0]
    title = ModelUtil.titleParser(lines[0])
    if title :
        className = title
    if not re.search('[A-Z]+', className) :
        className = className.title()#如果全是小写，标题化
    className = className[0].upper() + className[1:len(className)]#首字母大写
    className = prefix + className + suffix
    results.append(pclass(className))

    #字段
    for line in lines :
        if ModelUtil.isTableLine(line) :
            eles = ModelUtil.lineParser(line)
            if not eles :
                continue

            propertyName = eles[0].strip()
            originType = eles[1].strip()
            comment = eles[2]

            #过滤被注释字段
            hit = False
            for filter in propertyFilters :
                if re.search(filter, propertyName) :
                    hit = True
                    break
            if hit :
                continue

            #类型解析
            typeResult = ModelUtil.typeParser(originType)
            type = typeResult[0]
            typeName = typeResult[1]
            level = typeResult[2]

            result = None
            #预设类
            if type in objcTypeDict.keys() :
                objcTypeResult = objcTypeDict[type]
                regex = objcTypeResult[0]
                objcType = objcTypeResult[1]
                result = regex(objcType, propertyName, comment)
            #列表
            elif type == PropertyTypes.List :
                contentType = None
                if typeName :
                    contentType = prefix + typeName + suffix
                if not contentType:
                    listType = 'List'
                else :
                    listType = 'List<'+contentType+'>'
                for i in range(1, level - 1) :
                    listType = 'List<'+listType+'>'
                result = pproperty(listType, propertyName, comment)
            #自定义类
            elif type == PropertyTypes.Custom :
                finalType = prefix + typeName + suffix
                result = pproperty(finalType, propertyName, comment)
            if result :
                results.append(result)
    results.append("\n}")
    return (className, results)

def export(folderPath, name, contents) :
    folderPath = os.path.join(folderPath, 'android')
    if not os.path.exists(folderPath) :
        os.makedirs(folderPath)
    hFile = folderPath + '/' + name + '.java'
    file = open(hFile, 'w+')
    for content in contents:
        file.write(content + '\n')
    file.close()
