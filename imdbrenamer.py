'''
					::IMDB RATING FILE RENAMER::
							@achute  


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
imdbtxt=open(rootDir+"\\imdbrating.txt","a")
trueforall=False
setForAll=False
movies_extension=["avi","mp4","mkv","mov"]
for dirName,subdirList,fileList in os.walk(rootDir):
	for fname in fileList:
		url="http://www.omdbapi.com/?t="
		year_info=False
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
					if(trueforall == False):
						a=input("\n SEARCH..(Y) -yes  (A) - Yes for all ")
					if(a.lower()=="a"):
						trueforall=True
					if(a.lower()=="y" or trueforall==True):
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
						choice = "f"
						if(setForAll==False and data['imdbRating'] != "N/A"):
							choice = input("\n Yes Change It ! (Y/N) \n Change For ALL - I trust You (A)")
						if((choice.lower()=='y' or choice.lower()=='a'or setForAll==True )and data['imdbRating'] != "N/A"):
							if(choice.lower()=="a"):
								setForAll=True	
							imdbtxt.write(data['imdbRating']+"\t"+details['title']+"\n")
							path = os.path.join(dirName,fname)
							path2 = os.path.join(dirName,details['title']+" ("+data['imdbRating']+") ."+details['container'])
							os.rename(path,path2)

imdbtxt.close()