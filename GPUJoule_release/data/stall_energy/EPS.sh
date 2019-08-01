#!/usr/bin/env bash

IDLE_POWER=4
INSTS=200000000
for uBM in *_power.txt
do
    uBM=${uBM%_power.txt}
    TIME="$(cat ${uBM}_time.txt)"
    POWER="$(awk '{total += $1} END {print total/NR}' ${uBM}_power.txt)"
    #EPI=$(echo "print(((${POWER}-${IDLE_POWER}.) * (${TIME}/1000.))/ (${INSTS}. * 12288.))" | python)
    EPI=$(echo "print(((${POWER}-${IDLE_POWER}.) * (${TIME}/1000.))/ (${INSTS}. * 384.))" | python)
    echo ${EPI}
done
