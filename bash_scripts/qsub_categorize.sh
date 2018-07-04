#!/bin/bash 
tile=$1
while read -r line
do  
    tile_name=$(echo $line | cut -c 1-7)
    tc_4type_file="/projectnb/landsat/projects/ABOVE/CCDC/$tile_name/out_tc_4type/"$tile_name"_dTC_NN_2013.tif"
    category_file="/projectnb/landsat/projects/ABOVE/CCDC/$tile_name/out_category/"$tile_name"_dTC_NN_2013_cl.tif"
    if [ -f $tc_4type_file ];
    then
        if [ ! -f $category_file ];
        then
            echo "Submitting tile $tile_name to categorize FF_NF_NN."
            #qsub categorize_tile.sh $tile_name
        else
            echo "category files exist. No need to update."
        fi
    fi
done < "ABOVE_tile_list.txt"
