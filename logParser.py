'''
 ----------- Scritp on github ---------------
'''
import json
import math
import sys
from pathlib import Path
from os import listdir
from os.path import isfile, join

#
#### Get LINE NUMBER, TIMESTAMP, CLICK DURATION, PAUSE BEFORE CLICK, CUMULATIVE DISTANCE
### and GET Clicks number, doubleclicks number, click duration mean, pause before click mean, Total Distance, Distance mean, Velocity mean, 
#
def euclideanDistance(x1, y1, x2, y2):
	return (math.sqrt(math.pow((x2 - x1), 2) +
			math.pow((y2 - y1), 2)))

#arg = sys.argv[1]
mypath = str(Path().absolute())+"\\logs"
Path(mypath+"\\results\\").mkdir(exist_ok=True) 

filesList = [f for f in listdir(mypath) if isfile(join(mypath, f))]

for f in filesList:
	print(f)

	
def readFiles(fileName):	
	print("fname"'', fileName)
	fileId = fileName.split("p")[1].split("-")[0]
	print(fileId)
	file = open(mypath+"\\"+fileName,"r") 
	bufferClicks = "LINE NUMBER, TIMESTAMP, CLICK DURATION, CUMULATIVE CLICK DURATION, PAUSE BEFORE CLICK, CUMULATIVE PAUSE BEFORE CLICK\n"
	bufferMetricas = ""
	bufferMetricasHeader = "Task Time (sec), MOUSEDOWN-UP, NUM. CLICKS, NUM. DBCLICKS, MEAN CLICK DURATION (msec), MEAN PAUSE BEFORE CLICK (msec), MOUSE TOTAL DISTANCE, MOUSE MEAN DISTANCE, MOUSE MEAN VELOCITY (px/sec), MEAN STROKE LENGTH, MEAN STROKE DURATION (msec), MEAN STRAIGHTNESS, KEYS, TYPING VELOCITY (key/min), TOTAL TIME TYPING (sec), MEAN TIME TYPING (sec), DELETE, BACKSPACE, DELETE+BACKSPACE\n"
	bufferStroke = "LENGTH, DURATION, STRAIGHTNESS, TYPE\n"
	bufferMoves = "LINE NUMBER, TIMESTAMP, X1, Y1, X2, Y2, DISTANCE, CUMULATIVE DISTANCE \n"
	bufferKeyboard = "Number of keys pressed, duration, velocity, Number of interval, delete, backspace\n"  
	x1=x2=y1=y2= None
	somaDist = 0	
	dist = 0
	lineNumber = 1
	
	strokeLength = 0
	strokeDuration = 0
	straightness = 0
	pauseThreshold = 1000
	strokeIniTime = 0
	x1Stroke = y1Stroke = xNStroke = yNStroke = 0
	strokeLengthSum = 0
	strokeDurationSum = 0
	straightnessSum = 0
	strokes = 0
	
	zeroTime = 0
	backspace = 0
	delete = 0
	keyThreshold = 60000
	
	# keys = 0
	# timeKeyPrev = 0
	# timeKeyCurr = 0
	# timeKeyInterval = 0
	# keysInterval = 0
	# sumKeyVel = 0
	# numberKeysIntervals = 0
	# keyThreshold = 60000
	# timeLastKey = 0
	# totalTime = 0
	
	firstKey = 0
	lastKey = 0
	numeroTeclas = 0
	numeroTotalTeclas = 0
	tempoTotal = 0
	velTotal = 0
	numeroIntervalos = 0
	
	
	

	clicks = 0
	dblclicks = 0
	mousedown = 0
	mouseup = 0
	clickDuration = 0
	updown = 0
	clickDurationSum = 0
	pauseSum = 0
	pauses = 0
	currTime = None
	countMoves = 0
	prevTime = 0
	moveTimeSum = 0

	
	file.readline()
	for line in file:			
		
		data = line.split(",")
        #get initial time to calculate Total task time
		if zeroTime == 0:
			zeroTime = int(data[2].strip('"'))
		
		if numeroTeclas > 0:
			if int(data[2].strip('"')) - lastKey > keyThreshold:
				print("TEMPO ", int(data[2].strip('"')) - lastKey)
				time = lastKey - firstKey
				if time == 0:
					velKey = 1
				else:
					velKey = numeroTeclas / (time / 60000)
				print("Tempo, numero, vel ", time, numeroTeclas, velKey, numeroIntervalos+1, numeroTotalTeclas + numeroTeclas)
				bufferKeyboard += str(numeroTeclas) + ", " + str(time) + ", " + str(velKey) + ", " + str(numeroIntervalos+1) + ", " + str(delete) + ", " + str(backspace) + "\n"
				velTotal += velKey
				tempoTotal += time
				numeroTotalTeclas += numeroTeclas
				numeroTeclas = 0
				numeroIntervalos += 1
				
			
		
		# if keysInterval != 0:
			# #print("keysInterval ini ", keysInterval)
			# timeLastKey += int(data[2].strip('"')) - timeKeyCurr
			# #print("time ", timeLastKey)
			# #print("timeINterval ", timeKeyInterval)
			# timeKeyCurr = int(data[2].strip('"'))
			# #print(timeKeyCurr, timeKeyPrev, timeKeyCurr - time
			# if timeLastKey > keyThreshold:
				# if timeKeyInterval == 0:
					# #print(timeKeyCurr, timeKeyPrev)
					# timeKeyInterval = timeKeyCurr - timeKeyPrev
				# typingVel = keysInterval / (timeKeyInterval/60000)
				# print("number ---, time, vel, numbero de intervalos", keysInterval, timeKeyInterval, typingVel, numberKeysIntervals)
				# bufferKeyboard += str(keysInterval) + ", " + str(timeKeyInterval) + ", " + str(typingVel) + ", " + str(numberKeysIntervals+1) + ", " + str(delete) + ", " + str(backspace) + "\n"
				# sumKeyVel += typingVel
				# numberKeysIntervals += 1
				# totalTime += timeKeyInterval
				# timeKeyInterval = 0
				# timeKeyPrev = 0
				# keysInterval = 0
				# timeLastKey = 0
				
			
		if str(data[3]) == "\"mousemove\"":
			prevTime = currTime
			currTime = int(data[2].strip('"'))
                
			coord = (data[7].strip('"')).split("x")
			countMoves += 1
			#print("coord ", coord)
			if x1 is None:
				#print(coord[0])
				x1 =  int(coord[0])
				y1 =  int(coord[1].split("|")[0])
				if strokeIniTime == 0:
					strokeIniTime = currTime
					x1Stroke = x1
					y1Stroke = y1
				strokeLength += math.sqrt( math.pow(x1, 2) + math.pow(y1,2) )
				bufferMoves += str(lineNumber) + ", " + str(currTime) + ", " + str(x1) + ", " + str(y1) + ", " + str(0) + ", " + str(0) + ", " + str(0)
				#print("Y1 ", y1)				
			else:
				x2 =  int(coord[0])
				y2 =  int(coord[1].split("|")[0])	
				if strokeIniTime == 0:
					strokeIniTime = currTime
					x1Stroke = x2
					y1Stroke = y2
				xNStroke = x2
				yNStroke = y2
					
				strokeLength += math.sqrt( math.pow(x2,2) + math.pow(y2,2) )
				dist = round(euclideanDistance(x1,y1,x2,y2),3)
				moveTimeSum += currTime - prevTime
				bufferMoves += str(lineNumber) + ", " + str(currTime) + ", " + str(x1) + ", " + str(y1) + ", " + str(x2) + ", " + str(y2) + ", " + str(round(dist,3))
				#print("Times ", currTime, prevTime, currTime - prevTime, moveTimeSum)				
				#print(x1,y1,x2,y2,dist)				
				x1 = x2
				y1 = y2		
			somaDist += dist
			bufferMoves += ", " + str(round(somaDist,3)) + "\n"
		elif str(data[3]) == "\"mousedown\"":
			mousedown = int(data[2].strip('"'))
			if strokeLength == 0:
				strokeDuration = straightness = 0
			else:
				strokeDuration = mousedown - strokeIniTime
				straightness  =  math.sqrt(math.pow(x1Stroke - xNStroke, 2) + math.pow(y1Stroke - yNStroke, 2))/strokeLength
			
			
			#print("StrokeLength ", strokeLength, mousedown, strokeIniTime, strokeDuration, straightness)
			bufferStroke += str(round(strokeLength,3)) + ", " + str(strokeDuration) + ", " + str(round(straightness,3)) + ", click\n"
			strokeDurationSum += strokeDuration
			strokeLengthSum += strokeLength
			straightnessSum += straightness
			strokes += 1
			
			strokeLength =  strokeIniTime = 0
			if currTime is not None:
				pause = mousedown - currTime
			else:
				pause = 0
			#print("Pause last move ", currTime, mousedown, mousedown - currTime)
			pauseSum += pause
			pauses += 1
			#print("Ini ", iniTime)
			#print(lineNumber, mousedown, data[3])
			
			
		elif str(data[3]) == "\"mouseup\"" and mousedown != 0:
			mouseup = int(data[2].strip('"'))
			clickDuration = mouseup - mousedown
			clickDurationSum += clickDuration
			#print(lineNumber, mousedown, mouseup, data[3], clickDuration, clickDurationSum)
			bufferClicks += str(lineNumber) + "," +  data[2].strip('"') + "," + str(clickDuration) + "," + str(clickDurationSum) + "," + str(pause) + "," + str(pauseSum) + "\n"
			mousedown = 0
			mouseup = 0
			updown += 1
			
		elif str(data[3]) == "\"click\"":
			clicks += 1
			#print(lineNumber, data[2].strip('"'), clicks, data[3], clickDuration)
			
			
		elif str(data[3]) == "\"dblclick\"":
			dblclicks += 1
			#print(lineNumber, data[2].strip('"'), dblclicks, data[3])	
			
		elif str(data[3]) == "\"keydown\"":
			print(numeroTeclas)
			if numeroTeclas > 0:
				if int(data[2].strip('"')) - lastKey > keyThreshold:
					print("TEMPO 2", int(data[2].strip('"')) - lastKey)
					time = lastKey - firstKey
					if time == 0:
						velKey = 1
					else:
						velKey = numeroTeclas / (time / 60000)
						
					print("Tempo2, numero, vel ", time, numeroTeclas, velKey, numeroIntervalos+1, numeroTotalTeclas + numeroTeclas)
					bufferKeyboard += str(numeroTeclas) + ", " + str(time) + ", " + str(velKey) + ", " + str(numeroIntervalos+1) + ", " + str(delete) + ", " + str(backspace) + "\n"
					velTotal += velKey
					firstKey = lastKey = int(data[2].strip('"')) 
					tempoTotal += time
					numeroTotalTeclas += numeroTeclas
					numeroTeclas = 1
					numeroIntervalos += 1
				else:
					lastKey = int(data[2].strip('"')) 
					numeroTeclas += 1
			else:
				firstKey = lastKey = int(data[2].strip('"')) 
				numeroTeclas = 1
				
			#if timeKeyCurr != 0:
			# timeKeyPrev = timeKeyCurr
			# timeKeyCurr = int(data[2].strip('"'))
			#else:
			#	timeKeyCurr = timeKeyPrev = int(data[2].strip('"'))
			
			# timeLastKey += timeKeyCurr - timeKeyPrev
			# if keysInterval != 0:
				# if timeLastKey > keyThreshold:
					# if timeKeyInterval == 0:
						# timeKeyInterval = timeKeyCurr - timeKeyPrev
					# typingVel = keysInterval / (timeKeyInterval/60000)
					# print("number, time, vel, numero de intervalos", keysInterval, timeKeyInterval, typingVel, numberKeysIntervals)
					# bufferKeyboard += str(keysInterval) + ", " + str(timeKeyInterval) + ", " + str(typingVel) + ", " + str(numberKeysIntervals+1) + ", " + str(delete) + ", " + str(backspace) + "\n"
					# sumKeyVel += typingVel
					# numberKeysIntervals += 1
					# totalTime += timeKeyInterval
					# timeKeyInterval = 0
					# timeKeyPrev = 0
					# keysInterval = 0
					
				# else:
					# timeKeyInterval += timeKeyCurr - timeKeyPrev
			# timeLastKey = 0
			# keys += 1
			# keysInterval += 1
			
			if data[6] == "\"8\"":
				print("backspace")
				backspace += 1
			elif data[6] == "\"46\"":
				print("DELETE")
				delete += 1
			print("key", data[6])
		else:
			#print("---data----: ", data)
			time = int(data[2].strip('"')) 
			if strokeLength > 0 and time - currTime > pauseThreshold:
				#print("ev, time, ", data[3],data[2].strip('"'))
				if strokeLength == 0:
					strokeDuration = straightness = 0
				else:
					strokeDuration = time - strokeIniTime
					straightness  =  math.sqrt(math.pow(x1Stroke - xNStroke, 2) + math.pow(y1Stroke - yNStroke, 2))/strokeLength
				#print("StrokeLengthPause ", strokeLength, time, strokeIniTime, strokeDuration, straightness)
				bufferStroke += str(round(strokeLength,3)) + ", " + str(strokeDuration) + ", " + str(round(straightness,3)) + ", pause\n"
				#print("x1Xn ", x1Stroke, y1Stroke, xNStroke, yNStroke)
				strokeDurationSum += strokeDuration
				strokeLengthSum += strokeLength
				straightnessSum += straightness
				strokeLength =  strokeIniTime = 0
				strokes += 1
			
			
		lineNumber +=1

	# end of lines -------------------
    
    
    
	prevTime = currTime
	currTime = int(data[2].strip('"'))
	moveTimeSum += currTime - prevTime
	taskTotalTime = (currTime - zeroTime)/1000
	print("Times ", currTime, prevTime, currTime - prevTime, moveTimeSum, zeroTime, taskTotalTime)	

	if numeroTeclas > 0:
		print("TEMPO 3", int(data[2].strip('"')) - lastKey)
		time = lastKey - firstKey
		if time == 0:
			velKey = 1
		else:
			velKey = numeroTeclas / (time / 60000)			
		print("Tempo 3, numero, vel ", time, numeroTeclas, velKey, numeroIntervalos+1, numeroTotalTeclas + numeroTeclas)
		bufferKeyboard += str(numeroTeclas) + ", " + str(time) + ", " + str(velKey) + ", " + str(numeroIntervalos+1) + ", " + str(delete) + ", " + str(backspace) + "\n"
		velTotal += velKey
		tempoTotal += time
		numeroTotalTeclas += numeroTeclas
		numeroIntervalos += 1
	
	if numeroIntervalos > 0:
		print("totalTeclas, velTotal, numeroIntervalos, mediaVel ", numeroTotalTeclas, velTotal, numeroIntervalos, velTotal/numeroIntervalos, delete, backspace)
		
	# if keysInterval != 0:
		# if timeKeyInterval == 0:
			# timeKeyInterval = timeKeyCurr - timeKeyPrev
		# typingVel = keysInterval / (timeKeyInterval/60000)
		# print("numberffff, time, vel, numero de intervalos", keysInterval, timeKeyInterval, typingVel, numberKeysIntervals)
		# bufferKeyboard += str(keysInterval) + ", " + str(timeKeyInterval) + ", " + str(typingVel) + ", " + str(numberKeysIntervals+1) + ", " + str(delete) + ", " + str(backspace) + "\n"
		# totalTime += timeKeyInterval
		# sumKeyVel += typingVel
		# numberKeysIntervals += 1
	# if numberKeysIntervals != 0:
		# print("delete, backspace, keys, sumKeyVel, numberKeysIntervals", delete, backspace, keys, sumKeyVel, numberKeysIntervals, sumKeyVel / numberKeysIntervals)
	
	
		outFileKeyboard= open(mypath+"\\results\\"+fileId+"-outKeyboard.txt","w")
		print("\n\tArquivo gerado ", outFileKeyboard)
		outFileKeyboard.write(bufferKeyboard)
		
		outFileKeyboard.write("\n keys: "+str(numeroTotalTeclas))
		outFileKeyboard.write("\n Velocidade acumulada: " +str( velTotal))
		outFileKeyboard.write("\n Numero de intervalos: "+str( numeroIntervalos))
		outFileKeyboard.write("\n Velocidade média: "+str( velTotal/numeroIntervalos))
		outFileKeyboard.write("\n Total time: "+str( tempoTotal))
		outFileKeyboard.write("\n Total Delete: "+str( delete))
		outFileKeyboard.write("\n Total backspace: "+str( backspace))
		outFileKeyboard.close()
		
		# outFileKeyboard.write("\n keys: "+str(keys))
		# outFileKeyboard.write("\n Velocidade acumulada: " +str( sumKeyVel))
		# outFileKeyboard.write("\n Numero de intervalos: "+str( numberKeysIntervals))
		# outFileKeyboard.write("\n Velocidade média: "+str( sumKeyVel/numberKeysIntervals))
		# outFileKeyboard.write("\n Total time: "+str( totalTime))
		# outFileKeyboard.write("\n Total Delete: "+str( delete))
		# outFileKeyboard.write("\n Total backspace: "+str( backspace))
		#outFileKeyboard.write("\n Velocidade time: "+str( sumKeyVel/totalTime))
		# outFileKeyboard.close()
	
	
	
	outFileStrokes= open(mypath+"\\results\\"+fileId+"-outStrokes.txt","w")
	print("\n\tArquivo gerado ", outFileStrokes)
	outFileStrokes.write(bufferStroke)
	outFileStrokes.close()
	
	outFileMoves= open(mypath+"\\results\\"+fileId+"-outMoves.txt","w")
	print("\n\tArquivo gerado ", outFileMoves)
	outFileMoves.write(bufferMoves)
	outFileMoves.close()
	
	bufferMetricas += str(taskTotalTime) + ", " + str(updown) + ", " + str(clicks) + ", " + str(dblclicks) + ", " +str(round((clickDurationSum/updown)/1000, 3)) + ", " +str(round((pauseSum/pauses)/1000, 3)) + ", " +str(round(somaDist, 3)) + ", " +str(round(somaDist/countMoves, 3)) + ", " + str(round(somaDist / (moveTimeSum/1000), 3)) + ", " + str(round(strokeLengthSum/strokes, 3)) + ", " + str(round((strokeDurationSum/strokes)/1000, 3))+ ", " + str(round(straightnessSum/strokes, 3)) 
	
	if numeroIntervalos > 0:
		print("Keys ",numeroTotalTeclas, delete, backspace)
		bufferMetricas += ", " + str(numeroTotalTeclas) + ", " + str( velTotal/numeroIntervalos) + ", " +  str(tempoTotal/1000) + ", " +  str(tempoTotal/numeroIntervalos/1000) + ", " + str(delete) + ", " + str(backspace) + ", " + str(delete + backspace) 
	else:
		bufferMetricas += ", " + str(0) + ", " + str(0) + ", " +  str(0) + ", " +  str(0) + ", " + str(0) + ", " + str(0) + ", " + str(0) 
	
	
	# if numberKeysIntervals > 0:
		# print("Keys ",keys, delete, backspace)
		# bufferMetricas += ", " + str(keys) + ", " + str( sumKeyVel/numberKeysIntervals) + ", " +  str(totalTime/1000) + ", " +  str(totalTime/numberKeysIntervals) + ", " + str(delete) + ", " + str(backspace) + ", " + str(delete + backspace) 
	# else:
		# bufferMetricas += ", " + str(0) + ", " + str(0) + ", " +  str(0) + ", " +  str(0) + ", " + str(0) + ", " + str(0) + ", " + str(0) 
	
	outFileMetricas= open(mypath+"\\results\\"+fileId+"-outMetricas.txt","w")
	print("\n\tArquivo gerado ", outFileMetricas)
	outFileMetricas.write(bufferMetricasHeader)
	outFileMetricas.write(bufferMetricas)
	outFileMetricas.close()
	
	global count
	global bufferTudo
	if count == 0:		
		count +=1
		bufferTudo += "ID," + bufferMetricasHeader
		
	bufferTudo += fileId + "," + bufferMetricas + "\n"
	
	
	print("Clicks", clicks)
	print("dblclicks", dblclicks)
	print("updown ", updown)
	print("clickDurationSum ", clickDurationSum)
	print("pauseSum ", pauseSum)
	print("clickDurationSumAVG", clickDurationSum/updown)
	print("pauseSumAVG ", pauseSum/pauses)
	print("Pauses ", pauses)
	print("SomaDist ", somaDist)
	print("countMoves ", countMoves)
	print("DistAVG ", somaDist/countMoves)
	print("Velocity ", somaDist / (moveTimeSum/1000))
	
	outFileClick = open(mypath+"\\results\\"+fileId+"-outCLICKS.txt","w")
	print("\n\tArquivo gerado ", outFileClick)
	outFileClick.write(bufferClicks)
	if lineNumber-1 == 0:
		print(fileName)
	outFileClick.close()
		
		
		
		# data = json.loads(line)
		# if 'values' in data:
			# frame = data["values"]["frame"]
			# if x1AVG == -1:
				# x1AVG =  frame["avg"]["x"]
				# y1AVG =  frame["avg"]["y"]
				# iniTime = data["values"]["frame"]["time"]
				# buffer = buffer + str(lineNumber) + "," + str(iniTime) + "," + str(x1AVG) + "," + str(y1AVG) +"," + "0" + "," + str(round(distAVG,3))
			# else:
				# currTime = data["values"]["frame"]["time"]
				# x2AVG =  frame["avg"]["x"]
				# y2AVG =  frame["avg"]["y"]
				
				# distAVG = round(euclideanDistance(x1AVG,y1AVG,x2AVG,y2AVG),3)
				
				# sum = somaDistAVG + distAVG
				# print(distAVG, somaDistAVG, sum)
				# buffer = buffer + "\n" +str(lineNumber) + "," + str(currTime) + "," + str(x2AVG) + "," + str(y2AVG) + "," + str(round(distAVG, 3)) + "," + str(round(sum, 3))
				# x1AVG = x2AVG
				# y1AVG = y2AVG
				
			# buffer = buffer + "," + str(frame["lefteye"]["psize"])
			# lineNumber += 1
			# somaDistAVG += distAVG
			
	# outFile = open(mypath+"\\results\\"+fileName.split(".")[0]+"-out.txt","w")
	# print("Arquivo gerado ", outFile)
	# outFile.write(buffer)
	# outFile.write("\nsomaDistAVG, "+str(round(somaDistAVG,3)))
	# outFile.write("\nlineNumber, "+str(lineNumber-1))
	# if lineNumber-1 == 0:
		# print(fileName)
	# outFile.write("\nsomaDistAVG/lineNumber, "+str(round(somaDistAVG/(lineNumber-1),3)))
	# outFile.write("\niniTime, "+str(iniTime))
	# outFile.write("\nendTime, "+str(currTime))
	# outFile.write("\ntotalTime, "+str(currTime-iniTime))
	# outFile.write("\nVelocity, "+str(round(somaDistAVG/ ((currTime-iniTime)/1000) ,3 )))
	
bufferTudo = ""	
count = 0
for f in filesList:
	readFiles(f)
outTudo = open(mypath+"\\results\\OUT-METRICAS-TODOS.txt","w")
print("Arquivo gerado ", outTudo)
outTudo.write(bufferTudo)
