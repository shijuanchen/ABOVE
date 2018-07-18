#!/bin/bash -l
#$ -V
#$ -l h_rt=10:00:00
#$ -N eco_table
#$ -j y
#$ -l mem_total=98G

tile=$1
module purge
source /projectnb/landsat/users/shijuan/miniconda3/bin/activate yatsm_v0.6_par
python /usr3/graduate/shijuan/Desktop/my_ABOVE_git/eco_region_table.py --tile_name $tile
source deactivate

echo "Finished submitting tile $tile for eco_region_table."
