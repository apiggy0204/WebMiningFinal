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

"""
Retrieve titles of the songs for reference
"""
refSongTitles = []
root = tree.getroot()
for list in root:
    theme = list[0].text
    #print theme
    
    if theme != None and re.search(query, theme, re.UNICODE):
        print theme
        for song in list:
            title = song.text
            if title != None and title != theme:
                refSongTitles.append(title)
                print '\t' + title                
                                
"""
get refSong's id and lyrics
"""
               
dbPath = res_path + 'lyrics2/' 
fSongs = os.listdir(dbPath)
for fSong in fSongs:
    try:
        xml = ET.parse(dbPath + fSong)
        root = xml.getroot()
        
        lyrics = root[0].findall('lyrics')[0].text
        author = root[0].findall('author')[0].text
        title = root[0].findall('title')[0].text
        sid = int(root[0].findall('sid')[0].text)
        lid = int(root[0].findall('lid')[0].text)
        
        for refTitle in refSongTitles:
            if title == refTitle:
                print lyrics
                break
        
    except:
        pass
        
