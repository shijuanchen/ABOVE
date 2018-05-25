#### R code to create four set of dtc_map based on land cover map: 
#### forest to forest; forest to non-forest; forest to non-forest; non-forest to non-forest

## load raster packages
#if(!require(rgdal)) install.packages('rgdal',repos = "http://cran.us.r-project.org")
#if(!require(raster)) install.packages('raster',,repos = "http://cran.us.r-project.org")
library(rgdal)
library(raster)
"%+%" <- function(x,y) paste(x,y,sep="")
tile_name = 'Bh12v10'
tc_dir = "/projectnb/landsat/projects/ABOVE/CCDC/"%+%tile_name%+%"/out_tc_pre/"
LC_map_dir = "/projectnb/modislc/users/jonwang/data/rf/rast/tc_20180416_noGeo_k55_pam_rf/"%+%tile_name%+%"/remap/"
output_dir = "/projectnb/landsat/projects/ABOVE/CCDC/"%+%tile_name%+%"/out_tc_4type/"



file_name_FF = paste0(tile_name, '_dTC_FF_')
file_name_FN = paste0(tile_name, '_dTC_FN_')
file_name_NF = paste0(tile_name, '_dTC_NF_')
file_name_NN = paste0(tile_name, '_dTC_NN_')
ras_list <- list.files(tc_dir,pattern="*.tif$", full.names=T) # 29 files in total
LC_list <- list.files(LC_map_dir,pattern="*.tif$", full.names=T) # 29 files in total

# i in 1:29
for (i in 2:29){
  layers = stack(ras_list[i])
  year = 1984 + i  
  LC_pre <- stack(LC_list[i-1])
  LC_aft <- stack(LC_list[i])
  LC_FF <- LC_pre
  LC_FN <- LC_pre
  LC_NF <- LC_pre
  LC_NN <- LC_pre
  
  # forest to forest
  LC_FF[LC_pre>3 | LC_aft>3] <- NA
  TC_FF <- mask(layers, LC_FF)
  filename_FF = paste0(output_dir,file_name_FF,as.character(year),".tif",sep="")
  print(filename_FF)
  writeRaster(TC_FF,filename_FF,format="GTiff", overwrite=TRUE) 
  
  # forest to non-forest
  LC_FN[LC_pre>3 | LC_aft<=3] <- NA
  TC_FN <- mask(layers, LC_FN)
  filename_FN = paste0(output_dir,file_name_FN,as.character(year),".tif",sep="")
  print(filename_FN)
  writeRaster(TC_FN,filename_FN,format="GTiff", overwrite=TRUE) 
  
  # non-forest to forest
  LC_NF[LC_pre<=3 | LC_aft>3] <- NA
  TC_NF <- mask(layers, LC_NF)
  filename_NF = paste0(output_dir,file_name_NF,as.character(year),".tif",sep="")
  print(filename_NF)
  writeRaster(TC_NF,filename_NF,format="GTiff", overwrite=TRUE) 
  
  # non-forest to non-forest
  LC_NN[LC_pre<=3 | LC_aft<=3] <- NA
  TC_NN <- mask(layers, LC_NN)
  filename_NN = paste0(output_dir,file_name_NN,as.character(year),".tif",sep="")
  print(filename_NN)
  writeRaster(TC_NN,filename_NN,format="GTiff", overwrite=TRUE) 
} 
