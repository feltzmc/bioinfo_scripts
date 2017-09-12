import sys
import os
from pyfasta import Fasta
import subprocess
import shlex

##Global Variables
input_fastq = sys.argv[1]
input_fastq_basename = os.path.splitext(input_fastq)[0]
split_fasta = True

##Make sure input file exists
if not os.path.isfile(input_fastq):
	print "Input file "+input_fastq+" not found"
	sys.exit(0)

##Trim reads using trimGalore
##Settings
trim_galore = "/mnt/NAS/teamprograms/trim_galore_zip/trim_galore"
min_quality = "20"
phred_type = "phred33"
min_length = "30"
output_dir = "/home/mfeltz/workdir"
trimmed_out_file = input_fastq_basename+"_trimmed.fq"
##Run
trim_cmd = trim_galore+" -q "+min_quality+" --"+phred_type+" --fastqc --length "+min_length+" -o "+output_dir+" "+input_fastq
print trim_cmd
subprocess.call(trim_cmd, shell=True)

##Remove PhiX reads using bowtie2
##Settings
phiX_index = "/home/team_data/PhiX_Illumina_Index/phiX_illumina_idx"
filtered_out_file = input_fastq_basename + "_trimmed_filtered.fastq"
##Run
filter_cmd = "bowtie2 -x "+phiX_index+" -U "+trimmed_out_file+" --un "+filtered_out_file + " > phiX_aligned.sam"
print filter_cmd
subprocess.call(filter_cmd, shell=True)

##Convert fastq to fasta
##Settings
fasta_out_file = input_fastq_basename + "_trimmed_filtered.fa"
quality_type = "Q33"
##Run
convert_cmd = "fastq_to_fasta -n -"+quality_type+" -i "+filtered_out_file+" -o "+fasta_out_file
print convert_cmd
subprocess.call(convert_cmd, shell=True)

if(split_fasta):
	##Split fasta into multiple parts
	##Settings
	num_parts = "16"
	num_lines = int(subprocess.check_output('wc -l {}'.format(fasta_out_file), shell=True).split()[0])
	lines_per_file = num_lines/int(num_parts)
	fasta_out_prefix = fasta_out_file[:-2]
	#Ensure lines per file is an even number
	if(lines_per_file % 2 != 0): 
		lines_per_file += 1
	##Run
	split_cmd = "split -d -l "+str(lines_per_file)+" "+fasta_out_file+" "+fasta_out_prefix
	print split_cmd
	subprocess.call(split_cmd, shell=True)

	##Blast reads against nt using one command per fasta
	##Settings
	nt_database = "/home/team_data/Databases/Databases/nt/nt"
	fasta_out_prefix = fasta_out_file[:-3]
	##Run
	for i in xrange(0,int(num_parts)):
		i = str(i)
		if(len(i) == 1):
			i = "0"+i
		fasta_out_part = fasta_out_prefix+"."+i
		blast_out_part = input_fastq_basename + "_out."+i+".blast"
		blast_cmd = "blastn -db "+nt_database+" -query "+fasta_out_part+' -outfmt "6 std qlen slen stitle" -out '+blast_out_part
		print blast_cmd
		##Submit all jobs at once in this loop
		p=subprocess.Popen(blast_cmd, shell=True)
	##Wait for all jobs to finish
	p.wait()

	##Join the blast parts back together
	##Settings
	blast_out_file = input_fastq_basename + "_out.blast"
	##Run
	cat_cmd = "cat"
	for i in xrange(0,int(num_parts)):
		i = str(i)
		if(len(i) == 1):
			i = "0"+i
		blast_out_part = input_fastq_basename + "_out."+i+".blast"
		cat_cmd += " "+blast_out_part
	cat_cmd += " >> "+blast_out_file
	print cat_cmd
	subprocess.call(cat_cmd, shell=True)

else:
	##Blast reads against nt
	##Settings
	nt_database = "/home/team_data/Databases/Databases/nt/nt"
	blast_out_file = input_fastq_basename + "_out.blast"
	threads="16"
	##Run
	blast_cmd = "blastn -db "+nt_database+" -query "+fasta_out_file+' -outfmt "6 std qlen slen stitle" -out '+blast_out_file+" -num_threads "+threads
	print blast_cmd
	subprocess.call(blast_cmd, shell=True)

##Awk 90/90 filter the blast results
##Settings
awk_out_file = input_fastq_basename + "_filtered.blast"
##Run
awk_cmd = 'awk -F \"\\t\" \'$3 >= 90 && $4 >= ($13 * .9)\' '+blast_out_file+" > "+awk_out_file
print awk_cmd
subprocess.call(awk_cmd, shell=True)

##Build the krona file
##Settings
krona_tax = "/home/team_data/KronaTools-2.7/taxonomy/"
krona_out_file = input_fastq_basename + "_krona.html"
##Run
krona_cmd = "ktImportBLAST "+awk_out_file+" -tax "+krona_tax+" -o "+krona_out_file
print krona_cmd
subprocess.call(krona_cmd, shell=True)