import json
import math
import sys
from pathlib import Path

#
####
#### GET LINE NUMBER, TIMESTAMP, X, Y, CUMULATIVE DIST. RAW and AVG for each line
### and GET TOTAL DIST., MEAN DIST., NUMBER OF POINTOS, VELOCITY
#

def euclideanDistance(x1, y1, x2, y2):
	return (math.sqrt(math.pow((x2 - x1), 2) +
			math.pow((y2 - y1), 2)))

#mypath = "C:\\Users\\danim\\Documents\\THIAGO MESTRADO E DOUTORADO\\Python\\testes"

arg = sys.argv[1]
mypath = str(Path().absolute())+"\\files"
Path(mypath+"\\results\\").mkdir(exist_ok=True) 
from os import listdir
from os.path import isfile, join
filesList = [f for f in listdir(mypath) if isfile(join(mypath, f))]

for f in filesList:
	print(f)

	
def readFiles(fileName):			
	file = open(mypath+"\\"+fileName,"r") 
	buffer = "LINE NUMBER, TIMESTAMP, X AVG, Y AVG, CUMULATIVE DIST AVG, X RAW, Y RAW, CUMULATIVE DIST RAW, Pupil Size\n"

	x1AVG=x2AVG=y1AVG=y2AVG=-1
	x1RAW=x2RAW=y1RAW=y2RAW=-1

	somaDistAVG = 0
	somaDistRAW = 0
	lineNumber = 1
	distAVG = 0
	distRAW = 0
	for line in file:
		#print(line)
		data = json.loads(line)
		if 'values' in data:
			if arg == "frame":
				frame = data["values"]["frame"]
			elif arg == "left":
				frame = data["values"]["frame"]["lefteye"]
			elif arg == "right":
				frame = data["values"]["frame"]["righteye"]
			if x1AVG == -1:
				x1AVG =  frame["avg"]["x"]
				y1AVG =  frame["avg"]["y"]
				x1RAW =  frame["raw"]["x"]
				y1RAW =  frame["raw"]["y"]
				iniTime = data["values"]["frame"]["time"]
				buffer = buffer + str(lineNumber) + "," + str(iniTime) + "," + str(x1AVG) + "," + str(y1AVG) + "," + str(round(distAVG,3)) + "," + str(x1RAW) + "," + str(y1RAW) + "," + str(round(distRAW,3))
			else:
				currTime = data["values"]["frame"]["time"]
				x2AVG =  frame["avg"]["x"]
				y2AVG =  frame["avg"]["y"]
				x2RAW =  frame["raw"]["x"]
				y2RAW =  frame["raw"]["y"]
				distAVG = round(euclideanDistance(x1AVG,y1AVG,x2AVG,y2AVG),3)
				distRAW = round(euclideanDistance(x1RAW,y1RAW,x2RAW,y2RAW),3)
				#print("AVG ",distAVG)
				#print("RAW ",distRAW)
				buffer = buffer + "\n" +str(lineNumber) + "," + str(currTime) + "," + str(x2AVG) + "," + str(y2AVG) + "," + str(round(somaDistAVG + distAVG, 3)) + "," + str(x2RAW) + "," + str(y2RAW) + "," + str(round(somaDistRAW + distRAW, 3))
				x1AVG = x2AVG
				y1AVG = y2AVG
				x1RAW = x2RAW
				y1RAW = y2RAW
			if arg == "right" or arg == "left":
				buffer = buffer + "," + str(frame["psize"])
			lineNumber += 1
			somaDistAVG += distAVG
			somaDistRAW += distRAW
	outFile = open(mypath+"\\results\\"+fileName.split(".")[0]+"_"+arg+"-out.txt","w")
	print("Arquivo gerado ", outFile)
	outFile.write(buffer)
	outFile.write("\nsomaDistAVG, "+str(round(somaDistAVG,3)))
	outFile.write("\nlineNumber, "+str(lineNumber-1))
	if lineNumber-1 == 0:
		print(fileName)
	outFile.write("\nsomaDistAVG/lineNumber, "+str(round(somaDistAVG/(lineNumber-1),3)))
	outFile.write("\niniTime, "+str(iniTime))
	outFile.write("\nendTime, "+str(currTime))
	outFile.write("\ntotalTime, "+str(currTime-iniTime))
	outFile.write("\nVelocity, "+str(round(somaDistAVG/ ((currTime-iniTime)/1000) ,3 )))
	
	outFile.write("\nsomaDistRAW, "+str(round(somaDistRAW,3)))
	outFile.write("\nlineNumber, "+str(lineNumber-1))
	outFile.write("\nsomaDistRAW/lineNumber, "+str(round(somaDistRAW/(lineNumber-1),3)))
	outFile.write("\niniTime, "+str(iniTime))
	outFile.write("\nendTime, "+str(currTime))
	outFile.write("\ntotalTime, "+str(currTime-iniTime))
	outFile.write("\nVelocity, "+str(round(somaDistRAW/ ((currTime-iniTime)/1000) ,3 )))
	outFile.close()

	#print(somaDistAVG)
	#print(lineNumber-1)
	#print(somaDistAVG/(lineNumber-1))
	
	#print(somaDistRAW)
	#print(lineNumber-1)
	#print(somaDistRAW/(lineNumber-1))

for f in filesList:
	readFiles(f)
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