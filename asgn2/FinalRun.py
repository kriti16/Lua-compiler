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
        self.AddrDesc = Gensym.AddrDesc
        self.AddrMem = Gensym.AddrMem
        self.leaders = Gensym.leaders
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
        x86istr=x86istr+'\n.section .text\nfmtstr:\n  .asciz "%d\\n"\n\n.globl main\n\nmain:\n'
        print x86istr

    def footer(self):
        print "\n\tMOVL $1,%EAX\nMOVL $0,%EBX\nint $0x80\n"

    def Run(self):	
        RegFind = RegisterFinder(self.deadAlive,self.nextUse)
        i=0;
        #print [vars(x) for x in self.list_op_3ops]
        #print self.leaders.keys()
        for ops in self.list_op_3ops:
            if str(i) in self.leaders.keys():
                print "LEE"+str(self.leaders[str(i)])+":"
            if ops.InstrType == 'IfElse':
                
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
                    print "\tPUSHL " + x
                print "\tPUSHL $fmtstr"
                print "\tCALL printf"
                #print vars(self.RegDesc),self.AddrDesc
                i+= 1
                continue



            if ops.InstrType=='Assign':
                x,y = ops.SymtabEntry1, ops.SymtabEntry2
                try:
                    if self.AddrDesc[y]==None:
                        raise Exception()
                except:
                    R,self.RegDesc,self.AddrDesc=RegFind.getRegE(ops.SymtabEntry2,self.RegDesc,self.AddrDesc,i)
                    if check_variable(y):
                        print "\tMOVL $"+str(y)+",%"+R
                        self.AddrDesc[x]=R
                        setattr(self.RegDesc,R,x)
                        i += 1
                        continue
                    else:
                        print "\tMOVL "+y+",%"+R
                        self.AddrDesc[y]=R                        
                        setattr(self.RegDesc,R,y)
                Rdash=self.AddrDesc[x]=self.AddrDesc[y]
                print Rdash
                tmpVar=getattr(self.RegDesc,Rdash)+x
                setattr(self.RegDesc,Rdash,tmpVar)
                if self.nextUse[i][y]==-1:
                    tmpVar=getattr(self.RegDesc,Rdash).remove(y)
                    setattr(self.RegDesc,Rdash,tmpVar)
                i += 1
                continue



            if ops.Operator == '/':
                L,self.RegDesc,self.AddrDesc = RegFind.divModGetReg(ops.SymtabEntry2,self.RegDesc,self.AddrDesc,i)
            else:
                L,self.RegDesc,self.AddrDesc = RegFind.getReg(ops.SymtabEntry2,self.RegDesc,self.AddrDesc,i)
            x,y,z = ops.SymtabEntry1, ops.SymtabEntry2, ops.SymtabEntry3
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
                if self.AddrDesc[y] == 'Spilled':
                        self.AddrDesc[y] = None
                else:
                    if y not in getattr(self.RegDesc,L):
                        print "\tMOVL %"+ydash+",%"+L
            zdash=None



            if ops.Operator=='/':
                if check_variable(z):
                    RegFind.storeMem('ESI',self.RegDesc,self.AddrDesc)
                    print "\tMOVL $"+str(z)+",%ESI"
                RegFind.storeMem('EDX',self.RegDesc,self.AddrDesc)



            try:
                if self.AddrDesc[z] == None:
                    raise Exception()
                zdash=self.AddrDesc[z]
            except:
                zdash = z;
            gen(ops, zdash, L)
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
            i += 1
if __name__=='__main__':
    fname = sys.argv[1]
    runner = Runner(fname)
    runner.header()
    runner.Run()
    runner.footer()
    #print vars(runner)
