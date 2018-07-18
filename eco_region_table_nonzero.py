# This script product a ecoregion table for tiles

from osgeo import gdal, gdal_array, osr, ogr
import numpy as np
from scipy import stats
import click

def ecoregion_table(eco_folder_path, output_file_path, tile_name):
    eco_file = eco_folder_path+'/biome.' + tile_name + '.tif'
    print(eco_file)
    ds = gdal.Open(eco_file)
    eco_raster = ds.ReadAsArray()
    eco_array = np.array(eco_raster)
    eco_array = np.reshape(eco_array, (1, 36000000))
    eco_array_nonzero = eco_array[np.nonzero(eco_array)]
    if eco_array_nonzero.size > 0:
        eco = stats.mode(eco_array_nonzero, axis=None)
        eco = str(eco[0][0])
    else:
        eco = '0'
    print('eco=')
    print(eco)
    f=open(output_file_path, "w")
    f.write(tile_name)
    f.write(' ')
    f.write(eco)
    f.write('\n')
    f.close()
    
@click.command()
@click.option('--tile_name', default='Bh04v06', help='Name of the tile, for example: Bh04v06')    
             
def main(tile_name):
    eco_folder_path = r'/projectnb/modislc/projects/above/tiles/EPA_L1_ECO'.format(tile_name)
    output_file_path = r'/projectnb/landsat/users/shijuan/above/eco_region_nonzero/{0}_eco.txt'.format(tile_name)
    ecoregion_table(eco_folder_path, output_file_path, tile_name)
main()
