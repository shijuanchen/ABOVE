#!/bin/bash -l
#$ -V
#$ -l h_rt=24:00:00
#$ -N categorize_FF_NF_NN
#$ -j y
#$ -l mem_total=98G

tile=$1
out_dir="/projectnb/landsat/projects/ABOVE/CCDC/$tile/out_category"
if [ ! -d "$folder" ];
    then
        mkdir out_dir
        module purge
        source /projectnb/landsat/users/shijuan/miniconda3/bin/activate yatsm_v0.6_par
        python /usr3/graduate/shijuan/Desktop/my_ABOVE_git/categorize_FF_NF_NN_v3.py --tile_name $tile
        source deactivate
    else
        echo "$out_dir exists!" 
fi
echo "Finished submitting tile $tile"
