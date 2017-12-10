.globl _main
_main:
pushl %ebp
movl %esp, %ebp
subl $4, %esp

movl $0, %edi
movl $3, %edx
# trampoline _1
jmp start__1
zz_1_thenj: jmp thenlabel__1.j
zz_1_ebx: jmp *%ebx
start__1:
movl $thenlabel__1, %ebx
movl $elselabel__1, %ecx
cmp $0, %edi
cmove %ecx, %ebx
start__1.j:
jmp zz_1_thenj
thenlabel__1:
movl %edx, %edx
movl %eax, %eax
movl $3, %eax
# trampoline _2
jmp start__2
zz_2_thenj: jmp thenlabel__2.j
zz_2_ebx: jmp *%ebx
start__2:
movl $thenlabel__2, %ebx
movl $elselabel__2, %ecx
cmp $0, %edi
cmove %ecx, %ebx
start__2.j:
jmp zz_2_thenj
thenlabel__2:
movl %edx, %edx
movl %eax, %edx
movl $endlabel__2, %ebx
thenlabel__2.j:
jmp zz_2_ebx
elselabel__2:
movl %eax, %eax
movl %edx, %eax
endlabel__2:

movl $endlabel__1, %ebx
thenlabel__1.j:
jmp zz_1_ebx
elselabel__1:
movl %edi, %eax
movl %edx, %eax
endlabel__1:

movl $0, %eax
leave
ret
