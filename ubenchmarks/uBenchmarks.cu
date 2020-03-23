#include <stdio.h>
#include <stdlib.h>
// Includes
#include <stdio.h>
#include <string>

// includes, project
#include "include/sdkHelper.h"  // helper for shared functions common to CUDA SDK samples
#include "include/argparse.hpp"
#include "include/repeat.h"
//#include <shrQATest.h>
//#include <shrUtils.h>

// includes CUDA
#include <cuda_runtime.h>

#define THREADS_PER_BLOCK 1024
#define NUM_OF_BLOCKS 20
#define ITERATIONS 100000000
#define SMID 5
#include "include/ContAcq-IntClk.h"

// Variables
float* h_A;
float* h_B;
float* h_C;
float* d_A;
float* d_B;
float* d_C;
bool noprompt = false;
unsigned int my_timer;

// Functions
void CleanupResources(void);
void RandomInit(float*, int);
void RandomInit(unsigned*, int);
void ParseArguments(int, char**);

////////////////////////////////////////////////////////////////////////////////
// These are CUDA Helper functions

// This will output the proper CUDA error strings in the event that a CUDA host call returns an error
#define checkCudaErrors(err)  __checkCudaErrors (err, __FILE__, __LINE__)

inline void __checkCudaErrors(cudaError err, const char *file, const int line )
{
  if(cudaSuccess != err){
	fprintf(stderr, "%s(%i) : CUDA Runtime API error %d: %s.\n",file, line, (int)err, cudaGetErrorString( err ) );
	 exit(-1);
  }
}

// This will output the proper error string when calling cudaGetLastError
#define getLastCudaError(msg)      __getLastCudaError (msg, __FILE__, __LINE__)

inline void __getLastCudaError(const char *errorMessage, const char *file, const int line )
{
  cudaError_t err = cudaGetLastError();
  if (cudaSuccess != err){
	fprintf(stderr, "%s(%i) : getLastCudaError() CUDA error : %s : (%d) %s.\n",file, line, errorMessage, (int)err, cudaGetErrorString( err ) );
	exit(-1);
  }
}

// end of CUDA Helper Functions

__device__ uint get_smid(void) {

     uint ret;
     asm("mov.u32 %0, %smid;" : "=r"(ret) );
     return ret;
}


////////////////////////////////////////////////////////////////////////////////
//Funcational benchmarks

__global__ void SM(const float* A, const float* B, float* C, int N)
{
    int i = blockDim.x * blockIdx.x + threadIdx.x;
    //Do Some Computation
    float Value1=A[i];
    unsigned int I1=A[i];
    unsigned int I2=B[i];
    float Value2=0;
    float Value=0;
    unsigned I3 = 0;
    // exponential function
    unsigned int smid = get_smid();
    if(smid == SMID)
    {
        for(unsigned long k=0; k<ITERATIONS;k++) 
	{
            repeat2048(asm volatile ("sin.approx.ftz.f32 %0, %2;\n\t"
				     "sin.approx.ftz.f32 %1, %3;" :
				     "=f"(Value2),"=f"(Value) : "f" (Value1), "f"(Value2));
                       asm volatile ("add.rz.f32 %0, %1, %2;": "=f"(Value) : "f"(Value1), "f"(Value2));
                       asm volatile ("add.u32 %0, %1, %2;": "=r"(I3) : "r"(I1), "r"(I2));
                      )
        }
    }
   Value=I3;		

    C[i]=Value;
    __syncthreads();
}
__global__ void SFU_EXP(const float* A, const float* B, float* C, int N)
{
    int i = blockDim.x * blockIdx.x + threadIdx.x;
    //Do Some Computation
    float Value1=A[i];
    float Value2=0;
    float Value3=0;
    float Value=0;
    // exponential function
    unsigned int smid = get_smid();
    if(smid == SMID)
    {
        for(unsigned long k=0; k<ITERATIONS;k++) 
	{
            repeat2048(Value2=expf(Value1);Value3=expf(Value2);Value1=expf(Value3);)
        }
    }
   Value=Value3-Value2;		

    C[i]=Value;
    __syncthreads();
}
__global__ void SFU_LOG(const float* A, const float* B, float* C, int N)
{
    int i = blockDim.x * blockIdx.x + threadIdx.x;
    //Do Some Computation
    float Value1=0;
    float Value2=0;
    float Value3=0;
    float Value=0;
    float I1=A[i];
    float I2=B[i];


    // logarithmic
    unsigned int smid = get_smid();
    if(smid == SMID)
    {
        for(unsigned long k=0; k<ITERATIONS;k++)
        {
	    repeat2048(asm volatile ("lg2.approx.ftz.f32 %0, %2;\n\t"
				     "lg2.approx.ftz.f32 %1, %3;" :
				     "=f"(Value1),"=f"(Value2) : "f" (I1), "f"(I2));)
        }
    }

   Value=Value3-Value2+Value1;		

    C[i]=Value;
    __syncthreads();

}

