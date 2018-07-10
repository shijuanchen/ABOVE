""" Functions relevant for mapping abrupt changes
"""
from datetime import datetime as dt
import logging
import pdb
import re
import patsy
from timeit import default_timer as timer

## for spatial filtering
import scipy.ndimage

import numpy as np
## for parallel job running
from joblib import Parallel, delayed, load, dump
from multiprocessing import Pool, cpu_count
import tempfile
import os

## load functions from other yatsm scripts
from .utils import find_result_attributes, find_indices
from ..utils import find_results, iter_records, write_output
from ..regression.transforms import harm
from .pytables import manage_pytables
from .prediction import read_meta,read_grid_info

logger = logging.getLogger('yatsm')

## main function that calls the other functions and writes the results
def get_change_mags(hdf_file, out_dir, ndv=-9999):
    """ Output a raster with the predictions from model fit for a given date

    Args:
        hdf_file (str): Location of input hdf file
        out_dir (str): Location where out tiffs will be written to
        ndv (int, optional): NoDataValue
        
    """

    ## open up the hdf file for reading
    # import the functions
    pt = manage_pytables()

    # open the HDF file
    pt.open_hdf_file(hdf_file)

    ## location of the grid info metadata
    grid_info = read_grid_info(pt.h5_file.root.grid)

    ## load the chunk metadata - x,y coordinates for each pixel
    meta = pt.h5_file.root.metadata
    nchunks = meta.nrows           
    meta_info = read_meta(meta)          # y_coords 2000 ??? , x_coords 0-6000
    chunk_nrows = len(meta_info['y_coords'][0,])      # chunck_nrows = 2
    fill = -32767

    ## create output raster arrays 
    ## could record for multiple disturbances
    n_breaks = 3
    n_mets = 8  
    n_tc = 3
    n_tc_mets = 6

    logger.debug('Allocating memory')
    ## dist mets will have n_mets bands - int16
    dist_mets = np.ones((grid_info['nrows'], grid_info['ncols'], n_mets),
                     dtype=np.int16) * int(fill)
    ## date_map has one band but int32
    date_map = np.ones((grid_info['nrows'], grid_info['ncols']),
                     dtype=np.int32) * int(fill)

    ## tc dist mets will have n_tc_mets bands - int16
    tc_dist_mets = np.ones((grid_info['nrows'], grid_info['ncols'], n_tc_mets),
                     dtype=np.int16) * int(fill)
    ## tc date_map has 3 bands but int32
    tc_date_map = np.ones((grid_info['nrows'], grid_info['ncols'], n_tc),
                     dtype=np.int32) * int(fill)

    logger.debug('Processing results')
    start = timer()
    ## loop through the chunks, meta_info['ids'] is the chunk id
    for n in meta_info['ids']:
        array_name = "/C{}/Ref".format(n)
        ## load the current chunk
        h5_node = pt.h5_file.get_node(array_name).read()
        
        start_loc = n*chunk_nrows
        end_loc = (n*chunk_nrows) + chunk_nrows
        
        ## process the current chunk
        dates,out_mets,tc_dates,tc_mets = calc_magnitude(h5_node,meta_info['years'],mid_date=grid_info['doy'],ndv=ndv)
        ## reshape output to 3 dimensions
        date_map[start_loc:end_loc,:] = dates.reshape(chunk_nrows,grid_info['ncols'])
        ## first is num, num_brks, dnbr, devi, pre_nbr, pre_evi, pre_rmse
        dist_mets[start_loc:end_loc,:,:] = out_mets.reshape(chunk_nrows,grid_info['ncols'],n_mets)

         ## reshape output to 3 dimensions
        tc_date_map[start_loc:end_loc,:,:] = tc_dates.reshape(chunk_nrows,grid_info['ncols'],n_tc)
        ## first is num, num_brks, dnbr, devi, pre_nbr, pre_evi, pre_rmse
        tc_dist_mets[start_loc:end_loc,:,:] = tc_mets.reshape(chunk_nrows,grid_info['ncols'],n_tc_mets)

    end = timer()
    ## print the time of the loop
    print(end - start)

    ## write the outputs to file
    cur_name = "{0}/{1}.dates.tif".format(out_dir,grid_info['tile'])
    logger.debug('Writing output file {}'.format(cur_name))
    write_output(date_map, cur_name, grid_info, gdal_frmt='GTiff',ndv=fill)

    cur_name = "{0}/{1}.dist_mets.tif".format(out_dir,grid_info['tile'])
    logger.debug('Writing output file {}'.format(cur_name))
    write_output(dist_mets, cur_name, grid_info, gdal_frmt='GTiff',ndv=fill)

    ## write the outputs to file
    cur_name = "{0}/{1}.tc_dates.tif".format(out_dir,grid_info['tile'])
    logger.debug('Writing output file {}'.format(cur_name))
    write_output(tc_date_map, cur_name, grid_info, gdal_frmt='GTiff',ndv=fill)

    cur_name = "{0}/{1}.tc_dist_mets.tif".format(out_dir,grid_info['tile'])
    logger.debug('Writing output file {}'.format(cur_name))
    write_output(tc_dist_mets, cur_name, grid_info, gdal_frmt='GTiff',ndv=fill)

    pt.close_hdf()
    ## fxn doesnt return anything

