from ISA import *
import sys


def generate_code(nb_instr, instr, template_code):
	instr_type = TYPES[ISA_table[instr][1]][0]
	source_width = int(instr_type[1:])
	source_s_u = instr_type[:1]
	dest_width = source_width*ISA_table[instr][2]
	assert dest_width <= 64
	instr_nb_source_operands = ISA_table[instr][0]-1
	generated_instr_code = "\tasm volatile(\".reg ."+source_s_u+str(dest_width)+" %r12;\\n\"\n"

	for i in range(instr_nb_source_operands):
		 generated_instr_code += "\t\t\t\".reg ."+source_s_u+str(source_width)+" %r"+str(13+i)+";\\n\"\n"

	for i in range(nb_instr):
		
		generated_instr_code += "\t\t\t\""+instr+"."+source_s_u+str(source_width)+" %r12, "
		instr_operands = ""
		for j in range(instr_nb_source_operands):
			instr_operands += "%r"+str(13+j)+", "
		instr_operands = instr_operands[:-2]+";\\n\"\n"
		generated_instr_code += instr_operands
	generated_instr_code += ");\n"
	template_code = template_code.replace("INSERT_CODE_HERE", generated_instr_code)
	return template_code


def main():
	nb_instr = int(sys.argv[1])	#Number of instructions in the code
	f = open("template.tmp",'r')
	template_code  = f.read()
	f.close()
	for i in ISA_table:
		code = generate_code(nb_instr, i, template_code)
		f = open(i+".cu",'w')
		f.write(code)
		f.close()

if __name__ == "__main__":
	main()			
