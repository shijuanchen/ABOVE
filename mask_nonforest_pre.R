#### R code to extract the forest area either in 1985 or in 2014 based on LC map for Bh09v15

## load raster packages
#if(!require(rgdal)) install.packages('rgdal',repos = "http://cran.us.r-project.org")
#if(!require(raster)) install.packages('raster',,repos = "http://cran.us.r-project.org")
library(rgdal)
library(raster)

tc_dir = "/projectnb/landsat/projects/ABOVE/CCDC/Bh09v15/out_tc_pre"
LC_1985_map = '/projectnb/landsat/users/shijuan/above/bh09v15/LCmap/Bh09v15_1985_tc_20180416_noGeo_k55_pam_rf_remap.tif'
LC_2014_map = '/projectnb/landsat/users/shijuan/above/bh09v15/LCmap/Bh09v15_2014_tc_20180416_noGeo_k55_pam_rf_remap.tif'
output_dir = "/projectnb/landsat/projects/ABOVE/CCDC/Bh09v15/out_tc_F_or_F/"
tile_name = 'Bh09v15'

file_name = paste0(tile_name, '_dTC_F_or_F_')
ras_list <- list.files(tc_dir,pattern="*.tif$", full.names=T) # 29 files in total

# read 1985 LC map and 2014 LC map
LC_1985 <- stack(LC_1985_map)
LC_2014 <- stack(LC_2014_map)
LC <- stack(LC_1985_map)

LC[LC_1985 > 3] <- NA
LC[LC_2014 <=3] <- 1

for (i in 1:29){
  layers = stack(ras_list[i])
  TC_forest <- mask(layers, LC)
  year = 1984 + i
  filename = paste0(output_dir,file_name,as.character(year),".tif",sep="")
  print(filename)
  writeRaster(TC_forest,filename,format="GTiff", overwrite=TRUE)  
} 
