#!/usr/bin/env bash

echo "test,precision,power,time,epi"
cd arithmetic
./test.sh
cd ../comp_sel
./test.sh
cd ../logic_shift
./test.sh
cd ../ 
