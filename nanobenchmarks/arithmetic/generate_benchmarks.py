from ISA import *
import sys

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
	generated_instr_code = "\tasm volatile(\".reg ."+source_suf+str(dest_width)+" %r0;\\n\"\n"
	
	# If preventing divide by zero, we have one register less so that we out an immadiate instead
	# If the source is equal to the last source width, it should be handled differently in (1). So we skip the last source declaration
	if (instr in div_by_zero) or (instr in last_source_equals_dest):
		instr_nb_source_operands -= 1

	# Source declaration
	reg_num = 0
	for i in range(instr_nb_source_operands):
		generated_instr_code += "\t\t\t\".reg ."+source_suf+str(source_width)+" %r"+str(1+i)+";\\n\"\n"
		reg_num += 1

	# (1)
	if instr in last_source_equals_dest:
		generated_instr_code += "\t\t\t\".reg ."+source_suf+str(dest_width)+" %r"+str(reg_num+1)+";\\n\"\n"
		instr_nb_source_operands += 1 # Make the number of operands to the original "number of operands"
	
	# Generate code to instruction	
	for i in range(nb_instr):
		# Add instruction and the dest register which always is r0
		generated_instr_code += "\t\t\t\""+instr+"."+source_suf+str(source_width)+" %r0, "
		instr_operands = ""
		# Add operands 
		for j in range(instr_nb_source_operands):
			instr_operands += "%r"+str(1+j)+", "
		
		# Cut the unnecessary added ", "  from the last operand
		instr_operands = instr_operands[:-2]
		
		# To handle divide by zero, the dividend should be /= 0, we use an immediate here
		if instr in div_by_zero:
			instr_operands += ", 10"
		
		instr_operands += ";\\n\"\n"
		generated_instr_code += instr_operands

	generated_instr_code += ");\n"
	
	# Put the generated instruction into the template code
	template_code = template_code.replace("INSERT_CODE_HERE", generated_instr_code)

	return template_code


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
		supported_types = TYPES[ISA_table[instr][1]]	# list of instruction supported types

		# For every supported type for the currenct instruction instr (in ISA.py file)
		for typee in supported_types:
			# Generate the code 
			code = generate_code(nb_instr, instr, template_code, typee)
			# Write to file
			f = open(instr+"."+str(typee)+".cu",'w')
			f.write(code)
			f.close()


if __name__ == "__main__":
	main()			
