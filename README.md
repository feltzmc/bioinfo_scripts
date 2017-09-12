# bioinfo_scripts

HEREIN: An explanation of what each script is supposed to do (most are in working order, some have hard coded paths that may need to be changed)

-awk_seq_extract.sh
Awk one-liner to do the same thing as extract_fasta_seqs.py

-AWS_Docker.sh
Script to run blast tests on AWS

-blast_pipeline.py
Trims reads using trimGalore, Remove PhiX reads using bowtie2, Converts the input fastq to fasta (Note: should be updated to check if file is fastq), Split readfile into multiple parts, 
Blast reads against nt using one command per part, submits jobs to background and waits til all are finished, joins the result parts back together, Awk 90/90 filters the blast results, builds krona plot

-download_all_bacteria.py
Downloads all complete bacterial genomes from genbank, counts downloads done, skips assemblies it sees are already downloaded

-Equalize_Paired_Reads.py
Takes two fastq files with paired reads that have been trimmed to different lengths, finds the shorter read for each pair and trims both reads and qualities to that length

-extract_fasta_seqs.py
Script that extracts sequences with desired accessions from a given fasta file, can be done instead with a one liner awk command

-fasta_map_taxonomy.py
Supposed to manually make a taxid2accession file, DOESN'T WORK

-fasta_to_fastq.pl
Written by someone else, converts a fasta readile to a fastq readfile by adding spaces and maximum quality score

-fix_accessions.py
Useful script, iterates through an acc2tax.map file, finds accessions where the version is > 1, adds all previous versions for that accession to the map file
For example NC_400813.5 would become:  NC_400813.5, NC_400813.4, NC_400813.3, NC_400813.2, NC_400813.1 so all versions map to one taxid

-fix_fasta_seqids.py
I think this was supposed to try and fix the acc2tax issues on the fasta side by replacing all accessions in the fasta with the correct version, fix_accessions is a more permanent solution and works better

-get_taxid_from_accession.py
Given a list of accessions and 'nucl_gb.accession2taxid', make an acc2tax mapping file

-make_contig_mags.py
Iterate through a contigs fasta file, make a mags file for use with krona tools, maps the seq_id to the length of the sequence

-make_kraken_fasta.py
Edits a given fasta file (hardcoded) to add Kraken specific tags to the fasta sequence ids

-Make_Slimm_FASTA.py
Makes a FASTA file compatible with the SLIMM tool

-SAM_Best_Hit_Filter.py
Supposed to iterate through a SAM file and grab only the best hit for each read, not sure it works

-SAM_Count_Hits
Iterate through a SAM file and for each read print the readname, number of hits, and sum_length of sequences matched (mainly used with mapping contigs)

-unpack_nt.sh
Simple loop to unpack nt blast database into a fasta

-whoosh_indexer.py
Makes use of Python's whoosh library to index and search PubMed XML files
