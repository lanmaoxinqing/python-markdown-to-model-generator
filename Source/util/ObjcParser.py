# -*- coding: UTF-8 -*-

import re
import os
import ModelUtil
from ModelUtil import PropertyTypes

pinterface = lambda title : '@interface '+title+' : NSObject<YYModel> \n'
passign = lambda type, name, comment : '@property (nonatomic, assign) %s %s;//%s'%(type, name, comment)
pstrong = lambda type, name, comment : '@property (nonatomic, strong) %s *%s;//%s'%(type, name, comment)

prefix = 'MZ'
suffix = ''

objcTypeDict = {
    PropertyTypes.Bool : (passign, 'BOOL'),
    PropertyTypes.Int : (passign, 'NSInteger'),
    PropertyTypes.Long : (passign, 'NSInteger'),
    PropertyTypes.Point : (passign, 'double'),
    PropertyTypes.String : (pstrong, 'NSString'),
}

#支持正则
propertyFilters = [
    '~~(.+)~~',
]

def parse(filePath) :
    results = []
    lines = ModelUtil.readFile(filePath)
    #类名
    fileName = os.path.basename(filePath)
    className = os.path.splitext(fileName)[0]
    title = ModelUtil.titleParser(lines[0])
    # if title :
    #     className = title
    if not re.search('[A-Z]+', className) :
        className = className.title()#如果全是小写，标题化
    className = className[0].upper() + className[1:len(className)]#首字母大写
    className = prefix + className + suffix
    headerLine = pinterface(className)
    results.append(headerLine)

    for line in lines :
        #字段
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

            header = None
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
                    header = '#import "'+ contentType +'.h"'
                if not contentType:
                    listType = 'NSArray'
                else :
                    listType = 'NSArray<'+contentType+' *>'
                for i in range(1, level - 1) :
                    listType = 'NSArray<'+listType+' *>'
                result = pstrong(listType, propertyName, comment)
            #自定义类
            elif type == PropertyTypes.Custom :
                finalType = prefix + typeName + suffix
                header = '#import "'+ finalType +'.h"'
                result = pstrong(finalType, propertyName, comment)

            if header :
                results.insert(0, header)
            if result :
                results.append(result)
    results.append("\n@end")
    return (className, results)

def export(folderPath, name, contents) :
    folderPath = os.path.join(folderPath, 'iOS')
    if not os.path.exists(folderPath) :
        os.makedirs(folderPath)
    hFile = folderPath + '/' + name + '.h'
    file = open(hFile, 'w+')
    for content in contents:
        file.write(content + '\n')
    file.close()

    mFile = folderPath + '/' + name + '.m'
    file = open(mFile, 'w+')
    file.write('#import "'+name+'.h"\n\n')
    file.write('@implementation ' + name + '\n\n')
    file.write('@end\n')
    file.close()
