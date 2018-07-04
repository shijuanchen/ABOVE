#!/bin/bash 
tile=$1
while read -r line
do  
    tile_name=$(echo $line | cut -c 1-7)
    tc_4type_file="/projectnb/landsat/projects/ABOVE/CCDC/$tile_name/out_tc_4type/"$tile_name"_dTC_NN_2013.tif"
    if [ -f $tc_4type_file ];
    then
        echo "Submitting tile $tile_name to do rf_FN_NN."
        #qsub rf_FN_NN_tile.sh $tile_name
    fi
done < "ABOVE_tile_list.txt"
