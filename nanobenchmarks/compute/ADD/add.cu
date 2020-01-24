__global__ void
Kernel()
{
	asm volatile(".reg .s32 %r12;\n\t"
		     "add.s32 %r12, 23, 13;\n\t"
		     "add.s32 %r12, 23, 13;\n\t"
		     "add.s32 %r12, 23, 13;\n\t"
		     "add.s32 %r12, 23, 13;\n\t"
		     "add.s32 %r12, 23, 13;\n\t"
		     "add.s32 %r12, 23, 13;\n\t"
		     "add.s32 %r12, 23, 13;\n\t"
		     "add.s32 %r12, 23, 13;\n\t"
		     "add.s32 %r12, 23, 13;\n\t"
		     "add.s32 %r12, 23, 13;\n\t"
		     "add.s32 %r12, 23, 13;\n\t"
		     "add.s32 %r12, 23, 13;\n\t"
		     "add.s32 %r12, 23, 13;\n\t"
		     "add.s32 %r12, 23, 13;\n\t"
		     "add.s32 %r12, 23, 13;\n\t"
		     "add.s32 %r12, 23, 13;\n\t"
		     "add.s32 %r12, 23, 13;\n\t"
		     "add.s32 %r12, 23, 13;\n\t"
		     "add.s32 %r12, 23, 13;\n\t"
		     "add.s32 %r12, 23, 13;\n\t"
		     "add.s32 %r12, 23, 13;\n\t"
		     "add.s32 %r12, 23, 13;\n\t"
		     "add.s32 %r12, 23, 13;\n\t"
		     "add.s32 %r12, 23, 13;\n\t"
		     "add.s32 %r12, 23, 13;\n\t"
		     "add.s32 %r12, 23, 13;\n\t"
		     "add.s32 %r12, 23, 13;\n\t"
		     "add.s32 %r12, 23, 13;\n\t"
		     "add.s32 %r12, 23, 13;\n\t"
		     "add.s32 %r12, 23, 13;\n\t"
		     "add.s32 %r12, 23, 13;\n\t"
		     "add.s32 %r12, 23, 13;\n\t");
	/*asm volatile(".reg .s32 %r12;\n\t"
		     ".reg .s32 %r23;\n\t"
		     ".reg .s32 %r13;\n\t"
		     "add.s32 %r12, %r23, %r13;\n\t"
		     "add.s32 %r12, %r23, %r13;\n\t"
		     "add.s32 %r12, %r23, %r13;\n\t"
		     "add.s32 %r12, %r23, %r13;\n\t"
		     "add.s32 %r12, %r23, %r13;\n\t"
		     "add.s32 %r12, %r23, %r13;\n\t"
		     "add.s32 %r12, %r23, %r13;\n\t"
		     "add.s32 %r12, %r23, %r13;\n\t"
		     "add.s32 %r12, %r23, %r13;\n\t"
		     "add.s32 %r12, %r23, %r13;\n\t"
		     "add.s32 %r12, %r23, %r13;\n\t"
		     "add.s32 %r12, %r23, %r13;\n\t"
		     "add.s32 %r12, %r23, %r13;\n\t"
		     "add.s32 %r12, %r23, %r13;\n\t"
		     "add.s32 %r12, %r23, %r13;\n\t"
		     "add.s32 %r12, %r23, %r13;\n\t"
		    );*/
}

int main( int argc, char** argv) 
{
	Kernel<<<1, 32>>>();
	return 0;
}
