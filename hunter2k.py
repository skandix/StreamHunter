import requests
import shutil
import sys
import re

import urllib3
urllib3.disable_warnings()

#subject = "is214"
#baseUrl = "https://live.uia.no/live/ngrp:{0}_all/playlist.m3u8".format(subject)
#baseUrl = "https://httpcache0-47115-httpcache0.dna.qbrick.com/47115-cachelive0/21/0/hls/nrk1/playlist.m3u8"
#baseUrl = "https://nrk-live-no.telenorcdn.net/21/0/hls/nrk1/playlist.m3u8"
baseUrl = "https://nrk-nrk2.akamaized.net/22/0/hls/nrk2/"

def getStream(url, stremState=False):
	return requests.get(url, stream=stremState, verify=True)

resolution = re.findall(re.compile(ur'(RESOLUTION=\d{1,4}x\d{1,4})'), getStream(baseUrl+"playlist.m3u8").text)
fps = re.findall(re.compile(ur'(FRAME-RATE=\d{2})'), getStream(baseUrl+"playlist.m3u8").text)

def chunklist(url): #only used to get the chuks 
	return re.findall(re.compile(ur'chunklist_[^.]+'), getStream(baseUrl).text)

def m3u8_parser(resolution,fps,debug=False):
	segments = ""
	playlist = re.findall(re.compile(ur'#EXT-X-STREAM-INF:[A-Z=0-9,\"x\-.a-z \r\n#_]+'), getStream(baseUrl+"playlist.m3u8").text)
	for entry in playlist:
		if resolution in entry and fps in entry:	
			segments = entry.split(',')[4].replace('mp4a.40.2"','').replace('#EXT-X-STREAM-INF','').strip() #going to switch out the replace statements with regex later.. just want to get this shit running
			segmentsUrls = "/".join(baseUrl.split('/')[:8])+segments
			tsUrls = getStream(segmentsUrls).text.replace('\n','\r')
			tsFiles = re.findall(re.compile(ur'([0-9-]+.ts\?version_hash=\d+\w{2})'), tsUrls)
			for urls in tsFiles:
				print urls
				### then download the shits..
				## then merge them, and convert to a mp4 file.
				# AND THEN it migth hopefully play

#			for urls in tsFiles:				
#				with open(urls[:37], 'wb+') as file:						
#					shutil.copyfileobj(getStream("/".join(baseUrl.split('/')[:8])+"/"+urls, True).raw, file)
#				print "{:s}".format(urls)

if getStream(baseUrl+"playlist.m3u8").status_code == 200:
	try:
		m3u8_parser(resolution[4], fps[4])

	except TypeError:
		print "Avaliable Stream Quality"
		for k,v in enumerate(resolution):
			print "{0} {1} - {2}".format(k,v, fps[k])
else:
	print "something fucked up"
	sys.exit(1)
