# This script take random forest images as inputs and write disturbance year of the most recent 
# deforestation, degradation, and recovery. 

from osgeo import gdal, gdal_array, osr, ogr
import numpy as np
import click

def pixel_count(cl_folder_path, output_file_path, tile_name):

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
                for k in np.arange(1, class_num):
                    if int(pix) == k:
                        count[k] += 1
        print(count)
        f.write(str(year))
        f.write(',')
        wline1 = ','.join(str(x) for x in count)
        f.write(wline1)
        f.write('\n')
    f.close()
    
@click.command()
@click.option('--tile_name', default='Bh04v06', help='Name of the tile, for example: Bh04v06')    
             
def main(tile_name):
    cl_folder_path = r'/projectnb/landsat/projects/ABOVE/CCDC/{0}/out_classes'.format(tile_name)
    output_file_path = r'/projectnb/landsat/users/shijuan/above/area_estimates/pixel_counts/{0}_pc.txt'.format(tile_name)
    pixel_count(cl_folder_path, output_file_path, tile_name)
main()
