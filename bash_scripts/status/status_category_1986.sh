#!/bin/bash 
tile=$1
output="ABOVE_category_1986.txt"
>"ABOVE_category_1986.txt"
counter=0
while read -r line
do  
    tile_name=$(echo $line | cut -c 1-7)
    category_1986="/projectnb/landsat/projects/ABOVE/CCDC/$tile_name/out_category/"$tile_name"_dTC_FF_1986_cl.tif"
    if [ -f $category_1986 ];
    then
        echo "$tile_name Y" >> $output
        counter=$((counter+1))
    else
        echo "$tile_name N" >> $output
    fi
done < "ABOVE_tile_list.txt"
echo "Number of tiles with categorize FF_NF_NN :$counter."
