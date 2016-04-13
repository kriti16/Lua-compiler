.section .data
t2:
  .long 0
t3:
  .long 0
t0:
  .long 0
t1:
  .long 0
3:
  .long 0
2:
  .long 0
y:
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
	CALL CreateDict
	MOVL %EAX,t0
	MOVL t0,%EAX
	PUSHL $2
	MOVL %EAX,t0
	MOVL %EAX,t1
	CALL itoa
	MOVL %EAX,t2
	PUSHL $3
	PUSHL t2
	PUSHL t1
	CALL insertDict
	MOVL %EAX,t1
	ADDL $12, %ESP
	PUSHL $2
	CALL itoa
	MOVL %EAX,t3
	PUSHL t3
	PUSHL t1
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

