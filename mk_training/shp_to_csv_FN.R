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
#out_dir = "/projectnb/landsat/users/shijuan/above/bh14v14/"
#shp_loc = "/projectnb/landsat/users/shijuan/above/bh14v14/" # directory
#shp_name = "bh14v14_training_data_pts" # no .shp

args <- commandArgs(trailingOnly=TRUE)
tile_name <- args[1]
out_dir = "/projectnb/landsat/users/shijuan/above/training_data/0725_training/FN/"
shp_loc = "/projectnb/landsat/users/shijuan/above/training_data/0725_training/FN/"%+%tile_name%+%"_pts_FN.shp"
shp_name = tile_name%+%"_pts_FN" # no .shp

# read the shapefile
pts_df = readOGR(shp_loc, shp_name)
#print(pts_df)
out_file = out_dir%+%tile_name%+%"_pts_FN.csv"
write.table(pts_df, file=out_file,sep=",",col.names=T,row.names=F, quote=F)
