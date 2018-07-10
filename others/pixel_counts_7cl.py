# This script take random forest images as inputs and write disturbance year of the most recent 
# deforestation, degradation, and recovery. 

from osgeo import gdal, gdal_array, osr, ogr
import numpy as np

cl_folder_path = r'/projectnb/landsat/projects/ABOVE/CCDC/Bh09v15/out_classes'
output_file_path = r'/projectnb/landsat/users/shijuan/above/area_estimates/Bh09v15_7cl.txt'
tile_name = 'Bh09v15'
year_avail = np.arange(1986, 2014, dtype=np.int16)

nrows=6000
ncols=6000
fill = -32767

f=open(output_file_path, "w")
cl_values=np.arange(0,21)
f.write(',')
header=','.join(str(x) for x in cl_values)
f.write(header)
f.write('\n')
for year in year_avail:
    cl_file = cl_folder_path+'/'+tile_name+'_FF_FN_NF_NN_' + str(year) +'_cl.tif'
    print(cl_file)
    ds = gdal.Open(cl_file)
    cl_raster = ds.ReadAsArray()
    cl_array = np.array(cl_raster)
    class_num = 21    #zero is no change, only count for 1-6, and 19, 20
    count = np.zeros(class_num, dtype=np.int32)
    for i in np.arange(0, nrows):
        for j in np.arange(0,ncols):
            pix = cl_array[i, j]
            if int(pix) == fill:
                count[0] += 1
            for k in np.arange(1, 7):
                if int(pix) == i:
                    count[k] += 1
            if int(pix) == 19:
                count[19] += 1
            if int(pix) == 20:
                count[20] += 1
    print(count)
    f.write(str(year))
    f.write(',')
    wline1 = ','.join(str(x) for x in count)
    f.write(wline1)
    f.write('\n')
f.close()
    
    


                
