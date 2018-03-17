# Random forest classification

rm(list=ls())

library(randomForest)
library(rgdal)
library(raster)

train_csv_path = "/projectnb/landsat/users/shijuan/above/bh09v15/rand_forest/combined_csv.csv"
img_dir = "/projectnb/landsat/projects/ABOVE/CCDC/Bh09v15/out_tc/"
#img = "Bh09v15_dTC_2006.tif"
#img_2006 = paste0(img_dir, img)
output_dir = "/projectnb/landsat/users/shijuan/above/bh09v15/rand_forest/rf_img_v1/"

# for now, only 37 training samples
agent_train <- read.csv(file=train_csv_path,header=T)
agent_train <- agent_train[complete.cases(agent_train),]

agent_rf <- randomForest(agent ~ db + dg + dw, data=agent_train)

img_files <- list.files(path=img_dir,pattern="*.tif$",all.files=T,full.names=T)

for(file in img_files){
  img <- brick(file)
  names(img) <- c('db', 'dg', 'dw')
  preds_rf <- predict(img, model=agent_rf, na.rm=T)
  file_name = strsplit(basename(file),'[.]')[[1]]
  new_name = paste0(file_name[1],'_rf.tif')
  output_path = paste0(output_dir,new_name)
  print(output_path)
  writeRaster(preds_rf, filename=output_path,format='GTiff',overwrite=TRUE)
}

