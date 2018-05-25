# This script makes plots of Tasseled Cap metrics, brightness, greenness and wetness

import numpy as np
import matplotlib.pyplot as plt
# question why "from ..utils import write_output" gave an error of "attempted relative import beyond top-level package"
from osgeo import gdal, gdal_array, osr, ogr
import logging
import pdb
import click
logger = logging.getLogger('yatsm')

def plot_bgw(npz_file_path, outdir_path):
    """
    Read in .npz.npy file and make plots
    Args:
        npz_file_path: input npz_file_path of TC metrics of all breaks
        outdir_path: output directory path of all figures
    Return:
        None
    """
    data_arr = np.load(npz_file_path)
    print('Loading .npz.npy file...')  
    # data_arr.keys() to get the key 'arr_0', 
      
    data_arr = data_arr['arr_0'] 
    # now data_arr contains all pix lists
    dif_bright = []
    dif_green = []
    dif_wet = []
    dif_nbr = []
    num_brk_list = []
    
    for chunk in data_arr:
        for pix in chunk:
            num_brk = int((len(pix) - 2 ) / 10)       # 10 varibles for each break ((ID), Year, Date, dnbr, nbr...)
            num_brk_list.append(num_brk)
            for i in np.arange(0, num_brk):
                dif_nbr.append(pix[10 * i + 5])
                dif_bright.append(pix[10 * i + 7])
                dif_green.append(pix[10 * i + 9])
                dif_wet.append(pix[10 * i + 11])    
        
    fig_brk = plt.figure()
    bins_value = np.arange(min(num_brk_list), max(num_brk_list)+1, 1)
    plt.hist(num_brk_list, bins=bins_value)
    plt.xticks(bins_value)
    plt.savefig(outdir_path + 'hist_break.png')
    plt.show()
    
    fig = plt.figure()
    ax1 = fig.add_subplot(2, 2, 1)
    ax2 = fig.add_subplot(2, 2, 2)
    ax3 = fig.add_subplot(2, 2, 3)
    ax4 = fig.add_subplot(2, 2, 4)
    
    #bins_value = np.arange(-10000, 10000, 500)
    bins_value = np.arange(-5000, 5000, 200)
    #bins_value = np.arange(-2500, 2500, 100)  
    #bins_value = np.arange(-1000, 1000, 50)
    
    # plot histograms of delta bgw
    print('Drawing histogram...')
    ax1.hist(dif_bright, bins=bins_value)
    ax1.set_title('Brightness differences')
    ax2.hist(dif_green, bins=bins_value)
    ax2.set_title('Greenness differences')
    ax3.hist(dif_wet, bins=bins_value)
    ax3.set_title('Wetness differences')
    ax4.hist(dif_nbr, bins=bins_value)
    ax4.set_title('NBR differences')
    plt.tight_layout()
    plt.savefig(outdir_path+'hist.png')
    plt.show()
    
    # plot scatter plots of delta bgw
    fig2, axes = plt.subplots(1, 3, figsize=(20, 5))
    # random sample 5000 points
    rand_id = np.random.choice(np.arange(len(dif_bright)), 5000, replace=False)
    dif_bright_sample = np.take(dif_bright,rand_id)
    dif_green_sample = np.take(dif_green,rand_id)
    dif_wet_sample = np.take(dif_wet, rand_id)
    dif_nbr_sample = np.take(dif_nbr, rand_id)
    
    axes[0].plot(dif_bright_sample,dif_green_sample, 'b.', markersize=1)
    axes[0].set_xlabel('D_Brightness')
    axes[0].set_ylabel('D_Greenness')
    bright_green_cf = np.corrcoef(dif_bright_sample,dif_green_sample)
    axes[0].set_title('D_Brightness VS D_Greenness R={:.3}'.format(bright_green_cf[0][1]))
    
    axes[1].plot(dif_bright_sample,dif_wet_sample, 'b.', markersize=1)
    axes[1].set_xlabel('D_Brightness')
    axes[1].set_ylabel('D_Wetness')
    bright_wet_cf = np.corrcoef(dif_bright_sample,dif_wet_sample)
    axes[1].set_title('D_Brightness VS D_Wetness R={:.3}'.format(bright_wet_cf[0][1]))
    
    axes[2].plot(dif_green_sample,dif_wet_sample, 'b.', markersize=1)
    axes[2].set_xlabel('D_Greenness')
    axes[2].set_ylabel('D_Wetness')
    green_wet_cf = np.corrcoef(dif_green_sample,dif_wet_sample)
    axes[2].set_title('D_Greenness VS D_Wetness R={:.3}'.format(green_wet_cf[0][1]))
    
    for ax in axes:
        ax.set_xlim(-2500, 2500)
        ax.set_ylim(-2500, 2500)

    plt.tight_layout()
    plt.savefig(outdir_path+'bgw_scatter_plots.png')
    plt.show()
    plt.close()
    
	# plot scatter plots of delta nbr vs delta bgw
    fig3, axes = plt.subplots(1, 3, figsize=(20, 5))
    
    axes[0].plot(dif_nbr_sample,dif_green_sample, 'b.', markersize=1)
    axes[0].set_xlabel('D_NBR')
    axes[0].set_ylabel('D_Greenness')
    nbr_green_cf = np.corrcoef(dif_nbr_sample,dif_green_sample)
    axes[0].set_title('D_NBR VS D_Greenness R={:.3}'.format(nbr_green_cf[0][1]))
    
    axes[1].plot(dif_nbr_sample,dif_wet_sample, 'b.', markersize=1)
    axes[1].set_xlabel('D_NBR')
    axes[1].set_ylabel('D_Wetness')
    nbr_wet_cf = np.corrcoef(dif_nbr_sample,dif_wet_sample)
    axes[1].set_title('D_NBR VS D_Wetness R={:.3}'.format(nbr_wet_cf[0][1]))
    
    axes[2].plot(dif_nbr_sample,dif_bright_sample, 'b.', markersize=1)
    axes[2].set_xlabel('D_NBR')
    axes[2].set_ylabel('D_Brightness')
    nbr_bright_cf = np.corrcoef(dif_nbr_sample,dif_bright_sample)
    axes[2].set_title('D_NBR VS D_Brightness R={:.3}'.format(nbr_bright_cf[0][1]))
    
    for ax in axes:
        ax.set_xlim(-5000, 5000)
        ax.set_ylim(-5000, 5000)
	
    plt.tight_layout()
    plt.savefig(outdir_path+'nbr_bgw_plots.png')
    plt.show()
    plt.close()
    return

