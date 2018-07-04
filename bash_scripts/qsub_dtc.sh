#!/bin/bash 
tile=$1
while read -r line
do  
    tile_name=$(echo $line | cut -c 1-7)
    dtc_2013="/projectnb/landsat/projects/ABOVE/CCDC/$tile_name/out_tc_pre/"$tile_name"_dTC_2013.tif" 
    img_file="/projectnb/landsat/projects/ABOVE/CCDC/$tile_name/out_tif/"$tile_name"_1984.tif"
    if [ ! -f $dtc_2013 ];
    then
        if [ ! -f $img_file ];
        then
            echo "synthetic image for tile $tile_name does not exist, will not sumbit this tile."
        else      
            echo "Submitting tile $tile_name to make dtc change maps"
            qsub map_bgw_tile.sh $tile_name
        fi
    else
        echo "dTC map for tile $tile_name exists!"
    fi
done < "ABOVE_tile_list.txt"
