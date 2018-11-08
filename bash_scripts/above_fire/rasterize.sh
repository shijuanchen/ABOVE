#!/bin/bash
#$ -N rasterize
#$ -l h_rt=24:00:00
#$ -l mem_total=98G

module purge
source /projectnb/landsat/users/shijuan/miniconda3/bin/activate yatsm_v0.6_par
input_folder="/projectnb/landsat/users/shijuan/above/ABOVE_fires/shp_year"
output_folder="/projectnb/landsat/users/shijuan/above/ABOVE_fires/tif_year"
for i in `seq 1987 2013`;
do
    echo "gdal_rasterize -burn 1 -tr 30 30 -l ABoVE_Fires_year_"$i" -a_nodata 0 $input_folder/ABoVE_Fires_year_"$i".shp $output_folder/ABoVE_Fires_year_"$i".tif"
    gdal_rasterize -burn 1 -tr 30 30 -l ABoVE_Fires_year_"$i" -a_nodata 0 $input_folder/ABoVE_Fires_year_"$i".shp $output_folder/ABoVE_Fires_year_"$i".tif
done

