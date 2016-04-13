.section .data
t4:
  .long 0
t2:
  .long 0
t3:
  .long 0
t0:
  .long 0
t1:
  .long 0
_empty_:
  .long 0

.section .text
inptstr:
  .asciz "%d" 
fmtstr:  .asciz "%d\n" 
strfmt:  .asciz "%s\n"

 .globl main

main:

LEE1:
	MOVL $2,%EAX
	MOVL %EAX,t0
	PUSHL t0
	PUSHL $fmtstr
	CALL printf
	ADDL $8, %ESP
	CALL g1
	MOVL %EAX,t3
	ADDL $0, %ESP
	MOVL t3,%EAX
	MOVL %EAX,t3
	MOVL %EAX,t4
	PUSHL t4
	PUSHL $fmtstr
	CALL printf
	ADDL $8, %ESP
	MOVL $0,%EAX
	MOVL %EAX,_empty_

	MOVL $1,%EAX
	MOVL $0,%EBX
int $0x80

f1:
	MOVL $222,%EAX
	MOVL $3333,%EBX
	MOVL %EAX,t0
	MOVL %EBX,t1
	PUSHL t1
	PUSHL $fmtstr
	CALL printf
	ADDL $8, %ESP
	PUSHL t0
	PUSHL $fmtstr
	CALL printf
	ADDL $8, %ESP
	CALL z
	MOVL %EAX,t2
	ADDL $0, %ESP
	MOVL t2,%EAX
	MOVL %EAX,t2
	MOVL %EAX,t0
	PUSHL t0
	PUSHL $fmtstr
	CALL printf
	ADDL $8, %ESP
	MOVL $322,%EAX
	MOVL %EAX,t0
	PUSHL t0
	PUSHL $fmtstr
	CALL printf
	ADDL $8, %ESP
	MOVL t0,%EAX
	RET
	MOVL $0,%EAX
	MOVL %EAX,_empty_
z:
	MOVL $3,%EAX
	MOVL %EAX,t0
	PUSHL t0
	PUSHL $fmtstr
	CALL printf
	ADDL $8, %ESP
	MOVL $6,%EAX
	RET
	MOVL $0,%EAX
	MOVL %EAX,_empty_
g1:
	MOVL $333,%EAX
	MOVL %EAX,t0
	MOVL t0,%EAX
	RET
	MOVL $0,%EAX
