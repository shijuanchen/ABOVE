#### R code to mask the non-forest area based on LC map for Bh12v11

## load raster packages
#if(!require(rgdal)) install.packages('rgdal',repos = "http://cran.us.r-project.org")
#if(!require(raster)) install.packages('raster',,repos = "http://cran.us.r-project.org")
library(rgdal)
library(raster)

tc_dir = "/projectnb/landsat/projects/ABOVE/CCDC/Bh09v15/out_tc_pre"
LC_1985_map = '/projectnb/landsat/users/shijuan/above/bh09v15/LCmap/Bh09v15_1985_tc_20180219_k25_mn_sub_pam_rf_remap.tif'
output_dir = "/projectnb/landsat/projects/ABOVE/CCDC/Bh09v15/out_tc_Forest/"
tile_name = 'Bh09v15'

file_name = paste0(tile_name, '_dTC_F_')
ras_list <- list.files(tc_dir,pattern="*.tif$", full.names=T) # 29 files in total

# read 1985 LC map
LC <- stack(LC_1985_map)

LC[LC > 3] <- NA

for (i in 1:29){
  layers = stack(ras_list[i])
  TC_forest <- mask(layers, LC)
  year = 1984 + i
  filename = paste0(output_dir,file_name,as.character(year),".tif",sep="")
  print(filename)
  writeRaster(TC_forest,filename,format="GTiff", overwrite=TRUE)  
} 
