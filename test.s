.globl _main
_main:
pushl %ebp
movl %esp, %ebp
subl $4, %esp

movl $10, %edi

PYYC_TEMP_5:
cmpl $0, %edi
je PYYC_TEMP_6
pushl %edi
call _print_int_nl 
addl $4, %esp
movl $1, %eax
negl %eax
addl %edi, %eax
movl %eax, %edi
movl $2, %eax
movl $4, %eax
negl %eax
addl %edi, %eax
# trampoline 7
jmp start_7
zz7_thenj: jmp thenlabel_7.j
zz7_ebx: jmp *%ebx
start_7:
movl $thenlabel_7, %ebx
movl $elselabel_7, %ecx
cmp $0, %eax
cmove %ecx, %ebx
start_7.j:
jmp zz7_thenj
thenlabel_7:
movl $0, %edx
movl $endlabel_7, %ebx
thenlabel_7.j:
jmp zz7_ebx
elselabel_7:
movl $1, %edx
endlabel_7:

# trampoline 8
jmp start_8
zz8_thenj: jmp thenlabel_8.j
zz8_ebx: jmp *%ebx
start_8:
movl $thenlabel_8, %ebx
movl $elselabel_8, %ecx
cmp $0, %edx
cmove %ecx, %ebx
start_8.j:
jmp zz8_thenj
thenlabel_8:
pushl %edi
call _print_int_nl 
addl $4, %esp
movl $endlabel_8, %ebx
thenlabel_8.j:
jmp zz8_ebx
elselabel_8:
pushl $987
call _print_int_nl 
addl $4, %esp
endlabel_8:

jmp PYYC_TEMP_5
PYYC_TEMP_6:

movl $0, %eax
leave
ret
