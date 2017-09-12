import os
import sys
import operator

inname = sys.argv[1]
countDict = {}
bpDict = {}
with open (inname,'r') as infile:
	for line in infile:
		line = line.strip()
		if(line[0] == '@'):
			continue
		lineArr = line.split('\t')
		accession = lineArr[2]
		readLen = len(lineArr[9])
		print lineArr[9]
		if accession not in countDict:
			countDict[accession] = 1
		else:
			countDict[accession] += 1
		if accession not in bpDict:
			bpDict[accession] = readLen
		else:
			bpDict[accession] += readLen

for accession,count in sorted(countDict.items(), key=operator.itemgetter(1), reverse=True):
	print accession + " : " + str(count) + " : " + str(bpDict[accession])