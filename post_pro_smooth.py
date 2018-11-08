# This script improve the change map for agriculture area.

from osgeo import gdal, gdal_array, osr, ogr
import numpy as np
import logging
import click
from scipy import stats
logger = logging.getLogger('post_pro_agr')
fill = -32767

def post_process_filter(tile_name, combine_folder, output_folder):
    
    year_avail = np.arange(1986, 2014, dtype=np.int16)
    nrows=6000
    ncols=6000
    
    for year in year_avail:

        cc_file = combine_folder+'/'+tile_name+'_FF_FN_NF_NN_' + str(year) +'_cl.tif'
        cc_ds = gdal.Open(cc_file)
        cc_raster = cc_ds.ReadAsArray()
        cc_array = np.array(cc_raster)
        
        map_array = np.ones((nrows, ncols, 1), dtype=np.int16) * fill  
             
        for i in np.arange(1, nrows-1):
            for j in np.arange(1,ncols-1):  
               cc = int(cc_array[i, j])
               map_array[i, j, 0] = cc
               window = np.array([cc_array[i-1, j-1], cc_array[i-1, j], cc_array[i-1, j+1], \
                                 cc_array[i,   j-1],                   cc_array[i,   j+1], \
                                 cc_array[i+1, j-1], cc_array[i+1, j], cc_array[i+1, j+1] ])
               if cc != fill:
                   if max(window) == min(window) == fill:
                       map_array[i, j, 0] = fill
                   else:
                       cc_win = []
                       cc_win.append(cc)
                       for x in window:
                           if x != fill:
                               cc_win.append(x) 
                       mode =stats.mode(cc_win, axis=None)
                       map_array[i, j, 0] = str(mode[0][0])
 #           print("cc={0}, window={1}, map={2}".format(cc, window, map_array[i, j, 0]))        
                       
                                     
        outfile = output_folder+'/'+tile_name+'_FF_FN_NF_NN_' + str(year) +'_cl.tif'
            
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
def main(tile_name):

    combine_folder = r'/projectnb/landsat/projects/ABOVE/CCDC/{0}/out_classes'.format(tile_name)
    output_folder = r'/projectnb/landsat/users/shijuan/above/post_process/filtering/{0}'.format(tile_name)
    post_process_filter(tile_name, combine_folder, output_folder)

main()

