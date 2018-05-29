#!/bin/bash 
#$ -V
#$ -l h_rt=48:00:00
#$ -N chain1
tile=$1
while read -r line
do  
    tile_name=$(echo $line | cut -c 1-7)
    echo "Submitting tile $tile_name to make npz. files"
    map_table_tile.sh $tile_name
    map_bgw_tile.sh $tile_name
    mask_4type_tile.sh $tile_name
done < "tile_chain_0529.txt"
