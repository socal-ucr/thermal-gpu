#!/usr/bin/env bash

GPUJoule_dir="/home/mchow/thermal-gpu/GPUJoule_release"

NumCTA="12"
NumThd="1024"
NumIter="1000000"

    for bench in $GPUJoule_dir/energy_model_ubench/data_movement_ept/fadd_l1d_64p/*.out;
    do
        uBM=${bench##*/}
        uBM=${uBM%.out}
        echo $uBM
        ${bench} $NumCTA $NumThd $NumIter 32 1 &>> $GPUJoule_dir/energy_model_data/data_movement_energy/l1_cache/"$uBM"_"$NumIter"iter_time.txt
        sleep 30
    done

    for bench in $GPUJoule_dir/energy_model_ubench/data_movement_ept/fadd_shared_64p/*.out;
    do
        uBM=${bench##*/}
        uBM=${uBM%.out}
        echo $uBM
        $bench $NumCTA $NumThd $NumIter 32 1 &>> $GPUJoule_dir/energy_model_data/data_movement_energy/shd_mem/"$uBM"_"$NumIter"iter_time.txt
        sleep 30
    done
    
    for bench in $GPUJoule_dir/energy_model_ubench/data_movement_ept/fadd_l2d_64p/*.out;
    do
        uBM=${bench##*/}
        uBM=${uBM%.out}
        echo $uBM
        $bench $NumCTA $NumThd $NumIter 32 1 &>> $GPUJoule_dir/energy_model_data/data_movement_energy/l2_cache/"$uBM"_"$NumIter"iter_time.txt
        sleep 30
    done

    for bench in $GPUJoule_dir/energy_model_ubench/data_movement_ept/fadd_dram_64p/*.out;
    do
        uBM=${bench##*/}
        uBM=${uBM%.out}
        echo $uBM
        $bench $NumCTA $NumThd $NumIter 32 1 &>> $GPUJoule_dir/energy_model_data/data_movement_energy/dram/"$uBM"_"$NumIter"iter_time.txt
        sleep 30
    done