## this is the function that processes each pixel in the current row chunk
## returns the disturbance metrics
def calc_magnitude(in_array,years,mid_date=212,ndv=-9999,fill=-32767):
    """ Calculates change magnitudes

    Args:
      in_array (iterable): input array with dimensions of 12000 pix x 8 bands x 31 years

    Returns:
      np.ndarray: indices containing magnitude change information from the
        tested indices

    Raises:
        KeyError: Raise KeyError when a required result output is missing
            from the saved record structure
    """

    ## order of in_array is 7 bands, date of break (if not fill), 7 rmse values
    ## read in date of break
    dates = in_array[:,7,:]
    ## use the swir1 rmse 
    ## rmse starts at index 8 + 5th band
    rmse = in_array[:,12,:]
    npix = dates.shape[0]
    nyears = dates.shape[1]

    n_mets = 8

    n_tc = 6

    ## dist mets will have n_mets bands - int16
    tc_dist_mets = np.ones((npix,n_tc),dtype=np.int16) * int(fill)
    tc_date_map = np.ones((npix,3),dtype=np.int32) * int(fill)

    ## setup output arrays
    dist_mets = np.ones((npix,n_mets),dtype=np.int16) * int(fill)
    date_map = np.ones(npix,dtype=np.int32) * int(fill)

    ## first array are the x array tuples that have changed 
    ## if look at the second tuple can also see the years that have changed
    ## this is an index of all the breaks in time - multiple breaks are possible per pixel
    all_breaks = np.where(dates != ndv)
    un_years = np.unique(all_breaks[1])
    un_x = np.unique(all_breaks[0])
    ## make sure no breaks are in the first or last year
    un_years = un_years[(un_years>0) & (un_years<(nyears-1))]

    ### now we simply calculate the indices for each date - before and after
    ## loop through the pixels not the years
    ## could parallellize this function later
    for x in un_x:    
        ## this gives us all the locations where the dates are not fill
        cur_x = dates[x,]
        cur_y = np.where(cur_x>0)[0]
        ## make a separate array just with the pixels with breaks
        breaks = cur_x[cur_y]
   
        ## calculate the before, after years for each break in the series
        b_y,a_y,out_dates = get_break_years(breaks,mid_date,cur_y,years)
       
        ## if the function returns null go onto the next pixel
        num_breaks = len(b_y)
        if num_breaks==0:
            continue

        ## only need the first 6 bands for all years
        b_ref = in_array[x,0:6,b_y]
        a_ref = in_array[x,0:6,a_y]

        ## the rmse for the pre-dist segment in swir1
        pre_rmse = rmse[x,b_y]

        ## choose a year before or after, respectively, if there is a data gap
        for b in np.arange(0,num_breaks):
            ## counts the missing data in the current year's reflectance values
            ## if there are missing values uses the year before as the current year
            cur_count = count_na(b_ref[b,:],ndv)
            con = (cur_count>0) & (b_y[b]>0)
            if con:
                b_ref[b,:] = in_array[x,0:6,(b_y[b]-1)]
                pre_rmse[b] = rmse[x,(b_y[b]-1)]

            ## for the after disturbance year loop
            ## through to the end of the time series 
            ## to find the right date without missing data
            for t in np.arange(a_y[b],nyears):
                cur_ref = in_array[x,0:6,t]
                cur_count = count_na(cur_ref,ndv)
                if (cur_count == 0):
                    break 
       
            a_ref[b,:] = cur_ref

        ## call the function to calculate the dist mets for that pixel
        dnbr_thres = 1000
        dist_date,pix_mets = get_dist_nbr(b_ref,a_ref,out_dates,dnbr_thres,fill,n_mets,pre_rmse)
        ## save pixel outputs to the chunk output arrays
        ## first is num, dnbr, pre_nbr, devi, pre_evi, num_brks, pre_rmse
        for n in np.arange(0,7):
            dist_mets[x,n] = pix_mets[n]
        
        dist_mets[x,7] = num_breaks
        date_map[x] = dist_date

        tc_thres = 1000
        tc_dates,tc_mets = get_dist_bgw(b_ref,a_ref,out_dates,tc_thres,fill,n_tc)
        for n in np.arange(0,n_tc):
            tc_dist_mets[x,n] = tc_mets[n]
 
        for n in np.arange(0,3):
            tc_date_map[x,n] = tc_dates[n]

    return date_map,dist_mets,tc_date_map,tc_dist_mets


