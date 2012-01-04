# -*- coding: utf-8 -*-
'''
Created on 2011/12/13

@author: EE
'''
from lib.BeautifulSoup import BeautifulSoup
import elementtree.ElementTree as ET
import urllib2
import re
import codecs
import os
from youtube.getStatisticsFromYT import getViewCount

startId = 3
endId   = 7725
minViewCount = 200000

siteUrl = "http://lyrics.oiktv.com/"
lyricsDbPath = "../../resources/lyrics_hot/"

def fetchSong(url, viewCount):
    try:
        #Get song info from url
        songInfo = {}
        _get = url.split('?')[1]
        tokens = _get.split('&')
        for token in tokens:
            toks = token.split('=')
            songInfo[toks[0]] = int(toks[1])
        
        #fetch the html
        lyricsWeb = urllib2.urlopen(url)  
        webContent = lyricsWeb.read()  
        lyricsWeb.close()       
    
        soup = BeautifulSoup(webContent)
    
        lyrics = soup.findAll(id="mylrc")[0].contents
        author = soup.findAll(attrs={'class' : 'link_hb'})[0].contents[0]
        album = soup.findAll(attrs={'class' : 'link_hb'})[1].contents[0]
        title = soup.findAll(attrs={'class' : 'link_hb'})[2].contents[0]    
        
        #print lyrics
        lyricsText = ''
        for line in lyrics:
            for t in line:
                lyricsText += t                       
        
        #Construct the xml
        root = ET.Element("xml")
        doc = ET.SubElement(root, "doc")
        
        sidNode = ET.SubElement(doc, "sid")
        sidNode.text = str(songInfo[u'sid'])
        aidNode = ET.SubElement(doc, "aid")
        aidNode.text = str(songInfo[u'aid'])
        lidNode = ET.SubElement(doc, "lid")
        lidNode.text = str(songInfo[u'lid'])        
        titleNode = ET.SubElement(doc, "title")
        titleNode.text = title
        authorNode = ET.SubElement(doc, "author")
        authorNode.text = author
        viewCountNode = ET.SubElement(doc, "viewCount")
        viewCountNode.text = str(viewCount)
        lyricsNode = ET.SubElement(doc, "lyrics")
        lyricsNode.text = lyricsText
        
                       
        #Construct the tree
        tree = ET.ElementTree(root)
        filename = lyricsDbPath + str(songInfo['lid']) + ".txt"        
        tree.write(filename, "utf-8")
        
    except:
        pass

########################start of main###################################

for i in range(startId, endId):
    
    url = "http://lyrics.oiktv.com/singer.php?sid=" + str(i)

    #lyricsWeb = urllib2.urlopen("http://lyrics.oiktv.com/singer.php?sid=51")  
    lyricsWeb = urllib2.urlopen(url)
    
    webContent = lyricsWeb.read()  
    lyricsWeb.close()  
    
    soup = BeautifulSoup(webContent)
    
    pages = soup.findAll('a')
    wantedPages = []
    for page in pages:        
        if re.search("&page=", page['href']):
            #print page['href']
            url = page['href']
            wantedPages.append(url)
            
    if len(wantedPages) > 1: #find those who has more than 20 albums    
        
        maxPageNum = 1 #Max 1 page for each singer
        pageNum = 0
        maxSongNum = 250
        songNum = 0  
        fetchNum = 0
        
        for url in wantedPages:
            pageNum += 1
            if pageNum > maxPageNum:
                break
            print url
            
            lyricsWeb = urllib2.urlopen(url)  
            webContent = lyricsWeb.read()  
            lyricsWeb.close()
            
                      
            ahref = soup.findAll('a', attrs={'class' : 'link_04'})
            for a in ahref:
                songNum += 1
                #if songNum <= 50:
                #    continue
                if songNum > maxSongNum:
                    break
                print songNum
                
                title = ''
                if len(a.contents) > 0:
                    for w in a.contents:
                        title += w
                if title != None and title != '':
                    viewCount = getViewCount(title)
                    if viewCount > minViewCount:
                        print title
                        print viewCount                        
                        lyricsUrl = siteUrl + a['href']
                        fetchSong(lyricsUrl, viewCount)
                        fetchNum += 1
        
        
        print 'fetched: ', fetchNum