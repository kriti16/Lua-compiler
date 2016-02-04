#!/usr/bin/python
import ply.lex as lex
import numpy as np
import sys
from ThreeOp import ThreeOp
from pprint import pprint
from helperScripts import *
class GenSym(object):
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
                next_use={}
                for i in range(0,self.lines):
                        TOC = self.list_of_3op[i]
                        if not check_variable(TOC.SymtabEntry2):
                                dict_perm[TOC.SymtabEntry2] = 0
                                next_use[TOC.SymtabEntry2] = -1
                        if not check_variable(TOC.SymtabEntry3):
                                dict_perm[TOC.SymtabEntry3] = 0
                                next_use[TOC.SymtabEntry3] = -1
                        if not check_variable(TOC.SymtabEntry1):
                                dict_perm[TOC.SymtabEntry1] = 0
                                next_use[TOC.SymtabEntry1] = -1
                #print dict_perm
                for i in range(self.lines-1,-1,-1):
                        TOC = self.list_of_3op[i]
                        dict_dead={}
                        dict_next={}
                        try:
                                dict_dead[TOC.SymtabEntry2] = dict_perm[TOC.SymtabEntry2]
                                dict_next[TOC.SymtabEntry2] = next_use[TOC.SymtabEntry2]
                                dict_perm[TOC.SymtabEntry2]=1
                                next_use[TOC.SymtabEntry2]=i+1
                        except:
                                pass
                        
                        try:
                                dict_dead[TOC.SymtabEntry3]=dict_perm[TOC.SymtabEntry3]
                                dict_next[TOC.SymtabEntry3]=next_use[TOC.SymtabEntry3]
                                dict_perm[TOC.SymtabEntry3]=1
                                next_use[TOC.SymtabEntry3]=i+1
                        except:
                                pass
                        try:
                                dict_dead[TOC.SymtabEntry1]=dict_perm[TOC.SymtabEntry1]
                                dict_next[TOC.SymtabEntry1]=next_use[TOC.SymtabEntry1]
                                dict_perm[TOC.SymtabEntry1]=0
                                next_use[TOC.SymtabEntry1]=-1
                        except:
                                pass
                        self.deadAlive.insert(0,dict_dead)
                        self.nextUse.insert(0,dict_next)
                                                

if __name__=='__main__':
        fname = sys.argv[1]
        Gensym = GenSym()
        Gensym.read(fname)
        list_op_3ops = Gensym.list_of_3op
        Gensym.genSymTable()
        pprint ([x for x in Gensym.deadAlive])
        print
        pprint ([x for x in Gensym.nextUse])





