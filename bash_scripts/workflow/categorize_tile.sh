#!/bin/bash -l
#$ -V
#$ -l h_rt=48:00:00
#$ -N categorize_FF_NF_NN
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

tile=$1
out_dir="/projectnb/landsat/projects/ABOVE/CCDC/$tile/out_category"
if [ ! -d "$out_dir" ];
then
    mkdir $out_dir
fi
module purge
source /projectnb/landsat/users/shijuan/miniconda3/bin/activate yatsm_v0.6_par
python /usr3/graduate/shijuan/Desktop/my_ABOVE_git/categorize_FF_NF_NN_v3.py --tile_name $tile
source deactivate
