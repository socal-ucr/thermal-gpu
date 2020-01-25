#!/bin/bash
RED='\033[0;31m'
NC='\033[0m'


GPU_ARCH=GTX480
NB_INSTR=4096

if [ -z ${GPGPUSIM_ROOT} ]; then 
	echo "Please set GPGPU-SIM environment variables"; 
	exit 110; 
fi

make clean

echo -e "${RED}Generating benchmarks with $NB_INSTR instructions${NC}"
python generate_int_arith_benchmarks.py $NB_INSTR

rm -f all_stats _cuobjdump* *.log _ptx* *.pyc gpgpu* config* *.xml

echo -e "${RED}Compiling...${NC}"
make -j$(nproc) > /dev/null

cp $GPGPUSIM_ROOT/configs/$GPU_ARCH/* ./ && echo -e "${RED}$GPU_ARCH is copied as gpgpusim arch confing file${NC}"

printf "INSTR,IC_H,IC_M,DC_RH,DC_RM,DC_WH,DC_WM,TC_H,TC_M,CC_H,CC_M,SHRD_ACC,REG_R,REG_W,NON_REG_OPs,SFU_ACC,SP_ACC,FPU_ACC,TOT_INST,FP_INT,DRAM_RD,DRAM_WR,DRAM_PRE,L2_RH,L2_RM,L2_WH,L2_WM,PIPE,NOC_A,IDLE_CORE_N,\n" >> all_stats;

echo -e "${RED}Running benchmarks...${NC}"
for i in *.cu; 
do 
	echo $i; 
	./${i::-3} > /dev/null && \
	printf "%s," ${i::-3} >> all_stats && \
	sed -n 2p gpgpusim_power_report__*.log >> all_stats;
	rm *.log; 
done