## function to filter out the breaks for one that may be a disturbance
def get_dist_nbr(b_ref,a_ref,out_dates,thres,fill,n_mets,pre_rmse):
    ## initialize outputs
    out_mets = np.ones(n_mets,dtype=np.int16) * fill
    dist_date = fill

    ## calculate nbr for before and after
    b_nbr = calc_nbr(b_ref[:,(3,5)])
    a_nbr = calc_nbr(a_ref[:,(3,5)])
    ## calculate evi2 before and after
    b_evi2 = calc_evi2(b_ref[:,(2,3)])
    a_evi2 = calc_evi2(a_ref[:,(2,3)])
    b_ndwi = calc_ndwi(b_ref[:,(1,3)])
        
    ## very important check - this filters out pixels we dont want to map disturbance for
    ## check that neither are fill - and that they dont equal exactly zero
    ## also check that the evi2 value before the break is larger than 0.1 - screen out non-vegetated changes
    ## check that the NDWI is less than 0.2 - non-water changes
    ## b_nbr should be larger than 0.2 but less than 0.9
    good_nbr = np.not_equal(a_nbr,fill) & np.not_equal(b_nbr,fill) & np.not_equal(a_nbr,0) \
                    & np.greater(b_nbr,2000) & np.greater(b_evi2,1000) & np.less(b_ndwi,2000) & np.less(b_nbr,9000)

    a_nbr = a_nbr[good_nbr]
    b_nbr = b_nbr[good_nbr]
    out_dates = out_dates[good_nbr]
    cur_rmse = pre_rmse[good_nbr]
    pre_swir1 = b_ref[good_nbr,4]    
    a_evi2 = a_evi2[good_nbr]
    b_evi2 = b_evi2[good_nbr]

    ## skip if all observations have fill - maybe fill with something different
    if len(b_nbr)==0:
        return(dist_date,out_mets)

    ## calculate deltas
    d_nbr = a_nbr - b_nbr
    d_evi2 = a_evi2 - b_evi2

    ## test that the disturbance exceeds a d_nbr thres
    dist_ind = d_nbr > thres
        
    ## could return different flags besides fill
    if len(d_nbr[dist_ind])==0:
        return(dist_date,out_mets)

    ## goes num dist, dnbr, devi, pnbr, pevi, rmse b5, num_brks
    ## dist dates is saved separately because it is int32    
    ## here is where we could output more than one disturbance
    dnbr_out = d_nbr[dist_ind]
    cur_max = np.where(dnbr_out == max(dnbr_out))[0]
    if len(cur_max)>1:
        cur_max = cur_max[0]
    
    out_mets[0] = len(d_nbr[dist_ind])
    
    ## only want one output per pixel 
    out_mets[1]=dnbr_out[cur_max]
    temp = b_nbr[dist_ind]
    out_mets[2]=temp[cur_max]
    temp = d_evi2[dist_ind]
    out_mets[3]=temp[cur_max]
    temp = b_evi2[dist_ind]
    out_mets[4]=temp[cur_max]
    temp = pre_swir1[dist_ind]
    out_mets[5]=temp[cur_max]   
    temp = cur_rmse[dist_ind]
    out_mets[6]=temp[cur_max]

    temp = out_dates[dist_ind]
    dist_date = temp[cur_max]

    return(dist_date,out_mets)


