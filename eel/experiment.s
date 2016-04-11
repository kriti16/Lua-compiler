.section .data
.section .text
outstr:
    .asciz "%u"

 .globl main

main:
pushl $10
pushl $15
    call subtract

addl $8, %esp    

pushl $15
pushl %eax
    call get

addl $8, %esp    

 
pushl %eax
pushl $outstr 
call printf
pushl $0
call exit
