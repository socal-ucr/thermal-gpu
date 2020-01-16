## GPUJoule

## Filter Heatmaps

## ubenchmarks

## Nano Benchmarks (GPGPU-SIM)
Single instruction benchmarks that run on GPGPU-SIM

### How to use

1) **makefile:**Define the following environment variables on top of the Makefile:

        CUDA_INSTALL_PATH
        NVIDIA_COMPUTE_SDK_LOCATION

   The first, ```CUDA\_INSTALL\_PATH```, should point to the directory you installed
   the NVIDIA CUDA Toolkit (e.g., /usr/local/cuda).

   The second, ```NVIDIA\_COMPUTE\_SDK\_LOCATION```, should point to the directory you
   installed the NVIDIA GPU Computing SDK (e.g., ```~/NVIDIA\_GPU\_Computing\_SDK```)

   You must also ensure your ```PATH``` includes ```$CUDA\_INSTALL\_PATH/bin```.


2) **Error troubleshooting:** in case you encounter the following error when you want to run nano benchmarks:

        GPGPU-Sim \** ERROR: Cannot open config file 'gpgpusim.config'

   run ```set_env``` script to copy GPU architecture config file to ```bin/release```


3) **set_env script:** gets the GPU architecture supported by GPGPU-SIM as input argument. (default is: GTX480)