## calculates nbr as an integer between -10000 and positive 10000
## could go larger if the ref[3]+ref[5] are very small
def calc_nbr(ref,ndv=-9999,fill = -32767):
    
    nrows = ref.shape[0]
    out = np.ones(nrows,dtype=np.int16) * fill

    ## loop through the breaks
    for i in np.arange(0,nrows):
        ## check to make sure observation is good
        con = ((ref[i,0] + ref[i,1]) != 0) & (ref[i,0]!=ndv) & (ref[i,1]!=ndv)
        if con:
            out[i] = 10000*((ref[i,0]-ref[i,1])/(ref[i,0]+ref[i,1]))
        
    return(out)

## calculates evi2 as an integer between -10000 and positive 10000
def calc_evi2(ref,ndv=-9999,fill = -32767):
    
    nrows = ref.shape[0]
    out = np.ones(nrows,dtype=np.int16) * fill

    ## loop through the breaks
    for i in np.arange(0,nrows):
        ## check to make sure observation is good
        con = ((ref[i,1] + (2.4*ref[i,0]) + 10000) != 0) & (ref[i,0]!=ndv) & (ref[i,1]!=ndv)
        if con:
            out[i] = 10000*2.5*((ref[i,1]-ref[i,0])/(ref[i,1] + (2.4*ref[i,0]) + 10000))
        
    return(out)

## calculates ndwi as an integer between -10000 and positive 10000
def calc_ndwi(ref,ndv=-9999,fill = -32767):
    
    nrows = ref.shape[0]
    out = np.ones(nrows,dtype=np.int16) * fill

    #good_vals = np.not_equal(ref[,0],ndv) & np.not_equal(ref[,1],ndv) & np.not_equal((ref[,0]+ref[,1]),0)
    #out[good_vals] = 10000*(ref[good_vals,0]-ref[good_vals,1])/(ref[good_vals,0] + ref[good_vals,1])
    ## loop through the breaks
    for i in np.arange(0,nrows):
        ## check to make sure observation is good
        con = ((ref[i,0] + ref[i,1]) != 0) & (ref[i,0]!=ndv) & (ref[i,1]!=ndv)
        if con:
            out[i] = 10000*(ref[i,0]-ref[i,1])/(ref[i,0] + ref[i,1])
        
    return(out)


## to calculate Tasselled Cap-BGW
def calc_bgw(ref,ndv=-9999,fill = -32767): 

    nrows = ref.shape[0]
    out = np.ones((nrows,3),dtype=np.int16) * fill

    ### we use the landsat 5 coefficients    
    refB = (0.2043, 0.4158, 0.5524, 0.5741, 0.3124, 0.2303) # for Landsat 4/5
    #refB = c(0.3561, 0.3972, 0.3904, 0.6966, 0.2286, 0.1596) # for Landsat 7

    refG = (-0.1603, -0.2819, -0.4934, 0.7940, -0.0002, -0.1446) # for Landsat 4/5
    #refG = c(-0.3344, -0.3544, -0.4556, 0.6966, -0.0242,-0.2630) # for Landsat 7

    refW = (0.0315, 0.2021, 0.3102, 0.1594, -0.6806, -0.6109) # for Landsat 4/5
    #refW = c(0.2626, 0.2141, 0.0926, 0.0656, -0.7629, -0.5388) # for Landsat 7

    ## loop through the breaks
    for i in np.arange(0,nrows):
        ## check to make sure observation is good
        con = len(ref[i,(ref[i,]==ndv)])==0
        if con:
            b = 0
            g = 0
            w = 0
            for r in np.arange(0,6):
                b = b + (ref[i,r] * refB[r])
                g = g + (ref[i,r] * refG[r])
                w = w + (ref[i,r] * refW[r])

            out[i,0] = b.astype(np.int16)
            out[i,1] = g.astype(np.int16)
            out[i,2] = w.astype(np.int16)
        
    return(out)

