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

    def inject(self,operator,tmp_list):
        OpCode = ThreeOp()
        if operator in ['+','-','*','/','%','>>','<<','&','|','^^']:
            OpCode.InstrType = "Math"
            OpCode.SymtabEntry1 = tmp_list[0]
            OpCode.SymtabEntry2 = tmp_list[1]
            OpCode.SymtabEntry3 = tmp_list[3]
            OpCode.Operator = tmp_list[2]
        if operator == '=':
            OpCode.InstrType = "Assign"
            OpCode.SymtabEntry1 = tmp_list[0]
            OpCode.SymtabEntry2 = tmp_list[2]
        self.TAC.append(OpCode)
        
    def print_OpCodes(self):
        for code in self.TAC:
            print vars(code)
        
