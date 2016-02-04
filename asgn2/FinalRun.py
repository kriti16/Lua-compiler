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
        x86istr=x86istr+'\n.section .text\nfmtstr:\n  .string "%d\\n"\n\n.globl _start\n\n_start:\n'
        print x86istr

    def footer(self):
        print "MOVL $1,%EAX\nMOVL $0,%EBX\nint $0x80\n"

    def Run(self):	
        RegFind = RegisterFinder(self.deadAlive,self.nextUse)
        i=0;
        for ops in self.list_op_3ops:
            if ops.InstrType=='Print':
                x = ops.SymtabEntry1
                if check_variable(x):
                    print "PUSH $" + x
                else:
                    if self.AddrDesc[x] == None:
                        print "PUSH " + x
                    else:
                        print "PUSH + %" + self.AddrDesc[x]
                print "PUSH $fmtstr"
                print "CALL printf"
                continue
            if ops.Operator == '/':
                L,self.RegDesc,self.AddrDesc = RegFind.divModGetReg(ops,self.RegDesc,self.AddrDesc,i)
            else:
                L,self.RegDesc,self.AddrDesc = RegFind.getReg(ops,self.RegDesc,self.AddrDesc,i)
            x,y,z = ops.SymtabEntry1, ops.SymtabEntry2, ops.SymtabEntry3
            try:
                if self.AddrDesc[y] == None:
                    raise Exception()
                ydash = self.AddrDesc[y]
                #print "Found " + ydash +" for "+y
            except:
                if check_variable(y):
                    print "MOVL $"+y+",%"+L
                else:
                    print "MOVL "+y+",%"+L
            else:
                if self.AddrDesc[y] == 'Spilled':
                        self.AddrDesc[y] = None
                else:
                    if y not in getattr(self.RegDesc,L):
                        print "MOVL %"+ydash+","+L
            zdash=None
            try:
                if self.AddrDesc[z] == None:
                    raise Exception()
                zdash=self.AddrDesc[z]
            except:
                zdash = z;
            if ops.Operator=='/':
                if check_variable(zdash):
                    RegFind.storeMem('ESI',self.RegDesc,self.AddrDesc)
                RegFind.storeMem('EDX',self.RegDesc,self.AddrDesc)
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
            i += 1
if __name__=='__main__':
    fname = sys.argv[1]
    runner = Runner(fname)
    runner.header()
    runner.Run()
    runner.footer()
    #print vars(runner)
