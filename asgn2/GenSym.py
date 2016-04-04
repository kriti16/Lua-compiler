#!/usr/bin/python
import ply.lex as lex
import numpy as np
import sys
from DataStruct import ThreeOp
from pprint import pprint
from helperScripts import *
class GenSym(object):
        def __init__(self,):
                self.list_of_3op = []
                self.deadAlive = []
                self.nextUse = []
                self.AddrDesc = {}
                self.AddrMem = {}
                self.ArrayDesc ={}
                self.lines = 0
                self.leaders = {str(0):1}
        def read(self,fname):
                f = open(fname,'r')
                data = f.read()
                f.close()
                input_lines=data.split("\n")
                #print input_lines
                for i in range(0,len(input_lines)):
	                tmp_list=input_lines[i].split(" ")
                        #print tmp_list
                        OpCode = ThreeOp()
                        if tmp_list[0] == 'array':
                                OpCode.InstrType = "Array"
                                arr_list = tmp_list[1].split('[')
                                OpCode.SymtabEntry1 = arr_list[0]
#                                print arr_list[1].split(']')[0]
                                OpCode.SymtabEntry2 = arr_list[1].split(']')[0]
                        elif tmp_list[0] == 'fun':
                                OpCode.InstrType = "Func"
                                OpCode.SymtabEntry1 = tmp_list[1]
                        elif tmp_list[0] == 'scanf':
                                OpCode.InstrType = 'Scan'
                                OpCode.SymtabEntry2 = tmp_list[1]
                        elif tmp_list[0] == 'ret':
                                OpCode.InstrType = 'Return'
                                OpCode.SymtabEntry1 = tmp_list[1]
                        elif tmp_list[0] == 'goto':
                                OpCode.InstrType = "GoTo"
                                OpCode.Target = tmp_list[1]
                        elif tmp_list[0] == 'if':
                                OpCode.SymtabEntry1 = tmp_list[1]
                                OpCode.Operator = tmp_list[2]
                                OpCode.SymtabEntry2 = tmp_list[3]
                                OpCode.Target = tmp_list[5]
                                OpCode.InstrType = 'IfElse'
                        elif tmp_list[0]=='print':
                                OpCode.InstrType='Print'
                                OpCode.SymtabEntry1 = tmp_list[1]
                        elif len(tmp_list)==3 and tmp_list[1]=='=' and '[' in tmp_list[0] :
                                OpCode.InstrType = "PtrWrite" #B[z] = A
                                arr_var = tmp_list[0].split('[')
                                OpCode.SymtabEntry1 = arr_var[0] #Array name
                                OpCode.SymtabEntry2 = arr_var[1].split(']')[0] #Array Index
                                OpCode.SymtabEntry3 = tmp_list[2] #Value to write
                        elif len(tmp_list)==3 and tmp_list[1]=='=' and ']' in tmp_list[2]:
                                OpCode.InstrType = 'PtrRead' #A = B[z]
                                arr_var = tmp_list[2].split('[')
                                OpCode.SymtabEntry1 = tmp_list[0] #Variable
                                OpCode.SymtabEntry3 = arr_var[0] #Array Name
                                OpCode.SymtabEntry2 = arr_var[1].split(']')[0] #Array Index
                        elif len(tmp_list)==3 and tmp_list[1]=='=':
                                #print "Twent"
                                #print tmp_list
                                OpCode.InstrType = "Assign"
                                OpCode.SymtabEntry1 = tmp_list[0]
                                OpCode.SymtabEntry2 = tmp_list[2]
                        elif tmp_list[3] in ['+','-','*','/','%','>>','<<','&','|','^^']:
                                #print "Third"
                                #print tmp_list
                                OpCode.InstrType = "Math"
                                OpCode.SymtabEntry1 = tmp_list[0]
                                OpCode.SymtabEntry2 = tmp_list[2]
                                OpCode.SymtabEntry3 = tmp_list[4]
                                OpCode.Operator = tmp_list[3]
                                #print tmp_list
                        elif tmp_list[3] in ['<','>','==','<=','>=','~=']:
                         	OpCode.InstrType = "Compare"
                         	OpCode.SymtabEntry1 = tmp_list[0]
                         	OpCode.SymtabEntry2 = tmp_list[2]
                         	OpCode.SymtabEntry3 = tmp_list[4]
                         	OpCode.Operator = tmp_list[3]
                        elif tmp_list[3] in ['and','or']:
                                OpCode.InstrType = "Logical"
                                OpCode.SymtabEntry1 = tmp_list[0]
                                OpCode.SymtabEntry2 = tmp_list[2]
                                OpCode.SymtabEntry3 = tmp_list[4]
                                OpCode.Operator = tmp_list[3]
                        elif tmp_list[2] == 'call':
                                OpCode.InstrType = 'FunCall'
                                OpCode.SymtabEntry1 = tmp_list[3]
                                OpCode.SymtabEntry2 = tmp_list[0]
                                #print OpCode.InstrType,len(tmp_list),tmp_list
                        elif tmp_list[0] == 'array':
                                OpCode.InstrType = "Array"
                                arr_list = tmp_list[1].split('[')
                                OpCode.SymtabEntry1 = arr_list[0]
