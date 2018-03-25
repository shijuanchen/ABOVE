# This script masks the non forest values of delta and pre tc metrics
# input is the image file path of the land cover map of 1985 and the folder path of image of the delta and pre tc metrics
# output is the image of delta and pre tc metrics

from osgeo import gdal, gdal_array, osr, ogr
import numpy as np

lc_map_path = r'/projectnb/landsat/users/shijuan/above/bh12v11/LCmap/Bh12v11_1985_tc_20180219_k25_mn_sub_pam_rf_remap.tif'
tc_folder_path = r'/projectnb/landsat/projects/ABOVE/CCDC/Bh12v11/out_tc_pre'
output_path = r'/projectnb/ladnsat/projects/ABOVE/CCDC/Bh12v11/'

def mask_non_forest(lc_map_path, tc_folder_path, output_path):
	
