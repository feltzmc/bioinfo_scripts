import sys
import os

##Argument 1 infile
if(sys.argv[1]):
    if os.path.isfile(sys.argv[1]):
	##Make accession to tax_id map
	taxAccDict = {}
        with open("/home/mfeltz/workdir/CENTRIFUGE/11-28-2016_all_bacteria/assembly_summary.txt", 'rb') as assemblySum:
	    for line in assemblySum:
		if line[0] == '#':
		    continue
		else:
		    lineArr = line.strip().split("\t")
		    taxAccDict[lineArr[7]] = lineArr[5]	    
	with open(sys.argv[1], 'rb') as fastaFile:
	    matched = 0
	    unmatched = 0	
	    for line in fastaFile:
		line = line.strip()
		try:
		    if line[0] == '>':
		        lineArr = line.replace('chromosome',',').split(',')[0].split(' ')
			del lineArr[0]
			line = ' '.join(lineArr)
			if line in taxAccDict:
			    ##print taxAccDict[line]
			    matched += 1
			else:
			    ##print line
			    unmatched += 1
                except:
                    print "empty line"
	    print "Matched: " + str(matched)
	    print "Unmatched: " + str(unmatched)

