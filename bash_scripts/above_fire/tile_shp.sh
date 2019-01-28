#!/bin/bash
module purge
source /projectnb/landsat/users/shijuan/miniconda3/bin/activate yatsm_v0.6_par
tile=$1
in_folder="/projectnb/modislc/projects/above/tiles/above_regions"
out_folder="/projectnb/landsat/users/shijuan/above/ABOVE_fires_new/tile_shp"
while read -r line
do
    tile_name=$(echo $line | cut -c 1-7)
    tif_file="$in_folder/Region_ID."$tile_name".tif"
    shp_file="$out_folder/"$tile_name".shp"
    echo "make shape files of $tif_file ."
    gdaltindex $shp_file $tif_file
done < "ABOVE_tile_list.txt"
