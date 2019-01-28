#!/bin/bash 
tile=$1
output="ABOVE_rf_FN_NN.txt"
>"ABOVE_rf_FN_NN.txt"
counter=0
while read -r line
do  
    tile_name=$(echo $line | cut -c 1-7)
    rf_NN_2013="/projectnb/landsat/projects/ABOVE/CCDC/$tile_name/out_category/"$tile_name"_dTC_NN_2013_rf.tif"
    if [ -f $rf_NN_2013 ];
    then
        echo "$tile_name Y" >> $output
        counter=$((counter+1))
    else
        echo "$tile_name N" >> $output
    fi
done < "ABOVE_tile_list.txt"
echo "Number of tiles with random forest for FN and NN :$counter."