## function to find the years before and after the break with good data
def get_break_years(breaks,mid_date,cur_y,years):
    
    num_breaks = len(breaks)
    cur_years = years[cur_y]
    num_years = len(years)
        
    out_dates = np.ones(num_breaks,dtype=np.int32) * 0
    for i in np.arange(0,num_breaks):
        out_dates[i] = int("{0}{1}".format(cur_years[i],breaks[i]))

    ## make sure we dont exceed the year arrays
    late_ind = breaks >= mid_date
    early_ind = breaks < mid_date
             
    b_y = np.ones(num_breaks,dtype=np.int16) * -1
    a_y = np.ones(num_breaks,dtype=np.int16) * -1

    ## might want to consider more years - to get less miss data
    b_y[late_ind] = cur_y[late_ind]
    a_y[late_ind] = cur_y[late_ind]+1

    b_y[early_ind] = cur_y[early_ind]-1
    a_y[early_ind] = cur_y[early_ind]

    ## remove any bad year values
    good_ind = np.greater(b_y,0)
    b_y = b_y[good_ind]
    a_y = a_y[good_ind]
    out_dates = out_dates[good_ind]

    good_ind = np.less(a_y,num_years)
    b_y = b_y[good_ind]
    a_y = a_y[good_ind]
    out_dates = out_dates[good_ind]

    return(b_y,a_y,out_dates)



## older function - dsm wrote to get change in the Tasselled Cap BGW metrics 
## not currently used
def get_dist_bgw(b_ref,a_ref,out_dates,thres,fill,n_mets):

    ## initialize outputs
    out_mets = np.ones(n_mets,dtype=np.int16) * fill
    dist_dates = np.ones(3,dtype=np.int32) * fill

    ## calculate nbr for before and after
    all_b_bgw = calc_bgw(b_ref[:,0:7])
    all_a_bgw = calc_bgw(a_ref[:,0:7])

    delta_list = []
    for i in np.arange(0,3):
        ## check that neither are fill
        a_bgw = all_a_bgw.take(i,axis=1)
        b_bgw = all_b_bgw.take(i,axis=1)

        good_bgw = np.not_equal(a_bgw,fill) & np.not_equal(b_bgw,fill)
        a_bgw = a_bgw[good_bgw]
        b_bgw = b_bgw[good_bgw]
        out_dates_temp = out_dates[good_bgw]

        ## skip if all observations have fill - maybe fill with something different
        if len(b_bgw)==0:
            continue
    
        ## calculate deltas
        delta = a_bgw - b_bgw
        delta_list.append(delta)
        pdb.set_trace()
        ## test that the disturbance exceeds an absolute threshold
        dist_ind = abs(delta) > thres
        
        ## could return different flags besides fill
        if len(delta[dist_ind])==0:
            continue

        dates_temp = out_dates_temp[dist_ind]
        delta_temp = delta[dist_ind]
        pre_temp = b_bgw[dist_ind]

        ## if you want to return multiple disturbances comment this part out 
        #  and make the outputs the above
        ## select only the maximum disturbance value
        out_ind = np.where(delta_temp == max(delta_temp))[0]
        if len(out_ind)>1:
            out_ind = out_ind[0]
        
        out_mets[(i*2)] = delta_temp[out_ind]
        out_mets[(i*2)+1] = pre_temp[out_ind]
        ### needs to be fixed to return 3 values
        dist_dates[i] = dates_temp[out_ind]
    
    return(dist_dates,out_mets)


def count_na(arr_in,fill):
    return(len(arr_in[arr_in==fill]))



