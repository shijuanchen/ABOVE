#!/bin/bash
#$ -N rasterize
#$ -l h_rt=24:00:00
#$ -l mem_total=98G

module purge
source /projectnb/landsat/users/shijuan/miniconda3/bin/activate yatsm_v0.6_par
input_folder="/projectnb/landsat/users/shijuan/above/ABOVE_fires_new/ABOVE_fire_DB_year"
output_folder="/projectnb/landsat/users/shijuan/above/ABOVE_fires_new/raster_year"
for i in `seq 1987 2017`;
do
    echo "gdal_rasterize -burn 1 -tr 30 30 -l ABOVE_fire_DB__YEAR_"$i" -a_nodata 0 $input_folder/ABOVE_fire_DB__YEAR_"$i".shp $output_folder/ABOVE_fires_year_"$i".tif"
    gdal_rasterize -burn 1 -tr 30 30 -l ABOVE_fire_DB__YEAR_"$i" -a_nodata 0 -ot Byte -co TILED=YES -co BLOCKXSIZE=256 -co BLOCKYSIZE=256 -co COMPRESS=DEFLATE $input_folder/ABOVE_fire_DB__YEAR_"$i".shp $output_folder/ABOVE_fires_year_"$i".tif
done

