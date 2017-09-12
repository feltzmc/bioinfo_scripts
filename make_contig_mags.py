import sys
import os

infile = sys.argv[1]
if not os.path.isfile(infile):
	print "Input file "+infile+" not found"
	sys.exit(0)

outfile = os.path.basename(infile).split('.')[0] + "_mags.txt"

with open(outfile,'w') as mags:
	with open(infile, 'r') as infasta:
		while True:
			line1 = infasta.readline()
			line2 = infasta.readline()
			if not line2: break  # EOF
			seq_id = line1.split(' ')[0][1:]
			magnitude = len(line2.strip())
			mags.write(seq_id + "\t" + str(magnitude) + "\n")
