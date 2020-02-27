#!/bin/bash
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

NB_INSTR=1	# Default number of instructions in each benchmark

##################################
# Check if GPGPUSIM setup_environment is sourced
if [ -z ${GPGPUSIM_ROOT} ]; then
        echo "Please set GPGPU-SIM environment variables";
        exit 110;
fi
if [ "$1" = "clean" ]; then
	for i in `ls -d */`; do 
		echo -e "${BLUE}Cleaning: ${i::-1} ${NC}";
		cd $i && ./run.sh clean && cd ..;
	done
        exit
else
	# check if NB_INSTR needs to be changed
	if [ -n "$1" ]; then NB_INSTR=$1;fi
	for i in `ls -d */`; do 
		echo -e "${BLUE}Runnig benchmark: ${i::-1} ${NC}";
		cd $i && ./run.sh clean && ./run.sh $NB_INSTR && cd ..;
	done
fi

