__global__ void
Kernel()
{
        int i;
        asm volatile("add.s32 %0, 23, 12;" : "=r"(i) );
}

int main( int argc, char** argv) 
{
	Kernel<<<1, 1>>>();
	return 0;
}
