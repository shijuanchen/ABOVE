#!/bin/bash 
tile=$1
while read -r line
do    
    file="/projectnb/landsat/projects/ABOVE/CCDC/$line/$line*.npz"
    if [ -f $file ];
    then    
        echo "list .npz files within $(dirname $file)"
        ls -lh $file
    else    
        echo "$file not found!"    
    fi
done < "tile_05_29.txt"
