#!/usr/bin/python2
from DataStruct import *
from GenSym import *
from RegisterFinder import *
from gen import *
from helperScripts import *
class Runner(object):
    def __init__(self,fname):
        Gensym = GenSym()
        Gensym.read(fname)
        Gensym.genSymTable()
        self.list_op_3ops = Gensym.list_of_3op
        self.deadAlive = Gensym.deadAlive
        self.nextUse = Gensym.nextUse
        self.RegDesc = Register()
        #print vars(self.RegDesc)
        self.AddrDesc = Gensym.AddrDesc
        self.AddrMem = Gensym.AddrMem
        self.ArrayDesc = Gensym.ArrayDesc
        self.leaders = Gensym.leaders
        self.Sleep = 0
        ###########Printers#####################
        #pprint ([x for x in Gensym.deadAlive])
        #print
        #pprint ([x for x in Gensym.nextUse])
        #print Gensym.AddrDesc
        ##########################################

    def header(self):
        x86istr=".section .data\n"
        for key in self.AddrDesc:
            x86istr=x86istr+key+":\n  .long 0\n"
        #x86istr=x86istr+".section .bss\n"
        for key in self.ArrayDesc:
            x86istr = x86istr +".lcomm\t"+key+", "+str(int(self.ArrayDesc[key])*4)
            #x86istr = x86istr+"\t"+key+":\n  .long 0\n"#+":   "+str(int(self.ArrayDesc[key])*4)+"\n"
        x86istr=x86istr+'\n.section .text\ninptstr:\n  .asciz "%d" \nfmtstr:  .asciz "%d\\n"\n\n .globl main\n\nmain:\n'
        print x86istr

    def footer(self):
        print "\n\tMOVL $1,%EAX\n\tMOVL $0,%EBX\nint $0x80\n"
        
    def endBlock(self,RegFind,regDesc,AddrDesc):
        '''
        Pushing all variables that are still present
        in the Addr Descriptor to memory.
        However Not deleting their register values'''
        for var in AddrDesc.keys():
            if self.AddrDesc[var] != None:
                reg = self.AddrDesc[var]
                regDesc,AddrDesc = RegFind.storeMem(reg,regDesc,AddrDesc)
        return regDesc,AddrDesc

                
    def Run(self):	
        RegFind = RegisterFinder(self.deadAlive,self.nextUse)
        i=0;
        #print [vars(x) for x in self.list_op_3ops]
        #print self.leaders
        for ops in self.list_op_3ops:
            #print i,vars(ops)
            #print vars(self.RegDesc),self.AddrDesc
            if str(i) in self.leaders.keys() and ops.InstrType != 'IfElse' and ops.InstrType != 'FunCall' and ops.InstrType != 'Return' and ops.InstrType != 'GoTo':
                self.endBlock(RegFind,self.RegDesc,self.AddrDesc)
            if str(i) in self.leaders.keys() and ops.InstrType != 'Func' :#and ops.InstrType != 'FunCall':
                self.endBlock(RegFind,self.RegDesc,self.AddrDesc)
                print "LEE"+str(self.leaders[str(i)])+":"#, i,vars(ops)
            if ops.InstrType == 'Array':
                i += 1
                continue
            if ops.InstrType == 'Return':
                RegFind.storeMem('EDX',self.RegDesc,self.AddrDesc)
                if check_variable(ops.SymtabEntry1):
                    print "\tMOVL $"+ops.SymtabEntry1+",%EDX"
                else:
                    if self.AddrDesc[ops.SymtabEntry1] == None:
                        print "\tMOVL "+ops.SymtabEntry1+",%EDX"
                    else:
                        print "\tMOVL %"+self.AddrDesc[ops.SymtabEntry1]+",%EDX"
                i+=1
                self.endBlock(RegFind,self.RegDesc,self.AddrDesc)
                print "\tRET"
                continue
            if ops.InstrType == 'FunCall':
                self.endBlock(RegFind,self.RegDesc,self.AddrDesc)
                print "\tCALL "+ops.SymtabEntry1
                print "\tMOVL %EDX,"+ops.SymtabEntry2
                i += 1
                continue
            if ops.InstrType == 'Func':
                if self.Sleep == 0:
                    self.footer()
                    self.Sleep += 1
                    
                print ops.SymtabEntry1+":"
                i+=1
                continue
            if ops.InstrType == 'IfElse':
                Entry1 = ops.SymtabEntry1
                Entry2 = ops.SymtabEntry2
                regX = regY = None
                try:
                    if self.AddrDesc[Entry1]==None:
                        raise Exception()
                    regX = self.AddrDesc[Entry1]
                except:
                    R,self.RegDesc,self.AddrDesc=RegFind.getRegE(Entry2,self.RegDesc,self.AddrDesc,i)
                    regX = R
                    if check_variable(Entry1):
                        print "\tMOVL $"+str(Entry1)+",%"+R
                    else:
                        print "\tMOVL "+Entry1+",%"+R
                        self.AddrDesc[Entry1]=R                        
                        setattr(self.RegDesc,R,[Entry1])
                try:
                    if self.AddrDesc[Entry2]==None:
                        raise Exception()
                    regY = self.AddrDesc[Entry2]
                except:
                    R,self.RegDesc,self.AddrDesc=RegFind.getRegE(Entry1,self.RegDesc,self.AddrDesc,i)
                    #print vars(self.RegDesc),self.AddrDesc
                    regY = R
                    if check_variable(Entry2):
                        print "\tMOVL $"+Entry2 +",%"+R
                    else:
                        print "\tMOVL "+Entry2 +",%"+R
                        self.AddrDesc[Entry2]=R                        
                        setattr(self.RegDesc,R,Entry2g)
                print "\tCMP %"+regY+",%"+regX
                #print vars(self.RegDesc),self.AddrDesc
                self.endBlock(RegFind,self.RegDesc,self.AddrDesc)
                #print vars(self.RegDesc),self.AddrDesc
                opr = ops.Operator
                tgt = ops.Target
                if opr == '==':
                    print "\tJE "+"LEE"+str(self.leaders[tgt])
                elif opr == '<':
                    print "\tJL "+"LEE"+str(self.leaders[tgt])
                elif opr == '=>':
                    print "\tJGE "+"LEE"+str(self.leaders[tgt])
                elif opr == '>':
                    print "\tJG "+"LEE"+str(self.leaders[tgt])
                elif opr == '<=':
                    print "\tJLE "+"LEE"+str(self.leaders[tgt])
                elif opr == '~=':
                    print "\tJNE "+"LEE"+str(self.leaders[tgt])
                i += 1
                continue


            elif ops.InstrType=='GoTo':
                self.endBlock(RegFind,self.RegDesc,self.AddrDesc)
                print "\tJMP LEE"+str(self.leaders[ops.Target])
                i += 1
                continue
            if ops.InstrType == 'PtrRead':
                #print vars(ops)
                x,y,z = ops.SymtabEntry1, ops.SymtabEntry2,ops.SymtabEntry3 #x = z[y]
                RegFind.storeMem('ECX',self.RegDesc,self.AddrDesc)
                RegFind.storeMem('EDX',self.RegDesc,self.AddrDesc)
                if self.AddrDesc[y] == None:
                    print "\tMOVL "+str(y)+",%ECX"
                elif self.AddrDesc[x] != 'ECX':
                    print "\tMOVL %"+self.AddrDesc[y]+",%ECX"
                if self.AddrDesc[x] == None:
                    print "\tMOVL "+str(x)+",%EDX"
                elif self.AddrDesc[x] != 'EDX':
                    print "\tMOVL %"+self.AddrDesc[x]+",%EDX"
                print "\tMOVL "+z+"(,%ECX,4),%EDX"
                self.AddrDesc[x]='EDX'                        
                setattr(self.RegDesc,'EDX',[x])
                self.AddrDesc[y]='ECX'                        
                setattr(self.RegDesc,'ECX',[y])
                i += 1
                continue
            if ops.InstrType == 'PtrWrite':
                #print vars(ops)
                x,y,z = ops.SymtabEntry1, ops.SymtabEntry2,ops.SymtabEntry3 #z[y] = x
                RegFind.storeMem('ECX',self.RegDesc,self.AddrDesc)
                RegFind.storeMem('EDX',self.RegDesc,self.AddrDesc)
                
                if self.AddrDesc[y] == None:
                    print "\tMOVL "+str(y)+",%ECX"
                elif self.AddrDesc[y] != 'ECX':
                    print "\tMOVL %"+self.AddrDesc[y]+",%ECX"
                if self.AddrDesc[z] == None:
                    print "\tMOVL "+str(z)+",%EDX"
                elif self.AddrDesc[z] != 'EDX':
                    print "\tMOVL %"+self.AddrDesc[z]+",%EDX"
                print "\tMOVL "+"%EDX,"+x+"(,%ECX,4)"
                self.AddrDesc[x]='EDX'                        
                setattr(self.RegDesc,'EDX',[x])
                self.AddrDesc[y]='ECX'                        
                setattr(self.RegDesc,'ECX',[y])
                i += 1
                continue
            if ops.InstrType=='Print':
                x = ops.SymtabEntry1
                if check_variable(x):
                    print "\tPUSHL $" + x
                else:
                    RegFind.storeMem('EAX',self.RegDesc,self.AddrDesc)
                    RegFind.storeMem('EBX',self.RegDesc,self.AddrDesc)
                    RegFind.storeMem('ECX',self.RegDesc,self.AddrDesc)
                    RegFind.storeMem('EDX',self.RegDesc,self.AddrDesc)
                    if self.AddrDesc[x] == None:
                        print "\tPUSHL " + x
                    else:
                        print "\tPUSHL %" + self.AddrDesc[x]
                    print "\tPUSHL $fmtstr"
                print "\tCALL printf"
                print "\tADDL $8, %ESP" 
                #print vars(self.RegDesc),self.AddrDesc
                i+= 1
                continue
            if ops.InstrType=='Scan':
                x = ops.SymtabEntry2
                if check_variable(x):
                    print "\tPUSHL $" + x
                else:
                    RegFind.storeMem('EAX',self.RegDesc,self.AddrDesc)
                    RegFind.storeMem('EBX',self.RegDesc,self.AddrDesc)
                    RegFind.storeMem('ECX',self.RegDesc,self.AddrDesc)
                    RegFind.storeMem('EDX',self.RegDesc,self.AddrDesc)
                    print "\tPUSHL $" + x
                print "\tPUSHL $inptstr"
                print "\tCALL scanf"
                print "\tADDL $8, %ESP" 
                #print vars(self.RegDesc),self.AddrDesc
                i+= 1
                continue
            
            if ops.InstrType=='Assign':
                x,y = ops.SymtabEntry1, ops.SymtabEntry2
                try:
                    if self.AddrDesc[y]==None:
                        raise Exception()
                except:
                #    print vars(self.RegDesc),self.AddrDesc
                    R,self.RegDesc,self.AddrDesc=RegFind.getRegE(ops.SymtabEntry2,self.RegDesc,self.AddrDesc,i)
                    if check_variable(y):
                        print "\tMOVL $"+str(y)+",%"+R
                        i += 1
                        var = getattr(self.RegDesc,R) + [x]
                        setattr(self.RegDesc,R,var)
                        self.AddrDesc[x] = R
                        #print vars(self.RegDesc),self.AddrDesc
                
                        continue
                    else:
                        print "\tMOVL "+y+",%"+R
                        self.AddrDesc[y]=R                        
                        setattr(self.RegDesc,R,[y])

                #print self.AddrDesc[x],self.AddrDesc[y]
                Rdash=self.AddrDesc[x]=self.AddrDesc[y]
                tmpVar=getattr(self.RegDesc,Rdash)+[x]
                #print tmpVar,Rdash
                setattr(self.RegDesc,Rdash,tmpVar)
                #print self.nextUse[i+1],self.nextUse[i],y
                if self.nextUse[i][y]==-1:
                    #print tmpVar,y,getattr(self.RegDesc,Rdash)
                    tmpVar=getattr(self.RegDesc,Rdash)
                    #print "###############################"
                    tmpVar.remove(y)
                    if tmpVar == None:
                        tmpVar = [] 
                    setattr(self.RegDesc,Rdash,tmpVar)
                    #print getattr(self.RegDesc,Rdash)
                    try:
                        if check_variable(y):
                            raise Exception()
                        self.AddrDesc[y] = None
                    except:
                        pass
                i += 1
                #print vars(self.RegDesc),self.AddrDesc
                continue

            x,y,z = ops.SymtabEntry1, ops.SymtabEntry2, ops.SymtabEntry3

            if ops.Operator == '/' or ops.Operator=='%':
                L,self.RegDesc,self.AddrDesc = RegFind.divModGetReg(ops.SymtabEntry2,self.RegDesc,self.AddrDesc,i)
            else:
                if ops.Operator in ['<<','>>']:
                    if not check_variable(z):
                        zdash,self.RegDesc,self.AddrDesc = RegFind.shiftGetReg(ops.SymtabEntry3,self.RegDesc,self.AddrDesc,i)
                L,self.RegDesc,self.AddrDesc = RegFind.getReg(ops.SymtabEntry2,self.RegDesc,self.AddrDesc,i)
            try:
                if self.AddrDesc[y] == None:
                    raise Exception()
                ydash = self.AddrDesc[y]
                #print "Found " + ydash +" for "+y
            except:
                if check_variable(y):
                    print "\tMOVL $"+y+",%"+L
                else:
                    print "\tMOVL "+y+",%"+L
            else:
                if y not in getattr(self.RegDesc,L):
                    print "\tMOVL %"+ydash+",%"+L
            
            zdash=None
            if ops.InstrType=='Compare':
                RegFind.storeMem('EAX',self.RegDesc,self.AddrDesc)
            
            if ops.Operator=='/' or ops.Operator=='%':
                if check_variable(z):
                    RegFind.storeMem('ESI',self.RegDesc,self.AddrDesc)
                    print "\tMOVL $"+str(z)+",%ESI"
                RegFind.storeMem('EDX',self.RegDesc,self.AddrDesc)        

            try:
                if self.AddrDesc[z] == None:
                    raise Exception()
                zdash=self.AddrDesc[z]
                #print zdash
                #print "z:"+z+" x:"+x
                if z==x:
                    #print "hi"
                    tempVar=getattr(self.RegDesc,zdash)
                    tmpVar.remove(z)
                    #print "hi"+tempVar
                    if tempVar==None:
                        setattr(self.RegDesc,zdash,[])
                    else:
                        setattr(self.RegDesc,zdash,tempVar)    
                    #print "hi"                
            except:
                zdash = z;
            #print vars(ops),zdash,L,z,x
            gen(ops, zdash, L,i)
            self.AddrDesc[x] = L
            setattr(self.RegDesc,L,[x])
            try:
                if self.nextUse[i][y]==-1:
                    self.AddrDesc[y] = None
            except:
                pass


            try:
                if self.nextUse[i][z]==-1:
                    self.AddrDesc[z] = None
            except:
                pass
            #print vars(self.RegDesc),self.AddrDesc
            #print vars(ops),i
            i += 1
if __name__=='__main__':
    fname = sys.argv[1]
    runner = Runner(fname)
    runner.header()
    runner.Run()
    if runner.Sleep == 0:
        runner.footer()
    #print runner.leaders
    #runner.footer()
    #print vars(runner)
