
.data

STRING238:
	.string "x"

STRING239:
	.string "DESUGAR_LIST#3"

STRING240:
	.string "DESUGAR_LIST#3"

STRING241:
	.string "DESUGAR_LIST#3"

STRING242:
	.string "DESUGAR_LIST#3"

STRING243:
	.string "l"

STRING244:
	.string "l"

STRING245:
	.string "__init__"

STRING246:
	.string "y"

STRING247:
	.string "__init__"

STRING248:
	.string "__init__"

STRING249:
	.string "__init__"

STRING250:
	.string "__init__"

STRING251:
	.string "x"

.text
_CLOSED_LAMBDA36:
pushl %ebp
movl %esp, %ebp
movl %ebx, -4(%ebp)
movl %esi, -8(%ebp)
movl %edi, -12(%ebp)
subl $12, %esp

subl $12, %esp
call _input 
addl $0, %esp
addl $12, %esp
sall $2, %eax
movl -4(%ebp), %ebx
movl -8(%ebp), %esi
movl -12(%ebp), %edi
leave 
ret 
_CLOSED_LAMBDA39:
pushl %ebp
movl %esp, %ebp
movl %ebx, -4(%ebp)
movl %esi, -8(%ebp)
movl %edi, -12(%ebp)
subl $12, %esp

movl $5, %eax
sall $2, %eax
movl -4(%ebp), %ebx
movl -8(%ebp), %esi
movl -12(%ebp), %edi
leave 
ret 
_CLOSED_LAMBDA42:
pushl %ebp
movl %esp, %ebp
movl %ebx, -4(%ebp)
movl %esi, -8(%ebp)
movl %edi, -12(%ebp)
subl $12, %esp

pushl 16(%ebp)
pushl $STRING238
pushl 12(%ebp)
call _set_attr 
addl $12, %esp
movl $0, %eax
movl -4(%ebp), %ebx
movl -8(%ebp), %esi
movl -12(%ebp), %edi
leave 
ret 
.globl _main
_main:
pushl %ebp
movl %esp, %ebp
subl $8, %esp

movl $0, %eax
sall $2, %eax
subl $12, %esp
pushl %eax
call _create_list 
addl $4, %esp
addl $12, %esp
orl $3, %eax
subl $8, %esp
pushl %eax
pushl $_CLOSED_LAMBDA36
call _create_closure 
addl $8, %esp
addl $8, %esp
orl $3, %eax
movl $1, %eax
sall $2, %eax
orl $1, %eax
movl $0, %eax
sall $2, %eax
orl $1, %eax
movl $1, %eax
sall $2, %eax
subl $12, %esp
pushl %eax
call _create_list 
addl $4, %esp
addl $12, %esp
orl $3, %eax
movl %eax, %edi
movl $0, %eax
sall $2, %eax
movl $1, %edx
sall $2, %edx
subl $4, %esp
pushl %edx
pushl %eax
pushl %edi
call _set_subscript 
addl $12, %esp
addl $4, %esp
movl %edi, %eax
movl %eax, %ebx
movl $0, %eax
sall $2, %eax
subl $12, %esp
pushl %eax
call _create_list 
addl $4, %esp
addl $12, %esp
orl $3, %eax
subl $12, %esp
pushl %eax
call _create_class 
addl $4, %esp
addl $12, %esp
orl $3, %eax
movl %eax, %edi
movl $1, %eax
sall $2, %eax
subl $12, %esp
pushl %eax
call _create_list 
addl $4, %esp
addl $12, %esp
orl $3, %eax
movl %eax, %esi
subl $8, %esp
pushl $STRING239
pushl %edi
call _has_attr 
addl $8, %esp
addl $8, %esp
sall $2, %eax
orl $1, %eax
movl %eax, %edx
movl %edx, %ecx
andl $3, %ecx
movl $0, %eax
cmpl %ecx, %eax
sete %cl 
movzbl %cl, %eax

cmpl $0, %eax
je iflabel_else253
movl $1, -8(%ebp)
jmp iflabel_end254
iflabel_else253:
movl %edx, %ecx
andl $3, %ecx
movl $1, %eax
cmpl %ecx, %eax
sete %cl 
movzbl %cl, %eax

