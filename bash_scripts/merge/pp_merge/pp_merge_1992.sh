#!/bin/bash
#$ -N merge_year
#$ -l h_rt=24:00:00
#$ -l mem_total=98G

module purge
source /projectnb/landsat/users/shijuan/miniconda3/bin/activate yatsm_v0.6_par
gdal_merge.py -o /projectnb/landsat/users/shijuan/above/above_merge_pp/above_merge_pp_1992.tif -a_nodata 0 -ot Byte -co TILED=YES -co BLOCKXSIZE=256 -co BLOCKYSIZE=256 -co COMPRESS=DEFLATE /projectnb/landsat/projects/ABOVE/CCDC/Bh01v03/new_map/out_pp/Bh01v03_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh01v04/new_map/out_pp/Bh01v04_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh01v05/new_map/out_pp/Bh01v05_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh02v02/new_map/out_pp/Bh02v02_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh02v03/new_map/out_pp/Bh02v03_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh02v04/new_map/out_pp/Bh02v04_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh02v05/new_map/out_pp/Bh02v05_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh02v06/new_map/out_pp/Bh02v06_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh03v01/new_map/out_pp/Bh03v01_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh03v02/new_map/out_pp/Bh03v02_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh03v03/new_map/out_pp/Bh03v03_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh03v04/new_map/out_pp/Bh03v04_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh03v05/new_map/out_pp/Bh03v05_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh03v06/new_map/out_pp/Bh03v06_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh04v01/new_map/out_pp/Bh04v01_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh04v02/new_map/out_pp/Bh04v02_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh04v03/new_map/out_pp/Bh04v03_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh04v04/new_map/out_pp/Bh04v04_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh04v05/new_map/out_pp/Bh04v05_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh05v00/new_map/out_pp/Bh05v00_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh05v01/new_map/out_pp/Bh05v01_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh05v02/new_map/out_pp/Bh05v02_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh05v03/new_map/out_pp/Bh05v03_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh05v04/new_map/out_pp/Bh05v04_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh05v05/new_map/out_pp/Bh05v05_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh05v06/new_map/out_pp/Bh05v06_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh06v00/new_map/out_pp/Bh06v00_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh06v01/new_map/out_pp/Bh06v01_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh06v02/new_map/out_pp/Bh06v02_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh06v03/new_map/out_pp/Bh06v03_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh06v04/new_map/out_pp/Bh06v04_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh06v05/new_map/out_pp/Bh06v05_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh06v06/new_map/out_pp/Bh06v06_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh06v07/new_map/out_pp/Bh06v07_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh06v08/new_map/out_pp/Bh06v08_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh06v09/new_map/out_pp/Bh06v09_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh07v00/new_map/out_pp/Bh07v00_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh07v01/new_map/out_pp/Bh07v01_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh07v02/new_map/out_pp/Bh07v02_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh07v03/new_map/out_pp/Bh07v03_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh07v04/new_map/out_pp/Bh07v04_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh07v05/new_map/out_pp/Bh07v05_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh07v06/new_map/out_pp/Bh07v06_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh07v07/new_map/out_pp/Bh07v07_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh07v08/new_map/out_pp/Bh07v08_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh07v09/new_map/out_pp/Bh07v09_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh07v10/new_map/out_pp/Bh07v10_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh08v01/new_map/out_pp/Bh08v01_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh08v02/new_map/out_pp/Bh08v02_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh08v03/new_map/out_pp/Bh08v03_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh08v04/new_map/out_pp/Bh08v04_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh08v05/new_map/out_pp/Bh08v05_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh08v06/new_map/out_pp/Bh08v06_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh08v07/new_map/out_pp/Bh08v07_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh08v08/new_map/out_pp/Bh08v08_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh08v09/new_map/out_pp/Bh08v09_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh08v10/new_map/out_pp/Bh08v10_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh08v11/new_map/out_pp/Bh08v11_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh08v12/new_map/out_pp/Bh08v12_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh08v13/new_map/out_pp/Bh08v13_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh08v14/new_map/out_pp/Bh08v14_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh09v03/new_map/out_pp/Bh09v03_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh09v04/new_map/out_pp/Bh09v04_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh09v05/new_map/out_pp/Bh09v05_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh09v06/new_map/out_pp/Bh09v06_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh09v07/new_map/out_pp/Bh09v07_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh09v08/new_map/out_pp/Bh09v08_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh09v09/new_map/out_pp/Bh09v09_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh09v10/new_map/out_pp/Bh09v10_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh09v11/new_map/out_pp/Bh09v11_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh09v12/new_map/out_pp/Bh09v12_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh09v13/new_map/out_pp/Bh09v13_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh09v14/new_map/out_pp/Bh09v14_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh09v15/new_map/out_pp/Bh09v15_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh10v04/new_map/out_pp/Bh10v04_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh10v05/new_map/out_pp/Bh10v05_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh10v06/new_map/out_pp/Bh10v06_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh10v07/new_map/out_pp/Bh10v07_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh10v08/new_map/out_pp/Bh10v08_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh10v09/new_map/out_pp/Bh10v09_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh10v10/new_map/out_pp/Bh10v10_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh10v11/new_map/out_pp/Bh10v11_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh10v12/new_map/out_pp/Bh10v12_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh10v13/new_map/out_pp/Bh10v13_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh10v14/new_map/out_pp/Bh10v14_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh10v15/new_map/out_pp/Bh10v15_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh10v16/new_map/out_pp/Bh10v16_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh10v17/new_map/out_pp/Bh10v17_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh11v05/new_map/out_pp/Bh11v05_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh11v06/new_map/out_pp/Bh11v06_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh11v07/new_map/out_pp/Bh11v07_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh11v08/new_map/out_pp/Bh11v08_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh11v09/new_map/out_pp/Bh11v09_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh11v10/new_map/out_pp/Bh11v10_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh11v11/new_map/out_pp/Bh11v11_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh11v12/new_map/out_pp/Bh11v12_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh11v13/new_map/out_pp/Bh11v13_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh11v14/new_map/out_pp/Bh11v14_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh11v15/new_map/out_pp/Bh11v15_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh11v16/new_map/out_pp/Bh11v16_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh12v05/new_map/out_pp/Bh12v05_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh12v06/new_map/out_pp/Bh12v06_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh12v07/new_map/out_pp/Bh12v07_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh12v08/new_map/out_pp/Bh12v08_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh12v09/new_map/out_pp/Bh12v09_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh12v10/new_map/out_pp/Bh12v10_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh12v11/new_map/out_pp/Bh12v11_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh12v12/new_map/out_pp/Bh12v12_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh12v13/new_map/out_pp/Bh12v13_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh12v14/new_map/out_pp/Bh12v14_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh12v15/new_map/out_pp/Bh12v15_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh12v16/new_map/out_pp/Bh12v16_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh13v04/new_map/out_pp/Bh13v04_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh13v06/new_map/out_pp/Bh13v06_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh13v07/new_map/out_pp/Bh13v07_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh13v08/new_map/out_pp/Bh13v08_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh13v09/new_map/out_pp/Bh13v09_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh13v10/new_map/out_pp/Bh13v10_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh13v11/new_map/out_pp/Bh13v11_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh13v12/new_map/out_pp/Bh13v12_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh13v13/new_map/out_pp/Bh13v13_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh13v14/new_map/out_pp/Bh13v14_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh13v15/new_map/out_pp/Bh13v15_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh13v16/new_map/out_pp/Bh13v16_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh14v03/new_map/out_pp/Bh14v03_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh14v05/new_map/out_pp/Bh14v05_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh14v07/new_map/out_pp/Bh14v07_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh14v08/new_map/out_pp/Bh14v08_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh14v09/new_map/out_pp/Bh14v09_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh14v10/new_map/out_pp/Bh14v10_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh14v11/new_map/out_pp/Bh14v11_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh14v12/new_map/out_pp/Bh14v12_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh14v13/new_map/out_pp/Bh14v13_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh14v14/new_map/out_pp/Bh14v14_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh14v15/new_map/out_pp/Bh14v15_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh15v05/new_map/out_pp/Bh15v05_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh15v06/new_map/out_pp/Bh15v06_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh15v07/new_map/out_pp/Bh15v07_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh15v08/new_map/out_pp/Bh15v08_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh15v09/new_map/out_pp/Bh15v09_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh15v10/new_map/out_pp/Bh15v10_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh15v11/new_map/out_pp/Bh15v11_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh15v12/new_map/out_pp/Bh15v12_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh15v13/new_map/out_pp/Bh15v13_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh15v15/new_map/out_pp/Bh15v15_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh16v05/new_map/out_pp/Bh16v05_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh16v06/new_map/out_pp/Bh16v06_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh16v07/new_map/out_pp/Bh16v07_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh16v08/new_map/out_pp/Bh16v08_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh16v09/new_map/out_pp/Bh16v09_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh16v10/new_map/out_pp/Bh16v10_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh16v11/new_map/out_pp/Bh16v11_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh16v12/new_map/out_pp/Bh16v12_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh16v13/new_map/out_pp/Bh16v13_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh16v14/new_map/out_pp/Bh16v14_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh17v06/new_map/out_pp/Bh17v06_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh17v07/new_map/out_pp/Bh17v07_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh17v08/new_map/out_pp/Bh17v08_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh17v09/new_map/out_pp/Bh17v09_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh17v10/new_map/out_pp/Bh17v10_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh17v11/new_map/out_pp/Bh17v11_FF_FN_NF_NN_1992_cl_pp.tif /projectnb/landsat/projects/ABOVE/CCDC/Bh17v12/new_map/out_pp/Bh17v12_FF_FN_NF_NN_1992_cl_pp.tif 