#!/bin/bash
tile=$1
out_folder="/projectnb/landsat/users/shijuan/above/post_process/agr_tiles_tif"
while read -r line
do
    tile_name=$(echo $line | cut -c 1-7)
    class_file="/projectnb/landsat/projects/ABOVE/CCDC/$tile_name/out_classes/"$tile_name"_FF_FN_NF_NN_2006_cl.tif"
    echo "copy $class_file."
    cp $class_file $out_folder
done < "agr_tiles.txt"
