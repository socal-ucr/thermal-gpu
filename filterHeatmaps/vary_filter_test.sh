#!/usr/bin/env bash

for FILTER in {1..50..1}
do
    ./filterHeatmaps.py --filter $FILTER &
    if [ $(($FILTER % 8)) -eq  0 ]
    then
        wait
    fi
done

wait
