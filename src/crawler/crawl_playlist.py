#-*- coding: utf-8 -*-
'''
Created on 2011/12/28

@author: EE
'''
from src.lib.BeautifulSoup import BeautifulSoup
import urllib2
import codecs
import re
import elementtree.ElementTree as ET

siteUrl = "http://www.ptt.cc"

"""
def writeToXML(playlists):
    f = codecs.open('query.xml', 'w', 'utf-8')
    xml = "<?xml version=\"1.0\" encoding=\"UTF-8\" ?>\n"
    xml += "<xml>\n"
    
    
    for key in playlists.keys():
        xml += "<theme>\n"
        xml += "<title>"
        xml += key
        xml += "</title>\n"
        
        for song in playlists[key]:
            xml += "<song>"
            xml += song
            xml += "</song>\n"
            
        xml += "</theme>\n\n"        
    
    xml += "</xml>"
    
    f.write(xml)
    f.close()
"""

def appendToXML(playlists):
    tree = ET.parse("query.xml")
    
    #root = ET.Element("xml")
    root = tree.getroot()
    
    for key in playlists.keys():
        list = ET.SubElement(root, "list")
        theme = ET.SubElement(list, "theme")
        theme.text = key
        for s in playlists[key]:
            song = ET.SubElement(list, "song")
            song.text = s
    
    tree = ET.ElementTree(root)
    tree.write("query.xml", "utf-8")
    
def getPlaylists(text):
    
    playlists = {}
    lines = text.split('\n')
    theme = ''
    for line in lines:
        
        if(re.match(u'題組', line, re.UNICODE)):
            if len(line.split(u'：')) != 2:
                continue
            firstLine = line.split(u'：')[1]
            #print firstLine
            tokens = firstLine.split(u'■')
            if len(tokens)!=2:
                tokens = firstLine.split(u'□')
            if len(tokens)!=2:
                continue
            theme = tokens[0]
            print "THEME: ", theme
            playlists[theme] = []
            songTitle = tokens[1].split('(')[0]
            print songTitle
            playlists[theme].append(songTitle)
        
        elif(re.match(u' *[■□]', line ,re.UNICODE)):
            line = line.strip().strip(u'■').strip(u'□')
            tokens = line.split('(')
            songTitle = tokens[0]
            print songTitle
            playlists[theme].append(songTitle)
    """    
    for key in playlists.keys():
        print "key", key
        for song in playlists[key]:
            print "song", song
    """
    return playlists           
    

def fetchPlaylist(url):
    
    web = urllib2.urlopen(url)
    webContent = web.read()
    web.close()

    soup = BeautifulSoup(webContent)
    text = soup.pre.contents[0]
    playlists = getPlaylists(text)
    appendToXML(playlists)
    
for i in range(1, 59):
    url = "http://www.ptt.cc/bbs/Million_star/index" + str(i) + ".html"
    pttweb = urllib2.urlopen(url)  
    webContent = pttweb.read()  
    pttweb.close()  
    
    soup = BeautifulSoup(webContent)
    ahrefs = soup.findAll('a')
    for a in ahrefs:
        result1 = re.search("bbs/Million_star/M", a['href'])    
        if result1 != None:                
            result2 = re.search(u'歌庫', a.contents[0], re.UNICODE)
            if result2 != None:
                url = siteUrl + a['href']
                print url
                fetchPlaylist(url)
             
            
            #print url, a.contents[0]
           
#print url


