#!/bin/bash 
tile=$1
while read -r line
do  
    tile_name=$(echo $line | cut -c 1-7)
    tc_pre_file="/projectnb/landsat/projects/ABOVE/CCDC/$tile_name/out_tc_pre/"$tile_name"_dTC_1986.tif"    
    if [ ! -f $tc_pre_file ];
    then
        echo $tile_name
        echo "Submitting tile $tile_name to make npz. files"
        qsub map_table_tile.sh $tile_name
    #else
       # echo "no need to update for tile $tile_name."
    fi
done < "ABOVE_tile_list.txt"
