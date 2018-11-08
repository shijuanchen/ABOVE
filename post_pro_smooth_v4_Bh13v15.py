# This script improve the change map for agriculture area.

from osgeo import gdal, gdal_array, osr, ogr
import numpy as np
import logging
import click
from scipy import stats
logger = logging.getLogger('post_pro_agr')
fill = -32767

def post_process_smoothing(tile_name, combine_folder, category_folder, lc_folder, output_folder):
    
    year_avail = np.arange(1986, 2013, dtype=np.int16)
    #year_avail = np.arange(1995, 1996, dtype=np.int16)
    nrows=6000
    ncols=6000

    for year in year_avail:
        print(year)
        fire_y0 = r'/projectnb/landsat/users/shijuan/above/ABOVE_fires/test_tiles/output/' + tile_name + '/' \
                  +tile_name+'_fireBD_'+ str(year-1) + '.tif'
        fire_y1 = r'/projectnb/landsat/users/shijuan/above/ABOVE_fires/test_tiles/output/' + tile_name + '/' \
                  +tile_name+'_fireBD_'+ str(year)  + '.tif'
        fire_y2 = r'/projectnb/landsat/users/shijuan/above/ABOVE_fires/test_tiles/output/' + tile_name + '/' \
                  +tile_name+'_fireBD_'+ str(year+1) + '.tif'
        fdb_ds0 = gdal.Open(fire_y0)
        fdb_raster0 = fdb_ds0.ReadAsArray()
        fdb_array0 = np.array(fdb_raster0)
        
        fdb_ds1 = gdal.Open(fire_y1)
        fdb_raster1 = fdb_ds1.ReadAsArray()
        fdb_array1 = np.array(fdb_raster1)
        
        fdb_ds2 = gdal.Open(fire_y2)
        fdb_raster2 = fdb_ds2.ReadAsArray()
        fdb_array2 = np.array(fdb_raster2)
        
        cc_file = combine_folder+'/'+tile_name+'_FF_FN_NF_NN_' + str(year) + '_cl.tif'
        cc_ds = gdal.Open(cc_file)
        cc_raster = cc_ds.ReadAsArray()
        cc_array = np.array(cc_raster)
        
        ct_file = category_folder+'/'+tile_name+ '_dTC_NN_' + str(year) + '_cl.tif'
        ct_ds = gdal.Open(ct_file)
        ct_raster = ct_ds.ReadAsArray()
        ct_array = np.array(ct_raster)
        
        lc_af_file = lc_folder+'/'+tile_name+ '_' + str(year) + '_tc_20180416_noGeo_k55_pam_rf_remap.tif'
        lc_af_ds = gdal.Open(lc_af_file)
        lc_af_raster = lc_af_ds.ReadAsArray()
        lc_af_array = np.array(lc_af_raster)
        
        lc_bf_file = lc_folder+'/'+tile_name+ '_' + str(year-1) + '_tc_20180416_noGeo_k55_pam_rf_remap.tif'
        lc_bf_ds = gdal.Open(lc_bf_file)
        lc_bf_raster = lc_bf_ds.ReadAsArray()
        lc_bf_array = np.array(lc_bf_raster)
        
        map_array = np.ones((nrows, ncols, 1), dtype=np.int16) * fill 
        window_size = 11
        n = int(window_size) 
        k = int((n-1)/2)
        
        window_size_s = 5  # a smaller window size for general filtering
        ns = int(window_size_s) 
        ks = int((ns-1)/2)
        
        #preserve the border
        map_array[0:k+1,:, 0] = cc_array[0:k+1, :]
        map_array[:,0:k+1, 0] = cc_array[:, 0:k+1]
        map_array[nrows-k:nrows,:,0] = cc_array[nrows-k:nrows, :]
        map_array[:, nrows-k:nrows,0] = cc_array[:, nrows-k:nrows]
        for i in np.arange(k, nrows-k):
            for j in np.arange(k,ncols-k):  
                cc = int(cc_array[i, j])
                map_array[i, j, 0] = cc   
                # if the pixel is FN fire (1)
                if cc == 1:
                    # if in fire database, it is fire
                    if (fdb_array0[i, j] == 1 or fdb_array1[i, j] == 1 or fdb_array2[i, j]) == 1:
                        map_array[i, j, 0] = 1
                    else:
                    # if out of fire database
                        window = np.array(cc_array[i-k:i+k+1, j-k:j+k+1])
                        window = np.reshape(window, n * n)
                        cc_win_FN = []                        
                        fn_fire = 0
                        for pix in window:
                            pix = int(pix)
                            if pix > fill:
                                if pix == 1 or 20:
                                    fn_fire += 1
                                elif pix == 2 or pix == 3 or pix == 19:
                                    cc_win_FN.append(pix)
                        # if more than half is fire, it is fire.
                        if fn_fire > 60:
                            map_array[i, j, 0] = 1
                        # else take the most frequent non-fire FN class
                        else:
                            if cc_win_FN:
                                mode = stats.mode(cc_win_FN, axis=None)
                                map_array[i, j, 0] = mode[0] 
                            # if it is null assign to 19
                            else:
                                map_array[i, j, 0] = 19
                # if the pixel is FN insects, FN logging or FN others
                elif cc == 2 or cc==3 or cc==19:
                    # if the pixel is in the fire database (exact the same year)
                    if (fdb_array1[i, j] == 1):
                        window_s = np.array(cc_array[i-ks:i+ks+1, j-ks:j+ks+1])
                        window_s = np.reshape(window_s, ns * ns)
                        cc_win_FN = []
                        for pix in window_s:
                                pix = int(pix)
                                if pix==1 or pix==2 or pix==3 or pix==19:
                                    cc_win_FN.append(pix)
                        if cc_win_FN:
                            mode = stats.mode(cc_win_FN, axis=None)
                            # if the plurality is fire, it is fire
                            if mode[0]==1:                         
                                map_array[i, j, 0] = 1
                    # if the pixel is out of the fire database
                    else:
                        window_s = np.array(cc_array[i-ks:i+ks+1, j-ks:j+ks+1])
                        window_s = np.reshape(window_s, ns * ns)
                        cc_win_FN_no_fire = []
                        for pix in window_s:
                                pix = int(pix)
                                if pix==2 or pix==3 or pix==19:
                                    cc_win_FN_no_fire.append(pix)
                        if cc_win_FN_no_fire:
                            mode = stats.mode(cc_win_FN_no_fire, axis=None)
                            map_array[i, j, 0] = mode[0]
                # if the pixel is NN fire
                elif cc==20:
                    # if the pixel is in the database
                    if (fdb_array0[i, j] == 1 or fdb_array1[i, j] == 1 or fdb_array2[i, j] == 1):
                        map_array[i, j, 0] = 20
                    # if the pixel is outside fire database    
                    else:
                        # if there is no land cover change before and after, it is no fire
                        if int(lc_bf_array[i, j]) == int(lc_af_array[i, j]):
                            map_array[i, j, 0] = ct_array[i, j]
                        # if less than half of pixel is not fire, it is not fire
                        window = np.array(cc_array[i-k:i+k+1, j-k:j+k+1])
                        window = np.reshape(window, n * n)                      
                        nn_fire = 0
                        for pix in window:
                            pix = int(pix)
                            if pix == 20 or 1:
                                nn_fire += 1
                        # if less than a half is fire, it is not fire
                        if nn_fire < 60:
                            map_array[i, j, 0] = ct_array[i, j]

                elif cc >= 7 and cc <= 15:
                    # if the pixel is in the fire database
                    if (fdb_array1[i, j] == 1):
                        window_s = np.array(cc_array[i-ks:i+ks+1, j-ks:j+ks+1])
                        window_s = np.reshape(window_s, ns * ns)
                        cc_win_NN = []
                        for pix in window:
                            pix = int(pix)
                            if pix >= 7 and pix <= 15 or pix==20:
                                cc_win_NN.append(pix)
                        if cc_win_NN:
                            mode = stats.mode(cc_win_NN, axis=None)
                            if mode[0] == 20:
                                map_array[i, j, 0] == 20
                                     
        outfile = output_folder+'/'+tile_name+'_FF_FN_NF_NN_' + str(year) +'_cl_' + str(window_size) + '_sm_v4.tif'
            
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
    #combine_folder = r'/projectnb/landsat/projects/ABOVE/CCDC/{0}/out_classes'.format(tile_name)
    combine_folder = r'/projectnb/landsat/users/zhangyt/above/out_class_sample/{0}/out_classes'.format(tile_name)
    #category_folder = r'/projectnb/landsat/projects/ABOVE/CCDC/{0}/out_category'.format(tile_name)
    category_folder = r'/projectnb/landsat/users/zhangyt/above/out_class_sample/{0}/out_category'.format(tile_name)
    lc_folder = r'/projectnb/modislc/users/jonwang/data/rf/rast/tc_20180416_noGeo_k55_pam_rf/{0}/remap'.format(tile_name)
    output_folder = r'/projectnb/landsat/users/shijuan/above/post_process/smooth_v4/{0}'.format(tile_name)
    post_process_smoothing(tile_name, combine_folder, category_folder, lc_folder, output_folder)

main()

