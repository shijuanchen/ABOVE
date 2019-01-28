#!/bin/bash 
tile=$1
output="ABOVE_pixel_count.txt"
>"ABOVE_pixel_count.txt"
counter=0
while read -r line
do  
    tile_name=$(echo $line | cut -c 1-7)
    pixel_count_file="/projectnb/landsat/users/shijuan/above/area_estimates/pixel_counts/"$tile_name"_pc.txt"
    if [ -f $pixel_count_file ];
    then
        echo "$tile_name Y" >> $output
        counter=$((counter+1))
    else
        echo "$tile_name N" >> $output
    fi
done < "ABOVE_tile_list.txt"
echo "Number of tiles with pixel counts :$counter."
