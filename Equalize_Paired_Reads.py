import sys
import os
import re

pair1_file = sys.argv[1]
pair2_file = sys.argv[2]

if not os.path.isfile(pair1_file):
	print "Input file "+pair1_file+" not found"
	sys.exit(1)

if not os.path.isfile(pair2_file):
	print "Input file "+pair2_file+" not found"
	sys.exit(1)

pair1_out_file = os.path.basename(pair1_file).split('.')[0] + "_Equalized.fq"
pair2_out_file = os.path.basename(pair2_file).split('.')[0] + "_Equalized.fq"

with open(pair1_file,"r") as pair1:
	with open(pair2_file,"r") as pair2:
		with open(pair1_out_file,"w") as pair1out:
			with open(pair2_out_file,"w") as pair2out:
				for pair1line in pair1:
					pair1line=pair1line.strip()
					pair2line=pair2.readline().strip()
					pair1len = len(pair1line)
					pair2len = len(pair2line)
					if pair1len == pair2len:
						m = re.search('length=(.+)', pair1line)
						if m:
							found1 = m.group(1)
						m = re.search('length=(.+)', pair2line)
						if m:
							found2 = m.group(1)
						if found1 != found2:
							if found1 > found2:
								pair1line = pair1line.replace(found1,found2)
							else:
								pair2line = pair2line.replace(found2,found1)
						pair1out.write(pair1line + "\n")
						pair2out.write(pair2line + "\n")
					else:
						pair1line = pair1line[:pair2len]
						pair2line = pair2line[:pair1len]
						pair1out.write(pair1line + "\n")
						pair2out.write(pair2line + "\n")