__global__ void SFU_SIN(const float* A, const float* B, float* C, int N)
{
    int i = blockDim.x * blockIdx.x + threadIdx.x;
    //Do Some Computation
    float Value1=A[i];
    float Value2=0;
    float Value3=0;
    float Value=0;

    //sinusoidal functions
    unsigned int smid = get_smid();
    if(smid == SMID)
    {
        for(unsigned long k=0; k<ITERATIONS;k++) 
        {  
	    repeat2048(asm volatile ("sin.approx.ftz.f32 %0, %2;\n\t"
				     "sin.approx.ftz.f32 %1, %3;" :
				     "=f"(Value2),"=f"(Value3) : "f" (Value1), "f"(Value2));)  
        }
    }


   Value=Value3-Value2+Value1;		

    C[i]=Value;
    __syncthreads();

}

__global__ void SFU_SQRT(const float* A, const float* B, float* C, int N)
{
    int i = blockDim.x * blockIdx.x + threadIdx.x;
    //Do Some Computation
    float Value1=0;
    float Value2=9999999;
    float Value3=9999999;
    float Value=0;

    //square root
    unsigned int smid = get_smid();
    if(smid == SMID)
    {
        for(unsigned long k=0; k<ITERATIONS;k++) 
        {
	    repeat2048(asm volatile ("sqrt.approx.ftz.f32 %0, %2;\n\t"
				     "sqrt.approx.ftz.f32 %1, %3;" :
				     "=f"(Value),"=f"(Value1) : "f" (Value2), "f"(Value3));)
        }
    }
   Value=Value3-Value2+Value1;		

    C[i]=Value;
    __syncthreads();

}
__global__ void FP_ADD(const float* A, const float* B, float* C, int N)
{
    int i = blockDim.x * blockIdx.x + threadIdx.x;
    //Do Some Computation
    float Value1=0;
    float I1=A[i];
    float I2=B[i];

    unsigned int smid = get_smid();

    if (smid == SMID)
    {
        // Excessive Addition access
    	for(unsigned long k=0; k<ITERATIONS;k++)
	{
	    repeat2048(asm volatile ("add.rz.f32 %0, %1, %2;": "=f"(Value1) : "f"(I1), "f"(I2));)
    	}
    }
    __syncthreads();
    C[i]=Value1;
}

__global__ void FP_DIV(const float* A, const float* B, float* C, int N)
{
    int i = blockDim.x * blockIdx.x + threadIdx.x;
    //Do Some Computation
    float Value1 = 0.0;
    float I1=A[i];
    float I2=B[i];


    __syncthreads();
   // Excessive Division Operations
    unsigned int smid = get_smid();
    if(smid == SMID)
    {
        for(unsigned long k=0; k<ITERATIONS;k++) 
        {
	    repeat2048(asm volatile ("div.rz.f32 %0, %1, %2;": "=f"(Value1) : "f"(I1), "f"(I2));)
        }
    }
    __syncthreads();
    C[i]= Value1;
}

__global__ void FP_MAD(const float* A, const float* B, float* C, int N)
{
    int i = blockDim.x * blockIdx.x + threadIdx.x;
    //Do Some Computation
    float Value;
    float I1=A[i];
    float I2=B[i];

    // Excessive Addition access
    unsigned int smid = get_smid();
    if(smid == SMID)
    {
        for(unsigned long k=0; k<ITERATIONS;k++) {
            repeat2048(asm volatile ("fma.rz.f32 %0, %1, %2, %2;": "=f"(Value) : "f"(I1), "f"(I2));)
        }
    }
    __syncthreads();

    C[i]=Value;
}

__global__ void FP_MUL(const float* A, const float* B, float* C, int N)
{
    int i = blockDim.x * blockIdx.x + threadIdx.x;
    //Do Some Computation
    float Value1;
    float I1=A[i];
    float I2=B[i];

    // Excessive Addition access
    unsigned int smid = get_smid();
    if(smid == SMID)
    {
        for(unsigned long k=0; k<ITERATIONS;k++)
        {
	    repeat2048(asm volatile ("mul.rz.f32 %0, %1, %2;": "=f"(Value1) : "f"(I1), "f"(I2));)
        }
    }
    __syncthreads();

    C[i]=Value1;

}

