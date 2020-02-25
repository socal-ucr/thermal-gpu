from ISA import *
import sys

# Main function for code generation, given instr name and type
def generate_code(nb_instr, instr, instr_type, nb_sources, last_op_type, template_code):

	# Register declaration
	nb_op = 0
	generated_instr_code = "\tasm volatile(\".reg "+instr_type+" %r"+str(nb_op)+";\\n\"\n"
	nb_op += 1
	for i in range(nb_sources-1):
		generated_instr_code += "\t\t\t\".reg "+instr_type+" %r"+str(nb_op)+";\\n\"\n"
		nb_op += 1
	if last_op_type == "same":
		generated_instr_code += "\t\t\t\".reg "+instr_type+" %r"+str(nb_op)+";\\n\"\n"
	else:
		generated_instr_code += "\t\t\t\".reg "+last_op_type+" %r"+str(nb_op)+";\\n\"\n"

	# Generate code to instruction	
	for i in range(nb_instr):
		# Add instruction and the dest register which always is r0
		generated_instr_code += "\t\t\t\""+instr+instr_type+" %r0, "
		
		for j in  range(1,nb_sources+1):	
			generated_instr_code +=	"%r"+str(j)+", "

		generated_instr_code = generated_instr_code[:-2]
		
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
		for instr_type in TYPES[ISA_table[instr][0]]:
			code = generate_code(nb_instr, instr, instr_type, ISA_table[instr][1], \
					     ISA_table[instr][2], template_code)
			write_to_file(instr+instr_type+".cu", code)
					
if __name__ == "__main__":
	main()			
