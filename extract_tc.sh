#!/bin/bash -l

#Time limit
#$ -l h_rt=10:00:00

#Specify the name of the job
#$ -N extract_tc

#Send email report at the end of the job
#$ -m e

#Load modules:
module purge
module load R/3.3.0
module load gdal/1.11.3

#Run the program
Rscript /usr3/graduate/shijuan/Desktop/my_ABOVE_git/extract_tc.R