__global__ void INT_ADD(const float* A, const float* B, float* C, int N)
{
    int i = blockDim.x * blockIdx.x + threadIdx.x;
    //Do Some Computation
    unsigned Value1=0;
    unsigned I1=(unsigned)A[i];
    unsigned I2=(unsigned)B[i];

    // Excessive Addition access
    unsigned int smid = get_smid();
    if(smid == SMID)
    {
        for(unsigned long k=0; k<ITERATIONS;k++) 
        {
	    repeat2048(asm volatile ("add.u32 %0, %1, %2;": "=r"(Value1) : "r"(I1), "r"(I2));)
        }
    }
    __syncthreads();

    C[i]=(float)Value1;
}
__global__ void INT_DIV(const float* A, const float* B, float* C, int N)
{
    int i = blockDim.x * blockIdx.x + threadIdx.x;
    //Do Some Computation
    unsigned Value1=0;
    unsigned I1=(unsigned)A[i];
    unsigned I2=(unsigned)B[i];

    // Excessive Addition access
    unsigned int smid = get_smid();
    if(smid == SMID)
    {
        for(unsigned long k=0; k<ITERATIONS;k++) 
        {
	    repeat2048(asm volatile ("div.u32 %0, %1, %2;": "=r"(Value1) : "r"(I1), "r"(I2));)
        }
    }
    __syncthreads();

    C[i]=(float)Value1;
}
__global__ void INT_LOGIC(const float* A, const float* B, float* C, int N)
{
    int i = blockDim.x * blockIdx.x + threadIdx.x;
    //Do Some Computation
    unsigned Value1=0;
    unsigned I1=(unsigned)A[i];
    unsigned I2=(unsigned)B[i];

    // Excessive Addition access
    unsigned int smid = get_smid();
    if(smid == SMID)
    {
        for(unsigned k=0; k<ITERATIONS;k++) 
        {
	    repeat2048(asm volatile ("and.b32 %0, %1, %2;": "=r"(Value1) : "r"(I1), "r"(I2));)
	    repeat2048(asm volatile ("or.b32 %0, %1, %2;": "=r"(Value1) : "r"(I1), "r"(I2));)
        }
    }
    __syncthreads();

    C[i]=(float)Value1;

}
__global__ void INT_MUL(const float* A, const float* B, float* C, int N)
{
    int i = blockDim.x * blockIdx.x + threadIdx.x;
    //Do Some Computation
    unsigned Value1=0;
    unsigned I1=(unsigned)A[i];
    unsigned I2=(unsigned)B[i];

    // Excessive Addition access
    unsigned int smid = get_smid();
    if(smid == SMID)
    {
        for(unsigned long k=0; k<ITERATIONS;k++) 
        {
	    repeat2048(asm volatile ("mul.lo.u32 %0, %1, %2;": "=r"(Value1) : "r"(I1), "r"(I2));)
        }
    }
    __syncthreads();

    C[i]=(float)Value1;
}

///////////////////// CACHE and MEMORY BENCHMARKS/////////////////////////////////
__global__ void L1(float* A, float* C, int N){
    int tid = blockDim.x * blockIdx.x + threadIdx.x;
    //Do Some Computation

    //int size = (LINE_SIZE*ASSOC*SETS)/sizeof(int);
    //unsigned j=0, k=0;
    unsigned long k=0;
    // Excessive Addition access
    unsigned int smid = get_smid();
    int temp = 0;
    if(smid == SMID)
    {
	// Fill the L1 cache, Miss on first LD, Hit on subsequent LDs
	for(k=0; k<ITERATIONS; ++k){
            repeat2048(asm volatile ("ld.global.u32 %0, [%1];" : "=r"(temp): "l" (A+tid));)
	}

	C[tid]=temp;
    }
    __syncthreads();
}
__global__ void L1_ALL(float* A, float* C, int N){
    int tid = blockDim.x * blockIdx.x + threadIdx.x;
    //Do Some Computation

    //int size = (LINE_SIZE*ASSOC*SETS)/sizeof(int);
    //unsigned j=0, k=0;
    unsigned k=0;
    // Excessive Addition access
    unsigned int smid = get_smid();
    int temp = 0;
    // Fill the L1 cache, Miss on first LD, Hit on subsequent LDs
    for(k=0; k<ITERATIONS; ++k){
        repeat2048(asm volatile ("ld.global.u32 %0, [%1];" : "=r"(temp): "l" (A+tid));)
    }

    C[tid]=temp;
    __syncthreads();
}

