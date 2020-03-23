#PTX ISA 6.3

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
	"u64"		: ["u64"],
}


#TODO: Some instructions (like testp, and copysign) are not added yet. Add them
ISA_table = {

	#"Instruction"		: [num of operands, list of supported types by the instruction, dest reg width according to the sources width
        "mov"                      : [2, "all_fp", 1],
        "ld.global.ca"             : [2, "all_fp", 1],
        "ld.global.cg"             : [2, "all_fp", 1],
        "ld.global.cv"             : [2, "all_fp", 1],
        "ld.shared.cv"             : [2, "all_fp", 1],
        "st.global.wb"             : [2, "all_fp", 1],
        "st.global.cg"             : [2, "all_fp", 1],
        "st.global.wt"             : [2, "all_fp", 1],
        "st.shared.wt"             : [2, "all_fp", 1],
        "prefetch.L1"              : [1, "u64",    1],
}
