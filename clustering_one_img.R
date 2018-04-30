# This script clusters the dTC-preTC change map using unsupervised random forest classification.

# Random forest classification

rm(list=ls())

library(randomForest)
library(rgdal)
library(raster)
library(cluster)

img = "/projectnb/landsat/projects/ABOVE/CCDC/Bh09v15/out_tc_pre/Bh09v15_dTC_2006.tif"
output = "/projectnb/landsat/projects/ABOVE/CCDC/Bh09v15/clustering_v1/Bh09v15_dTC_2006_clust.tif"

image <- stack(img)
v <- getValues(image)
i <- which(!is.na(v))
v <- na.omit(v)
E <- kmeans(v,12, iter.max=100, nstart=10)
kmeans_raster <- raster(img_df)
kmeans_raster[i]<-E$cluster
plot(kmeans_raster)
#randomForest(img_df, importance=TRUE,ntree=500, type=unsupervised, na.rm=T)



