# Random forest classification

rm(list=ls())

library(randomForest)
library(rgdal)
library(raster)

train_csv_path = "/projectnb/landsat/users/shijuan/above/bh09v15/rand_forest_v4/combined_train_dist.csv"
#img_dir = "/projectnb/landsat/users/shijuan/above/bh09v15/rand_forest_v4/FN/"
#output_dir = "/projectnb/landsat/users/shijuan/above/bh09v15/rand_forest_v4/FN_class/"
img_dir = "/projectnb/landsat/projects/ABOVE/CCDC/Bh09v14/out_tc_4type/"
output_dir = "/projectnb/landsat/projects/ABOVE/CCDC/Bh09v14/out_category/"

agent_train <- read.csv(file=train_csv_path,header=T,colClasses=c(agent="character"))
agent_train <- agent_train[complete.cases(agent_train),]

agent_rf <- randomForest(factor(agent) ~ db + dg + dw + pb + pg + pw, data=agent_train)

img_files <- list.files(path=img_dir,pattern="*.tif$",all.files=T,full.names=T)

for(file in img_files){
  type = strsplit(file,'[_]')[[1]][5]
  if(type=='FN'){
    print(file)
    img <- brick(file)
    names(img) <- c('db', 'dg', 'dw','pb', 'pg', 'pw')
    preds_rf <- predict(img, model=agent_rf, na.rm=T)
    file_name = strsplit(basename(file),'[.]')[[1]]
    new_name = paste0(file_name[1],'_rf.tif')
    output_path = paste0(output_dir,new_name)
    print(output_path)
    writeRaster(preds_rf, filename=output_path,format='GTiff',overwrite=TRUE)
  }
}

