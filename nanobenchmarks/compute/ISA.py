#PTX ISA 2.3
TYPES = {
	"all" 	 : ["u32", "u16", "s32", "u64", "s16", "s64"],
	"32s"	 : ["u32", "s32"],
	"signed" : ["s16", "s32", "s64"],
	"bits"	 : ["b32", "b64"],
	"32s_64s": ["u32", "u64", "s32", "s64"],
	"bit32"  : ["b32"]
}

ISA_table = {
	#"operator"	: 	[num of operands, types, dest width based on sources
	"add"       :	[3, "all", 1],	
	"sub"       :	[3, "all", 1],
	"addc"	    :	[3, "32s", 1],
	"subc"      :	[3, "32s", 1],
	"mul.wide"  :	[3, "all", 2],
	"mad.hi"    :	[4, "all", 1],
	"mul24.hi"  :	[3, "32s", 1],
	"mad24.hi"  :	[4, "32s", 1],
	"sad" 	    :	[4, "all", 1],
	"div" 	    :	[3, "all", 1],
	"rem" 	    :	[3, "all", 1],
	"abs" 	    :	[2, "signed", 1],
	"neg" 	    :	[2, "signed", 1],
	"min" 	    :	[3, "all", 1],
	"max" 	    :	[3, "all", 1],
	"popc"	    :	[2, "bits", 1],
	"clz" 	    :	[2, "bits", 1],
	"bfind"	    :	[2, "32s_64s", 1],
	"brev"	    :	[2, "bits", 1],
	"bfe" 	    :	[4, "32s_64s", 1],
	"bfi" 	    :	[5, "bits", 1],
	"prmt"      :	[4, "bit32", 1]
}
