#!/bin/bash 
tile=$1
while read -r line
do  
    tile_name=$(echo $line | cut -c 1-7)
    combine_file="/projectnb/landsat/projects/ABOVE/CCDC/$tile_name/out_classes/"$tile_name"_FF_FN_NF_NN_2013_cl.tif"    
    if [ -f $combine_file ];
    then
        echo "Submitting tile $tile_name to do pixel count."
        #qsub pixel_counts_tile.sh $tile_name
    fi
done < "ABOVE_tile_list.txt"
