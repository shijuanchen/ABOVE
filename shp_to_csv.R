# This script extracts delta tc metrics of points shp from the raster to the csv

rm(list=ls())

# load raster packages
library(rgdal)
library(raster)

# This script extracts delta tc metrics of points shp from the raster to the csv

rm(list=ls())

# load raster packages
library(rgdal)
library(raster)

# function to abbrevaite paste
"%+%" <- function(x,y) paste(x,y,sep="")
out_dir = "/projectnb/landsat/users/shijuan/above/bh09v15/rand_forest_v3/assess_sample/"
shp_loc = "/projectnb/landsat/users/shijuan/above/bh09v15/rand_forest_v3/assess_sample/" # directory
shp_name = "assess_sample_2006_pts" # no .shp

# read the shapefile
pts_df = readOGR(shp_loc, shp_name)
#print(pts_df)
out_file = out_dir%+%shp_name%+%".csv"
write.table(pts_df, file=out_file,sep=",",col.names=T,row.names=F, quote=F)
