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
        print "\n\tMOVL $1,%EAX\n\tMOVL $0,%EBX\nint $0x80\n"
        
    def endBlock(self):
        '''
        Pushing all variables that are still present
        in the Addr Descriptor to memory.
        However Not deleting their register values'''
        for var in self.AddrDesc.keys():
            if self.AddrDesc[var] != None:
                print '\tMOVL %'+self.AddrDesc[var]+","+var
    def Run(self):	
        RegFind = RegisterFinder(self.deadAlive,self.nextUse)
        i=0;
        #print [vars(x) for x in self.list_op_3ops]
        print self.leaders.keys()
        for ops in self.list_op_3ops:
            print i#,vars(ops)
            if str(i) in self.leaders.keys():
                print "LEE"+str(self.leaders[str(i)])+":"
                
                
            if ops.InstrType == 'IfElse':
                self.endBlock()
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
                        self.AddrDesc[x]=R
                        setattr(self.RegDesc,R,x)
                    else:
                        print "\tMOVL "+Entry1+",%"+R
                        self.AddrDesc[Entry1]=R                        
                        setattr(self.RegDesc,R,Entry1)
                try:
                    if self.AddrDesc[Entry2]==None:
                        raise Exception()
                    regY = self.AddrDesc[Entry2]
                except:
                    R,self.RegDesc,self.AddrDesc=RegFind.getRegE(Entry1,self.RegDesc,self.AddrDesc,i)
                    regY = R
                    if check_variable(Entry2):
                         print "\tMOVL $"+Entry2 +",%"+R
                         self.AddrDesc[Entry2]=R
                         setattr(self.RegDesc,R,Entry2)
                    else:
                        print "\tMOVL "+Entry2 +",%"+R
                        self.AddrDesc[Entry2]=R                        
                        setattr(self.RegDesc,R,Entry2)
                print "\tCMP %"+regX+",%"+regY
                opr = ops.Operator
                tgt = ops.Target
                if opr == '==':
                    print "\tJE "+"LEE"+str(self.leaders[tgt])
                elif opr == '<':
                    print "\tJL "+"LEE"+str(self.leaders[tgt])
                elif opr == '<=':
                    print "\tJLE "+"LEE"+str(self.leaders[tgt])
                elif opr == '>':
                    print "\tJG "+"LEE"+str(self.leaders[tgt])
                elif opr == '>=':
                    print "\tJGE "+"LEE"+str(self.leaders[tgt])
                elif opr == '~=':
                    print "\tJNE "+"LEE"+str(self.leaders[tgt])
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
