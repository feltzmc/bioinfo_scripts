import os
taxAccDict = {}
with open("/home/mfeltz/workdir/CENTRIFUGE/11-28-2016_all_bacteria/assembly_summary.txt", 'rb') as assemblySum:
	    for line in assemblySum:
		if line[0] == '#':
		    continue
		else:
		    lineArr = line.strip().split("\t")
		    taxAccDict[lineArr[0]] = lineArr[5]
assemblySum.close()
with open('New_All_Bacteria.fna','wb') as allBacFasta:
    for fn in os.listdir('/home/mfeltz/workdir/CENTRIFUGE/11-28-2016_all_bacteria'):
        if fn[0] == 'G':
	    fnArray = fn.split('_')
	    accNum = fnArray[0] + '_' + fnArray[1]
	    taxID = taxAccDict[accNum]
	    fullFileName = '/home/mfeltz/workdir/CENTRIFUGE/11-28-2016_all_bacteria/' + fn
	    with open(fullFileName, 'rb') as fnaFile:
	        content = ''
	        for line in fnaFile:
		    if line[0] == '>':
		        header = line
		    elif line[0] == 'A' or line[0] == 'T' or line[0] == 'G' or line[0] == 'C':
		        content = content + line  
		    headArr = header.split(' ')
		    headIdxZero = headArr[0] 
		    del headArr[0]
	    	allBacFasta.write(headIdxZero + '|kraken:taxid|' + taxID + ' ' + " ".join(headArr))
	    	allBacFasta.write(content)
