'''
					::IMDB RATING FILE RENAMER::
							@achute  
TO DO:
1. Add a File called imdbrating.txt in the root directory with all the imdb ratings 
'''
import os
import json
import urllib.request
import sys
from urllib.parse import quote
from guessit import guess_file_info
print (str(sys.argv[1]))
if len(sys.argv) <=1:
	sys.exit()
rootDir=str(sys.argv[1])
movies_extension=["avi","mp4","mkv","mov"]
for dirName,subdirList,fileList in os.walk(rootDir):
	for fname in fileList:
		url="http://www.omdbapi.com/?t="
		year_info=False
		setForAll=False
		details = guess_file_info(fname)
		#print(details)
		if 'year' in details:
			#has the year info use it
			year_info=True
		#if(details['container'] in movies_extension):
		if 'container' in details:
			if details['container'] in movies_extension:
				if 'title' in details:
					print('\n For file : %s'%fname)
					if year_info:
						url = url + quote(details['title']) + "&y=" +quote(str(details['year']))
					else:
						url = url + quote(details['title'])
					f = urllib.request.urlopen(url)
					str_response = f.readall().decode('utf-8')
					data = json.loads(str_response)
					if 'imdbRating' not in data:
						break
					if year_info:
						print (details['title']+"("+data['Year']+")"+" ("+data['imdbRating']+") ."+details['container'])
					else:
						print (details['title']+" ("+data['imdbRating']+") ."+details['container'])
					if(setForAll==False)
						choice = input("\n Yes Change It ! (Y/N) \n Change For ALL - I trust You (A)")
					if(choice.lower()=='y'||(choice.lower)=='a'||setForAll):
						if(choice.lower)=='a':
							setForAll=True
						path = os.path.join(dirName,fname)
						path2 = os.path.join(dirName,details['title']+" ("+data['imdbRating']+") ."+details['container'])
						os.rename(path,path2)

#details = guess_file_info(fname)