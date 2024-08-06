#!/bin/python

import pandas as pd
import sys
import argparse
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm

parser = argparse.ArgumentParser()

parser.add_argument('--input_table1', required=True, help='Path to input the summary table file')
parser.add_argument('--input_table2', required=True, help='Path to input the output file')

args = parser.parse_args()

summary_table = pd.read_csv(args.input_table1, delimiter='\t')
df = pd.read_csv(args.input_table2, delimiter=',')

print(df.head())
print("\nColumns:")
for i, col in enumerate(df.columns):
    print(f"{i}: {col}")

roi_column = int(input("Enter the column number that corresponds to the ROIs: "))
column_name = df.columns[roi_column]
df.rename(columns={column_name: 'ROI'}, inplace=True)

variable_column = input("Please enter the column numbers you want to extract, separated by commas: ")
variable_column = [int(num.strip()) for num in variable_column.split(',')]
column_names = [df.columns[num] for num in variable_column]
new_column_names = []
for col in column_names:
    new_name = input(f"Enter a new name for the column '{col}': ")
    new_column_names.append(new_name if new_name else col)

# Set the index of the dataframe to ROI
df.set_index('ROI', inplace=True)

# Extract the desired columns
extracted_columns = df[column_names]
extracted_columns.columns = new_column_names

summary_table = pd.merge(summary_table, extracted_columns, on='ROI', how='left')

# Save the updated summary table back to the file
summary_table.to_csv('summarytable.tsv', sep='\t')
print(summary_table.head())
print(f"Columns '{', '.join(column_names)}' have been transferred to the summary table.")
