#!/bin/bash -l

#Time limit
#$ -l h_rt=10:00:00

#Specify the name of the job
#$ -N mask_non_forest

#Send email report at the end of the job
#$ -m e

#Load modules:
module load R/R-3.1.1

#Run the program
Rscript /usr3/graduate/shijuan/Desktop/my_ABOVE_git/mask _nonforest_pre.R

