#!/usr/bin/env bash
for bench in *.cu;
do
    /home/mchow/cuda-8.0/bin/nvcc -arch=sm_61 -O0 -Xcompiler -O0 -Xptxas -O0 ${bench} -o ${bench}.out
done
