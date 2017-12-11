.globl _main
_main:
pushl %ebp
movl %esp, %ebp
subl $4, %esp

movl $10, %esi
jmp test_label_PYYC_TEMP_6
zz1_PYYC_TEMP_9:
jmp body_label_j_PYYC_TEMP_7
zz2_PYYC_TEMP_10:
jmp *%ebx
test_label_PYYC_TEMP_6:
movl $body_label_PYYC_TEMP_7, %ebx
movl $end_label_PYYC_TEMP_8, %ecx
cmpl $0, %esi
cmove %ecx, %ebx
jmp zz1_PYYC_TEMP_9
body_label_PYYC_TEMP_7:
movl $5, %edi
jmp test_label_PYYC_TEMP_11
zz1_PYYC_TEMP_14:
jmp body_label_j_PYYC_TEMP_12
zz2_PYYC_TEMP_15:
jmp *%ebx
test_label_PYYC_TEMP_11:
movl $body_label_PYYC_TEMP_12, %ebx
movl $end_label_PYYC_TEMP_13, %ecx
cmpl $0, %edi
cmove %ecx, %ebx
jmp zz1_PYYC_TEMP_14
body_label_PYYC_TEMP_12:
movl %esi, %eax
addl %edi, %eax
pushl %eax
call _print_int_nl 
addl $4, %esp
movl $1, %eax
negl %eax
addl %edi, %eax
movl %eax, %edi
movl $test_label_PYYC_TEMP_11, %ebx
body_label_j_PYYC_TEMP_12:
jmp zz2_PYYC_TEMP_15
end_label_PYYC_TEMP_13:

movl $1, %eax
negl %eax
addl %esi, %eax
movl %eax, %esi
movl $test_label_PYYC_TEMP_6, %ebx
body_label_j_PYYC_TEMP_7:
jmp zz2_PYYC_TEMP_10
end_label_PYYC_TEMP_8:

movl $0, %eax
leave
ret
