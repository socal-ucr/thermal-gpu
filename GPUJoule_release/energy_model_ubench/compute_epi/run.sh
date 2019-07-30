#!/usr/bin/env bash

GPUJoule_dir="/home/mchow/thermal-gpu/GPUJoule_release"

NumCTA="12"
NumThd="1024"
NumIter="1000000"

for bench in *.out
do
    bm=${bench%.out}
    $GPUJoule_dir/nvml_power_monitor/example/power_monitor 5 > $GPUJoule_dir/data/compute_energy/"$bm"_"$NumIter"iter_power.txt &
    PM_PID=$!
    ./${bench} $NumCTA $NumThd $NumIter 32 > $GPUJoule_dir/data/compute_energy/"$bm"_"$NumIter"iter_time.txt
    sleep 5
    kill -15 $PM_PID
    sleep 30
done
