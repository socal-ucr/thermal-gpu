#####################################################
# CUDA PATH Settings
#####################################################
export CUDA_INSTALL_PATH=
export NVIDIA_COMPUTE_SDK_LOCATION=
include ./source.mk #for now to make above vars hidden in commits
 
#####################################################
# make
#####################################################
# TODO: Other benchmarks than Compute should be added
make_compute:
	make -C compute

make_all: make_compute

default: make_all

#####################################################
# clean
# ###################################################
clean_compute:
	make -C compute clean

clean_all: clean_compute

clean: clean_all
