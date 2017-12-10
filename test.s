.globl _main
_main:
pushl %ebp
movl %esp, %ebp
subl $44, %esp

movl $0, -32(%ebp)
movl $3, %edi
movl -32(%ebp), %eax
movl %eax, -28(%ebp)
movl %edi, -24(%ebp)
movl -8(%ebp), %eax
movl %eax, %edx
movl -32(%ebp), %eax
movl %eax, %esi
movl $1, %esi
movl $3, %edx
movl -24(%ebp), %eax
movl %eax, -16(%ebp)
movl %edx, -16(%ebp)
movl %edx, %eax
movl -24(%ebp), %eax
movl -24(%ebp), %ecx
cmpl $0, %esi
cmovne -16(%ebp), %ecx
movl %ecx, -24(%ebp)
movl %edx, %ecx
cmpl $0, %esi
cmove %eax, %ecx
movl %ecx, %edx
movl -8(%ebp), %eax
movl -32(%ebp), %eax
movl %eax, -16(%ebp)
movl -20(%ebp), %eax
movl %eax, -36(%ebp)
movl %edi, -16(%ebp)
movl $8, -44(%ebp)
movl -36(%ebp), %eax
movl %eax, -40(%ebp)
movl $34, -40(%ebp)
movl -36(%ebp), %eax
movl $3, %eax
movl -36(%ebp), %ecx
cmpl $0, -44(%ebp)
cmovne -40(%ebp), %ecx
movl %ecx, -36(%ebp)
movl -36(%ebp), %ecx
cmpl $0, -44(%ebp)
cmove %eax, %ecx
movl %ecx, -36(%ebp)
movl -36(%ebp), %eax
movl %edi, %ecx
cmpl $0, -28(%ebp)
cmovne -24(%ebp), %ecx
movl %ecx, %edi
movl -8(%ebp), %ecx
cmpl $0, -28(%ebp)
cmovne %edx, %ecx
movl %ecx, -8(%ebp)
movl -32(%ebp), %ecx
cmpl $0, -28(%ebp)
cmovne %esi, %ecx
movl %ecx, -32(%ebp)
movl -8(%ebp), %ecx
cmpl $0, -28(%ebp)
cmove %eax, %ecx
movl %ecx, -8(%ebp)
movl -32(%ebp), %ecx
cmpl $0, -28(%ebp)
cmove -16(%ebp), %ecx
movl %ecx, -32(%ebp)
movl -20(%ebp), %ecx
cmpl $0, -28(%ebp)
cmove -36(%ebp), %ecx
movl %ecx, -20(%ebp)
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
