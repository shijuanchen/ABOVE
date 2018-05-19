# This script write FF (forest->forest), NF (non-forest->forest), NN (non-forest->non-forest) into categories

from osgeo import gdal, gdal_array, osr, ogr
import numpy as np
import logging
logger = logging.getLogger('dist_year')
fill = -32767
tile_name = 'Bh14v14'

def classify_FF(FF_tc_folder_path, FF_output_folder_path):

    year_avail = np.arange(1986, 2014, dtype=np.int16)

    nrows=6000
    ncols=6000
    
    for year in year_avail:
        map_array = np.ones((nrows, ncols, 1), dtype=np.int16) * fill
        FF_file = FF_tc_folder_path+'/'+tile_name+'_dTC_FF_' + str(year) +'.tif'
        print(FF_file)
        ds = gdal.Open(FF_file)
        FF_raster = ds.ReadAsArray()
        FF_array = np.array(FF_raster)
        
        # write FF_class, FF-Growth-4, FF-decline-5
        for i in np.arange(0, nrows):
            for j in np.arange(0,ncols):
                # delta wetness
                dw = FF_array[2, i, j]
                if dw > 0 :
                    map_array[i,j,0] = 4
                elif dw < 0 and dw > -30000:
                    map_array[i,j,0] = 5
        FF_outfile = FF_output_folder_path+'/'+tile_name+'_dTC_FF_' + str(year) +'_cl.tif'
            
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
        write_output(map_array, FF_outfile, grid_info, gdal_frmt, band_names=None, ndv=fill)

def classify_NF(NF_tc_folder_path, NF_output_folder_path):
    year_avail = np.arange(1986, 2014, dtype=np.int16)

    nrows=6000
    ncols=6000
    
    for year in year_avail:
        map_array = np.ones((nrows, ncols, 1), dtype=np.int16) * fill
        NF_file = NF_tc_folder_path+'/'+tile_name+'_dTC_NF_' + str(year) +'.tif'
        print(NF_file)
        ds = gdal.Open(NF_file)
        NF_raster = ds.ReadAsArray()
        NF_array = np.array(NF_raster)
        
        # write NF_class, NF-Growth-6
        for i in np.arange(0, nrows):
            for j in np.arange(0,ncols):
                dw = NF_array[2, i, j]
                if dw > -30000:
                    map_array[i,j,0] = 6
        NF_outfile = NF_output_folder_path+'/'+tile_name+'_dTC_NF_' + str(year) +'_cl.tif'
            
        img_file = gdal.Open(NF_file)
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
        write_output(map_array, NF_outfile, grid_info, gdal_frmt, band_names=None, ndv=fill)

def classify_NN(NN_tc_folder_path, NN_output_folder_path):

    year_avail = np.arange(1986, 2014, dtype=np.int16)

    nrows=6000
    ncols=6000
    
    for year in year_avail:
        map_array = np.ones((nrows, ncols, 1), dtype=np.int16) * fill
        NN_file = NN_tc_folder_path+'/'+tile_name+'_dTC_NN_' + str(year) +'.tif'
        print(NN_file)
        ds = gdal.Open(NN_file)
        NN_raster = ds.ReadAsArray()
        NN_array = np.array(NN_raster)
        
        """
        # write NN_class, (class 7 to 15)
        Class(dw>10 and dg>10)=7             Class(-30000<dw<-10 and dg>10)=8           Class(-10<dw<10 and dg>10)=9
        Class(dw>10 and -30000<dg<-10)=10    Class(-30000<dw<-10 and -30000<dg<-10)=11  Class(-10<dw<10 and -30000<dg<-10)=12
        Class(dw>10 and -10<dg<10)=13        Class(-30000<dw<-10 and -10<dg<10)=14      Class(-10<dw<10 and -10<dg<10)=15
        """
        for i in np.arange(0, nrows):
            for j in np.arange(0,ncols):
                dg = NN_array[1, i, j]
                dw = NN_array[2, i, j]
                if dw>10 and dg>10:
                    map_array[i,j,0] = 7
                elif -30000<dw<-10 and dg>10:
                    map_array[i,j,0] = 8
                elif -10<dw<10 and dg>10:
                    map_array[i,j,0] = 9
                elif dw>10 and -30000<dg<-10:
                    map_array[i,j,0] = 10
                elif -30000<dw<-10 and -30000<dg<-10:
                    map_array[i,j,0] = 11
                elif -10<dw<10 and -30000<dg<-10:
                    map_array[i,j,0] = 12
                elif dw>10 and -10<dg<10:
                    map_array[i,j,0] = 13
                elif -30000<dw<-10 and -10<dg<10:
                    map_array[i,j,0] = 14
                elif -10<dw<10 and -10<dg<10:
                    map_array[i,j,0] = 15
                else:
                    map_array[i,j,0] = fill
             
        NN_outfile = NN_output_folder_path+'/'+tile_name+'_dTC_NN_' + str(year) +'_cl.tif'
            
        img_file = gdal.Open(NN_file)
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
        write_output(map_array, NN_outfile, grid_info, gdal_frmt, band_names=None, ndv=fill)


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

tc_folder_path = r'/projectnb/landsat/projects/ABOVE/CCDC/'+tile_name+'/out_tc_4type'
output_folder_path = r'/projectnb/landsat/projects/ABOVE/CCDC/'+tile_name+'/out_category'

# process FF
#FF_tc_folder_path = r'/projectnb/landsat/users/shijuan/above/bh09v15/rand_forest_v4/FF'
#FF_output_folder_path = r'/projectnb/landsat/users/shijuan/above/bh09v15/rand_forest_v4/FF_class'
FF_tc_folder_path = tc_folder_path
FF_output_folder_path = output_folder_path
classify_FF(FF_tc_folder_path, FF_output_folder_path)

# process NF
#NF_tc_folder_path = r'/projectnb/landsat/users/shijuan/above/bh09v15/rand_forest_v4/NF'
#NF_output_folder_path = r'/projectnb/landsat/users/shijuan/above/bh09v15/rand_forest_v4/NF_class'
NF_tc_folder_path = tc_folder_path
NF_output_folder_path = output_folder_path
classify_NF(NF_tc_folder_path, NF_output_folder_path)

# process NN
#NN_tc_folder_path = r'/projectnb/landsat/users/shijuan/above/bh09v15/rand_forest_v4/NN'
#NN_output_folder_path = r'/projectnb/landsat/users/shijuan/above/bh09v15/rand_forest_v4/NN_class'
NN_tc_folder_path = tc_folder_path
NN_output_folder_path = output_folder_path
classify_NN(NN_tc_folder_path, NN_output_folder_path)
