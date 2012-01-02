# -*- coding: utf-8 -*-
'''
Created on 2012/1/1

@author: EE
'''
import elementtree.ElementTree as ET
import codecs
import os
import re

query = u'分手'
res_path = '../../resources/'
tree = ET.parse(res_path + 'playlists2.xml')


#f = codecs.open('query_tf.txt', 'w', 'utf-8')

root = tree.getroot()
for list in root:
    theme = list[0].text
    #print theme
    
    if theme != None and re.search(query, theme, re.UNICODE) != None:
        print theme
        for song in list:
            title = song.text
            if title != theme:
                print '\t' + title
                
dbPath = res_path + 'lyrics2/' 
fSongs = os.listdir(dbPath)
for fSong in fSongs:
    try:
        xml = ET.parse(dbPath + fSong)
        root = xml.getroot()
        authors = root[0].findall('author')
        for author in authors:
            print author.text
        
    except:
        pass
        
