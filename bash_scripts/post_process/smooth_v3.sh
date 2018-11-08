#!/bin/bash
#$ -V
#$ -l h_rt=48:00:00
#$ -N smooth_v3
#$ -j y
#$ -l mem_total=128G
#$ -pe omp 8

tile=$1
module purge
source /projectnb/landsat/users/shijuan/miniconda3/bin/activate yatsm_v0.6_par
python /usr3/graduate/shijuan/Desktop/my_ABOVE_git/post_pro_smooth_v3.py --tile_name $tile
source deactivate
