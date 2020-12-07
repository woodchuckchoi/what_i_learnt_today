global _start

section .text
_start:
	mov ecx, 100
	mov ebx, 42
	mov eax, 1
	cmp ecx, 100
	jl skip
	mov ebx, 13 ; if ecx is less than 100, this line is skipped
skip:
	int 0x80
