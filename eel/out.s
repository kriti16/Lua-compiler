.section .data
t6:
  .long 0
t7:
  .long 0
t4:
  .long 0
t5:
  .long 0
t2:
  .long 0
t3:
  .long 0
t1:
  .long 0
3:
  .long 0
5:
  .long 0
y:
  .long 0
8:
  .long 0
_empty_:
  .long 0

t0:	.ascii	"sdds"
.section .text
inptstr:
  .asciz "%d" 
fmtstr:  .asciz "%d\n" 
strfmt:  .asciz "%s\n"

 .globl main

main:

LEE1:
LEE1:
	PUSHL $t0
	CALL createStringP
	MOVL %EAX,t1
	CALL CreateDict
	MOVL %EAX,t2
	PUSHL $8
	PUSHL t1
	PUSHL t2
	CALL insertDict
	MOVL %EAX,t2
	ADDL $12, %ESP
	PUSHL $5
	CALL itoa
	MOVL %EAX,t3
	PUSHL $3
	PUSHL t3
	PUSHL t2
	CALL insertDict
	MOVL %EAX,t2
	ADDL $12, %ESP
	MOVL t2,%EAX
	PUSHL $t0
	MOVL %EAX,t2
	MOVL %EAX,t4
	CALL createStringP
	MOVL %EAX,t6
	PUSHL t6
	PUSHL t4
	CALL getDict
	MOVL %EAX,y
	ADDL $8, %ESP
	PUSHL y
	PUSHL $fmtstr
	CALL printf
	ADDL $8, %ESP
	PUSHL $5
	CALL itoa
	MOVL %EAX,t7
	PUSHL t7
	PUSHL t4
	CALL getDict
	MOVL %EAX,y
	ADDL $8, %ESP
	PUSHL y
	PUSHL $fmtstr
	CALL printf
	ADDL $8, %ESP
	MOVL $0,%EAX

	MOVL $1,%EAX
	MOVL $0,%EBX
int $0x80

