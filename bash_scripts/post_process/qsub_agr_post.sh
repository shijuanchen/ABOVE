#!/bin/bash
tile=$1
while read -r line
do
    tile_name=$(echo $line | cut -c 1-7)
    echo "Submitting tile $tile_name for agr_post_pro"
    qsub agr_post_tile.sh $tile_name
done < agr_tiles.txt
