imdbfilerenamer
===============

A python script that searches your folders and scan for movie files and tries to download 
its corresponding IMDB rating and it renames your movie file with the rating.

example
=======
Million Dollar Arm 2014.mkv 

will be renamed with 

Million Dollar Arm (2014) (7.2).mkv

Usage
=====

python imdbrenamer.py <PATH TO YOUR MOVIES FOLDER>

example:
python imdbrenamer.py E:\movies\

Python Modules Used
===================
guessit - to guess for the correct movie name and extract the year and title information.
omdbapi - to perform request and find the movie rating.