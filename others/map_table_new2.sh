#!/bin/bash -l
#$ -V
#$ -l h_rt=24:00:00
#$ -N YATSM_map
#$ -j y
#$ -l mem_total=98G
#$ -pe omp 16

## this is a script to read the YATSM model and extract tables of peak-summer reflectances and break dates
if [ -z "$1" ]
then
	echo Usage \"./make_summ_table.sh scene_name 
	exit 1
else
	name=$1
fi

#Root directory where the images are stored
cur_dir=$(readlink -f $(pwd))
root="$cur_dir"

#Name of result folder where YATSM/CCDC results are stored
results="$root/output"
output="./${name}.h5"

module purge
source /projectnb/landsat/users/shijuan/miniconda3/bin/activate yatsm_v0.6_par

i="change"
#for i in "map" "change" "rmse"; do

    echo yatsm summ_table --root $root $i $output
    yatsm summ_table --root $root $i $output
#done

source deactivate

echo "Finished submitting tile $name"
