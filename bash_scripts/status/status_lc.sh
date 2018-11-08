#!/bin/bash
tile=$1
counter=0
output="ABOVE_lc.txt"
while read -r line
do
    tile_name=$(echo $line | cut -c 1-7)
    lc_file="/projectnb/modislc/users/jonwang/data/rf/rast/tc_20180416_noGeo_k55_pam_rf/$tile_name/remap/"$tile_name"_1985_tc_20180416_noGeo_k55_pam_rf_remap.tif"
    if [ -f $lc_file ];
    then
        echo "$tile_name Y" >> $output
        counter=$((counter+1))
    else
        echo "$tile_name N" >> $output
    fi
done < "ABOVE_tile_list.txt"
echo "Number of tiles with land cover images: $counter."
