#PTX ISA 2.3

# Supported types by instruction
#TODO: types' name are messy. Clean them
TYPES = {
	"all_fp"	: ["u32", "u16", "s32", "u64", "s16", "s64", "f32", "f64"],
	"fp"		: ["f16", "f32", "f64"],
	"fp16_fp32"	: ["f16", "f32"],
	"fp32_fp64"	: ["f32", "f64"],
	"fp32"		: ["f32"],
	"fp64"		: ["f64"],
	"all"		: ["u32", "u16", "s32", "u64", "s16", "s64"],
	"16s_32s"	: ["u32", "u16", "s32", "s16"],
	"32s"		: ["u32", "s32"],
	"signed"	: ["s32", "s16", "s64"],
	"signed_fp"	: ["s32", "s16", "s64", "f32", "f64"],
	"bits"		: ["b32", "b64"],
	"32s_64s"	: ["u32", "u64", "s32", "s64"],
	"bit32"		: ["b32"],
}


#TODO: Some instructions (like testp, and copysign) are not added yet. Add them
ISA_table = {

	#"Instruction"		: [num of operands, list of supported types by the instruction, dest reg width according to the sources width
	
	"add"			: [3, "all_fp", 1],	
	"sub"      		: [3, "all_fp", 1],
	#"addc.cc"   		: [3, "32s", 1],	# not supported by GPGPU-SIM
	#"subc.cc"   		: [3, "32s", 1],	# not supported by GPGPU-SIM
	"mul.lo"    		: [3, "all", 1], 	# INT: all
	"mul.rn"    		: [3, "fp32_fp64", 1],	# FP: 32 and 64
	"mul.wide"  		: [3, "16s_32s", 2],	# INT: 16 and 32 TODO: mad d a b c  => size(d and c) = 2 * size(b and a)
	"mad.lo"    		: [4, "all", 1],	# INT: all
	"mad.wide"    		: [4, "16s_32s", 2],	# INT: 16 and 32 TODO: same as mul.wide
	"mad.rn"   		: [4, "fp32_fp64", 1],	# FP: 32 and 64
	"fma.rn"   		: [4, "fp", 1],		# FP: all
	"mul24.lo"  		: [3, "32s", 1],	# INT: 32 
	"mad24.lo"  		: [4, "32s", 1],	# INT: 32
	"sad" 	    		: [4, "all", 1],
	"div" 	    		: [3, "all", 1],
	"div.rn"   		: [3, "fp32_fp64", 1],	# FP
	"div" 	    		: [3, "all", 1],	# INT
	"rem" 	    		: [3, "32s_64s", 1],	# INT (In PTX documentation, 16 bit is also supported but GPGPU-SIM crashes)
	"abs" 	    		: [2, "signed_fp", 1],	
	"neg" 	    		: [2, "signed_fp", 1],
	"min" 	    		: [3, "all_fp", 1],
	"max" 	    		: [3, "all_fp", 1],
	#"popc"	    		: [2, "bits", 1],	# Not Supported by GPGPU-SIM
	#"clz" 	    		: [2, "bits", 1],	# Not Supported by GPGPU-SIM
	#"bfind"    		: [2, "32s_64s", 1],	# Not Supported by GPGPU-SIM
	#"brev"	    		: [2, "bits", 1],	# Not Supported by GPGPU-SIM
	#"bfe" 	    		: [4, "32s_64s", 1],	# Not Supported by GPGPU-SIM
	#"bfi" 	    		: [5, "bits", 1],	# Not Supported by GPGPU-SIM
	"prmt"      		: [4, "bit32", 1],	
	"rcp.rn"		: [2, "fp32_fp64", 1],
	"rcp.approx.ftz"	: [2, "fp64", 1],
	"sqrt.rn" 	    	: [2, "fp32_fp64", 1],
	"rsqrt.approx"		: [2, "fp32_fp64", 1],
	"rsqrt.approx.ftz"	: [2, "fp64", 1],
	"sin.approx"		: [2, "fp32", 1],
	"cos.approx"		: [2, "fp32", 1],
	"lg2.approx"		: [2, "fp32", 1],
	"ex2.approx"		: [2, "fp32", 1]
}
