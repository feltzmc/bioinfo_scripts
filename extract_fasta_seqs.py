import os

input_fasta = "/home/mfeltz/workdir/select_agents_ref.fasta"
output_fasta = "/home/mfeltz/workdir/selected_seqs.fasta"
wanted_seqs = ['>NC_007880.1','>NC_003143.1','>NC_027213|Organism:Raccoonpox']

lines_processed = 0
with open(output_fasta,'w') as outfasta:
	with open(input_fasta, 'r') as infasta:
		line = infasta.readline()
		lines_processed+=1
		while(line):
			if lines_processed%1000000 == 0:
				print str(lines_processed) + " lines processed" 
			if line[0] == '>':
				lineArr = line.split()
				if lineArr[0] in wanted_seqs:
					print "Found wanted seq: " + line.strip()
					outfasta.write(line)
					while(True):
						line = infasta.readline()
						lines_processed+=1
						if line[0] == '>':
							break
						else:
							outfasta.write(line)
				else:
					line = infasta.readline()
					lines_processed+=1
			else:
				line = infasta.readline()
				lines_processed+=1