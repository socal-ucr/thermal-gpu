#!/usr/bin/env bash

echo "test,precision,power,time,epi"
cd arithmetic
#./test.sh > arithmetic_data.csv
cd ../comp_sel
./test.sh > comp_sel_data.csv
cd ../logic_shift
./test.sh > logic_shift_data.csv
cd ../data_movement
./test.sh > data_movement.csv
cd ../
 
