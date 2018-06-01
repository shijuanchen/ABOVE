#!/bin/bash 
#$ -V
#$ -l h_rt=48:00:00
#$ -N chain1
tile_name=$1
bash map_table_tile.sh $tile_name
bash map_bgw_tile.sh $tile_name
bash mask_4type_tile.sh $tile_name
