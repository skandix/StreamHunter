from datetime import datetime
import requests, shutil, sys, re, os

def UIA(subject:str) -> str:
	"""
	subject: str - is the course name one want to stream
	returns, a compiled string for watching the livestream of the course.

	note: i think this is not a correct generic url for uia's livestreams
	"""
	return (f"https://live.uia.no/live/ngrp:{subject}_all/")
	pass

baseUrl = "https://nrk-nrk2.akamaized.net/22/0/hls/nrk2/"
#baseUrl = "https://nrk-nrk1.akamaized.net/21/0/hls/nrk1/playlist.m3u8"

def getStream(url:str, stream:bool=False) -> str:
	if url.endswith('playlist.m3u8'):
		return requests.get(url, stream=stream)
	else:
		return requests.get(url+"playlist.m3u8", stream=stream)



resolution = re.findall(re.compile(r'(RESOLUTION=\d{1,4}x\d{1,4})'), getStream(baseUrl).text)
fps = re.findall(re.compile(r'(FRAME-RATE=\d{2})'), getStream(baseUrl).text)


def detect_encryption(url:str) -> str:

	# encryption method
	print(getStream(url).text)
	method = re.findall(re.compile(r'(METHOD=[^,]+)'), getStream(url).text)

	# The value is a quoted-string containing a URI that specifies how to obtain the key
	# This attribute is REQUIRED unless the METHOD is NONE.
	keyUri = re.findall(re.compile(r'(URI=[^,]+)'), getStream(url).text)

	# The value is a hexadecimal-sequence that specifies a 128-bit
	# unsigned integer Initialization Vector to be used with the key.
	# aa = 1 byte
	iv = re.findall(re.compile(r'(IV=\S+)'), getStream(url).text)
	return "{0} \n{1} \n{2}".format(method, keyUri, iv)



def dotTS_merger(fileName:str):
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
		print(k,v)
		if v == sSortedList[k]:
			#return "O.K!"
			continue

		else:
			print ("Does not look good, make issue at github.")
			break

			#something is not rigth here...
	with open(fileName+'.ts', 'wb') as filename:
		for vids in sSortedList:
			print (vids)
			with open(vids, 'rb') as mergeFile:
				shutil.copyfileobj(mergeFile, filename)

def decryptDownloads(url:str ):
	"""
	Use pycrypto to encrypt the content inside the .ts files.
	then just download with 
	
	with open(urls[:37], 'wb+') as file:						
		shutil.copyfileobj(getStream("/".join(baseUrl.split('/')[:8])+"/"+urls, True).raw, file)
	return "{:s}".format(urls)
	---
	#EXT-X-KEY:METHOD=AES-128,URI="keys/1.key",IV=0x865832653759693f5f5ad4df269caaad
	curl https://nrk-nrk1.akamaized.net/21/0/hls/nrk1/keys/1.key
	keys/1.key is appended on the baseURL without the playlist.m3u8 on the end
	loot = (requests.get("https://nrk-nrk1.akamaized.net/21/0/hls/nrk1/keys/1.key").text).encode('utf-8')
	print(loot.hex())

	this in acording to the IV is used to decrypt the stream

	"""
	pass

def download(urls:str ):
	with open(urls[:37], 'wb+') as file:						
		shutil.copyfileobj(getStream("/".join(baseUrl.split('/')[:8])+"/"+urls, True).raw, file)
	return "{:s}".format(urls)

def m3u8_parser(resolution:int ,fps:int) -> str:

	print(f"{getStream(baseUrl).text}\n\n")

	playlist = re.findall(re.compile(r'#EXT-X-STREAM-INF:([^\?]+)'), getStream(baseUrl).text)
	for entry in playlist:
		if resolution in entry and fps in entry:
			#print(entry)
			playlistEnd = re.findall(re.compile(r'([\d{,10}\-]+\-\w{,10}[\.m3u8]+)'),entry)[0]
			playlistStart = "/".join(baseUrl.split('/')[:8])
			playlistURL = playlistStart+playlistEnd
			print (playlistURL)
			print (detect_encryption(playlistURL))


			#tsUrls = getStream().text.replace('\n','\r')
			#tsFiles = re.findall(re.compile(r'([0-9-]+.ts\?version_hash=\d+\w{2})'), tsUrls)
			#for urls in tsFiles:
			#	print (urls)
			#	print (download(urls))
			

if __name__ == '__main__':
	try:
		if getStream(baseUrl).ok:
			
			try:
				m3u8_parser(resolution[-1], fps[-1])
				#m3u8_parser()

			except TypeError:
				print ("Avaliable Stream Quality")
				for idx, quality_string in enumerate(resolution):
					print (f"\t[{idx}] {quality_string} - {fps[idx]}")
				print ("Please select a quality profile")

		else:
			print ("something fucked up")
			sys.exit(1)
	except KeyboardInterrupt:
		print ("\n[+] Detected KeyboardInterrupt\nStarting Merging of .ts files\n")
		dotTS_merger(baseUrl)
