#!/bin/bash 
tile=$1
while read -r line
do  
    tile_name=$(echo $line | cut -c 1-7)
    category_file="/projectnb/landsat/projects/ABOVE/CCDC/$tile_name/out_category/"$tile_name"_dTC_NN_2013_cl.tif"
    if [ -f $category_file ];
    then
        echo "Submitting tile $tile_name to combine classes."
        #qsub combine_classes_tile.sh $tile_name
    fi
done < "ABOVE_tile_list.txt"
