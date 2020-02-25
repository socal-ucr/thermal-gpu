from ISA import *
import sys

# Main function for code generation, given instr name and type
def generate_code(nb_instr, instr, comp_op, stype, template_code, dtype="", bool_op=""):

	# Register declaration
	# For slct, 1st,2nd,and 3rd operands are the same width as the first instruction type (i.e. dtype)
	# Last operand width size is equal to the second instruction type (i.e. stype)
	if instr == "slct": 
		generated_instr_code = "\tasm volatile(\".reg "+dtype+" %r0;\\n\"\n \
				\".reg "+dtype+" %r1;\\n\"\n \
				\".reg "+dtype+" %r2;\\n\"\n \
				\".reg "+stype+" %r3;\\n\"\n"
	else:
		dest_type = dtype
		# For selp, dtype is equal to stype
		if instr == "selp":
			dest_type = stype
		# For setp, dtype is predicate
		elif instr == "setp":
			dest_type = ".pred"
		generated_instr_code = "\tasm volatile(\".reg "+dest_type+" %r0;\\n\"\n \
				\".reg "+stype+" %r1;\\n\"\n \
				\".reg "+stype+" %r2;\\n\"\n \
				\".reg .pred %r3;\\n\"\n"

	# Generate code to instruction	
	for i in range(nb_instr):
		# Add instruction and the dest register which always is r0
		generated_instr_code += "\t\t\t\""+instr+comp_op+bool_op
		
		#selp and slct have an extra predicate operand (i.e. %r3)
		if instr == "selp" or instr == "slct":
			generated_instr_code += dtype+stype+" %r0, %r1, %r2, %r3"
		else:	
			generated_instr_code +=	dtype+stype+" %r0, %r1, %r2"
		
		generated_instr_code += ";\\n\"\n"

	generated_instr_code += ");\n"
	
	# Put the generated instruction into the template code
	template_code = template_code.replace("INSERT_CODE_HERE", generated_instr_code)

	return template_code

def write_to_file(file_name, code):
	f = open(file_name,'w')
	f.write(code)
	f.close()

def main():

	nb_instr = 4096

	# Check for input arg
	if len(sys.argv) == 1:
		print("Generating 4096 instructions")
	else: 	
		nb_instr = int(sys.argv[1])	#Number of instructions to be generated
	
	# Read the template code
	# TODO: thread block size and grid are fixed now. (32 and 1 respectively)
	f = open("template.tmp",'r')
	template_code  = f.read()
	f.close()

	# For every instructions in the ISA, generate the benchmark
	for instr in ISA_table:
		supported_stypes = S_TYPES[ISA_table[instr][0]]
		supported_dtypes = D_TYPES[ISA_table[instr][1]] 
		inst = instr[:-1]
		for stype in supported_stypes:
			#set and setp have comp_op and stype
			if inst == "set" or inst == "setp":
				supported_comp_sel_ops = COMP_OPS[ISA_table[instr][0]] 
				for comp_op in supported_comp_sel_ops:
					if inst == "set" :#set has stype, and dtype
						for dtype in supported_dtypes:
							code = generate_code(nb_instr, inst, comp_op, \
									     stype, template_code, dtype)
							write_to_file(inst+comp_op+dtype+stype+".cu", code)
					
					else:#setp has stype 
						code = generate_code(nb_instr, inst, comp_op, \
								     stype, template_code)
						write_to_file(inst+comp_op+stype+".cu", code)
			else:#selp and slct does NOT have comp_op 
				if inst == "selp":#selp has only stype
					code = generate_code(nb_instr, inst, "", \
							     stype, template_code)
					write_to_file(inst+stype+".cu", code)

				else:#slct has stype and dtype
					for dtype in supported_dtypes:
						code = generate_code(nb_instr, inst, "", \
								     stype, template_code, dtype)
						write_to_file(inst+dtype+stype+".cu", code)
					
if __name__ == "__main__":
	main()			
