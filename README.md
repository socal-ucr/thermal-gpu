## GPUJoule

## Filter Heatmaps

## ubenchmarks

## Nano Benchmarks (GPGPU-SIM)
Generates, compiles, runs, and collects the stats. All arithmetic instructions with different data types supported in PTX 6.3

### Environment Setup

1- source the GPGPU-SIM ```setup_environment``` file.

2- Set ```CC``` in ```Makefile``` to ```nvcc``` binary path in your system. All benchmarks are tested with ```CUDA V10.0.130```. 

### Notes

1- ```ISA.py``` contains PTX 6.3 integer and floating point arithmetic instructions and their supported types.


2- ```generate_arith_benchmarks.py``` generates all instructions existing in ```ISA.py```. You can specify the number of instructions with an input argument to the script. By default (no input argument), 4096 instructions are generated.

3- ```run.sh``` script generates benchmarks for all instructions with different supported types using the script mentioned in 2, compiles all of them, runs them on GPGPU-SIM, and saves all the stats in a file named ```all_stats```. 

4- ```run.sh``` runs the benchmarks using ```SM2_GTX480``` config. In order to run with another config file, change ```GPU_ARCH``` in line 6 to one of the following:

	- SM2_GTX480

	- SM6_TITANX

	- SM7_TITANV

### How to use

After setting up the environment, execute:

```./run.sh```
