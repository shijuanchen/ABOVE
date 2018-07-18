#!/bin/bash
module purge
source /projectnb/landsat/users/shijuan/miniconda3/bin/activate qgis
tile=$1
out_folder="/projectnb/landsat/users/shijuan/above/post_process"
while read -r line
do
    tile_name=$(echo $line | cut -c 1-7)
    in_tif="$out_folder/abbc_lc_rep.tif"
    shp_file="$out_folder/agr_tiles_tif/"$tile_name".shp"
    out_file="$out_folder/lc_tiles/"$tile_name"_lc.tif"
    echo "gdalwarp -cutline $shp_fiile -crop_to_cutline $in_tif $out_file"
    gdalwarp -cutline $shp_file -crop_to_cutline $in_tif $out_file -ts 6000 6000
done < "agr_tiles.txt"
