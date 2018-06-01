#!/bin/bash 
tile=$1
while read -r line
do  
    tile_name=$(echo $line | cut -c 1-7)
    echo "Submitting tile $tile_name to make dtc change maps"
    qsub map_bgw_tile.sh $tile_name
done < "tile_npz_0529.txt"
