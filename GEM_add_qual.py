import os
import sys

inname = sys.argv[1]
name,ext = os.path.splitext(inname)
outname = name+'_corrected'+ext
with open (inname,'r') as infile:
	with open (outname,'w') as outfile:
		for line in infile:
			line = line.strip()
			if(line[0] == '@'):
				outfile.write(line+'\n')
				continue
			lineArr = line.split('\t')
			lineArr[10] = '*'
			outline = '\t'.join(lineArr)
			outfile.write(outline+'\n')