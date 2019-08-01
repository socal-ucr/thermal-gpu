#!/usr/bin/env bash

IDLE_POWER=4
INSTS=200000000
for uBM in */
do
    cd $uBM
    TIME="$(awk '{print $5}' *0_100_64p_1000000iter_time.txt )"
    POWER="$(awk '{total += $1} END {print total/NR}' *0_100_64p_asm_power.txt)"
    EPT=$(echo "print(((${POWER}-${IDLE_POWER}.) * (${TIME}/1000.))/ (${INSTS}. * 384.))" | python)
    echo ${uBM%/},${EPT}
    cd ../
done
