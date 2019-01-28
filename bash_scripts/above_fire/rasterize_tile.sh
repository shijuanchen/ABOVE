#!/bin/bash
#$ -N rasterize
#$ -l h_rt=24:00:00
#$ -l mem_total=98G

tile=$1
module purge
source /projectnb/landsat/users/shijuan/miniconda3/bin/activate yatsm_v0.6_par

function gdal_extent() {
    if [ -z "$1" ]; then
        echo "Missing arguments. Syntax:"
        echo "  gdal_extent <input_raster>"
        return
    fi
    EXTENT=$(gdalinfo $1 |\
        grep "Upper Left\|Lower Right" |\
        sed "s/Upper Left  //g;s/Lower Right //g;s/).*//g" |\
        tr "\n" " " |\
        sed 's/ *$//g' |\
        tr -d "[(]" | tr "," " ")
    EXTENT=`echo $EXTENT | awk '{print $1 " " $4 " " $3 " " $2}'`
    echo -n "$EXTENT"
}

fire_shp_folder="/projectnb/landsat/users/shijuan/above/ABOVE_fires_new/ABOVE_fire_DB_year"
tile_tif="/projectnb/modislc/projects/above/tiles/above_regions/Region_ID."$tile".tif"
out_folder="/projectnb/landsat/users/shijuan/above/ABOVE_fires_new/ABOVE_fireDB"
mkdir "$out_folder/$tile"
tile_extent=$(gdal_extent $tile_tif)
for i in `seq 1983 2017`;
do
    echo "gdal_rasterize -burn 1 -tr 30 30 -l ABOVE_fire_DB__YEAR_"$i" -a_nodata 0 -ot Byte -te $tile_extent -co TILED=YES -co BLOCKXSIZE=256 -co BLOCKYSIZE=256 -co COMPRESS=DEFLATE $fire_shp_folder/ABOVE_fire_DB__YEAR_"$i".shp $out_folder/$tile/"$tile"_fireDB_"$i".tif"
    gdal_rasterize -burn 1 -tr 30 30 -l ABOVE_fire_DB__YEAR_"$i" -a_nodata 0 -ot Byte -te $tile_extent -co TILED=YES -co BLOCKXSIZE=256 -co BLOCKYSIZE=256 -co COMPRESS=DEFLATE $fire_shp_folder/ABOVE_fire_DB__YEAR_"$i".shp $out_folder/$tile/"$tile"_fireDB_"$i".tif
done

