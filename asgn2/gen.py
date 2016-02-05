from helperScripts import *
from DataStruct import *

math_symbol={"+":"ADDL","-":"SUBL","*":"IMULL","/":"IDIVL"}
cmp_symbol={">":("CMOVG",'CMOVLE'),"<":("CMOVL","CMOVGE"),">=":("CMOVGE","CMOVL"),"<=":("CMOVLE","CMOVG"),"==":("CMOVE","CMOVNE"),"~=":("CMOVNE","CMOVE")}
def gen(ops,zdash,L):
	if ops.InstrType=="Math":
		opr=math_symbol[ops.Operator]
		if opr!="IDIVL":
			if check_variable(zdash):
				print "\t"+opr+" $"+str(zdash)+",%"+L
			elif zdash==ops.SymtabEntry3:
				print "\t"+opr+" "+zdash+",%"+L
			else:
				print "\t"+opr+" %"+zdash+",%"+L
		else:
			print "\tMOVL $0,%EDX"
			if check_variable(ops.SymtabEntry3):
				print "\t"+opr+" %ESI"
			elif ops.SymtabEntry3==zdash:
				print "\t"+opr+" "+zdash
			else:
				print "\t"+opr+" %"+zdash

	elif ops.InstrType=="Compare":
		opr=cmp_symbol[ops.Operator]
		z=ops.SymtabEntry3
		if check_variable(z):
			print "\t+CMPL $"+str(z)+",%"+L
			print "\t"+opr[0]+" $1,%"+L
			print "\t"+opr[1]+" $0,%"+L
		elif zdash==ops.SymtabEntry3:
			print "\tCMPL "+zdash+",%"+L
			print "\t"+opr[0]+" $1,%"+L
			print "\t"+opr[1]+" $0,%"+L 
		else:
			print "\tCMPL %"+zdash+",%"+L
			print "\t"+opr[0]+" $1,%"+L
			print "\t"+opr[1]+" $0,%"+L
		
if __name__=='__main__':
    op=ThreeOp()
    op.SymtabEntry3='z'
    op.Operator='/'
    gen(op,'EBX','EAX')
