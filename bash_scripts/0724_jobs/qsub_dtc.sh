#!/bin/bash 
tile=$1
while read -r line
do  
    tile_name=$(echo $line | cut -c 1-7)
    dtc_2013="/projectnb/landsat/projects/ABOVE/CCDC/$tile_name/out_tc_pre/"$tile_name"_dTC_2013.tif" 
    if [ ! -f $dtc_2013 ];
    then      
        echo "Submitting tile $tile_name to make dtc change maps"
        qsub map_bgw_tile.sh $tile_name
    else
        echo "dTC map for tile $tile_name exists!"
    fi
done < "ABOVE_lc_ndtc.txt"
