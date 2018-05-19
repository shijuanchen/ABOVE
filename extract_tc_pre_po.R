# This script extracts delta tc metrics of polygon shp from the raster to the csv

rm(list=ls())

# load raster packages
library(rgdal)
library(raster)

# function to abbrevaite paste
"%+%" <- function(x,y) paste(x,y,sep="")
out_dir = "/projectnb/landsat/users/zhangyt/above/Bh13v15/rand_forest/"
tc_dir = "/projectnb/landsat/users/zhangyt/above/Bh13v15/out_tc_Y2NF/"
shp_loc = "/projectnb/landsat/users/zhangyt/above/Bh13v15/rand_forest/rf_file_v3/training_data.shp" # can also be a directory
shp_name = "training_data"     # no .shp

# read the shapefile
ploygon_df = readOGR(shp_loc, shp_name)
#print(ploygon_df)

# set an array to save the values
npl = length(ploygon_df[1])
print(npl)
n_mets = 6
col_names = array(NA, dim = c(n_mets * 28 + 1))
# out_tab_csv = array(NA, dim = c(1, n_mets * 29 + 1))

for(year in 1986:2013){
  tc_year = tc_dir%+%"Bh13v15_dTC_Y2NF_"%+%toString(year)%+%".tif"
  n = year - 1985 
  
  for (ipls in 1:npl){
    current_poly = ploygon_df[ipls,]
    
    # extract delta brightness
    db_ras = raster(tc_year, band=1)
    temp_tab <- extract(db_ras, current_poly)
    # define the output table
    current_len <- length(temp_tab[[1]])
    out_tab = array(NA, dim = c(current_len, n_mets * 28 + 1))
    out_tab[, 1] = c(ploygon_df[['id']][ipls])
    
    # write to the matrix
    out_tab[, 6*n-4] <- unlist(temp_tab)
    col_names[6*n-4] = "db_"%+%toString(year)
    
    
    # extract delta greenness
    dg_ras = raster(tc_year, band=2)
    temp_tab <- extract(dg_ras, current_poly)
    # write to the matrix
    out_tab[, 6*n-3] <- unlist(temp_tab)
    col_names[6*n-3] = "dg_"%+%toString(year)
    
    
    # extract delta wetness
    dw_ras = raster(tc_year, band=3)
    temp_tab <- extract(dw_ras, current_poly)
    # write to the matrix
    out_tab[, 6*n-2] <- unlist(temp_tab)
    col_names[6*n-2] = "dw_"%+%toString(year)
    
    
    # extract pre brightness
    bb_ras = raster(tc_year, band=4)
    temp_tab <- extract(bb_ras, current_poly)    
    # write to the matrix
    out_tab[, 6*n-1] <- unlist(temp_tab)
    col_names[6*n-1] = "bb_"%+%toString(year)
 
    
    # extract pre greenness
    bg_ras = raster(tc_year, band=5)
    temp_tab <- extract(bg_ras, current_poly)    
    # write to the matrix
    out_tab[, 6*n] <- unlist(temp_tab)
    col_names[6*n] = "bg_"%+%toString(year)
    
    
    # extract pre wetness
    bw_ras = raster(tc_year, band=6)
    temp_tab <- extract(bw_ras, current_poly)    
    # write to the matrix
    out_tab[, 6*n+1] <- unlist(temp_tab)
    col_names[6*n+1] = "bw_"%+%toString(year)
    
    if (year==1986 & ipls==1){
      out_tab_csv <- out_tab
    }
    else{
      out_tab_csv <- rbind(out_tab_csv, out_tab)
    }
   
  }
  print(year)
}

col_names[1] = "pix"
colnames(out_tab_csv) = col_names
out_file = out_dir%+%"val_Bh13v15_tc.csv"
write.table(out_tab_csv, file=out_file,sep=",",col.names=T,row.names=F, quote=F)


