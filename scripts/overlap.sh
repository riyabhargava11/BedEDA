#!/bin/bash

roi=$1
reference=$2
merged_filename=$3
independent_filename=$4

# Validate input parameters
if [ "$#" -ne 4 ]; then
    echo "Usage: $0 <ROI file> <Reference file> <Merge Output filename> <Independent Output filename>"
    exit 1
fi

# Load the required module
module load BEDTools/2.30.0-GCCcore-10.2.0

# Generate overlap file using bedtools
bedtools intersect -wao -a $roi -b $reference > independent_overlap.bed
head independent_overlap.bed

# Prompt user for column indices
read -p 'Specify columns that correspond to Chromosome, ROI Start, ROI Stop, ROI, Reference, and Overlap Length, in that order (e.g., 1,2,3,4,5,6): ' columns

# Split the columns into an array
IFS=',' read -r -a col_array <<< "$columns"

# Assign columns to variables
chromosome_col=${col_array[0]}
roi_start_col=${col_array[1]}
roi_stop_col=${col_array[2]}
roi_col=${col_array[3]}
reference_col=${col_array[4]}
overlap_length_col=${col_array[5]}

# Process the file and calculate overlap percentage
awk -v start_col=$roi_start_col -v stop_col=$roi_stop_col -v ol_col=$overlap_length_col -F'\t' '
{
    roi_start = $start_col
    roi_stop = $stop_col
    overlap_length = $ol_col
    roi_length = roi_stop - roi_start
    overlap_percentage = (overlap_length / roi_length) * 100
    print $0 "\t" overlap_percentage
}' independent_overlap.bed > independent_overlap3.bed
head independent_overlap3.bed

read -p 'Specify columns that correspond to Chromosome, ROI, Reference, Overlap Length, and Overlap Percentage, in that order (e.g., 1,2,3,4,5): ' columns2
cut -f$columns2 overlap3.bed > $independent_filename


echo "Overlap percentage calculation complete. Output saved to $independent_filename"

head $reference
read -p "We will now use bedtools merge to find any overlap between elements in the reference file. specify columns to include in the merged intervals, aside from chromosome, start point, end point: " columns_merged
bedtools merge -i $reference -c $columns_merged -o distinct > merged_overlap.bed
bedtools intersect -wao -a $roi -b merged_overlap.bed > overlap2.bed

# Display first few lines of the overlap file
head overlap2.bed

# Prompt user for column indices
read -p 'Specify columns that correspond to Chromosome, ROI Start, ROI Stop, ROI, Reference, and Overlap Length, in that order (e.g., 1,2,3,4,5,6): ' columns4

# Split the columns into an array
IFS=',' read -r -a col_array <<< "$columns4"

# Assign columns to variables
chromosome_col=${col_array[0]}
roi_start_col=${col_array[1]}
roi_stop_col=${col_array[2]}
roi_col=${col_array[3]}
reference_col=${col_array[4]}
overlap_length_col=${col_array[5]}

awk -v start_col=$roi_start_col -v stop_col=$roi_stop_col -v ol_col=$overlap_length_col -F'\t' '
{
    roi_start = $start_col
    roi_stop = $stop_col
    overlap_length = $ol_col
    roi_length = roi_stop - roi_start
    overlap_percentage = (overlap_length / roi_length) * 100
    print $0 "\t" overlap_percentage
}' overlap2.bed > overlap3.bed
head overlap3.bed

read -p 'Specify columns that correspond to Chromosome, ROI, Reference, Overlap Length, and Overlap Percentage, in that order (e.g., 1,2,3,4,5): ' columns5
cut -f$columns5 overlap3.bed > $merged_filename

echo "Overlap percentage calculation complete. Output saved to $merged_filename"

#module load miniconda 
#conda activate chromevo_bivalency_2 
#python overlap.py --input_table1 overlap_rep1.bed --input_table2 overlap_rep2.bed
