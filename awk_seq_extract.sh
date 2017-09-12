#!/bin/bash


awk "/(NC_007880.1|NC_003143.1|NC_027213)/,/^$/" select_agents_ref.fasta >> references.txt

