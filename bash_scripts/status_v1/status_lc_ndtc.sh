#!/bin/bash
tile=$1
counter=0
output="ABOVE_lc_ndtc.txt"
>"ABOVE_lc_ndtc.txt"
while read -r line
do
    tile_name=$(echo $line | cut -c 1-7)
    lc_file="/projectnb/modislc/users/jonwang/data/rf/rast/tc_20180416_noGeo_k55_pam_rf/$tile_name/remap/"$tile_name"_1985_tc_20180416_noGeo_k55_pam_rf_remap.tif"
    dtc_1985="/projectnb/landsat/projects/ABOVE/CCDC/$tile_name/out_tc_pre/"$tile_name"_dTC_1985.tif" 
    if [ -f $lc_file ];
    then
        if [ ! -f $dtc_1985 ];
        then
            echo "$tile_name" >> $output
            counter=$((counter+1))
        fi
    fi
done < "ABOVE_tile_list.txt"
echo "Number of tiles with land cover images but without dtc: $counter."
