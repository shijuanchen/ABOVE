#!/bin/bash
tile=$1
while read -r line
do
    tile_name=$(echo $line | cut -c 1-7)
    echo $tile_name
    mkdir "/projectnb/landsat/users/shijuan/above/post_process/agr_post_pro/$tile_name"
done < "agr_tiles.txt"
