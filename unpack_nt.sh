#!/bin/bash
for i in 0{1..9} {10..43}
  do
    blastdbcmd -db /mnt/Passport1/Databases/nt/nt.$i -out /home/mfeltz/workdir/nt_fastas/nt.${i}.fasta -outfmt %f -entry 'all'
  done

