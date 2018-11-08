#!/bin/bash -l
#$ -V
#$ -l h_rt=48:00:00
#$ -N rf_FN_NN
#$ -j y
#$ -l mem_total=128G
#$ -pe omp 8

if [ -z "$1" ];
then
    echo "Input error!"
    exit 1
else
    tile=$1
fi

#input tile name
tile_name=$1
out_dir="/projectnb/landsat/projects/ABOVE/CCDC/$tile/out_category"
if [ ! -d "$out_dir" ];
then
    mkdir $out_dir
fi

#Load modules:
module purge
module load R/R-3.1.1

#Run the program
Rscript /usr3/graduate/shijuan/Desktop/my_ABOVE_git/rand_forest_classify_dist.R "$tile_name"

