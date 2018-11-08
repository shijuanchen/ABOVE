#!/bin/bash -l
#$ -V
#$ -l h_rt=48:00:00
#$ -N mask_4type
#$ -j y
#$ -l mem_total=128G
#$ -pe omp 8

#input tile name
if [ -z "$1" ];
then
    echo "Input error!"
    exit 1
else
    tile_name=$1
fi

$out_dir="/projectnb/landsat/projects/ABOVE/CCDC/$tile_name/out_tc_4type"
if [ ! -d $out_dir ];
then
    mkdir $out_dir
fi

#Load modules:
module purge
module load R/R-3.1.1

#Run the program
Rscript /usr3/graduate/shijuan/Desktop/my_ABOVE_git/mask_4types_pre_v2.R "$tile_name"

