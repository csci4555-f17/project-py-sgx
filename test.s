.globl _main
_main:
pushl %ebp
movl %esp, %ebp
subl $44, %esp

movl $0, -32(%ebp)
movl $3, %edi
movl -32(%ebp), %ecx
movl -32(%ebp), %ecx
movl %edi, -28(%ebp)
movl -8(%ebp), %ecx
movl -8(%ebp), %ecx
movl -32(%ebp), %eax
movl $1, %eax
movl $3, -20(%ebp)
movl -28(%ebp), %esi
movl -20(%ebp), %esi
movl -20(%ebp), %edx
movl -28(%ebp), %edx
movl -28(%ebp), %ecx
cmpl $0, %eax
cmovne %esi, %ecx
movl %ecx, -28(%ebp)
movl -20(%ebp), %ecx
cmpl $0, %eax
cmove %edx, %ecx
movl %ecx, -20(%ebp)
movl -8(%ebp), %edx
movl -32(%ebp), %ecx
movl -32(%ebp), %ecx
movl -24(%ebp), %ecx
movl -24(%ebp), %ecx
movl %edi, -12(%ebp)
movl $8, -16(%ebp)
movl -40(%ebp), %esi
movl $34, %esi
movl -40(%ebp), %edx
movl $3, %edx
movl -40(%ebp), %ecx
cmpl $0, -16(%ebp)
cmovne %esi, %ecx
movl %ecx, -40(%ebp)
movl -40(%ebp), %ecx
cmpl $0, -16(%ebp)
cmove %edx, %ecx
movl %ecx, -40(%ebp)
movl -40(%ebp), %edx
movl %edi, %ecx
cmpl $0, -44(%ebp)
cmovne -28(%ebp), %ecx
movl %ecx, %edi
movl -8(%ebp), %ecx
cmpl $0, -44(%ebp)
cmovne -20(%ebp), %ecx
movl %ecx, -8(%ebp)
movl -32(%ebp), %ecx
cmpl $0, -44(%ebp)
cmovne %eax, %ecx
movl %ecx, -32(%ebp)
movl -8(%ebp), %ecx
cmpl $0, -44(%ebp)
cmove %edx, %ecx
movl %ecx, -8(%ebp)
movl -32(%ebp), %ecx
cmpl $0, -44(%ebp)
cmove -12(%ebp), %ecx
movl %ecx, -32(%ebp)
movl -24(%ebp), %ecx
cmpl $0, -44(%ebp)
cmove -40(%ebp), %ecx
movl %ecx, -24(%ebp)
subl $8, %esp
pushl -32(%ebp)
call _print_int_nl 
addl $4, %esp
addl $8, %esp
subl $8, %esp
pushl %edi
call _print_int_nl 
addl $4, %esp
addl $8, %esp
subl $8, %esp
pushl -8(%ebp)
call _print_int_nl 
addl $4, %esp
addl $8, %esp
movl $0, %eax
leave
ret
