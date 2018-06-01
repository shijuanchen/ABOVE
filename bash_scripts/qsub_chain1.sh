#!/bin/bash 
tile=$1
while read -r line
do  
    tile_name=$(echo $line | cut -c 1-7)
    img_file="/projectnb/landsat/projects/ABOVE/CCDC/$tile_name/out_tif/"$tile_name"_1984.tif"
    echo $img_file
    if [ -f $img_file ];
    then
        echo "Submitting tile $tile_name for chain process"
        qsub chain1_tile.sh $tile_name
    else
        echo "1984 image does not exits! Need to process later."
    fi
done < "ABOVE_tile_list.txt"
