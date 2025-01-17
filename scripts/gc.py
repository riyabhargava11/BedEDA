#!/bin/python


import pandas as pd
import sys
import argparse
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image, Spacer, PageBreak
import os

parser=argparse.ArgumentParser()

parser.add_argument('--input_table', required=True, help='Path to the input BED file')

args=parser.parse_args()

df = pd.read_csv(args.input_table, sep = '\t', header=None, names=["Chromosome", "ROI", "GC Content"])
output_table = input("Your output table will now be saved as a tsv. Enter a filename (without extension): ") 
output = output_table + ".tsv"
df.to_csv(output)

def classification(df):
    # Dictionary to store substrings and their categorize
    
	substrings = {}
    
    # Function to get user input for substrings and categories
	def get_user_input():
		while True:
			substring = input("Enter a substring to look for (or type 'done' to finish): ")
			if substring.lower() == 'done':
 				break
			category = input(f"Enter the category for the substring '{substring}': ")
			substrings[substring.lower()] = category
    
    # Function to classify based on substrings
	def classify_name(name):
		for key, value in substrings.items():
			if key in name.lower():
				return value
		return "Unknown"  # Default category if no substring matches
    
    # Get user inputs
	get_user_input()
    
    # Apply classification
	df['ROI Category'] = df['ROI'].apply(classify_name)
    
	return df
ROI_choice = input("Do you want to categorize your ROIs? \n1. Yes \n2. No \nOptions(1-2): ")
if ROI_choice == "1":
	print("Classification for  the independent dataframe")
	classification(df)
	print("Your ROIs have been classified.")
else: 
    print("Your ROIs are unclassified.")

#Filtering out unclassified ROIs
filtered_df = df[df['ROI Category'] != 'Unknown']

#EDA 
#Genome Wide KDE Analysis
def genome_KDE(df):
	sns.kdeplot(df['GC Content'], color='r', shade=True, label='Overlap', cmap="Reds", thresh=0.05)

	plt.xlabel('GC Content(%)')
	plt.ylabel('Distribution Density')
	plt.title('Overlap Percentage Distribution for all ROI types')
    
    # Add a legend
	plt.legend()

    # Prompt the user for the output file name
	output_file_genome_KDE = output_table + "_genome_KDE.png"
	dpi = 300 
	plt.savefig(output_file_genome_KDE, dpi=dpi)
	plt.show()
	elements.append(Image(output_file_genome_KDE, width=400, height=300))       

#Genome wide KDE, per ROI Type 
def genome_KDE_per_roi(df):
	sns.set(style="whitegrid")
	plt.figure(figsize=(10, 6))
	sns.kdeplot(data=df, x='GC Content', hue= "ROI Category", palette="Set2", fill=True, common_norm=False, alpha=0.35)
	plt.xlabel('GC Content(%)')  # Label for the x-axis
	plt.ylabel('Density')  # Label for the y-axis
	plt.title('GC Content Distribution ROI type-wise')
  
	output_file_genome_KDE_per_roi = output_table + "_genome_KDE_per_roi.png"
	dpi = 300
	plt.savefig(output_file_genome_KDE_per_roi, dpi=dpi)
	plt.show()
	elements.append(Image(output_file_genome_KDE_per_roi, width=400, height=300))
#    print("Genome-wide KDE per ROI complete.")

#Genome wide Boxplots, per ROI type
def genome_roi_boxplot(df):
	categories = {}
	for category in df['ROI Category'].unique():
		categories[category] = df[df['ROI Category'] == category]['GC Content']
	sorted_categories = sorted(categories.keys())
    
  # Extract the data and labels for the boxplot
	data = [categories[category] for category in sorted_categories]
	labels = sorted_categories

  # Plot the boxplot
	plt.figure(figsize=(10, 6))
	box = plt.boxplot(data, notch=True, patch_artist=True, labels=labels)
	if choicelog == "1":
		plt.yscale('log')