__global__ void L2(float* A, float* C, int N){
    int tid = blockDim.x * blockIdx.x + threadIdx.x;
    //Do Some Computation

    //int size = (LINE_SIZE*ASSOC*SETS)/sizeof(int);
    //unsigned j=0, k=0;
    unsigned long k=0;
    // Excessive Addition access
    unsigned int smid = get_smid();
    int temp = 0;
    if(smid == SMID)
    {
	// Fill the L1 cache, Miss on first LD, Hit on subsequent LDs
	for(k=0; k<ITERATIONS; ++k){
            repeat2048(asm volatile ("ld.cg.u32 %0, [%1];" : "=r"(temp): "l" (A+tid));)
	}

	C[tid]=temp;
    }
    __syncthreads();
}

__global__ void L2_ALL(float* A, float* C, int N){
    int tid = blockDim.x * blockIdx.x + threadIdx.x;
    //Do Some Computation

    //int size = (LINE_SIZE*ASSOC*SETS)/sizeof(int);
    //unsigned j=0, k=0;
    unsigned k=0;
    int temp = 0;
    for(k=0; k<ITERATIONS; ++k){
        repeat2048(asm volatile ("ld.cg.u32 %0, [%1];" : "=r"(temp): "l" (A+tid));)
    }

    C[tid]=temp;
    __syncthreads();
}

__global__ void I_CACHE(float* A, float* C, int N){
    int tid = blockDim.x * blockIdx.x + threadIdx.x;
    //Do Some Computation

    //int size = (LINE_SIZE*ASSOC*SETS)/sizeof(int);
    //unsigned j=0, k=0;
    int temp = 0;
    unsigned int smid = get_smid();
    if(smid == SMID)
    {
        for(unsigned long k=0; k<ITERATIONS; ++k){
LABEL:
            goto LABEL;
        }
    }

    C[tid]=temp;
    __syncthreads();
}

__global__ void REG_FILE(float* A, float* C, int N){
    int tid = blockDim.x * blockIdx.x + threadIdx.x;
    //Do Some Computation

    //int size = (LINE_SIZE*ASSOC*SETS)/sizeof(int);
    //unsigned j=0, k=0;
    unsigned long k = 0;
    unsigned long temp = 123456789;
    unsigned long temp1 = 0;
    unsigned int smid = get_smid();
    if(smid == SMID)
    {
        for(k=0; k<ITERATIONS; ++k){
            repeat2048(asm volatile ("mov.u64 %0, %1;" : "=l"(temp1): "l" (temp));)
        }
    }
    k = temp1;
    C[tid]=temp;
    __syncthreads();
}
__global__ void SHD_MEM(float* A, float* C, int N){
    //int size = (LINE_SIZE*ASSOC*SETS)/sizeof(int);
    //unsigned j=0, k=0;
    unsigned long k=0;
    unsigned int smid = get_smid();

    __shared__ unsigned long long sdata[THREADS_PER_BLOCK];

    __shared__ void **tmp_ptr;

    __shared__ void *arr[THREADS_PER_BLOCK];
    int i =0; 
    if (threadIdx.x == 0) {
        for (i=0; i < THREADS_PER_BLOCK; i++) {
            arr[i] = (void *)&sdata[i];
        }
        for (i=0; i < (THREADS_PER_BLOCK - 1); i++) {
            sdata[i] = (unsigned long long)arr[i+1];
        }
        sdata[THREADS_PER_BLOCK - 1] = (unsigned long long) arr[0];
    }

    __syncthreads();

    tmp_ptr = (void **)(&(arr[(threadIdx.x + 1)%THREADS_PER_BLOCK]));
    if(smid == SMID)
    {
        for(k=0; k<ITERATIONS; ++k){
            repeat2048(tmp_ptr = (void**)(*tmp_ptr);)
        }
    }
    __syncthreads();
}