#                                print arr_list[1].split(']')[0]
                                OpCode.SymtabEntry2 = arr_list[1].split(']')[0]

	                self.list_of_3op.append(OpCode)
                        self.lines += 1
                        #print [vars(x) for x in  self.list_of_3op]
                #pprint ([vars(x) for x in self.list_of_3op])
        def genSymTable(self):
                dict_perm={}
                next_use={}
                leader_count = 2
                #print self.leaders
                for i in range(0,self.lines):
                        TOC = self.list_of_3op[i]
                        #print vars(TOC)
                        if TOC.InstrType == 'Array':
                                self.ArrayDesc[TOC.SymtabEntry1] = TOC.SymtabEntry2
                                continue
                        if TOC.InstrType == 'GoTo':
                                self.leaders[str(i+1)]=leader_count
                                leader_count += 1
                                self.leaders[TOC.Target]=leader_count
                                leader_count += 1
                                continue
                                #print "b",self.leaders
                        if TOC.InstrType == 'FunCall':
                                self.leaders[str(i+1)] = leader_count
                                #print vars(TOC),i+1
                                leader_count += 1
                                #print "e",self.leaders
                        if TOC.InstrType == 'IfElse':
                                self.leaders[str(i+1)]=leader_count
                                leader_count += 1
                                self.leaders[TOC.Target]=leader_count
                                leader_count += 1
                                #print "a",self.leaders
                        if TOC.InstrType == 'Func':
                                self.leaders[str(i)] = leader_count
                                leader_count += 1
                                #print "c",self.leaders
                                continue
                        if TOC.InstrType == 'Print' or TOC.InstrType == 'Return':
                                continue
                        if TOC.InstrType == 'PtrRead':
                                dict_perm[TOC.SymtabEntry1] = 1
                                next_use[TOC.SymtabEntry1] = self.lines-1
                                self.AddrDesc[TOC.SymtabEntry1] = None
                                self.AddrMem[TOC.SymtabEntry1] = None
                                continue
                        if TOC.InstrType == 'PtrWrite':
                                dict_perm[TOC.SymtabEntry3] = 1
                                next_use[TOC.SymtabEntry3] = self.lines-1
                                self.AddrDesc[TOC.SymtabEntry3] = None
                                self.AddrMem[TOC.SymtabEntry3] = None
                                continue
                        if not check_variable(TOC.SymtabEntry2) :
                                dict_perm[TOC.SymtabEntry2] = 1
                                next_use[TOC.SymtabEntry2] = self.lines-1
                                self.AddrDesc[TOC.SymtabEntry2] = None
                                self.AddrMem[TOC.SymtabEntry2] = None
                        
                        if TOC.InstrType != 'Scan' and not check_variable(TOC.SymtabEntry1) and TOC.InstrType != 'FunCall' :
                                dict_perm[TOC.SymtabEntry1] = 1
                                next_use[TOC.SymtabEntry1] = self.lines-1
                                self.AddrDesc[TOC.SymtabEntry1] = None
                                self.AddrMem[TOC.SymtabEntry2] = None
                        if TOC.InstrType != 'Assign' and TOC.InstrType != 'IfElse' and TOC.InstrType != 'FunCall' and TOC.InstrType != 'Scan':
                                if not check_variable(TOC.SymtabEntry3):
                                        dict_perm[TOC.SymtabEntry3] = 1
                                        next_use[TOC.SymtabEntry3] = self.lines-1
                                        self.AddrDesc[TOC.SymtabEntry3] = None
                                        self.AddrMem[TOC.SymtabEntry3] = None
                        
                #print dict_perm
                for i in range(self.lines-1,-1,-1):
                        TOC = self.list_of_3op[i]
                        #If end of block make all variables' next use on
                        if TOC.InstrType == 'GoTo':
                                self.deadAlive.insert(0,{})
                                self.nextUse.insert(0,{})
                                continue
                        elif TOC.InstrType == 'Print' or TOC.InstrType == 'Return':
                                dict_dead = {}
                                dict_next = {}
                                
                                try:
                                        if check_variable(TOC.SymtabEntry1):
                                                raise Exception()
                                        dict_dead[TOC.SymtabEntry1]=dict_perm[TOC.SymtabEntry1]
                                        dict_next[TOC.SymtabEntry1]=next_use[TOC.SymtabEntry1]
                                except:
                                        pass
                                try:
                                        dict_perm[TOC.SymtabEntry1]=1
                                        next_use[TOC.SymtabEntry1]=i+1
                                except:
                                        pass
                                
                                self.deadAlive.insert(0,dict_dead)
                                self.nextUse.insert(0,dict_next)
                                continue
                        #print dict_perm
                        elif TOC.InstrType == 'IfElse':
                                dict_next = {}
                                dict_dead = {}
                                
                                try:
                                        if check_variable(TOC.SymtabEntry1)  :
                                                raise Exception()
                                        dict_dead[TOC.SymtabEntry1]=dict_perm[TOC.SymtabEntry1]
                                        dict_next[TOC.SymtabEntry1]=next_use[TOC.SymtabEntry1]

                                except:
                                        pass
                                
                                try:
                                        if check_variable(TOC.SymtabEntry2):
                                                raise Exception()
                                        dict_dead[TOC.SymtabEntry2]=dict_perm[TOC.SymtabEntry2]
                                        dict_next[TOC.SymtabEntry2]=next_use[TOC.SymtabEntry2]
                                except:
                                        pass
                                
                                
                                try:
                                        if check_variable(TOC.SymtabEntry1):
                                                raise Exception()
                                        dict_perm[TOC.SymtabEntry1]=1
                                        next_use[TOC.SymtabEntry1]=i+1
                                        
                                except:
                                        pass
                                
                                try:
                                        if   check_variable(TOC.SymtabEntry2):
                                                raise Exception()
                                       
                                        dict_perm[TOC.SymtabEntry2]=1
                                        next_use[TOC.SymtabEntry2]=i+1
                                except:
                                        pass
                                

                                
                                self.deadAlive.insert(0,dict_dead)
                                self.nextUse.insert(0,dict_next)
                                continue
                        
                        dict_dead={}
                        dict_next={}
                        try:
                                if check_variable(TOC.SymtabEntry1):
                                        raise Exception()
                                dict_dead[TOC.SymtabEntry1]=dict_perm[TOC.SymtabEntry1]
                                dict_next[TOC.SymtabEntry1]=next_use[TOC.SymtabEntry1]
                                #print "^^^^^^^^^^^^^^^^^^^^^^^^"
                                #print dict_next
                                #print "^^^^^^^^^^^^^^^^^^^^^^^^^^^^"
                        except:
                                pass
                        
                        try:
                                if check_variable(TOC.SymtabEntry2):
                                        raise Exception()
                                dict_dead[TOC.SymtabEntry2] = dict_perm[TOC.SymtabEntry2]
                                dict_next[TOC.SymtabEntry2] = next_use[TOC.SymtabEntry2]
                       #         print 'a',i,vars(TOC)
                       #         print  next_use[TOC.SymtabEntry2], TOC.SymtabEntry2
                        except:
                                pass
                        
                        try:
                                if check_variable(TOC.SymtabEntry3):
                                        raise Exception()
                                dict_dead[TOC.SymtabEntry3]=dict_perm[TOC.SymtabEntry3]
                                dict_next[TOC.SymtabEntry3]=next_use[TOC.SymtabEntry3]
                        #        print 'b',i,vars(TOC)
                        #        print next_use[TOC.SymtabEntry3], TOC.SymtabEntry3
                        except:
                                pass
                        ##################Updates############################
                        try:
                                dict_perm[TOC.SymtabEntry1]=0
                                next_use[TOC.SymtabEntry1]=-1
                        except:
                                pass
                        
                        try:
                                dict_perm[TOC.SymtabEntry2]=1
                                next_use[TOC.SymtabEntry2]=i+1
                        except:
                                pass
                        
                        try:
                                dict_perm[TOC.SymtabEntry3]=1
                                next_use[TOC.SymtabEntry3]=i+1
                        except:
                                pass
                        #print "&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&"
                        #print dict_dead,dict_next
                        #print self.AddrDesc
                        self.deadAlive.insert(0,dict_dead)
                        self.nextUse.insert(0,dict_next)
                for keysd in self.nextUse[-1].keys():
                        self.nextUse[-1][keysd]=self.lines-1
                #print self.nextUse
if __name__=='__main__':
        fname = sys.argv[1]
        Gensym = GenSym()
        Gensym.read(fname)
        list_op_3ops = Gensym.list_of_3op
        Gensym.genSymTable()
        #pprint ([x for x in Gensym.deadAlive])
        #print
        #pprint ([x for x in Gensym.nextUse])
        #print Gensym.AddrDesc




