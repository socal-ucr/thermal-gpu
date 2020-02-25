#PTX ISA 6.3

# Supported types by instruction
D_TYPES = {
	"32s"	:	[".u32",".s32",".f32"],
	"all"		:	[".b16", ".b32", ".b64",
				 ".u16", ".u32", ".u64",
				 ".s16", ".s32", ".s64",
				 ".f32", ".f64" ]
}

S_TYPES = {
	"unsigned"	:	[".u16", ".u32", ".u64"],
	"signed_int"	:	[".s16", ".s32", ".s64"],
	"fp"		:	[".f32", ".f64"],
	"bits"		:	[".b16", ".b32", ".b64"],
	"sf"		:	[".s32", ".f32"],
	"all"		:	[".b16", ".b32", ".b64",
				 ".u16", ".u32", ".u64",
				 ".s16", ".s32", ".s64",
				 ".f32", ".f64" ]
	}

COMP_OPS = {	"signed_int"	:	[".eq", ".ne", ".lt", ".le", ".gt", ".ge"],
		"unsigned"	:	[".eq", ".ne", ".lo", ".ls", ".hi", ".hs"],
		"fp"		:	[".eq", ".ne", ".lt", ".le", ".gt", ".ge", 
					 ".equ", ".neu", ".ltu", ".leu", ".gtu", 
					 ".geu", ".num", ".nan"],
		"bits"		:	[".eq", ".ne"],
	}

BOOL_OPS = [ ".and", ".or", ".xor", ""]	#none is used for instructions without .pred operands	

ISA_table = {
	#instruction:   [source operandss types & comparison operation (if applicable), destination operand's types]
	"seti"	:	["signed_int", "32s"],
	"setu"	:	["unsigned", "32s"],
	"setf"	:	["fp", "32s"],
	"setpb"	:	["bits", "32s"],
	"setpi"	:	["signed_int", "32s"],
	"setpu"	:	["unsigned", "32s"],
	"setpf"	:	["fp", "32s"],
	"setb"	:	["bits", "32s"],
	"selpa"	:	["all", "32s"],
	"slcta"	:	["sf", "all"]
}
