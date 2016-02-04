from DataStruct import *
from GenSym import *
from RegisterFinder import *
#from codeGen import *
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
            L,self.RegDesc,self.AddrDesc = RegFind.getReg(ops,self.RegDesc,self.AddrDesc)
            x,y,z = ops.SymtabEntry1, ops.SymtabEntry2, ops.SymtabEntry3
            try: 
                ydash = AddrDesc[y]
            except:
                if check_variable(y):
                    print "MOV $%d,\%%s"%(y,L)
                else:
                    print "MOV %s,\%%s"%(y,L)
            else:
                if y not in getattr(RegDesc,L):
                    print "MOV \%%s,\%%s"%(ydash,L)

            try:
                zdash=AddrDesc[z]
            except:
                zdash = z;
            gen(ops, zdash, L)
            self.AddrDesc[x] = L
            setattr(self.RegDesc,L,[x])

            if self.nextUse[i][y]==-1:
                try:
                    del self.AddrDesc[y]
                except:
                    pass
            if self.nextUse[i][z]==-1:
                try:
                    del self.AddrDesc[z]
                except:
                    pass


if __name__=='__main__':
    fname = sys.argv[1]
    runner = Runner(fname)
    runner.Run()
    #print vars(runner)
