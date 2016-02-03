#!/usr/bin/python
import ply.lex as lex
import numpy as np
import sys
from ThreeOp import ThreeOp
from pprint import pprint
class Reader(object):
        def __init__(self,):
                self.list_of_3op = []
                self.deadAlive = []
                self.nextUse = []
                
                self.lines = 0
        def read(self,fname):
                #fname=sys.argv[1]
                #Read the File
                #print fname
                f = open(fname,'r')
                data = f.read()
                f.close()
                input_lines=data.split("\n")
                #print input_lines
                for i in range(0,len(input_lines)):
	                tmp_list=input_lines[i].split(",")
                        OpCode = ThreeOp()
                        OpCode.InstrType = "Math"
                        OpCode.SymtabEntry1 = tmp_list[0]
                        OpCode.SymtabEntry2 = tmp_list[2]
                        OpCode.SymtabEntry3 = tmp_list[4]
                        OpCode.Operator = tmp_list[3]
	                self.list_of_3op.append(OpCode)
                        self.lines += 1
                #pprint ([vars(x) for x in self.list_of_3op])
        def genSymTable(self):
                dict_perm={}
                for i in range(0,self.lines):
                        TOC = self.list_of_3op[i]
                        dict_perm[TOC.SymtabEntry2] = 0
                        dict_perm[TOC.SymtabEntry3] = 0
                        dict_perm[TOC.SymtabEntry1] = 0
                #print dict_perm
                for i in range(self.lines-1,-1,-1):
                        TOC = self.list_of_3op[i]
                        dict_dead = {TOC.SymtabEntry2:dict_perm[TOC.SymtabEntry2],TOC.SymtabEntry3:dict_perm[TOC.SymtabEntry3],TOC.SymtabEntry1:dict_perm[TOC.SymtabEntry1]}
                        self.deadAlive.insert(0,dict_dead)
                        #print TOC.SymtabEntry1,dict_perm['z']
                        dict_perm[TOC.SymtabEntry1]=0
                        dict_perm[TOC.SymtabEntry2]=1
                        #print TOC.SymtabEntry2, TOC.SymtabEntry3, TOC.SymtabEntry1
                        dict_perm[TOC.SymtabEntry3]=1
                        #print len(self.deadAlive),i
                        #print self.deadAlive[0] 
                                                
if __name__=='__main__':
        fname = sys.argv[1]
        Reader = Reader()
        Reader.read(fname)
        list_op_3ops = Reader.list_of_3op
        Reader.genSymTable()
        pprint ([x for x in Reader.deadAlive])





