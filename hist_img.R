# Random forest classification

rm(list=ls())
library(rgdal)
library(raster)
img_dir = "/projectnb/landsat/users/shijuan/above/bh09v15/rand_forest_v3/rf_map/Bh09v15_dTC_F_or_F_2008_rf.tif"
img <- brick(img_dir)
count=0
for(pix in img):
  if(pix==1):
    count++
