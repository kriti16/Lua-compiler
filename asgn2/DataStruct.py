class ThreeOp(object):
    InstrType = None
    SymtabEntry1 = None
    SymtabEntry2 = None
    SymtabEntry3 = None
    Target = None
    Operator = None
class Register(object):
    EAX = []
    EBX = []
    ECX = []
    EDX = []
    ESI  = []
    EDI  = []
    EBP = []
    EIP = []
    ESP = []
    def __init__(self):
         self.EAX = []
         self.EBX = []
         self.ECX = []
         self.EDX = []
         self.ESI  = []
         self.EDI  = []
         self.EBP = []
         self.EIP = []
         self.ESP = []
