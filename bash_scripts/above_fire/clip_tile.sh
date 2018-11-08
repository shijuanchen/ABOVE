#!/bin/bash
module purge
source /projectnb/landsat/users/shijuan/miniconda3/bin/activate yatsm_v0.6_par
tile=$1
in_folder="/projectnb/landsat/users/shijuan/above/ABOVE_fires/tif_year"
shp_folder="/projectnb/landsat/users/shijuan/above/ABOVE_fires/test_tiles/tile_boundary/$tile"
out_folder="/projectnb/landsat/users/shijuan/above/ABOVE_fires/test_tiles/output/$tile"
for i in $(seq 1983 2013)
do
    in_tif="$in_folder/ABoVE_Fires_year_"$i".tif"
    shp_file="$shp_folder/"$tile".shp"
    out_file="$out_folder/"$tile"_fireBD_"$i".tif"
    echo "gdalwarp -cutline $shp_file -crop_to_cutline $in_tif $out_file"
    gdalwarp -cutline $shp_file -crop_to_cutline $in_tif $out_file -ts 6000 6000
done
