class ThreeOp(object):
    InstrType = None
    SymtabEntry1 = None
    SymtabEntry2 = None
    SymtabEntry3 = None
    Target = None
    Operator = None
    
class TACList():
    def __init__(self,):
        self.TAC=[]
        self.mile = -1
        self.nextMile = 0
        
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

        if operator == 'goto':
            OpCode.InstrType = "GoTo"
            if len(tmp_list) >0:
                OpCode.Target = tmp_list[0]
        if operator in ['<','>','=>','<=','==','~=']:
            OpCode.InstrType = 'IfElse'
            OpCode.Operator = tmp_list[0]
            OpCode.SymtabEntry1 = tmp_list[1]
            OpCode.SymtabEntry2 = tmp_list[2]

        self.mile += 1
        self.nextMile += 1
        self.TAC.append(OpCode)


    def backpatch(self, PatchList, GodMile):
        for instr in PatchList:
            if instr < self.nextMile and self.TAC[instr].InstrType =='GoTo' or  self.TAC[instr].InstrType =='IfElse':
                self.TAC[instr].Target = GodMile
        
    def print_OpCodes(self):
        for code in self.TAC:
            print vars(code)

    def print_ir_code(self):
        for code in self.TAC:
            if code.Operator in ['+','-','*','/','%','>>','<<','and','or']:
                print str(code.SymtabEntry1)+" = "+str(code.SymtabEntry2)+" "+code.Operator+" "+str(code.SymtabEntry3)

            if code.InstrType == 'Assign':
                print str(code.SymtabEntry1)+" = "+str(code.SymtabEntry2)

            if code.InstrType == 'GoTo':
                print "goto "+str(code.Target)

            if code.Operator in ['<','>','=>','<=','==','~=']:
                print "if "+str(code.SymtabEntry1)+" "+code.Operator+" "+str(code.SymtabEntry2)+" goto "+str(code.Target)
            
