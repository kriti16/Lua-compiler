#!/usr/bin/python
import ply.lex as lex
import numpy as np
import sys
from ThreeOp import ThreeOp
from pprint import pprint
fname=sys.argv[1]
#Read the File
#print fname
f = open(fname,'r')

list_of_3ac=[]

data = f.read()
#print data

input_lines=data.split("\n")

for i in range(0,len(input_lines)):
	tmp_list=input_lines[i].split(",")
        OpCode = ThreeOp()
        OpCode.InstrType = "Math"
        OpCode.SymtabEntry1 = tmp_list[0]
        OpCode.SymtabEntry2 = tmp_list[2]
        OpCode.SymtabEntry3 = tmp_list[4]
        OpCode.Operator = tmp_list[3]
	list_of_3ac.append(OpCode)

pprint ([vars(x) for x in list_of_3ac])






