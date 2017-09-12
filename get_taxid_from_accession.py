import sys
import os
import subprocess
import glob

''''
##Argument 1 infile
if(sys.argv[1]):
	if os.path.isfile(sys.argv[1]):	
		with open(sys.argv[1], 'rb') as accFile:
			mapFileName = os.path.basename(sys.argv[1]).split('_')[0] + '.map'
			with open(mapFileName, 'wb') as mapfile:
				acc_to_tax = {}
				print "loading index"
				with open('nucl_gb.accession2taxid', 'rb') as accession2taxid:
					for line in accession2taxid:
						taxID = line.strip().split('\t')[2]
						accID = line.strip().split('\t')[1]
						acc_to_tax[accID] = taxID
				print "Mapping accession to taxID"
				for line in accFile:
					accID = line.strip()
					taxID = acc_to_tax[accID]
					print accID + ' ' + taxID
					mapfile.write(accID + ' ' + taxID + '\n')
'''
##Argument 1 is directory of accession lists
if(sys.argv[1] and os.path.isdir(sys.argv[1])):
	with open('nucl_gb.accession2taxid', 'rb') as accession2taxid:
		acc_to_tax = {}
		print "loading index"
		for line in accession2taxid:
			taxID = line.strip().split('\t')[2]
			accID = line.strip().split('\t')[1]
			acc_to_tax[accID] = taxID
		print "finished loading index"
		fileArr = glob.glob(sys.argv[1] + '*')
		print fileArr
		for file in fileArr:
			if(os.path.isfile(file)):
				print "made it here"
				mapFileName = os.path.basename(file).split('_')[0] + '.map'
				print "Creating " + mapFileName
				with open(file, 'rb') as accFile:
					print "opened acc file"
					with open(mapFileName, 'wb') as mapfile:
						print "opened map file"
						for line in accFile:
							accID = line.strip()
							try:
								taxID = acc_to_tax[accID]
								print accID + ' ' + taxID
								mapfile.write(accID + ' ' + taxID + '\n')
							except:
								taxID = 'unknown'
								print accID + ' ' + taxID
								mapfile.write(accID + ' ' + taxID + '\n')