# BedEDA

# Important Terminology 
Regions of Interest: ROIs refer to any functional genomic annotations that want to characterize by quantifying their nature and relationship with other genomic elements or properties. Using the current iteration of BedEDA, you can measure their distance from other genomic elements, such as promoters, CREs, etc. You can also categorize your ROIs using substring classification.

Reference: Depending on the functionality you use, reference elements can refer to the following: 
  1. Distance: You can calculate the distance between your annotated ROIs and other genomic elements, such as TADs, promoters, CREs, etc. We recommend downloading .bed files containing their chromosome, starting position, and stopping positions from ENCODE or the UCSC genome browser.
  2. Overlap: You can quantify the overlap between your annotated ROIs and other genomic elements, such as promoters, repeat elements, etc. Most often used to quantify the relationship between ROIs and repeat elements, you can also classify reference elements when you use our Overlap functionality and generate a heatmap between the different types of ROIs and different types of references.
  3. CG Content: You can calculate the CG content of your annotated ROIs.

# Preparing Your Files 

## ROI .bed files
BedEDA takes in .bed files to perform different kinds of exploratory data analysis (EDA) on it. To prepare your .bed file for BedEDA, make sure to follow the conventional format: 
1. chromosome name,
2. start position,
3. end position, and 
4. region of interest name.

If you have chromatin signals associated with ROIs, you can also input them into your .bed file for later application of linear regression between ...

## Reference .bed files 

e recommend downloading .bed files containing their chromosome, starting positions, and stopping positions from ENCODE or the UCSC genome browser. Transfer these files into the cluster directory you will be working in, which will be uploaded when the software prompts you. 

## Genome .fa files
To perform the GC Content EDA, keep an unzipped fasta file with the appropriate genome ready to upload.

# External dependencies are contained in environment.yml


```
conda env create -f environment.yml
```

To activate the environment, 
```
module load miniconda
conda activate bedEDA_environment
```


# Substring Classification
Substring classification is the task of assigning labels to specific substrings within a larger string based on their content or context.

