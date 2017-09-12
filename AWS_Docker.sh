#!/bin/bash

#Required programs:
#
# blast
# kronatools

# required databases
#
# nt
# krona taxonomy

data_folder=$1
result_folder=$2
run_one=$3

#Adjust directories for associated databases on machine
ntdbdir="/home/databases/nt/nt"
#ntdbdir="/mnt/Passport1/Databases/nt/nt"
kronatax="/home/KronaTools-2.7/taxonomy"
#kronatax="/home/team_data/KronaTools-2.7/taxonomy"

#DEFAULT VARIABLES
threads=`nproc`
fastaext=".fasta"
TIME_FILE_NAME="Process_time.txt"
OLDIFS="$IFS"
nt="nt"
blast=".blast"
underscore="_"
default="defaultsettings"
krona="_krona.html"
fastq=".fastq"
fasta=".fasta"
blast_folder="blast_output"
krona_folder="krona_output"
slash="/"
filtered="_filtered"
taxTab="taxonomy.tab"
acc2Tax="all.accession2taxid.sorted"

# functions
function quit {
	exit
}

function foldermake {
if [ ! -d "$result_folder" ]; then
        echo "$result_folder does not exist, making folder now"
		mkdir $result_folder
else
        echo "$result_folder exists"
fi

if [ ! -d "$result_folder$slash$blast_folder$underscore$timestamp" ]; then
        echo "$result_folder$slash$blast_folder$underscore$timestamp does not exist, making folder now"
        mkdir $result_folder$slash$blast_folder$underscore$timestamp
else
        echo "$result_folder$slash$blast_folder$underscore$timestamp exists"
fi

if [ ! -d "$result_folder$slash$krona_folder$underscore$timestamp" ]; then
        echo "$result_folder$slash$krona_folder$underscore$timestamp does not exist, making folder now"
        mkdir $result_folder$slash$krona_folder$underscore$timestamp
else
        echo "$result_folder$slash$krona_folder$underscore$timestamp exists"
fi
}

function datafolderread() {
echo "The following files will be processed"
string=$1
array=($@)
for j in ${array[@]};
do
	if [[ $j == *.fasta ]] || [[ $j == *.fa ]] || [[ $j == *.fastq ]]; then
		echo $j
	fi
done
}

#default NT blast
function dent {
        echo "Processing file through Blast NT default settings"
		blastntdefstarttime=$(date -u +"%s")
		finalblastfile=$result_folder$slash$blast_folder$underscore$timestamp$slash$sample_name$underscore$default$underscore$nt$blast
        blastn -db $ntdbdir -query $file -outfmt "6 std qlen slen stitle" -out $finalblastfile -num_threads $threads
        blastntdefendtime=$(date -u +"%s")
        blastntdefdiff=$(($blastntdefendtime-$blastntdefstarttime))
        echo "It took $(($blastntdefdiff / 60)) minutes and $(($blastntdefdiff % 60)) seconds to perform the NT blast with default settings ($blastntdefdiff seconds)." >> $TIME_FILE
		blastntdeffilterstarttime=$(date -u +"%s")
		awk -F "\t" '$3 >= 90 && $4 >= ($13 * .9)' $finalblastfile > $finalblastfile$filtered
		blastntdeffilterendtime=$(date -u +"%s")
		blastntdeffilterdiff=$(($blastntdeffilterendtime-$blastntdeffilterstarttime))
		echo "It took $(($blastntdeffilterdiff / 60 )) minutes and $(($blastntdeffilterdiff % 60)) seconds to perform the 90x90 filtering ($blastntdeffilterdiff seconds)." >>$TIME_FILE
		blastntdefkronastarttime=$(date -u +"%s")
		ktImportBLAST $finalblastfile$filtered -tax $kronatax -o $result_folder$slash$krona_folder$underscore$timestamp$slash$sample_name$underscore$nt$underscore$default$krona
		blastntdifkronaendtime=$(date -u +"%s")
		blastntdefkronadiff=$(($blastntdifkronaendtime-$blastntdefkronastarttime))
		echo "It took $(($blastntdefkronadiff / 60 )) minutes and $(($blastntdefkronadiff % 60)) seconds to perform the krona plot ($blastntdefkronadiff seconds)." >> $TIME_FILE
}

# Program start
##Download the files from s3
aws s3 sync s3://rioja-blast-testing/nt /home/databases/nt/ --exclude '*.tar.gz*'
aws s3 sync s3://rioja-blast-testing/taxonomy $kronatax
aws s3 sync s3://rioja-blast-testing/NBC01_2.5 /home/mfeltz/NBC01_2.5/
aws s3 sync s3://rioja-blast-testing/NBC01_5 /home/NBC01_5/

##Run the analysis
timestamp=$( date +%Y%m%d_%H%M%S )
foldermake
TIME_FILE=$result_folder$slash$timestamp$opt$underscore$TIME_FILE_NAME
filetoprocess=$data_folder$slash$run_one
IFS='/' read -ra ADDR <<< "$filetoprocess"
samplename=${ADDR[-1]}
IFS='.' read -ra ADDR <<< "$samplename"
sample_name=${ADDR[0]}
starttime=$(date -u +"%s")
echo "Working on $filetoprocess through analysis" >> $TIME_FILE
echo >> $TIME_FILE	
file=$data_folder$slash$sample_name$fasta
cat $filetoprocess | awk 'NR%4==1{printf ">%s\n", substr($0,2)}NR%4==2{print}' > $file
dent
echo "It took $(($diff / 60)) minutes and $(($diff % 60)) seconds to perform the screening analysis on $data_folder." >> $TIME_FILE

##Sync the results to S3
aws s3 sync $result_folder s3://rioja-blast-testing/NBC01_Batch_Results/
aws s3 cp $TIME_FILE_NAME s3://rioja-blast-testing/NBC01_Batch_Results/$run_one$TIME_FILE_NAME