#!/bin/bash
RED='\033[0;31m'
NC='\033[0m'


GPU_ARCH=SM2_GTX480 	# Default GPGPUSIM config arch
NB_INSTR=4096		# Number of instructions in each benchmark

##################################
# Check if GPGPUSIM setup_environment is sourced
if [ -z ${GPGPUSIM_ROOT} ]; then 
	echo "Please set GPGPU-SIM environment variables"; 
	exit 110; 
fi

##################################
# Cleaning
make clean > /dev/null
rm -rf all_stats _cuobjdump* *.log _ptx* *.pyc gpgpu* config* *.xml _app_cuda_version* *.ptx* checkpoint* __pycache__

##################################
# Copy GPGPUSIM Config filea
cp $GPGPUSIM_ROOT/configs/tested-cfgs/$GPU_ARCH/* ./ && echo -e "${RED}$GPU_ARCH is going to be used as gpgpusim arch confing file${NC}"

###################################
# Generation and compilation
echo -e "${RED}Generating benchmarks with $NB_INSTR instructions${NC}"
python generate_benchmarks.py $NB_INSTR

echo -e "${RED}Compiling...${NC}"
if make -j$(nproc) &> compile.log; then
	rm compile.log
else
	echo -e "${RED}Compiled FAILED. see compile.log${NC}"
	exit
fi


##################################
# Stats collection
printf "INSTR_NAME, LINE#, INSTR_CNT, T_DECODE, T_ALU, T_FP, T_INT_MUL, T_TEX, T_FP_MUL, T_TRANS, T_INT_DIV, T_FP_DIV, T_INT, T_SP, T_SFU, T_DP, T_FP_SQRT, T_FP_LG, T_FP_EXP, T_FP_SIN, T_COLL_UNT, T_TENSOR, NB_MEM_ACC, NB_RF_RD, NB_RF_WR, NB_NON_RF_OPRND, T_INT_MUL24, T_INT_MUL32, DIVERGENCE, NB_LD, NB_ST, IS_SHMEM_INST, IS_SSTAR_INST, IS_TEX_INST, IS_CONST_INST, IS_PARAM_INST, NB_LOCAL_MEM_RD, NB_LOCAL_MEM_WR, NB_TEX_MEM, NB_CONST_MEM, NB_GLOB_MEM_RD, NB_GLOB_MEM_WR, IC_HIT, IC_MISS, DC_L1_LD, DC_L1_ST,\n" >> all_stats;

echo -e "${RED}Running benchmarks...${NC}"
for i in *.cu; 
do 
	echo $i; 
	if ./${i::-3} > ./${i::-3}.log 2>&1; then
        	rm ./${i::-3}.log
		printf "%s," ${i::-3} >> all_stats
		sed -n 2p gpgpu_inst_stats.txt >> all_stats;
	else
        	echo -e "${RED}Running ${i::-3} with gpgpu-sim failed. see ${i::-3}.log${NC}"
	fi
done
