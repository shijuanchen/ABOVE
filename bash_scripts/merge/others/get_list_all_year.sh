#!/bin/bash 
tile=$1
output_list="classes_list.txt"
>"classes_list.txt"
while read -r line
do  
    tile_name=$(echo $line | cut -c 1-7)
    for i in `seq 1985 2013`;
    classes_file="/projectnb/landsat/projects/ABOVE/CCDC/$tile_name/new_map/out_classes/"$tile_name"_FF_FN_NF_NN_2006_cl.tif"
    if [ -f $classes_file ];
    then
        echo -n "$classes_file " >> $output_list
    fi
done < "ABOVE_tile_list.txt"
