#!/bin/bash -l
#$ -V
#$ -l h_rt=24:00:00
#$ -N map_bgw
#$ -j y
#$ -l mem_total=98G

tile=$1
mkdir /projectnb/landsat/projects/ABOVE/CCDC/$tile/out_tc_pre
module purge
source /projectnb/landsat/users/shijuan/miniconda3/bin/activate yatsm_v0.6_par
python /usr3/graduate/shijuan/codes/above/yatsm_v0.6_par/yatsm/mapping/plot_bgw.py --tile_name $tile
source deactivate

echo "Finished submitting tile $tile"
