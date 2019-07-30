#!/usr/bin/env bash

GPUJoule_dir="/home/mchow/thermal-gpu/GPUJoule_release"

NumCTA="12"
NumThd="1024"
NumIter="1000000"

    for bench in $GPUJoule_dir/energy_model_ubench/compute_epi/*.out
    do
        echo "$bench"_"$NumIter"iter_power.txt
        $GPUJoule_dir/nvml_power_monitor/example/power_monitor 5 > "$bench"_"$NumIter"iter_power.txt
       # PM_PID=$!
       # $bench $NumCTA $NumThd $NumIter 32 > $GPUJoule_dir/energy_model_data/compute_energy/"$bench"_"$NumIter"iter_time.txt
       # sleep 5
       # kill -15 $PM_PID
       # sleep 5
    done
