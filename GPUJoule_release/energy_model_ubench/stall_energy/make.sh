#!/usr/bin/env bash
for dir in  `find . -mindepth 1 -type d`
do
    echo $dir
    cd $dir
    for bench in *.cu;
    do
       /home/mchow/cuda-8.0/bin/nvcc -arch=sm_61 -O0 -Xcompiler -O0 -Xptxas -O0 ${bench} -o ${bench%.cu}.out
    done
    cd ../
done
