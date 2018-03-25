#!/bin/bash -l
#$ -V
#$ -l h_rt=10:00:00
#$ -N map_bgw
#$ -j y
#$ -l mem_total=98G
#$ -pe omp 16

module purge
source activate yatsm_v0.6_par
python /usr3/graduate/shijuan/codes/above/yatsm_v0.6_par/yatsm/mapping/plot_bgw.py --tile_name Bh12v10
source deactivate

echo "Finished submitting this tile"
