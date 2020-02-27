#!/bin/bash
RED='\033[0;31m'
NC='\033[0m'


NB_INSTR=1	        # Default number of instructions in each benchmark
BENCHMARK="arithmetic"

##################################
# Cleaning
make clean > /dev/null

##################################
# If just cleaning => exit, otherwise, compile and run all benchmarks
if [ "$1" = "clean" ]; then
	exit
else
	###################################
	# Generation and compilation
	if [ -n "$1" ]; then NB_INSTR=$1; fi
	echo -e "${RED}Generating benchmarks with $NB_INSTR instructions${NC}"
	python generate_benchmarks.py -NI $NB_INSTR --hardware

	echo -e "${RED}Compiling...${NC}"
	if make -j$(nproc) &> compile.log; then
        	rm compile.log
	else
        	echo -e "${RED}Compiled FAILED. see compile.log${NC}"
	        exit
	fi
fi
