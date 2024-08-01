#!/bin/python


import pandas as pd
import sys
import argparse
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm

parser=argparse.ArgumentParser()

parser.add_argument('--input_table1', required=True, help='Path to input the summary table file')
parser.add_argument('--input_table2', required=True, help='Path to input output file')

args=parser.parse_args()

sum = pd.read_csv(args.input_table1,  delimiter='\t')
df = pd.read_csv(args.input_table2,  delimiter=',')

print(df.head())
print("\nColumns:")
for i, col in enumerate(df.columns):
    print(f"{i}: {col}")

column_numbers = input("Please enter the column numbers you want to extract, separated by commas: ")

# Convert the input string into a list of integers
column_numbers = [int(num.strip()) for num in column_numbers.split(',')]

# Validate the column numbers
valid_columns = [num for num in column_numbers if 0 <= num < len(df.columns)]
if not valid_columns:
    print("No valid column numbers entered.")
else:
    # Extract the column names using the column numbers
    column_names = [df.columns[num] for num in valid_columns]

     # Ask the user for new column names
    new_column_names = []
    for col in column_names:
        new_name = input(f"Enter a new name for the column '{col}': ")
        new_column_names.append(new_name if new_name else col)
    
    # Set the index of the dataframe to ROI
    df.set_index('ROI', inplace=True)
    
    # Extract the desired columns
    extracted_columns = df[column_names]
    extracted_columns.columns = new_column_names

    
    # Transfer the columns to the summary table
    sum = sum.join(extracted_columns, how='left')
    
    # Save the updated summary table back to the file
    sum.to_csv('summarytable.tsv', sep='\t')
    print(sum.head())    
    print(f"Columns '{', '.join(column_names)}' have been transferred to the summary table.")
