GitVersionParsing
=================

Parses git logs and calculates number of files and lines changed between tags. I used this to get the number of files and lines changed for each version of my code base. It is really only useful if you tag the versions of your code.

To Use: 
copy file into root directory of any git repository. 
run it from command line.
the output is in .CSV format and is displayed in stdout as well as in a file that is created called GitVersionChanges.csv

Note: this only goes back 3 months dues to how long it takes to run and the fact that we didn't tag code at first. to change this just edit line 25. 
