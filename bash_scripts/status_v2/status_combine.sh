#!/bin/bash 
tile=$1
output="ABOVE_combine_v2.txt"
>"ABOVE_combine_v2.txt"
counter=0
while read -r line
do  
    tile_name=$(echo $line | cut -c 1-7)
    combine_file="/projectnb/landsat/projects/ABOVE/CCDC/$tile_name/new_map/out_classes/"$tile_name"_FF_FN_NF_NN_2013_cl.tif"
    if [ -f $combine_file ];
    then
        echo "$tile_name Y" >> $output
        counter=$((counter+1))
    else
        echo "$tile_name N" >> $output
    fi
done < "ABOVE_tiles_wLC.txt"
echo "Number of tiles with combine FF_FN_NF_NN :$counter."