cmpl $0, %eax
je iflabel_else255
movl $1, -8(%ebp)
jmp iflabel_end256
iflabel_else255:
movl $0, -8(%ebp)
iflabel_end256:

movl -8(%ebp), %eax
movl %eax, -8(%ebp)
iflabel_end254:


cmpl $0, -8(%ebp)
je iflabel_else257
movl %edx, %eax
sarl $2, %eax
movl %eax, %edx
jmp iflabel_end258
iflabel_else257:
subl $12, %esp
pushl %edx
call _is_true 
addl $4, %esp
addl $12, %esp
movl %eax, %eax
movl %eax, %eax
sall $2, %eax
orl $1, %eax
movl %eax, %eax
sarl $2, %eax
movl %eax, %edx
iflabel_end258:


cmpl $0, %edx
je iflabel_else259
subl $8, %esp
pushl $STRING240
pushl %edi
call _get_attr 
addl $8, %esp
addl $8, %esp
movl %eax, %eax
movl %eax, %edx
jmp iflabel_end260
iflabel_else259:
movl %esi, %edx
iflabel_end260:

movl $0, %eax
sall $2, %eax
movl $4, %ecx
sall $2, %ecx
subl $4, %esp
pushl %ecx
pushl %eax
pushl %edx
call _set_subscript 
addl $12, %esp
addl $4, %esp
subl $8, %esp
pushl $STRING241
pushl %edi
call _has_attr 
addl $8, %esp
addl $8, %esp
sall $2, %eax
orl $1, %eax
movl %eax, -8(%ebp)
movl -8(%ebp), %edx
andl $3, %edx
movl $0, %eax
cmpl %edx, %eax
sete %cl 
movzbl %cl, %eax

cmpl $0, %eax
je iflabel_else261
movl $1, %edx
jmp iflabel_end262
iflabel_else261:
movl -8(%ebp), %edx
andl $3, %edx
movl $1, %eax
cmpl %edx, %eax
sete %cl 
movzbl %cl, %eax

cmpl $0, %eax
je iflabel_else263
movl $1, %edx
jmp iflabel_end264
iflabel_else263:
movl $0, %edx
iflabel_end264:

movl %edx, %edx
iflabel_end262:


cmpl $0, %edx
je iflabel_else265
movl -8(%ebp), %eax
sarl $2, %eax
movl %eax, %edx
jmp iflabel_end266
iflabel_else265:
subl $12, %esp
pushl -8(%ebp)
call _is_true 
addl $4, %esp
addl $12, %esp
movl %eax, %eax
movl %eax, %eax
sall $2, %eax
orl $1, %eax
movl %eax, %eax
sarl $2, %eax
movl %eax, %edx
iflabel_end266:


cmpl $0, %edx
je iflabel_else267
subl $8, %esp
pushl $STRING242
pushl %edi
call _get_attr 
addl $8, %esp
addl $8, %esp
movl %eax, %eax
movl %eax, %edx
jmp iflabel_end268
iflabel_else267:
movl %esi, %edx
iflabel_end268:

