#!/bin/bash -l
#$ -V
#$ -l h_rt=120:00:00
#$ -N YATSM_map
#$ -j y
#$ -l mem_total=98G
#$ -pe omp 16

## this is a script to read the YATSM model and extract tables of peak-summer reflectances and break dates
if [ -z "$1" ]
then
	echo "Input error!"
	exit 1
else
	tile_name=$1
fi

module purge
source /projectnb/landsat/users/shijuan/miniconda3/bin/activate yatsm_v0.6_par
root="/projectnb/landsat/projects/ABOVE/CCDC/$tile_name"
output="$root/$tile_name.h5"
echo $root
echo $output
yatsm summ_table --root $root "change" $output

source deactivate

echo "Finished submitting tile $tile_name"
