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
        pprint ([x for x in Gensym.deadAlive])
        print
        pprint ([x for x in Gensym.nextUse])
        print Gensym.AddrDesc
        ##########################################

    def Run(self):
	
        RegFind = RegisterFinder(self.deadAlive,self.nextUse)
        i=0;
        for ops in self.list_op_3ops:
            L,self.RegDesc,self.AddrDesc = RegFind.getReg(ops,self.RegDesc,self.AddrDesc,i)
            x,y,z = ops.SymtabEntry1, ops.SymtabEntry2, ops.SymtabEntry3
            try:
                if self.AddrDesc[y] == None:
                    raise Exception()
                ydash = self.AddrDesc[y]
                #print "Found " + ydash +" for "+y
            except:
                if check_variable(y):
                    print "MOV $"+y+",%"+L
                else:
                    print "MOV "+y+",%"+L
            else:
                if self.AddrDesc[y] == 'Spilled':
                        self.AddrDesc[y] = None
                else:
                    if y not in getattr(self.RegDesc,L):
                        print "MOV1 %"+ydash+","+L
            zdash=None
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
            i += 1
if __name__=='__main__':
    fname = sys.argv[1]
    runner = Runner(fname)
    runner.Run()
    #print vars(runner)
