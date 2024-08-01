#!/bin/bash

roi=$1
fasta=$2
filename=$3

module load BEDTools/2.30.0-GCCcore-10.2.0

bedtools nuc -fi $fasta -bed $roi > gc.bed

head gc.bed

read -p 'Specify columns that correspond to Chromosome, ROI, and GC Content, in that order (e.g. 1,2,3): ' columns
cut -f$columns gc.bed > $filename

module load miniconda
conda activate chromevo_bivalency_2
python gc.py --input_table $filename
