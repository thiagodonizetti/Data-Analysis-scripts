import json
#import math
#import sys
import os
from os import listdir
from os.path import isfile, join
from pathlib import Path

#print(Path().absolute())


mypath = str(Path().absolute())+"\\fix"
exist_ok=True
Path(mypath+"\\filtered\\").mkdir(exist_ok=True) 
filesList = [f for f in listdir(mypath) if isfile(join(mypath, f))]

for f in filesList:
	print(f)

	
def filterFile(fileName):		
	buffer = ""
	#print(fileName)
	file = open(mypath+"\\"+fileName,"r") 
	for line in file:
		data = json.loads(line)
		if 'values' in data and data["statuscode"]== 200:
			#print(data)
			fix = data["values"]["frame"]["fix"]
			#print(fix)
			if fix:
				buffer = buffer +  line
	
	
	outFile = open(mypath+"\\filtered\\"+fileName.split(".")[0]+"-filtered.txt","w") 	
	print("Arquivo gerado: ",outFile.name)
	outFile.write(buffer)
	outFile.close()

for f in filesList:
	filterFile(f)
	#print(data)
	#print(frame)
	
#frame = data[0]["values"]["frame"]

#print(data[0])
#print(file.readline())
#for x in file:
#	for a in x.split(","):
#		print(a)

#l = file.readline()
#s = l.split(",")

#for a in s:
#	print(a)

#print("x: " + s[3].split("\"x\":")[1])
#Valor de x
#print ("x: " + re.sub("[^0-9.]", "", s[3]))