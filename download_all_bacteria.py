import os
import subprocess

print ("Getting Assembly Summary.txt")
#subprocess.call("wget --no-check-certificate https://ftp.ncbi.nlm.nih.gov/genomes/genbank/bacteria/assembly_summary.txt", shell=True)

print ("Stripping unused info")
#subprocess.call("awk -F '\t' '{if($12=="Complete Genome") print $20}' assembly_summary.txt > assembly_summary_complete_genomes.txt", shell=True)

with open("assembly_summary_complete_genomes.txt", 'r') as genome_list:
	result = subprocess.check_output("wc -l assembly_summary_complete_genomes.txt", shell=True)
	line_count = int(result.split(' ')[0])
	print ("Preparing to download " + str(line_count) + " reference genomes")
	download_count = 0
	for line in genome_list:
		if(download_count % 100 == 0):
			remaining = line_count - download_count
			print (str(download_count) + " downloads completed", str(remaining) + " downloads remaining")
		line = line.strip().replace('ftp://','https://')
		##Get name of assembly
		assembly_name = line.split('/')[-1].strip()
		download_path = line + '/'+ assembly_name + '_genomic.fna.gz'
		gzipped_name = assembly_name + '_genomic.fna.gz'
		##Download Assembly if it doesn't already exist
		if not os.path.isfile(gzipped_name):
			print "Downloading " + assembly_name
			subprocess.call('wget --no-check-certificate ' + download_path, shell=True)
		##Unzip Assembly
		print "Unzipping " + assembly_name
		subprocess.call('gunzip ' + gzipped_name, shell=True)
		download_count += 1