#	else:
#		break
	plt.xlabel('ROI Category')
	plt.ylabel('GC Content(%)')
	plt.title('GC Content % Distribution Boxplots ROI-wise')
	plt.grid(True)

    # Prompt the user for the output file name
	output_file_genome_roi_boxplot = output_table + "_genome_roi_boxplot.png"
	dpi = 300  # Set a default dpi for saving the figure

    # Save the plot
	plt.savefig(output_file_genome_roi_boxplot, dpi=dpi)
	plt.show()
	elements.append(Image(output_file_genome_roi_boxplot, width=400, height=300))
#    print("Genome-wide Boxplots per ROI complete.")


#Chromosome-wise analysis 
def chromosome_wise(df,df2):
	df = df.sort_values('Chromosome').reset_index(drop=True)
    
    # Get user input for chromosomes
	chrom_choice = input("Number of Chromosomes: Select a species, or, to input a custom number of chromosomes, select 'Custom': \n1. Human \n2. Rhesus Macaque \n3. Rat \n4. Opossum \n5. Mouse \n6. Bull \n.7. Custom \nOption(1-7): ")
	if chrom_choice == "1":
		user_input = "chr1, chr2, chr3, chr4, chr5, chr6, chr7, chr8, chr9, chr10, chr11, chr12, chr13, chr14, chr15, chr16, chr17, chr18, chr19, chr20, chr21, chr22, chrX, chrY"
	elif chrom_choice == "2": 
		user_input = "chr1, chr2, chr3, chr4, chr5, chr6, chr7, chr8, chr9, chr10, chr11, chr12, chr13, chr14, chr15, chr16, chr17, chr18, chr19, chr20, chrX, chrY"
	elif chrom_choice == "3":
		user_input = "chr1, chr2, chr3, chr4, chr5, chr6, chr7, chr8, chr9, chr10, chr11, chr12, chr13, chr14, chr15, chr16, chr17, chr18, chr19, chr20, chrX, chrY"
	elif chrom_choice == "4":
		user_input = "chr1, chr2, chr3, chr4, chr5, chr6, chr7, chrUn, chrX, chrY"
	elif chrom_choice == "5":
		user_input = "chr1, chr2, chr3, chr4, chr5, chr6, chr7, chr8, chr9, chr10, chr11, chr12, chr13, chr14, chr15, chr16, chr17, chr18, chr19, chrX, chrY"
	elif chrom_choice == "6": 
		user_input = "chr1, chr2, chr3, chr4, chr5, chr6, chr7, chr8, chr9, chr10, chr11, chr12, chr13, chr14, chr15, chr16, chr17, chr18, chr19, chr20, chr21, chr22, chr23, chr24, chr25, chr26, chr27, chr28, chr29, chrX, chrY"
	else:
		user_input = input("Enter the chromosomes you want to use, separated by commas (e.g., 'chr1, chr2, chr3'): ")
    
	chrom = [x.strip() for x in user_input.split(',')]
    
    # Check if the entered chromosomes are present in the DataFrame
	valid_chromosomes = df['Chromosome'].unique()
	chromosome_dict = {}

	for chr in chrom:
		df_chr = df[df['Chromosome'] == chr].reset_index(drop=True)
        # Use exec() to dynamically create variables
		exec(f"df_{chr.replace(' ', '_').lower()} = df_chr")

		chromosome_dict[chr] = df_chr
	for chr in chrom: 
		df2_chr = df2[df2['Chromosome'] == chr].reset_index(drop=True)
		exec(f"df2_{chr.replace(' ', '_').lower()} = df2_chr")
		chromosome_dict[chr] = df2_chr
        
	def chromosome_KDE(df):
		sns.set(font_scale=.5)
		sns.set_style(style="white")
		
		# Determine the grid size based on the number of chromosomes
		num_chromosomes = len(chromosome_dict)
		grid_size = int(num_chromosomes**0.5) + 1
		
		fig, axes = plt.subplots(grid_size, grid_size, figsize=(30, 20))

		for idx, (chr_name, df_chr) in enumerate(chromosome_dict.items()):
			row, col = divmod(idx, grid_size)
			ax = axes[row, col]
			sns.kdeplot(df_chr['GC Content'], ax=ax, color='r', shade=True, label='Overlap %', cmap="Reds", thresh=0.05)
			ax.set_title(chr_name)
			ax.legend()

		# Hide any unused subplots
		for i in range(num_chromosomes, grid_size**2):
			row, col = divmod(i, grid_size)
			fig.delaxes(axes[row, col])

		plt.tight_layout()
		output_file_chromosome_kde = output_table + "_chromosome_kde.png"
		dpi = 300
		plt.savefig(output_file_chromosome_kde, dpi=dpi)
		plt.show()

		elements.append(Image(output_file_chromosome_kde, width=400, height=300))
		elements.append(space)

        
	def chromosome_kde_per_roi(df):
		sns.set(font_scale=.5)
		sns.set_style(style="white")
		    
		    # Determine the grid size based on the number of chromosomes
		num_chromosomes = len(chromosome_dict)
		grid_size = int(num_chromosomes**0.5) + 1
		    
		fig, axes = plt.subplots(grid_size, grid_size, figsize=(30, 20))

		for idx, (chr_name, df_chr) in enumerate(chromosome_dict.items()):
			row, col = divmod(idx, grid_size)
			ax = axes[row, col]
			sns.kdeplot(data=df_chr, x='GC Content', hue='ROI Category', fill=True, alpha=0.3, ax=ax, legend=(idx == 0))
			ax.set_title(chr_name)

		    # Hide any unused subplots
		for i in range(num_chromosomes, grid_size**2):
		    row, col = divmod(i, grid_size) 
		    fig.delaxes(axes[row, col])

		plt.tight_layout()
		output_file_chromosome_kde_per_roi = output_table + "_chromosome_kde_per_roi.png"
		dpi = 300
		plt.savefig(output_file_chromosome_kde_per_roi, dpi=dpi)
		plt.show()

		elements.append(Image(output_file_chromosome_kde_per_roi, width=400, height=300))
		page_break = PageBreak()

	def chromosome_boxplot_per_roi(df):
