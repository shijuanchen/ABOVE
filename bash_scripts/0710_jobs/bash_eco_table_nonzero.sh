#!/bin/bash 
tile=$1
while read -r line
do  
    tile_name=$(echo $line | cut -c 1-7)
    echo "Submitting tile $tile_name to do eco region table nonzero."
    bash eco_table_nonzero_tile.sh $tile_name
done < "ABOVE_tile_list.txt"
