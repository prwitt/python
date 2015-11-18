# -*- coding: utf-8 -*-
"""
Created on Tue Feb 17 23:16:32 2015

@author: prenato
"""

"download file from Training Class"
"Author: Paulo Renato"
"Date: 20140720 - Lisbon"
"Version: 0.1 - 20140720"
"Version: x.x - YYYYMMDD"

import time
import urllib

url = 'https://dl.dropboxusercontent.com/u/256235288/python-intro-mef-04/pub/'
arquivo = '/Users/prenato/Projects/python/Training/downloads/files.txt'
dirname = '/Users/prenato/Projects/python/Training/downloads/'
sufixo = ".html"
mainpage = "index.html"
url1= url+mainpage
filename1 = dirname+mainpage
inicio = time.ctime() #script start time

# download index page
u = urllib.urlopen(url1)
mp = u.read()
with open(filename1, "w") as xyz1:
	xyz1.write(mp)

# get relevant names from the index - look at filename1 format prior to do any change
with open(filename1) as f1:
	allRecords=[] # define list
	for line1 in f1:
		corte = (line1.split('"')[-1]).__contains__(".py")
		if corte == True:
			newpage = (line1.split('"')[-1]).split('>')[1].split('.')[0]+sufixo
			allRecords.append(newpage)

# creates empty file
x = ""
with open(arquivo,"w") as textfile:
	textfile.write(x)

# writes list to the file
for line2 in allRecords:
	allRecordsN = str(line2+"\n")
	with open(arquivo, "a") as textfile:
		textfile.writelines(allRecordsN)

# download pages
with open(arquivo) as f:
	for line in f:
		filenameX = line.strip("\n") #remove new line from previous step
		filename = dirname+filenameX
		pagina = str(url+line)
		print ('Downloading %s' % filename)
		line = str(line)
		u = urllib.urlopen(pagina)
		codigo = u.read()
		with open(filename, "wb") as imgfile:
			imgfile.write(codigo)
		
print inicio
print time.ctime()