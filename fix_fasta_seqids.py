import sys
import os

infile=sys.argv[1]

seqid_dict = {}
if os.path.isfile(infile):
	with open(infile,'r') as fasta:
		for line in fasta:
			line = line.strip()
			if(line[0] == '>'):
				lineArr = line.split('|')
				seqid = lineArr[1]
				if seqid not in seqid_dict:
					seqid_dict[seqid] = 0
					print line
				else:
					new_seqid = seqid + ".1"
					i=1
					while True:
						if new_seqid in seqid_dict:
							i += 1
							new_seqid = seqid + "." + str(i)
						else:
							seqid_dict[new_seqid] = 0
							print lineArr[0] + '|' + new_seqid + '|' + lineArr[2]
							break
			else:
				print line
else:
	print infile + " not found"