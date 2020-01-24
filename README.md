## GPUJoule

## Filter Heatmaps

## ubenchmarks

## Nano Benchmarks (GPGPU-SIM)
Single-instruction benchmarks that run on GPGPU-SIM

### How to use

1) **Makefile:** define the following environment variables on top of the Makefile:

        CUDA_INSTALL_PATH
        NVIDIA_COMPUTE_SDK_LOCATION

* The first, ```CUDA_INSTALL_PATH```, should point to the directory you installed
  the NVIDIA CUDA Toolkit (e.g., /usr/local/cuda).

* The second, ```NVIDIA_COMPUTE_SDK_LOCATION```, should point to the directory you
  installed the NVIDIA GPU Computing SDK (e.g., ```~/NVIDIA_GPU_Computing_SDK```)

* You must also ensure your ```PATH``` includes ```$CUDA_INSTALL_PATH/bin```.


* **GPU_ARCH** is a make variable for setting the GPU architecture supported by GPGPU-SIM to run compiled binaries. Supported architectures are as follows:

&nbsp;&nbsp;&nbsp;&nbsp;* GTX480 (will be copied to ```compute/bin/release``` by default, i.e. no argument)
&nbsp;&nbsp;&nbsp;&nbsp;* QuadroFX5600 
&nbsp;&nbsp;&nbsp;&nbsp;* QuadroFX5800  
&nbsp;&nbsp;&nbsp;&nbsp;* TeslaC2050 

&nbsp;&nbsp;&nbsp;&nbsp;To compile and copy GTX480 config file run: ```make GPU_ARCH=GTX480```

&nbsp;&nbsp;&nbsp;&nbsp;To just copy GTX480 config file run: ```make arch_conf GPU_ARCH=GTX480```

2) **Error troubleshooting:** in case you encounter the following error when you want to run nano benchmarks:

        GPGPU-Sim \** ERROR: Cannot open config file 'gpgpusim.config'

   run ```set_env``` script to copy GPU architecture config file to ```bin/release```



### Run example
From nanobenchmarks root dir, run the following command:

```cd compute/bin/release && ./ADD```
