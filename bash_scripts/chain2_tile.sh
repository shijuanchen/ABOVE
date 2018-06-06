#!/bin/bash 
#$ -V
#$ -l h_rt=48:00:00
#$ -N chain2
tile_name=$1
bash rf_FN_NN_tile.sh $tile_name
bash categorize_tile.sh $tile_name
bash combine_classes_tile.sh $tile_name
