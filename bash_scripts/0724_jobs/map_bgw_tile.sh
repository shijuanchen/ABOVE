#!/bin/bash -l
#$ -V
#$ -l h_rt=48:00:00
#$ -N map_bgw
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

out_tc_dir="/projectnb/landsat/projects/ABOVE/CCDC/$tile/out_tc_pre"
if [ ! -d $out_tc_dir ];
then
    mkdir /projectnb/landsat/projects/ABOVE/CCDC/$tile/out_tc_pre
fi
module purge
source /projectnb/landsat/users/shijuan/miniconda3/bin/activate yatsm_v0.6_par
python /usr3/graduate/shijuan/codes/above/yatsm_v0.6_par/yatsm/mapping/plot_bgw.py --tile_name $tile
source deactivate

echo "Finished submitting tile $tile"
