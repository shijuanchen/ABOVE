#!/bin/bash -l

#Time limit
#$ -l h_rt=10:00:00

#Specify the name of the job
#$ -N rf_training

#input tile name
tile_name=$1

#Load modules:
module purge
module load R/R-3.1.1

#Run the program
Rscript /usr3/graduate/shijuan/Desktop/my_ABOVE_git/mk_training/extract_tc_FN.R "$tile_name"
echo "extract_tc_FN for tile $tile_name  done."
Rscript /usr3/graduate/shijuan/Desktop/my_ABOVE_git/mk_training/shp_to_csv_FN.R "$tile_name"
echo "shp_to_csv_FN for tile $tile_name  done."
Rscript /usr3/graduate/shijuan/Desktop/my_ABOVE_git/mk_training/combine_train_csv_FN.R "$tile_name"
echo "combine_train_csv_FN for tile $tile_name  done."
