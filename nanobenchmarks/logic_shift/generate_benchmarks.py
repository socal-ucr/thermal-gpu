from ISA import *
import sys
from random import random
import argparse

BASE_REG_NUM = 21
# Main function for code generation, given instr name and type
def generate_code(nb_instr, instr, instr_type, nb_sources, last_op_type, template_code):

	# Register declaration
	nb_op = 0
	register_code = "\tasm volatile(\".reg "+instr_type+" %r"+str(BASE_REG_NUM)+";\\n\"\n"
	nb_op += 1
	not_pred = False
	if not instr_type == ".pred":
		not_pred = True
		instr_width = int(instr_type[2:])
	for i in range(nb_sources-1):
		register_code += "\t\t\t\".reg "+instr_type+" %r"+str(BASE_REG_NUM+i+1)+";\\n\"\n"
		if not_pred:
			register_code += "\"mov"+instr_type+" %r"+str(BASE_REG_NUM+i+1)+", "+str(int(1000000*random()) % 2**min(32, instr_width))+";\\n\"\n"
		nb_op += 1
	if last_op_type == "same":
		register_code += "\t\t\t\".reg "+instr_type+" %r"+str(BASE_REG_NUM+nb_sources)+";\\n\"\n "
		if not_pred:
			register_code += "\"mov"+instr_type+" %r"+str(BASE_REG_NUM+nb_sources)+", "+str(int(1000000*random()) % 2**min(32, instr_width))+";\\n\"\n" 
	else:
		lo_width = int(last_op_type[2:])
		register_code += "\t\t\t\".reg "+last_op_type+" %r"+str(BASE_REG_NUM+nb_sources)+";\\n\"\n"
		if not_pred:
			register_code += "\"mov.u32 %r"+str(BASE_REG_NUM+nb_sources)+", "+str(int(1000000*random()) % 2**min(32, lo_width))+";\\n\"\n" 

	register_code += ");\n"
	template_code = template_code.replace("REGISTER_CODE", register_code)
	compute_code = "\tasm volatile(\n"; 
	# Generate code to instruction	
	for i in range(nb_instr):
		# Add instruction and the dest register which always is r0
		compute_code += "\t\t\t\""+instr+instr_type+" %r"+str(BASE_REG_NUM)+", "
		
		for j in  range(1,nb_sources+1):	
			compute_code +=	"%r"+str(BASE_REG_NUM+j)+", "

		compute_code = compute_code[:-2]
		
		compute_code += ";\\n\"\n"

	compute_code += ");\n"
	
	# Put the generated instruction into the template code
	template_code = template_code.replace("COMPUTE_CODE", compute_code)
	template_code = template_code.replace("GEN_N", str(nb_instr))

	return template_code

def write_to_file(file_name, code):
	f = open(file_name,'w')
	f.write(code)
	f.close()

def main():
	parser = argparse.ArgumentParser()
        parser.add_argument("-NI", help="number of instructions to be generated (default=1)", dest="nb_instr", action='store', default=1, type=int)
        parser.add_argument("--hardware", help="generates hardware code (default=false)", action="store_true")
        args = parser.parse_args()

        nb_instr = args.nb_instr

        # Read the template code
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
