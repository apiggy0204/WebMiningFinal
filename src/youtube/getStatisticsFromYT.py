# -*- coding: utf-8 -*-
'''
Created on 2012/1/2

@author: EE
'''
from src.lib.BeautifulSoup import BeautifulSoup
import urllib2
import elementtree.ElementTree as ET

 
youtube = 'http://gdata.youtube.com/feeds/api/videos?v=2&max-results=1&q='
query = u'孤獨患者'

web = urllib2.urlopen("http://gdata.youtube.com/feeds/api/videos?v=2&q=%E9%99%B3%E5%A5%95%E8%BF%85&max-results=1")
content = web.read()
web.close()

soup = BeautifulSoup(content)
stats = soup.findAll('yt:statistics')

print stats[0]['viewcount']
