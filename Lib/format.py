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
        sys.path.append('.')
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

def fontsJson(install, filename):
    
    content = {"fonts": {filename: { "path": filename + ".json", "container": "<i class='icon ion-*****'></i>"} } }
    
    f = open(install + '/fonts.json', 'wb')
    f.write(json.dumps(content))
    f.close()
    
def cpttf(install, ttfPath, filename):
    t = install + '/ttf-files/'
    if os.path.isdir(t):
        shutil.rmtree(t)
    os.mkdir(t)
    shutil.copy(ttfPath, t)
    
def ttfJson(install, ttfPath, filename):
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
    
    t = install + '/bundle'
    if os.path.isdir(t) == False:
        os.mkdir(t)
    f = open(t + '/' + filename + '.json', 'wb')
    f.write(json.dumps({'icons': contents}))
    f.close()

if __name__ == "__main__":
    args = sys.argv
    
    install = args[1]
    
    if os.path.isdir(install + '/bundle'):
        shutil.rmtree(install + '/bundle')
    if os.path.isdir(install + '/ttf-files'):
        shutil.rmtree(install + '/ttf-files')

    for i in range(2, len(sys.argv)):
        ttfPath = args[i]
        filename = str(os.path.split(os.path.splitext(ttfPath)[0])[1])
        fontsJson(install, filename)
        cpttf(install, ttfPath, filename)
        ttfJson(install, ttfPath, filename)
    print('全部制作完成，导出目录: %s' % install)