## main function that calls the other functions and writes the results
def get_change_mags_list(hdf_file, out_dir, ndv=-9999):
    """ Output a raster with the predictions from model fit for a given date

    Args:
        hdf_file (str): Location of input hdf file
        out_dir (str): Location where out tiffs will be written to
        ndv (int, optional): NoDataValue
        
    """

    ## open up the hdf file for reading
    # import the functions
    pt = manage_pytables()

    # open the HDF file
    pt.open_hdf_file(hdf_file)

    ## location of the grid info metadata
    grid_info = read_grid_info(pt.h5_file.root.grid)

    ## load the chunk metadata - x,y coordinates for each pixel
    meta = pt.h5_file.root.metadata
    nchunks = meta.nrows
    meta_info = read_meta(meta)
    chunk_nrows = len(meta_info['y_coords'][0,])
    fill = -32767

    ## create output raster arrays 
    ## could record for multiple disturbances
    n_breaks = 3
    n_mets = 8  
    n_tc = 3
    n_tc_mets = 6

    logger.debug('Allocating memory')
    ## dist mets will have n_mets bands - int16
    dist_mets = np.ones((grid_info['nrows'], grid_info['ncols'], n_mets),
                     dtype=np.int16) * int(fill)
    ## date_map has one band but int32
    date_map = np.ones((grid_info['nrows'], grid_info['ncols']),
                     dtype=np.int32) * int(fill)

    ## tc dist mets will have n_tc_mets bands - int16
    tc_dist_mets = np.ones((grid_info['nrows'], grid_info['ncols'], n_tc_mets),
                     dtype=np.int16) * int(fill)
    ## tc date_map has 3 bands but int32
    tc_date_map = np.ones((grid_info['nrows'], grid_info['ncols'], n_tc),
                     dtype=np.int32) * int(fill)

    logger.debug('Processing results')
    start = timer()
    out_list = []
    ## loop through the chunk ids
    for n in meta_info['ids']:
        array_name = "/C{}/Ref".format(n)
        ## load the current chunk
        h5_node = pt.h5_file.get_node(array_name).read()
        
        #start_loc = n*chunk_nrows
        #end_loc = (n*chunk_nrows) + chunk_nrows
        temp_list = []
        # n is the chunk id
        temp_list = get_TC_break_list(n, h5_node,meta_info['years'],mid_date=grid_info['doy'], ndv=ndv)
        
        out_list.append(temp_list)
       
    end = timer()
    ## print the time of the loop
    print(end - start)

    cur_name = "{0}/{1}.all_breaks.npy.npz".format(out_dir,grid_info['tile'])
    np.savez_compressed(cur_name, out_list)
    pt.close_hdf()
    ## fxn doesnt return anything



