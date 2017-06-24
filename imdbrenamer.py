'''
                    ::IMDB RATING FILE RENAMER::
                            @achute


'''
import os
import json
import requests
import sys
from guessit import guessit


API_KEY             = "xxxxxxx"
if API_KEY is None:
    print("Please set the api key in the file")
    exit(1)

OMDB_API            = "http://www.omdbapi.com/?apikey="+API_KEY
ROOT_DIR            = None

KNOWN_EXTENSIONS    = ["avi","mp4","mkv","mov"]
MOVIES_FILE         = "imdbratings.csv"
FILE_HEADERS        = "movie_name,imdb_ratings,metascore,rotten_tomatoes,genre,plot\n"


def get_movie_details(file_name):
    movie = False
    movie_name = None
    movie_year = None
    extension = None
    try:
        details = guessit(file_name)
    except Exception as e:
        print (str(e))
        print ("Guess! Guess it is not working ")
        return movie, movie_name, movie_year, extension
    if 'container' in details:
        try:
            if details['container'] in KNOWN_EXTENSIONS:
                movie = True
                extension = details['container']
                # This must be a video file :)
                if 'year' in details:
                    # has the year info use it
                    movie_year = details['year']
                if 'title' in details:
                    movie_name = details['title']
        except Exception as e:
            print (str(e))
            print("Cannot Seem to get it right :)")
    return movie, movie_name, movie_year, extension

def get_ratings(movie_name, movie_year):
    imdb_rating = None
    metascore = None
    plot = None
    genre = None
    url = OMDB_API + "&t="
    if movie_year:
        url = url + movie_name + "&y=" + movie_year
    else:
        url = url + movie_name
    str_response = requests.get(url)
    print str_response.text
    data = json.loads(str_response.text)
    try:
        plot = data['Plot']
        genre = data['Genre']
    except Exception as e:
        print (e)
    try:
        imdb_rating = data['imdbRating']
        metascore = data['Metascore']
    except Exception as e:
        print data
        print (str(e))
    return imdb_rating, metascore, genre, plot

def main_func(root_dir):
    if os.path.exists(root_dir):
        ROOT_DIR = root_dir
    else:
        print("Please supply a valid folder path, which contains the movies")
        exit(1)

    if not os.path.isfile(ROOT_DIR+"\\"+MOVIES_FILE):
        imdb_csv = open(ROOT_DIR + "\\" + MOVIES_FILE, "w")
        imdb_csv.write(FILE_HEADERS)
    else:
        imdb_csv=open(ROOT_DIR+"\\"+MOVIES_FILE,"a")
    trueforall=False
    setForAll=False
    for dirName,subdirList,fileList in os.walk(ROOT_DIR):
        for fname in fileList:
            year_info=False
            print (fname)
            movie, movie_name, movie_year, extension = get_movie_details(fname)
            if movie:
                print ("We got this :) ")
                print ("Movie Name : "+str(movie_name))
                print ("Movie Year : "+str(movie_year))
            else :
                # print ("We don't think this is a movie :P ")
                continue
            #print(details)
            print('\n For file : %s'%fname)
            if movie_name is None:
                movie_name = raw_input("Well, we need your help,"
                                       " say the movie name!")
            print ("Searching with : "+str(movie_name))
            if(trueforall == False):
                a=raw_input("\n SEARCH..(Y) -yes  (A) - Yes for all ")
            if(a.lower()=="a"):
                trueforall=True
            if(a.lower()=="y" or trueforall==True):
                imdb_rating, metascore, genre, plot = get_ratings(movie_name,
                                                                  movie_year)
                choice = "f"
                if(setForAll==False and imdb_rating != "N/A"):
                    print movie_name+" ("+imdb_rating+") ."+extension
                    choice = raw_input("\n Yes Change It ! (Y/N) \n Change For ALL - I trust You (A)")
                if((choice.lower()=='y' or choice.lower()=='a'or
                            setForAll==True )and imdb_rating != "N/A"):
                    if(choice.lower()=="a"):
                        setForAll=True
                    imdb_csv.write(movie_name+","+imdb_rating+","+
                                   metascore+","+genre+","+plot+"\n")
                    path = os.path.join(dirName,fname)
                    path2 = os.path.join(dirName,movie_name+" ("+imdb_rating+") ."+extension)
                    os.rename(path,path2)

    imdb_csv.close()

if __name__ == '__main__':
    if len(sys.argv) <=1:
        print("Please supply the directory path along")
        print("Example: python imdbrenamer.py D:\Movies")
        exit(1)
    main_func(sys.argv[1])