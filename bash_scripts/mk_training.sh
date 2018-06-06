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
Rscript /usr3/graduate/shijuan/Desktop/my_ABOVE_git/extract_tc.R "$tile_name"
echo "extract_tc done."
Rscript /usr3/graduate/shijuan/Desktop/my_ABOVE_git/shp_to_csv.R "$tile_name"
echo "shp_to_csv done."
Rscript /usr3/graduate/shijuan/Desktop/my_ABOVE_git/combine_train_csv.R "$tile_name"
echo "combine_train_csv done."
