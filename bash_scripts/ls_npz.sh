#!/bin/bash 
tile=$1
while read -r line
do  
    echo $line
    tile_name=$(echo $line | cut -c 1-7)  
    file="/projectnb/landsat/projects/ABOVE/CCDC/$tile_name/$tile_name*.npz"
    if [ -f $file ];
    then    
        echo "list .npz files within $(dirname $file)"
        ls -lh $file
    else    
        echo "$file not found!"    
    fi
done < "tile_npz_0529.txt"
