#!/bin/bash 

while read -r line
do  
    tile_name=$(echo $line | cut -c 1-7)
    echo "Submitting tile $tile_name to extract FN tc."
    qsub make_trainingFN_tile.sh $tile_name
done < "training_listFN.txt"
