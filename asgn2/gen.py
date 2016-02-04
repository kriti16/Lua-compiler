from helperScripts import *
from DataStruct import *

def symbol(op):
	if op=='+':
		return "ADDL"
	elif op=='-':
		return "SUBL"
	elif op=='*':
		return "IMUL"
	elif op=='/':
		return "IDIV"

def gen(ops,zdash,L):
	opr=symbol(ops.Operator)
	if opr!="IDIV":
		if check_variable(zdash):
			print opr+" $"+str(zdash)+",%"+L
		elif zdash==ops.SymtabEntry3:
			print opr+" "+zdash+",%"+L
		else:
			print opr+" %"+zdash+",%"+L
	else:
		if check_variable(zdash):
			print "MOVL $"+str(zdash)+",%ESI"
			print "IDIV %ESI"
		elif zdash==ops.SymtabEntry3:
			print opr+" "+zdash
		else:
			print opr+" %"+zdash

op=ThreeOp()
op.SymtabEntry3='z'
op.Operator='/'
gen(op,'EBX','EAX')
