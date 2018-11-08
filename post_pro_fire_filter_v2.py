# This script improve the change map for agriculture area.

from osgeo import gdal, gdal_array, osr, ogr
import numpy as np
import logging
import click
from scipy import stats
logger = logging.getLogger('post_pro_agr')
fill = -32767

def post_process_fire_filter(tile_name, combine_folder, output_folder, window_size):
    
    year_avail = np.arange(1995, 1996, dtype=np.int16)
    nrows=6000
    ncols=6000
    CAN_LFDB = r'/projectnb/modislc/projects/above/tiles/CAN_LFDB/CAN_LFDB.'+ tile_name + '.tif'
    fdb_ds = gdal.Open(CAN_LFDB)
    fdb_raster = fdb_ds.ReadAsArray()
    fdb_array = np.array(fdb_raster)
    
    for year in year_avail:

        cc_file = combine_folder+'/'+tile_name+'_FF_FN_NF_NN_' + str(year) + '_cl.tif'
        cc_ds = gdal.Open(cc_file)
        cc_raster = cc_ds.ReadAsArray()
        cc_array = np.array(cc_raster)
        
        map_array = np.ones((nrows, ncols, 1), dtype=np.int16) * fill 
        n = int(window_size) 
        k = int((n-1)/2)
        
        #preserve the border
        map_array[0:k+1,:, 0] = cc_array[0:k+1, :]
        map_array[:,0:k+1, 0] = cc_array[:, 0:k+1]
        map_array[nrows-k:nrows,:,0] = cc_array[nrows-k:nrows, :]
        map_array[:, nrows-k:nrows,0] = cc_array[:, nrows-k:nrows]
        for i in np.arange(k, nrows-k):
            for j in np.arange(k,ncols-k):  
                cc = int(cc_array[i, j])
                map_array[i, j, 0] = cc   
                if cc==1 or cc==20:
                    if abs(int(fdb_array[i, j]) + 1792 - year) <= 2:
                       # print('Y')
                        map_array[i, j, 0] = cc
                    else:
                        window = np.array(cc_array[i-k:i+k+1, j-k:j+k+1])
                        #print(window)
                        window = np.reshape(window, n * n)
                        cc_win = []
                        for pix in window:
                            pix = int(pix)
                            if pix==5:
                                pix = 2
                            if pix != fill:
                                cc_win.append(pix)
                        if cc_win:
                            mode = stats.mode(cc_win, axis=None)
                            map_array[i, j, 0] = mode[0]                     
                                     
        outfile = output_folder+'/'+tile_name+'_FF_FN_NF_NN_' + str(year) +'_cl_' + str(window_size) + '_v2.tif'
            
        img_file = gdal.Open(cc_file)
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

@click.command()
@click.option('--tile_name', default='Bh04v06', help='Name of the tile, for example: Bh04v06')
@click.option('--window_size', default='5', help='window size of fire filter')
def main(tile_name, window_size):
    combine_folder = r'/projectnb/landsat/projects/ABOVE/CCDC/{0}/out_classes'.format(tile_name)
    output_folder = r'/projectnb/landsat/users/shijuan/above/post_process/fire_filtering/{0}'.format(tile_name)
    post_process_fire_filter(tile_name, combine_folder, output_folder, window_size)

main()