def map_bgw(npz_file_path, img_file_path, outdir_path):
    """
    Read in .npz.npy file and make maps
    Args:
        npz_file_path: input npz_file_path of TC metrics of all breaks
        outdir_path: output directory path of maps of delta TC metrics for each year
    Return:
        None
    """
    data_arr = np.load(npz_file_path)
    print('Loading .npz.npy file...')    
    data_arr = data_arr['arr_0']    # data_arr.keys() to get the key 'arr_0', 
    # now data_arr contains all data
    year_avail = np.arange(1985, 2014, dtype=np.int16)  # [1985, 2014) No changes in the first year or last year
    #year_avail = np.arange(2009, 2010, dtype=np.int16)
    fill = -32767
    nrows = 6000
    ncols = 6000
    n_mets = 3
    for year in year_avail:
        map_array = np.ones((nrows, ncols, n_mets), dtype=np.int16) * int(fill)
        for chunk in data_arr:
            for pix in chunk:
                num_brk = int((len(pix) - 2 ) / 10)       # 10 varibles for each break ((ID), Year, Date, dnbr, nbr...)
                chunk_id = pix[0]
                pix_id = pix[1]
                # chunk_indict is the chunk indicator that indicates if it is in the first row
                # or in the second row of a chunk
                chunk_indict = int(pix_id / 6000)
                x = chunk_id * 2 + chunk_indict
                y = int(pix_id % 6000)
                  
                loc_yr = 0        
                for i in np.arange(0, num_brk):
                    yr_dist = pix[10*i+2]
                    if int(yr_dist) == int(year):
                        loc_yr = 10*i+2
                
                if loc_yr > 0:
                    db = pix[loc_yr + 5]
                    dg = pix[loc_yr + 7]
                    dw = pix[loc_yr + 9]
                    if abs(db) < 10000 and abs(dg) < 10000 and abs(dw) < 10000:
                        map_array[x, y, 0] = db
                        map_array[x, y, 1] = dg
                        map_array[x, y, 2] = dw
        tile_name = npz_file_path.split('.')[0].split('/')[-1]
        output = "{0}/{1}_dTC_{2}.tif".format(outdir_path, tile_name, year)
        img_file = gdal.Open(img_file_path)
        geo_info = img_file.GetGeoTransform()
        #proj_info = img_file.GetProjection()
        ulx = geo_info[0]
        uly = geo_info[3]
        cols = img_file.RasterXSize
        rows = img_file.RasterYSize
        #get projection from a shapefile 
        driver = ogr.GetDriverByName('ESRI Shapefile')
        shp = driver.Open(r'/projectnb/landsat/projects/ABOVE/validation/make_sample_110517/val_out_110517/val_Bh09v15.shp')
        layer = shp.GetLayer()
        spatialRef = layer.GetSpatialRef()
        prj_wkt = spatialRef.ExportToWkt()
        #print('prj_wkt={}'.format(prj_wkt))
        grid_info = {'nrows':rows, 'ncols':cols, 'projection':prj_wkt, 
                     'ulx':ulx, 'pix_x':30, 'uly':uly, 'pix_y':-30}
        gdal_frmt = 'GTiff'
        
        write_output(map_array, output, grid_info, gdal_frmt, ndv=fill)
        
# MAPPING UTILITIES
def write_output(raster, output, grid_info, gdal_frmt, band_names=None, ndv=-9999):
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

#npz_file_path = r'/projectnb/landsat/users/shijuan/above/bh04v06_tc/plot_bgw/Bh10v15/Bh10v15.all_breaks.npy.npz'
#outdir_path = r'/projectnb/landsat/users/shijuan/above/bh04v06_tc/plot_bgw/Bh10v15'
#plot_bgw(npz_file_path, outdir_path)

@click.command()
@click.option('--tile_name', default='Bh04v06', help='Name of the tile, for example: Bh04v06')
def main(tile_name):
	npz_file_path = r'/projectnb/landsat/projects/ABOVE/CCDC/{0}/{0}.all_breaks.npy.npz'.format(tile_name)
	img_file_path = r'/projectnb/landsat/projects/ABOVE/CCDC/{0}/out_tif/{0}_1984.tif'.format(tile_name)
	outdir_path = r'/projectnb/landsat/projects/ABOVE/CCDC/{0}/out_tc'.format(tile_name)
	map_bgw(npz_file_path, img_file_path, outdir_path)

main()

#driver = ogr.GetDriverByName('ESRI Shapefile')
#shp = driver.Open(r'/projectnb/landsat/projects/ABOVE/validation/make_sample_110517/val_out_110517/val_Bh09v15.shp')
#layer = shp.GetLayer()
#spatialRef = layer.GetSpatialRef()


