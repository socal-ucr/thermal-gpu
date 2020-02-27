from ISA import *
import sys
import argparse 
from random import random

BASE_REG_NUM = 21
# Main function for code generation, given instr name and type
def generate_code(nb_instr, instr, comp_op, stype, template_code, dtype="", bool_op=""):
	dest_width = 0
	if not dtype == "":
		dest_width = int(dtype[2:])
	
	s_fp = ""
	if "f" in stype :
		s_fp = ".0"
	d_fp = ""
	if "f" in dtype :
		d_fp = ".0"
	
	source_width = int(stype[2:])
	# Register declaration
	# For slct, 1st,2nd,and 3rd operands are the same width as the first instruction type (i.e. dtype)
	# Last operand width size is equal to the second instruction type (i.e. stype)
	if instr == "slct": 
		register_code = "\tasm volatile(\".reg "+dtype+" %r"+str(BASE_REG_NUM)+";\\n\"\n \
				\".reg "+dtype+" %r"+str(BASE_REG_NUM+1)+";\\n\"\n \
				\".reg "+dtype+" %r"+str(BASE_REG_NUM+2)+";\\n\"\n \
				\".reg "+stype+" %r"+str(BASE_REG_NUM+3)+";\\n\"\n \
				\"mov"+dtype+" %r"+str(BASE_REG_NUM)+", "+str(int(1000000*random()) % 2**source_width)+d_fp+";\\n\"\n \
				\"mov"+dtype+" %r"+str(BASE_REG_NUM+1)+", "+str(int(1000000*random()) % 2**source_width)+d_fp+";\\n\"\n \
				\"mov"+dtype+" %r"+str(BASE_REG_NUM+2)+", "+str(int(1000000*random()) % 2**source_width)+d_fp+";\\n\"\n \
				\"mov"+stype+" %r"+str(BASE_REG_NUM+3)+", "+str(int(1000000*random()) % 2**source_width)+s_fp+";\\n\"\n"
				
	else:
		dest_type = dtype
		# For selp, dtype is equal to stype
		if instr == "selp":
			dest_type = stype
		# For setp, dtype is predicate
		elif instr == "setp":
			dest_type = ".pred"
		register_code = "\tasm volatile(\".reg "+dest_type+" %r"+str(BASE_REG_NUM)+";\\n\"\n \
				\".reg "+stype+" %r"+str(BASE_REG_NUM+1)+";\\n\"\n \
				\".reg "+stype+" %r"+str(BASE_REG_NUM+2)+";\\n\"\n \
				\".reg .pred %r"+str(BASE_REG_NUM+3)+";\\n\"\n" 
		d_fp = ""
		if "f" in dest_type :
			d_fp = ".0"
		if not dest_type == ".pred":
			register_code += "\t\t\t\t\"mov"+dest_type+" %r"+str(BASE_REG_NUM)+", "+str(int(1000000*random()) % 2**dest_width)+d_fp+";\\n\"\n"
		register_code += "\t\t\t\t\"mov"+stype+" %r"+str(BASE_REG_NUM+1)+", "+str(int(1000000*random()) % 2**source_width)+s_fp+";\\n\"\n \
				\"mov"+stype+" %r"+str(BASE_REG_NUM+2)+", "+str(int(1000000*random()) % 2**source_width)+s_fp+";\\n\"\n"
	
	register_code += ");\n"
	template_code = template_code.replace("REGISTER_CODE", register_code)
	compute_code = "\tasm volatile(\n";	
	# Generate code to instruction	
	for i in range(nb_instr):
		# Add instruction and the dest register which always is r0
		compute_code += "\t\t\t\""+instr+comp_op+bool_op
		
		#selp and slct have an extra predicate operand (i.e. %r3)
		if instr == "selp" or instr == "slct":
			compute_code += dtype+stype+" %r"+str(BASE_REG_NUM)+", %r"+str(BASE_REG_NUM+1)+", %r"+str(BASE_REG_NUM+2)+", %r"+str(BASE_REG_NUM+3)
		else:	
			compute_code +=	dtype+stype+" %r"+str(BASE_REG_NUM)+", %r"+str(BASE_REG_NUM+1)+", %r"+str(BASE_REG_NUM+2)
		
		compute_code += ";\\n\"\n"

	compute_code += ");\n"
	
	# Put the generated instruction into the template code
	template_code = template_code.replace("COMPUTE_CODE", compute_code)

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
	
	# Make it compilable for GPGPU-SIM	
	if not args.hardware:
		lines = template_code.split("\n")
		template_code = ""
		for i in lines:
			if not "power" in i:
				template_code += i+"\n"

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
