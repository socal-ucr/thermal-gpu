#!/usr/bin/env bash

IDLE_POWER=4
INSTS=200000000
for uBM in *_power.txt
do
    uBM=${uBM%_power.txt}
    TIME="$(awk '{print $5}' *0_100_64p_1000000iter_time.txt )"
    POWER="$(awk '{total += $1} END {print total/NR}' ${uBM}_power.txt)"
    echo "print(((${POWER}-${IDLE_POWER}.) * (${TIME}/1000.))/ (${INSTS}. * 12288.))" | python
done
