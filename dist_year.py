# This script take random forest images as inputs and write disturbance year of the most recent 
# deforestation, degradation, and recovery. 

from osgeo import gdal, gdal_array, osr, ogr
import numpy as np
import logging
logger = logging.getLogger('dist_year')

rf_folder_path = r'/projectnb/landsat/users/shijuan/above/bh09v15/rand_forest/rf_img_v3'
output_file_path = r'/projectnb/landsat/users/shijuan/above/bh09v15/rand_forest/rf_year_v3.tif'
tile_name = 'Bh09v15'
year_avail = np.arange(1985, 2014, dtype=np.int16)

nrows=6000
ncols=6000
fill = -32767
map_array = np.ones((nrows, ncols, 3), dtype=np.int16) * fill
# map_array updates everytime when read the image for a new year 
print(map_array.shape)
for year in year_avail:
    rf_file = rf_folder_path+'/'+tile_name+'_dTC_F_' + str(year) +'_rf.tif'
    print(rf_file)
    ds = gdal.Open(rf_file)
    rf_raster = ds.ReadAsArray()
    rf_array = np.array(rf_raster)
    for i in np.arange(0, nrows):
        for j in np.arange(0,ncols):
            # write deforestation 1:fire, 3:logging
            pix = rf_array[i, j]
            if int(pix)==1 or int(pix)==3:
                map_array[i,j,0] = year
            # write degradation 2: degradation
            if int(pix)==2:
                map_array[i,j,1] = year
            # write recovery 4:recovery
            if int(pix)==4:
                map_array[i,j,2] = year
        
img_file = gdal.Open(rf_file)
geo_info = img_file.GetGeoTransform()
ulx = geo_info[0]
pix_x = geo_info[1]
uly = geo_info[3]
pix_y = geo_info[5]
cols = img_file.RasterXSize
rows = img_file.RasterYSize
proj_info = img_file.GetProjection()
grid_info = {'nrows':rows, 'ncols':cols, 'projection':proj_info, 
             'ulx':ulx, 'pix_x':pix_x, 'uly':uly, 'pix_y':pix_y}
gdal_frmt = 'GTiff'

# MAPPING UTILITIES
def write_output(raster, output, grid_info, gdal_frmt, band_names=None, ndv=fill):
    """ Write raster to output file """
    

    logger.debug('Writing output to disk')
    driver = gdal.GetDriverByName(str(gdal_frmt))

    if len(raster.shape) > 2:
        nband = raster.shape[2]
    else:
        nband = 1

    ds = driver.Create(
        output,
        grid_info['ncols'], grid_info['nrows'], nband,
        gdal_array.NumericTypeCodeToGDALTypeCode(raster.dtype.type)
    )

    if band_names is not None:
        if len(band_names) != nband:
            logger.error('Did not get enough names for all bands')
            sys.exit(1)

    if raster.ndim > 2:
        for b in range(nband):
            logger.debug('    writing band {b}'.format(b=b + 1))
            ds.GetRasterBand(b + 1).WriteArray(raster[:, :, b])
            ds.GetRasterBand(b + 1).SetNoDataValue(ndv)

            if band_names is not None:
                ds.GetRasterBand(b + 1).SetDescription(band_names[b])
                ds.GetRasterBand(b + 1).SetMetadata({
                    'band_{i}'.format(i=b + 1): band_names[b]
                })
    else:
        logger.debug('    writing band')
        ds.GetRasterBand(1).WriteArray(raster)
        ds.GetRasterBand(1).SetNoDataValue(ndv)

        if band_names is not None:
            ds.GetRasterBand(1).SetDescription(band_names[0])
            ds.GetRasterBand(1).SetMetadata({'band_1': band_names[0]})
    #print(grid_info["projection"])
    ds.SetProjection(grid_info["projection"])
    ## the geo transform goes - ulx, pix_x(w-e pixel resolution), easting, uly, northing, pix_y(n-s pixel resolution, negative value)
    ds.SetGeoTransform((grid_info["ulx"],grid_info["pix_x"],0,
                        grid_info["uly"],0,grid_info["pix_y"]))

    ds = None

write_output(map_array, output_file_path, grid_info, gdal_frmt, band_names=None, ndv=-9999)

