#!/bin/bash 
tile=$1
counter=0
output="ABOVE_tc_pre_status.txt"
while read -r line
do  
    tile_name=$(echo $line | cut -c 1-7)
    tc_pre_file="/projectnb/landsat/projects/ABOVE/CCDC/$tile_name/out_tc_pre/"$tile_name"_dTC_2013.tif"
    if [ -f $tc_pre_file ];
    then
        echo "$tile_name Y" >> $output
        counter=$((counter+1))
    else
        echo "$tile_name N" >> $output
    fi
done < "ABOVE_tile_list.txt"
echo "Number of tiles with dtc change maps: $counter."
