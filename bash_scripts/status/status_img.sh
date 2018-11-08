#!/bin/bash 
tile=$1
counter=0
output="ABOVE_img_status.txt"
while read -r line
do  
    tile_name=$(echo $line | cut -c 1-7)
    img_file="/projectnb/landsat/projects/ABOVE/CCDC/$tile_name/out_tif/"$tile_name"_1984.tif"
    if [ -f $img_file ];
    then
        echo "$tile_name Y" >> $output
        counter=$((counter+1))
    else
        echo "$tile_name N" >> $output
    fi
done < "ABOVE_tile_list.txt"
echo "Number of tiles with synthetic images: $counter."