movl %edx, %eax
subl $4, %esp
pushl %eax
pushl $STRING243
pushl %edi
call _set_attr 
addl $12, %esp
addl $4, %esp
subl $12, %esp
pushl %ebx
call _print_any 
addl $4, %esp
addl $12, %esp
subl $8, %esp
pushl $STRING244
pushl %edi
call _get_attr 
addl $8, %esp
addl $8, %esp
subl $12, %esp
pushl %eax
call _print_any 
addl $4, %esp
addl $12, %esp
movl $0, %eax
sall $2, %eax
subl $12, %esp
pushl %eax
call _create_list 
addl $4, %esp
addl $12, %esp
orl $3, %eax
subl $8, %esp
pushl %eax
pushl $_CLOSED_LAMBDA39
call _create_closure 
addl $8, %esp
addl $8, %esp
orl $3, %eax
movl %eax, %edi
movl $0, %eax
sall $2, %eax
subl $12, %esp
pushl %eax
call _create_list 
addl $4, %esp
addl $12, %esp
orl $3, %eax
subl $12, %esp
pushl %eax
call _create_class 
addl $4, %esp
addl $12, %esp
orl $3, %eax
movl %eax, %ebx
movl $1, %eax
sall $2, %eax
subl $12, %esp
pushl %eax
call _create_list 
addl $4, %esp
addl $12, %esp
orl $3, %eax
movl %eax, %esi
movl $0, %eax
sall $2, %eax
subl $4, %esp
pushl %ebx
pushl %eax
pushl %esi
call _set_subscript 
addl $12, %esp
addl $4, %esp
movl %esi, %eax
subl $12, %esp
pushl %eax
call _create_class 
addl $4, %esp
addl $12, %esp
orl $3, %eax
movl %eax, %ebx
movl $0, %eax
sall $2, %eax
subl $12, %esp
pushl %eax
call _create_list 
addl $4, %esp
addl $12, %esp
orl $3, %eax
subl $8, %esp
pushl %eax
pushl $_CLOSED_LAMBDA42
call _create_closure 
addl $8, %esp
addl $8, %esp
orl $3, %eax
subl $4, %esp
pushl %eax
pushl $STRING245
pushl %ebx
call _set_attr 
addl $12, %esp
addl $4, %esp
movl $1, %eax
sall $2, %eax
subl $4, %esp
pushl %eax
pushl $STRING246
pushl %ebx
call _set_attr 
addl $12, %esp
addl $4, %esp
movl %ebx, %esi
subl $12, %esp
pushl %edi
call _is_class 
addl $4, %esp
addl $12, %esp
sall $2, %eax
orl $1, %eax
sarl $2, %eax

cmpl $0, %eax
je iflabel_else269
subl $12, %esp
pushl %edi
call _create_object 
addl $4, %esp
addl $12, %esp
movl %eax, %eax
movl %eax, %eax
orl $3, %eax
movl %eax, %ebx
subl $8, %esp
pushl $STRING247
pushl %edi
call _has_attr 
addl $8, %esp
addl $8, %esp
movl %eax, %eax
movl %eax, %eax
sall $2, %eax
orl $1, %eax
movl %eax, %eax
sarl $2, %eax

cmpl $0, %eax
je iflabel_else271
subl $8, %esp
pushl $STRING248
pushl %edi
call _get_attr 
addl $8, %esp
addl $8, %esp
movl %eax, %eax
subl $12, %esp
pushl %eax
call _get_function 
addl $4, %esp
addl $12, %esp
movl %eax, %eax
movl %eax, %eax
orl $3, %eax
movl %eax, -8(%ebp)
subl $12, %esp
pushl -8(%ebp)
call _get_fun_ptr 
addl $4, %esp
addl $12, %esp
movl %eax, %edi
subl $12, %esp
pushl -8(%ebp)
call _get_free_vars 
addl $4, %esp
addl $12, %esp
movl %eax, %eax
subl $8, %esp
pushl %ebx
pushl %eax
call * %edi
addl $8, %esp
addl $8, %esp
movl %eax, %eax
movl %ebx, %eax
movl %eax, %eax
movl %eax, %edx
jmp iflabel_end272
iflabel_else271:
movl %ebx, %edx
iflabel_end272:

movl %edx, %edx
jmp iflabel_end270
iflabel_else269:
subl $12, %esp
pushl %edi
call _is_bound_method 
addl $4, %esp
addl $12, %esp
movl %eax, %eax
movl %eax, %eax
sall $2, %eax
orl $1, %eax
movl %eax, %eax
sarl $2, %eax

cmpl $0, %eax
je iflabel_else273
subl $12, %esp
pushl %edi
call _get_function 
addl $4, %esp
addl $12, %esp
movl %eax, %eax
movl %eax, %eax
orl $3, %eax
movl %eax, -8(%ebp)
subl $12, %esp
pushl -8(%ebp)
call _get_fun_ptr 
addl $4, %esp
addl $12, %esp
movl %eax, %ebx
subl $12, %esp
pushl -8(%ebp)
call _get_free_vars 
addl $4, %esp
addl $12, %esp
movl %eax, -8(%ebp)
subl $12, %esp
pushl %edi
call _get_receiver 
addl $4, %esp
addl $12, %esp
movl %eax, %eax
movl %eax, %eax
orl $3, %eax
subl $8, %esp
pushl %eax
pushl -8(%ebp)
call * %ebx
addl $8, %esp
addl $8, %esp
movl %eax, %eax
movl %eax, %edx
jmp iflabel_end274
iflabel_else273:
subl $12, %esp
pushl %edi
call _is_unbound_method 
addl $4, %esp
addl $12, %esp
movl %eax, %eax
movl %eax, %eax
sall $2, %eax
orl $1, %eax
movl %eax, %eax
sarl $2, %eax

