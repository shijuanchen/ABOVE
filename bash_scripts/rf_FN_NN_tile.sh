#!/bin/bash -l

#Time limit
#$ -l h_rt=10:00:00

#Specify the name of the job
#$ -N rf_FN_NN

#input tile name
tile_name=$1

#Load modules:
module purge
module load R/R-3.1.1

#Run the program
Rscript /usr3/graduate/shijuan/Desktop/my_ABOVE_git/rand_forest_classify_dist.R "$tile_name"

