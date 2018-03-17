# This script extracts delta tc metrics of points shp from the raster to the csv

rm(list=ls())

# load raster packages
library(rgdal)
library(raster)

# function to abbrevaite paste
"%+%" <- function(x,y) paste(x,y,sep="")
out_dir = "/projectnb/landsat/users/shijuan/above/bh09v15/rand_forest/"
tc_dir = "/projectnb/landsat/projects/ABOVE/CCDC/Bh09v15/out_tc/"
shp_loc = "/projectnb/landsat/users/shijuan/above/bh09v15/rand_forest/val_Bh09v15.shp" # can also be a directory
shp_name = "val_Bh09v15" # no .shp

# read the shapefile
pts_df = readOGR(shp_loc, shp_name)
#print(pts_df)

# set an array to save the values
npix = length(pts_df[1])
print(npix)
n_mets = 3
out_tab = array(NA,dim=c(npix,n_mets*29+1))
col_names = array(NA, dim=c(n_mets*29+1))
out_tab[,c(1:1)] = c(pts_df[['pix']])

for(year in 1985:2013){
  tc_year = tc_dir%+%"Bh09v15_dTC_"%+%toString(year)%+%".tif"
  n = year - 1984
  # extract delta brightness
  col_names[3*n-1] = "db_"%+%toString(year)
  db_ras = raster(tc_year,band=1)
  out_tab[,c(3*n-1)] <- extract(db_ras,pts_df)
  
  # extract delta greenness
  col_names[3*n] = "dg_"%+%toString(year)
  dg_ras = raster(tc_year,band=2)
  out_tab[,c(3*n)] <- extract(dg_ras,pts_df)
  
  # extract delta wetness
  col_names[3*n+1] = "dw_"%+%toString(year)
  dw_ras = raster(tc_year,band=3)
  out_tab[,c(3*n+1)] <- extract(dw_ras,pts_df)
}
col_names[1] = "pix"
colnames(out_tab) = col_names
out_file = out_dir%+%"val_Bh09v15_tc.csv"
write.table(out_tab, file=out_file,sep=",",col.names=T,row.names=F, quote=F)


