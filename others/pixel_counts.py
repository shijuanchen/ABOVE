# This script take random forest images as inputs and write disturbance year of the most recent 
# deforestation, degradation, and recovery. 

from osgeo import gdal, gdal_array, osr, ogr
import numpy as np
import logging
logger = logging.getLogger('dist_year')

rf_folder_path = r'/projectnb/landsat/users/shijuan/above/bh09v15/rand_forest_v3/rf_map'
output_file_path = r'/projectnb/landsat/users/shijuan/above/bh09v15/rand_forest_v3/rf_map/area_2008.txt'
tile_name = 'Bh09v15'
year_avail = np.arange(2008, 2009, dtype=np.int16)

nrows=6000
ncols=6000
fill = -32767

for year in year_avail:
    rf_file = rf_folder_path+'/'+tile_name+'_dTC_F_or_F_' + str(year) +'_rf.tif'
    print(rf_file)
    ds = gdal.Open(rf_file)
    rf_raster = ds.ReadAsArray()
    rf_array = np.array(rf_raster)
    count = [0, 0, 0, 0, 0, 0, 0]
    weight = [0, 0, 0, 0, 0, 0, 0]
    for i in np.arange(0, nrows):
        for j in np.arange(0,ncols):
            pix = rf_array[i, j]
            if int(pix)<1 or int(pix)>5:
                count[0] +=1
            if int(pix)==1:
                count[1] +=1
            if int(pix)==2:
                count[2] +=1
            if int(pix)==3:
                count[3] +=1
            if int(pix)==4:
                count[4] +=1
            if int(pix)==5:
                count[5] += 1
    for k in np.arange(0,6):
        weight[k] = count[k]/(ncols*nrows*1.0)
    f=open(output_file_path, "w")
    count[6] = np.sum(count)
    weight[6] = np.sum(weight)
    wline1 = ','.join(str(x) for x in count)
    wline2=','.join(str(x) for x in weight)
    f.write(wline1)
    f.write('\n')
    f.write(wline2)
    f.close()
    
    


                
