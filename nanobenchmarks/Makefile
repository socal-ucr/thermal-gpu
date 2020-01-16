################################################################################
#
# Copyright 1993-2006 NVIDIA Corporation.  All rights reserved.
#
# NOTICE TO USER:   
#
# This source code is subject to NVIDIA ownership rights under U.S. and 
# international Copyright laws.  
#
# NVIDIA MAKES NO REPRESENTATION ABOUT THE SUITABILITY OF THIS SOURCE 
# CODE FOR ANY PURPOSE.  IT IS PROVIDED "AS IS" WITHOUT EXPRESS OR 
# IMPLIED WARRANTY OF ANY KIND.  NVIDIA DISCLAIMS ALL WARRANTIES WITH 
# REGARD TO THIS SOURCE CODE, INCLUDING ALL IMPLIED WARRANTIES OF 
# MERCHANTABILITY, NONINFRINGEMENT, AND FITNESS FOR A PARTICULAR PURPOSE.   
# IN NO EVENT SHALL NVIDIA BE LIABLE FOR ANY SPECIAL, INDIRECT, INCIDENTAL, 
# OR CONSEQUENTIAL DAMAGES, OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS 
# OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE 
# OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE 
# OR PERFORMANCE OF THIS SOURCE CODE.  
#
# U.S. Government End Users.  This source code is a "commercial item" as 
# that term is defined at 48 C.F.R. 2.101 (OCT 1995), consisting  of 
# "commercial computer software" and "commercial computer software 
# documentation" as such terms are used in 48 C.F.R. 12.212 (SEPT 1995) 
# and is provided to the U.S. Government only as a commercial end item.  
# Consistent with 48 C.F.R.12.212 and 48 C.F.R. 227.7202-1 through 
# 227.7202-4 (JUNE 1995), all U.S. Government End Users acquire the 
# source code with only those rights set forth herein.
#
################################################################################
#
# Build script for project
#
################################################################################

CUDA_INSTALL_PATH
NVIDIA_COMPUTE_SDK_LOCATION


BINDIR:=$(shell pwd)/bin


SETENV=export BINDIR=$(BINDIR) \
	   export ROOTDIR=$(NVIDIA_COMPUTE_SDK_LOCATION)/C/src/; \
           export BOOST_LIB=/usr/lib64; \
           export BOOST_ROOT=/usr/include; \
           export BOOST_VER=""; \
           export OPENMPI_BINDIR=/usr/lib64/mpich/bin/;

noinline?=0

default: check_environment common
	$(SETENV) make noinline=$(noinline) -C ADD
	#$(SETENV) make noinline=$(noinline) -C MUL


check_environment:
	@if [ ! -n "$(CUDA_INSTALL_PATH)" ]; then \
                echo "ERROR *** CUDA_INSTALL_PATH not set; please see README.ISPASS-2009"; \
                exit 201; \
	elif [ ! -d "$(CUDA_INSTALL_PATH)" ]; then \
                echo "ERROR *** CUDA_INSTALL_PATH=$(CUDA_INSTALL_PATH) invalid (directory does not exist)."; \
                exit 202; \
	elif [ ! -n "$(NVIDIA_COMPUTE_SDK_LOCATION)" ]; then \
                echo "ERROR *** NVIDIA_COMPUTE_SDK_LOCATION not set; please see README.ISPASS-2009"; \
                exit 203; \
        elif [ ! -d "$(NVIDIA_COMPUTE_SDK_LOCATION)" ]; then \
                echo "ERROR *** NVIDIA_COMPUTE_SDK_LOCATION=$(NVIDIA_COMPUTE_SDK_LOCATION) invalid (directory does not exist)."; \
                exit 204; \
        elif [ ! -f "$(NVIDIA_COMPUTE_SDK_LOCATION)/C/lib/libcutil_x86_64.a" -a  ! -f "$(NVIDIA_COMPUTE_SDK_LOCATION)/C/lib/libcutil.a" ]; then \
                echo "ERROR *** could not find $(NVIDIA_COMPUTE_SDK_LOCATION)/C/lib/libcutil_x86_64.a (or libcutil.a)"; \
                echo "          Build the NVIDIA GPU Computing SDK; please see README.ISPASS-2009"; \
                exit 205; \
        else \
                NVCC_PATH=`which nvcc`; \
                if [ $$? = 1 ]; then \
                        echo ""; \
                        echo "ERROR ** nvcc (from CUDA Toolkit) was not found in PATH but required to build the ISPASS 2009 benchmarks."; \
                        echo "         Try adding $(CUDA_INSTALL_PATH)/bin/ to your PATH environment variable."; \
                        echo "         Please also be sure to read README.ISPASS-2009 if you have not done so."; \
                        echo ""; \
                        exit 206; \
                else true; \
                fi \
         fi



common:
	@rm -f common; ln -s $(NVIDIA_COMPUTE_SDK_LOCATION)/C/common common;

clean:
	@rm -rf bin
	@rm -rf ADD/obj
	@unlink common