cmpl $0, %eax
je iflabel_else275
subl $12, %esp
pushl %edi
call _get_function 
addl $4, %esp
addl $12, %esp
movl %eax, %eax
movl %eax, %eax
orl $3, %eax
movl %eax, %edi
subl $12, %esp
pushl %edi
call _get_fun_ptr 
addl $4, %esp
addl $12, %esp
movl %eax, %ebx
subl $12, %esp
pushl %edi
call _get_free_vars 
addl $4, %esp
addl $12, %esp
movl %eax, %eax
subl $12, %esp
pushl %eax
call * %ebx
addl $4, %esp
addl $12, %esp
movl %eax, %eax
movl %eax, %edx
jmp iflabel_end276
iflabel_else275:
movl %edi, %edi
subl $12, %esp
pushl %edi
call _get_fun_ptr 
addl $4, %esp
addl $12, %esp
movl %eax, %ebx
subl $12, %esp
pushl %edi
call _get_free_vars 
addl $4, %esp
addl $12, %esp
movl %eax, %eax
subl $12, %esp
pushl %eax
call * %ebx
addl $4, %esp
addl $12, %esp
movl %eax, %eax
movl %eax, %edx
iflabel_end276:

movl %edx, %edx
iflabel_end274:

movl %edx, %edx
iflabel_end270:

movl %edx, %edi
subl $12, %esp
pushl %esi
call _is_class 
addl $4, %esp
addl $12, %esp
sall $2, %eax
orl $1, %eax
sarl $2, %eax

cmpl $0, %eax
je iflabel_else277
subl $12, %esp
pushl %esi
call _create_object 
addl $4, %esp
addl $12, %esp
movl %eax, %eax
movl %eax, %eax
orl $3, %eax
movl %eax, %ebx
subl $8, %esp
pushl $STRING249
pushl %esi
call _has_attr 
addl $8, %esp
addl $8, %esp
movl %eax, %eax
movl %eax, %eax
sall $2, %eax
orl $1, %eax
movl %eax, %eax
sarl $2, %eax

cmpl $0, %eax
je iflabel_else279
subl $8, %esp
pushl $STRING250
pushl %esi
call _get_attr 
addl $8, %esp
addl $8, %esp
movl %eax, %eax
subl $12, %esp
pushl %eax
call _get_function 
addl $4, %esp
addl $12, %esp
movl %eax, %eax
movl %eax, %eax
orl $3, %eax
movl %eax, -8(%ebp)
subl $12, %esp
pushl -8(%ebp)
call _get_fun_ptr 
addl $4, %esp
addl $12, %esp
movl %eax, %esi
subl $12, %esp
pushl -8(%ebp)
call _get_free_vars 
addl $4, %esp
addl $12, %esp
movl %eax, %edx
movl $1, %eax
sall $2, %eax
subl $4, %esp
pushl %eax
pushl %ebx
pushl %edx
call * %esi
addl $12, %esp
addl $4, %esp
movl %eax, %eax
movl %ebx, %eax
movl %eax, %eax
movl %eax, %edx
jmp iflabel_end280
iflabel_else279:
movl %ebx, %edx
iflabel_end280:

movl %edx, %edx
jmp iflabel_end278
iflabel_else277:
subl $12, %esp
pushl %esi
call _is_bound_method 
addl $4, %esp
addl $12, %esp
movl %eax, %eax
movl %eax, %eax
sall $2, %eax
orl $1, %eax
movl %eax, %eax
sarl $2, %eax

