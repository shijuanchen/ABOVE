#!/bin/bash 
tile=$1
output="ABOVE_tc_4type_status.txt"
>"ABOVE_tc_4type_status.txt"
counter=0
while read -r line
do  
    tile_name=$(echo $line | cut -c 1-7)
    tc_4type_file="/projectnb/landsat/projects/ABOVE/CCDC/$tile_name/out_tc_4type/"$tile_name"_dTC_NN_2013.tif"
    if [ -f $tc_4type_file ];
    then
        echo "$tile_name Y" >> $output
        counter=$((counter+1))
    else
        echo "$tile_name N" >> $output
    fi
done < "ABOVE_tile_list.txt"
echo "Number of tiles with 4types of tc change maps :$counter."
