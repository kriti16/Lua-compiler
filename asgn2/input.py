#!/usr/bin/python
import ply.lex as lex
import numpy as np
import sys

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
	list_of_3ac.append(tmp_list)

print list_of_3ac






