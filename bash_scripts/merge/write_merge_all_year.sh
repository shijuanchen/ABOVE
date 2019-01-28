#!/bin/bash
for year in `seq 1985 2013`;
do
tile=$1
output_file="pp_merge_"$year".sh"
>"pp_merge_"$year".sh"
echo -n "#!/bin/bash
#$ -N merge_year
#$ -l h_rt=24:00:00
#$ -l mem_total=98G

module purge
source /projectnb/landsat/users/shijuan/miniconda3/bin/activate yatsm_v0.6_par
gdal_merge.py -o /projectnb/landsat/users/shijuan/above/above_merge_pp/above_merge_pp_"$year".tif -a_nodata 0 -ot Byte -co TILED=YES -co BLOCKXSIZE=256 -co BLOCKYSIZE=256 -co COMPRESS=DEFLATE "> $output_file
while read -r line
do  
    tile_name=$(echo $line | cut -c 1-7)
    pp_file="/projectnb/landsat/projects/ABOVE/CCDC/$tile_name/new_map/out_pp/"$tile_name"_FF_FN_NF_NN_"$year"_cl_pp.tif"
    if [ -f $pp_file ];
    then
        echo -n "$pp_file " >> $output_file
    fi
done < "ABOVE_tile_list.txt"
done
