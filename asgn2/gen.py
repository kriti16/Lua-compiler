from helperScripts import *
from DataStruct import *

def symbol(op):
	if op=='+':
		return "ADDL"
	elif op=='-':
		return "SUBL"
	elif op=='*':
		return "IMULL"
	elif op=='/':
		return "IDIVL"

def gen(ops,zdash,L):
	opr=symbol(ops.Operator)
	if opr!="IDIVL":
		if check_variable(zdash):
			print "\t"+opr+" $"+str(zdash)+",%"+L
		elif zdash==ops.SymtabEntry3:
			print "\t"+opr+" "+zdash+",%"+L
		else:
			print "\t"+opr+" %"+zdash+",%"+L
	else:
		print "MOVL $0,%EDX"
		if check_variable(ops.SymtabEntry3):
			print "\t"+opr+" %ESI"
		elif ops.SymtabEntry3==zdash:
			print "\t"+opr+" "+zdash
		else:
			print "\t"+opr+" %"+zdash
		
if __name__=='__main__':
    op=ThreeOp()
    op.SymtabEntry3='z'
    op.Operator='/'
    gen(op,'EBX','EAX')
