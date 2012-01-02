'''
Created on 2011/12/13

@author: EE
'''
from src.lib.BeautifulSoup import BeautifulSoup
import urllib2
import re
import codecs
import os

startId = 5122
endId   = 7725

siteUrl = "http://lyrics.oiktv.com/"
lyricsDbPath = "../../resources/lyrics2/"

def fetchSong(url):
    try:
        #Get song info from url
        songInfo = {}
        _get = url.split('?')[1]
        tokens = _get.split('&')
        for token in tokens:
            toks = token.split('=')
            songInfo[toks[0]] = int(toks[1])
        #print songInfo
        
        #fetch the html
        lyricsWeb = urllib2.urlopen(url)  
        webContent = lyricsWeb.read()  
        lyricsWeb.close()       
    
        soup = BeautifulSoup(webContent)
    
        lyrics = soup.findAll(id="mylrc")[0].contents
        author = soup.findAll(attrs={'class' : 'link_hb'})[0].contents
        album = soup.findAll(attrs={'class' : 'link_hb'})[1].contents
        title = soup.findAll(attrs={'class' : 'link_hb'})[2].contents
    
        #write to an xml file    
        xml = "<?xml version=\"1.0\" encoding=\"UTF-8\" ?>\n" + "<xml>\n" + "<doc>\n"
        xml += "<sid>" + str(songInfo[u'sid']) + "</sid>\n"
        xml += "<aid>" + str(songInfo[u'aid']) + "</aid>\n"
        xml += "<lid>" + str(songInfo[u'lid']) + "</lid>\n"
        xml += "<title>"
        for w in title:
            xml += w 
        xml += "</title>\n"
        xml += "<author>"
        for w in author:
            xml += w 
        xml += "</author>\n"
        xml += "<lyrics>\n"
        for s in lyrics:
            for w in s:
                xml += w
        xml += "</lyrics>\n"
        xml += "</doc>\n"
        xml += "</xml>\n"
        
        #write into db    
        filename = lyricsDbPath + str(songInfo['lid']) + ".txt"
        f = codecs.open(filename, 'w', 'utf-8')
        f.write(xml)
        f.close()
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
            
    if len(wantedPages) > 1:
        maxPageNum = 1 #Max 1 page for each singer
        pageNum = 0
        for url in wantedPages:
            pageNum += 1
            if pageNum > maxPageNum:
                break
            print url
            
            lyricsWeb = urllib2.urlopen(url)  
            webContent = lyricsWeb.read()  
            lyricsWeb.close()
            
            maxSongNum = 50
            songNum = 0            
            ahref = soup.findAll('a', attrs={'class' : 'link_04'})
            for a in ahref:
                songNum += 1
                if songNum > maxSongNum:
                    break
                print songNum
                lyricsUrl = siteUrl + a['href']                
                fetchSong(lyricsUrl)
                
