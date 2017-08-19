from datetime import datetime

import requests
import shutil
import sys
import re
import os

import urllib3
urllib3.disable_warnings()

#subject = "is214"
#baseUrl = "https://live.uia.no/live/ngrp:{0}_all/".format(subject)
baseUrl = "https://httpcache0-47115-httpcache0.dna.qbrick.com/47115-cachelive0/21/0/hls/nrk1/"
#baseUrl = "https://nrk-live-no.telenorcdn.net/21/0/hls/nrk1/playlist.m3u8"
#baseUrl = "https://nrk-nrk2.akamaized.net/22/0/hls/nrk2/"

def getStream(url, stremState=False):
	return requests.get(url, stream=stremState, verify=True)

resolution = re.findall(re.compile(ur'(RESOLUTION=\d{1,4}x\d{1,4})'), getStream(baseUrl+"playlist.m3u8").text)
fps = re.findall(re.compile(ur'(FRAME-RATE=\d{2})'), getStream(baseUrl+"playlist.m3u8").text)

def dotTS_merger(fileName):
	dotTS = []
	unSorted = []
	
	# only used to testing the lists to see that it's in the rigth order
	elements = os.listdir(os.getcwd())
	for elem in elements:
		if elem.endswith(".ts"):
			dotTS.append(elem)
			unSorted.append(elem)
			sSortedList = sorted(dotTS)

	for k, v in enumerate(unSorted):
		if v == sSortedList[k]:
			#return "O.K!"
			continue

		else:
			print "Does not look good, make issue at github."
			break

			#something is not rigth here...
	with open(fileName+'.ts', 'wb') as filename:
		for vids in sSortedList:
			print vids
			with open(vids, 'rb') as mergeFile:
				shutil.copyfileobj(mergeFile, filename)

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
				with open(urls[:37], 'wb+') as file:						
					shutil.copyfileobj(getStream("/".join(baseUrl.split('/')[:8])+"/"+urls, True).raw, file)
				print "{:s}".format(urls)

try:
	if getStream(baseUrl+"playlist.m3u8").status_code == 200:
		
		try:
			m3u8_parser()

		except TypeError:
			print "Avaliable Stream Quality"
			for k,v in enumerate(resolution):
				print "{0} {1} - {2}".format(k,v, fps[k])

	else:
		print "something fucked up"
		sys.exit(1)
except KeyboardInterrupt: #so it will start merging what it downloaded so far, and then delete the other files.
	dotTS_merger()
