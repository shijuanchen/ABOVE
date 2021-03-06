# This script reorganize the csv data sheets. 
rm(list=ls())

"%+%" <- function(x,y) paste(x,y,sep="")
args <- commandArgs(trailingOnly=TRUE)
tile_name <- args[1]
out_dir = "/projectnb/landsat/users/shijuan/above/training_data/0725_training/FN/"
tc_csv_path = out_dir%+%tile_name%+%"_tc_FN.csv"
interpt_csv_path = out_dir%+%tile_name%+%"_pts_FN.csv"
out_csv_path = out_dir%+%tile_name%+%"_combined_FN.csv"
  
tc_df <- read.csv(file=tc_csv_path, header=TRUE, sep=",",stringsAsFactors=FALSE)
interpt_df <- read.csv(file=interpt_csv_path, header=TRUE, sep=",",stringsAsFactors=FALSE)

n_pix = nrow(interpt_df)
out_tab = array(NA,dim=c(n_pix, 10))
colnames(out_tab) = c("shp_id","dis_year","agent","ag_label","db","dg","dw","pb","pg","pw")

# reorder by ID
interpt_df <- interpt_df[order(interpt_df[,'shp_id']),]
out_tab[,'shp_id'] <- interpt_df[,'shp_id']
out_tab[,'agent'] <- interpt_df[,'agent']
out_tab[,'ag_label'] <- interpt_df[,'ag_label']

# get disturbance year
for(i in 1:n_pix){
  dis_time <- interpt_df[i,'year']
  if(!is.na(dis_time)){
    out_tab[i,'dis_year'] = substr(dis_time, start=1, stop=4)
  }
}

# get db, dg, dw
tc_colname = colnames(tc_df)
num_col = length(tc_df[1,])
for(j in 1:n_pix){
  for(k in 1:num_col){
    tc_year = substr(tc_colname[k],start=4, stop=7)
    if(identical(toString(out_tab[j,'dis_year']), tc_year)){
        #print(tc_colname[k])
        dtc = substr(tc_colname[k],start=1, stop=2)
        if(dtc=='db'){
          out_tab[j,'db'] = tc_df[j,tc_colname[k]]
        }
        if(dtc=='dg'){
          out_tab[j,'dg'] = tc_df[j,tc_colname[k]]
        }
        if(dtc=='dw'){
          out_tab[j,'dw'] = tc_df[j,tc_colname[k]]
        }
        if(dtc=='pb'){
          out_tab[j,'pb'] = tc_df[j,tc_colname[k]]
        }
        if(dtc=='pg'){
          out_tab[j,'pg'] = tc_df[j,tc_colname[k]]
        }
        if(dtc=='pw'){
          out_tab[j,'pw'] = tc_df[j,tc_colname[k]]
        }
        
    }
  }
}
write.table(out_tab,file=out_csv_path,sep=",",col.names=F,row.names=F,quote=F)
