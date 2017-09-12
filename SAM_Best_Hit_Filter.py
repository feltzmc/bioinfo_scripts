import os
import sys

inname = sys.argv[1]
name,ext = os.path.splitext(inname)
outname = name+'_filtered'+ext
headerArr = []
contigDict = {}
with open (inname,'r') as infile:
	for line in infile:
		line = line.strip()
		if(line[0] == '@'):
			headerArr.append(line)
			continue
		lineArr = line.split('\t')
		readName = lineArr[0]
		if readName not in contigDict:
			contigDict[readName] = {}
			mapScore = lineArr[4]
		if mapScore not in contigDict[readName]:
			contigDict[readName][mapScore] = []
		contigDict[readName][mapScore].append(line)

with open (outname,'w') as outfile:
	for line in headerArr:
		outfile.write(line+'\n')
	for readName in sorted(contigDict):
		scoreDict = contigDict[readName]
		min_score = min(scoreDict, key=lambda k: scoreDict[k])
		if len(scoreDict[min_score]) == 1:
			outfile.write(scoreDict[min_score][0]+'\n')
			
		
		