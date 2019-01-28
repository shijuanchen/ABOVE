#!/bin/bash 
tile=$1
output_list="pp_list_2006.txt"
>"pp_list_2006.txt"
while read -r line
do  
    tile_name=$(echo $line | cut -c 1-7)
    pp_file="/projectnb/landsat/projects/ABOVE/CCDC/$tile_name/new_map/out_pp/"$tile_name"_FF_FN_NF_NN_2006_cl_pp.tif"
    if [ -f $pp_file ];
    then
        echo -n "$pp_file " >> $output_list
    fi
done < "ABOVE_tile_list.txt"
