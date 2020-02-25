#PTX ISA 6.3

# Supported types by instruction
TYPES = {
	"b32"		:	[".b32"],
	"bits"		:	[".b32", ".b16", ".b64"],
	"all_bits"	:	[".pred", ".b16", ".b32", ".b64"],
	"all"		:	[".b16", ".b32", ".b64", ".u16", ".u32", ".u64", ".s16", ".s32", ".s64"]
}

MODES = [ ".clamp.b32", ".wrap.b32" ]

ISA_table = {
	#instruction:   [source operands types & comparison operation (if applicable), destination operand's types]
	"and"		:	["all_bits", 2, "same"],
	"or"		:	["all_bits",2, "same"],
	"xor"		:	["all_bits",2, "same"],
	"not"		:	["all_bits", 1, "same"],
	"cnot"		:	["bits", 1, "same"],
	#"lop3"		:	["all"], #Not supported yet
	"shf.l.clamp"	:	["b32", 3, ".u32"],
	"shf.l.wrap"	:	["b32", 3, ".u32"],
	"shf.r.clamp"	:	["b32", 3, ".u32"],
	"shf.r.wrap"	:	["b32", 3, ".u32"],
	"shl"		:	["bits", 2, ".u32"],
	"shr"		:	["all", 2, ".u32"]
}
