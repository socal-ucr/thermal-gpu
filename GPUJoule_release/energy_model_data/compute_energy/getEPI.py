#!/usr/bin/python3

import sys

#print ('Number of arguments:', len(sys.argv), 'arguments.')
#print ('Argument List:', str(sys.argv))

FilePath = sys.argv[1]
Unroll = int(sys.argv[2])
Iterations = int(sys.argv[3])
NumCTA = int(sys.argv[4])
NumThread = int(sys.argv[5])
WarpSize = int(sys.argv[6])
IdlePower = int(sys.argv[7])

TotalInstructions = Unroll * Iterations * NumCTA * NumThread / WarpSize;
#print("Total Warp Instruction count: ", TotalInstructions)

InputFile = open(FilePath,'r')
Power = int(InputFile.readline().split(",")[1])
Time = float(InputFile.readline().split(",")[1])
Energy = (Power-IdlePower)/1000.0 * Time/1000.0
#print("Power (mW): ", Power, " Time (ms): ", Time, " Energy (J): ", Energy)

EPI = Energy / TotalInstructions
# print("EPI: ",EPI)
print(FilePath.split("_1000000")[0],",",EPI)