cmpl $0, %eax
je iflabel_else281
subl $12, %esp
pushl %esi
call _get_function 
addl $4, %esp
addl $12, %esp
movl %eax, %eax
movl %eax, %eax
orl $3, %eax
movl %eax, -8(%ebp)
subl $12, %esp
pushl -8(%ebp)
call _get_fun_ptr 
addl $4, %esp
addl $12, %esp
movl %eax, %ebx
subl $12, %esp
pushl -8(%ebp)
call _get_free_vars 
addl $4, %esp
addl $12, %esp
movl %eax, -8(%ebp)
subl $12, %esp
pushl %esi
call _get_receiver 
addl $4, %esp
addl $12, %esp
movl %eax, %eax
movl %eax, %eax
orl $3, %eax
movl $1, %edx
sall $2, %edx
subl $4, %esp
pushl %edx
pushl %eax
pushl -8(%ebp)
call * %ebx
addl $12, %esp
addl $4, %esp
movl %eax, %eax
movl %eax, %edx
jmp iflabel_end282
iflabel_else281:
subl $12, %esp
pushl %esi
call _is_unbound_method 
addl $4, %esp
addl $12, %esp
movl %eax, %eax
movl %eax, %eax
sall $2, %eax
orl $1, %eax
movl %eax, %eax
sarl $2, %eax

cmpl $0, %eax
je iflabel_else283
subl $12, %esp
pushl %esi
call _get_function 
addl $4, %esp
addl $12, %esp
movl %eax, %eax
movl %eax, %eax
orl $3, %eax
movl %eax, %ebx
subl $12, %esp
pushl %ebx
call _get_fun_ptr 
addl $4, %esp
addl $12, %esp
movl %eax, %esi
subl $12, %esp
pushl %ebx
call _get_free_vars 
addl $4, %esp
addl $12, %esp
movl %eax, %eax
movl $1, %edx
sall $2, %edx
subl $8, %esp
pushl %edx
pushl %eax
call * %esi
addl $8, %esp
addl $8, %esp
movl %eax, %eax
movl %eax, %edx
jmp iflabel_end284
iflabel_else283:
movl %esi, %esi
subl $12, %esp
pushl %esi
call _get_fun_ptr 
addl $4, %esp
addl $12, %esp
movl %eax, %ebx
subl $12, %esp
pushl %esi
call _get_free_vars 
addl $4, %esp
addl $12, %esp
movl %eax, %eax
movl $1, %edx
sall $2, %edx
subl $8, %esp
pushl %edx
pushl %eax
call * %ebx
addl $8, %esp
addl $8, %esp
movl %eax, %eax
movl %eax, %edx
iflabel_end284:

movl %edx, %edx
iflabel_end282:

movl %edx, %edx
iflabel_end278:

subl $8, %esp
pushl $STRING251
pushl %edx
call _get_attr 
addl $8, %esp
addl $8, %esp
movl %eax, %edx
movl %edi, %ebx
andl $3, %ebx
movl $0, %eax
cmpl %ebx, %eax
sete %cl 
movzbl %cl, %eax

cmpl $0, %eax
je iflabel_else285
movl $1, %ebx
jmp iflabel_end286
iflabel_else285:
movl %edi, %ebx
andl $3, %ebx
movl $1, %eax
cmpl %ebx, %eax
sete %cl 
movzbl %cl, %eax

cmpl $0, %eax
je iflabel_else287
movl $1, %ebx
jmp iflabel_end288
iflabel_else287:
movl $0, %ebx
iflabel_end288:

movl %ebx, %ebx
iflabel_end286:


cmpl $0, %ebx
je iflabel_else289
movl %edi, %eax
sarl $2, %eax
movl %edx, %edx
sarl $2, %edx
movl %edx, %edx
addl %eax, %edx
movl %edx, %edx
movl %edx, %eax
sall $2, %eax
movl %eax, %edx
jmp iflabel_end290
iflabel_else289:
movl %edi, %eax
andl $0xfffffffc, %eax
movl %edx, %edx
andl $0xfffffffc, %edx
subl $8, %esp
pushl %edx
pushl %eax
call _add 
addl $8, %esp
addl $8, %esp
movl %eax, %eax
movl %eax, %eax
orl $3, %eax
movl %eax, %edx
iflabel_end290:

subl $12, %esp
pushl %edx
call _print_any 
addl $4, %esp
addl $12, %esp
movl $0, %eax
leave 
ret 
