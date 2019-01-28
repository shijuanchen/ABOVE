#!/bin/bash
#$ -N merge_year
#$ -l h_rt=24:00:00
#$ -l mem_total=98G

module purge
source /projectnb/landsat/users/shijuan/miniconda3/bin/activate yatsm_v0.6_par
gdal_merge.py -o /projectnb/landsat/users/shijuan/above/above_merge/above_merge_v01_2006.tif -a_nodata 0 -ot Byte -co TILED=YES -co BLOCKXSIZE=256 -co BLOCKYSIZE=256 -co COMPRESS=DEFLATE 
