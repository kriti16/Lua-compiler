class ThreeOp(object):
    InstrType = None
    SymtabEntry1 = None
    SymtabEntry2 = None
    SymtabEntry3 = None
    Target = None
    Operator = None
    
class TACList():
    def __init__(self,ST):
        self.TAC={}
        self.mile = -1
        self.nextMile = 0
        self.ST = ST
    
    def inject(self,operator,tmp_list):
        OpCode = ThreeOp()
        if operator in ['+','-','*','/','%','>>','<<','and','or']:
            OpCode.InstrType = "Math"
            OpCode.SymtabEntry1 = tmp_list[0]
            OpCode.SymtabEntry2 = tmp_list[1]
            OpCode.SymtabEntry3 = tmp_list[3]
            OpCode.Operator = tmp_list[2]
        if operator == '=':
            OpCode.InstrType = "Assign"
            OpCode.SymtabEntry1 = tmp_list[0]
            OpCode.SymtabEntry2 = tmp_list[1]
        if operator == 'param':
            OpCode.InstrType = 'param'
            OpCode.SymtabEntry1 = tmp_list[0]
        if operator == 'goto':
            OpCode.InstrType = "GoTo"
            if len(tmp_list) >0:
                OpCode.Target = tmp_list[0]
        if operator in ['<','>','=>','<=','==','~=']:
            OpCode.InstrType = 'IfElse'
            OpCode.Operator = tmp_list[0]
            OpCode.SymtabEntry1 = tmp_list[1]
            OpCode.SymtabEntry2 = tmp_list[2]
        if operator == 'print':
            OpCode.InstrType = 'Print'
            OpCode.SymtabEntry1 = tmp_list[0]
        if operator == 'pop':
            OpCode.InstrType = 'PopVar'
            OpCode.SymtabEntry1 = tmp_list[0]
        if operator == 'prints':
            OpCode.InstrType = 'Prints'
            OpCode.SymtabEntry1 = tmp_list[0]
        if operator == 'printd':
            OpCode.InstrType = 'Printd'
            OpCode.SymtabEntry1 = tmp_list[0]
        if operator == 'Func':
            OpCode.InstrType = 'Func'
            OpCode.SymtabEntry1 = tmp_list[0]
        if operator == 'call':
            OpCode.InstrType = 'FunCall'
            OpCode.SymtabEntry1 = tmp_list[0]
            if len(tmp_list) == 1:
                OpCode.SymtabEntry2 = '_empty'
            else:
                OpCode.SymtabEntry2 = tmp_list[1]
            if len(tmp_list) == 3:
                OpCode.SymtabEntry3 = tmp_list[2]
            else:
                OpCode.SymtabEntry3 = 0
                self.mile += 1
        if operator == 'return':
            OpCode.InstrType = 'Return'
            OpCode.SymtabEntry1 = tmp_list[0]
        self.nextMile += 1
        if self.ST.CurrFunc not in self.TAC.keys(): 
            self.TAC[self.ST.CurrFunc] = []
        self.TAC[self.ST.CurrFunc].append(OpCode)
        #print [vars(x) for x in self.TAC[self.ST.CurrFunc]]
            


    def backpatch(self, PatchList, GodMile):
        for instr in PatchList:
            #print GodMile,PatchList,vars(self.ST.scope[self.ST.CurrFunc]),self.ST.funcList,instr,self.nextMile
            #print len(self.TAC[self.ST.CurrFunc])
            #for funcs in self.ST.funcList:
            #    if funcs != self.ST.CurrFunc:
            #        GodMile += len(self.TAC[funcs])
            #        print GodMile,"Godmile"
            if instr < self.nextMile and (self.TAC[self.ST.CurrFunc][instr].InstrType =='GoTo' or  self.TAC[self.ST.CurrFunc][instr].InstrType =='IfElse') and  self.TAC[self.ST.CurrFunc][instr].Target == None:
                self.TAC[self.ST.CurrFunc][instr].Target = GodMile
       #         print GodMile,"IFFF"
        
    def print_OpCodes(self):
        for code in self.TAC:
            print vars(code)

    def get_mile(self):
        instr = self.nextMile 
        return instr
    
    def print_ir_code(self):
        total_count = 0
        temp_count = 0
        for functions in self.ST.funcList:
            total_count += temp_count
            temp_count = 0
            for code in self.TAC[functions]:
                temp_count += 1
                if code.Operator in ['+','-','*','/','%','>>','<<','and','or']:
                    print str(code.SymtabEntry1)+" = "+str(code.SymtabEntry2)+" "+code.Operator+" "+str(code.SymtabEntry3)
                if code.InstrType == 'Func':
                    print 'fun '+code.SymtabEntry1
                if code.InstrType == 'Assign':
                    print str(code.SymtabEntry1)+" = "+str(code.SymtabEntry2)

                if code.InstrType == 'GoTo':
                    try:
                        print "goto "+str(code.Target+total_count)
                    except:
                        print "goto "+str(code.Target)+str(total_count)
                if code.InstrType == 'Return':
                    print "ret "+str(code.SymtabEntry1)
                if code.Operator in ['<','>','=>','<=','==','~=']:
                    print "if "+str(code.SymtabEntry1)+" "+code.Operator+" "+str(code.SymtabEntry2)+" goto "+str(code.Target+total_count)
                if code.InstrType == 'Print':
                    print "print "+str(code.SymtabEntry1)
                if code.InstrType == 'Prints':
                    print "prints "+str(code.SymtabEntry1)
                if code.InstrType == 'Printd':
                    print "printd "+str(code.SymtabEntry1)
                if code.InstrType == 'FunCall':
                    print code.SymtabEntry2+" = call "+str(code.SymtabEntry1)+" "+str(code.SymtabEntry3)
                if code.InstrType == 'param':
                    print "param "+code.SymtabEntry1
                if code.InstrType == 'PopVar':
                    print "popVar "+code.SymtabEntry1.Locate
