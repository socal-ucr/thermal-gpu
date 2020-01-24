#####################################################
# CUDA PATH Settings
#####################################################
export CUDA_INSTALL_PATH=
export NVIDIA_COMPUTE_SDK_LOCATION=
include ./source.mk #for now to make above vars hidden in commits
 
GPU_ARCH?=GTX480
#####################################################
# make
#####################################################
# TODO: Other benchmarks than Compute should be added
default: make_all copy_arch_conf

make_compute:
	make -C compute

make_all: make_compute

copy_arch_conf:
	@if [ -z ${GPGPUSIM_ROOT} ]; then echo "Please set GPGPU-SIM environment variables"; exit 110; fi
	@cp $(GPGPUSIM_ROOT)/configs/$(GPU_ARCH)/* compute/bin/release/	
	@echo "$(GPU_ARCH) is copied as gpgpusim arch confing file"

#####################################################
# clean
# ###################################################
clean_compute:
	@make -C compute clean

clean_all: clean_compute

clean: clean_all
