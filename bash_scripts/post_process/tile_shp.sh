#!/bin/bash
module purge
source /projectnb/landsat/users/shijuan/miniconda3/bin/activate yatsm_v0.6_par
tile=$1
out_folder="/projectnb/landsat/users/shijuan/above/post_process/agr_tiles_tif"
while read -r line
do
    tile_name=$(echo $line | cut -c 1-7)
    tif_file="$out_folder/"$tile_name"_FF_FN_NF_NN_2006_cl.tif"
    shp_file="$out_folder/"$tile_name".shp"
    echo "make shape files of $tif_file ."
    gdaltindex $shp_file $tif_file
done < "agr_tiles.txt"
