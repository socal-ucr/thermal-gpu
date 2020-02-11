#!/bin/bash
RED='\033[0;31m'
NC='\033[0m'


GPU_ARCH=SM2_GTX480
NB_INSTR=1

if [ -z ${GPGPUSIM_ROOT} ]; then 
	echo "Please set GPGPU-SIM environment variables"; 
	exit 110; 
fi

make clean
rm -rf all_stats _cuobjdump* *.log _ptx* *.pyc gpgpu* config* *.xml _app_cuda_version* *.ptx* checkpoint* __pycache__

echo -e "${RED}Generating benchmarks with $NB_INSTR instructions${NC}"
python generate_int_arith_benchmarks.py $NB_INSTR

echo -e "${RED}Compiling...${NC}"
make -j$(nproc) > /dev/null

cp $GPGPUSIM_ROOT/configs/tested-cfgs/$GPU_ARCH/* ./ && echo -e "${RED}$GPU_ARCH is copied as gpgpusim arch confing file${NC}"

printf "INSTR_NAME, LINE#, INSTR_CNT, T_DECODE, T_ALU, T_FP, T_INT_MUL, T_TEX, T_FP_MUL, T_TRANS, T_INT_DIV, T_FP_DIV, T_INT, T_SP, T_SFU, T_DP, T_FP_SQRT, T_FP_LG, T_FP_EXP, T_FP_SIN, T_COLL_UNT, T_TENSOR, NB_MEM_ACC, NB_RF_RD, NB_RF_WR, NB_NON_RF_OPRND, T_INT_MUL24, T_INT_MUL32, DIVERGENCE, NB_LD, NB_ST, IS_SHMEM_INST, IS_SSTAR_INST, IS_TEX_INST, IS_CONST_INST, IS_PARAM_INST, NB_LOCAL_MEM_RD, NB_LOCAL_MEM_WR, NB_TEX_MEM, NB_CONST_MEM, NB_GLOB_MEM_RD, NB_GLOB_MEM_WR, IC_HIT, IC_MISS, DC_L1_LD, DC_L1_ST,\n" >> all_stats;

echo -e "${RED}Running benchmarks...${NC}"
for i in *.cu; 
do 
	echo $i; 
	./${i::-3} > /dev/null && \
	printf "%s," ${i::-3} >> all_stats && \
	sed -n 2p gpgpu_inst_stats.txt >> all_stats;
done


#tail -n +2 gpgpu_inst_stats.txt | awk '{print $2}' | xargs -I% sed -n %p vadd.1.sm_30.ptx | cut -d '.' -f1
