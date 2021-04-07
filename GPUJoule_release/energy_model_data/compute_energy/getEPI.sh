#!/usr/bin/env bash

IDLE_POWER=17800
INSTS=256000000

UNROLL=256
ITER=1000000
NumCTA=12
NumThread=1024
WarpSize=1

for uBM in *_1000000iter_time.txt
do
    python3 getEPI.py ${uBM} ${UNROLL} ${ITER} ${NumCTA} ${NumThread} ${WarpSize} ${IDLE_POWER}

    # EPI=$(echo "print(((${POWER}-${IDLE_POWER}.) * (${TIME}/1000.))/ (${INSTS}. * 12288.))" | python)
    #echo ${bm},${EPI}
done
