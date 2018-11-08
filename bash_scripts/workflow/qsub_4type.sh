#!/bin/bash 
tile=$1
while read -r line
do  
    tile_name=$(echo $line | cut -c 1-7)
    dtc_2013="/projectnb/landsat/projects/ABOVE/CCDC/$tile_name/out_tc_pre/"$tile_name"_dTC_2013.tif"
    if [ -f $dtc_2013 ];
    then
        echo "Submitting tile $tile_name to create 4types of dtc maps."
        qsub mask_4type_tile.sh $tile_name
    fi
done < "ABOVE_tile_list.txt"
