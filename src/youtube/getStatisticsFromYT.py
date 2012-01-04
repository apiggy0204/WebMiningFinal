# -*- coding: utf-8 -*-
'''
Created on 2012/1/2

@author: EE
'''
from lib.BeautifulSoup import BeautifulSoup
import urllib2


def getViewCount(songTitle): 
    
    try:
        youtube = 'http://gdata.youtube.com/feeds/api/videos?v=2&max-results=1&q='
        #songTitle = urllib2.quote(songTitle)
        #print songTitle
        url = youtube + songTitle     
        #print url  
        
        web = urllib2.urlopen(url)
        content = web.read()
        web.close()
        
        soup = BeautifulSoup(content)
        stats = soup.findAll('yt:statistics')
        
        return int(stats[0]['viewcount'])

    except:
        return 0