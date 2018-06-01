#!/bin/bash 
tile=$1
while read -r line
do  
    echo $line
    tile_name=$(echo $line | cut -c 1-7)
    folder="/projectnb/landsat/projects/ABOVE/CCDC/$tile_name/out_tif"
    if [ -d "$folder" ];
    then    
        echo "list file numbers within $folder"
        echo $(ls $folder | wc -l)
    else    
        echo "$folder not found!"    
    fi
done < "ABOVE_tile_list.txt"
