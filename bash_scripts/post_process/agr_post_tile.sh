#!/bin/bash
#$ -V
#$ -l h_rt=48:00:00
#$ -N agr_post
#$ -j Y
#$ -l mem_total=128G
#$ -pe omp 8

tile=$1
module purge
source /projectnb/landsat/users/shijuan/miniconda3/bin/activate yatsm_v0.6_par
python /usr3/graduate/shijuan/Desktop/my_ABOVE_git/post_pro_agr.py --tile_name $tile
source deactivate
echo "Finished submitting tile $tile"
