#!/bin/bash 
tile=$1
counter=0
output="ABOVE_npz_status_non_zero.txt"
>"ABOVE_npz_status_non_zero.txt"
while read -r line
do  
    tile_name=$(echo $line | cut -c 1-7)
    npz_file="/projectnb/landsat/projects/ABOVE/CCDC/$tile_name/$tile_name.all_breaks.npy.npz"
    file_size=$(stat -c%s "$npz_file")
    if [ $file_size -gt 0 ];
    then
        echo "$tile_name Y" >> $output
        counter=$((counter+1))
    else
        echo "$tile_name N" >> $output
    fi
done < "ABOVE_tile_list.txt"
echo "Number of tiles with non-zero npz files: $counter."
