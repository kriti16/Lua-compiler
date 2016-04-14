.section .data
t6:
  .long 0
t4:
  .long 0
t5:
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
	MOVL $4,%EBX
	PUSHL %EAX
	MOVL %EAX,t0
	MOVL %EBX,t1
	CALL itoa
	MOVL %EAX,t2
	PUSHL t1
	CALL itoa
	MOVL %EAX,t3
	PUSHL t3
	PUSHL t2
	CALL MergeString
	MOVL %EAX,t4
	MOVL t4,%EAX
	PUSHL %EAX
	MOVL %EAX,t4
	MOVL %EAX,t5
	CALL PrintString
	MOVL %EAX,t6
	ADDL $4, %ESP
	MOVL $0,%EAX

	MOVL $1,%EAX
	MOVL $0,%EBX
int $0x80