#		choicelog = input("Calculate on log scale?: \n1. Yes \n2. No \n(Option 1-2): ")
#		print(choicelog)
		category_distances = {category: [] for category in df['ROI Category'].unique()}
		for chr in chrom:
			for category in df['ROI Category'].unique():
				df_chr = chromosome_dict.get(chr, pd.DataFrame())
				category_distances[category].append(df_chr[df_chr['ROI Category'] == category]['GC Content'])
		plt.figure(figsize=(12, 8))
		for i, category in enumerate(df['ROI Category'].unique(), 1):
		    plt.subplot(2, 2, i)
		    plt.boxplot(category_distances[category], notch=True, patch_artist=True)
		    plt.title(category)
		    if choicelog == "1":
		    	plt.yscale('log')
#		    else:
#		    	break
		    plt.xlabel('Chromosomes')
		    plt.ylabel('GC Content%')
		plt.tight_layout()
		output_file_chromosome_boxplot_per_roi = output_table + "_chromosome_boxplot_per_roi.png"
		plt.savefig(output_file_chromosome_boxplot_per_roi, dpi=300)
		plt.show()

		elements.append(Image(output_file_chromosome_boxplot_per_roi, width=400, height=300))
		page_break = PageBreak()

#making the pdf file 
pdf_file = output_table + '.pdf'  # Save the PDF in the current directory
pdf = SimpleDocTemplate(pdf_file, pagesize=letter)
elements = []

#defining a spacer
space = Spacer(width=0, height=20)  # 20 units of vertical space

#appending the figures
genome_KDE(filtered_df)
elements.append(space)

genome_KDE_per_roi(filtered_df)
page_break = PageBreak()
#elements.append(Image(output_file_genome_KDE_per_roi, width=400, height=300))
#elements.append(Image([[' ']] * 3))

choicelog = input("Calculate on log scale?: \n1. Yes \n2. No \n(Option 1-2): ")
print(choicelog)

genome_roi_boxplot(filtered_df)
page_break = PageBreak()
#elements.append(Image(output_file_genome_roi_boxplot, width=400, height=300))
#elements.append(Image([[' ']] * 3))

chromosome_wise(filtered_df)

# Build the PDF
pdf.build(elements)

print(f'PDF saved to {os.path.abspath(pdf_file)}')

