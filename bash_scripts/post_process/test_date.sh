date1=$(date -r Bh07v07_FF_FN_NF_NN_1986_cl.tif +"%Y%m%d")
echo $date1
date2=$(date -d 2018-07-19 +"%Y%m%d")
echo $date2
if [ $date1 -ge $date2 ];
then
    echo "this file is created after 2018-07-19";
fi
