#!/usr/bin/env bash

for SM in {0..14}
do
    #compile
    #sed -i "s/define SMID.*/define SMID ${SM}/g" functional_benchmarks.cu
    #nvcc --use_fast_math functional_benchmarks.cu -o ${SM}.out

    for BM in SM
    do
        echo ${SM}_${BM}
        read -p "Press to start test"
        ./${SM}.out --test ${BM} &
        PID=$!
        read -p "Press to kill"
        kill $PID
    done
done
