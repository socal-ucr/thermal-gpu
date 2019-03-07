#!/usr/bin/env bash

for SM in {0..5}
do
    #compile
    sed -i "s/define SMID.*/define SMID ${SM}/g" uBenchmarks.cu
    nvcc --use_fast_math -O0 uBenchmarks.cu -o ${SM}.out

    #for BM in FP_ADD INT_ADD SFU_SIN L1 L2 I_CACHE REG_FILE SHD_MEM
    #do
    #    echo ${SM}_${BM}
    #    read -p "Press to start test"
    #    ./${SM}.out --test ${BM} &
    #    PID=$!
    #    read -p "Press to kill"
    #    kill $PID
    #done
done
