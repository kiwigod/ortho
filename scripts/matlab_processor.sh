#!/bin/bash
#Author: Arjun Sardjoe Missier

BASE=/home/yuqi/Downloads/raw_data/cat_4
OUT=/home/yuqi/out
TMP=/home/yuqi/tmp


for pat in $(ls $BASE);
do
    mkdir -p $TMP
    cp -r $BASE/$pat $TMP

    matlab -nojvm -r "process_patient $TMP $OUT"
    #ls $TMP/$pat

    rm -rf $TMP
done
echo "Done~!"