int main(int argc, const char** argv)
{
    ArgumentParser parser;
    parser.addArgument("-t","--test",1,false);

    parser.parse(argc, argv);
    std::string test_name = parser.retrieve<std::string>("test");
    int N = THREADS_PER_BLOCK*NUM_OF_BLOCKS;
    size_t size = N * sizeof(float);
    // Allocate input vectors h_A and h_B in host memory
    h_A = (float*)malloc(size);
    if (h_A == 0) CleanupResources();
    h_B = (float*)malloc(size);
    if (h_B == 0) CleanupResources();
    h_C = (float*)malloc(size);
    if (h_C == 0) CleanupResources();

    // Initialize input vectors
    RandomInit(h_A, N);
    RandomInit(h_B, N);

    // Allocate vectors in device memory
    checkCudaErrors( cudaMalloc((void**)&d_A, size) );
    checkCudaErrors( cudaMalloc((void**)&d_B, size) );
    checkCudaErrors( cudaMalloc((void**)&d_C, size) );

    // Copy vectors from host memory to device memory
    checkCudaErrors( cudaMemcpy(d_A, h_A, size, cudaMemcpyHostToDevice) );
    checkCudaErrors( cudaMemcpy(d_B, h_B, size, cudaMemcpyHostToDevice) );

    dim3 dimGrid(NUM_OF_BLOCKS,1,1);
    dim3 dimBlock(THREADS_PER_BLOCK,1,1);

    printf("Microbenchmarks-%s\n",test_name.c_str());
    if(test_name.compare("SM") == 0)
        SM<<<dimGrid,dimBlock>>>(d_A, d_B, d_C, N);
    else if(test_name.compare("SFU_EXP") == 0)
        SFU_EXP<<<dimGrid,dimBlock>>>(d_A, d_B, d_C, N);
    else if(test_name.compare("SFU_LOG") == 0)
        SFU_LOG<<<dimGrid,dimBlock>>>(d_A, d_B, d_C, N);
    else if(test_name.compare("SFU_SIN") == 0)
        SFU_SIN<<<dimGrid,dimBlock>>>(d_A, d_B, d_C, N);
    else if(test_name.compare("SFU_SQRT") == 0)
        SFU_SQRT<<<dimGrid,dimBlock>>>(d_A, d_B, d_C, N);
    else if(test_name.compare("FP_ADD") == 0)
        FP_ADD<<<dimGrid,dimBlock>>>(d_A, d_B, d_C, N);
    else if(test_name.compare("FP_DIV") == 0)
        FP_DIV<<<dimGrid,dimBlock>>>(d_A, d_B, d_C, N);
    else if(test_name.compare("FP_MAD") == 0)
        FP_MAD<<<dimGrid,dimBlock>>>(d_A, d_B, d_C, N);
    else if(test_name.compare("FP_MUL") == 0)
        FP_MUL<<<dimGrid,dimBlock>>>(d_A, d_B, d_C, N);
    else if(test_name.compare("INT_ADD") == 0)
        INT_ADD<<<dimGrid,dimBlock>>>(d_A, d_B, d_C, N);
    else if(test_name.compare("INT_DIV") == 0)
        INT_DIV<<<dimGrid,dimBlock>>>(d_A, d_B, d_C, N);
    else if(test_name.compare("INT_LOGIC") == 0)
        INT_LOGIC<<<dimGrid,dimBlock>>>(d_A, d_B, d_C, N);
    else if(test_name.compare("INT_MUL") == 0)
        INT_MUL<<<dimGrid,dimBlock>>>(d_A, d_B, d_C, N);
    else if(test_name.compare("L1") == 0)
        L1<<<dimGrid,dimBlock>>>(d_A, d_C, N);
    else if(test_name.compare("L1_ALL") == 0)
        L1_ALL<<<dimGrid,dimBlock>>>(d_A, d_C, N);
    else if(test_name.compare("L2") == 0)
        L2<<<dimGrid,dimBlock>>>(d_A, d_C, N);
    else if(test_name.compare("L2_ALL") == 0)
        L2_ALL<<<dimGrid,dimBlock>>>(d_A, d_C, N);
    else if(test_name.compare("I_CACHE") == 0)
        I_CACHE<<<dimGrid,dimBlock>>>(d_A, d_C, N);
    else if(test_name.compare("REG_FILE") == 0)
        REG_FILE<<<dimGrid,dimBlock>>>(d_A, d_C, N);
    else if(test_name.compare("SHD_MEM") == 0)
        SHD_MEM<<<dimGrid,dimBlock>>>(d_A, d_C, N);
    else
    {
        printf("INVALID TEST\n");
        exit(1);
    }

    getLastCudaError("kernel launch failure");
    cudaDeviceSynchronize();
    printf("after\n");

    // Copy result from device memory to host memory
    // h_C contains the result in host memory
    checkCudaErrors( cudaMemcpy(h_C, d_C, size, cudaMemcpyDeviceToHost) );
     
    CleanupResources();

    return 0;
}

void CleanupResources(void)
{
  // Free device memory
  if (d_A)
	cudaFree(d_A);
  if (d_B)
	cudaFree(d_B);
  if (d_C)
	cudaFree(d_C);

  // Free host memory
  if (h_A)
	free(h_A);
  if (h_B)
	free(h_B);
  if (h_C)
	free(h_C);

}

// Allocates an array with random float entries.
void RandomInit(float* data, int n)
{
  for (int i = 0; i < n; ++i){ 
	data[i] = rand() / RAND_MAX;
  }
}
