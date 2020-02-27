from ISA import *
import sys
import argparse
from random import random

BASE_REG_NUM = 21			# Registers are named starting from this number

div_by_zero = ["div", "rem"] 		# Are handled differently to avoid divide by zero

last_source_equals_dest = ["mad.wide"]	# For this instructions, one of the source's size is equal to dest size

# Main function for code generation, given instr name and type
def generate_code(nb_instr, instr, template_code, instr_type):

	source_width = int(instr_type[1:])			# Source registers size
	source_suf = instr_type[:1]				# Source type: s(igned), u(nsigned), f(loating point)
	dest_width = source_width*ISA_table[instr][2]		# Destination width based on the ISA table

	assert dest_width <= 64					# we do not have instruction with dest width greater than 64

	instr_nb_source_operands = ISA_table[instr][0]-1	# Number of instruction operands

	# Register declaration
	register_code = "\tasm volatile(\".reg ."+source_suf+str(dest_width)+" %r"+str(BASE_REG_NUM)+";\\n\\t\"\n"
	
	# If preventing divide by zero, we have one register less so that we out an immadiate instead
	# If the source is equal to the last source width, it should be handled differently in (1). So we skip the last source declaration
	if (instr in div_by_zero) or (instr in last_source_equals_dest):
		instr_nb_source_operands -= 1

	# Source declaration
	reg_num = 0
	for i in range(BASE_REG_NUM, BASE_REG_NUM+instr_nb_source_operands):
		register_code += "\t\t\t\".reg ."+source_suf+str(source_width)+" %r"+str(1+i)+";\\n\\t\"\n"
		reg_num += 1

	# (1)
	if instr in last_source_equals_dest:
		register_code += "\t\t\t\".reg ."+source_suf+str(dest_width)+" %r"+str(BASE_REG_NUM+reg_num+1)+";\\n\\t\"\n"
	# Data movement: puts random data in vars
	floating_point = ""
	if source_suf == "f":
		floating_point = ".0"
	register_code += "\t\t\t\"mov."+source_suf+str(dest_width)+" %r"+str(BASE_REG_NUM)+", "+str(int(1000000*random())%2**dest_width)+floating_point+";\\n\\t\"\n"
	for i in range(BASE_REG_NUM+1,BASE_REG_NUM+instr_nb_source_operands+1):
		register_code += "\t\t\t\"mov."+source_suf+str(source_width)+" %r"+str(i)+", "+str(int(1000000*random())%2*source_width)+floating_point+";\\n\\t\"\n"
	
	# (1)
	if instr in last_source_equals_dest:
		register_code += "\t\t\t\"mov."+source_suf+str(dest_width)+" %r"+str(BASE_REG_NUM+reg_num+1)+", "+str(int(1000000*random()) % 2**dest_width)+floating_point+";\\n\\t\"\n"
		instr_nb_source_operands += 1 # Make the number of operands to the original "number of operands"
	
	# Data movement: puts random data in vars
	register_code += ");\n"
	template_code = template_code.replace("REGISTER_CODE", register_code)
	# Generate code to instruction	
	compute_code = "\tasm volatile(\n"
	for i in range(nb_instr):
		# Add instruction and the dest register which always is r0
		compute_code += "\t\t\t\""+instr+"."+source_suf+str(source_width)+" %r"+str(BASE_REG_NUM)+", "
		instr_operands = ""
		# Add operands 
		for j in range(BASE_REG_NUM, BASE_REG_NUM+instr_nb_source_operands):
			instr_operands += "%r"+str(1+j)+", "
		
		# Cut the unnecessary added ", "  from the last operand
		instr_operands = instr_operands[:-2]
		
		# To handle divide by zero, the dividend should be /= 0, we use an immediate here
		if instr in div_by_zero:
			instr_operands += ", 10"
		
		instr_operands += ";\\n\\t\"\n"
		compute_code += instr_operands

	compute_code += ");\n"
	
	# Put the generated instruction into the template code
	template_code = template_code.replace("COMPUTE_CODE", compute_code)

	return template_code


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
	
	# Make it compilable for GPGPU-SIM	
	if not args.hardware:
		lines = template_code.split("\n")
		template_code = ""
		for i in lines:
			if not "power" in i:
				template_code += i+"\n"

	# For every instructions in the ISA, generate the benchmark
	for instr in ISA_table:
		supported_types = TYPES[ISA_table[instr][1]]	# list of instruction supported types

		# For every supported type for the currenct instruction instr (in ISA.py file)
		for typee in supported_types:
			# Generate the code 
			code = generate_code(args.nb_instr, instr, template_code, typee)
			# Write to file
			f = open(instr+"."+str(typee)+".cu",'w')
			f.write(code)
			f.close()


if __name__ == "__main__":
	main()			
