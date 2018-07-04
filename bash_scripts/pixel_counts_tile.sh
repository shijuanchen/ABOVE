#!/bin/bash -l
#$ -V
#$ -l h_rt=48:00:00
#$ -N pixel_counts
#$ -j y
#$ -l mem_total=98G

tile=$1
module purge
source /projectnb/landsat/users/shijuan/miniconda3/bin/activate yatsm_v0.6_par
python /usr3/graduate/shijuan/Desktop/my_ABOVE_git/pixel_counts_cl.py --tile_name $tile
source deactivate

echo "Finished submitting tile $tile for pixel counts."
