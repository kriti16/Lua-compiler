.section .data
"PQRST":
  .long 0
t8:
  .long 0
t9:
  .long 0
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
t0:
  .long 0
t1:
  .long 0
t14:
  .long 0
t15:
  .long 0
t16:
  .long 0
t17:
  .long 0
t10:
  .long 0
t11:
  .long 0
t12:
  .long 0
t13:
  .long 0

t3:	.ascii	"PQRST"
.section .text
inptstr:
  .asciz "%d" 
fmtstr:  .asciz "%d\n" 
strfmt:  .asciz "%s\n"

 .globl main

main:

LEE1:
	MOVL $0,%EAX
	MOVL %EAX,t0
	CALL CreateDict
	MOVL %EAX,t1
	MOVL t1,%EAX
	MOVL t3,%EBX
	PUSHL $t3
	MOVL %EAX,t1
	MOVL %EAX,t2
	MOVL %EBX,t3
	CALL createStringP
	MOVL %EAX,t4
	MOVL t4,%EAX
	MOVL %EAX,t4
	MOVL %EAX,t5
	CALL InputString
	MOVL %EAX,t6
	MOVL t6,%EAX
	PUSHL t5
	MOVL %EAX,t6
	MOVL %EAX,t7
	CALL PrintString
	MOVL %EAX,t8
	ADDL $4, %ESP
LEE5:
	MOVL t0,%EAX
	MOVL $20,%EBX
	CMP %EBX,%EAX
	MOVL %EAX,t0
	JL LEE3
LEE2:
	JMP LEE4
LEE3:
	PUSHL t0
	PUSHL t0
	PUSHL t1
	CALL insertDict
	MOVL %EAX,t1
	ADDL $12, %ESP
	PUSHL t0
	PUSHL $fmtstr
	CALL printf
	ADDL $8, %ESP
	MOVL t0,%EAX
	ADDL $1,%EAX
	MOVL %EAX,t9
	MOVL %EAX,t0
	JMP LEE5
LEE4:
	MOVL $3,%EAX
	MOVL t0,%EBX
	SUBL $3,%EBX
	PUSHL %EBX
	PUSHL t2
	MOVL %EBX,t11
	MOVL %EBX,t0
	MOVL %EAX,t10
	CALL getDict
	MOVL %EAX,t12
	ADDL $8, %ESP
	MOVL t0,%EAX
	MOVL $0,%EBX
	CMP %EBX,%EAX
	MOVL %EAX,t0
	JG LEE7
LEE6:
	JMP LEE8
LEE7:
	PUSHL t12
	PUSHL $fmtstr
	CALL printf
	ADDL $8, %ESP
	JMP LEE9
LEE8:
	MOVL t12,%EAX
	ADDL $1,%EAX
	MOVL %EAX,t13
	PUSHL t13
	PUSHL $fmtstr
	CALL printf
	ADDL $8, %ESP
LEE9:
	PUSHL t0
	PUSHL $fmtstr
	CALL printf
	ADDL $8, %ESP
	PUSHL t7
	CALL PrintString
	MOVL %EAX,t14
	ADDL $4, %ESP
	PUSHL t7
	PUSHL t5
	CALL MergeString
	MOVL %EAX,t15
	MOVL t15,%EAX
	PUSHL %EAX
	MOVL %EAX,t15
	MOVL %EAX,t16
	CALL PrintString
	MOVL %EAX,t17
	ADDL $4, %ESP
	MOVL $0,%EAX

	MOVL $1,%EAX
	MOVL $0,%EBX
int $0x80

