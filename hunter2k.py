import requests
import shutil
#import m3u8
import sys
import re

import urllib3
urllib3.disable_warnings()

#subject = "is214"
#baseUrl = "https://live.uia.no/live/ngrp:{0}_all/playlist.m3u8".format(subject)
baseUrl = "https://httpcache0-47115-httpcache0.dna.qbrick.com/47115-cachelive0/21/0/hls/nrk1/playlist.m3u8"

def getStream(url, stremState=False):
	return requests.get(url, stream=stremState)

def chunklist(url): #only used to get the chuks 
	return re.findall(re.compile(ur'chunklist_[^.]+'), getStream(baseUrl).text)

def m3u8_parser(segments=""):
	playlist = re.findall(re.compile(ur'#EXT-X-STREAM-INF:[A-Z=0-9,\"x\-.a-z \r\n#_]+'), getStream(baseUrl).text)
	for entry in playlist:
		if "1280x720" in entry and "50" in entry:	
			segments = entry.split(',')[4].replace('mp4a.40.2"','').replace('#EXT-X-STREAM-INF','').strip() #going to switch out the replace statements with regex later.. just want to get this shit running
			segmentsUrls = "/".join(baseUrl.split('/')[:8])+"/"+segments
			tsUrls = getStream(segmentsUrls).text.replace('\n','\r')
			tsFiles = re.findall(re.compile(ur'([0-9-]+.ts\?version_hash=\d+\w{2})'), tsUrls)
			for urls in tsFiles:
				print urls




print m3u8_parser()

# this is what we want ...
#EXT-X-STREAM-INF:BANDWIDTH=5160000,RESOLUTION=1280x720,FRAME-RATE=50.000,CODECS="avc1.640020,mp4a.40.2"
#1709241829-123787468-prog_index.m3u8
#EXT-X-STREAM-INF:BANDWIDTH=64000,CODECS="mp4a.40.2"
#1380275607-1380275607-prog_index.m3u8

# test stream
# https://httpcache0-47115-httpcache0.dna.qbrick.com/47115-cachelive0/21/0/hls/nrk1/playlist.m3u8?b=500-3500&__b__=1428&__a__=off
"""while streamLive:
	with open(subject+".mp4", 'wb+') as file:	
	    shutil.copyfileobj(getStream(baseUrl, True).raw, file)
	print "{:s}".format(chunklist(baseUrl))"""
