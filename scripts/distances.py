#!/bin/python


import pandas as pd
import sys
import argparse
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm

parser=argparse.ArgumentParser()

parser.add_argument("--input_table", type=str, help="bedtools intersect output file name")

args=parser.parse_args()

df = pd.read_csv(args.input_table, sep = '\t', header=None, names=["Chromosome", "ROI", "Reference Name", "Distance"])

output_table = input("Name your output table (without extension): ") + ".tsv"
df.to_csv(output_table)

def classification(df):
    # Dictionary to store substrings and their categories
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
	df['Category'] = df['ROI'].apply(classify_name)
    
	return df

classification(df)
# creating a data distribution
df = df.sort_values('Distance')


def distance_dist(df):
	sns.kdeplot(df['Distance'], color='r', shade=True, label='Distance', cmap="Reds", thresh=0.05)

	plt.xlabel('Distance')
	plt.ylabel('Distribution Density')
	plt.title('Distance Distribution for all ROI types')
    
    # Add a legend
	plt.legend()

    # Prompt the user for the output file name
	output_file = input("Name your output file (without extension): ") + ".png"
	dpi = 300 
	plt.savefig(output_file, dpi=dpi)
	plt.show()

#sns.distance_dist(df).figure.savefig('output_plot.png', dpi=300)


def distance_per_roi(df):
	sns.set(style="whitegrid")
	#fa_palette = sns.color_palette("husl", df['Category'].nunique())
	
	# Create a figure and set the size
	plt.figure(figsize=(10, 6))
	# Create a KDE plot for each category
	#for category in df['Category'].unique():
	#	subset = df[df['Category'] == category]
	sns.kdeplot(data=df, x='Distance', hue= "Category", palette="Set2", fill=True, common_norm=False, alpha=0.35)
#plt.title('CHR 12: Density of GC Content Distribution for Different ROIs')  # Adds a title
	plt.xlabel('Distance')  # Label for the x-axis
	plt.ylabel('Density')  # Label for the y-axis
#	plt.legend(title='Category')  # Adds a legend with a title
#plt.show()  # Displays the plot

# Setting the axis limits
# plt.xlim(0, 2000000)  # Adjust these values based on the region you are interested in
# plt.ylim(0, 0.0001)    # Adjust these values to zoom vertically
    # Prompt the user for the output file name
	output_file = input("Name your output file (without extension): ") + ".png"
	dpi = 300
	plt.savefig(output_file, dpi=dpi)
	plt.show()	


def distance_boxplot(df):
    # Create a dictionary of dataframes for each category
	categories = {}
	for category in df['Category'].unique():
		categories[category] = df[df['Category'] == category]['Distance']
    
    # Sort categories by their names to maintain order in the plot
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
	plt.xlabel('Category')
	plt.ylabel('Distance')
	plt.grid(True)

    # Prompt the user for the output file name
	output_file = input("Name your output file (without extension): ") + ".png"
	dpi = 300  # Set a default dpi for saving the figure

    # Save the plot
	plt.savefig(output_file, dpi=dpi)
	plt.show()


def chromosome_wise(df):
	df = df.sort_values('Chromosome').reset_index(drop=True)
    
    # Get user input for chromosomes
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


	if choice2 == "1":
		sns.set(font_scale=.5)
		sns.set_style(style="white")
		
		# Determine the grid size based on the number of chromosomes
		num_chromosomes = len(chromosome_dict)
		grid_size = int(num_chromosomes**0.5) + 1
		
		fig, axes = plt.subplots(grid_size, grid_size, figsize=(30, 20))

		for idx, (chr_name, df_chr) in enumerate(chromosome_dict.items()):
			row, col = divmod(idx, grid_size)
			ax = axes[row, col]
			sns.kdeplot(df_chr['Distance'], ax=ax, color='r', shade=True, label='Distance', cmap="Reds", thresh=0.05)
			ax.set_title(chr_name)
			ax.legend()

		# Hide any unused subplots
		for i in range(num_chromosomes, grid_size**2):
			row, col = divmod(i, grid_size)
			fig.delaxes(axes[row, col])

		plt.tight_layout()
		output_file = input("Name your output file (without extension): ") + ".png"
		dpi = 300
		plt.savefig(output_file, dpi=dpi)
		plt.show()
		
	elif choice2 == "2":
		sns.set(font_scale=.5)
		sns.set_style(style="white")
		    
		    # Determine the grid size based on the number of chromosomes
		num_chromosomes = len(chromosome_dict)
		grid_size = int(num_chromosomes**0.5) + 1
		    
		fig, axes = plt.subplots(grid_size, grid_size, figsize=(30, 20))

		for idx, (chr_name, df_chr) in enumerate(chromosome_dict.items()):
			row, col = divmod(idx, grid_size)
			ax = axes[row, col]
			sns.kdeplot(data=df_chr, x='Distance', hue='Category', fill=True, alpha=0.3, ax=ax, legend=(idx == 0))
			ax.set_title(chr_name)

		    # Hide any unused subplots
		for i in range(num_chromosomes, grid_size**2):
		    row, col = divmod(i, grid_size) 
		    fig.delaxes(axes[row, col])

		plt.tight_layout()
		output_file = input("Name your output file (without extension): ") + ".png"
		dpi = 300
		plt.savefig(output_file, dpi=dpi)
		plt.show()

	else:
		choicelog = input("Calculate on log scale?: \n1. Yes \n2. No \n(Option 1-2): ")
		print(choicelog)
		category_distances = {category: [] for category in df['Category'].unique()}
		for chr in chrom:
			for category in df['Category'].unique():
				df_chr = chromosome_dict.get(chr, pd.DataFrame())
				category_distances[category].append(df_chr[df_chr['Category'] == category]['Distance'])
		plt.figure(figsize=(12, 8))
		for i, category in enumerate(df['Category'].unique(), 1):
		    plt.subplot(2, 2, i)
		    plt.boxplot(category_distances[category], notch=True, patch_artist=True)
		    plt.title(category)
		    if choicelog == "1":
		    	plt.yscale('log')
#		    else:
#		    	break
		    plt.xlabel('Chromosomes')
		    plt.ylabel('Distance')
		plt.tight_layout()
		output_file = input("Name your output file (without extension): ") + ".png"
		plt.savefig(output_file, dpi=300)
		plt.show()

choice1 = input("Select one of the following options(1-4): \n1. Genome-wide \n2. By-Chromosome \nOption(1-2): ")
print(choice1)
if choice1 == "1":
	choice2 = input("Select one of the following options(1-4): \n1. KDE \n2. KDE per ROI \n3. Boxplot? \nOption(1-3): ")
	print(choice2)
	if choice2 == "1":
		distance_dist(df)
	elif choice2 == "2":
		distance_per_roi(df)
	else:
		choicelog = input("Calculate on log scale?: \n1. Yes \n2. No \n(Option 1-2): ")
		print(choicelog)
		distance_boxplot(df)
	
else: 
	choice2 = input("Select one of the following options(1-4): \n1. KDE \n2. KDE per ROI \n3. Boxplot? \nOption(1-4): ")
	print(choice2)
	chromosome_wise(df)
