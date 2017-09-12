import os
import sys

with open('newAcc2Tax.map','r') as accFile:
	with open('acc2tax.map','w') as outFile:
		for line in accFile:
			line = line.strip()
			lineArr = line.split('\t')
			accID = lineArr[0]
			taxID = lineArr[1]
			try:
				accIDArr = accID.split('.')
				accIDBase = accIDArr[0]
				accIDVer = int(accIDArr[1])
				if accIDVer > 1:
					while accIDVer >= 1:
						out.write(accIDBase + '.' + str(accIDVer) + '\t' + taxID +'\n'
						accIDVer = accIDVer - 1
				else:
					out.write(line+'\n')
			except:
				print "Unable to split accID"