#!/usr/bin/python
#-*- coding: UTF-8 -*-

import sys
import os
import json
import shutil

try:
    from fontTools.ttLib import TTFont, TTLibError, newTable
    from fontTools.ttLib.tables.otTables import *
except:
    try:
        sys.path.append('/Users/FDD/.jenkins/workspace/lib/fonttools/Lib')
        import fontTools
        from fontTools.ttLib import TTFont, TTLibError, newTable
        from fontTools.ttLib.tables.otTables import *
    except:
        print("Install https://github.com/behdad/fonttools/archive/master.zip \n OR `pip install fonttools`")
        sys.exit(1)

def unicode2Hex(unicode):
    hexUnicode = '%X'.lstrip('0x') % unicode
    str = '0' * (4 - len(hexUnicode)) + hexUnicode
    return str

def fontsJson(filename):
    
    content = {"fonts": {filename: { "path": filename + ".json", "container": "<i class='icon ion-*****'></i>"} } }
    
    f = open('./fonts.json', 'wb')
    f.write(json.dumps(content))
    f.close()
    
def cpttf(ttfPath, filename):
    t = './ttf-files/'
    if os.path.isdir(t):
        shutil.rmtree(t)
    os.mkdir(t)
    shutil.copy(ttfPath, t)
    
def ttfJson(ttfPath, filename):
    try:
        ttx = TTFont(ttfPath)
    except TTLibError:
        print("Cannot open %s" % ttfPath)
        sys.exit(1)

    unicodes = {}
    for table in ttx['cmap'].tables:
        unicodes.update(table.cmap)

    contents = []
    for key,value in unicodes.items():
        content = {}
        content['name'] = value
        content['id'] = str(key)
        content['created'] = 1
        content['unicode'] = unicode2Hex(key)
        contents.append(content)
    
    t = './bundle'
    if os.path.isdir(t) == False:
        os.mkdir(t)
    f = open(t + '/' + filename + '.json', 'wb')
    f.write(json.dumps({'icons': contents}))
    f.close()

if __name__ == "__main__":
    args = sys.argv
    
    ttfPath = args[1]
    filename = str(os.path.split(os.path.splitext(ttfPath)[0])[1])
    print('开始制作 %s ...' % filename)
    fontsJson(filename)
    cpttf(ttfPath, filename)
    ttfJson(ttfPath, filename)
    print('%s 制作完成 ～' % filename)