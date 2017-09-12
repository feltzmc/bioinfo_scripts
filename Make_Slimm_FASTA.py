import sys
import os

print "Importing taxonomy file"
##Argument 1 mapfile
with open(sys.argv[1], 'r') as MAPFILE:
	mapDict = {}
	for line in MAPFILE:
		lineArr = line.strip().split('\t')
		acc = lineArr[0]
		tax = lineArr[1]
		mapDict[acc] = tax
print "Finished importing taxonomy file"

##Argument 2 mapfile
print "Generating new FASTA"
with open(sys.argv[2], 'r') as INFASTA:
	with open("/home/mfeltz/SLIMM_NT.fa", 'w') as OUTFASTA:
		for line in INFASTA:
			if line[0] == '>':
				try:
					accOld = line.split(' ')[0]
					accID = accOld.split('.')[0][1:]
					accNew = '>' + accID + "|ti|" + mapDict[accID]
					line = line.replace(accOld,accNew)
					OUTFASTA.write(line)
				except:
					OUTFASTA.write(line)
			else:
				OUTFASTA.write(line)
print "Done"