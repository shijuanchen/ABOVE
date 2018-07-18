#!bin/bash
module purge
source /projectnb/landsat/users/shijuan/miniconda3/bin/activate yatsm_v0.6_par
tile=$1
lc_folder="/projectnb/landsat/users/shijuan/above/lc_map/ab/lc_tif"
while read -r line
do
    tile_name=$(echo $line | cut -c 1-7)
    echo "gdal_wrap $tile_name"
    in_tif="$lc_folder/$tile_name"*".TIF"
    in_proj="$lc_folder/$tile_name"*".prj"
    out_tif="$lc_folder/reprj/"$tile_name"_rep.TIF"
    #echo "gdalwarp -overwrite $in_tif $out_tif -s_srs $in_proj -t_srs EPSG:102001"
    gdalwarp -overwrite $in_tif $out_tif -s_srs $in_proj -t_srs EPSG:102001
done < "ab_tile_list.txt" 
