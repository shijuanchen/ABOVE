#!/bin/bash
#$ -V
#$ -l h_rt=24:00:00
#$ -N merge_tif

module purge
source /projectnb/landsat/users/shijuan/miniconda3/bin/activate yatsm_v0.6_par
gdal_merge.py -o /projectnb/landsat/users/shijuan/above/test/test2.tif /projectnb/landsat/users/shijuan/above/bh09v15/Bh09v15_dTC_2006.tif /projectnb/landsat/users/shijuan/above/bh10v15/Bh10v15/map_bgw/Bh10v15_dTC_2006.tif
