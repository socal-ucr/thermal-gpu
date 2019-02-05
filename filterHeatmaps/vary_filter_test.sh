#!/usr/bin/env bash

for FILTER in {1..1200..1}
do
    ./extractPowermapsOnly.py --filter $FILTER &
    if [ $(($FILTER % 12)) -eq  0 ]
    then
        wait
    fi
done

wait
