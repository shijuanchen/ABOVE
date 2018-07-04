#!/bin/bash -l

#Time limit
#$ -l h_rt=48:00:00

#Specify the name of the job
#$ -N mask_4typest

#input tile name
tile_name=$1

$out_dir="/projectnb/landsat/projects/ABOVE/CCDC/$tile/out_tc_4type"
if [ ! -d $out_dir ];
then
    mkdir $out_dir
fi

#Load modules:
module purge
module load R/R-3.1.1

#Run the program
Rscript /usr3/graduate/shijuan/Desktop/my_ABOVE_git/mask_4types_pre_v2.R "$tile_name"

