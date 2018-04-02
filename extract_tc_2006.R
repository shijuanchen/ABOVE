# This script extracts delta tc metrics of points shp from the raster to the csv

rm(list=ls())

# load raster packages
library(rgdal)
library(raster)

shp_file = "/projectnb/landsat/users/shijuan/above/bh09v15/train_sample/training_sample.shp"
dtc_file = "/projectnb/landsat/projects/ABOVE/CCDC/Bh09v15/out_tc/Bh09v15_dTC_2006.tif"

shp_name = "training_sample" # no .shp

# read the shapefile
pts_df = readOGR(shp_file, shp_name)

db_ras = raster(dtc_file,band=1)
out_tab[,1] <- extract(db_ras,pts_df)

dg_ras = raster(dtc_file,band=2)
out_tab[,2] <- extract(dg_ras,pts_df)

dw_ras = raster(dtc_file,band=3)
out_tab[,3] <- extract(dw_ras,pts_df)