## this is the function that processes each pixel in the current row chunk
## returns the disturbance metrics
def get_TC_break_list(chunk_id, in_array,years, mid_date=212, ndv=-9999,fill=-32767):
    """ Calculates change magnitudes

    Args:
      in_array (iterable): input array with dimensions of 12000 pix x 8 bands x 31 years

    Returns:
      np.ndarray: indices containing magnitude change information from the
        tested indices

    Raises:
        KeyError: Raise KeyError when a required result output is missing
            from the saved record structure
    """

    ## order of in_array is 7 bands, date of break (if not fill), 7 rmse values
    ## read in date of break
    dates = in_array[:,7,:]

    npix = dates.shape[0]
    nyears = dates.shape[1]

    n_mets = 10

    ## first array are the x array tuples that have changed 
    ## if look at the second tuple can also see the years that have changed
    ## this is an index of all the breaks in time - multiple breaks are possible per pixel
    all_breaks = np.where(dates != ndv)
    un_years = np.unique(all_breaks[1])
    un_x = np.unique(all_breaks[0])
    ## make sure no breaks are in the first or last year
    un_years = un_years[(un_years>0) & (un_years<(nyears-1))]

    out_list = []
    ### now we simply calculate the indices for each date - before and after
    ## loop through the pixels not the years
    ## could parallellize this function later
    for x in un_x:    
        ## this gives us all the locations where the dates are not fill
        cur_x = dates[x,]
        cur_y = np.where(cur_x>0)[0]
        ## make a separate array just with the pixels with breaks
        breaks = cur_x[cur_y]
   
        ## calculate the before, after years for each break in the series
        b_y,a_y,out_dates,out_years = get_break_dates(breaks,mid_date,cur_y,years)
       
        ## if the function returns null go onto the next pixel
        num_breaks = len(b_y)
        if num_breaks==0:
            continue

        ## only need the first 6 bands for all years
        b_ref = in_array[x,0:6,b_y]
        a_ref = in_array[x,0:6,a_y]

        ## choose a year before or after, respectively, if there is a data gap
        for b in np.arange(0,num_breaks):
            ## counts the missing data in the current year's reflectance values
            ## if there are missing values uses the year before as the current year
            cur_count = count_na(b_ref[b,:],ndv)
            con = (cur_count>0) & (b_y[b]>0)
            if con:
                b_ref[b,:] = in_array[x,0:6,(b_y[b]-1)]

            ## for the after disturbance year loop
            ## through to the end of the time series 
            ## to find the right date without missing data
            for t in np.arange(a_y[b],nyears):
                cur_ref = in_array[x,0:6,t]
                cur_count = count_na(cur_ref,ndv)
                if (cur_count == 0):
                    break 
       
            a_ref[b,:] = cur_ref

        ## calculate nbr for before and after
        b_bgw = calc_bgw(b_ref[:,0:7])
        a_bgw = calc_bgw(a_ref[:,0:7])
        d_bgw = a_bgw - b_bgw
        
        ## calculate nbr for before and after
        b_nbr = calc_nbr(b_ref[:,(3,5)])
        a_nbr = calc_nbr(a_ref[:,(3,5)])
        d_nbr = a_nbr - b_nbr

        total_out = (num_breaks*n_mets)+2
        out_pix = np.ones(total_out,dtype=np.int16) * int(fill)
        out_pix[0] = chunk_id
        out_pix[1] = x
        ## choose a year before or after, respectively, if there is a data gap
        for b in np.arange(0,num_breaks):
            cur_loc = (n_mets*b)+2
            out_pix[cur_loc:(cur_loc+n_mets)] = (out_years[b],out_dates[b],b_nbr[b],d_nbr[b], \
                            b_bgw[b,0],d_bgw[b,0],b_bgw[b,1],d_bgw[b,1],b_bgw[b,2],d_bgw[b,2])

        out_list.append(out_pix)

        
        

    return out_list


## function to find the years before and after the break with good data
## returns dates and year separately
def get_break_dates(breaks,mid_date,cur_y,years):
    
    num_breaks = len(breaks)
    cur_years = years[cur_y]
    num_years = len(years)
        
    out_dates = np.ones(num_breaks,dtype=np.int16) * 0
    out_years = np.ones(num_breaks,dtype=np.int16) * 0
    for i in np.arange(0,num_breaks):
        out_dates[i] = breaks[i]
        out_years[i] = cur_years[i]

    ## make sure we dont exceed the year arrays
    late_ind = breaks >= mid_date
    early_ind = breaks < mid_date
             
    b_y = np.ones(num_breaks,dtype=np.int16) * -1
    a_y = np.ones(num_breaks,dtype=np.int16) * -1

    ## might want to consider more years - to get less miss data
    b_y[late_ind] = cur_y[late_ind]
    a_y[late_ind] = cur_y[late_ind]+1

    b_y[early_ind] = cur_y[early_ind]-1
    a_y[early_ind] = cur_y[early_ind]

    ## remove any bad year values
    good_ind = np.greater(b_y,0)
    b_y = b_y[good_ind]
    a_y = a_y[good_ind]
    out_dates = out_dates[good_ind]
    out_years = out_years[good_ind]

    good_ind = np.less(a_y,num_years)
    b_y = b_y[good_ind]
    a_y = a_y[good_ind]
    out_dates = out_dates[good_ind]
    out_years = out_years[good_ind]

    return(b_y,a_y,out_dates,out_years)


