from DataStruct import *
from GenSym import *
from RegisterFinder import *
from codeGen import *
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
        ###########Printers#####################
        pprint ([x for x in Gensym.deadAlive])
        print
        pprint ([x for x in Gensym.nextUse])
        print Gensym.AddrDesc
        ##########################################

    def Run(self):
        RegFind = RegisterFinder(self.deadAlive,self.nextUse)
        for ops in self.list_op_3ops:
            x = RegFind.getReg(ops,self.RegDesc,self.AddrDesc)
            print x
if __name__=='__main__':
    fname = sys.argv[1]
    runner = Runner(fname)
    runner.Run()
    #print vars(runner)
