#!/bin/bash

roi=$1
reference=$2
filename=$3

module load BEDTools/2.30.0-GCCcore-10.2.0

bedtools closest -d -a $roi \
                     -b $reference > distances.bed

head distances.bed 

read -p 'Specify columns that correspond to Chromosome, ROI, Reference, and Distance, in that order (e.g. 1,2,8,9): ' columns

cut -f$columns distances.bed > $filename

module load miniconda
conda activate chromevo_bivalency_2
python distances.py --input_table $filename
