#!/bin/bash 
tile=$1
counter=0
output="ABOVE_hdf5_status.txt"
while read -r line
do  
    tile_name=$(echo $line | cut -c 1-7)
    hdf5_file="/projectnb/landsat/projects/ABOVE/CCDC/$tile_name/$tile_name.h5"
    if [ -f $hdf5_file ];
    then
        echo "$tile_name Y" >> $output
        counter=$((counter+1))
    else
        echo "$tile_name N" >> $output
    fi
done < "ABOVE_tile_list.txt"
echo "Number of tiles with hdf5 files: $counter."
