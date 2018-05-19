# This script write FF (forest->forest), NF (non-forest->forest), NN (non-forest->non-forest) into categories

from osgeo import gdal, gdal_array, osr, ogr
import numpy as np
import logging
logger = logging.getLogger('dist_year')
fill = -32767
tile_name = 'Bh14v14'
def combine_FF_FN_NF_NN_class(FF_folder_path, FN_folder_path, NF_folder_path, NN_folder_path, output_folder_path):
    
    year_avail = np.arange(1986, 2014, dtype=np.int16)

    nrows=6000
    ncols=6000
    
    for year in year_avail:
        map_array = np.ones((nrows, ncols, 1), dtype=np.int16) * fill
        FF_file = FF_folder_path+'/'+tile_name+'_dTC_FF_' + str(year) +'_cl.tif'
        FN_file = FN_folder_path+'/'+tile_name+'_dTC_FN_' + str(year) +'_rf.tif'
        NF_file = NF_folder_path+'/'+tile_name+'_dTC_NF_' + str(year) +'_cl.tif'
        NN_file = NN_folder_path+'/'+tile_name+'_dTC_NN_' + str(year) +'_cl.tif'
        NN_file_rf = NN_folder_path+'/'+tile_name+'_dTC_NN_' + str(year) +'_rf.tif'

        FF_ds = gdal.Open(FF_file)
        FF_raster = FF_ds.ReadAsArray()
        FF_array = np.array(FF_raster)
        
        FN_ds = gdal.Open(FN_file)
        FN_raster = FN_ds.ReadAsArray()
        FN_array = np.array(FN_raster)
        
        NF_ds = gdal.Open(NF_file)
        NF_raster = NF_ds.ReadAsArray()
        NF_array = np.array(NF_raster)
        
        NN_ds = gdal.Open(NN_file)
        NN_raster = NN_ds.ReadAsArray()
        NN_array = np.array(NN_raster)
        
        NN_ds_rf = gdal.Open(NN_file_rf)
        NN_raster_rf = NN_ds_rf.ReadAsArray()
        NN_array_rf = np.array(NN_raster_rf)
        
        # write all 16 classes
        for i in np.arange(0, nrows):
            for j in np.arange(0,ncols):
                # get category, if there is change, one value should be 1-15 or 20-21, the other three should be -32767, so we take the max
                # if there is no change. max is -32767
                
                category = max(FF_array[i, j], FN_array[i, j], NF_array[i, j], NN_array[i, j], NN_array_rf[i, j])
                if category == 21:
                    category = NN_array[i, j]
                map_array[i, j, 0] = int(category)
        outfile = output_folder_path+'/'+tile_name+'_FF_FN_NF_NN_' + str(year) +'_cl.tif'
            
        img_file = gdal.Open(FF_file)
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
        write_output(map_array, outfile, grid_info, gdal_frmt, band_names=None, ndv=fill)

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

category_folder = r'/projectnb/landsat/projects/ABOVE/CCDC/'+tile_name+'/out_category'
FF_folder_path = category_folder
FN_folder_path = category_folder
NF_folder_path = category_folder
NN_folder_path = category_folder
output_folder_path = r'/projectnb/landsat/projects/ABOVE/CCDC/'+tile_name+'/out_classes'
combine_FF_FN_NF_NN_class(FF_folder_path,FN_folder_path,NF_folder_path,NN_folder_path, output_folder_path)

