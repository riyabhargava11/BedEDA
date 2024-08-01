#!/bin/bash

roi=$1

head $roi
read -p 'To create the a summary table to store relevant characterisitics in the same place, specify columns that correspond to Chromosome, ROI Start, ROI Stop, and ROI, in that order (e.g., 1,2,3,4): ' columns

cut -f$columns $roi > summarytable.tsv
sed -i '1i Chromosome\tROI Start\tROI Stop\tROI' summarytable.tsv
head summarytable.tsv

for (( ; ; ))
do
	read -p "Select an analysis: (1) Distance (2) Overlap (3) GC Content (1-3) " num

	if [ "$num" -eq 1 ]; then
		echo "We are now performing an EDA on distances between ROIs and References."
		read -p "Enter the reference file: " reference
		read -p "Enter the output file name: " filename
		bash distances.sh "$roi" "$reference" "$filename"

		#script runs 
		echo "The EDA is complete."
		python_output="python_output_distances.tsv"
		read -p "Would you like extract a column to the summary table? (1) Yes (2) No (1-2): " choice
		if [ "$choice" -eq 1 ]; then 
			module load miniconda
			conda activate chromevo_bivalency_2
			python summary.py --input_table1 summarytable.tsv  --input_table2 python_output_distances.tsv
		fi
	fi
			
	read -p "(1) Continue Session or (2) End Session (Options 1-2): " session
	if [ "$session" -eq 2 ]; then
		echo "Ending Session"
		break
	fi
done

echo "Session Ended"
